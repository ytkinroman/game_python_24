import pygame as pg


class Scene:
    """Базовый класс для всех сцен в игре."""
    def __init__(self, game) -> None:
        self._game = game

    def handle_events(self, event: pg.event.Event) -> None:
        """Обработка нажатий."""
        pass

    def update(self, delta_time: float) -> None:
        """Обновление сцены."""
        pass

    def render(self, screen: pg.Surface) -> None:
        """Рендеринг сцены на экран."""
        pass
