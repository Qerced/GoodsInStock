from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Order, OrderItem, Product


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def get(
        self, session: AsyncSession, id: int, for_update: bool = False
    ) -> Union[Order, OrderItem, Product]:
        if for_update:
            instance = await session.execute(
                select(self.model).with_for_update().where(self.model.id == id)
            )
        else:
            instance = await session.execute(
                select(self.model).where(self.model.id == id)
            )

        return instance.scalar_one_or_none()

    async def get_list(
        self, session: AsyncSession
    ) -> List[Union[Order, OrderItem, Product]]:
        instances = await session.execute(select(self.model))
        return instances.scalars().all()
