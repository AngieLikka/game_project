import pygame
from PIL import Image

tiles_group = pygame.sprite.Group()  # группа частей поля
bad_cat = pygame.sprite.Group()
cat_group = pygame.sprite.Group()  # группа героя


class Cat(pygame.sprite.Sprite):  # класс героя
    def __init__(self, im, help, coins, *groups):
        super().__init__(*groups)
        self.photo = im
        self.num = 300
        self.transfer = help
        self.coins = coins
        im = Image.open(self.photo)
        im_crop = im.crop((0, 0, 300, 200))
        im_crop.save('cat.png', quality=95)
        self.image = pygame.transform.scale(pygame.image.load('cat.png'), (80, 55))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 300
        self.mask = pygame.mask.from_surface(self.image)

    def new(self):
        im = Image.open(self.photo)
        self.num += 300
        self.num %= im.size[0]
        im_crop = im.crop((self.num, 0, self.num + 300, 200))
        im_crop.save('cat.png', quality=95)
        self.image = pygame.transform.scale(pygame.image.load('cat.png'), (80, 55))

    def update(self, n, *args):
        global coin
        for i in tiles_group:
            if pygame.sprite.collide_mask(self, i):
                if self.rect.x + self.rect.width - 20 <= i.rect.x <= self.rect.x + self.rect.width + 20:
                    self.rect = self.rect.move(-1, 0)
                if i.rect.y <= self.rect.y + self.rect.height <= i.rect.y + 50 and n == 1:
                    n = 0
                    break
                elif i.rect.y - 1 <= self.rect.y <= i.rect.y + 50 and n == -1:
                    n = 0
                    break
        self.rect = self.rect.move(0, n)
        for i in self.transfer.get_thingsgroup():
            if pygame.sprite.collide_mask(self, i):
                i.kill()
                self.coins.add_coin()
                return 1


class BadCat(pygame.sprite.Sprite):  # класс плохого кота
    def __init__(self, y, help, *groups):
        super().__init__(*groups)
        self.photo = "evil.png"
        self.num = 0
        im = Image.open(self.photo)
        im_crop = im.crop((0, 0, 300, 200))
        im_crop.save('newe.png', quality=95)
        self.image = pygame.transform.scale(pygame.image.load('newe.png'), (80, 55))
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def peresec(self):
        for i in cat_group:
            return pygame.sprite.collide_mask(self, i)

    def new(self):
        im = Image.open(self.photo)
        self.num += 300
        self.num %= im.size[0]
        im_crop = im.crop((self.num, 0, self.num + 300, 200))
        im_crop.save('newe.png', quality=95)
        self.image = pygame.transform.scale(pygame.image.load('newe.png'), (80, 55))

    def update(self, n, *args):
        if n == 0:
            self.rect = self.rect.move(-2, 0)
