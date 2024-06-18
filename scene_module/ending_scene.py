import pygame as pg
from scene_module.scene import Scene
from ui_module.ending_ui import UIEnding


class EndingScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._game = game
        self._ending_good = None
        self._final_scene_ui = None
        self._score = 0

    def set_good_ending(self):
        self._ending_good = True
        self._final_scene_ui = UIEnding(self._game, self._ending_good, self._score)

    def set_bad_ending(self):
        self._ending_good = False
        self._final_scene_ui = UIEnding(self._game, self._ending_good, self._score)

    def set_score(self, score):
        self._score = score

    def render(self, screen: pg.Surface) -> None:
        self._final_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        self._final_scene_ui.handle_events(event)
