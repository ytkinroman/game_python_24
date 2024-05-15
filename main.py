import sys
import pygame as pg
from colors import Colors
from game_settings import GameSettings


class Scene:
    """Базовый класс для всех сцен в игре."""
    def __init__(self) -> None:
        """Инициализация сцены."""
        pass

    def handle_events(self, events: list[pg.event.Event]) -> None:
        """Обработка нажатий."""
        pass

    def update(self, delta_time: float) -> None:
        """Обновление состояния сцены."""
        pass

    def render(self, screen: pg.Surface) -> None:
        """Рендеринг сцены на экран."""
        pass


class Game:
    def __init__(self, fps: int) -> None:
        self._is_paused = False
        self._fps = fps
        self._game_speed = 1.0
        self._delta_time = round(1 / self._fps, 3)
        self._scene = MainMenuScene(self)

    def toggle_pause(self) -> None:
        self._is_paused = not self._is_paused

    def is_game_paused(self) -> bool:
        return self._is_paused

    def set_game_speed(self, speed) -> None:
        self._game_speed = speed

    def update(self) -> None:
        scaled_delta_time = self._delta_time * self._game_speed
        self._scene.update(scaled_delta_time)

    def render(self, screen: pg.Surface) -> None:
        """Отрисовка действующей сцены."""
        self._scene.render(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        """Обработка событий действующей сцены."""
        self._scene.handle_events(event)

    def change_scene(self, scene: Scene):
        """Поменять действующую сцену."""
        self._scene = scene


class MainMenuScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._background = colors.color_blue

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self._background)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self._game.change_scene(StoryScene(self._game))


class StoryScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._background = colors.color_yellow

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self._background)

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self._game.change_scene(GameScene(self._game))


class GameScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._background = colors.color_green

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self._background)

    def update(self, scaled_delta_time: float) -> None:
        if not self._game.is_game_paused():
            self._update_game_world(scaled_delta_time)
        else:
            self._update_paused_state()

    def _update_game_world(self, scaled_delta_time: float) -> None:
        pass

    def _update_paused_state(self) -> None:
        pass

    def handle_events(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._game.toggle_pause()
            elif event.key == pg.K_1:
                self._game.change_scene(EndScene(self._game))


class EndScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__()
        self._game = game
        self._background = colors.color_black

    def render(self, screen: pg.Surface) -> None:
        screen.fill(self._background)

    def update(self, delta_time: float) -> None:
        pass

    def handle_events(self, event: pg.event.Event) -> None:
        pass


if __name__ == "__main__":
    pg.init()

    game_settings = GameSettings()
    colors = Colors()

    pg.display.set_icon(pg.image.load(game_settings.screen_icon))
    pg.display.set_caption(game_settings.screen_title)
    screen = pg.display.set_mode(game_settings.screen_size)

    clock = pg.time.Clock()
    game = Game(game_settings.game_fps_max)

    running = True
    while running:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
            game.handle_event(event)

        game.update()
        game.render(screen)

        pg.display.flip()
        clock.tick(game_settings.game_fps_max)

    pg.quit()
    sys.exit()
