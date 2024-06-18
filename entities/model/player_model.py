import random
import pygame as pg
from math import sqrt
from effects import Explosion


class PlayerModel:
    """Отвечает за логику игрока."""
    def __init__(self, x_position: int, y_position: int):
        self.__x = x_position
        self.__y = y_position

        self.__target_x = None
        self.__target_y = None

        self.__speed = 2.8

        self.__score = 0
        self.__score_random_min = 20
        self.__score_random_max = 35

        self.__is_moving = False
        self.__is_alive = True
        self.__looking_right = True

    def get_position(self) -> tuple[int, int]:
        return self.__x, self.__y

    def set_position(self, new_position_x: int, new_position_y: int) -> None:
        self.__x = new_position_x
        self.__y = new_position_y

    def get_score(self) -> int:
        return self.__score

    def add_score(self, score: int) -> None:
        self.__score += score

    def add_score_random(self) -> None:
        self.add_score(random.randint(self.__score_random_min, self.__score_random_max))

    def set_target_position(self, new_target_position_x: int, new_target_position_y: int) -> None:
        if (new_target_position_x, new_target_position_y) != (self.__target_x, self.__target_y):
            self.__target_x = new_target_position_x
            self.__target_y = new_target_position_y

    def get_target_position(self) -> tuple[int, int]:
        return self.__target_x, self.__target_y

    def is_moving(self) -> bool:
        return self.__is_moving

    def is_looking_right(self) -> bool:
        return self.__looking_right

    def is_alive(self) -> bool:
        return self.__is_alive

    def move_stop(self) -> None:
        self.set_target_position(self.__x, self.__y)
        self.__is_moving = False

    def update_physics(self):
        self.move_to_target()

    def move_to_target(self) -> None:
        if self.__target_x is not None and self.__target_y is not None:
            direction_x = self.__target_x - self.__x
            direction_y = self.__target_y - self.__y

            distance = sqrt(direction_x ** 2 + direction_y ** 2)

            if distance > self.__speed:
                self.__is_moving = True

                normalized_dx = direction_x / distance
                normalized_dy = direction_y / distance

                self.__x += normalized_dx * self.__speed
                self.__y += normalized_dy * self.__speed

                if self.is_moving():
                    if self.__target_x > self.__x:
                        self.__looking_right = True
                    else:
                        self.__looking_right = False
            else:
                self.__is_moving = False
                self.set_position(self.__target_x, self.__target_y)
                self.set_target_position(None, None)

    def die(self, explosions_group: pg.sprite.Group) -> None:
        """Уничтожить сущность."""
        if self.__is_alive:
            self.__is_alive = False
            explosion_position = self.get_position()
            explosion = Explosion(explosion_position[0], explosion_position[1])
            explosions_group.add(explosion)
