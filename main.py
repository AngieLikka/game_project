import pygame
import os
import sys
from random import choice, randint
# from tiles_class import Tiles
from things_class import Things
from cat_class import Cat

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


class Tiles(pygame.sprite.Sprite):  # класс частей поля
    def __init__(self, x, y, long):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('tile.png', -1), (100, 100))
        self.rect = self.image.get_rect()

    def update(self):
        pass


def terminate():  # функция завершения игры
    pygame.quit()
    sys.exit()


def start_screen():  # функция запуска стартового экрана (заставки)
    pass


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()  # группа частей поля
cat_group = pygame.sprite.Group()  # группа героя
things_group = pygame.sprite.Group()  # группа вещей, которые герой собирает
platform = []
a = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('fon_sky.jpg'), (W, H))
    screen.blit(fon, (0, 0))
    pygame.display.set_caption('game')
    if len(tiles_group) < 5:
        platform = Tiles(0 + a, 0 + a, randint(40, 100))
        tiles_group.add(platform)
        a += 100
    tiles_group.draw(screen)
    things_group.draw(screen)
    cat_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
