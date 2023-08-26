from Setting import *

class Point(pg.sprite.Sprite):
    def __init__(self, screen, cord):
        super().__init__()
        self.screen = screen
        self.size = (10, 10)
        self.value = 10
        picture = pg.image.load('images/Point.png')
        self.image = pg.transform.scale(picture, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = cord

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))