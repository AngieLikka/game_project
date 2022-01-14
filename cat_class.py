import pygame
from main import tiles_group, things_group


class Cat(pygame.sprite.Sprite):  # класс героя
    def __init__(self, im, *groups):
        super().__init__(*groups)
        self.photo = im
        self.num = 0
        self.i = 0
        try:
            while 1:
                im.seek(self.num)
                self.num += 1
        except EOFError:
            pass
        im.seek(self.i)
        im.save('new.png')
        self.image = pygame.transform.scale(pygame.image.load('new.png'), (100, 85))
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 300
        self.g = 1

    def update(self, n, *args):
        self.rect = self.rect.move(0, n)
        if self.g == self.num * 23:
            self.photo.seek(self.i)
            self.photo.save('new.png')
            self.i += 1
            self.i %= self.num
            self.image = pygame.transform.scale(pygame.image.load('new.png'), (100, 85))
            self.g = 0
        self.g += 1
        flag = False
        for i in tiles_group:
            if pygame.sprite.collide_mask(self, i):
                self.rect = self.rect.move(0, 1)
                if pygame.sprite.collide_mask(self, i):
                    self.rect = self.rect.move(-1, 0)
                self.rect = self.rect.move(0, -1)
                flag = True
                break
        if flag:
            self.rect = self.rect.move(0, n)
        for i in things_group:
            if pygame.sprite.collide_mask(self, i):
                pass
            # надо удалить объект и добавить какую-то циферку к сумме баллов
