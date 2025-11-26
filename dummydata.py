from models.Book import Book

def get_dummy_books(): 
    book1 = Book('Lejár: 2025.11.07', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book2 = Book('Lejár: 2025.11.09', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book3 = Book('Lejár: 2025.12.19', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    return [book1, book2, book3]