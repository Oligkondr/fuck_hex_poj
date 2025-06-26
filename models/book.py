# Здесь должна быть модель Book согласно README.md

from datetime import datetime

class Book:
    def __init__(self, title, author, isbn, year, quantity) -> None:
        self._validate_data(title, author, isbn, year, quantity)

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

    def _validate_data(self, title, author, isbn, year, quantity) -> None:
        if title.strip() == "":
            raise ValueError("Invalid title")

        if author.strip() == "":
            raise ValueError("Invalid author")

        if isbn.strip() == "":
            raise ValueError("Invalid ISBN")

        if year <= 0:
            raise ValueError("Invalid year")

        if quantity <= 0:
            raise ValueError("Invalid quantity")
