import os
import random
import sys
import pygame_gui
import sqlite3
from PIL import Image, ImageSequence
import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
from tiles_class import Tiles
from things_class import Things
from cat_class import Cat
from random import randint
from speed_class import Speed
from text import TextInputBox
from rainbow import RainbowBAD, Rainbow
from cat import BadCat
from t import Transfer
from coins import Coins

pygame.init()
pygame.mixer.music.load('Nyan Cat.mp3')
pygame.mixer.music.play(-1)
size = W, H = 900, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Nyan Cat')
clock = pygame.time.Clock()
FPS = 300
FONT = pygame.font.SysFont(None, 25)
NUM = 0
coin = Coins()
new_record = False
CATS = {0: "cat0.gif", 1: "cat1.gif", 2: "cat2.gif", 3: "cat3.gif", 4: "cat4.gif",
        5: "cat6.gif", 6: "cat7.gif", 7: "cat9.gif", 8: "cat10.gif", 9: "cat11.gif"}
PINK = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
time = 0
score = 0
v = 100
speed = Speed(v)


def load_image(filname, colorkey=None):  # функция загрузки изображения
    fulname = os.path.join("data", filname)
    if not os.path.isfile(filname):
        print('File is not found :(')
        print(filname)
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
    intro_text = ["Логин", "", "Пароль", "", "Чтобы закончить ввод, нажмите ЕNTER", "", "", "", "", "", "", "", "", "",
                  "",
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
                r = False
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
    global time, score, new_record
    new_record = False
    coin.set_coins()
    rainbow_bad.empty()
    rainbow.empty()
    screen = pygame.display.set_mode(size)
    t = True
    font = pygame.font.SysFont(None, 100)
    cat = Cat(Image.open(CATS[NUM]), transfer, coin)
    cat_group.add(cat)
    score = 0
    schetchik_1 = 0
    schetchik_2 = 0
    schetchik_3 = 0
    schetchik_4 = 0
    schetchik_5 = 0
    bad = 0
    main_f = False
    for i in range(-30, 220, 30):
        if i % 60 == 0:
            rain = Rainbow(i, 306, 30)
        else:
            rain = Rainbow(i, 308, 30)
        rainbow.add(rain)
    with Image.open('fon2.gif') as im:
        try:
            while 1:
                im.seek(schetchik_4)
                schetchik_4 += 1
        except EOFError:
            pass
    while t:
        if schetchik_5 == 25:
            with Image.open('fon2.gif') as im:
                im.seek(schetchik_3)
                im.save('newf.png')
            schetchik_3 += 1
            schetchik_3 %= schetchik_4
            schetchik_5 = 0
        schetchik_5 += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t = False
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    schetchik_1 = -1
                if event.key == pygame.K_DOWN:
                    schetchik_1 = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    schetchik_1 = 0
                if event.key == pygame.K_UP:
                    schetchik_1 = 0
        fon = pygame.transform.scale(pygame.image.load('newf.png'), (W, H))
        screen.blit(fon, (0, 0))
        generate_platforms()
        for i in tiles_group:
            if i.rect.x < 0:
                add_platform()
            if i.rect.x + i.rect.width < 0:
                i.kill()
        for i in things_group:
            if i.rect.x + i.rect.width < 0:
                i.kill()
        if time % 50 == 0:  # добавление очков
            score += 1
        time += 1
        if time % 9000 == 8000:
            bad = BadCat(random.randint(0, 620), transfer)
            bad_cat.add(bad)
            for i in range(960, 2080, 30):
                if i % 60 == 0:
                    rr = RainbowBAD(i, bad.rect.y + 1, transfer)
                else:
                    rr = RainbowBAD(i, bad.rect.y - 1, transfer)
                rainbow_bad.add(rr)
        if score % 300 == 0:
            speed.change_v()
        if bad != 0 and bad.rect.x <= -82:
            bad.kill()
            bad = 0
        for i in rainbow_bad:
            if i.rect.x <= - 30:
                i.kill()
        if bad != 0:
            bad.update(0)
        if schetchik_1 != 0:
            schetchik_2 = schetchik_2 + 1
            if schetchik_2 == 3:
                cat_group.update(schetchik_1)
                schetchik_2 = 0
        if bad != 0:
            main_f = bad.peresec()
        screen.blit(fon, (0, 0))
        tiles_group.draw(screen)  # отрисовка и обновление спрайтов
        tiles_group.update()
        things_group.draw(screen)
        things_group.update()
        rainbow_bad.update()
        rainbow_bad.draw(screen)
        bad_cat.update(1)
        bad_cat.draw(screen)
        rainbow.update(cat.rect.x, cat.rect.y)
        rainbow.draw(screen)
        cat_group.update(0)
        cat_group.draw(screen)
        if cat.rect.x <= -50 or cat.rect.y < 0 or cat.rect.y + cat.rect.height > 700 or main_f:
            if bad != 0:
                bad.kill()
                for i in rainbow_bad:
                    i.kill()
            cat.kill()
            time = 0
            speed.set_v()
            tiles_group.empty()
            things_group.empty()
            t = False
            cur.execute("UPDATE users SET allmoney = ? WHERE id = ?",
                        (cur.execute("""SELECT allmoney FROM users WHERE id = ?""",
                                     (user,)).fetchall()[0][0] + coin.get_coins() // 10, user,)).fetchall()
            mr = cur.execute("""SELECT maxroad FROM users WHERE name = ?""", [login]).fetchone()
            if score > int(*mr):
                new_record = True
                cur.execute("""UPDATE users SET maxroad = ? WHERE name = ?""", [score, login])
            con.commit()
            fon = pygame.transform.scale(load_image('game_over.png'), (W, H))
            screen.blit(fon, (0, 0))
            t1 = font.render('Игра окончена!', True, WHITE)
            screen.blit(t1, (200, 200))
            t2 = FONT.render('Для продолжения нажмите любую клавишу', True, WHITE)
            screen.blit(t2, (200, 500))
            pygame.display.flip()
            end_screen()
        text = FONT.render('Nyan метры: ' + str(score), True, PINK)
        screen.blit(text, (100, 650))
        text = FONT.render('Собранные предметы: ' + str(coin.get_coins()), True, PINK)
        screen.blit(text, (100, 680))
        pygame.display.update()


def add_platform():  # функция добавления платформы
    tile_y = randint(0, H - 100)
    tile_w = randint(300, 600)
    a = 0
    if check(tile_y):
        platform = Tiles(W, tile_y, tile_w, speed)
        tiles_group.add(platform)
        for i in range(tile_w // 60):
            add_thing(W + a, tile_y)
            a += 60


def add_thing(x, y):  # функция добавления вещей на платформы
    thing = Things(x, y, things_names_all[NUM], things_images_all[NUM], speed)
    things_group.add(thing)


def check(y):  # проверка местоположения платформы
    count = 0
    for i in tiles_group:
        if y not in range(i.rect.y - 50, i.rect.y + 50):
            count += 1
    if len(tiles_group) == count:
        return True
    else:
        return False


def generate_platforms():
    if len(tiles_group) < 2:  # создание платформ
        if len(tiles_group) == 0:
            add_platform()
        else:
            add_platform()


def end_screen():
    r = True
    while r:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = False
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                r = False
                final_menu()


def final_menu():
    manager = pygame_gui.UIManager((W, H))
    tomenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 100), (200, 50)),
                                          text='В главное меню', manager=manager)
    watch_rec = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 300), (200, 50)),
                                             text='Таблица рекордов', manager=manager)
    toplay = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 500), (200, 50)),
                                          text='Играть', manager=manager)
    req = con.execute("""SELECT maxroad FROM users WHERE name = ?""", [login]).fetchone()
    text = ['Пройденное расстояние: ' + str(score), 'Полученные монеты: ' + str(coin.get_coins() // 10),
            'Максимальное пройденное расстояние: ' + str(req[0])]
    font = pygame.font.SysFont(None, 100)
    record_text = font.render('', True, WHITE)
    if new_record:
        record_text = font.render('Новый рекорд!', True, WHITE)
    text_coord = 200
    t = True
    show_text = False
    fon = pygame.transform.scale(load_image('game_over.png'), (W, H))
    screen.blit(fon, (0, 0))
    while t:
        manager.update(FPS)
        manager.draw_ui(screen)
        if not show_text:
            screen.blit(record_text, (300, 100))
            for line in text:
                l = FONT.render(line, True, WHITE)
                l_rect = l.get_rect()
                text_coord += 15
                l_rect.top = text_coord
                l_rect.x = 300
                text_coord += l_rect.height
                screen.blit(l, l_rect)
                show_text = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t = False
                terminate()
            if event.type == USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == tomenu:
                        t = False
                        menu()
                    if event.ui_element == watch_rec:
                        t = False
                        records()
                    if event.ui_element == toplay:
                        t = False
                        play()
            manager.process_events(event)
            pygame.display.flip()


def records():
    manager = pygame_gui.UIManager((W, H))
    tofinal = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 500), (200, 50)),
                                           text='Назад', manager=manager)
    res = con.execute("""SELECT name, maxroad, allmoney FROM users ORDER BY maxroad DESC""").fetchmany(7)
    text_player = ['Игрок']
    text_maxroad = ['Максимальный путь']
    text_money = ['Количество монет']
    for i in res:
        text_player.append(str(i[0]))
        text_maxroad.append(str(i[1]))
        text_money.append(str(i[2]))
    font = pygame.font.SysFont(None, 40)
    r = True
    while r:
        fon = pygame.transform.scale(load_image('game_over.png'), (W, H))
        screen.blit(fon, (0, 0))
        text_c = 70
        for line in range(len(text_player)):
            l_p = font.render(text_player[line], True, WHITE)
            lp_rect = l_p.get_rect()
            l_mr = font.render(text_maxroad[line], True, WHITE)
            lmr_rect = l_mr.get_rect()
            l_m = font.render(text_money[line], True, WHITE)
            lm_rect = l_m.get_rect()
            text_c += 15
            lp_rect.top, lmr_rect.top, lm_rect.top = text_c, text_c, text_c
            lp_rect.x, lmr_rect.x, lm_rect.x = 50, 250, 550
            text_c += lp_rect.height
            screen.blit(l_p, lp_rect)
            screen.blit(l_mr, lmr_rect)
            screen.blit(l_m, lm_rect)
        manager.update(FPS)
        manager.draw_ui(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = False
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == tofinal:
                        r = False
                        final_menu()
            manager.process_events(event)
            pygame.display.flip()


def setting():
    global CATS, NUM
    NUM = 0
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(pygame.image.load('menu.jpg'), (W, H))
    manager = pygame_gui.UIManager((W, H))
    tomenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 640), (200, 50)),
                                          text='В меню', manager=manager)
    next = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 600), (200, 85)),
                                        text='Следующий', manager=manager)
    money = con.execute("""SELECT allmoney FROM users WHERE name = ?""", [login]).fetchone()
    t = True
    i = 0
    k = 0
    font = pygame.font.SysFont(None, 40)
    with Image.open(CATS[NUM]) as im:
        im.seek(i)
        im.save('new.png')
        try:
            while 1:
                im.seek(k)
                k += 1
        except EOFError:
            pass
    buy = 0
    text_money = str(*money)
    while t:
        with Image.open(CATS[NUM]) as im:
            im.seek(i)
            im.save('new.png')
        i += 1
        i %= k
        screen.blit(fon, (0, 0))
        text_playermoney = font.render('Ваши монеты: {}'.format(text_money), True, BLACK)
        screen.blit(text_playermoney, (350, 100))
        screen.blit(pygame.transform.scale(pygame.image.load('new.png'), (300, 250)), (300, 180))
        result = cur.execute("""SELECT * FROM kittens WHERE id == ?""", (user,)).fetchall()
        if result[0][NUM + 1] == 0 and buy == 0:
            buy = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((370, 620), (200, 65)),
                                               text='Купить', manager=manager)
        elif result[0][NUM + 1] == 1 and buy != 0:
            buy.kill()
            buy = 0
        if result[0][NUM + 1] == 0:
            text = FONT.render(f'{NUM * 15} coins', True, PINK)
            screen.blit(text, (370, 600))
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t = False
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == next:
                        NUM += 1
                        NUM %= 10
                        k = 0
                        i = 0
                        with Image.open(CATS[NUM]) as im:
                            try:
                                while 1:
                                    im.seek(k)
                                    k += 1
                            except EOFError:
                                pass
                    if event.ui_element == tomenu:
                        if result[0][NUM + 1] == 0:
                            NUM = 0
                        t = False
                        menu()
                    if buy != 0 and event.ui_element == buy:
                        coin = cur.execute("""SELECT allmoney FROM users WHERE id == ?""", (user,)).fetchall()[0][0]
                        if coin >= NUM * 15:
                            print(1)
                            cur.execute("""UPDATE users SET allmoney = ? WHERE id = ?""",
                                        (coin - NUM * 15, user,)).fetchall()
                            text_money = coin - NUM * 15
                            pygame.display.flip()
                            cur.execute(f"UPDATE kittens SET cat{NUM} = 1 WHERE id = {user}").fetchall()
                            con.commit()
            manager.process_events(event)
        clock.tick(10)


