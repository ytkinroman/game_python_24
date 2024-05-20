import os
import pygame as pg
from math import sqrt
from effects import Explosion


class Player(pg.sprite.Sprite):
    def __init__(self, x_position: int, y_position: int) -> None:
        super().__init__()

        self.__score = 0
        self.__speed = 2.8

        self.__delay_timer = 0

        self.__frame_index = 0
        self.__idle_animation_speed = 0.25
        self.__move_animation_speed = 0.08

        self.__x = x_position
        self.__y = y_position

        self.__target_x = self.__x
        self.__target_y = self.__y

        self.__is_moving = False
        self.__looking_right = True
        self.__is_alive = True

        self._idle_frames_number = 6
        self._move_frames_number = 10
        self._scale_factor = 2.4

        self.__idle_frames = []
        for i in range(1, self._idle_frames_number + 1):
            frame = pg.image.load(os.path.join("images", "Player", "Idle", f"player_idle_{i}.png"))
            frame = pg.transform.scale(frame, (frame.get_width() * self._scale_factor, frame.get_height() * self._scale_factor))
            self.__idle_frames.append(frame)

        self.__move_frames = []
        for i in range(1, self._move_frames_number + 1):
            frame = pg.image.load(os.path.join("images", "Player", "Walk", f"player_walk_{i}.png"))
            frame = pg.transform.scale(frame, (frame.get_width() * self._scale_factor, frame.get_height() * self._scale_factor))
            self.__move_frames.append(frame)

        self.image = self.__idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (round(self.__x), round(self.__y))

    def set_position(self, new_position_x: int, new_position_y: int) -> None:
        """Установить новую позицию."""
        self.__x = new_position_x
        self.__y = new_position_y

    def get_position(self) -> tuple[int, int]:
        """Получить позицию."""
        return self.__x, self.__y

    def set_target_position(self, new_target_x: int, new_target_y: int) -> None:
        """Установить новую цель."""
        self.__target_x = new_target_x
        self.__target_y = new_target_y

    def get_target_position(self) -> tuple[int, int]:
        """Получить позицию цели."""
        return self.__target_x, self.__target_y

    def add_score(self, score: int) -> None:
        """Добавить игроку очки."""
        self.__score += score

    def get_score(self) -> int:
        """Получить кол-во очков игрока."""
        return self.__score

    def is_alive(self) -> bool:
        """Возвращает True, если игрок жив."""
        return self.__is_alive

    def is_moving(self) -> bool:
        """Возвращает True, если игрок находится в движении."""
        return self.__is_moving

    def is_looking_right(self) -> bool:
        """Возвращает True, если игрок смотрит вправо."""
        return self.__looking_right

    def toggle_alive(self) -> None:
        """Переключить состояние жизни сущности."""
        self.__is_alive = not self.__is_alive

    def toggle_moving(self) -> None:
        """Переключить состояние движения сущности."""
        self.__is_moving = not self.__is_moving

    def toggle_looking_right(self) -> None:
        """Повернуть сущность в другую сторону."""
        self.__looking_right = not self.__looking_right

    def __move_target(self, scaled_delta_time: float) -> None:
        """Обработка движения игрока к цели."""
        direction_x = self.__target_x - self.__x  # РАЗНИЦА МЕЖДУ ТОЧКОЙ ЦЕЛИ И ТЕКУЩЕЙ КООРДИНАТАМИ ПО ОСИ X.
        direction_y = self.__target_y - self.__y  # РАЗНИЦА МЕЖДУ ЦЕЛЕВОЙ И ТЕКУЩЕЙ КООРДИНАТАМИ ПО ОСИ Y.

        distance = sqrt(direction_x ** 2 + direction_y ** 2)  # ВЫЧИСЛЯЕМ РАССТОЯНИЕ МЕЖДУ ТЕКУЩИМ ПОЛОЖЕНИЕМ И ЦЕЛЬЮ.

        if distance > self.__speed:
            normalized_dx = direction_x / distance  # НОРМАЛИЗУЕМ ВЕКТОР ДВИЖЕНИЯ (ДЕЛИМ НА РАССТОЯНИЕ).
            normalized_dy = direction_y / distance

            self.__x += normalized_dx * self.__speed  # ОБНОВЛЯЕМ КООРДИНАТЫ ПРИЗРАКА С УЧЕТОМ СКОРОСТИ.
            self.__y += normalized_dy * self.__speed

            self.rect.center = (round(self.__x), round(self.__y))  # ОБНОВЛЯЕМ ПРЯМОУГОЛЬНИК, ОГРАНИЧИВАЮЩИЙ СПРАЙТ.
            # print(f"CURRENT POSITION: ({self.__x}, {self.__y}), TARGET POSITION: ({self.__target_x}, {self.__target_y})")

            if self.__target_x > self.__x:  # ПРОВЕРЯЕМ КУДА СМОТРИТ ИГРОК.
                self.__looking_right = True
            else:
                self.__looking_right = False

            self.__is_moving = True
        else:
            self.set_position(self.__target_x, self.__target_y)
            self.rect.center = (round(self.__x), round(self.__y))
            # print(f"PLAYER STOPPED AT POSITION: ({self.__x}, {self.__y})")
            self.__is_moving = False

    def __update_animation(self, scaled_delta_time: float) -> None:
        """Обновление анимации игрока."""
        move_animation_speed_coefficient = scaled_delta_time / self.__move_animation_speed  # ВЫЧИСЛЯЕМ КОЭФФИЦИЕНТЫ СКОРОСТИ АНИМАЦИЙ
        idle_animation_speed_coefficient = scaled_delta_time / self.__idle_animation_speed

        if self.__is_moving:  # ВЫБИРАЕМ АНИМАЦИИ
            frames = self.__move_frames
            animation_speed = move_animation_speed_coefficient
        else:
            frames = self.__idle_frames
            animation_speed = idle_animation_speed_coefficient

        # ОБНОВЛЯЕМ ИНДЕКС ТЕКУЩЕГО КАДРА АНИМАЦИИ
        self.__frame_index += animation_speed
        if self.__frame_index >= len(frames):
            self.__frame_index = 0

        # ВЫБИРАЕМ НАПРАВЛЕНИЕ ДЛЯ СПРАЙТА
        if not self.__looking_right:
            self.image = pg.transform.flip(frames[int(self.__frame_index)], True, False)
        else:
            self.image = frames[int(self.__frame_index)]

    def update(self, scaled_delta_time: float) -> None:
        """Обновление физики и анимации Игрока."""
        self.__move_target(scaled_delta_time)
        self.__update_animation(scaled_delta_time)

    def set_delay(self, seconds: float) -> None:
        """Остановить игрока на какое-то время."""
        self.__delay_timer = seconds

    def move_stop(self) -> None:
        """Остановить движение Игрока."""
        self.__is_moving = False
        self.__target_x = round(self.__x)
        self.__target_y = round(self.__y)

    def die(self, explosions_group: pg.sprite.Group) -> None:
        """Уничтожить Игрока."""
        if self.__is_alive:
            self.__is_alive = False
            explosion_position = self.get_position()
            explosion = Explosion(explosion_position[0], explosion_position[1])
            explosions_group.add(explosion)
            self.kill()


