import pygame as pg
from game_settings import GameSettings


class UI:
    def __init__(self) -> None:
        """Инициализация списка элементов пользовательского интерфейса."""
        self.elements = []

    def add_element(self, element: pg.Surface) -> None:
        """Добавление элемента в список элементов пользовательского интерфейса."""
        self.elements.append(element)

    def draw(self, screen: pg.Surface) -> None:
        """Отрисовка элементов пользовательского интерфейса на экране."""
        for element in self.elements:
            element.draw(screen)


class Text:
    def __init__(self, text: str, size: int, color: tuple[int, int, int], position: tuple[int, int, int]) -> None:
        """Инициализация текстового элемента пользовательского интерфейса."""
        self.text = text
        self.size = size
        self.position = position
        self.color = color
        self.font = pg.font.Font(GameSettings.game_base_font, self.size)
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
