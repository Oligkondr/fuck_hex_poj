from datetime import datetime

class Loan:
    def __init__(self, book_id: int, reader_id: int, loan_date: datetime, return_date: datetime) -> None:
        if book_id <= 0 or reader_id <= 0:
            raise ValueError("ID книги и читателя должны быть положительными числами")
        
        if not isinstance(loan_date, datetime) or not isinstance(return_date, datetime):
            raise ValueError("Даты должны быть типа datetime")
            
        if return_date <= loan_date:
            raise ValueError("Дата возврата должна быть позже даты выдачи")
        
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