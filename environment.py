import os
import pygame as pg


class BackgroundSprite(pg.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pg.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


class DecorationSprite(pg.sprite.Sprite):
    def __init__(self, image_path: str, x_position: int, y_position: int) -> None:
        super().__init__()
        self.scale_factor = 0.82

        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (self.image.get_width() * self.scale_factor, self.image.get_height() * self.scale_factor))
        self.rect = self.image.get_rect()
        self.rect.center = (x_position, y_position)


class HerbSmall(DecorationSprite):
    def __init__(self, x_position: int, y_position: int):
        image_path = os.path.join("images", "Environment", "herbs", "herb_2.png")
        super().__init__(image_path, x_position, y_position)


class HerbBig(DecorationSprite):
    def __init__(self, x_position: int, y_position: int):
        image_path = os.path.join("images", "Environment", "herbs", "herb_1.png")
        super().__init__(image_path, x_position, y_position)


class StumpSmall(DecorationSprite):
    def __init__(self, x_position: int, y_position: int):
        image_path = os.path.join("images", "Environment", "stumps", "stump_1.png")
        super().__init__(image_path, x_position, y_position)


class StumpBig(DecorationSprite):
    def __init__(self, x_position: int, y_position: int):
        image_path = os.path.join("images", "Environment", "stumps", "stump_2.png")
        super().__init__(image_path, x_position, y_position)


class FlowerBlue(DecorationSprite):
    def __init__(self, x_position: int, y_position: int):
        image_path = os.path.join("images", "Environment", "flowers", "flower_2.png")
        super().__init__(image_path, x_position, y_position)


class FlowerWhite(DecorationSprite):
    def __init__(self, x_position: int, y_position: int):
        image_path = os.path.join("images", "Environment", "flowers", "flower_1.png")
        super().__init__(image_path, x_position, y_position)


class MushroomBrown(DecorationSprite):
    def __init__(self, x_position: int, y_position: int):
        image_path = os.path.join("images", "Environment", "mushrooms", "mushroom_1.png")
        super().__init__(image_path, x_position, y_position)


class MushroomPurple(DecorationSprite):
    def __init__(self, x_position: int, y_position: int):
        image_path = os.path.join("images", "Environment", "mushrooms", "mushroom_2.png")
        super().__init__(image_path, x_position, y_position)


class Dummy(DecorationSprite):
    def __init__(self, x_position: int, y_position: int):
        image_path = os.path.join("images", "Environment", "other", "dummy_1.png")
        super().__init__(image_path, x_position, y_position)
        self.__scale_factor = 2.0
        self.image = pg.transform.scale(self.image, (self.image.get_width() * self.__scale_factor, self.image.get_height() * self.__scale_factor))


class Environment(pg.sprite.Group):
    def __init__(self):
        super().__init__()

        self.__background = BackgroundSprite(os.path.join("images", "game_background.png"))
        self.add(self.__background)

        decorations = (
            MushroomPurple(900, 300),
            MushroomPurple(400, 550),
            MushroomPurple(700, 700),
            MushroomBrown(900, 600),
            FlowerBlue(800, 500),
            FlowerBlue(100, 100),
            FlowerWhite(200, 300),
            FlowerWhite(400, 50),
            StumpSmall(800, 350),
            StumpSmall(50, 500),
            StumpSmall(150, 600),
            StumpBig(50, 650),
            StumpBig(700, 700),
            StumpBig(150, 50),
            HerbSmall(50, 200),
            HerbSmall(950, 600),
            HerbSmall(950, 350),
            HerbSmall(300, 650),
            HerbSmall(200, 500),
            HerbSmall(300, 300),
            HerbSmall(700, 200),
            HerbSmall(900, 700),
            HerbSmall(850, 700),
            HerbSmall(450, 550),
            HerbSmall(750, 50),
            HerbBig(100, 250),
            HerbBig(200, 650),
            HerbBig(250, 700),
            HerbBig(900, 100),
            HerbBig(850, 150),
            HerbBig(650, 150),
            HerbBig(800, 650),
            Dummy(700, 100)
        )

        for decoration in decorations:
            self.add(decoration)
