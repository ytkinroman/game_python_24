import pygame as pg
from entities.ghost import Ghost
from entities.player import Player
from spawn_system_module.spawner import Spawner


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
