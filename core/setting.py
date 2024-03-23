import os
from emoji import emojize


TOKEN = '6899962628:AAFyonrDwTtJKH1i8HxgmBTEpsROKUyLz0I'
NAME_DB = 'R-443Y_shop.db'
VERSION = '0.0.1'
AUTHOR = 'R-443Y_company'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(f'sqlite:///{BASE_DIR}', NAME_DB)

COUNT = 0

# кнопки управления
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'SEMIPRODUCT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
    'AUTO': emojize('🚘 автомобили'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLAY': '✅ Оформить заказ',
    'COPY': '©️'
}

# id категорий продуктов
CATEGORY = {
    'SEMIPRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3,
    'AUTO': 4,
}

# названия команд
COMMANDS = {
    'START': "start",
    'HELP': "help",
}
