import pygame
import os
import sys


FPS = 60
all_sprites = pygame.sprite.Group()


def load_image(filname, colorkey=None):  # функция загрузки изображения
    fulname = os.path.join("data", filname)
    if not os.path.isfile(filname):
        print('File is not found :(')
        sys.exit()
    image = pygame.image.load(fulname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image.convert_alpha()
    return image


class Tiles(pygame.sprite.Sprite):  # класс частей поля
    def __init__(self, x, y, long, sp):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('tile.png', -1), (long, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.speed = sp

    def update(self):
        self.rect.x -= self.speed.get_v() // FPS
