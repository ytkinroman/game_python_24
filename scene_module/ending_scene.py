import pygame as pg
from scene_module.scene import Scene
from ui_module.ending_ui import UIEnding


class EndingScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._game = game
        self._ending_good = None
        self._final_scene_ui = UIEnding(self._game, self._ending_good)

    def set_good_ending(self):
        self._ending_good = True

    def set_bad_ending(self):
        self._ending_good = False

    def reset(self) -> None:
        self._ending_good = None

    def render(self, screen: pg.Surface) -> None:
        self._final_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._game.stop()
            elif event.key == pg.K_SPACE:
                self._game.new_game()
