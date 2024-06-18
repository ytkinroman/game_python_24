import pygame as pg
from utils import load_frames


class PlayerView:
    """Отвечает за отображение игрока на экране и его анимацию."""
    def __init__(self, model):
        self.model = model

        self.__idle_frames_quantity = 6
        self.__move_frames_quantity = 10
        self.__scale_frames_factor = 2.4

        self.__frame_index = 0
        self.__idle_animation_speed = 0.41
        self.__move_animation_speed = 0.14

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
