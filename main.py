import sys
import pygame as pg
from utils import GameSettings, Colors
from environment import Environment
from simple_ui import UIPause, UIGamePlay, UIMainMenu, UIStory, UIEnding
from scene import Scene
from player import Player
from spawn_system import GhostSpawner


class Game:
    def __init__(self, fps: int) -> None:
        self.__running = True
        self._paused = False

        self._fps = fps
        self._game_speed = 1.0
        self._delta_time = round(1 / self._fps, 3)

        self._scene = GameScene(self)

    def toggle_pause(self) -> None:
        """Переключение состояния паузы."""
        self._paused = not self._paused

    def stop(self) -> None:
        """Останавливает игру."""
        self.__running = False

    def is_game_paused(self) -> bool:
        """Возвращает True, если игра находится в состоянии паузы."""
        return self._paused

    def is_game_running(self) -> bool:
        """Возвращает True, если игра запущена."""
        return self.__running

    def update(self) -> None:
        """Обновляет игру каждый кадр."""
        scaled_delta_time = self._delta_time * self._game_speed
        self._scene.update(scaled_delta_time)

    def render(self, screen: pg.Surface) -> None:
        """Отображение графики сцены на экране."""
        self._scene.render(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        """Обработка событий, которые происходят в сцене."""
        self._scene.handle_events(event)

    def change_scene(self, scene: Scene) -> None:
        """Сменить текущую сцену."""
        self._scene = scene


class MainMenuScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.__game = game
        self.__menu_scene_ui = UIMainMenu()

    def render(self, screen: pg.Surface) -> None:
        self.__menu_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.__game.change_scene(StoryScene(self.__game))


class StoryScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.__game = game
        self.__story_scene_ui = UIStory()

    def render(self, screen: pg.Surface) -> None:
        self.__story_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self.__story_scene_ui.is_next_story_text():
                    self.__story_scene_ui.next_story_text()
                    self.__story_scene_ui.set_story_text(self.__story_scene_ui.get_story_current_text())

                    if self.__story_scene_ui.get_current_index_story() == self.__story_scene_ui.is_last_story:
                        self.__story_scene_ui.set_ending_support_text()
                else:
                    self.__game.change_scene(GameScene(self.__game))


class GameScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.__game_settings = GameSettings()
        self.__colors = Colors()
        self.__game = game

        self.__environment_group = Environment()
        self.__players_group = pg.sprite.Group()
        self.__ghosts_group = pg.sprite.Group()
        self.__explosions_group = pg.sprite.Group()

        self.__gameplay_pause_ui = UIPause()
        self.__gameplay_ui = UIGamePlay()

        self.__player = Player(self.__game_settings.SCREEN_WIDTH + 150, self.__game_settings.SCREEN_HEIGHT// 2)
        self.__players_group.add(self.__player)

        self.__points_list = [(self.__game_settings.SCREEN_WIDTH // 2, 0), (0, 0),
                              (0, self.__game_settings.SCREEN_HEIGHT // 2),
                              (self.__game_settings.SCREEN_WIDTH, self.__game_settings.SCREEN_HEIGHT // 2),
                              (self.__game_settings.SCREEN_WIDTH, self.__game_settings.SCREEN_HEIGHT),
                              (0, self.__game_settings.SCREEN_HEIGHT), (self.__game_settings.SCREEN_HEIGHT, 0),
                              (self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT)]
        self.__ghosts_spawner_interval = 1.4
        self.__next_scene_delay = 6

        self.__ghosts_spawner = GhostSpawner(self.__ghosts_spawner_interval, self.__ghosts_group, self.__player)

        self.__ghosts_spawner.add_points(self.__points_list)

        self.__player.set_target_position(self.__game_settings.SCREEN_WIDTH // 2, self.__game_settings.SCREEN_HEIGHT // 2)

        self.__ghosts_spawner.set_active()

    def update(self, scaled_delta_time: float) -> None:
        if not self.__game.is_game_paused():
            self.__update_game_world(scaled_delta_time)
        else:
            self.__update_game_pause()

    def __update_game_world(self, scaled_delta_time: float) -> None:
        self.__players_group.update(scaled_delta_time)
        self.__ghosts_group.update(scaled_delta_time)
        self.__explosions_group.update(scaled_delta_time)

        self.__gameplay_ui.update(self.__player)

        if self.__player.is_alive():
            self.__ghosts_spawner.update(scaled_delta_time)

            if self.__player.get_score() >= 800:
                self.__ghosts_spawner.stop_active()

                if not self.__ghosts_group.sprites():
                    self.__player.set_target_position(-150, self.__game_settings.SCREEN_HEIGHT // 2)

                    if self.__next_scene_delay > 0:
                        self.__next_scene_delay -= scaled_delta_time
                        return

                    self.__game.change_scene(EndingScene(self.__game, self.__player))

            for ghost in self.__ghosts_group:
                if ghost.is_collide_with_player():
                    self.__player.die(self.__explosions_group)

        else:
            self.__ghosts_spawner.stop_active()

            for ghost in self.__ghosts_group:
                ghost.move_stop()

            if self.__next_scene_delay > 0:
                self.__next_scene_delay -= scaled_delta_time
                return

            self.__game.change_scene(EndingScene(self.__game, self.__player))

    def __update_game_pause(self) -> None:
        pass

    def render(self, screen: pg.Surface) -> None:
        if not self.__game.is_game_paused():
            self.__render_game_world()
        else:
            self.__render_game_pause()

    def __render_game_world(self) -> None:
        self.__environment_group.draw(screen)
        self.__players_group.draw(screen)
        self.__ghosts_group.draw(screen)
        self.__explosions_group.draw(screen)
        self.__gameplay_ui.draw(screen)

    def __render_game_pause(self) -> None:
        self.__environment_group.draw(screen)
        self.__players_group.draw(screen)
        self.__ghosts_group.draw(screen)
        self.__explosions_group.draw(screen)
        self.__gameplay_pause_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        mouse_position = pg.mouse.get_pos()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and self.__player.is_alive():
                self.__game.toggle_pause()

        if not self.__game.is_game_paused():
            self.__player.handle_events(event, mouse_position, self.__ghosts_group, self.__explosions_group)


class EndingScene(Scene):
    def __init__(self, game: Game, player: Player) -> None:
        super().__init__()
        self.__game = game
        self.__player = player
        self.__final_scene_ui = UIEnding(self.__player)

    def render(self, screen: pg.Surface) -> None:
        self.__final_scene_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.__game.stop()
            if event.key == pg.K_SPACE:
                self.__game.change_scene(GameScene(self.__game))


if __name__ == "__main__":
    pg.init()

    game_settings = GameSettings()
    colors = Colors()

    pg.display.set_icon(pg.image.load(game_settings.SCREEN_ICON))
    pg.display.set_caption(game_settings.SCREEN_TITLE)
    screen = pg.display.set_mode(game_settings.SCREEN_SIZE)

    clock = pg.time.Clock()
    game = Game(game_settings.GAME_FPS_MAX)

    while game.is_game_running():
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                game.stop()
            game.handle_events(event)

        game.update()
        game.render(screen)

        pg.display.flip()
        clock.tick(game_settings.GAME_FPS_MAX)

    pg.quit()
    sys.exit()
