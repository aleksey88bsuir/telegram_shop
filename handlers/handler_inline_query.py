from handlers.handler import Handler
from core.message import MESSAGES


class HandlerInlineQuery(Handler):
    def __init__(self, bot):
        super().__init__(bot)

    def pressed_btn_product(self, call, code):
        self.BD._add_orders(1, code, int(call.id))
        name, title, price, quantity = self.BD.select_single_product_attrs(
            code)
        self.bot.answer_callback_query(
            call.id,
            MESSAGES.get('product_order').format(
                name, title, price, quantity),
            show_alert=True
            )

    def handle(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            code = call.data
            if code.isdigit():
                code = int(code)
            self.pressed_btn_product(call, code)
