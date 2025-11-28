from models.Book import Book


def compare_books(books: list[Book], chached_books: list[Book]):
    if not chached_books:
        return
    for book in books:
        for chached_book in chached_books:
            if book.id == chached_book.id:
                compare_book(book, chached_book)

def compare_book(book: Book, chached_book: Book):
    for printed_book in book.printed_books:
        book_changed = True 
        for chached_printed_book in chached_book.printed_books:
            if chached_printed_book.address == printed_book.address and chached_printed_book.status == printed_book.status:
                book_changed = False
                chached_book.printed_books.remove(chached_printed_book); 
        printed_book.changed = book_changed