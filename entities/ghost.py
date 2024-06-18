import pygame as pg
from entities.model.ghost_model import GhostModel
from entities.view.ghost_view import GhostView
from entities.controller.ghost_controller import GhostController


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
