from .handler_all_text import HandlerAllText
from .handler_commands import HandlerCommands


class HandlerMain:
    """
    Класс компоновщик
    """
    def __init__(self, bot):
        self.bot = bot
        self.handler_commands = HandlerCommands(self.bot)
        self.handler_all_text = HandlerAllText(self.bot)

    def handle(self):
        self.handler_commands.handle()
        self.handler_all_text.handle()
