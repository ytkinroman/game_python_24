import pygame as pg
from scene_module.scene import Scene
from ui_module.story_ui import UIStory


class StoryScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._story_scene_ui = UIStory(self._game)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self._story_scene_ui.next_story_text()

    def render(self, screen: pg.Surface) -> None:
        self._story_scene_ui.draw(screen)
