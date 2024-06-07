import pygame as pg
from utils import GameSettings
from scene_module.scene import Scene
from ui_module.pause_ui import UIPause
from ui_module.gameplay_ui import UIGamePlay
from environment import Environment
from entities.player import Player
from spawn_system import GhostSpawner


class GameScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

        self._game_settings = GameSettings

        self._game_win_score = 800

        self._next_scene_delay = 3

        self._environment_group = Environment()
        self._players_group = pg.sprite.Group()
        self._ghosts_group = pg.sprite.Group()
        self._explosions_group = pg.sprite.Group()

        self._player = Player(self._game_settings.SCREEN_WIDTH + 150, self._game_settings.SCREEN_HEIGHT // 2)
        self._players_group.add(self._player)

        self._pause_ui = UIPause(self._player, self)
        self._gameplay_ui = UIGamePlay(self._player)

        self._spawn_points_list = [
            (self._game_settings.SCREEN_WIDTH // 2, 0), (0, 0),
            (0, self._game_settings.SCREEN_HEIGHT // 2),
            (self._game_settings.SCREEN_WIDTH, self._game_settings.SCREEN_HEIGHT // 2),
            (self._game_settings.SCREEN_WIDTH, self._game_settings.SCREEN_HEIGHT),
            (0, self._game_settings.SCREEN_HEIGHT), (self._game_settings.SCREEN_HEIGHT, 0),
            (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT)
        ]
        self._ghosts_spawner_interval = 2.0
        self._ghosts_spawner = GhostSpawner(self._ghosts_spawner_interval, self._ghosts_group, self._player)
        self._ghosts_spawner.add_points(self._spawn_points_list)

        self._player.set_target_position(self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT // 2)
        self._ghosts_spawner.set_active()

    def update(self, scaled_delta_time: float) -> None:
        if not self._game.is_game_paused():
            self._update_game_world(scaled_delta_time)
        else:
            self._update_game_pause()

    def get_win_score(self) -> int:
        return self._game_win_score

    def _update_game_world(self, scaled_delta_time: float) -> None:
        self._players_group.update(scaled_delta_time)
        self._ghosts_group.update(scaled_delta_time)
        self._explosions_group.update(scaled_delta_time)
        self._gameplay_ui.update()
        self._ghosts_spawner.update(scaled_delta_time)

        if self._player.is_alive():
            if self._player.get_score() >= self._game_win_score:
                self._ghosts_spawner.stop_active()

                if not self._ghosts_group.sprites():

                    self._player.set_target_position(-150, self._game_settings.SCREEN_HEIGHT // 2)

                    if self._next_scene_delay > 0:
                        self._next_scene_delay -= scaled_delta_time
                        return

                    self._game.set_good_ending()
                    self._game.change_scene("end")

            for ghost in self._ghosts_group:
                if ghost.is_collide_with_player():
                    self._player.die(self._explosions_group)
        else:
            self._ghosts_spawner.stop_active()
            for ghost in self._ghosts_group:
                ghost.move_stop()

            if self._next_scene_delay > 0:
                self._next_scene_delay -= scaled_delta_time
                return

            self._game.set_bad_ending()
            self._game.change_scene("end")

    def _update_game_pause(self) -> None:
        self._pause_ui.update()

    def render(self, screen: pg.Surface) -> None:
        if not self._game.is_game_paused():
            self._render_game_world(screen)
        else:
            self._render_game_pause(screen)

    def _render_game_world(self, screen: pg.Surface) -> None:
        self._environment_group.draw(screen)
        self._players_group.draw(screen)
        self._ghosts_group.draw(screen)
        self._explosions_group.draw(screen)
        self._gameplay_ui.draw(screen)

    def _render_game_pause(self, screen: pg.Surface) -> None:
        self._environment_group.draw(screen)
        self._players_group.draw(screen)
        self._ghosts_group.draw(screen)
        self._explosions_group.draw(screen)
        self._pause_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if self._player.is_alive():
            if not self._game.is_game_paused():
                mouse_position = pg.mouse.get_pos()
                self._player.handle_events(event, mouse_position, self._ghosts_group, self._explosions_group)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._game.toggle_pause()
