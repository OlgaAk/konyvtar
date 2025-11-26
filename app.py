from flask import Flask, render_template, session, redirect
import os
from models.Book import Book
from scrape import scrape



app = Flask(__name__)
app.secret_key = "supersecret"

mode = os.getenv('APP_ENV', 'production')
print(mode)

@app.route('/')
def index():
    stored_books = session.get('books', []);
    books = [Book(**b) for b in stored_books]  # recreate Book objects
    print(books)
    if (not books):
        if (mode == 'test'):
            books = scape_dummy()
            print('Running in test mode')
        else:
            books = scrape()
    books.sort(key=lambda x: x.status)
    session['books'] = [b.to_dict() for b in books]
    
    check_status_change(books)
    
    return render_template('index.html', items=books)

@app.route('/reload')
def reload():
    if 'books' in session:
        session['previous_books'] = session['books']
        del session['books']
    return redirect('/')


# def scape_dummy(): 
#     return [{'address': 'KK Sárkányos Gyerekkönyvtár, 1. szint', 'status': 'Lejár: 2025.11.06.'}, 
#             {'address': 'KK Sárkányos Gyerekkönyvtár, 1. szint', 'status': 'Lejár: 2025.10.08.'}, 
#              {'address': 'Boraros ter', 'status': 'Lejár: 2025.12.30'}, 
#             {'address': 'KK Sárkányos Gyerekkönyvtár, 1. szint', 'status': 'Lejár: 2025.12.02.'}]

def scape_dummy(): 
    book1 = Book('Lejár: 2025.11.07', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book2 = Book('Lejár: 2025.11.09', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book3 = Book('Lejár: 2025.12.19', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    return [book1, book2, book3]

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

