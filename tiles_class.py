import pygame


class Tiles(pygame.sprite.Sprite):  # класс частей поля
    def __init__(self, *groups):
        super().__init__(*groups)
