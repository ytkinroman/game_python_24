import os
import pygame as pg


class Explosion(pg.sprite.Sprite):
    def __init__(self, x_position: int, y_position: int) -> None:
        super().__init__()

        self.__x, self.__y = x_position, y_position

        self.__explosion_duration = 0.8
        self.__explosion_volume = 0.2

        self.__scale_factor_frame = 3.2
        self.__animation_frames_amount = 13

        self.__current_frame = 0
        self.__elapsed_time = 0

        self.__animation_frames = []
        for i in range(1, self.__animation_frames_amount + 1):
            frame = pg.image.load(os.path.join("images", "Explosions", f"explosion_{i}.png"))
            frame = pg.transform.scale(frame, (frame.get_width() * self.__scale_factor_frame, frame.get_height() * self.__scale_factor_frame))
            self.__animation_frames.append(frame)

        self.__frame_duration = self.__explosion_duration / len(self.__animation_frames)

        self.__explosion_sound = pg.mixer.Sound(os.path.join("sounds", "explosion-1.mp3"))
        self.__explosion_sound.set_volume(self.__explosion_volume)
        self.__explosion_sound.play()

        self.image = self.__animation_frames[self.__current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.__x, self.__y)

    def update(self, scaled_delta_time: float) -> None:
        """Обновление анимации взрыва."""
        self.__elapsed_time += scaled_delta_time

        self.__current_frame = int(self.__elapsed_time / self.__frame_duration)

        if self.__current_frame >= len(self.__animation_frames):
            self.__current_frame = len(self.__animation_frames) - 1
            self.kill()

        self.image = self.__animation_frames[self.__current_frame]
