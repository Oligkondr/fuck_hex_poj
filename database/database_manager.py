# Здесь должен быть менеджер базы данных согласно README.md

import sqlite3
from models.book import Book
from models.reader import Reader
from models.loan import Loan
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="library.db") -> None:
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.create_tables()

    def close(self) -> None:
        self.cursor.close()
        self.connection.close()

    def create_tables(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                available INTEGER NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                registration_date TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                reader_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                return_date TEXT NOT NULL,
                is_returned INTEGER DEFAULT 0,
                FOREIGN KEY(book_id) REFERENCES books(id),
                FOREIGN KEY(reader_id) REFERENCES readers(id)
            )
        """)

    def add_book(self, book: Book) -> int:
        self.cursor.execute(
            """
            INSERT INTO books (title, author, isbn, year, quantity, available)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                book.title,
                book.author,
                book.isbn,
                book.year,
                book.quantity,
                book.quantity,
            ),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_book_by_id(self, book_id) -> Book | None:
        self.cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = self.cursor.fetchone()
        if row:
            book = Book(
                title=row["title"],
                author=row["author"],
                isbn=row["isbn"],
                year=row["year"],
                quantity=row["quantity"],
            )
            book.id = row["id"]
            book.available = row["available"]
            return book
        return None

    def get_all_books(self) -> list[Book]:
        self.cursor.execute("SELECT * FROM books")
        books = []
        for row in self.cursor.fetchall():
            book = Book(
                title=row["title"],
                author=row["author"],
                isbn=row["isbn"],
                year=row["year"],
                quantity=row["quantity"],
            )
            book.id = row["id"]
            book.available = row["available"]
            books.append(book)
        return books

    def update_book(self, book_id, **kwargs) -> bool:
        if not kwargs:
            return False

        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [book_id]

        self.cursor.execute(f"UPDATE books SET {set_clause} WHERE id = ?", values)
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_book(self, book_id) -> bool:
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def search_books(self, query) -> list[Book]:
        pattern = f"%{query}%"
        self.cursor.execute(
            """
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
        """,
            (pattern, pattern, pattern),
        )

        books = []
        for row in self.cursor.fetchall():
            book = Book(
                title=row["title"],
                author=row["author"],
                isbn=row["isbn"],
                year=row["year"],
                quantity=row["quantity"],
            )
            book.id = row["id"]
            book.available = row["available"]
            books.append(book)
        return books

    def add_reader(self, reader: Reader) -> int:
        self.cursor.execute(
            """
            INSERT INTO readers (name, email, phone, registration_date)
            VALUES (?, ?, ?, ?)
        """,
            (reader.name, reader.email, reader.phone, datetime.now().isoformat()),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_reader_by_id(self, reader_id) -> Reader | None:
        self.cursor.execute("SELECT * FROM readers WHERE id = ?", (reader_id,))
        row = self.cursor.fetchone()
        if row:
            reader = Reader(name=row["name"], email=row["email"], phone=row["phone"])
            reader.id = row["id"]
            reader.registration_date = datetime.fromisoformat(row["registration_date"])
            return reader
        return None

    def get_all_readers(self) -> list[Reader]:
        self.cursor.execute("SELECT * FROM readers")
        readers = []
        for row in self.cursor.fetchall():
            reader = Reader(name=row["name"], email=row["email"], phone=row["phone"])
            reader.id = row["id"]
            reader.registration_date = datetime.fromisoformat(row["registration_date"])
            readers.append(reader)
        return readers

    def update_reader(self, reader_id, **kwargs) -> bool:
        if not kwargs:
            return False

        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [reader_id]

        self.cursor.execute(f"UPDATE readers SET {set_clause} WHERE id = ?", values)
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_reader(self, reader_id) -> bool:
        self.cursor.execute("DELETE FROM readers WHERE id = ?", (reader_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def add_loan(self, loan: Loan) -> int:
        self.cursor.execute(
            """
            INSERT INTO loans (book_id, reader_id, loan_date, return_date, is_returned)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                loan.book_id,
                loan.reader_id,
                loan.loan_date.isoformat(),
                loan.return_date.isoformat(),
                int(loan.is_returned),
            ),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_loan_by_id(self, loan_id) -> Loan | None:
        self.cursor.execute("SELECT * FROM loans WHERE id = ?", (loan_id,))
        row = self.cursor.fetchone()
        if row:
            loan = Loan(
                book_id=row["book_id"],
                reader_id=row["reader_id"],
                loan_date=datetime.fromisoformat(row["loan_date"]),
                return_date=datetime.fromisoformat(row["return_date"]),
            )
            loan.id = row["id"]
            loan.is_returned = bool(row["is_returned"])
            return loan
        return None

    def get_all_loans(self) -> list[Loan]:
        self.cursor.execute("SELECT * FROM loans")
        loans = []
        for row in self.cursor.fetchall():
            loan = Loan(
                book_id=row["book_id"],
                reader_id=row["reader_id"],
                loan_date=datetime.fromisoformat(row["loan_date"]),
                return_date=datetime.fromisoformat(row["return_date"]),
            )
            loan.id = row["id"]
            loan.is_returned = bool(row["is_returned"])
            loans.append(loan)
        return loans

    def update_loan(self, loan_id, **kwargs) -> bool:
        if not kwargs:
            return False

        set_clause = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        values = list(kwargs.values()) + [loan_id]

        self.cursor.execute(f"UPDATE loans SET {set_clause} WHERE id = ?", values)
        self.connection.commit()
        return self.cursor.rowcount > 0

    def get_reader_loans(self, reader_id) -> list[Loan]:
        self.cursor.execute("SELECT * FROM loans WHERE reader_id = ?", (reader_id,))
        loans = []
        for row in self.cursor.fetchall():
            loan = Loan(
                book_id=row["book_id"],
                reader_id=row["reader_id"],
                loan_date=datetime.fromisoformat(row["loan_date"]),
                return_date=datetime.fromisoformat(row["return_date"]),
            )
            loan.id = row["id"]
            loan.is_returned = bool(row["is_returned"])
            loans.append(loan)
        return loans

    def get_overdue_loans(self) -> list[Loan]:
        today = datetime.now().isoformat()
        self.cursor.execute(
            """
            SELECT * FROM loans 
            WHERE return_date < ? AND is_returned = 0
        """,
            (today,),
        )

        loans = []
        for row in self.cursor.fetchall():
            loan = Loan(
                book_id=row["book_id"],
                reader_id=row["reader_id"],
                loan_date=datetime.fromisoformat(row["loan_date"]),
                return_date=datetime.fromisoformat(row["return_date"]),
            )
            loan.id = row["id"]
            loan.is_returned = bool(row["is_returned"])
            loans.append(loan)
        return loans
