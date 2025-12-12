import random
from schemas.PrintedBookDTO import PrintedBookDTO
from schemas.BookDTO import BookDTO

def get_dummy_books() -> list[BookDTO]: 
    book = BookDTO("1415430", "Dummy Book some name lorem ipsum lorem ipsum", "Dummy Author", "2020", "B 40", [])
    randomDate1 = random.randint(3,28)
    printedBook1 = PrintedBookDTO(f'Lejár: 2025.11.{randomDate1}', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook2 = PrintedBookDTO(f'Lejár: 2025.11.{randomDate1-1}', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook3 = PrintedBookDTO(f'Lejár: 2025.12.31', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book.printed_books.extend([printedBook1, printedBook2, printedBook3])
    book.printed_books.sort(key=lambda x: x.status)
    
    book2 = BookDTO("1435665", "Dummy Book some name lorem ipsum lorem ipsum", "Dummy Author", "2020", "B 40", [])
    printedBook4 = PrintedBookDTO(f'Lejár: 2025.11.{randomDate1}', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook5 = PrintedBookDTO(f'Lejár: 2025.11.{randomDate1-1}', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook6 = PrintedBookDTO(f'Lejár: 2025.12.31', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book2.printed_books.extend([printedBook4, printedBook5, printedBook6])
    book2.printed_books.sort(key=lambda x: x.status)
    
    book3 = BookDTO("1413839", "Dummy Book some name lorem ipsum lorem ipsum", "Dummy Author", "2020", "B 40", [])
    printedBook7 = PrintedBookDTO(f'Lejár: 2025.11.{randomDate1}', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook8 = PrintedBookDTO(f'Lejár: 2025.11.{randomDate1-1}', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook9 = PrintedBookDTO(f'Lejár: 2025.12.31', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book3.printed_books.extend([printedBook7, printedBook8, printedBook9])
    book3.printed_books.sort(key=lambda x: x.status)
    
    book4 = BookDTO("1413840", "Dummy Book some name lorem ipsum lorem ipsum", "Dummy Author", "2020", "B 40", [])
    printedBook10 = PrintedBookDTO(f'Lejár: 2025.11.{randomDate1}', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook11 = PrintedBookDTO(f'Lejár: 2025.11.{randomDate1-1}', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    printedBook12 = PrintedBookDTO(f'Lejár: 2025.12.31', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book4.printed_books.extend([printedBook10, printedBook11, printedBook12])
    book4.printed_books.sort(key=lambda x: x.status)
    
    return [book, book2, book3, book4]