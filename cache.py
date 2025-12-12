from flask import session
from schemas.BookDTO import BookDTO

def save_to_cache(books: list[BookDTO]):
    session['books'] = [b.to_dict() for b in books]

def load_from_cache()-> list[BookDTO]:
    stored_books = session.get('books', []);
    books = [BookDTO.from_dict(b) for b in stored_books] 
    return books