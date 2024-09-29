from http import HTTPStatus
from typing import Union

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import order_item_crud
from app.models import Order, OrderItem, Product

NOT_FOUND = 'No such object found in the database.'
QUANTITY_OF_GOODS = 'Incorrect quantity of goods'
EXISTING_ORDER = 'The item cannot be removed due to an existing order'


async def check_exists(
    instance: Union[Order, OrderItem, Product]
) -> Union[Order, OrderItem, Product]:
    if not instance:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=NOT_FOUND
        )
    return instance


async def check_quantity(instance: Product, expected_quantity: int) -> Product:
    if 0 < expected_quantity <= instance.quantity:
        return instance
    raise HTTPException(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        detail=QUANTITY_OF_GOODS
    )


async def check_can_be_deleted(
    session: AsyncSession, instance: Product
) -> Product:
    if await order_item_crud.get_by_product_id(session, instance.id):
        raise HTTPException(
            status_code=HTTPStatus.LOCKED,
            detail=EXISTING_ORDER
        )
    return instance
