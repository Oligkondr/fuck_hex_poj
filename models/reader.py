# Здесь должна быть модель Reader согласно README.md

from datetime import datetime
import re

class Reader:
    def __init__(self, name, email, phone) -> None:
        self._validate_data(name, email)

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
        if not self._is_valid_name(name):
            raise ValueError("Invalid name")

        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")

    def update_info(self, name=None, email=None, phone=None) -> None:
        if name is not None:
            if not self._is_valid_name(name):
                raise ValueError("Invalid email format")

            self.name = name

        if email is not None:
            if not self._is_valid_email(email):
                raise ValueError("Invalid email format")

            self.email = email

        if phone is not None:
            self.phone = phone

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "registration_date": self.registration_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
