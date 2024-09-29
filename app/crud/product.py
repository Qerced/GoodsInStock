from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Product
from app.schemas import ProductCreateDb


class CRUDProduct(CRUDBase):
    async def create(
        self, session: AsyncSession, schema: ProductCreateDb
    ) -> Product:
        instance = self.model(**schema.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def update(
        self, session: AsyncSession, instance: Product, schema: ProductCreateDb
    ) -> Product:
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(instance, field, value)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def delete(
        self, session: AsyncSession, instance: Product
    ) -> Product:
        await session.delete(instance)
        await session.commit()
        return instance


product_crud = CRUDProduct(Product)
