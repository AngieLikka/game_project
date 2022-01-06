import pygame
import os
import sys
from random import randint, choice
# from tiles_class import Tiles
# from things_class import Things
from cat_class import Cat

pygame.init()
pygame.font.init()
size = W, H = 800, 600
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
v = 200
FPS = 60
score = 0
font =  pygame.font.Font(None, 50)
PINK = (255, 0, 255)
time = 0


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
        self.image = pygame.transform.scale(load_image('tile.png', -1), (long, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= v // FPS


class Things(pygame.sprite.Sprite):  # класс вещей, которые герой собирает
    def __init__(self, x, y):
        super().__init__(all_sprites)
        im = choice(things_names)
        self.image = pygame.transform.scale(things_images[im], (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= v // FPS


def terminate():  # функция завершения игры
    pygame.quit()
    sys.exit()


def start_screen():  # функция запуска стартового экрана (заставки)
    pass


def add_platform():
    tile_y = randint(0, H - 100)
    tile_w = randint(300, 600)
    a = 0
    if check(tile_y):
        platform = Tiles(W, tile_y, tile_w)
        tiles_group.add(platform)
        for i in range(tile_w // 60):
            add_thing(W + a, tile_y)
            a += 60


def add_thing(x, y):
    thing = Things(x, y)
    things_group.add(thing)


def check(y):
    count = 0
    for i in tiles_group:
        if y not in range(i.rect.y - 50, i.rect.y + 50):
            count += 1
    if len(tiles_group) == count:
        return True
    else:
        return False


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()  # группа частей поля
cat_group = pygame.sprite.Group()  # группа героя
things_group = pygame.sprite.Group()  # группа вещей, которые герой собирает
things_images = {'coin' : load_image('coin.jpg', -1), 'money' : load_image('money.png', -1),
                 'milk' : load_image('milk.png')}
things_names = ['coin', 'money', 'milk']
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
    screen.fill((0, 0, 0))
    fon = pygame.transform.scale(load_image('fon_sky.jpg'), (W, H))
    screen.blit(fon, (0, 0))
    pygame.display.set_caption('game')
    if len(tiles_group) < 2:
        if len(tiles_group) == 0:
            add_platform()
        else:
            add_platform()
    for i in tiles_group:
        if i.rect.x < 0:
            add_platform()
        if i.rect.x + i.rect.width < 0:
            i.kill()
    for i in things_group:
        if i.rect.x < 0:
            i.kill()
    if time % 2 == 0:
        score += 1
    time += 1
    if score > 500:
        v += 0.5

    tiles_group.draw(screen)
    tiles_group.update()
    things_group.draw(screen)
    things_group.update()
    cat_group.draw(screen)

    text = font.render(str(score), True, PINK)
    screen.blit(text, (100, 500))

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
