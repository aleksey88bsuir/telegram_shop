from sqlalchemy.orm import sessionmaker

from core import setting
from core.models.product import Products
from core.models.order import Order
from core.utility import _convert

from sqlalchemy import create_engine
from .dbcore import Base
from os import path
from datetime import datetime


class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальную точку доступа.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """
    Класс менеджер для работы с БД
    """

    def __init__(self):
        """
        Инициализация сесии и подключения к БД
        """
        self.engine = create_engine(setting.DATABASE)
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(setting.DATABASE):
            Base.metadata.create_all(self.engine)

    def select_all_products_category(self, category):
        """
        Возвращает все товары категории
        """
        result = self._session.query(Products).filter_by(
            category_id=category).all()

        self.close()
        return result

    def close(self):
        """ Закрывает сессию """
        self._session.close()

    def _add_orders(self, quantity, product_id, user_id):
        all_id_product = self.select_all_product_id()
        quantity_product = self.select_single_product_quantity(product_id)
        if product_id in all_id_product:
            if quantity_product < quantity:
                print("Недостаточно товара на складе.")
                return
            quantity_order = self.select_order_quantity(product_id)
            quantity_order += 1
            self.update_order_value(product_id, 'quantity', quantity_order)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        else:
            if quantity_product < quantity:
                print("Недостаточно товара на складе.")
                return
            order = Order(quantity=quantity, product_id=product_id,
                          user_id=user_id, data=datetime.now())
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_product_id(self):
        result = self._session.query(Order.product_id).all()
        self.close()
        return _convert(result)

    def update_order_value(self, product_id, name, value):
        self._session.query(Order).filter_by(
            product_id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def update_product_value(self, rownum, name, value):
        self._session.query(Products).filter_by(id=rownum).update({name: value})
        self._session.commit()
        self.close()

    def select_order_quantity(self, product_id):
        result = self._session.query(Order.quantity).filter_by(
            product_id=product_id).one()
        self.close()
        return result.quantity

    def count_rows_order(self):
        result = self._session.query(Order).count()
        self.close()
        return result

    def select_single_product_title(self, rownum):
        result = self._session.query(Products.title).filter_by(id=rownum).one()
        self.close()
        return result.title

    def select_single_product_name(self, rownum):
        result = self._session.query(Products.name).filter_by(id=rownum).one()
        self.close()
        return result.name

    def select_single_product_quantity(self, rownum):
        result = self._session.query(
            Products.quantity).filter_by(id=rownum).one()
        self.close()
        return result.quantity

    def select_single_product_price(self, rownum):
        result = self._session.query(Products.price).filter_by(id=rownum).one()
        self.close()
        return result.price

    def select_single_product_attrs(self, rownum):
        result = self._session.query(Products.name,
                                     Products.title,
                                     Products.price,
                                     Products.quantity).filter_by(
            id=rownum
        ).one()
        self.close()
        return result.name, result.title, result.price, result.quantity

    def delete_order(self, product_id):
        self._session.query(Order).filter_by(product_id=product_id).delete()
        self._session.commit()
        self.close()

    def delete_all_order(self):
        all_id_orders = self.select_all_order_id()
        for itm in all_id_orders:
            self._session.query(Order).filter_by(id=itm).delete()
            self._session.commit()
        self.close()

    def select_all_order_id(self):
        result = self._session.query(Order.id).all()
        self.close()
        return _convert(result)
