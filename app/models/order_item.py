from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.db import Base


class OrderItem(Base):
    __table_args__ = (UniqueConstraint('product_id', 'order_id'),)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    order_id = Column(ForeignKey('order.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")
