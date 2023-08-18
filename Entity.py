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
        self.future_cell = None
        # все клетки
        self.cells = cells
        # координаты (по умолчанию совмещают центр объекта с центром клетки)
        self.rect = pg.Rect(0, 0, *self.size)
        self.rect.center = self.cell.rect.center
        self.x = self.rect.x
        self.y = self.rect.y

    def move(self):
        try:
            if self.rect.center == get_cell(self.rect.center, self.cells).rect.center:
                self.update_cell(get_cell(self.rect.center, self.cells))
                if self.move_future[1] > 0:
                    cell = get_cell_by_cord((self.cell.cord[0], self.cell.cord[1]+1), self.cells)
                    if self.move_now == self.move_future:
                        self.future_cell = cell
                    if cell.type:
                        self.move_now = self.move_future
                elif self.move_future[1] < 0:
                    cell = get_cell_by_cord((self.cell.cord[0], self.cell.cord[1]-1), self.cells)
                    if self.move_now == self.move_future:
                        self.future_cell = cell
                    if cell.type:
                        self.move_now = self.move_future
                elif self.move_future[0] > 0:
                    cell = get_cell_by_cord((self.cell.cord[0]+1, self.cell.cord[1]), self.cells)
                    if self.move_now == self.move_future:
                        self.future_cell = cell
                    if cell.type:
                        self.move_now = self.move_future
                elif self.move_future[0] < 0:
                    cell = get_cell_by_cord((self.cell.cord[0]-1, self.cell.cord[1]), self.cells)
                    if self.move_now == self.move_future:
                        self.future_cell = cell
                    if cell.type:
                        self.move_now = self.move_future
            if self.future_cell is not None and self.future_cell.type:
                self.x += self.move_now[0]
                self.y += self.move_now[1]
                self.rect.x, self.rect.y = self.x, self.y
        except AttributeError:
            pass

    def update_cell(self, cell):
        self.cell = cell
        self.rect.center = self.cell.rect.center
        self.x = self.rect.x
        self.y = self.rect.y