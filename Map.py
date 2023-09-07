from Setting import *
from Basic_func import *
from Point import *


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.cells = pg.sprite.Group()
        self.points = pg.sprite.Group()
        self.meal = pg.sprite.Group()
        self.create_cells()
        self.create_points()
        picture = pg.image.load(MAP_IMG_PASS)
        self.image_map = pg.transform.scale(picture, PLAY_BOARD_SIZE)
        self.score = 0

    def draw_map(self):
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

    def draw_points(self):
        for point in self.points:
            point.draw()

    def create_points(self):
        for y in range(len(MAP)):
            for x, type in enumerate(MAP[y]):
                if type == 1:
                    cell = get_cell_by_cord((x, y), self.cells)
                    point = Point(self.screen, cell.rect.center, 1)
                    cell.point = point
                    self.points.add(point)
                elif type == 3:
                    cell = get_cell_by_cord((x, y), self.cells)
                    point = Point(self.screen, cell.rect.center, 3)
                    cell.point = point
                    self.points.add(point)

    def update_meal(self):
        if self.score and self.score < 1800:
            self.draw_meal()
            self.score += 1
        elif self.score == 1800:
            self.score = 0
            for meal in self.meal:
                meal.kill()


    def create_meal(self):
        if (len(self.points) == 176 or len(self.points) == 76) and len(self.meal) < 1:
            self.score = 1
            cell = get_cell_by_cord((14, 17), self.cells)
            type = 1 if len(self.points) == 176 else 2
            meal = Meal(self.screen, 100, cell.rect.center, type)
            self.meal.add(meal)
            cell.meal = meal


    def draw_meal(self):
        if len(self.meal) >= 1:
            for meal in self.meal:
                meal.draw()



class Cell(pg.sprite.Sprite):
    def __init__(self, coord, type):
        super().__init__()
        self.cell_size = (int(PLAY_BOARD_SIZE[0]/27), int(PLAY_BOARD_SIZE[1]/30))
        self.cord = coord
        self.real_cord = (self.cord[0] * self.cell_size[0], self.cord[1] * self.cell_size[1])
        self.rect = pg.Rect(self.cord[0] * self.cell_size[0], self.cord[1] * self.cell_size[1], self.cell_size[0], self.cell_size[1])
        self.type = type
        self.point = None
        self.meal = None

