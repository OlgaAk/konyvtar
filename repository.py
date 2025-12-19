from db import db
from models.Book import Book

def get_books():
    return db.session.execute(db.select(Book).order_by(Book.title)).scalars()

def add_book(book: Book):
    db.session.add(book)
    db.session.commit()

def remove_book(library_id: str):
    book = db.session.execute(db.select(Book).where(Book.library_id == library_id)).scalar_one_or_none()
    if book:
        db.session.delete(book)
        db.session.commit()
    