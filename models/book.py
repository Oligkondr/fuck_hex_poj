# Здесь должна быть модель Book согласно README.md

from datetime import datetime

class Book:
    def __init__(self, title: str, author: str, isbn: str, year: int, quantity: int) -> None:
        self.id = None
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.quantity = quantity
        self.available = quantity

    def borrow_book(self) -> bool:
        if self.available > 0:
            self.available -= 1
            return True
        return False

    def return_book(self) -> bool:
        if self.available < self.quantity:
            self.available += 1
            return True
        return False

    def is_available(self) -> bool:
        return self.available > 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year,
            "quantity": self.quantity,
            "available": self.available,
        }

# class Book:
#     def __init__(self, title, author, isbn, year, quantity) -> None:
#         pass
#
#     def borrow_book(self) -> bool:
#         pass
#
#     def return_book(self) -> bool:
#         pass
#
#     def is_available(self) -> bool:
#         pass
#
#     def to_dict(self) -> dict:
#         pass

