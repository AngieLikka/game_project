import pygame
from main import load_image, all_sprites, v, FPS


class Things(pygame.sprite.Sprite):  # класс вещей, которые герой собирает
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image_coin = pygame.transform.scale(load_image('coin.jpg', -1), (100, 100))
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= v // FPS