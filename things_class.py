import pygame
from main import load_image, all_sprites, v, FPS
from random import choice


class Things(pygame.sprite.Sprite):  # класс вещей, которые герой собирает
    def __init__(self, x, y, name_t, image_t):
        super().__init__(all_sprites)
        im = choice(name_t)
        self.image = pygame.transform.scale(image_t[im], (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= v // FPS
