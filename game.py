import pygame as pg
from scene_module.main_menu_scene import MainMenuScene
from scene_module.story_scene import StoryScene
from scene_module.game_scene import GameScene
from scene_module.ending_scene import EndingScene


class Game:
    def __init__(self, fps: int, screen: pg.Surface) -> None:
        self._fps = fps
        self._game_speed = 1.0
        self._delta_time = round(1 / self._fps, 3)

        self._screen = screen

        self._running = True
        self._paused = False

        self._scenes = {
            "main_menu": MainMenuScene(self),
            "story": StoryScene(self),
            "game": GameScene(self),
            "end": EndingScene(self)
        }
        self._current_scene = self._scenes["game"]

    def toggle_pause(self) -> None:
        """Переключение состояния паузы."""
        self._paused = not self._paused

    def is_game_paused(self) -> bool:
        """Возвращает True, если игра находится в состоянии паузы."""
        return self._paused

    def stop(self) -> None:
        """Останавливает игру."""
        self._running = False

    def is_game_running(self) -> bool:
        """Возвращает True, если игра запущена."""
        return self._running

    def update(self) -> None:
        """Обновляет сцену каждый кадр."""
        scaled_delta_time = self._delta_time * self._game_speed
        self._current_scene.update(scaled_delta_time)

    def render(self) -> None:
        """Отображение графики сцены на экране."""
        self._current_scene.render(self._screen)

    def handle_events(self, event: pg.event.Event) -> None:
        """Обработка событий, которые происходят на сцене."""
        self._current_scene.handle_events(event)

    def change_scene(self, scene_name: str) -> None:
        """Сменить сцену."""
        self._current_scene = self._scenes[scene_name]
