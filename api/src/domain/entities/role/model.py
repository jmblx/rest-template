from dataclasses import dataclass

from domain.entities.role.value_objects import RoleID, RoleName


@dataclass
class Role:
    id: RoleID
    name: RoleName