def rules():
    fon = pygame.transform.scale(pygame.image.load('menu.jpg'), (W, H))
    screen.blit(fon, (0, 0))
    manager = pygame_gui.UIManager((W, H))
    tomenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 640), (200, 50)),
                                          text='В меню', manager=manager)
    text = ['Добро пожаловать в аналог игры Nyan Cat!', 'Правила:',
            '- Вы играете за котика! Вы можете выбрать разных героев в настройках',
            '- Котик управляется стрелками "вверх-вних" на клавиатуре',
            '- Ваша задача: пролететь как можно больше нян-метров и заработать как можно больше монет',
            '- Монеты даются за собирание разных предметов на платформах',
            '- Количество заработанных монет в конце игры будет делится на 10, чтобы играть было веселее :)',
            '- За монеты Bы можете купить новых героев', '- Кстати, у каждого героя свои предметы!',
            '- Осторожно! Вам будут мешать злые котики! Не попадайтесь у них на пути!',
            '- После окончания игры Вы сможете посмотреть свой личный результат и рекорды других игроков',
            'Удачной игры!']
    text_coord = 30
    show_text = False
    t = True
    while t:
        manager.update(FPS)
        manager.draw_ui(screen)
        if not show_text:
            for line in text:
                l = FONT.render(line, True, BLACK)
                l_rect = l.get_rect()
                text_coord += 15
                l_rect.top = text_coord
                l_rect.x = 30
                text_coord += l_rect.height
                screen.blit(l, l_rect)
                show_text = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t = False
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == tomenu:
                        t = False
                        menu()
            manager.process_events(event)
            pygame.display.flip()


