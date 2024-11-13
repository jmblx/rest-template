from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class RoleID:
    value: int
    _valid_values = (0, 1, 2)

    def __post_init__(self):
        if self.value not in self._valid_values:
            raise ValueError("RoleID must be a valid int and refer to a valid role.")


@dataclass(frozen=True)
class RoleName:
    value: str
    _allowed_names = {"user", "admin"}

    def __post_init__(self):
        if self.value not in self._allowed_names:
            raise ValueError("RoleName must be one of the allowed names.")
