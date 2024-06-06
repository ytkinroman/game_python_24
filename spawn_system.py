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

        self.__base_spawn_interval = self.__spawn_interval
        self.__score_increment = 50
        self.__spawn_interval_decrement = 0.2

        self.__start_delay = 6

        self.__last_score_check = 2

        self.__is_active = False
        self.__last_spawn = 0

    def update(self, scaled_delta_time: float) -> None:
        if self.__is_active:
            print(self.__spawn_interval)
            if self.__player.is_alive():
                if self.__start_delay > 0:
                    self.__start_delay -= scaled_delta_time
                    return

                if self.__last_score_check > 2:
                    self.__last_score_check -= scaled_delta_time
                else:
                    self.__last_score_check = 2
                    self.update_spawn_interval_on_score()

                self.__last_spawn += scaled_delta_time

                if self.__last_spawn >= self.__spawn_interval:
                    self.__last_spawn = 0
                    self.spawn_ghost()

    def update_spawn_interval_on_score(self):
        player_score = self.__player.get_score()

        new_spawn_interval = self.__base_spawn_interval - (player_score // self.__score_increment) * self.__spawn_interval_decrement

        if new_spawn_interval < 0.5:
            new_spawn_interval = 0.5

        self.__spawn_interval = new_spawn_interval

    def spawn_ghost(self) -> None:
        random_point_position_x, random_point_position_y = self.get_random_point()
        ghost = Ghost(random_point_position_x, random_point_position_y, self.__player)
        self.__ghost_group.add(ghost)

    def set_active(self) -> None:
        self.__is_active = True

    def stop_active(self) -> None:
        self.__is_active = False
