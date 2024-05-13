import sys
import pygame as pg

# Game:
GAME_FPS_MAX = 60

# Screen:
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_TITLE = "PyGame | PyGame PyGame | Name Name Name Name Name Name"
SCREEN_ICON = "images/screen_game_logo.png"

# Colors:
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (192, 192, 192)


class Game:
    def __init__(self, fps: int) -> None:
        self._is_paused = False
        self._fps = fps
        self._game_speed = 1.0
        self._delta_time = round(1 / self._fps, 3)

    def toggle_pause(self) -> None:
        self._is_paused = not self._is_paused

    def is_game_paused(self) -> bool:
        return self._is_paused

    def set_game_speed(self, speed) -> None:
        self._game_speed = speed

    def update(self) -> None:
        if not self._is_paused:
            scaled_delta_time = self._delta_time * self._game_speed
            self._update_game_world(scaled_delta_time)
        else:
            self._update_paused_state()

    def _update_game_world(self, scaled_delta_time: float) -> None:
        # print("GAMEPLAY")
        pass

    def _update_paused_state(self) -> None:
        # print("PAUSE")
        pass


if __name__ == "__main__":
    pg.init()

    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption(SCREEN_TITLE)

    clock = pg.time.Clock()
    game = Game(GAME_FPS_MAX)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # PAUSE
                    game.toggle_pause()

        screen.fill(COLOR_GREEN)  # BACKGROUND

        game.update()

        pg.display.flip()
        clock.tick(GAME_FPS_MAX)

    pg.quit()
    sys.exit()
