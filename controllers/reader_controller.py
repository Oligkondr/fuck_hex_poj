# Здесь должен быть контроллер для работы с читателями согласно README.md

from models.reader import Reader

class ReaderController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def add_reader(self, name, email, phone) -> int:
        reader = Reader(name, email, phone)
        return self.db.insert_reader(reader)

    def get_reader(self, reader_id) -> Reader | None:
        row = self.db.select_reader_by_id(reader_id)
        return Reader.from_row(row) if row else None

    def get_all_readers(self) -> list[Reader]:
        rows = self.db.select_all_readers()
        return [Reader.from_row(row) for row in rows]

    def update_reader(self, reader_id, **kwargs) -> bool:
        return self.db.update_reader(reader_id, **kwargs)

    def delete_reader(self, reader_id) -> bool:
        return self.db.delete_reader(reader_id)

    def get_reader_loans(self, reader_id) -> list:
        return self.db.select_loans_by_reader(reader_id)

# from models.reader import Reader

# class ReaderController:
#     def __init__(self, db_manager) -> None:
#         pass

#     def add_reader(self, name, email, phone) -> int:
#         pass

#     def get_reader(self, reader_id) -> Reader | None:
#         pass

#     def get_all_readers(self) -> list[Reader]:
#         pass

#     def update_reader(self, reader_id, **kwargs) -> bool:
#         pass

#     def delete_reader(self, reader_id) -> bool:
#         pass

#     def get_reader_loans(self, reader_id) -> list:
#         pass

