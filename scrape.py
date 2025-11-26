import requests, re
from bs4 import BeautifulSoup
from models.PrintedBook import PrintedBook

library_url = "https://saman.fszek.hu/WebPac/CorvinaWeb?action=onelong&showtype=longlong&recnum=1415430"
library1 = "Sárkányos Gyerekkönyvtár"
library2 = "Boráros tér"

def scrape() -> list[PrintedBook]:
    url = library_url
    response = requests.get(url)

    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    books = []

    target_tds = soup.find_all('td', string=re.compile("Sárkányos Gyerekkönyvtár|Boráros tér"))

    for td in target_tds:
        parent_tr = td.find_parent('tr')
        sibling_tds = parent_tr.find_all('td')
        sibling_td =  sibling_tds[7].text
        book = PrintedBook(sibling_td, td.text)
        books.append(book)

    return books