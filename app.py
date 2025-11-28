from flask import Flask, render_template, session
import os
from models.Book import Book
from scrape import scrape
from dummydata import get_dummy_books
from compare import compare_books

app = Flask(__name__)
app.secret_key = "supersecret"
mode = os.getenv('APP_ENV', 'test')
print(mode)

@app.route('/')
def index():
    books = get_books()
    return render_template('index.html', items=books)

def get_books() -> list[Book]:
    chached_books = load_from_cache()
    books = []
    if (mode == 'test'):
        books = scape_dummy()
        print('Running in test mode')
    else:
        books = scrape()
    save_to_cache(books)
    compare_books(books, chached_books)
    return books

def save_to_cache(books: list[Book]):
    session['books'] = [b.to_dict() for b in books]

def load_from_cache()-> list[Book]:
    stored_books = session.get('books', []);
    books = [Book.from_dict(b) for b in stored_books] 
    return books

def scape_dummy(): 
    return get_dummy_books()
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

