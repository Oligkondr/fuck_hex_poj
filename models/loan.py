# Здесь должна быть модель Loan согласно README.md

from datetime import datetime

from datetime import datetime

class Loan:
    id_counter = 1

    def __init__(self, book_id: int, reader_id: int, loan_date: datetime, return_date: datetime) -> None:
        self.id = Loan.id_counter
        Loan.id_counter += 1

        self.book_id = book_id
        self.reader_id = reader_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_returned = False

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
            "loan_date": self.loan_date.isoformat(),
            "return_date": self.return_date.isoformat(),
            "is_returned": self.is_returned,
        }


# class Loan:
#     def __init__(self, book_id, reader_id, loan_date, return_date) -> None:
#         pass
#
#     def return_book(self) -> bool:
#         pass
#
#     def is_overdue(self) -> bool:
#         pass
#
#     def to_dict(self) -> dict:
#         pass

