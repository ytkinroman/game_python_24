import pygame as pg
from scene import Scene


class Game:
    def __init__(self, fps: int) -> None:
        self.__running = True
        self._paused = False

        self._fps = fps
        self._game_speed = 1.0
        self._delta_time = round(1 / self._fps, 3)

        self._scenes = {
            "main_menu": MainMenuScene(self),
            "story": StoryScene(self),
            "game": GameScene(self),
            "ending": EndingScene(self)
        }
        self._current_scene = self._scenes["main_menu"]

    def toggle_pause(self) -> None:
        """Переключение состояния паузы."""
        self._paused = not self._paused

    def stop(self) -> None:
        """Останавливает игру."""
        self.__running = False

    def is_game_paused(self) -> bool:
        """Возвращает True, если игра находится в состоянии паузы."""
        return self._paused

    def is_game_running(self) -> bool:
        """Возвращает True, если игра запущена."""
        return self.__running

    def update(self) -> None:
        """Обновляет игру каждый кадр."""
        scaled_delta_time = self._delta_time * self._game_speed
        self._scene.update(scaled_delta_time)

    def render(self, screen: pg.Surface) -> None:
        """Отображение графики сцены на экране."""
        self._scene.render(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        """Обработка событий, которые происходят в сцене."""
        self._scene.handle_events(event)

    def change_scene(self, scene: Scene) -> None:
        """Сменить текущую сцену."""
        self._scene = scene
