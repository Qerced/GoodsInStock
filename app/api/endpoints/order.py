from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import check_exists, check_quantity
from app.core.db import get_async_session
from app.crud.order import order_crud
from app.crud.order_item import order_item_crud
from app.crud.product import product_crud
from app.models.order import OrderStatus
from app.schemas import OrderDb, OrderItemCreate, OrderWithItemDb

router = APIRouter()


@router.post("/", response_model=OrderDb)
async def create_order(
    order_schema: list[OrderItemCreate],
    session: AsyncSession = Depends(get_async_session)
):
    async with session.begin():
        new_order = await order_crud.create(session)
        for item in order_schema:
            product = await check_quantity(
                await check_exists(
                    await product_crud.get(session, item.product_id, True)
                ),
                item.quantity
            )
            product.quantity -= item.quantity
            await order_item_crud.create(
                session, product.id, new_order.id, item.quantity
            )
    await session.refresh(new_order)
    return new_order


@router.get("/{order_id}", response_model=OrderWithItemDb)
async def get_order(
    order_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await check_exists(
        await order_crud.get_with_related(session, order_id)
    )


@router.get("/", response_model=list[OrderDb])
async def get_orders(session: AsyncSession = Depends(get_async_session)):
    return await order_crud.get_list(session)


@router.patch("/{order_id}", response_model=OrderDb)
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    session: AsyncSession = Depends(get_async_session)
):
    return await order_crud.update(
        session,
        await check_exists(await order_crud.get(session, order_id, True)),
        status
    )