def music():
    fon = pygame.transform.scale(pygame.image.load('menu.jpg'), (W, H))
    screen.blit(fon, (0, 0))
    manager = pygame_gui.UIManager((W, H))
    tomenu = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 640), (200, 50)),
                                          text='В меню', manager=manager)
    nyancat = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 100), (200, 50)),
                                           text='Выбрать', manager=manager)
    vagner = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 170), (200, 50)),
                                          text='Выбрать', manager=manager)
    illusion = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 240), (200, 50)),
                                            text='Выбрать', manager=manager)
    gala = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 310), (200, 50)),
                                        text='Выбрать', manager=manager)
    lty = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 380), (200, 50)),
                                       text='Выбрать', manager=manager)
    lalala = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 450), (200, 50)),
                                          text='Выбрать', manager=manager)
    text = ['Здесь Вы можете выбрать музыку для игры', 'Nyan Cat', 'Вагнер - Полёт Валькирий',
            'Benny Benassi — Illusion', 'Gala — Freed From Desire', 'James Blake — Limit to Your Love',
            'Naughty Boy — La La La']
    text_coord = 0
    show_text = False
    t = True
    while t:
        manager.update(FPS)
        manager.draw_ui(screen)
        if not show_text:
            for line in text:
                l = FONT.render(line, True, BLACK)
                l_rect = l.get_rect()
                text_coord += 52
                l_rect.top = text_coord
                l_rect.x = 300
                text_coord += l_rect.height
                screen.blit(l, l_rect)
                show_text = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                t = False
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == tomenu:
                        t = False
                        menu()
                    if event.ui_element == nyancat:
                        pygame.mixer.music.load('Nyan Cat.mp3')
                        pygame.mixer.music.play(-1)
                    if event.ui_element == vagner:
                        pygame.mixer.music.load('Вагнер - Полет Валькирий (megasongs.net).mp3')
                        pygame.mixer.music.play(-1)
                    if event.ui_element == illusion:
                        pygame.mixer.music.load('Benny Benassi — Illusion (feat. Sandy).mp3')
                        pygame.mixer.music.play(-1)
                    if event.ui_element == gala:
                        pygame.mixer.music.load('Gala — Freed From Desire (MaxiGroove.mp3')
                        pygame.mixer.music.play(-1)
                    if event.ui_element == lty:
                        pygame.mixer.music.load('James Blake — Limit to Your Love.mp3')
                        pygame.mixer.music.play(-1)
                    if event.ui_element == lalala:
                        pygame.mixer.music.load('Naughty Boy — La La La (Feat. Sam Smith).mp3')
                        pygame.mixer.music.play(-1)
            manager.process_events(event)
            pygame.display.flip()


