import os
import pygame as pg


class Explosion(pg.sprite.Sprite):
    def __init__(self, x_position: int, y_position: int) -> None:
        super().__init__()

        self.image_path = os.path.join("images", "Explosions")
        self.sound_path = os.path.join("sounds", "explosion-1.mp3")
        self.scale_factor_frame = 3.2
        self.animation_frames_amount = 13
        self.explosion_duration = 0.8
        self.explosion_volume = 0.2

        self.x, self.y = x_position, y_position

        self.animation_frames = []
        for i in range(1, self.animation_frames_amount + 1):
            frame = pg.image.load(os.path.join(self.image_path, f"explosion_{i}.png"))
            frame = pg.transform.scale(frame, (frame.get_width() * self.scale_factor_frame, frame.get_height() * self.scale_factor_frame))
            self.animation_frames.append(frame)

        self.frame_duration = self.explosion_duration / len(self.animation_frames)

        self.explosion_sound = pg.mixer.Sound(self.sound_path)
        self.explosion_sound.set_volume(self.explosion_volume)
        self.explosion_sound.play()

        self.image = self.animation_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.current_frame = 0
        self.elapsed_time = 0

    def update(self, scaled_delta_time: float) -> None:
        """Обновление анимации взрыва."""
        self.elapsed_time += scaled_delta_time

        self.current_frame = int(self.elapsed_time / self.frame_duration)

        if self.current_frame >= len(self.animation_frames):
            self.current_frame = len(self.animation_frames) - 1
            self.kill()

        self.image = self.animation_frames[self.current_frame]
