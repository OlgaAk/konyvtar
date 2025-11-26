from flask import Flask, render_template, session, redirect
import os
from models.Book import Book
from scrape import scrape
from dummydata import get_dummy_books

app = Flask(__name__)
app.secret_key = "supersecret"
mode = os.getenv('APP_ENV', 'production')
print(mode)

@app.route('/')
def index():
    books = get_books()
    return render_template('index.html', items=books)

def get_books() -> list[Book]:
    books = load_from_cache()
    if (not books):
        if (mode == 'test'):
            books = scape_dummy()
            print('Running in test mode')
        else:
            books = scrape()
    books.sort(key=lambda x: x.status)
    save_to_cache(books)
    check_status_change(books)
    return books

def save_to_cache(books: list[Book]):
    session['books'] = [b.to_dict() for b in books]

def load_from_cache()-> list[Book]:
    stored_books = session.get('books', []);
    books = [Book(**b) for b in stored_books]  # recreate Book objects
    print(books)
    return books

@app.route('/reload')
def reload():
    if 'books' in session:
        session['previous_books'] = session['books']
        del session['books']
    return redirect('/')

def scape_dummy(): 
    return get_dummy_books()

def check_status_change(books):
    if 'previuos_books' in session:
        previuos_books = [Book(**b) for b in session['previuos_books']] 
        for book in books:
            book_changed = True
            for previous_book in previuos_books:
                if previous_book.address == book.address and previous_book.status == book.status:
                    book_changed = False
            if book_changed:
                book.changed = True

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