def menu():
    screen = pygame.display.set_mode(size)
    manager = pygame_gui.UIManager((W, H))
    toplay = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 540), (200, 85)),
                                          text='Играть', manager=manager)
    settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 540), (200, 85)),
                                            text='Настройки', manager=manager)
    torules = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((30, 50), (200, 85)),
                                           text='Правила', manager=manager)
    tomusic = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((670, 50), (200, 85)),
                                           text='Музыка', manager=manager)
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
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
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
                    if event.ui_element == torules:
                        t = False
                        rules()
                    if event.ui_element == tomusic:
                        t = False
                        music()
            manager.process_events(event)


# ВЕСЬ ЦИКЛ РАБОТЫ ПРОГРАММЫ!!!!!


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()  # группа частей поля
cat_group = pygame.sprite.Group()  # группа героя
things_group = pygame.sprite.Group()  # группа вещей, которые герой собирает
bad_cat = pygame.sprite.Group()
rainbow = pygame.sprite.Group()
rainbow_bad = pygame.sprite.Group()
transfer = Transfer(tiles_group, things_group, cat_group)
things_images_t0 = {'rainbow': load_image('rainbow.png', -1), 'cloud': load_image('cloud.png', -1)}
things_names_t0 = ['rainbow', 'cloud']
things_images_t1 = {'nut': load_image('nut.png', -1), 'nuts': load_image('nuts.jpg', -1)}
things_names_t1 = ['nut', 'nuts']
things_images_t2 = {'candy': load_image('candy.png'), 'donut': load_image('donut.png')}
things_names_t2 = ['candy', 'donut']
things_images_t3 = {'sandwitch': load_image('doner.png', -1), 'veg': load_image('vegetables.png', -1)}
things_names_t3 = ['sandwitch', 'veg']
things_images_t4 = {'molniia': load_image('molniia.png', -1), 'ball': load_image('ball.png', -1)}
things_names_t4 = ['molniia', 'ball']
things_images_t5 = {'coin': load_image('coin.jpg', -1), 'money': load_image('money.png', -1)}
things_names_t5 = ['coin', 'money']
things_images_t6 = {'lucky': load_image('lucky.png', -1), 'beer': load_image('beer.png', -1)}
things_names_t6 = ['lucky', 'beer']
things_images_t7 = {'bone': load_image('bone.png', -1), 'tako': load_image('tako.png', -1)}
things_names_t7 = ['bone', 'tako']
things_images_t8 = {'milk': load_image('milk.png'), 'cookie': load_image('cookie.png')}
things_names_t8 = ['milk', 'cookie']
things_images_t9 = {'sun': load_image('sun.png', -1), 'moon': load_image('moon.png')}
things_names_t9 = ['sun', 'moon']
things_names_all = [things_names_t0, things_names_t1, things_names_t2, things_names_t3, things_names_t4,
                    things_names_t5, things_names_t6, things_names_t7, things_names_t8, things_names_t9]
