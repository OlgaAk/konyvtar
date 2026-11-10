import os
import sqlite3
from contextlib import contextmanager
from typing import Optional

from models.Book import Book
from models.PrintedBook import PrintedBook


DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.sqlite3"),
)


@contextmanager
def _connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize():
    with _connect() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                author TEXT NOT NULL,
                year TEXT NOT NULL DEFAULT '',
                shelf_number TEXT NOT NULL DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS printed_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id TEXT NOT NULL REFERENCES books(id) ON DELETE CASCADE,
                status TEXT NOT NULL,
                address TEXT NOT NULL,
                changed INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS app_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )


def is_initialized() -> bool:
    with _connect() as connection:
        initialized = connection.execute(
            "SELECT value FROM app_state WHERE key = 'catalog_initialized'"
        ).fetchone()
        if initialized is not None and initialized["value"] == "1":
            return True
        return connection.execute("SELECT EXISTS(SELECT 1 FROM books)").fetchone()[0]


def _set_initialized(connection):
    connection.execute(
        """
        INSERT INTO app_state (key, value)
        VALUES ('catalog_initialized', '1')
        ON CONFLICT(key) DO UPDATE SET value = '1'
        """
    )


def list_books() -> list[Book]:
    with _connect() as connection:
        rows = connection.execute(
            "SELECT id, name, author, year, shelf_number FROM books ORDER BY name"
        ).fetchall()
        books = []
        for row in rows:
            printed_rows = connection.execute(
                """
                SELECT status, address, changed
                FROM printed_books
                WHERE book_id = ?
                ORDER BY status, address
                """,
                (row["id"],),
            ).fetchall()
            printed_books = [
                PrintedBook(item["status"], item["address"], bool(item["changed"]))
                for item in printed_rows
            ]
            books.append(
                Book(
                    row["id"],
                    row["name"],
                    row["author"],
                    row["year"],
                    row["shelf_number"],
                    printed_books,
                )
            )
        return books


def get_book(book_id: str) -> Optional[Book]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT id, name, author, year, shelf_number FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()
        if row is None:
            return None

        printed_rows = connection.execute(
            """
            SELECT status, address, changed
            FROM printed_books
            WHERE book_id = ?
            ORDER BY status, address
            """,
            (book_id,),
        ).fetchall()
        return Book(
            row["id"],
            row["name"],
            row["author"],
            row["year"],
            row["shelf_number"],
            [
                PrintedBook(item["status"], item["address"], bool(item["changed"]))
                for item in printed_rows
            ],
        )


def create_book(book: Book):
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO books (id, name, author, year, shelf_number)
            VALUES (?, ?, ?, ?, ?)
            """,
            (book.id, book.name, book.author, book.year, book.shelf_number),
        )
        _replace_printed_books(connection, book)
        _set_initialized(connection)


def update_book(book: Book):
    with _connect() as connection:
        result = connection.execute(
            """
            UPDATE books
            SET name = ?, author = ?, year = ?, shelf_number = ?
            WHERE id = ?
            """,
            (book.name, book.author, book.year, book.shelf_number, book.id),
        )
        if result.rowcount:
            _replace_printed_books(connection, book)
        return result.rowcount > 0


def delete_book(book_id: str) -> bool:
    with _connect() as connection:
        result = connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
        return result.rowcount > 0


def replace_books(books: list[Book]):
    with _connect() as connection:
        connection.execute("DELETE FROM books")
        for book in books:
            connection.execute(
                """
                INSERT INTO books (id, name, author, year, shelf_number)
                VALUES (?, ?, ?, ?, ?)
                """,
                (book.id, book.name, book.author, book.year, book.shelf_number),
            )
            _replace_printed_books(connection, book)
        _set_initialized(connection)


def _replace_printed_books(connection, book: Book):
    connection.execute("DELETE FROM printed_books WHERE book_id = ?", (book.id,))
    connection.executemany(
        """
        INSERT INTO printed_books (book_id, status, address, changed)
        VALUES (?, ?, ?, ?)
        """,
        [
            (book.id, printed.status, printed.address, int(printed.changed))
            for printed in book.printed_books
        ],
    )
