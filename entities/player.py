import pygame as pg
from entities.model.player_model import PlayerModel
from entities.view.player_view import PlayerView
from entities.controller.player_controller import PlayerController


class Player(pg.sprite.Sprite):
    def __init__(self, x_position: int, y_position: int) -> None:
        super().__init__()

        self.model = PlayerModel(x_position, y_position)
        self.view = PlayerView(self.model)
        self.controller = PlayerController(self.model, self.view)

        self.image = self.view.image
        self.rect = self.image.get_rect()
        self.rect.center = self.model.get_position()

    def update(self, scaled_delta_time: float) -> None:
        self.controller.update(scaled_delta_time)
        self.view.update_animation(scaled_delta_time)

        self.image = self.view.image
        self.rect = self.view.rect

    def set_target_position(self, new_target_position_x: int, new_target_position_y: int) -> None:
        self.model.set_target_position(new_target_position_x, new_target_position_y)

    def handle_events(self, event: pg.event.Event, mouse_position: tuple[int, int], ghosts_group: pg.sprite.Group, explosions_group: pg.sprite.Group) -> None:
        self.controller.handle_events(event, mouse_position, ghosts_group, explosions_group)

    def is_alive(self) -> bool:
        return self.model.is_alive()

    def is_moving(self) -> bool:
        return self.model.is_moving()

    def get_score(self) -> int:
        return self.model.get_score()

    def add_score_random(self) -> None:
        self.model.add_score_random()

    def die(self, explosions_group: pg.sprite.Group) -> None:
        self.model.die(explosions_group)
        self.kill()

    def get_position(self) -> tuple[int, int]:
        return self.model.get_position()

    def get_target_position(self) -> tuple[int, int]:
        return self.model.get_target_position()
