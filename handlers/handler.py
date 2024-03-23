import abc
# импортируем разметку клавиатуры и клавиш
from markup.markup import Keyboards
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot):
        self.bot = bot
        self.keybords = Keyboards()
        self.BD = DBManager()

    @abc.abstractmethod
    def handle(self):
        pass
