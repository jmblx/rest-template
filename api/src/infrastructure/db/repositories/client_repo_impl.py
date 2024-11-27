from typing import cast

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from application.client.interfaces.repo import ClientRepository
from application.dtos.client import ClientCreateDTO
from domain.entities.client.model import Client
from domain.entities.client.value_objects import ClientID
from infrastructure.db.models.client.client_models import client_table


class ClientRepositoryImpl(ClientRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, client: Client) -> ClientCreateDTO:
        """
        Сохраняет объект клиента (Client) в базе данных.
        """
        saved_client = await self.session.merge(client)
        await self.session.flush()
        return ClientCreateDTO(client_id=cast(saved_client.id, int))

    async def delete(self, client_id: ClientID) -> None:
        """
        Удаляет клиента по его идентификатору.
        """
        query = select(client_table).where(client_table.c.id == client_id.value)
        result = await self.session.execute(query)
        client = result.scalar_one_or_none()
        if client:
            await self.session.delete(client)
