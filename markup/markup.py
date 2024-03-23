# импортируем специальные типы телеграм бота для создания элементов интерфейса
from telebot.types import KeyboardButton
from core import setting
from data_base.dbalchemy import DBManager


class Keyboards:
    """
    Класс Keyboards предназначен для создания и разметки интерфейса бота
    """

    def __init__(self):
        self.markup = None
        self.BD = DBManager()

    def set_btn(self, name, step=0, quantity=0):
        """
        Создает и возвращает кнопку по входным параметрам
        """
        return KeyboardButton(setting.KEYBOARD[name])
