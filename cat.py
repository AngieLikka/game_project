import pygame
from PIL import Image
bad_cat = pygame.sprite.Group()
FPS = 60


class BadCat(pygame.sprite.Sprite):
    def __init__(self, y, *groups):
        super().__init__(*groups)
        self.photo = Image.open('evil.gif')
        self.num = 0
        self.i = 0
        try:
            while 1:
                self.photo.seek(self.num)
                self.num += 1
        except EOFError:
            pass
        self.photo.seek(self.i)
        self.photo.save('newe.png')
        self.image = pygame.transform.scale(pygame.image.load('newe.png'), (80, 55))
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = y
        self.g = 1
        self.mask = pygame.mask.from_surface(self.image)

    def peresec(self):
        for i in cat_group:
            return pygame.sprite.collide_mask(self, i)

    def update(self, n, *args):
        if self.g == self.num * 10:
            self.photo.seek(self.i)
            self.photo.save('newe.png')
            self.i += 1
            self.i %= self.num
            self.image = pygame.transform.scale(pygame.image.load('newe.png'), (80, 55))
            self.g = 0
        self.g += 1
        if n == 0:
            self.rect = self.rect.move(-2, 0)