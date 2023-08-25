from Setting import *
from Map import *
from Enemy import *
from Pac_man import *
from Basic_func import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.map = Map(self.screen)
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells)
        self.enemies = pg.sprite.Group()
        self.create_enemies()

    def draw_frame(self):
        self.map.draw()
        #self.map.draw_cells()
        self.pac_man.draw_pac_man()

    def create_frame(self):
        self.pac_man.move()

    def create_enemies(self):
        pass


