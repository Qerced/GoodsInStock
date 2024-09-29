from sqlalchemy import Column, Float, Integer, String

from app.core.db import Base


class Product(Base):
    title = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
