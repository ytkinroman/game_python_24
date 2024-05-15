import pygame as pg


class Scene:
    """Базовый класс для всех сцен в игре."""
    def __init__(self) -> None:
        """Инициализация сцены."""
        pass

    def handle_events(self, events: list[pg.event.Event]) -> None:
        """Обработка нажатий."""
        pass

    def update(self, delta_time: float) -> None:
        """Обновление состояния сцены."""
        pass

    def render(self, screen: pg.Surface) -> None:
        """Рендеринг сцены на экран."""
        pass

