import pygame
import os
import sys
from random import choice
from tiles_class import Tiles
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


def terminate():  # функция завершения игры
    pygame.quit()
    sys.exit()


def start_screen():  # функция запуска стартового экрана (заставки)
    pass


def generate_map(sc):
    map = [[0] * W for i in range(H)]
    cell_size = 30
    platforms_long = [3, 4, 5, 6]
    max_amount = 5
    left, top = 0, 0
    fon = pygame.transform.scale(load_image('fon_sky.jpg'), (W, H))
    screen.blit(fon, (0, 0))
    for i in range(W):
        for j in range(H):
            pygame.draw.rect(sc, (100, 100, 150), (left + (i * cell_size),
                                               top + (j * cell_size),
                                               cell_size, cell_size), 1)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()  # группа частей поля
cat_group = pygame.sprite.Group()  # группа героя
things_group = pygame.sprite.Group()  # группа вещей, которые герой собирает
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
    screen.fill((0, 0, 0))
    pygame.display.set_caption('game')
    generate_map(screen)
    tiles_group.draw(screen)
    things_group.draw(screen)
    cat_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
