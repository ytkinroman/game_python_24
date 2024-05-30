import pygame as pg
from utils import GameSettings, Colors
from player import Player


class UI:
    def __init__(self) -> None:
        """Инициализация списка элементов пользовательского интерфейса."""
        self.__elements = []

    def add_element(self, element: pg.Surface) -> None:
        """Добавление элемента в список элементов пользовательского интерфейса."""
        self.__elements.append(element)

    def draw(self, screen: pg.Surface) -> None:
        """Отрисовка элементов пользовательского интерфейса на экране."""
        for element in self.__elements:
            element.draw(screen)


class UIPause(UI):
    def __init__(self) -> None:
        """Инициализация пользовательского интерфейса паузы."""
        super().__init__()

        self.__game_settings = GameSettings()
        self.__colors = Colors()

        self.__pause_background = Background(self.__colors.COLOR_WHITE,(self.__game_settings.SCREEN_WIDTH, self.__game_settings.SCREEN_HEIGHT),(0, 0))
        self.__pause_background.surface.set_alpha(128)

        self.add_element(self.__pause_background)

        self.__pause_title = "Пауза"
        self.__pause_color = self.__colors.COLOR_BLACK
        self.__pause_size = 150
        self.__pause_position = (self.__game_settings.SCREEN_WIDTH * 0.15, self.__game_settings.SCREEN_HEIGHT * 0.07)  # ОТСТУП СЛЕВА 15%, СВЕРХУ 7% ЭКРАНА
        self.__pause = Text(self.__pause_title, self.__pause_size, self.__pause_color, self.__pause_position)

        self.add_element(self.__pause)

        self.__support_title = "Чтобы продолжить игру нажмите Esc (Эскейпт)."
        self.__support_color = self.__colors.COLOR_BLACK
        self.__support_size = 60
        self.__support_position = (self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT - (self.__game_settings.SCREEN_HEIGHT * 0.07))  # ОТСТУП 6% СНИЗУ ЭКРАНА
        self.__support = Text(self.__support_title, self.__support_size, self.__support_color, self.__support_position)

        self.add_element(self.__support)


class UIGamePlay(UI):
    def __init__(self) -> None:
        """Инициализация пользовательского игрового интерфейса."""
        super().__init__()

        self.__game_settings = GameSettings()
        self.__colors = Colors()

        self.__support_title = "* Не позволяйте Духам подойти слишком близко! *"
        self.__support_color = self.__colors.COLOR_WHITE
        self.__support_size = 60
        self.__support_position = (self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT - (self.__game_settings.SCREEN_HEIGHT * 0.06))
        self.support = Text(self.__support_title, self.__support_size, self.__support_color, self.__support_position)

        self.add_element(self.support)

        self.__score_title = "0000"
        self.__score_color = self.__colors.COLOR_WHITE
        self.__score_size = 80
        self.__score_position = (self.__game_settings.SCREEN_WIDTH - (self.__game_settings.SCREEN_WIDTH * 0.1), (self.__game_settings.SCREEN_HEIGHT * 0.05))
        self.score = Text(self.__score_title, self.__score_size, self.__score_color, self.__score_position)

        self.add_element(self.score)

    def update(self, player: Player):
        self.score.set_text("{:0>4d}".format(player.model.get_score()))


class UIMainMenu(UI):
    def __init__(self) -> None:
        """Инициализация интерфейса главного меню."""
        super().__init__()

        self.__game_settings = GameSettings()
        self.__colors = Colors()

        self.__background = Background(self.__colors.COLOR_WHITE,(self.__game_settings.SCREEN_WIDTH, self.__game_settings.SCREEN_HEIGHT),(0, 0))

        self.add_element(self.__background)

        self.__welcome_title = "Добро пожаловать в игру!"
        self.__welcome_color = self.__colors.COLOR_BLACK
        self.__welcome_size = 70
        self.__welcome_position = (self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT // 3)
        self.__welcome = Text(self.__welcome_title, self.__welcome_size, self.__welcome_color, self.__welcome_position)

        self.add_element(self.__welcome)

        self.__name_title = '"' + self.__game_settings.GAME_NAME + '"'
        self.__name_color = self.__colors.COLOR_GREEN
        self.__name_size = 90
        self.__name_position = (self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT // 2)
        self.__name = Text(self.__name_title, self.__name_size, self.__name_color, self.__name_position)

        self.add_element(self.__name)

        self.__support_title = "Чтобы начать игру нажмите Space (Пробел)."
        self.__support_color = self.__colors.COLOR_GRAY
        self.__support_size = 50
        self.__support_position = (self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT - (self.__game_settings.SCREEN_HEIGHT * 0.07))  # ОТСТУП СНИЗУ НА 7%
        self.__support = Text(self.__support_title, self.__support_size, self.__support_color, self.__support_position)

        self.add_element(self.__support)

        self.__author_title = "@" + self.__game_settings.GAME_AUTHOR_NICKNAME
        self.__author_color = self.__colors.COLOR_GRAY
        self.__author_size = 50
        self.__author_position = (self.__game_settings.SCREEN_WIDTH * 0.1, self.__game_settings.SCREEN_HEIGHT * 0.05)
        self.__author = Text(self.__author_title, self.__author_size, self.__author_color, self.__author_position)

        self.add_element(self.__author)


class Text:
    def __init__(self, text: str, size: int, color: pg.Color, position: tuple[int, int]) -> None:
        """Инициализация текстового элемента пользовательского интерфейса."""
        self.text = text
        self.size = size
        self.position = position
        self.game_settings = GameSettings
        self.color = color
        self.font = pg.font.Font(self.game_settings.GAME_BASE_FONT, self.size)
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=self.position)

    def draw(self, screen: pg.Surface) -> None:
        """Отрисовка текстового элемента на экране."""
        screen.blit(self.surface, self.rect)

    def set_text(self, new_text):
        """Изменение текста текстового элемента."""
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=self.position)


class Background:
    def __init__(self, color: pg.Color, size: tuple[int, int], position: tuple[int, int]) -> None:
        """Инициализация элемента фона."""
        self.__color = color
        self.__size = size
        self.__position = position

        self.surface = pg.Surface(self.__size)
        self.surface.fill(self.__color)

        self.rect = self.surface.get_rect()
        self.rect.topleft = self.__position

    def draw(self, screen: pg.Surface) -> None:
        """Отрисовка элемента фона на экране."""
        screen.blit(self.surface, self.rect)
