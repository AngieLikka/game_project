import pygame
from main import load_image, all_sprites, v, FPS


class Tiles(pygame.sprite.Sprite):  # класс частей поля
    def __init__(self, x, y, long):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('tile.png', -1), (long, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= v // FPS
