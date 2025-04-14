from Setting import *

class Point(pg.sprite.Sprite):
    def __init__(self, screen, cord, type:int = 1):
        super().__init__()
        self.screen = screen
        self.type = type
        self.size = (5, 5) if type == 1 else (10, 10)
        self.value = 10 if type == 1 else 50
        self.rect = pg.Rect((0, 0), self.size)
        self.rect.center = cord

    def draw(self):
        if self.type == 1:
            pg.draw.rect(self.screen, (240, 240, 10), (*self.rect.topleft, *self.size))
        else:
            pg.draw.circle(self.screen, (240, 240, 10), self.rect.center, self.size[0])

class Meal(pg.sprite.Sprite):
    def __init__(self, screen, value, cord, type:int = 1):
        super().__init__()
        self.screen = screen
        self.size = (40, 40)
        self.value = value
        picture = pg.image.load(f'images/meal_{type}.png')
        self.image = pg.transform.scale(picture, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = cord

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
