import sys
import pygame

# Game:
GAME_FPS_MAX = 60

# Screen:
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

SCREEN_TITLE = "Template PyGame 0.1"

# Colors:
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)


class Game:
    def __init__(self):
        self.is_paused = False
        self.game_speed = 1.0
        self.delta_time = 0.016

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def set_game_speed(self, speed):
        self.game_speed = speed

    def update(self):
        if not self.is_paused:
            scaled_delta_time = self.delta_time * self.game_speed
            self.update_game_world(scaled_delta_time)
        else:
            self.update_paused_state()

    def update_game_world(self, scaled_delta_time):
        pass

    def update_paused_state(self):
        pass


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(SCREEN_TITLE)

    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.toggle_pause()

        screen.fill(COLOR_GREEN)  # BACKGROUND

        game.update()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
