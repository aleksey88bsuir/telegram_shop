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
        Обрабатывает входящие текстовые сообщения
        от нажатия на кнопку 'О магазине'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['trading_store'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.info_menu())

    def pressed_btn_settings(self, message):
        """
        Обрабатывает входящие текстовые сообщения
        от нажатия на кнопку 'Настройки'.
        """
        self.bot.send_message(message.chat.id, MESSAGES['settings'],
                              parse_mode="HTML",
                              reply_markup=self.keybords.settings_menu())

    def pressed_btn_back(self, message):
        """
        Обрабатывает входящие текстовые сообщения от нажатия на кнопку 'Назад'.
        """
        self.bot.send_message(message.chat.id, "Вы вернулись назад",
                              reply_markup=self.keybords.start_menu())

    def pressed_btn_category(self, message):
        """
        Обработка события нажатия на кнопку 'Выбрать товар'. А точнее
        это выбор категории товаров
        """
        self.bot.send_message(message.chat.id, "Каталог категорий товара",
                              reply_markup=self.keybords.remove_menu())
        self.bot.send_message(message.chat.id, "Сделайте свой выбор",
                              reply_markup=self.keybords.category_menu())

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

    def pressed_btn_orders(self, message):
        self.step = 0
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def send_message_order(self, product_id, quantity, message):
        self.bot.send_message(
            message.chat.id,
            MESSAGES['order_number'].format(self.step+1),
            parse_mode="HTML"
        )
        name, title, price, quantity_ = self.BD.select_single_product_attrs(
            product_id)
        self.bot.send_message(
            message.chat.id,
            MESSAGES['order'].format(name, title, price, quantity),
            parse_mode="HTML",
            reply_markup=self.keybords.orders_menu(
                self.step, quantity
            )
        )

    def pressed_btn_up(self, message):
        count = self.BD.select_all_product_id()
        quantity_order = self.BD.select_order_quantity(count[self.step])
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        if quantity_product > 0:
            quantity_order += 1
            quantity_product -= 1
            self.BD.update_order_value(count[self.step],
                                       'quantity',
                                       quantity_order)
            self.BD.update_product_value(count[self.step],
                                         'quantity',
                                         quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_down(self, message):
        count = self.BD.select_all_product_id()
        quantity_order = self.BD.select_order_quantity(count[self.step])
        quantity_product = self.BD.select_single_product_quantity(
            count[self.step])
        if quantity_order > 0:
            quantity_order -= 1
            quantity_product += 1
            self.BD.update_order_value(count[self.step],
                                       'quantity',
                                       quantity_order)
            self.BD.update_product_value(count[self.step],
                                         'quantity',
                                         quantity_product)
        self.send_message_order(count[self.step], quantity_order, message)

    def pressed_btn_x(self, message):
        count = self.BD.select_all_product_id()
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(count[self.step])
            quantity_product = self.BD.select_single_product_quantity(
                count[self.step])
            quantity_product += quantity_order
            self.BD.delete_order(count[self.step])
            self.BD.update_product_value(count[self.step],
                                         'quantity',
                                         quantity_product)
            self.step -= 1
        count = self.BD.select_all_product_id()
        if count.__len__() > 0:
            quantity_order = self.BD.select_order_quantity(
                count[self.step]
            )
            self.send_message_order(count[self.step], quantity_order, message)
        else:
            self.bot.send_message(message.chat.id, MESSAGES['no_orders'],
                                  parse_mode="HTML",
                                  reply_markup=self.keybords.orders_menu())

    def pressed_btn_back_step(self, message):
        if self.step > 0:
            self.step -= 1
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_next_step(self, message):
        if self.step < self.BD.count_rows_order()-1:
            self.step += 1
        count = self.BD.select_all_product_id()
        quantity = self.BD.select_order_quantity(count[self.step])
        self.send_message_order(count[self.step], quantity, message)

    def pressed_btn_apllay(self):
        pass

    def handle(self):
        @self.bot.message_handler(func=lambda message: True)
        def handle(message):
            special_actions = {
                setting.KEYBOARD['INFO']: self.pressed_btn_info,
                setting.KEYBOARD['SETTINGS']: self.pressed_btn_settings,
                setting.KEYBOARD['<<']: self.pressed_btn_back,
                setting.KEYBOARD['CHOOSE_GOODS']: self.pressed_btn_category,
                setting.KEYBOARD['ORDER']: self.pressed_btn_orders,
                setting.KEYBOARD['UP']: self.pressed_btn_up,
                setting.KEYBOARD['DOWN']: self.pressed_btn_down,
                setting.KEYBOARD['X']: self.pressed_btn_x,
                setting.KEYBOARD['BACK_STEP']: self.pressed_btn_back_step,
                setting.KEYBOARD['NEXT_STEP']: self.pressed_btn_next_step,
                setting.KEYBOARD['PLACE_AN_ORDER']: self.pressed_btn_apllay,
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
