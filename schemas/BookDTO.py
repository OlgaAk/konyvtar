from schemas.PrintedBookDTO import PrintedBookDTO


class BookDTO:
    def __init__(self, id: str, name: str, author: str, 
                 year: str, shelf_number: str, printed_books: list[PrintedBookDTO]):
        self.id = id
        self.name = name
        self.author = author
        self.year = year
        self.shelf_number = shelf_number
        self.printed_books = printed_books  
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'year': self.year,
            'shelf_number': self.shelf_number,
            'printed_books': [pb.to_dict() for pb in self.printed_books]
        }
        
    @classmethod
    def from_dict(cls, data: dict):
        printed_books = [
            PrintedBookDTO(**pb) for pb in data.get("printed_books", [])
        ]
        data = {**data, "printed_books": printed_books}
        return cls(**data)
        

