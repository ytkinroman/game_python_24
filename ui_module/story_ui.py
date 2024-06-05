from ui_module.ui import UI, Text, Background
from story import StoryText
import pygame as pg


class UIStory(UI):
    def __init__(self, game) -> None:
        super().__init__()

        self._game = game

        self.__background = Background(self._colors.COLOR_WHITE, (self._game_settings.SCREEN_WIDTH, self._game_settings.SCREEN_HEIGHT))
        self.add_element(self.__background)

        self.__description_title = "* Режим истории *"
        self.__description_color = self._colors.COLOR_GRAY
        self.__description_size = 60
        self.__description_position = (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT * 0.05)
        self.__description = Text(self.__description_title, self.__description_size, self.__description_color, self.__description_position)
        self.add_element(self.__description)

        self.__support_title = "Чтобы продолжить повествование нажмите Enter..."
        self.__support_title_ending = "История закончилась. Нажмите Enter, чтобы начать играть."
        self.__support_color = self._colors.COLOR_GRAY
        self.__support_size = 50
        self.__support_x = self._game_settings.SCREEN_WIDTH // 2
        self.__support_y = (self._game_settings.SCREEN_HEIGHT - (self._game_settings.SCREEN_HEIGHT * 0.05))
        self.__support_position = (self.__support_x, self.__support_y)
        self.__support = Text(self.__support_title, self.__support_size, self.__support_color, self.__support_position)
        self.add_element(self.__support)

        self.__story_list = ["Эта история о противостоянии добра и зла.",
                             "Вы - величайший маг, обитатель мирной деревни \"Гринвич\".",
                             "Всё случилось во время праздника костюмов...",
                             "На вашу деревню напал злодей - неизвестный колдун.",
                             "Он призвал духов огня, чтобы уничтожить ваш любимый дом.",
                             "В панике вы бросились бежать со всех ног...",
                             "Оставив позади всех и всё, что у вас было.",
                             "...",
                             "Даже не успели снять праздничный костюм...",
                             "...",
                             "Всё оказалось не так просто...",
                             "Кажется, вы попали в засаду..."]
        self.__story_texts = StoryText(self.__story_list)

        self.__story_title = self.__story_texts.get_current_text()
        self.__story_color = self._colors.COLOR_BLACK
        self.__story_size = 55
        self.__story_x = self._game_settings.SCREEN_WIDTH // 2
        self.__story_y = self._game_settings.SCREEN_HEIGHT // 2
        self.__story_position = (self.__story_x, self.__story_y)
        self.__story = Text(self.__story_title, self.__story_size, self.__story_color, self.__story_position)
        self.add_element(self.__story)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self.__story_texts.is_next_text():
                    self.__story_texts.next_text()
                    self.__story.set_text(self.__story_texts.get_current_text())

                    if self.__story_texts.get_current_index() == self.__story_texts.get_texts_length() - 1:
                        self.__support.set_text(self.__support_title_ending)
                else:
                    self._game.change_scene("game")
