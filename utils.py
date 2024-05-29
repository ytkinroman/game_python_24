class GameSettings:
    """Класс для хранения настроек игры."""
    GAME_FPS_MAX = 60
    GAME_BASE_FONT = "fonts/thin_pixel-7.ttf"
    GAME_BASE_FONT_SIZE = 40
    GAME_TITLE = "Введите название игры"
    GAME_AUTHOR = "Крюков Никита Андреевич (РИ-130915)"

    SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    SCREEN_TITLE = f"| Python | PyGame | {GAME_TITLE} | {GAME_AUTHOR} | АТ-04 |"
    SCREEN_ICON = "images/screen_game_logo.png"


class Colors:
    """Класс для хранения часто используемых цветов."""
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_BLACK = (0, 0, 0)
    COLOR_WHITE = (255, 255, 255)
    COLOR_GRAY = (192, 192, 192)
