from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.models.database import Base
from core.db.db_types import intpk


class Role(Base):
    __tablename__ = "role"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(nullable=False)
    permissions: Mapped[dict] = mapped_column(JSON)
    users_role = relationship(
        "User",
        back_populates="role",
        uselist=True
    )


Role.users_role = relationship("User", back_populates="role", uselist=True)
