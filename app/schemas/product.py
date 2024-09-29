from pydantic import BaseModel


class ProductCreateDb(BaseModel):
    title: str
    description: str
    price: float
    quantity: int
