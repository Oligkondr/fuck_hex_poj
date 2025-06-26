# Здесь должна быть модель Reader согласно README.md

from datetime import datetime
import re

class Reader:
    def __init__(self, name, email, phone) -> None:
        self.id = None
        self.name = name
        self.email = email
        self.phone = phone
        self.registration_date = datetime.now()

    def _is_valid_email(self, email) -> bool:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def _is_valid_name(self, name) -> bool:
        return name.strip() != ""

    def _validate_data(self, name, email) -> None:
        if self._is_valid_name(name):
            raise ValueError("Invalid name")

        if self._is_valid_email(email):
            raise ValueError("Invalid email format")

    def update_info(self, name=None, email=None, phone=None) -> None:
        pass

    def to_dict(self) -> dict:
        pass
