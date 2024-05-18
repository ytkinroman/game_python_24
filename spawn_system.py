import random
import pygame as pg
from entities import Player, Ghost


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
        random_point = random.choice(self.__points)
        return random_point.get_position()


class GhostSpawner:
    def __init__(self, spawn_interval: float, spawn_group: pg.sprite.Group, spawner: Spawner, player: Player) -> None:
        self.__spawn_interval = spawn_interval

        self.__group = spawn_group
        self.__spawner = spawner
        self.__player = player

        self.__is_active = False

        self.__delay_timer = 5  # ЧЕРЕЗ СКОЛЬКО ВКЛЮЧИТЬСЯ

        #self._player_position = self.__player.get_position()
        #self.__target_x = (self._player_position[0] // 2)
        #self.__target_y = (self._player_position[1] // 2)

        self.__set_target()

        self.__last_spawn_time = 0

    def update(self, scaled_delta_time: float) -> None:
        """Обновляет состояние спавнера."""
        if self.__is_active:
            if self.__player.is_alive():
                if self.__delay_timer > 0:
                    self.__delay_timer -= scaled_delta_time
                    return

                self.__last_spawn_time += scaled_delta_time

                if self.__last_spawn_time >= self.__spawn_interval:
                    self.__last_spawn_time -= self.__spawn_interval
                    self.__set_target()
                    self.spawn_ghost()

    def spawn_ghost(self) -> None:
        """Спавн Духа."""
        random_point_position_x, random_point_position_y = self.__spawner.get_random_point()
        self.__monster = Ghost(random_point_position_x, random_point_position_y, self.__player)  # ПРИЗРАК.
        self.__group.add(self.__monster)

    def set_spawn_interval(self, new_interval: float) -> None:
        """Устанавливаем новый интервал."""
        self.__spawn_interval = new_interval

    def get_spawn_interval(self) -> float:
        """Получаем время интервала в секундах."""
        return self.__spawn_interval

    def toggle_active(self) -> None:
        """Изменяет состояние спавнера. Включает или выключает."""
        self.__is_active = not self.__is_active

    def is_active(self) -> bool:
        """Возвращает True если активный."""
        return self.__is_active

    def __set_target(self) -> None:
        self._player_position = self.__player.get_position()
        self.__target_x = (self._player_position[0] // 2)
        self.__target_y = (self._player_position[1] // 2)