from sqlalchemy.orm import Mapped, mapped_column
from db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    library_id: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(unique=True)
    author: Mapped[str]
    year: Mapped[int]
    shelf_number: Mapped[str]   