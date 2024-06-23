import pygame as pg
import os


def load_frames(animation_type: str, animation_object: str, frames_quantity: int, scale_factor: float) -> list:
    frames = []
    for i in range(1, frames_quantity + 1):
        frame = pg.image.load(os.path.join("images", animation_object, animation_type, f"{animation_object.lower()}_{animation_type.lower()}_{i}.png"))
        frame = pg.transform.scale(frame,(round(frame.get_width() * scale_factor), round(frame.get_height() * scale_factor)))
        frames.append(frame)
    return frames


class GameSettings:
    """Класс для хранения настроек игры."""
    GAME_FPS_MAX = 60
    GAME_BASE_FONT = "fonts/thin_pixel-7.ttf"
    GAME_BASE_FONT_SIZE = 40
    GAME_NAME = "Курица-волшебник: Побег от пламени"
    GAME_AUTHOR = "Крюков Никита А."
    GAME_AUTHOR_GROUP = "РИ-130915"

    SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    SCREEN_TITLE = f"{GAME_NAME}  //  {GAME_AUTHOR} {GAME_AUTHOR_GROUP}"
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
    COLOR_ORANGE = (239, 130, 13)


class SoundsList:
    """Класс для хранения звуков и музыки."""
    GAMEPLAY_MUSIC = "sounds/gameplay_music.mp3"
    STORY_MUSIC = "sounds/story_music.mp3"
    EXPLOSION_SOUND = "sounds/explosion_sound.mp3"
