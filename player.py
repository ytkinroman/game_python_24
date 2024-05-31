import pygame as pg
from utils import load_frames
from math import sqrt
import random


class PlayerModel:
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

    def is_moving(self) -> bool:
        return self.__is_moving

    def is_looking_right(self) -> bool:
        return self.__looking_right

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


class PlayerController:
    def __init__(self, model: PlayerModel):
        self.model = model
        self.view = PlayerView(self.model)

    def update(self, scaled_delta_time: float) -> None:
        self.model.update_physics()
        self.view.update_animation(scaled_delta_time)

    def handle_events(self, event, mouse_pos):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_t:  # Установить новую цель игрока (к ней он будет бежать)
                self.model.set_target_position(mouse_pos[0], mouse_pos[1])
            elif event.key == pg.K_s:  # Отменить цель игрока (остановит игрока на месте т.к цели больше нет)
                self.model.move_stop()
            elif event.key == pg.K_p:  # Установить новую позицию для игрока
                self.model.set_position(mouse_pos[0], mouse_pos[1])
            elif event.key == pg.K_a:  # Выдать игроку случайное кол-во очков (отобразится в UI)
                self.model.add_score_random()


class PlayerView:
    def __init__(self, model: PlayerModel):
        self.model = model

        self.__idle_frames_quantity = 6
        self.__move_frames_quantity = 10
        self.__scale_frames_factor = 2.4

        self.__frame_index = 0
        self.__idle_animation_speed = 0.25
        self.__move_animation_speed = 0.08

        self.__idle_frames = load_frames("Idle", "Player", self.__idle_frames_quantity, self.__scale_frames_factor)
        self.__move_frames = load_frames("Walk", "Player", self.__move_frames_quantity, self.__scale_frames_factor)

        self.image = self.__idle_frames[0]
        self.rect = self.image.get_rect()
        position = self.model.get_position()
        self.rect.center = (round(position[0]), round(position[1]))

    def update_animation(self, scaled_delta_time: float) -> None:
        move_animation_speed_coefficient = scaled_delta_time / self.__move_animation_speed
        idle_animation_speed_coefficient = scaled_delta_time / self.__idle_animation_speed

        if self.model.is_moving():
            frames = self.__move_frames
            animation_speed = move_animation_speed_coefficient
        else:
            frames = self.__idle_frames
            animation_speed = idle_animation_speed_coefficient

        self.__frame_index += animation_speed
        if self.__frame_index >= len(frames):
            self.__frame_index = 0

        if not self.model.is_looking_right():
            self.image = pg.transform.flip(frames[int(self.__frame_index)], True, False)
        else:
            self.image = frames[int(self.__frame_index)]

        self.rect = self.image.get_rect(center=self.model.get_position())


class Player(pg.sprite.Sprite):
    def __init__(self, x_position: int, y_position: int) -> None:
        super().__init__()

        self.model = PlayerModel(x_position, y_position)
        self.controller = PlayerController(self.model)
        self.view = PlayerView(self.model)

        self.image = self.view.image
        self.rect = self.image.get_rect()
        self.rect.center = self.model.get_position()

    def update(self, scaled_delta_time: float) -> None:
        self.controller.update(scaled_delta_time)
        self.view.update_animation(scaled_delta_time)
        self.image = self.view.image
        self.rect = self.view.rect
