import re
from dataclasses import dataclass
from enum import Enum

from domain.exceptions.client import ClientNameLengthError, InvalidUrlError


@dataclass(frozen=True)
class ClientID:
    value: int


class ClientTypeEnum(Enum):
    PUBLIC = 1
    PRIVATE = 2


@dataclass(frozen=True)
class ClientType:
    value: ClientTypeEnum

    def __post_init__(self) -> None:
        if not isinstance(self.value, ClientTypeEnum):
            raise TypeError("value must be an instance of ClientTypeEnum")


@dataclass(frozen=True)
class ClientName:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("value must be an instance of str")
        self.check_length()

    def check_length(self) -> None:
        if len(self.value) > 100:
            raise ClientNameLengthError(
                "value must be less than 100 characters"
            )


def check_is_valid_url(url: str) -> None:
    url_pattern = re.compile(
        r"^(https?://)?"
        r"([a-zA-Z0-9.-]+(\.[a-zA-Z]{2,})?)"
        r"(:\d{1,5})?"
        r"(/[-a-zA-Z0-9()@:%_\+.~#?&/=]*)?$"
    )
    if not url_pattern.match(url):
        raise InvalidUrlError("Invalid URL")


@dataclass(frozen=True)
class ClientBaseUrl:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("value must be an instance of str")
        check_is_valid_url(self.value)


@dataclass(frozen=True)
class ClientRedirectUrl:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("value must be an instance of str")
        check_is_valid_url(self.value)
