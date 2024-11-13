from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.models.database import Base
from core.db.db_types import added_at


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str]
    is_email_confirmed: Mapped[bool] = mapped_column(default=False)
    email_confirmation_token = mapped_column(nullable=True, type_=String(50))
    hashed_password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), default=1)
    role = relationship("Role", back_populates="users_role", uselist=False)
    file_path: Mapped[str] = mapped_column(nullable=True)
