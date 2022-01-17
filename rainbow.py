import pygame
import random


class RainbowBAD(pygame.sprite.Sprite):
    def __init__(self, x, y, help, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load('rainbowbad.jpg'), (30, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.transfer = help

    def update(self, *args):
        self.rect.x = self.rect.x - 2


class Rainbow(pygame.sprite.Sprite):
    def __init__(self, x, y, z, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load('rainbow.jpg'), (z, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, x, y, *args):
        self.rect.x = self.rect.x - 1
        if self.rect.x <= -20:
            self.rect.x = x + 5
            self.rect.y = y + random.randint(1, 3)

