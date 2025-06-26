# Здесь должна быть модель Reader согласно README.md

from datetime import datetime
import re

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

    def update_info(self, name=None, email=None, phone=None) -> None:
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "registration_date": self.registration_date.strftime("%Y-%m-%d %H:%M:%S")
        }

# class Reader:
#     def __init__(self, name, email, phone) -> None:
#         pass
#
#     def _is_valid_email(self, email) -> bool:
#         pass
#
#     def update_info(self, name=None, email=None, phone=None) -> None:
#         pass
#
#     def to_dict(self) -> dict:
#         pass
