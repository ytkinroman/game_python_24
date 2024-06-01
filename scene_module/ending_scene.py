import pygame as pg
from scene_module.scene import Scene
from ui_module.ending_ui import UIEnding


class EndingScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._final_scene_ui = UIEnding(self._game)

    def render(self, screen: pg.Surface) -> None:
        self._final_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._game.stop()
            elif event.key == pg.K_SPACE:
                pass
                # self._game.change_scene("game")
