import pygame as pg
from scene_module.scene import Scene
from ui_module.story_ui import UIStory


class StoryScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._story_scene_ui = UIStory(self._game)

    def render(self, screen: pg.Surface) -> None:
        self._story_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        self._story_scene_ui.handle_events(event)
