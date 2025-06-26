# controllers/reader_controller.py
from typing import List, Optional
from datetime import datetime
from models.reader import Reader
from database.database_manager import DatabaseManager

class ReaderController:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def add_reader(self, name: str, email: str, phone: str) -> int:
        reader = Reader(name, email, phone)
        return self.db.add_reader(reader)

    def get_reader(self, reader_id: int) -> Optional[Reader]:
        return self.db.get_reader_by_id(reader_id)

    def get_all_readers(self) -> List[Reader]:
        return self.db.get_all_readers()

    def update_reader(self, reader_id: int, **kwargs) -> bool:
        return self.db.update_reader(reader_id, **kwargs)

    def delete_reader(self, reader_id: int) -> bool:
        return self.db.delete_reader(reader_id)

    def get_reader_loans(self, reader_id: int) -> List[dict]:
        return self.db.get_reader_loans(reader_id)