import pygame


class Things(pygame.sprite.Sprite):  # класс вещей, которые герой собирает
    def __init__(self, *groups):
        super().__init__(*groups)
