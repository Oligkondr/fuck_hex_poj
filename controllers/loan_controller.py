# Здесь должен быть контроллер для работы с займами согласно README.md

from models.loan import Loan
from datetime import datetime

class LoanController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def create_loan(self, book_id, reader_id, loan_date, return_date) -> int:
        loan = Loan(book_id, reader_id, loan_date, return_date)
        return self.db.add_loan(loan)

    def get_loan(self, loan_id) -> Loan | None:
        return self.db.get_loan_by_id(loan_id)

    def get_all_loans(self) -> list[Loan]:
        return self.db.get_all_loans()

    def return_book(self, loan_id) -> bool:
        return self.db.update_loan(loan_id, is_returned=True)

    def get_overdue_loans(self) -> list[Loan]:
        return self.db.get_overdue_loans()

    def get_reader_loans(self, reader_id) -> list[Loan]:
        return self.db.get_reader_loans(reader_id)
