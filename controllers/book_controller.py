# controllers/book_controller.py
from typing import List, Optional
from models.book import Book
from database.database_manager import DatabaseManager

class BookController:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def add_book(self, title: str, author: str, isbn: str, year: int, quantity: int) -> int:
        book = Book(title, author, isbn, year, quantity)
        return self.db.add_book(book)

    def get_book(self, book_id: int) -> Optional[Book]:
        return self.db.get_book_by_id(book_id)

    def get_all_books(self) -> List[Book]:
        return self.db.get_all_books()

    def update_book(self, book_id: int, **kwargs) -> bool:
        return self.db.update_book(book_id, **kwargs)

    def delete_book(self, book_id: int) -> bool:
        return self.db.delete_book(book_id)

    def search_books(self, query: str) -> List[Book]:
        return self.db.search_books(query)

    def borrow_book(self, book_id: int) -> bool:
        book = self.get_book(book_id)
        if book and book.borrow_book():
            return self.db.update_book(book_id, available=book.available)
        return False

    def return_book(self, book_id: int) -> bool:
        book = self.get_book(book_id)
        if book and book.return_book():
            return self.db.update_book(book_id, available=book.available)
        return False