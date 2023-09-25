from Setting import *
from Basic_func import *
from Point import *


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.surface_map = pg.Surface(PLAY_BOARD_SIZE)
        self.surface_map_rect = self.surface_map.get_rect()
        self.cells = pg.sprite.Group()
        self.points = pg.sprite.Group()
        self.meal = pg.sprite.Group()
        self.numbers = pg.sprite.Group()
        self.create_cells()
        self.create_points()
        picture = pg.image.load(MAP_IMG_PASS)
        self.image_map = pg.transform.scale(picture, PLAY_BOARD_SIZE)
        self.score = 0

    def draw_map(self):
        self.surface_map.fill((10, 10, 10))
        self.draw_cells()
        self.draw_points()
        self.update_meal()
        for num in self.numbers:
            if num.alfa <= 0:
                num.kill()
                continue
            num.draw(self.surface_map)
        self.screen.blit(self.surface_map, self.surface_map_rect)


    def create_cells(self):
        for y in range(len(MAP)):
            for x, type in enumerate(MAP[y]):
                place_select = check_cell((x, y)) # является ли клетка развилкой лабиринта
                cell = Cell((x, y), type, place_select, self.get_adjacent_cells_cords((x, y), type))
                self.cells.add(cell)

    def get_adjacent_cells_cords(self, start_cord, type):
        adjacent_cells_cords = []
        data_set = [[-1, 0],
                    [-1, -1],
                    [0, -1],
                    [1, -1],
                    [1, 0],
                    [1, 1],
                    [0, 1],
                    [-1, 1]]
        for set in data_set:
            cord = (start_cord[0] + set[0], start_cord[1] + set[1])
            if check_number_in_gap(cord[0], (0, 28)) and check_number_in_gap(cord[1], (0, 31)):
                adjacent_cells_cords.append([cord, MAP[cord[1]][cord[0]]])
            else:
                adjacent_cells_cords.append(None)
        return adjacent_cells_cords


    def draw_cells(self):
        for cell in self.cells:
            if not cell.type:
                result = []
                offset = 8
                len_line_const = 10
                offset_len_line = 6
                len_line = 0
                if (cell.adjacent_cells_cords[0] is not None and cell.adjacent_cells_cords[0][1]):
                    if (cell.adjacent_cells_cords[1] is not None and cell.adjacent_cells_cords[2][1]) or \
                            (cell.adjacent_cells_cords[1] is not None and not cell.adjacent_cells_cords[1][1] and not cell.adjacent_cells_cords[2][1]):
                        len_line = len_line_const
                        if cell.adjacent_cells_cords[6] is not None and not cell.adjacent_cells_cords[6][1] and cell.adjacent_cells_cords[2][1]:
                            len_line += offset_len_line
                        else:
                            len_line -= offset_len_line
                    result.append((cell.rect.x + offset, cell.rect.y + len_line))
                    len_line = 0
                    if (cell.adjacent_cells_cords[6] is not None and cell.adjacent_cells_cords[6][1]) or \
                        (cell.adjacent_cells_cords[7] is not None and not cell.adjacent_cells_cords[7][1] and not cell.adjacent_cells_cords[6][1]):
                        len_line = len_line_const
                        if cell.adjacent_cells_cords[2] is not None and not cell.adjacent_cells_cords[2][1] and cell.adjacent_cells_cords[6][1]:
                            len_line += offset_len_line
                        else:
                            len_line -= offset_len_line
                    result.append((cell.rect.x + offset, cell.rect.y + cell.rect.height - len_line))
                    self.__draw_line(result)
                    len_line = 0
                if (cell.adjacent_cells_cords[4] is not None and cell.adjacent_cells_cords[4][1]):
                    if (cell.adjacent_cells_cords[3] is not None and cell.adjacent_cells_cords[2][1]) or \
                            (not cell.adjacent_cells_cords[3][1] and not cell.adjacent_cells_cords[2][1]):
                        len_line = len_line_const
                        if cell.adjacent_cells_cords[6] is not None and not cell.adjacent_cells_cords[6][1] and cell.adjacent_cells_cords[2][1]:
                            len_line += offset_len_line
                        else:
                            len_line -= offset_len_line
                    result.append((cell.rect.x + cell.rect.width - offset, cell.rect.y + len_line))
                    len_line = 0
                    if (cell.adjacent_cells_cords[6] is not None and cell.adjacent_cells_cords[6][1]) or \
                        (cell.adjacent_cells_cords[5] is not None and not cell.adjacent_cells_cords[5][1] and not cell.adjacent_cells_cords[6][1]):
                        len_line = len_line_const
                        if cell.adjacent_cells_cords[2] is not None and not cell.adjacent_cells_cords[2][1] and cell.adjacent_cells_cords[6][1]:
                            len_line += offset_len_line
                        else:
                            len_line -= offset_len_line
                    result.append((cell.rect.x + cell.rect.width - offset, cell.rect.y + cell.rect.height - len_line))
                    len_line = 0
                    self.__draw_line(result)
                if (cell.adjacent_cells_cords[2] is not None and cell.adjacent_cells_cords[2][1]):
                    if (cell.adjacent_cells_cords[1] is not None and cell.adjacent_cells_cords[0][1]) or \
                            (cell.adjacent_cells_cords[1] is not None and not cell.adjacent_cells_cords[1][1] and not cell.adjacent_cells_cords[0][1]):
                        len_line = len_line_const
                        if (cell.adjacent_cells_cords[4] is not None and not cell.adjacent_cells_cords[4][1] and cell.adjacent_cells_cords[0][1]):
                            len_line += offset_len_line
                        else:
                            len_line -= offset_len_line
                    result.append((cell.rect.x + len_line, cell.rect.y + offset))
                    len_line = 0
                    if (cell.adjacent_cells_cords[4] is not None and cell.adjacent_cells_cords[4][1]) or \
                        (cell.adjacent_cells_cords[3] is not None and not cell.adjacent_cells_cords[3][1] and not cell.adjacent_cells_cords[4][1]):
                        len_line = len_line_const
                        if (cell.adjacent_cells_cords[0] is not None and not cell.adjacent_cells_cords[0][1] and cell.adjacent_cells_cords[4][1]):
                            len_line += offset_len_line
                        else:
                            len_line -= offset_len_line
                    result.append((cell.rect.x + cell.rect.width - len_line, cell.rect.y + offset))
                    len_line = 0
                    self.__draw_line(result)
                if (cell.adjacent_cells_cords[6] is not None and cell.adjacent_cells_cords[6][1]):
                    if (cell.adjacent_cells_cords[7] is not None and cell.adjacent_cells_cords[0][1]) or \
                            (cell.adjacent_cells_cords[7] is not None and not cell.adjacent_cells_cords[7][1] and not cell.adjacent_cells_cords[0][1]):
                        len_line = len_line_const
                        if (cell.adjacent_cells_cords[4] is not None and not cell.adjacent_cells_cords[4][1] and cell.adjacent_cells_cords[0][1]):
                            len_line += offset_len_line
                        else:
                            len_line -= offset_len_line
                    result.append((cell.rect.x + len_line, cell.rect.y + cell.rect.height - offset))
                    len_line = 0
                    if (cell.adjacent_cells_cords[4] is not None and cell.adjacent_cells_cords[4][1]) or \
                        (cell.adjacent_cells_cords[5] is not None and not cell.adjacent_cells_cords[5][1] and not cell.adjacent_cells_cords[4][1]):
                        len_line = len_line_const
                        if (cell.adjacent_cells_cords[0] is not None and not cell.adjacent_cells_cords[0][1] and cell.adjacent_cells_cords[4][1]):
                            len_line += offset_len_line
                        else:
                            len_line -= offset_len_line
                    result.append((cell.rect.x + cell.rect.width - len_line, cell.rect.y + cell.rect.height - offset))
                    self.__draw_line(result)

    def __draw_line(self, cords):
        pg.draw.line(self.surface_map, (10, 10, 200), *cords, 3)
        cords.clear()


    def draw_points(self):
        for point in self.points:
            point.draw()

    def create_points(self):
        for y in range(len(MAP)):
            for x, type in enumerate(MAP[y]):
                if type == 1:
                    cell = get_cell_by_cord((x, y), self.cells)
                    point = Point(self.surface_map, cell.rect.center, 1)
                    cell.point = point
                    self.points.add(point)
                elif type == 3:
                    cell = get_cell_by_cord((x, y), self.cells)
                    point = Point(self.surface_map, cell.rect.center, 3)
                    cell.point = point
                    self.points.add(point)

    def update_meal(self):
        if self.score and self.score < 600:
            self.draw_meal()
            self.score += 1
        elif self.score == 600:
            self.score = 0
            for meal in self.meal:
                meal.kill()


    def create_meal(self):
        if (len(self.points) == 176 or len(self.points) == 76) and len(self.meal) < 1:
            self.score = 1
            cell = get_cell_by_cord((14, 17), self.cells)
            type = 1 if len(self.points) == 176 else 2
            meal = Meal(self.surface_map, 100, cell.rect.center, type)
            self.meal.add(meal)
            cell.meal = meal


    def draw_meal(self):
        if len(self.meal) >= 1:
            for meal in self.meal:
                meal.draw()

    def check_points(self):
        return False if len(self.points) else True



class Cell(pg.sprite.Sprite):
    def __init__(self, coord, type, place_select, adjacent_cells_cords: list):
        super().__init__()
        self.cell_size = (PLAY_BOARD_SIZE[0]/len(MAP[0]), PLAY_BOARD_SIZE[1]/len(MAP))
        self.cord = coord
        self.real_cord = (self.cord[0] * self.cell_size[0], self.cord[1] * self.cell_size[1])
        self.rect = pg.Rect(self.cord[0] * self.cell_size[0], self.cord[1] * self.cell_size[1], self.cell_size[0], self.cell_size[1])
        self.type = type
        self.place_select = place_select # является ли клетка развилкой лабиринта
        self.adjacent_cells_cords = adjacent_cells_cords
        self.point = None
        self.meal = None



