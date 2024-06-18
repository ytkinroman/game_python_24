import pygame as pg
from utils import load_frames


class GhostView:
    def __init__(self, model):
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
