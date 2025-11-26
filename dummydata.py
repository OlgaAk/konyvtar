from models.PrintedBook import PrintedBook

def get_dummy_books(): 
    book1 = PrintedBook('Lejár: 2025.11.07', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book2 = PrintedBook('Lejár: 2025.11.09', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    book3 = PrintedBook('Lejár: 2025.12.19', 'KK Sárkányos Gyerekkönyvtár, 1. szint')
    return [book1, book2, book3]