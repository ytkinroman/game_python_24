from utils import GameSettings
from spawn_system import GhostSpawner


class GameManager:
    def __init__(self, player, ghosts_group):
        self.__player = player
        self.__ghosts_group = ghosts_group

        self.__game_settings = GameSettings()

        self.__points_list = [(self.__game_settings.SCREEN_WIDTH // 2, 0), (0, 0),
                              (0, self.__game_settings.SCREEN_HEIGHT // 2),
                              (self.__game_settings.SCREEN_WIDTH, self.__game_settings.SCREEN_HEIGHT // 2),
                              (self.__game_settings.SCREEN_WIDTH, self.__game_settings.SCREEN_HEIGHT),
                              (0, self.__game_settings.SCREEN_HEIGHT), (self.__game_settings.SCREEN_HEIGHT, 0),
                              (self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT)]

        self.__ghosts_spawner_interval = 1.4

        self.__ghosts_spawner = GhostSpawner(self.__ghosts_spawner_interval, self.__ghosts_group, self.__player)

        self.__ghosts_spawner.add_points(self.__points_list)

        self.__ghosts_spawner.set_active()

    def update(self, scaled_delta_time: float) -> None:
        self.__ghosts_spawner.update(scaled_delta_time)
