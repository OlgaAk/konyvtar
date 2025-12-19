from flask import Blueprint, render_template, redirect, request
import os
import cache
import repository
from models.Book import Book
from schemas.BookDTO import BookDTO
import scrape
from dummydata import get_dummy_books
from compare import compare_books

mode = os.getenv('APP_ENV', 'production')
print(mode)

main_bp = Blueprint("main", __name__)

@main_bp.route('/')
def index():
    return redirect('/status')

# def get_books() -> list[BookDTO]:
#     chached_books = load_from_cache()
#     books = []
    # if (mode == 'test'):
    #     books = scape_dummy()
    #     print('Running in test mode')
    # else:
    #     books = scrape()
    # save_to_cache(books)
    # compare_books(books, chached_books)
    # return books

def scape_dummy(): 
    return get_dummy_books()


@main_bp.route("/books")
def books():
    books = repository.get_books()
    return render_template('books.html', book_list=books)

@main_bp.route("/status")
def status():
    cached_books_with_statuses = cache.load_from_cache()
    if cached_books_with_statuses:
        print("Loaded books from cache")
        return render_template('status.html', items=cached_books_with_statuses)
    
    books = repository.get_books()
    books_with_statuses = scrape.scrape_statuses_for_books(books)
    cache.save_to_cache(books_with_statuses)
    print("Loaded books from internet")
    return render_template('status.html', items=books_with_statuses)

@main_bp.route("/refresh")
def refresh():
    cache.delete_cache()
    return redirect("/status")


@main_bp.route("/add",  methods=["POST"])
def add_book():
    book_id: str = request.form.get("book_id")
    book: BookDTO = scrape.scrape_book(book_id)
    if not book:
        return redirect("/books")
  
    repository.add_book(Book.from_dto(book))
    books: list[Book] = repository.get_books()
    return render_template('books.html', book_list=books)


@main_bp.route("/delete/<int:book_library_id>")
def delete_book(book_library_id: str):
    repository.remove_book(book_library_id)
    books: list[Book] = repository.get_books()
    return render_template('books.html', book_list=books)