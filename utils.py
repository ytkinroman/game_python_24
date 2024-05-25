import pygame as pg


class BackgroundSprite(pg.sprite.Sprite):
    def __init__(self, image_path):
        super().__init__()
        self.image = pg.image.load(image_path).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)  # РАСПОЛОЖЕНИЕ В ВЕРХНЕМ ЛЕВОМ УГЛУ