things_images_all = [things_images_t0, things_images_t1, things_images_t2, things_images_t3, things_images_t4,
                     things_images_t5, things_images_t6, things_images_t7, things_images_t8, things_images_t9]
login, password = start_screen()
con = sqlite3.connect("nyan.db")
cur = con.cursor()
try:
    result = cur.execute("""SELECT * FROM users WHERE name == ? AND password == ?""", (login, password)).fetchall()
    try:
        r = result[0]
    except:
        r = -1
    if r == -1:
        cur.execute("""INSERT INTO users(name, password, maxroad, allmoney) VALUES(?, ?, ?, ?)""",
                    (login, password, 0, 0)).fetchall()
        con.commit()
        result = cur.execute("""SELECT * FROM users WHERE name == ? AND password == ?""", (login, password)).fetchall()
        r = result[0][0]
        cur.execute("INSERT INTO kittens (id, cat0, cat1, cat2, cat3, cat4, cat5, cat6, cat7, cat8, cat9) "
                    "VALUES(?, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)", (r,)).fetchall()
        user = r
        con.commit()
    else:
        user = result[0][0]
except:
    cur.execute('CREATE TABLE users ( id INTEGER PRIMARY KEY UNIQUE NOT NULL, name TEXT,'
                ' password TEXT, maxroad INTEGER, allmoney INTEGER)')
    cur.execute('CREATE TABLE kittens (id PRIMARY KEY REFERENCES users (id) UNIQUE NOT NULL, '
                'cat0 INTEGER DEFAULT (1), cat1 INTEGER DEFAULT (1), cat2 INTEGER DEFAULT (0), '
                'cat3 INTEGER DEFAULT (0), cat4 INTEGER DEFAULT (0), cat5 INTEGER DEFAULT (0), '
                'cat6 INTEGER DEFAULT (0), cat7 INTEGER DEFAULT (0), cat8 INTEGER DEFAULT (0), '
                'cat9 INTEGER DEFAULT (0))')
    cur.execute("INSERT INTO users(id, name, password, maxroad, allmoney) "
                "VALUES(0, ?, ?, ?, ?)", (login, password, 0, 0)).fetchall()
    cur.execute("INSERT INTO kittens (id, cat0, cat1, cat2, cat3, cat4, cat5, cat6, cat7, cat8, cat9) "
                "VALUES(0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)").fetchall()
    user = 0
    con.commit()

menu()
pygame.quit()
