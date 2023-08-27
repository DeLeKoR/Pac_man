from Setting import *
from Basic_func import *
from Entity import *

class Pac_man(Entity):
    def __init__(self, cell, screen, cells):
        super().__init__(screen, cell, cells)
        picture = pg.image.load(PAC_MAN_IMG_PASS)
        self.pac_man = pg.transform.scale(picture, self.size)



    def draw_pac_man(self):
        self.draw(self.pac_man)

    def eat_point(self, score):
        cell = get_cell(self.rect.center, self.cells)
        if cell is not None and cell.rect.center == self.rect.center and cell.point is not None:
            cell.point.kill()
            score[0] += cell.point.value
            cell.point = None
        if cell is not None and cell.rect.center == self.rect.center and cell.meal is not None:
            cell.meal.kill()
            score[0] += cell.meal.value
            cell.meal = None