from ui_module.ui import UI, Text, Background
import pygame as pg


class UIEnding(UI):
    def __init__(self, game, ending_good, score) -> None:
        super().__init__()

        self._game = game
        self._ending_good = ending_good
        self._score = score

        self._background = Background(self._colors.COLOR_BLACK, (self._game_settings.SCREEN_WIDTH, self._game_settings.SCREEN_HEIGHT))
        self.add_element(self._background)

        self.__text_title = "* Конец истории *"
        self.__text_color = self._colors.COLOR_WHITE
        self.__text_size = 80
        self.__text_position = (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT // 2)
        self.__text = Text(self.__text_title, self.__text_size, self.__text_color, self.__text_position)
        self.add_element(self.__text)

        if self._ending_good:
            self.__description_title = "Волшебник убежал, с ним остался костюм курицы... (Хорошая концовка)"
            self.__description_color = self._colors.COLOR_GREEN
        else:
            self.__description_title = "Волшебник, погиб оказавшийся в безвыходном положении... (Плохая концовка)"
            self.__description_color = self._colors.COLOR_RED

        self.__description_size = 45
        self.__description_position = (self._game_settings.SCREEN_WIDTH // 2, (self._game_settings.SCREEN_HEIGHT // 2) + (self._game_settings.SCREEN_HEIGHT * 0.07))
        self.__description = Text(self.__description_title, self.__description_size, self.__description_color, self.__description_position)
        self.add_element(self.__description)

        self.__score_title = str(self._score)
        self.__score_color = self._colors.COLOR_WHITE
        self.__score_size = 80
        self.__score_position = (self._game_settings.SCREEN_WIDTH // 2, (self._game_settings.SCREEN_HEIGHT * 0.05))
        self.__score = Text(self.__score_title, self.__score_size, self.__score_color,self.__score_position)
        self.add_element(self.__score)

        self.__support_title = "Чтобы выйти из игры нажмите Esc (Эскейпт)."
        self.__support_color = self._colors.COLOR_GRAY
        self.__support_size = 40
        self.__support_position = (self._game_settings.SCREEN_WIDTH // 2, (self._game_settings.SCREEN_HEIGHT - (self._game_settings.SCREEN_HEIGHT * 0.05)))
        self.__support = Text(self.__support_title, self.__support_size, self.__support_color,self.__support_position)
        self.add_element(self.__support)

        self.__replay_title = "Чтобы поиграть ещё раз нажмите Space (Пробел)."
        self.__replay_color = self._colors.COLOR_GRAY
        self.__replay_size = 40
        self.__replay_position = (self._game_settings.SCREEN_WIDTH // 2, (self._game_settings.SCREEN_HEIGHT - (self._game_settings.SCREEN_HEIGHT * 0.10)))
        self.__replay = Text(self.__replay_title, self.__replay_size, self.__replay_color, self.__replay_position)
        self.add_element(self.__replay)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._game.stop()
                elif event.key == pg.K_SPACE:
                    self._game.new_game()
