import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Union
from uuid import UUID
from decimal import Decimal, InvalidOperation

from domain.common.entities.value_objects import ValueObject


from dataclasses import dataclass, field
import re
from datetime import datetime
from uuid import UUID
from typing import Optional

@dataclass(frozen=True)
class RawPassword:
    value: str

    def __post_init__(self):
        if not self._validate():
            raise ValueError(
                "Invalid password. There must be at least one letter, one digit, "
                "one allowed special character, and a minimum of 8 characters."
            )

    def _validate(self) -> bool:
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$'
        return bool(re.match(pattern, self.value))


@dataclass(frozen=True)
class HashedPassword:
    value: str

    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Hashed password must be a non-empty string.")


@dataclass(frozen=True)
class FirstName:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("First name cannot be empty.")
        if not self.value.isalpha():
            raise ValueError("First name must contain only alphabetic characters.")


@dataclass(frozen=True)
class LastName:
    value: str

    def __post_init__(self):
        if not self.value or not self.value.strip():
            raise ValueError("Last name cannot be empty.")
        if not self.value.isalpha():
            raise ValueError("Last name must contain only alphabetic characters.")


@dataclass(frozen=True)
class FilePath:
    value: str

    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise ValueError("File path must be a valid string.")


@dataclass(frozen=True)
class RegisterDate:
    value: datetime

    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise ValueError("Register date must be a datetime instance.")
        if self.value > datetime.now():
            raise ValueError("Register date cannot be in the future.")


@dataclass(frozen=True)
class UserID:
    value: UUID

    def __post_init__(self):
        if not isinstance(self.value, UUID):
            raise ValueError("UserID must be a valid UUID.")


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self.is_valid_email(self.value):
            raise ValueError(f"Invalid email address: {self.value}")

    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))

