import sys
import pygame as pg
from utils import GameSettings, Colors
from environment import Environment
from simple_ui import UIPause, UIGamePlay
from scene import Scene
from player import Player


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


class GameScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self.__game_settings = GameSettings()
        self.__colors = Colors()
        self.__game = game

        self.__environment_group = Environment()
        self.__players_group = pg.sprite.Group()

        self.__gameplay_pause_ui = UIPause()
        self.__gameplay_ui = UIGamePlay()

        self.__player = Player(200, 200)
        self.__players_group.add(self.__player)

    def update(self, scaled_delta_time: float) -> None:
        if not self.__game.is_game_paused():
            self.__update_game_world(scaled_delta_time)
        else:
            self.__update_game_pause()

    def __update_game_world(self, scaled_delta_time: float) -> None:
        self.__players_group.update(scaled_delta_time)
        self.__gameplay_ui.update(self.__player)

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
        self.__gameplay_ui.draw(screen)

    def __render_game_pause(self) -> None:
        self.__environment_group.draw(screen)
        self.__players_group.draw(screen)
        self.__gameplay_pause_ui.draw(screen)

    def handle_events(self, event: pg.event.Event) -> None:
        mouse_pos = pg.mouse.get_pos()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.__game.toggle_pause()
            self.__player.controller.handle_events(event, mouse_pos)


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
