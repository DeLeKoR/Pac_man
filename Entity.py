from Setting import *
from Basic_func import *

class Entity:
    def __init__(self, screen, cell, cells):
        self.size = (40, 40)
        self.screen = screen
        # направление движения
        self.move_now = (0, 1)
        self.move_future = (0, 0)
        # клетка на которой расположен объект
        self.cell = cell
        self.next_cell = None
        self.future_cell = None
        # все клетки
        self.cells = cells
        # координаты (по умолчанию совмещают центр объекта с центром клетки)
        self.rect = pg.Rect(0, 0, *self.size)
        self.rect.center = self.cell.rect.center
        self.x = self.rect.x
        self.y = self.rect.y
        self.textures = []

    def move(self):
        try:
            if len(self.textures) >= 2:
                self.textures.pop(1)
            cell = get_cell(self.rect.center, self.cells)
            if self.rect.center == cell.rect.center:
                self.cell = cell
                cell = get_cell_by_cord((self.cell.cord[0] + self.move_future[0], self.cell.cord[1] + self.move_future[1]), self.cells)
                if cell.type:
                    self.move_now = self.move_future
                if self.move_now == self.move_future:
                    self.future_cell = cell
                self.next_cell = get_cell_by_cord((self.cell.cord[0] + self.move_now[0], self.cell.cord[1] + self.move_now[1]), self.cells)
            if self.future_cell is not None and self.next_cell is not None and self.future_cell.type and self.next_cell.type:
                self.x += self.move_now[0]
                self.y += self.move_now[1]
                self.rect.x, self.rect.y = self.x, self.y
        except AttributeError:
            if len(self.textures) < 2:
                self.textures.append(self.textures[0])
            self.x += self.move_now[0]
            if int(self.x + self.size[0] + self.cell.cell_size[0]/2) == int(-self.cell.cell_size[0]/2):
                self.cell = get_cell_by_cord((self.cell.cord[0]+26, self.cell.cord[1]), self.cells)
                self.rect.center = self.cell.rect.center
                self.x = self.rect.x
                self.textures.pop(1)


    def draw(self, object):
        if len(self.textures) == 0:
            self.textures.append(object)
        if len(self.textures) == 1:
            self.screen.blit(object, (self.x, self.y))
        elif len(self.textures) == 2:
            self.screen.blit(object, (self.x, self.y))
            self.screen.blit(object, (self.x+PLAY_BOARD_SIZE[0], self.y))

