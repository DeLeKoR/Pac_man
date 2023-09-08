from Setting import *
from Basic_func import *

class Entity(pg.sprite.Sprite):
    def __init__(self, screen, cell, cells):
        pg.sprite.Sprite.__init__(self)
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
        if len(self.textures) >= 2:
            self.textures.pop(1)
        cell = get_cell(self.rect.center, self.cells)
        if cell is not None:
            if ((cell.rect.centerx - SPEED/2 <= self.rect.centerx <= cell.rect.centerx + SPEED/2)
                    and (cell.rect.centery - SPEED/2 <= self.rect.centery <= cell.rect.centery + SPEED/2)):
                self.cell = cell
                self.rect.center = self.cell.rect.center
                self.x, self.y = self.rect.x, self.rect.y
                future_cell = get_cell_by_cord((self.cell.cord[0] + sing_number(self.move_future[0]), self.cell.cord[1] + sing_number(self.move_future[1])), self.cells)
                if future_cell is not None and future_cell.type:
                    self.move_now = self.move_future
                if self.move_now == self.move_future:
                    self.future_cell = future_cell
                self.next_cell = get_cell_by_cord((self.cell.cord[0] + sing_number(self.move_now[0]), self.cell.cord[1] + sing_number(self.move_now[1])), self.cells)
        if self.next_cell is None or self.future_cell is None:
            if len(self.textures) > 0:
                self.textures.append(self.textures[0])
            self.x += self.move_now[0]
            self.rect.x = self.x
            if int(-self.cell.cell_size[0]/2)-SPEED/2 <=self.rect.center[0] <= int(-self.cell.cell_size[0]/2)+SPEED/2 or (int(self.cell.cell_size[0]/2) + PLAY_BOARD_SIZE[0])-SPEED/2 <= self.rect.center[0] <= (int(self.cell.cell_size[0]/2) + PLAY_BOARD_SIZE[0])+SPEED/2:
                if self.rect.center[0] < 0:
                    self.rect.center = get_cell_by_cord((self.cell.cord[0]+27, self.cell.cord[1]), self.cells).rect.center
                else:
                    self.rect.center = get_cell_by_cord((self.cell.cord[0] - 27, self.cell.cord[1]),self.cells).rect.center
                self.x = self.rect.x
                self.textures.pop(1)
        if self.future_cell is not None and self.next_cell is not None and self.future_cell.type and self.next_cell.type:
            self.x += self.move_now[0]
            self.y += self.move_now[1]
            self.rect.x, self.rect.y = self.x, self.y


    def draw(self, object):
        if len(self.textures) == 0:
            self.textures.append(object)
        if len(self.textures) == 1:
            self.screen.blit(object, (self.x, self.y))
        elif len(self.textures) == 2:
            self.screen.blit(object, (self.x, self.y))
            if self.x < 0:
                self.screen.blit(object, (self.x+PLAY_BOARD_SIZE[0], self.y))
            else:
                self.screen.blit(object, (self.x-PLAY_BOARD_SIZE[0], self.y))


