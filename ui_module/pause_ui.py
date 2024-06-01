from ui_module.ui import UI, Text, Background


class UIPause(UI):
    def __init__(self) -> None:
        super().__init__()

        self.__pause_background = Background(self._colors.COLOR_WHITE, (self._game_settings.SCREEN_WIDTH, self._game_settings.SCREEN_HEIGHT))
        self.__pause_background.surface.set_alpha(128)
        self.add_element(self.__pause_background)

        self.__pause_title = "Пауза"
        self.__pause_color = self._colors.COLOR_BLACK
        self.__pause_size = 150
        self.__pause_position = (self._game_settings.SCREEN_WIDTH * 0.15, self._game_settings.SCREEN_HEIGHT * 0.07)
        self.__pause = Text(self.__pause_title, self.__pause_size, self.__pause_color, self.__pause_position)

        self.add_element(self.__pause)

        self.__support_title = "Чтобы продолжить игру нажмите Esc (Эскейпт)."
        self.__support_color = self._colors.COLOR_BLACK
        self.__support_size = 60
        self.__support_position = (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT - (self._game_settings.SCREEN_HEIGHT * 0.07))
        self.__support = Text(self.__support_title, self.__support_size, self.__support_color,self.__support_position)
        self.add_element(self.__support)
