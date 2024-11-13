from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.models import user_achievement
from infrastructure.db.models import User
from domain.repositories.user.repo import UserRepository
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class UserRepositoryImpl(BaseRepositoryImpl[User], UserRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def add_user_achievements(self, user_achievements: list[dict]) -> None:
        stmt = insert(user_achievement).values(user_achievements)
        await self._session.execute(stmt)
        await self._session.commit()
