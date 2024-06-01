import pygame as pg
from scene_module.scene import Scene
from simple_ui import UIMainMenu


class MainMenuScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._menu_scene_ui = UIMainMenu()

    def render(self, screen: pg.Surface) -> None:
        self._menu_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self._game.change_scene("story")
