from Setting import *
from Basic_func import *

class Pac_man:
    def __init__(self, cell, screen, cells):
        self.size = (40, 40)
        self.move_now = (0, 0)
        self.move_future = (0, 0)
        self.cell = cell
        self.x = cell.real_cord[0]-(self.size[0]/2-cell.cell_size[0]/2)-1
        self.y = cell.real_cord[1]-(self.size[1]/2-cell.cell_size[1]/2)-1
        self.all_cells = cells
        picture = pg.image.load(PAC_MAN_IMG_PASS)
        self.pac_man = pg.transform.scale(picture, self.size)
        self.screen = screen
        self.rect = None
        self.create()

    def create(self):
        self.rect = self.pac_man.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y



    def draw(self):
        self.screen.blit(self.pac_man, (self.x, self.y))


    def update_cell(self, cell):
        self.cell = cell
        if self.move_now[0]:
            self.y = cell.real_cord[1]-(self.size[1]/2-cell.cell_size[1]/2)-1
        if self.move_now[1]:
            self.x = cell.real_cord[0]-(self.size[0]/2-cell.cell_size[0]/2)-1

