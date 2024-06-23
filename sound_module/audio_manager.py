import pygame as pg
from utils import SoundsList


class AudioManager:
    def __init__(self):
        self.__music = SoundsList()
        pg.mixer.init()

    def play_story_music(self) -> None:
        pg.mixer.music.load(self.__music.STORY_MUSIC)
        pg.mixer.music.play(-1)

    def play_background_music(self) -> None:
        pg.mixer.music.load(self.__music.GAMEPLAY_MUSIC)
        pg.mixer.music.play(-1)

    def play_explosion_sound(self) -> None:
        exp = pg.mixer.Sound(self.__music.EXPLOSION_SOUND)
        exp.play()
