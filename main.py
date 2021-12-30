import pygame
import os
import sys

pygame.init()
size = W, H = 800, 600
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
FPS = 60


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


def terminate():  # функция завершения игры
    pygame.quit()
    sys.exit()


def start_screen():  # функция запуска стартового экрана (заставки)
    pass


class Tile(pygame.sprite.Sprite):  # класс частей поля
    def __init__(self, *groups):
        super().__init__(*groups)


class Hero(pygame.sprite.Sprite):  # класс героя
    def __init__(self, *groups):
        super().__init__(*groups)


class Things(pygame.sprite.Sprite):  # класс вещей, которые герой собирает
    def __init__(self, *groups):
        super().__init__(*groups)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()  # группа частей поля
hero_group = pygame.sprite.Group()  # группа героя
things_group = pygame.sprite.Group()  # группа вещей, которые герой собирает
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    hero_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
