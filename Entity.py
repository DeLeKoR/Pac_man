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
        # все клетки
        self.cells = cells
        # координаты (по умолчанию совмещают центр объекта с центром клетки)
        #self.x = cell.real_cord[0]-(self.size[0]/2-cell.cell_size[0]/2)-1
        #self.y = cell.real_cord[1]-(self.size[1]/2-cell.cell_size[1]/2)
        self.rect = pg.Rect(0, 0, *self.size)
        self.rect.center = self.cell.rect.center
        self.x = self.rect.x
        self.y = self.rect.y
       

    def move(self):
        if self.move_now[0] > 0:
            cell = get_cell_by_cord((self.cell.cord[0]+1, self.cell.cord[1]), self.cells)
            if cell.type:
                self.x += self.move_now[0]
        elif self.move_now[0] < 0:
            cell = get_cell_by_cord((self.cell.cord[0]-1, self.cell.cord[1]), self.cells)
            if cell.type:
                self.x += self.move_now[0]
        elif self.move_now[1] > 0:
            cell = get_cell_by_cord((self.cell.cord[0], self.cell.cord[1]+1), self.cells)
            if cell.type:
                self.y += self.move_now[1]
        elif self.move_now[1] < 0:
            cell = get_cell_by_cord((self.cell.cord[0], self.cell.cord[1]-1), self.cells)
            if cell.type:
                self.y += self.move_now[1]
        self.rect.x, self.rect.y = self.x, self.y

        if self.rect.center == get_cell(self.rect.center, self.cells).rect.center:
            self.update_cell(get_cell(self.rect.center, self.cells))
            if any([(self.move_now[0] and self.move_future[0]),
                    (self.move_now[1] and self.move_future[1])]):
                self.move_now = self.move_future
            elif self.move_future[1] > 0:
                cell = get_cell_by_cord((self.cell.cord[0], self.cell.cord[1]+1), self.cells)
                if cell.type:
                    self.move_now = self.move_future
            elif self.move_future[1] < 0:
                cell = get_cell_by_cord((self.cell.cord[0], self.cell.cord[1]-1), self.cells)
                if cell.type:
                    self.move_now = self.move_future
            elif self.move_future[0] > 0:
                cell = get_cell_by_cord((self.cell.cord[0]+1, self.cell.cord[1]), self.cells)
                if cell.type:
                    self.move_now = self.move_future
            elif self.move_future[0] < 0:
                cell = get_cell_by_cord((self.cell.cord[0]-1, self.cell.cord[1]), self.cells)
                if cell.type:
                    self.move_now = self.move_future

    def update_cell(self, cell):
        self.cell = cell
        if self.move_now[0]:
            self.y = cell.real_cord[1] - (self.size[1] / 2 - cell.cell_size[1] / 2)
        if self.move_now[1]:
            self.x = cell.real_cord[0] - (self.size[0] / 2 - cell.cell_size[0] / 2)-1