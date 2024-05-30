import os
import pygame as pg
from math import sqrt
from effects import Explosion
import random


class Entity(pg.sprite.Sprite):
    def __init__(self, x_position: int, y_position: int) -> None:
        super().__init__()

        self.__x = x_position
        self.__y = y_position

        self.__target_x = None
        self.__target_y = None

        self.__speed = 1.5

        self.__is_moving = False
        self.__is_alive = True
        self.__looking_right = True

        self.image = pg.Surface((25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (round(self.__x), round(self.__y))

    def set_speed(self, new_speed):
        """Установить новую скорость для сущности."""
        self.__speed = new_speed

    def set_position(self, new_position_x: int, new_position_y: int) -> None:
        """Устанавливает новую позицию сущности."""
        self.__x = new_position_x
        self.__y = new_position_y
        self.rect.center = (round(self.__x), round(self.__y))

    def set_target_position(self, new_target_position_x: int, new_target_position_y: int) -> None:
        """Устанавливает позицию цели для сущности."""
        if (new_target_position_x, new_target_position_y) != (self.__target_x, self.__target_y):
            self.__target_x = new_target_position_x
            self.__target_y = new_target_position_y

    def get_position(self) -> tuple[int, int]:
        """Получить позицию сущности."""
        return self.__x, self.__y

    def get_position_x(self) -> int:
        """Получить позицию сущности по x."""
        return self.__x

    def get_position_y(self) -> int:
        """Получить позицию сущности по y."""
        return self.__y

    def get_target_position(self) -> tuple[int, int]:
        """Получить позицию цели сущности."""
        return self.__target_x, self.__target_y

    def get_target_position_x(self) -> int:
        """Получить позицию цели сущности по x."""
        return self.__target_x

    def get_target_position_y(self) -> int:
        """Получить позицию цели сущности по y."""
        return self.__target_y

    def update(self, scaled_delta_time: float) -> None:
        """Обновить физику и анимация сущности."""
        self.__move_to_target()
        self.__update_animation(scaled_delta_time)

    def __move_to_target(self) -> None:
        """Двигаться к цели."""
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

                self.rect.center = (round(self.__x), round(self.__y))

                if self.is_moving():
                    if self.__target_x > self.__x:
                        self.__looking_right = True
                    else:
                        self.__looking_right = False
            else:
                self.__is_moving = False
                self.set_position(self.__target_x, self.__target_y)
                self.set_target_position(None, None)

    def move_stop(self) -> None:
        """Прервать движение сущности."""
        self.set_target_position(None, None)
        self.__is_moving = False
        self.set_position(self.__x, self.__y)

    def __update_animation(self, scaled_delta_time: float) -> None:
        """Обновление анимации сущности."""
        pass

    def is_moving(self) -> bool:
        """Возвращает True, если сущность находится в движении."""
        return self.__is_moving

    def is_alive(self) -> bool:
        """Возвращает True, если сущность жива."""
        return self.__is_alive

    def toggle_moving(self) -> None:
        """Переключить состояние движения сущности."""
        self.__is_moving = not self.__is_moving

    def toggle_alive(self) -> None:
        """Переключить состояние жизни сущности."""
        self.__is_alive = not self.__is_alive

    def is_looking_right(self) -> bool:
        """Возвращает True, если игрок смотрит вправо."""
        return self.__looking_right

    def toggle_looking_right(self) -> None:
        """Поворачивает игрока в противоположную сторону."""
        self.__looking_right = not self.__looking_right

    def die(self, explosions_group: pg.sprite.Group) -> None:
        """Уничтожить сущность."""
        if self.__is_alive:
            self.__is_alive = False
            explosion_position = self.get_position()
            explosion = Explosion(explosion_position[0], explosion_position[1])
            explosions_group.add(explosion)
            self.kill()

    def load_frames(self, animation_type: str, animation_object: str, frames_quantity: int, scale_factor: float) -> list:
        frames = []
        for i in range(1, frames_quantity + 1):
            frame = pg.image.load(
                os.path.join("images", animation_object, animation_type, f"{animation_object.lower()}_{animation_type.lower()}_{i}.png"))
            frame = pg.transform.scale(frame, (round(frame.get_width() * scale_factor), round(frame.get_height() * scale_factor)))
            frames.append(frame)
        return frames


class PlayerModel:
    pass


class PlayerView:
    pass


class PlayerController:
    pass


class Player(Entity):
    def __init__(self, x_position: int, y_position: int) -> None:
        super().__init__(x_position, y_position)
        self.__speed = 2.8
        self.set_speed(self.__speed)

        self.__score = 0

        self.__looking_right = True

        self.__idle_frames_quantity = 6
        self.__move_frames_quantity = 10
        self.__scale_frames_factor = 2.4

        self.__frame_index = 0
        self.__idle_animation_speed = 0.25
        self.__move_animation_speed = 0.08

        self.__idle_frames = self.load_frames("Idle", "Player", self.__idle_frames_quantity, self.__scale_frames_factor)
        self.__move_frames = self.load_frames("Walk", "Player", self.__move_frames_quantity, self.__scale_frames_factor)

        self.image = self.__idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (round(self.get_position_x()), round(self.get_position_y()))

    def update(self, scaled_delta_time: float) -> None:
        """Обновление физики и анимации игрока."""
        super().update(scaled_delta_time)
        self.__update_animation(scaled_delta_time)

    def __update_animation(self, scaled_delta_time: float) -> None:
        move_animation_speed_coefficient = scaled_delta_time / self.__move_animation_speed
        idle_animation_speed_coefficient = scaled_delta_time / self.__idle_animation_speed

        if self.is_moving():
            frames = self.__move_frames
            animation_speed = move_animation_speed_coefficient
        else:
            frames = self.__idle_frames
            animation_speed = idle_animation_speed_coefficient

        self.__frame_index += animation_speed
        if self.__frame_index >= len(frames):
            self.__frame_index = 0

        if not self.is_looking_right():
            self.image = pg.transform.flip(frames[int(self.__frame_index)], True, False)
        else:
            self.image = frames[int(self.__frame_index)]

    def get_score(self) -> int:
        """Получить кол-во очков игрока."""
        return self.__score

    def add_score(self, score: int) -> None:
        """Добавить игроку определенное кол-во очков."""
        self.__score += score

    def add_score_random(self) -> None:
        random_score = random.randint(20, 30)
        self.__score += random_score



class Ghost(Entity):
    def __init__(self, x_position: int, y_position: int, player: Player) -> None:
        super().__init__(x_position, y_position)
        self.__speed = 2.7
        self.set_speed(self.__speed)

        self.__player = player
        self.set_target_position(self.__player.get_position_x(), self.__player.get_position_y())

        self.__frame_index = 0
        self.__move_animation_speed = 0.2

        self.__move_frames_amount = 8
        self.__scale_factor = 1.8

        self.__move_frames = []
        for i in range(1, self.__move_frames_amount + 1):
            frame = pg.image.load(os.path.join("images", "Ghost", "FireGhost", f"ghost_fire_move_{i}.png"))
            frame = pg.transform.scale(frame, (frame.get_width() * self.__scale_factor, frame.get_height() * self.__scale_factor))
            self.__move_frames.append(frame)

        self.image = self.__move_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (round(self.get_position_x()), round(self.get_position_y()))

    def update(self, scaled_delta_time: float) -> None:
        """Обновление физики и анимации духа."""
        super().update(scaled_delta_time)
        self.__update_animation(scaled_delta_time)

    def __update_animation(self, scaled_delta_time: float) -> None:
        """Обновление анимации духа."""
        move_animation_speed_coefficient = scaled_delta_time / self.__move_animation_speed

        self.__frame_index += move_animation_speed_coefficient
        if self.__frame_index >= len(self.__move_frames):
            self.__frame_index = 0

        if not self.is_looking_right():
            self.image = pg.transform.flip(self.__move_frames[int(self.__frame_index)], True, False)
        else:
            self.image = self.__move_frames[int(self.__frame_index)]

    def is_collide_with_player(self) -> bool:
        """Возвращает True, если призрак столкнулся с игроком."""
        return pg.sprite.collide_circle(self, self.__player)

    def is_clicked(self, now_mouse_position: tuple[int, int]) -> bool:
        """Возвращает True, если было нажатие на призрака."""
        return self.rect.collidepoint(now_mouse_position)