class Ghost(pg.sprite.Sprite):
    def __init__(self, x_position: int, y_position: int, player: Player) -> None:
        super().__init__()

        self._player = player

        self._speed = 2.6
        self._move_animation_speed = 0.2

        self._is_alive = False
        self._is_moving = False
        self._looking_right = True

        self._x, self._y = x_position, y_position
        self._target_x, self._target_y = self._player.get_position()

        self._frame_index = 0

        self._move_frames_amount = 8
        self._scale_factor = 1.8

        self._move_frames = []
        for i in range(1, self._move_frames_amount + 1):
            frame = pg.image.load(os.path.join("images", "Ghost", "FireGhost", f"ghost_fire_move_{i}.png"))
            frame = pg.transform.scale(frame, (frame.get_width() * self._scale_factor, frame.get_height() * self._scale_factor))
            self._move_frames.append(frame)

        self.image = self._move_frames[self._frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (round(self._x), round(self._y))

    def _move_target(self) -> None:
        """Обработка движения Духа к цели."""
        direction_x = self._target_x - self._x
        direction_y = self._target_y - self._y

        distance = sqrt(direction_x ** 2 + direction_y ** 2)

        if distance > self._speed:
            normalized_dx = direction_x / distance
            normalized_dy = direction_y / distance

            self._x += normalized_dx * self._speed
            self._y += normalized_dy * self._speed

            self.rect.center = (round(self._x), round(self._y))

            if self._target_x > self._x:
                self._looking_right = True
            else:
                self._looking_right = False

            self._is_moving = True
        else:
            self._is_moving = False
            self.set_position(self._target_x, self._target_y)
            self.rect.center = (round(self._x), round(self._y))

    def move_stop(self) -> None:
        """Остановить движение Духа."""
        self._target_x = round(self._x)
        self._target_y = round(self._y)
        self._is_moving = False

    def _update_animation(self, scaled_delta_time: float) -> None:
        """Обновление анимации Духа."""
        move_animation_speed_coefficient = scaled_delta_time / self._move_animation_speed

        self._frame_index += move_animation_speed_coefficient
        if self._frame_index >= len(self._move_frames):
            self._frame_index = 0

        if not self._looking_right:
            self.image = pg.transform.flip(self._move_frames[int(self._frame_index)], True, False)
        else:
            self.image = self._move_frames[int(self._frame_index)]

    def update(self, scaled_delta_time: float) -> None:
        """Обновление физики и анимации Духа."""
        self._move_target()
        self._update_animation(scaled_delta_time)

    def die(self, explosions_group: pg.sprite.Group) -> None:
        """Уничтожить Духа."""
        self._is_alive = False
        explosion_position = self.get_position()
        explosion = Explosion(explosion_position[0], explosion_position[1])
        explosions_group.add(explosion)
        self.kill()

    def set_target(self, new_target_position_x: int, new_target_position_y: int) -> None:
        """Установить цель для Духа."""
        self._target_x = new_target_position_x
        self._target_y = new_target_position_y

    def get_target(self) -> tuple[int, int]:
        """Возвращает позицию цели Духа."""
        return self._target_x, self._target_y

    def set_position(self, new_position_x: int, new_position_y: int) -> None:
        """Установить позицию для Духа."""
        self._x = new_position_x
        self._y = new_position_y

    def get_position(self) -> tuple[int, int]:
        """Получить позицию Духа."""
        return self._x, self._y

    def collide_with_player(self, player: Player) -> bool:
        """Возвращает True, если призрак столкнулся с игроком."""
        return pg.sprite.collide_circle(self, player)

    def is_clicked(self, now_mouse_position: tuple[int, int]) -> bool:
        """Возвращает True, если было нажатие на призрака."""
        return self.rect.collidepoint(now_mouse_position)
