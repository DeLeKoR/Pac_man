from Setting import *
from Basic_func import *

class Map:
    def __init__(self, screen):
        self.screen = screen
        self.cells = pg.sprite.Group()
        self.create_cells()
        picture = pg.image.load(MAP_IMG_PASS)
        self.image_map = pg.transform.scale(picture, PLAY_BOARD_SIZE)

    def draw(self):
        self.screen.blit(self.image_map, (0, 0))

    def create_cells(self):
        for y in range(len(MAP)):
            for x, type in enumerate(MAP[y]):
                cell = Cell((x, y), type)
                self.cells.add(cell)

    def move(self, peace, x: int = 0, y: int = 0):
        if x > 0:
            cell = get_cell_by_cord((peace.cell.cord[0]+1, peace.cell.cord[1]), self.cells)
            if cell.type:
                peace.x += x
        if x < 0:
            cell = get_cell_by_cord((peace.cell.cord[0]-1, peace.cell.cord[1]), self.cells)
            if cell.type:
                peace.x += x
        if y > 0:
            cell = get_cell_by_cord((peace.cell.cord[0], peace.cell.cord[1]+1), self.cells)
            if cell.type:
                peace.y += y
        if y < 0:
            cell = get_cell_by_cord((peace.cell.cord[0], peace.cell.cord[1]-1), self.cells)
            if cell.type:
                peace.y += y
        peace.rect.x, peace.rect.y = peace.x, peace.y
        if peace.rect.center == get_cell(peace.rect.center, self.cells).rect.center:
            peace.update_cell(get_cell(peace.rect.center, self.cells))
            peace.move_now = peace.move_future

    def draw_cells(self):
        for cell in self.cells:
            color = (0, 200, 0) if cell.type else (200, 0, 0)
            pg.draw.rect(self.screen, color, cell)




class Cell(pg.sprite.Sprite):
    def __init__(self, coord, type):
        super().__init__()
        self.cell_size = (int(PLAY_BOARD_SIZE[0]/28), int(PLAY_BOARD_SIZE[1]/31))
        self.cord = coord
        self.real_cord = (self.cord[0] * self.cell_size[0], self.cord[1] * self.cell_size[1])
        self.rect = pg.Rect(self.cord[0] * self.cell_size[0], self.cord[1] * self.cell_size[1], self.cell_size[0], self.cell_size[1])
        self.type = type
