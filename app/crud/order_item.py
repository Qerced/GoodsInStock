from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import OrderItem


class CRUDOrderItem(CRUDBase):
    async def get_by_product_id(
        self, session: AsyncSession, product_id: int
    ) -> OrderItem:
        instance = await session.execute(
            select(self.model).where(self.model.product_id == product_id)
        )
        return instance.scalar_one_or_none()

    async def create(
        self,
        session: AsyncSession,
        product_id: int,
        order_id: int,
        quantity: int
    ) -> OrderItem:
        instance = self.model(
            product_id=product_id, order_id=order_id, quantity=quantity
        )
        session.add(instance)
        return instance


order_item_crud = CRUDOrderItem(OrderItem)
