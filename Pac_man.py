from Setting import *
from Basic_func import *
from Entity import *

class Pac_man(Entity):
    def __init__(self, cell, screen, cells):
        super().__init__(screen, cell, cells)
        picture = pg.image.load(PAC_MAN_IMG_PASS)
        self.pac_man = pg.transform.scale(picture, self.size)



    def draw(self):
        self.screen.blit(self.pac_man, (self.x, self.y))

