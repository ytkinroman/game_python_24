import pygame as pg
from game_settings import GameSettings


class UI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)


class Text:
    def __init__(self, text: str, size: int, color, position) -> None:
        self.text = text
        self.size = size
        self.position = position
        self.color = color
        self.font = pg.font.Font(GameSettings.game_base_font, self.size)
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=self.position)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)

    def set_text(self, new_text):
        self.text = new_text
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=self.position)

