from datetime import datetime

from pydantic import BaseModel

from app.schemas.order_item import OrderItemCreate


class OrderDb(BaseModel):
    id: int
    status: str
    created_at: datetime


class OrderWithItemDb(OrderDb):
    items: list[OrderItemCreate]
