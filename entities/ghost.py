import pygame as pg
from utils import load_frames
from math import sqrt
from effects import Explosion


class GhostModel:
    def __init__(self, x_position: int, y_position: int, player):
        self.__x = x_position
        self.__y = y_position

        self.__player = player

        self.__target_x, self.__target_y = self.__player.get_position()

        self.__speed = 2.8

        self.__is_moving = False
        self.__is_alive = True
        self.__looking_right = True

    def get_position(self) -> tuple[int, int]:
        return self.__x, self.__y

    def set_position(self, new_position_x: int, new_position_y: int) -> None:
        self.__x = new_position_x
        self.__y = new_position_y

    def set_target_position(self, new_target_position_x: int, new_target_position_y: int) -> None:
        if (new_target_position_x, new_target_position_y) != (self.__target_x, self.__target_y):
            self.__target_x = new_target_position_x
            self.__target_y = new_target_position_y

    def is_looking_right(self) -> bool:
        return self.__looking_right

    def is_moving(self) -> bool:
        return self.__is_moving

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
        if self.__is_alive:
            self.__is_alive = False
            explosion_position = self.get_position()
            explosion = Explosion(explosion_position[0], explosion_position[1])
            explosions_group.add(explosion)


class GhostView:
    def __init__(self, model: GhostModel):
        self.model = model

        self.__frame_index = 0
        self.__move_animation_speed = 0.25

        self.__move_frames_quantity = 8
        self.__scale_frames_factor = 1.8

        self.__move_frames = load_frames("Move", "Ghost", self.__move_frames_quantity, self.__scale_frames_factor)

        self.image = self.__move_frames[0]
        self.rect = self.image.get_rect()
        position = self.model.get_position()
        self.rect.center = (round(position[0]), round(position[1]))

    def update_animation(self, scaled_delta_time: float) -> None:
        move_animation_speed_coefficient = scaled_delta_time / self.__move_animation_speed

        self.__frame_index += move_animation_speed_coefficient
        if self.__frame_index >= len(self.__move_frames):
            self.__frame_index = 0

        if not self.model.is_looking_right():
            self.image = pg.transform.flip(self.__move_frames[int(self.__frame_index)], True, False)
        else:
            self.image = self.__move_frames[int(self.__frame_index)]

        self.rect = self.image.get_rect(center=self.model.get_position())


class GhostController:
    def __init__(self, model: GhostModel, view: GhostView):
        self.model = model
        self.view = view

    def update(self, scaled_delta_time: float) -> None:
        self.model.update_physics()
        self.view.update_animation(scaled_delta_time)


class Ghost(pg.sprite.Sprite):
    def __init__(self, x_position: int, y_position: int, player) -> None:
        super().__init__()

        self.__player = player

        self.__x = x_position
        self.__y = y_position

        self.model = GhostModel(x_position, y_position, self.__player)
        self.view = GhostView(self.model)
        self.controller = GhostController(self.model, self.view)

        self.image = self.view.image
        self.rect = self.image.get_rect()
        self.rect.center = self.model.get_position()

    def update(self, scaled_delta_time: float) -> None:
        self.controller.update(scaled_delta_time)
        self.view.update_animation(scaled_delta_time)

        self.image = self.view.image
        self.rect = self.view.rect

    def die(self, explosions_group: pg.sprite.Group) -> None:
        self.model.die(explosions_group)
        self.kill()

    def is_clicked(self, mouse_position: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_position)

    def is_collide_with_player(self) -> bool:
        return pg.sprite.collide_circle(self, self.__player)

    def move_stop(self) -> None:
        self.model.move_stop()
