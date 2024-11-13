from _decimal import Decimal
from typing import Optional
from datetime import datetime

from domain.entities.role.value_objects import RoleID
from domain.entities.user.value_objects import UserID, Email, RegisterDate, FilePath, LastName, FirstName, \
    HashedPassword

from dataclasses import dataclass, field


from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

@dataclass
class User:
    id: 'UserID' = field(init=False)
    first_name: 'FirstName'
    last_name: 'LastName'
    role_id: 'RoleID'
    email: 'Email'
    hashed_password: HashedPassword
    file_path: Optional['FilePath']
    registered_at: 'RegisterDate'

    @property
    def id_value(self) -> UUID:
        return self.id.value

    @property
    def email_value(self) -> str:
        return self.email.value

    @property
    def first_name_value(self) -> str:
        return self.first_name.value

    @property
    def last_name_value(self) -> str:
        return self.last_name.value

    @property
    def role_id_value(self) -> int:
        return self.role_id.value

    @property
    def file_path_value(self) -> Optional[str]:
        return self.file_path.value if self.file_path else None

    @property
    def registered_at_value(self) -> str:
        return self.registered_at.value
