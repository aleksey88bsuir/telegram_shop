from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from core.models.product import Product
from .base import Base


class Order(Base):
    """
    Класс для создания таблицы "Заказ",
    основан на декларативном стиле SQLAlchemy
    """
    quantity = Column(Integer)
    data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer)

    # для каскадного удаления данных из таблицы
    products = relationship(
        Product,
        backref=backref('orders',
                        uselist=True,
                        cascade='delete,all'))

    def __str__(self):
        return f"{self.quantity} {self.data}"
