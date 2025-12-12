import requests, re
from bs4 import BeautifulSoup
from schemas.BookDTO import BookDTO
from schemas.PrintedBookDTO import PrintedBookDTO

library_url = "https://saman.fszek.hu/WebPac/CorvinaWeb?action=onelong&showtype=longlong&recnum="
library1 = "Sárkányos Gyerekkönyvtár"
library2 = "Boráros tér"

book_urls = ["1415430", "1435665", "1413839", "1413840"]

def scrape() -> list[BookDTO]:
    books = []
    for book_id in book_urls:
        book = scrape_book(book_id)
        books.append(book)
    return books


def scrape_book(book_id: str) -> BookDTO:
    url = library_url + book_id
    response = requests.get(url)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    name = soup.find_all('td', string=re.compile("Cím:"))[0].findNext('td').text
    author = soup.find_all('td', string=re.compile("Szerző:"))[0].findNext('td').text
    year = soup.find_all('td', string=re.compile("Megjelenés éve:"))[0].findNext('td').text
    shelf_number = soup.find_all('td', string=re.compile("Cutter:"))[0].findNext('td').text
    book = Book(book_id, name, author, year, shelf_number, [])

    target_tds = soup.find_all('td', string=re.compile("Sárkányos Gyerekkönyvtár|Boráros tér"))

    for td in target_tds:
        parent_tr = td.find_parent('tr')
        sibling_tds = parent_tr.find_all('td')
        sibling_td =  sibling_tds[7].text
        printed_book = PrintedBookDTO(sibling_td, td.text)
        book.printed_books.append(printed_book)
    
    book.printed_books.sort(key=lambda x: x.status)
    return book