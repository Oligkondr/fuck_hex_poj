# Здесь должен быть контроллер для работы с займами согласно README.md

from models.loan import Loan
from datetime import datetime

class LoanController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def create_loan(self, book_id, reader_id, loan_date, return_date) -> int:
        loan = Loan(book_id, reader_id, loan_date, return_date)
        return self.db.insert_loan(loan)

    def get_loan(self, loan_id) -> Loan | None:
        row = self.db.select_loan_by_id(loan_id)
        return Loan.from_row(row) if row else None

    def get_all_loans(self) -> list[Loan]:
        rows = self.db.select_all_loans()
        return [Loan.from_row(row) for row in rows]

    def return_book(self, loan_id) -> bool:
        return self.db.mark_loan_returned(loan_id)

    def get_overdue_loans(self) -> list[Loan]:
        today = datetime.now().date()
        rows = self.db.select_overdue_loans(today)
        return [Loan.from_row(row) for row in rows]

    def get_reader_loans(self, reader_id) -> list[Loan]:
        rows = self.db.select_loans_by_reader(reader_id)
        return [Loan.from_row(row) for row in rows]

# from models.loan import Loan
# from datetime import datetime

# class LoanController:
#     def __init__(self, db_manager) -> None:
#         pass

#     def create_loan(self, book_id, reader_id, loan_date, return_date) -> int:
#         pass

#     def get_loan(self, loan_id) -> Loan | None:
#         pass

#     def get_all_loans(self) -> list[Loan]:
#         pass

#     def return_book(self, loan_id) -> bool:
#         pass

#     def get_overdue_loans(self) -> list[Loan]:
#         pass

#     def get_reader_loans(self, reader_id) -> list[Loan]:
#         pass

