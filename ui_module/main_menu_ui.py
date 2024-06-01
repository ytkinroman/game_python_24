from ui_module.ui import UI, Text, Background


class UIMainMenu(UI):
    def __init__(self) -> None:
        """Инициализация интерфейса главного меню."""
        super().__init__()

        self.__background = Background(self._colors.COLOR_WHITE,(self._game_settings.SCREEN_WIDTH, self._game_settings.SCREEN_HEIGHT))
        self.add_element(self.__background)

        self.__welcome_title = "Добро пожаловать в игру!"
        self.__welcome_color = self._colors.COLOR_BLACK
        self.__welcome_size = 65
        self.__welcome_position = (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT // 3)
        self.__welcome = Text(self.__welcome_title, self.__welcome_size, self.__welcome_color, self.__welcome_position)
        self.add_element(self.__welcome)

        self.__name_title = '"' + self._game_settings.GAME_NAME + '"'
        self.__name_color = self._colors.COLOR_GREEN
        self.__name_size = 90
        self.__name_position = (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT // 2)
        self.__name = Text(self.__name_title, self.__name_size, self.__name_color, self.__name_position)
        self.add_element(self.__name)

        self.__support_title = "Чтобы начать игру нажмите Space (Пробел)."
        self.__support_color = self._colors.COLOR_GRAY
        self.__support_size = 50
        self.__support_position = (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT - (self._game_settings.SCREEN_HEIGHT * 0.07))
        self.__support = Text(self.__support_title, self.__support_size, self.__support_color, self.__support_position)
        self.add_element(self.__support)

        self.__author_title = self._game_settings.GAME_AUTHOR
        self.__author_color = self._colors.COLOR_GRAY
        self.__author_size = 50
        self.__author_position = (self._game_settings.SCREEN_WIDTH * 0.15, self._game_settings.SCREEN_HEIGHT * 0.05)
        self.__author = Text(self.__author_title, self.__author_size, self.__author_color, self.__author_position)
        self.add_element(self.__author)

        self.__author_group_title = self._game_settings.GAME_AUTHOR_GROUP
        self.__author_group_color = self._colors.COLOR_GRAY
        self.__author_group_size = 50
        self.__author_group_position = (self._game_settings.SCREEN_WIDTH * 0.15, self._game_settings.SCREEN_HEIGHT * 0.1)
        self.__author_group = Text(self.__author_group_title, self.__author_group_size, self.__author_group_color, self.__author_group_position)
        self.add_element(self.__author_group)
