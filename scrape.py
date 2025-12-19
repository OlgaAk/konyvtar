import requests, re
from bs4 import BeautifulSoup
from models.Book import Book
from schemas.BookDTO import BookDTO
from schemas.PrintedBookDTO import PrintedBookDTO

library_url = "https://saman.fszek.hu/WebPac/CorvinaWeb?action=onelong&showtype=longlong&recnum="
library1 = "Sárkányos Gyerekkönyvtár"
library2 = "Boráros tér"

book_urls = ["1415430", "1435665", "1413839", "1413840"]

def scrape() -> list[BookDTO]:
    books = []
    for book_id in book_urls:
        book = scrape_book_with_statuses(book_id)
        books.append(book)
    return books


def scrape_book_with_statuses(book_id: str) -> BookDTO:
    soup = get_soup(book_id)
    if not soup:
        return None

    book = scrape_book_details(soup, book_id)
    printed_book_statuses = scrape_statuses_with_soup(soup)
    book.printed_books = printed_book_statuses

    return book


def scrape_book_details(soup: BeautifulSoup, book_id: str) -> BookDTO:
    title = soup.find_all('td', string=re.compile("Cím:"))[0].findNext('td').text
    author = soup.find_all('td', string=re.compile("Szerző:"))[0].findNext('td').text
    year = soup.find_all('td', string=re.compile("Megjelenés éve:"))[0].findNext('td').text
    shelf_number = soup.find_all('td', string=re.compile("Cutter:"))[0].findNext('td').text
    book = BookDTO(book_id, title, author, year, shelf_number, [])
    return book


def scrape_statuses_for_books(books: list[Book]) -> list[BookDTO]:
    books_with_statuses: list[BookDTO] = []
    for book in books:
        book_with_statuses: BookDTO = book.to_dto()
        book_with_statuses.printed_books = scrape_statuses_with_soup(get_soup(book.library_id))
        books_with_statuses.append(book_with_statuses)
    return books_with_statuses

def scrape_statuses_with_soup(soup: BeautifulSoup) -> list[PrintedBookDTO]:
    printed_books = []
    target_tds = soup.find_all('td', string=re.compile("Sárkányos Gyerekkönyvtár|Boráros tér"))

    for td in target_tds:
        parent_tr = td.find_parent('tr')
        sibling_tds = parent_tr.find_all('td')
        sibling_td =  sibling_tds[7].text
        printed_book = PrintedBookDTO(sibling_td, td.text)
        printed_books.append(printed_book)

    return sorted(printed_books, key=lambda x: x.status)


def get_soup(book_id: str) -> BeautifulSoup:
    url = library_url + book_id
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching book details:", e)
        return None

    return BeautifulSoup(response.text, 'html.parser')