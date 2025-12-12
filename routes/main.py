from flask import Blueprint, render_template
import os
from cache import load_from_cache, save_to_cache
from db import db
from models.Book import Book
from schemas.BookDTO import BookDTO
from scrape import scrape
from dummydata import get_dummy_books
from compare import compare_books

mode = os.getenv('APP_ENV', 'production')
print(mode)

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    #books = get_books()
    print(os.path.abspath("data.db"))
    book = Book(library_id = "1415431", 
                title = "Dummy Book2 some name lorem ipsum lorem ipsum", 
                author = "Dummy Author2", year = "2022", 
                shelf_number = "B 42")
    #db.session.add(book)
    #db.session.commit()
    books = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
    return render_template('index.html', items=books)

def get_books() -> list[BookDTO]:
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

def scape_dummy(): 
    return get_dummy_books()


@main_bp.route("/books")
def books():
    return render_template("books.html")

@main_bp.route("/status")
def status():
    books = db.session.execute(db.select(Book).order_by(Book.title)).scalars()
    return render_template('status.html', items=books)