import sys
import pygame as pg
from utils import GameSettings, Colors
from game import Game


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
