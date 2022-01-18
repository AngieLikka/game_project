import pygame


class Cat(pygame.sprite.Sprite):  # класс героя
    def __init__(self, im, help, coins, *groups):
        super().__init__(*groups)
        self.photo = im
        self.num = 0
        self.i = 0
        self.transfer = help
        self.coins = coins
        try:
            while 1:
                im.seek(self.num)
                self.num += 1
        except EOFError:
            pass
        im.seek(self.i)
        im.save('new.png')
        self.image = pygame.transform.scale(pygame.image.load('new.png'), (80, 55))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 300
        self.g = 1
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, n, *args):
        global coin
        if self.g == self.num * 5:
            self.photo.seek(self.i)
            self.photo.save('new.png')
            self.i += 1
            self.i %= self.num
            self.image = pygame.transform.scale(pygame.image.load('new.png'), (80, 55))
            self.g = 0
        self.g += 1
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
                else:
                    flag = False
                    break
        if flag:
            self.rect = self.rect.move(0, n)
        for i in self.transfer.get_thingsgroup():
            if pygame.sprite.collide_mask(self, i):
                i.kill()
                self.coins.add_coin()
                return 1