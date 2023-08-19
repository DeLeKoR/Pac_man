from Setting import *
from Map import *
from Enemies import *
from Pac_man import *
from Basic_func import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.map = Map(self.screen)
        self.pac_man = Pac_man(get_cell_by_cord((13, 23), self.map.cells), self.screen, self.map.cells)
        self.enemies = pg.sprite.Group()
        self.create_enemies()

    def draw_frame(self):
        self.map.draw()
        #self.map.draw_cells()
        self.pac_man.draw()
        self.enemies.draw(self.screen)

    def create_frame(self):
        self.pac_man.move()

    def create_enemies(self):
        for image, cords in zip(images_ghosts, cords_ghosts):
            cell = get_cell_by_cord(cords, self.map.cells)
            ghost = Ghost(cell, self.map.cells, self.screen, image)
            self.enemies.add(ghost)

