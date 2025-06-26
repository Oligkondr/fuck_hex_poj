# controllers/loan_controller.py
from typing import List, Optional
from datetime import datetime, timedelta
from models.loan import Loan
from database.database_manager import DatabaseManager

class LoanController:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_loan(self, book_id: int, reader_id: int,
                   loan_date: datetime, return_date: datetime) -> int:
        loan = Loan(book_id, reader_id, loan_date, return_date)
        return self.db.add_loan(loan)

    def get_loan(self, loan_id: int) -> Optional[Loan]:
        return self.db.get_loan_by_id(loan_id)

    def get_all_loans(self) -> List[Loan]:
        return self.db.get_all_loans()

    def return_book(self, loan_id: int) -> bool:
        return self.db.update_loan(loan_id, is_returned=True)

    def get_overdue_loans(self) -> List[Loan]:
        return self.db.get_overdue_loans()

    def get_reader_loans(self, reader_id: int) -> List[Loan]:
        return self.db.get_reader_loans(reader_id)