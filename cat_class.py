import pygame
from PIL import Image


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
        flag = True
        for i in self.transfer.get_tilesgroup():
            if pygame.sprite.collide_mask(self, i):
                if i.rect.x - 13 <= self.rect.x + self.rect.width <= i.rect.x + 13:
                    self.rect = self.rect.move(-1, 0)
                elif i.rect.y - 50 <= self.rect.y + self.rect.height <= i.rect.y + 50 and n == 1:
                    flag = False
                    break
                elif i.rect.y - 50 + i.rect.height <= self.rect.y <= i.rect.y + 50 + i.rect.height and n == -1:
                    flag = False
                    break
        if flag:
            self.rect = self.rect.move(0, n)
        for i in self.transfer.get_thingsgroup():
            if pygame.sprite.collide_mask(self, i):
                i.kill()
                self.coins.add_coin()
                return 1