import random
import pygame as pg
from entities.ghost import Ghost
from entities.player import Player


class Point:
    def __init__(self, x_position: int, y_position: int) -> None:
        """Создаёт точку."""
        self.__x = x_position
        self.__y = y_position

    def get_position(self) -> tuple[int, int]:
        """Возвращает координаты точки."""
        return self.__x, self.__y


class Spawner:
    def __init__(self) -> None:
        self.__points = []

    def add_point(self, x_position: int, y_position: int) -> None:
        """Добавляет в спавнер новую точку."""
        self.__points.append(Point(x_position, y_position))

    def add_points(self, points: list[tuple[int, int]]) -> None:
        """Добавляет в спавнер несколько новых точек."""
        for point in points:
            self.__points.append(Point(point[0], point[1]))

    def get_random_point(self) -> tuple[int, int]:
        """Возвращает координаты случайной точки из спавнера."""
        return random.choice(self.__points).get_position()


class GhostSpawner(Spawner):
    def __init__(self, spawn_interval: float, spawn_group: pg.sprite.Group, player: Player) -> None:
        super().__init__()
        self.__spawn_interval = spawn_interval
        self.__ghost_group = spawn_group
        self.__player = player

        self.__spawn_interval_controller = SpawnIntervalController(self)

        self.__is_active = False

        self.__start_delay_timer = 6
        self.__last_spawn_time = 0

    def update(self, scaled_delta_time: float) -> None:
        """Обновляет состояние спавнера."""
        if self.__is_active:
            if self.__player.is_alive():
                if self.__start_delay_timer > 0:
                    self.__start_delay_timer -= scaled_delta_time
                    return

                self.__last_spawn_time += scaled_delta_time

                if self.__last_spawn_time >= self.__spawn_interval:
                    self.__last_spawn_time = 0
                    self.__spawn_ghost()

        self.__spawn_interval_controller.update(self.__player.get_score())

    def __spawn_ghost(self) -> None:
        """Спавнер Духов."""
        random_point_position_x, random_point_position_y = self.get_random_point()
        ghost = Ghost(random_point_position_x, random_point_position_y, self.__player)
        self.__ghost_group.add(ghost)

    def get_spawn_interval(self) -> float:
        """Возвращает текущий интервал спавна."""
        return self.__spawn_interval

    def set_spawn_interval(self, new_interval: float) -> None:
        """Устанавливаем новый интервал."""
        self.__spawn_interval = new_interval

    def set_active(self) -> None:
        """Активирует спавнер."""
        self.__is_active = True

    def stop_active(self) -> None:
        """Деактивирует спавнер."""
        self.__is_active = False

    def is_active(self) -> bool:
        """Возвращает True если активный."""
        return self.__is_active


class SpawnIntervalController:
    def __init__(self, ghost_spawner: GhostSpawner):
        self.__ghost_spawner = ghost_spawner
        self.__base_interval = self.__ghost_spawner.get_spawn_interval()
        self.__interval_decrease = 0.062
        self.__score_threshold = 50

    def update(self, score):
        """Метод, который обновляет интервал спавна для GhostSpawner на основе score игрока."""
        num_decreases = score // self.__score_threshold
        spawn_interval = self.__base_interval - (num_decreases * self.__interval_decrease)

        if spawn_interval < 0.2:
            spawn_interval = 0.2

        self.__ghost_spawner.set_spawn_interval(spawn_interval)
