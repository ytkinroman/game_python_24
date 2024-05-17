import os
import pygame as pg


class Explosion(pg.sprite.Sprite):
    def __init__(self, x_position: int, y_position: int) -> None:
        super().__init__()

        self._explosion_duration = 0.75  # ДЛИТЕЛЬНОСТЬ ВЗРЫВА В СЕКУНДАХ
        self._explosion_volume = 0.2  # ГРОМКОСТЬ ВЗРЫВА

        self._x = x_position
        self._y = y_position

        self._current_frame = 0  # ТЕКУЩИЙ КАДР АНИМАЦИИ
        self._elapsed_time = 0  # ВРЕМЯ, ПРОШЕДШЕЕ С НАЧАЛА АНИМАЦИИ

        self._animation_frames = []  # АНИМАЦИЯ ВЗРЫВА
        for i in range(2, 13):
            frame = pg.image.load(os.path.join("images", "Explosions", f"explosion_{i}.png"))
            frame = pg.transform.scale(frame, (215, 215))
            self._animation_frames.append(frame)

        self._frame_duration = self._explosion_duration / len(self._animation_frames)  # ДЛИТЕЛЬНОСТЬ КАДРА

        self._explosion_sound = pg.mixer.Sound(os.path.join("sounds", "explosion-1.mp3"))  # ЗВУК ВЗРЫВА
        self._explosion_sound.set_volume(self._explosion_volume)
        self._explosion_sound.play()

        self.image = self._animation_frames[self._current_frame]  # ТЕКУЩЕЕ ИЗОБРАЖЕНИЕ ДЛЯ АНИМАЦИИ
        self.rect = self.image.get_rect()
        self.rect.center = (self._x, self._y)

    def update(self, scaled_delta_time: float) -> None:
        """Обновление анимации и физики взрыва."""
        self._elapsed_time += scaled_delta_time

        # РАСЧЕТ ИНДЕКСА ТЕКУЩЕГО ИЗОБРАЖЕНИЯ ДЛЯ АНИМАЦИИ
        self._current_frame = int(self._elapsed_time / self._frame_duration)

        # ПРОВЕРКА НА ЗАВЕРШЕНИЕ АНИМАЦИИ
        if self._current_frame >= len(self._animation_frames):
            self._current_frame = len(self._animation_frames) - 1
            self.kill()

        # ОБНОВЛЕНИЕ ТЕКУЩЕГО ИЗОБРАЖЕНИЯ ДЛЯ АНИМАЦИИ
        self.image = self._animation_frames[self._current_frame]
