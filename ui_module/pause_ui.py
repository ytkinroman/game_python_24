from ui_module.ui import UI, Text, Background


class UIPause(UI):
    def __init__(self, player, scene) -> None:
        super().__init__()
        self.__player = player
        self.__scene = scene

        self.__pause_background = Background(self._colors.COLOR_WHITE, (self._game_settings.SCREEN_WIDTH, self._game_settings.SCREEN_HEIGHT))
        self.__pause_background.surface.set_alpha(128)
        self.add_element(self.__pause_background)

        self.__pause_title = "Пауза"
        self.__pause_color = self._colors.COLOR_BLACK
        self.__pause_size = 160
        self.__pause_position = (self._game_settings.SCREEN_WIDTH * 0.16, self._game_settings.SCREEN_HEIGHT * 0.08)
        self.__pause = Text(self.__pause_title, self.__pause_size, self.__pause_color, self.__pause_position)
        self.add_element(self.__pause)

        self.__score_current = self.__player.get_score()
        self.__score_win = self.__scene.get_win_score()
        self.__score_title = f"{self.__score_current}/{self.__score_win}"
        self.__score_color = self._colors.COLOR_BLACK
        self.__score_size = 80
        self.__score_position = (self._game_settings.SCREEN_WIDTH * 0.16, self._game_settings.SCREEN_HEIGHT * 0.20)
        self.__score = Text(self.__score_title, self.__score_size, self.__score_color,self.__score_position)
        self.add_element(self.__score)

        self.__support_title = "Чтобы продолжить игру нажмите Esc (Эскейпт)."
        self.__support_color = self._colors.COLOR_BLACK
        self.__support_size = 60
        self.__support_position = (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT - (self._game_settings.SCREEN_HEIGHT * 0.07))
        self.__support = Text(self.__support_title, self.__support_size, self.__support_color,self.__support_position)
        self.add_element(self.__support)

    def update(self):
        self.__score_current = self.__player.get_score()
        score = f"{self.__score_current}/{self.__score_win}"
        self.__score.set_text(score)
