from sqlalchemy import Column, String, Boolean
from .base import Base


class Category(Base):
    """
    Класс-модель для описания таблицы "Категория товара",
    основан на декларативном стиле SQLAlchemy
    """

    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __str__(self):
        return self.name
