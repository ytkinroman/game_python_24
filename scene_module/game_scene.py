import pygame as pg
from utils import GameSettings
from scene_module.scene import Scene
from ui_module.pause_ui import UIPause
from ui_module.gameplay_ui import UIGamePlay
from environment import Environment
from entities.player import Player
from spawn_system import GhostSpawner
from game_manager import GameManager


class GameScene(Scene):
    def __init__(self, game) -> None:
        super().__init__(game)

        self._game_settings = GameSettings

        self._environment_group = Environment()
        self._players_group = pg.sprite.Group()
        self._ghosts_group = pg.sprite.Group()
        self._explosions_group = pg.sprite.Group()

        self._player = Player(self._game_settings.SCREEN_WIDTH + 150, self._game_settings.SCREEN_HEIGHT // 2)
        self._players_group.add(self._player)

        self._pause_ui = UIPause()
        self._gameplay_ui = UIGamePlay(self._player)

        self._spawn_points_list = [
            (self._game_settings.SCREEN_WIDTH // 2, 0), (0, 0),
            (0, self._game_settings.SCREEN_HEIGHT // 2),
            (self._game_settings.SCREEN_WIDTH, self._game_settings.SCREEN_HEIGHT // 2),
            (self._game_settings.SCREEN_WIDTH, self._game_settings.SCREEN_HEIGHT),
            (0, self._game_settings.SCREEN_HEIGHT), (self._game_settings.SCREEN_HEIGHT, 0),
            (self._game_settings.SCREEN_WIDTH // 2, self._game_settings.SCREEN_HEIGHT)
        ]
        self._ghosts_spawner_interval = 1.4
        self._ghosts_spawner = GhostSpawner(self._ghosts_spawner_interval, self._ghosts_group, self._player)
        self._ghosts_spawner.add_points(self._spawn_points_list)

        self._game_manager = GameManager(self._game,  self._ghosts_group, self._player, self._ghosts_spawner)

    def update(self, scaled_delta_time: float) -> None:
        if not self._game.is_game_paused():
            self._update_game_world(scaled_delta_time)
        else:
            self._update_game_pause()

    def _update_game_world(self, scaled_delta_time: float) -> None:
        self._players_group.update(scaled_delta_time)
        self._ghosts_group.update(scaled_delta_time)
        self._explosions_group.update(scaled_delta_time)
        self._game_manager.update(scaled_delta_time)
        self._gameplay_ui.update()

        if self._player.is_alive():
            self._ghosts_spawner.update(scaled_delta_time)

            for ghost in self._ghosts_group:
                if ghost.is_collide_with_player():
                    self._player.die(self._explosions_group)
        else:
            self._ghosts_spawner.stop_active()
            for ghost in self._ghosts_group:
                ghost.move_stop()

    def _update_game_pause(self) -> None:
        pass

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
            mouse_position = pg.mouse.get_pos()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self._game.toggle_pause()

            self._player.handle_events(event, mouse_position, self._ghosts_group, self._explosions_group)
