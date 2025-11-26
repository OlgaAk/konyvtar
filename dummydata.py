from models.PrintedBook import PrintedBook
from models.Book import Book

def get_dummy_books() -> list[Book]: 
    book = Book("Dummy Book", "Dummy Author", "2020", "B 40", [])
    printedBook1 = PrintedBook('Lejár: 2025.11.07', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook2 = PrintedBook('Lejár: 2025.11.09', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook3 = PrintedBook('Lejár: 2025.12.19', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book.printed_books.extend([printedBook1, printedBook2, printedBook3])
    book.printed_books.sort(key=lambda x: x.status)
    
    book2 = Book("Another Dummy Book", "Another Dummy Author", "2021", "C 12", [])
    printedBook4 = PrintedBook('Elérhető', 'KK Boráros tér, Fszek')
    book2.printed_books.append(printedBook4)
    return [book, book2]