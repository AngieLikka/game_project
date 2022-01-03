import pygame
from main import load_image, all_sprites


class Tiles(pygame.sprite.Sprite):  # класс частей поля
    def __init__(self, x, y, long):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('tile.png', -1), (100, 100))
        self.rect = self.image.get_rect()

    def update(self):
        pass