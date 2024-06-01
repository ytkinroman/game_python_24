import pygame as pg
from scene_module.scene import Scene
from simple_ui import UIStory


class StoryScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._story_scene_ui = UIStory()

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self._story_scene_ui.is_next_story_text():
                    self._story_scene_ui.next_story_text()
                    self._story_scene_ui.set_story_text(self._story_scene_ui.get_story_current_text())

                    if self._story_scene_ui.get_current_index_story() == self._story_scene_ui.is_last_story:
                        self._story_scene_ui.set_ending_support_text()
                else:
                    self._game.change_scene("game")

    def render(self, screen: pg.Surface) -> None:
        self._story_scene_ui.draw(screen)
