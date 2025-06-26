# Здесь должна быть модель Loan согласно README.md

from datetime import datetime

class Loan:
    def __init__(self, book_id, reader_id, loan_date, return_date) -> None:
        self.book_id = book_id
        self.reader_id = reader_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_returned = False
        self.id = None

    def return_book(self) -> bool:
        if not self.is_returned:
            self.is_returned = True
            return True
        return False

    def is_overdue(self) -> bool:
        return not self.is_returned and datetime.now() > self.return_date

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "book_id": self.book_id,
            "reader_id": self.reader_id,
            "loan_date": self.loan_date,
            "return_date": self.return_date,
            "is_returned": self.is_returned,
        }

    def _validate_data(self, book_id, reader_id, loan_date, return_date) -> None:
        if book_id <= 0:
            raise ValueError("Invalid book ID")

        if reader_id <= 0:
            raise ValueError("Invalid reader ID")

        if not isinstance(loan_date, datetime):
            raise ValueError("Invalid loan date")

        if not isinstance(return_date, datetime):
            raise ValueError("Invalid loan date")

        if return_date <= loan_date:
            raise ValueError("The loan date must be earlier than the return date")
