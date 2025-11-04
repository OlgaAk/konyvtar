from flask import Flask, render_template
import requests, re
from bs4 import BeautifulSoup


app = Flask(__name__)

library_url = "https://saman.fszek.hu/WebPac/CorvinaWeb?action=onelong&showtype=longlong&recnum=1415430"
library1 = "Sárkányos Gyerekkönyvtár"
library2 = "Boráros tér"


@app.route('/')
def index():
    # books = scrape()
    books = scape_dummy()
    return render_template('index.html', items=books)

def scape_dummy(): 
    return [{'address': 'KK Sárkányos Gyerekkönyvtár, 1. szint', 'status': 'Lejár: 2025.11.06.'}, {'address': 'KK Sárkányos Gyerekkönyvtár, 1. szint', 'status': 'Lejár: 2025.11.08.'}, {'address': 'KK Sárkányos Gyerekkönyvtár, 1. szint', 'status': 'Lejár: 2025.12.01.'}]

def scrape():
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
        books.append({"address": td.text, "status": sibling_td})

    return books

    
if __name__ == '__main__':

    app.run()