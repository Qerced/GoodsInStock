from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models import Order


class CRUDOrder(CRUDBase):
    async def get_with_related(self, session: AsyncSession, id: int) -> Order:
        instance = await session.execute(
            select(self.model)
            .where(self.model.id == id)
            .options(joinedload(self.model.items))
        )
        return instance.unique().scalar_one_or_none()

    async def create(self, session: AsyncSession) -> Order:
        instance = self.model()
        session.add(instance)
        return instance

    async def update(
        self, session: AsyncSession, instance: Order, status: str
    ) -> Order:
        instance.status = status
        await session.merge(instance)
        await session.commit()
        await session.refresh(instance)
        return instance


order_crud = CRUDOrder(Order)
