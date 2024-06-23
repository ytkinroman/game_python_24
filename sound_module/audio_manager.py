import pygame as pg
from utils import SoundsList


class AudioManager:
    def __init__(self):
        self.__music = SoundsList()
        pg.mixer.init()

    def play_background_music(self) -> None:
        pg.mixer.music.load(self.__music.GAMEPLAY_MUSIC)
        pg.mixer.music.play(-1)

    def play_explosion_sound(self, volume: float) -> None:
        exp = pg.mixer.Sound(self.__music.EXPLOSION_SOUND)
        exp.set_volume(volume)
        exp.play()

