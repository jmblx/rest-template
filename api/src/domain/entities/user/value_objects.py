from dataclasses import dataclass
import re
from datetime import datetime
from uuid import UUID, uuid4

from domain.exceptions.user import (
    InvalidEmailError,
    InvalidUserIDError,
    InvalidRegisterDateError,
    InvalidFilePathError,
    InvalidCharacterError,
    EmptyValueError,
    InvalidPasswordError,
)


@dataclass(frozen=True)
class RawPassword:
    value: str

    def __post_init__(self):
        if not self._validate():
            raise InvalidPasswordError(
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
            raise EmptyValueError(
                "Hashed password must be a non-empty string."
            )

    @staticmethod
    def create(password: str, hash_service) -> "HashedPassword":
        hashed = hash_service.hash_password(password)
        return HashedPassword(hashed)


@dataclass(frozen=True)
class UserID:
    value: UUID

    def __post_init__(self):
        if not isinstance(self.value, UUID):
            raise InvalidUserIDError("UserID must be a valid UUID.")

    @staticmethod
    def generate():
        return UserID(uuid4())


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if not self.is_valid_email(self.value):
            raise InvalidEmailError(f"Invalid email address: {self.value}")

    @staticmethod
    def is_valid_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(pattern, email))
