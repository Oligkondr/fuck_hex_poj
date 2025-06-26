# Здесь должен быть контроллер для работы с книгами согласно README.md

from models.book import Book

class BookController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def add_book(self, title, author, isbn, year, quantity) -> int:
        book = Book(title, author, isbn, year, quantity)
        return self.db.insert_book(book)

    def get_book(self, book_id) -> Book | None:
        row = self.db.select_book_by_id(book_id)
        return Book.from_row(row) if row else None

    def get_all_books(self) -> list[Book]:
        rows = self.db.select_all_books()
        return [Book.from_row(row) for row in rows]

    def update_book(self, book_id, **kwargs) -> bool:
        return self.db.update_book(book_id, **kwargs)

    def delete_book(self, book_id) -> bool:
        return self.db.delete_book(book_id)

    def search_books(self, query) -> list[Book]:
        rows = self.db.search_books(query)
        return [Book.from_row(row) for row in rows]

    def borrow_book(self, book_id) -> bool:
        book = self.get_book(book_id)
        if book and book.quantity > 0:
            return self.db.update_book(book_id, quantity=book.quantity - 1)
        return False

    def return_book(self, book_id) -> bool:
        book = self.get_book(book_id)
        if book:
            return self.db.update_book(book_id, quantity=book.quantity + 1)
        return False

# from models.book import Book

# class BookController:
#     def __init__(self, db_manager) -> None:
#         pass

#     def add_book(self, title, author, isbn, year, quantity) -> int:
#         pass

#     def get_book(self, book_id) -> Book | None:
#         pass

#     def get_all_books(self) -> list[Book]:
#         pass

#     def update_book(self, book_id, **kwargs) -> bool:
#         pass

#     def delete_book(self, book_id) -> bool:
#         pass

#     def search_books(self, query) -> list[Book]:
#         pass

#     def borrow_book(self, book_id) -> bool:
#         pass

#     def return_book(self, book_id) -> bool:
#         pass

