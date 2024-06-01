import pygame as pg
from utils import GameSettings, Colors


class UI:
    def __init__(self) -> None:
        """Инициализация списка элементов пользовательского интерфейса."""
        self._game_settings = GameSettings
        self._colors = Colors()
        self._elements = []

    def add_element(self, element: pg.Surface) -> None:
        """Добавление элемента в список элементов пользовательского интерфейса."""
        self._elements.append(element)

    def draw(self, screen: pg.Surface) -> None:
        """Отрисовка элементов пользовательского интерфейса на экране."""
        for element in self._elements:
            element.draw(screen)


class Background:
    def __init__(self, color: pg.Color, size: tuple[int, int]) -> None:
        self._color = color
        self._size = size
        self._position = (0, 0)

        self.surface = pg.Surface(self._size)
        self.surface.fill(self._color)

        self.rect = self.surface.get_rect()
        self.rect.topleft = self._position

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Text:
    def __init__(self, text: str, size: int, color: pg.Color, position: tuple[int, int]) -> None:
        self._game_settings = GameSettings

        self._text = text
        self._size = size
        self._color = color
        self._position = position

        self.font = pg.font.Font(self._game_settings.GAME_BASE_FONT, self._size)
        self.surface = self.font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect()
        self.rect.center = self._position

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)

    def set_text(self, new_text: str) -> None:
        self._text = new_text
        self.surface = self.font.render(self._text, True, self._color)
        self.rect = self.surface.get_rect()
        self.rect.center = self._position
