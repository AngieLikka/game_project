import pygame


class Cat(pygame.sprite.Sprite):  # класс героя
    def __init__(self, *groups):
        super().__init__(*groups)
