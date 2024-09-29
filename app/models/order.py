import enum

from sqlalchemy import Column, DateTime, Enum, func
from sqlalchemy.orm import relationship

from app.core.db import Base


class OrderStatus(enum.Enum):
    IN_PROGRESS = 'in progress'
    SENT = 'sent'
    DELIVERED = 'delivered'


class Order(Base):
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(
        Enum(OrderStatus, name='status_order'),
        nullable=False,
        default=OrderStatus.IN_PROGRESS
    )
    items = relationship('OrderItem', back_populates='order')
