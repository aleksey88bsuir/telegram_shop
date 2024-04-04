from core.message import MESSAGES
from core import setting
from handlers.handler import Handler


class HandlerAllText(Handler):
    """
    Класс обрабатывает входящие текстовые сообщения от нажатия на кнопки
    """
    def __init__(self, bot):
        super().__init__(bot)
        # шаг в заказе
        self.step = 0

    def pressed_btn_info(self, message):
        """
        обрабатывает входящие текстовые сообщения
        от нажатия на кнопку 'О магазине'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        """
        обрабатывает входящие текстовые сообщения
        от нажатия на кнопку 'Настройки'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_back(self, message):
        """
        обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Назад'.
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_category(self, message):
        """
        Обработка события нажатия на кнопку 'Выбрать товар'. А точнеe
        это выбор категории товаров
        """
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keybords.category_menu())

    # def pressed_btn_product2(self, message, product):
    #     """
    #     Обработка события нажатия на кнопку 'Выбрать товар'. А точнее
    #     это выбор товара из категории
    #     """
    #     product_info = self.get_product_info(product) # Предполагается, что у вас есть метод для получения информации о продукте
    #     formatted_message = f"""
    #     <b>{product_info.name}</b>
    #     <i>{product_info.description}</i>
    #     <code>{product_info.price/100} BYN</code>
    #     """
    #     self.bot.send_message(
    #         message.chat.id,
    #         formatted_message,
    #         parse_mode="HTML",
    #         reply_markup=self.keybords.set_select_category(
    #             setting.CATEGORY[product])
    #     )
    #     self.bot.send_message(message.chat.id, "Ок", reply_markup=self.keybords.category_menu())

    def pressed_btn_product(self, message, product):
        """
        Обработка события нажатия на кнопку 'Выбрать товар'. А точнее
        это выбор товара из категории
        """
        self.bot.send_message(message.chat.id, 'Категория ' +
                              setting.KEYBOARD[product],
                              reply_markup=self.keybords.set_select_category(
                                  setting.CATEGORY[product]))
        self.bot.send_message(message.chat.id, "Ок",
                              reply_markup=self.keybords.category_menu())

    # def handle(self):
    #     @self.bot.message_handler(func=lambda message: True)
    #     def handle(message):
    #         # ********** меню ********** #
    #
    #         if message.text == setting.KEYBOARD['INFO']:
    #             self.pressed_btn_info(message)
    #
    #         if message.text == setting.KEYBOARD['SETTINGS']:
    #             self.pressed_btn_settings(message)
    #
    #         if message.text == setting.KEYBOARD['<<']:
    #             self.pressed_btn_back(message)
    #
    #         if message.text == setting.KEYBOARD['CHOOSE_GOODS']:
    #             self.pressed_btn_category(message)
    #
    #         if message.text == setting.KEYBOARD['SEMIPRODUCT']:
    #             self.pressed_btn_product(message, 'SEMIPRODUCT')
    #
    #         if message.text == setting.KEYBOARD['GROCERY']:
    #             self.pressed_btn_product(message, 'GROCERY')
    #
    #         if message.text == setting.KEYBOARD['ICE_CREAM']:
    #             self.pressed_btn_product(message, 'ICE_CREAM')
    #
    #         if message.text == setting.KEYBOARD['AUTO']:
    #             self.pressed_btn_product(message, 'AUTO')

    def handle(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            special_actions = {
                setting.KEYBOARD['INFO']: self.pressed_btn_info,
                setting.KEYBOARD['SETTINGS']: self.pressed_btn_settings,
                setting.KEYBOARD['<<']: self.pressed_btn_back,
                setting.KEYBOARD['CHOOSE_GOODS']: self.pressed_btn_category,
                setting.KEYBOARD['SEMIPRODUCT']:
                    lambda message_:
                    self.pressed_btn_product(message_, 'SEMIPRODUCT'),
                setting.KEYBOARD['GROCERY']:
                    lambda message_:
                    self.pressed_btn_product(message_, 'GROCERY'),
                setting.KEYBOARD['ICE_CREAM']:
                    lambda message_:
                    self.pressed_btn_product(message_, 'ICE_CREAM'),
                setting.KEYBOARD['AUTO']:
                    lambda message_:
                    self.pressed_btn_product(message_, 'AUTO'),
            }

            for action, rule in special_actions.items():
                if message.text == action:
                    rule(message)
                    break
            else:
                self.bot.send_message(
                    message.chat.id,
                    "Данная кнопка не работает...",
                    reply_markup=self.keybords.start_menu()
                )
