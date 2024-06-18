import pygame as pg


class PlayerController:
    """Получает пользовательские события, обновляет модель игрока и представление."""
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self, scaled_delta_time: float) -> None:
        self.model.update_physics()
        self.view.update_animation(scaled_delta_time)

    def handle_events(self, event: pg.event.Event, mouse_position: tuple[int, int], ghosts_group: pg.sprite.Group, explosions_group: pg.sprite.Group) -> None:
        if self.model.is_alive():
            if event.type == pg.KEYDOWN:
                # if event.key == pg.K_t:  # Установить новую цель игрока (к ней он будет бежать)
                #     self.model.set_target_position(mouse_position[0], mouse_position[1])
                # elif event.key == pg.K_s:  # Отменить цель игрока (остановит игрока на месте т.к цели больше нет)
                #     self.model.move_stop()
                # elif event.key == pg.K_p:  # Установить новую позицию для игрока
                #     self.model.set_position(mouse_position[0], mouse_position[1])
                pass
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for ghost in ghosts_group:
                        if ghost.is_clicked(mouse_position):
                            ghost.die(explosions_group)
                            self.model.add_score_random()
