from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import check_can_be_deleted, check_exists
from app.core.db import get_async_session
from app.crud import product_crud
from app.schemas import ProductCreateDb

router = APIRouter()


@router.post("/", response_model=ProductCreateDb)
async def create_product(
    product: ProductCreateDb,
    session: AsyncSession = Depends(get_async_session)
):
    # TODO: check exists by name?
    return await product_crud.create(session, product)


@router.get("/{product_id}", response_model=ProductCreateDb)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return await check_exists(await product_crud.get(session, product_id))


@router.get("/", response_model=list[ProductCreateDb])
async def get_products(session: AsyncSession = Depends(get_async_session)):
    return await product_crud.get_list(session)


@router.put("/{product_id}", response_model=ProductCreateDb)
async def update_product(
    product_id: int,
    product_schema: ProductCreateDb,
    session: AsyncSession = Depends(get_async_session)
):
    return await product_crud.update(
        session,
        await check_exists(await product_crud.get(session, product_id)),
        product_schema
    )


@router.delete("/{product_id}", response_model=ProductCreateDb)
async def delete_product(
    product_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await product_crud.delete(
        session,
        await check_can_be_deleted(
            session,
            await check_exists(await product_crud.get(session, product_id))
        )
    )
