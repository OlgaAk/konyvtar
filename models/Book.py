from sqlalchemy.orm import Mapped, mapped_column
from db import db
from schemas.BookDTO import BookDTO

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    library_id: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    year: Mapped[int]
    shelf_number: Mapped[str]   
    
    
    def from_dto(dto: BookDTO) -> "Book":
        return Book(
            library_id=dto.library_id,
            title=dto.title,
            author=dto.author,
            year=int(dto.year) if dto.year.isdigit() else None,
            shelf_number=dto.shelf_number
        )
        
    def to_dto(self) -> BookDTO:
        return BookDTO(
            library_id=self.library_id,
            title=self.title,
            author=self.author,
            year=str(self.year) if self.year is not None else "",
            shelf_number=self.shelf_number,
            printed_books=[]
        )