# Здесь должен быть менеджер базы данных согласно README.md

import sqlite3
from models.book import Book
from models.reader import Reader
from models.loan import Loan
from datetime import datetime


class DatabaseManager:
    def init(self, db_path="library.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()

    def close(self) -> None:
        self.conn.close()

    def create_tables(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                isbn TEXT,
                year INTEGER,
                quantity INTEGER
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                registration_date TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                reader_id INTEGER,
                loan_date TEXT,
                return_date TEXT,
                returned INTEGER DEFAULT 0,
                FOREIGN KEY(book_id) REFERENCES books(id),
                FOREIGN KEY(reader_id) REFERENCES readers(id)
            )
        """)
        self.conn.commit()

    # --- BOOKS ---

    def add_book(self, book: Book) -> int:
        self.cursor.execute("""
            INSERT INTO books (title, author, isbn, year, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (book.title, book.author, book.isbn, book.year, book.quantity))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_book_by_id(self, book_id) -> Book | None:
        self.cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = self.cursor.fetchone()
        return Book.from_row(row) if row else None

    def get_all_books(self) -> list[Book]:
        self.cursor.execute("SELECT * FROM books")
        return [Book.from_row(row) for row in self.cursor.fetchall()]

    def update_book(self, book_id, **kwargs) -> bool:
        fields = ", ".join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values()) + [book_id]
        self.cursor.execute(f"UPDATE books SET {fields} WHERE id = ?", values)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_book(self, book_id) -> bool:
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def search_books(self, query) -> list[Book]:
        pattern = f"%{query}%"
        self.cursor.execute("""
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
        """, (pattern, pattern, pattern))
        return [Book.from_row(row) for row in self.cursor.fetchall()]

    # --- READERS ---

    def add_reader(self, reader: Reader) -> int:
        self.cursor.execute("""
            INSERT INTO readers (name, email, phone, registration_date)
            VALUES (?, ?, ?, ?)
        """, (reader.name, reader.email, reader.phone, reader.registration_date.isoformat()))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_reader_by_id(self, reader_id) -> Reader | None:
        self.cursor.execute("SELECT * FROM readers WHERE id = ?", (reader_id,))
        row = self.cursor.fetchone()
        return Reader.from_row(row) if row else None

    def get_all_readers(self) -> list[Reader]:
        self.cursor.execute("SELECT * FROM readers")
        return [Reader.from_row(row) for row in self.cursor.fetchall()]

    def update_reader(self, reader_id, **kwargs) -> bool:
        fields = ", ".join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values()) + [reader_id]
        self.cursor.execute(f"UPDATE readers SET {fields} WHERE id = ?", values)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_reader(self, reader_id) -> bool:
        self.cursor.execute("DELETE FROM readers WHERE id = ?", (reader_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # --- LOANS ---

    def add_loan(self, loan: Loan) -> int:
        self.cursor.execute("""
            INSERT INTO loans (book_id, reader_id, loan_date, return_date, returned)
            VALUES (?, ?, ?, ?, 0)
        """, (loan.book_id, loan.reader_id,
              loan.loan_date.isoformat(), loan.return_date.isoformat()))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_loan_by_id(self, loan_id) -> Loan | None:
        self.cursor.execute("SELECT * FROM loans WHERE id = ?", (loan_id,))
        row = self.cursor.fetchone()
        return Loan.from_row(row) if row else None

    def get_all_loans(self) -> list[Loan]:
        self.cursor.execute("SELECT * FROM loans")
        return [Loan.from_row(row) for row in self.cursor.fetchall()]

    def update_loan(self, loan_id, **kwargs) -> bool:
        fields = ", ".join([f"{k}=?" for k in kwargs])
        values = list(kwargs.values()) + [loan_id]
        self.cursor.execute(f"UPDATE loans SET {fields} WHERE id = ?", values)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_reader_loans(self, reader_id) -> list[Loan]:
        self.cursor.execute("SELECT * FROM loans WHERE reader_id = ?", (reader_id,))
        return [Loan.from_row(row) for row in self.cursor.fetchall()]

    def get_overdue_loans(self) -> list[Loan]:
        today = datetime.now().date().isoformat()
        self.cursor.execute("""
            SELECT * FROM loans
            WHERE return_date < ? AND returned = 0
        """, (today,))
        return [Loan.from_row(row) for row in self.cursor.fetchall()]

# class DatabaseManager:
#     def __init__(self, db_path="library.db") -> None:
#         pass
#
#     def close(self) -> None:
#         pass
#
#     def create_tables(self) -> None:
#         pass
#
#     def add_book(self, book: Book) -> int:
#         pass
#
#     def get_book_by_id(self, book_id) -> Book | None:
#         pass
#
#     def get_all_books(self) -> list[Book]:
#         pass
#
#     def update_book(self, book_id, **kwargs) -> bool:
#         pass
#
#     def delete_book(self, book_id) -> bool:
#         pass
#
#     def search_books(self, query) -> list[Book]:
#         pass
#
#     def add_reader(self, reader: Reader) -> int:
#         pass
#
#     def get_reader_by_id(self, reader_id) -> Reader | None:
#         pass
#
#     def get_all_readers(self) -> list[Reader]:
#         pass
#
#     def update_reader(self, reader_id, **kwargs) -> bool:
#         pass
#
#     def delete_reader(self, reader_id) -> bool:
#         pass
#
#     def add_loan(self, loan: Loan) -> int:
#         pass
#
#     def get_loan_by_id(self, loan_id) -> Loan | None:
#         pass
#
#     def get_all_loans(self) -> list[Loan]:
#         pass
#
#     def update_loan(self, loan_id, **kwargs) -> bool:
#         pass
#
#     def get_reader_loans(self, reader_id) -> list[Loan]:
#         pass
#
#     def get_overdue_loans(self) -> list[Loan]:
#         pass
