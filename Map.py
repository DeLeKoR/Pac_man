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


    def draw_cells(self):
        for cell in self.cells:
            color = (0, 200, 0) if cell.type else (200, 0, 0)
            pg.draw.rect(self.screen, color, cell)




class Cell(pg.sprite.Sprite):
    def __init__(self, coord, type):
        super().__init__()
        self.cell_size = (int(PLAY_BOARD_SIZE[0]/27), int(PLAY_BOARD_SIZE[1]/30))
        self.cord = coord
        self.real_cord = (self.cord[0] * self.cell_size[0], self.cord[1] * self.cell_size[1])
        self.rect = pg.Rect(self.cord[0] * self.cell_size[0], self.cord[1] * self.cell_size[1], self.cell_size[0], self.cell_size[1])
        self.type = type
