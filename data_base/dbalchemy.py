from sqlalchemy.orm import sessionmaker
from core import setting
from core.models import Product
from sqlalchemy import create_engine
from .dbcore import Base
from os import path


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
        result = self._session.query(Product).filter_by(
            category_id=category).all()

        self.close()
        return result

    def close(self):
        """ Закрывает сессию """
        self._session.close()
