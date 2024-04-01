from .base import Base
from sqlalchemy.orm import Mapped


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    category_id: Mapped[int]
    price: Mapped[int]

    def __str__(self):
        return (f'Название товара {self.name}, описание {self.description},'
                f'цена {self.price/100} BYN')
