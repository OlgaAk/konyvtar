from flask import Flask, flash, redirect, render_template, request, session, url_for
import os
from models.Book import Book
import database
from scrape import scrape
from dummydata import get_dummy_books
from compare import compare_books

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecret")
mode = os.getenv('APP_ENV', 'production')
print(mode)
database.initialize()

@app.route('/')
def index():
    books = database.list_books()
    if not database.is_initialized():
        books = load_initial_books()
        database.replace_books(books)
    compare_books(books, load_from_cache())
    save_to_cache(books)
    return render_template('index.html', items=books)

@app.route('/books', methods=['POST'])
def create_book():
    book_id = request.form.get('id', '').strip()
    name = request.form.get('name', '').strip()
    author = request.form.get('author', '').strip()
    if not book_id or not name or not author:
        flash('Book ID, title, and author are required.')
        return redirect(url_for('index'))

    book = Book(
        book_id,
        name,
        author,
        request.form.get('year', '').strip(),
        request.form.get('shelf_number', '').strip(),
        [],
    )
    if database.get_book(book_id):
        flash('A book with that ID already exists.')
        return redirect(url_for('index'))
    database.create_book(book)
    flash('Book added.')
    return redirect(url_for('index'))

@app.route('/books/<book_id>/edit', methods=['POST'])
def edit_book(book_id: str):
    name = request.form.get('name', '').strip()
    author = request.form.get('author', '').strip()
    if not name or not author:
        flash('Title and author are required.')
        return redirect(url_for('index'))

    book = database.get_book(book_id)
    if book is None:
        flash('Book not found.')
        return redirect(url_for('index'))
    book.name = name
    book.author = author
    book.year = request.form.get('year', '').strip()
    book.shelf_number = request.form.get('shelf_number', '').strip()
    database.update_book(book)
    flash('Book updated.')
    return redirect(url_for('index'))

@app.route('/books/<book_id>/delete', methods=['POST'])
def delete_book(book_id: str):
    if not database.delete_book(book_id):
        flash('Book not found.')
        return redirect(url_for('index'))
    flash('Book deleted.')
    return redirect(url_for('index'))

@app.route('/reload', methods=['POST'])
def reload_books():
    books = load_initial_books()
    compare_books(books, load_from_cache())
    database.replace_books(books)
    save_to_cache(books)
    flash('Books reloaded from the catalog.')
    return redirect(url_for('index'))

def load_initial_books() -> list[Book]:
    if mode == 'test':
        return scape_dummy()
    return scrape()

def save_to_cache(books: list[Book]):
    session['books'] = [b.to_dict() for b in books]

def load_from_cache()-> list[Book]:
    stored_books = session.get('books', [])
    books = [Book.from_dict(b) for b in stored_books]
    return books

def scape_dummy():
    return get_dummy_books()
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
