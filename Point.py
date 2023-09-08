from Setting import *

class Point(pg.sprite.Sprite):
    def __init__(self, screen, cord, type:int = 1):
        super().__init__()
        self.screen = screen
        self.type = type
        self.size = (10, 10) if type == 1 else (20, 20)
        self.value = 10 if type == 1 else 50
        picture = pg.image.load('images/Point.png')
        self.image = pg.transform.scale(picture, self.size)
        self.rect = self.image.get_rect()
        self.rect.center = cord

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

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
