from ui_module.ui import UI, Text


class UIGamePlay(UI):
    def __init__(self, player) -> None:
        super().__init__()

        self._player = player

        self.__support_title = "* Не позволяйте Духам подойти слишком близко! *"
        self.__support_color = self._colors.COLOR_WHITE
        self.__support_size = 60
        self.__support_position = (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT - (self._game_settings.SCREEN_HEIGHT * 0.06))
        self.support = Text(self.__support_title, self.__support_size, self.__support_color, self.__support_position)
        self.add_element(self.support)

        self.__score_title = "0000"
        self.__score_color = self._colors.COLOR_WHITE
        self.__score_size = 90
        self.__score_position = (self._game_settings.SCREEN_WIDTH - (self._game_settings.SCREEN_WIDTH * 0.1), (self._game_settings.SCREEN_HEIGHT * 0.05))
        self.score = Text(self.__score_title, self.__score_size, self.__score_color, self.__score_position)
        self.add_element(self.score)

    def update(self):
        self.score.set_text("{:0>4d}".format(self._player.get_score()))
