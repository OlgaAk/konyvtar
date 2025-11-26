from models.PrintedBook import PrintedBook
from models.Book import Book

def get_dummy_books() -> list[Book]: 
    book = Book("Dummy Book", "Dummy Author", [])
    printedBook1 = PrintedBook('Lejár: 2025.11.07', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook2 = PrintedBook('Lejár: 2025.11.09', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook3 = PrintedBook('Lejár: 2025.12.19', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book.printedBookList.extend([printedBook1, printedBook2, printedBook3])
    book.printedBookList.sort(key=lambda x: x.status)
    
    book2 = Book("Another Dummy Book", "Another Dummy Author", [])
    printedBook4 = PrintedBook('Elérhető', 'KK Boráros tér, Fszek')
    book2.printedBookList.append(printedBook4)
    return [book, book2]