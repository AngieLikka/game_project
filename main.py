import os
import sys
import pygame_gui
import sqlite3
from PIL import Image, ImageSequence
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
from tiles_class import Tiles
from things_class import Things
from cat_class import Cat

pygame.init()
size = W, H = 900, 700
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.SysFont(None, 25)


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width() + 10), 25), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft=self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()

    def get(self):
        return self.text


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


def entry():
    login = TextInputBox(250, 160, 400, FONT)
    password = TextInputBox(250, 230, 400, FONT)
    group = pygame.sprite.Group(login, password)
    pygame.display.update()
    intro_text = ["Логин", "", "Пароль", "", "", "", "", "", "", "", "", "", "", "", "",
                  "Для продолжения нажмите ПРОБЕЛ"]
    fon = pygame.transform.scale(pygame.image.load('input.jpg'), (W, H))
    r = True
    while r:
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 120
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 15
            intro_rect.top = text_coord
            intro_rect.x = 250
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        e = pygame.event.get()
        for event in e:
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    r = False
                    return login.get(), password.get()
        group.update(e)
        group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    return


def start_screen():
    line = "Для продолжения нажмите на любую клавишу"
    fon = pygame.transform.scale(pygame.image.load('start.jpg'), (W, H))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 670
    string_rendered = font.render(line, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = text_coord
    intro_rect.x = 210
    text_coord += intro_rect.height
    screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                l, p = entry()
                return l, p
        pygame.display.flip()
        clock.tick(FPS)


def play():
    screen = pygame.display.set_mode(size)


def setting():
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(pygame.image.load('menu.jpg'), (W, H))
    screen.blit(fon, (0, 0))
    pygame.display.flip()

def menu():
    screen = pygame.display.set_mode(size)
    manager = pygame_gui.UIManager((W, H))
    toplay = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 540), (200, 85)),
                                          text='Играть', manager=manager)
    settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 540), (200, 85)),
                                            text='Настройки', manager=manager)
    gif = Image.open('tomenu.gif')
    frames = [f.copy().convert("RGBA") for f in ImageSequence.Iterator(gif)]
    i = 0
    t = True
    while t:
        with Image.open('tomenu.gif') as im:
            im.seek(i)
            im.save('new.png'.format(i))
        i += 1
        i %= 50
        fon = pygame.transform.scale(pygame.image.load('new.png'), (W, H))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t = False
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == toplay:
                        t = False
                        play()
                    if event.ui_element == settings:
                        t = False
                        setting()
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)

# ВЕСЬ ЦИКЛ РАБОТЫ ПРОГРАММЫ!!!!!


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()  # группа частей поля
cat_group = pygame.sprite.Group()  # группа героя
things_group = pygame.sprite.Group()  # группа вещей, которые герой собирает
screen = pygame.display.set_mode((W, H))
login, password = start_screen()
con = sqlite3.connect("nyan.db")
cur = con.cursor()
try:
    result = cur.execute("""SELECT * FROM users WHERE name == ? AND password == ?""", (login, password)).fetchall()
    if len(result) == 0:
        cur.execute("""INSERT INTO users(name, password, maxroad, allmoney) VALUES(?, ?, ?, ?)""",
                    (login, password, 0, 0)).fetchall()
        user = (login, password, 0, 0)
        con.commit()
    else:
        user = result[0]
except:
    cur.execute('CREATE TABLE users ( id INTEGER PRIMARY KEY UNIQUE NOT NULL, name TEXT,'
                ' password TEXT, maxroad INTEGER, allmoney INTEGER)')
    cur.execute("INSERT INTO users(name, password, maxroad, allmoney) "
                "VALUES(?, ?, ?, ?)", (login, password, 0, 0)).fetchall()
    user = (login, password, 0, 0)
    con.commit()
menu()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
pygame.quit()
