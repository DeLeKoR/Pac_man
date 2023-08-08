from Setting import *
from Map import *
from Enemy import *
from Pac_man import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.map = Map(self.screen)
        self.pac_man_move = (0, 0)
        self.pac_man = Pac_man(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2, self.screen)
        self.enemies = pg.sprite.Group()
        self.create_enemies()

    def draw_frame(self):
        self.map.draw()
        self.pac_man.draw()

    def create_frame(self):
        self.pac_man.move(*self.pac_man_move)

    def create_enemies(self):
        pass


