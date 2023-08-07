from Setting import *

class Pac_man:
    def __init__(self,x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        picture = pg.image.load(PAC_MAN_IMG_PASS)
        self.pac_man = pg.transform.scale(picture, PAC_MAN_SIZE)
        self.rect = self.pac_man.get_rect()

    def move(self, x:int = 0, y:int = 0):
        if (self.x > 0 or x > 0) and (self.x < SCREEN_SIZE[0]-PAC_MAN_SIZE[0] or x < 0):
            self.x += x
            self.rect.x += x
        if (self.y > 0 or y > 0) and (self.y < SCREEN_SIZE[1] - PAC_MAN_SIZE[1] or y < 0):
            self.y += y
            self.rect.y += y

    def draw(self):
        self.screen.blit(self.pac_man, (self.x, self.y))

