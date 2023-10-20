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
                cell = Cell((x, y), type, place_select, self.surface_map, self.get_adjacent_cells_cords((x, y), type))
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
                cell.draw_cell()

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
    def __init__(self, coord, type, place_select, surface_map, adjacent_cells_cords: list):
        super().__init__()
        self.surface_map = surface_map
        self.size = (PLAY_BOARD_SIZE[0] / len(MAP[0]), PLAY_BOARD_SIZE[1] / len(MAP))
        self.cord = coord
        self.real_cord = (self.cord[0] * self.size[0], self.cord[1] * self.size[1])
        self.rect = pg.Rect(self.cord[0] * self.size[0], self.cord[1] * self.size[1], self.size[0], self.size[1])
        self.type = type
        self.place_select = place_select # является ли клетка развилкой лабиринта
        self.adjacent_cells_cords = adjacent_cells_cords
        self.point = None
        self.meal = None
        self.result = []
        self.const_offset = 12
        self.offset = self.const_offset
        self.len_line_const = 8
        self.len_line = 0


    def draw_cell(self):
        self.__draw_left_line()
        self.__draw_right_line()
        self.__draw_top_line()
        self.__draw_bottom_line()

    def __draw_left_line(self):

        if self.adjacent_cells_cords[0] is not None and self.adjacent_cells_cords[0][1]:
            # отрисовка левой вертикальной линии
            if self.adjacent_cells_cords[0][1] == 5 and self.adjacent_cells_cords[4][1]:
                self.offset = 0
            # начало линии верх
            if self.__check_wall_edge(1, 2):
                self.len_line = self.len_line_const
                if self.adjacent_cells_cords[0][1] == 5 and not self.adjacent_cells_cords[4][1]:
                    self.len_line = 6
                if self.adjacent_cells_cords[2][1]:
                    self.len_line += self.offset
                else:
                    self.len_line -= self.offset
            self.result.append((self.rect.x + self.offset, self.rect.y + self.len_line))
            self.len_line = 0

            # конец линии низ
            if self.__check_wall_edge(7, 6):
                self.len_line = self.len_line_const
                if self.adjacent_cells_cords[0][1] == 5 and not self.adjacent_cells_cords[4][1]:
                    self.len_line = -6
                if self.adjacent_cells_cords[6][1]:
                    self.len_line += self.offset
                else:
                    self.len_line -= self.offset

            self.result.append((self.rect.x + self.offset, self.rect.y + self.rect.height - self.len_line))
            self.len_line = 0
            self.offset = self.const_offset
            self.__draw_line(self.result)

    def __draw_right_line(self):

        if self.adjacent_cells_cords[4] is not None and self.adjacent_cells_cords[4][1]:
            # отрисовка правой вертикальной линии
            if self.adjacent_cells_cords[4][1] == 5 and self.adjacent_cells_cords[0][1]:
                self.offset = 0
            # начало линии
            if (self.adjacent_cells_cords[3] is not None and self.adjacent_cells_cords[2][1]) or \
                    (not self.adjacent_cells_cords[3][1] and not self.adjacent_cells_cords[2][1]):
                self.len_line = self.len_line_const
                if self.adjacent_cells_cords[4][1] == 5 and not self.adjacent_cells_cords[0][1]:
                    self.len_line = 6
                if self.adjacent_cells_cords[2][1]:
                    self.len_line += self.offset
                else:
                    self.len_line -= self.offset
            self.result.append((self.rect.x + self.rect.width - self.offset, self.rect.y + self.len_line))
            self.len_line = 0

            # конец линии
            if (self.adjacent_cells_cords[6] is not None and self.adjacent_cells_cords[6][1]) or \
                    (self.adjacent_cells_cords[5] is not None and not self.adjacent_cells_cords[5][1] and not
                    self.adjacent_cells_cords[6][1]):
                self.len_line = self.len_line_const
                if self.adjacent_cells_cords[4][1] == 5 and not self.adjacent_cells_cords[0][1]:
                    self.len_line = -6
                if self.adjacent_cells_cords[6][1]:
                    self.len_line += self.offset
                else:
                    self.len_line -= self.offset
            self.result.append((self.rect.x + self.rect.width - self.offset, self.rect.y + self.rect.height - self.len_line))
            self.len_line = 0
            self.offset = self.const_offset
            self.__draw_line(self.result)

    def __draw_top_line(self):
        if self.adjacent_cells_cords[2] is not None and self.adjacent_cells_cords[2][1]:
            # отрисовка верхней горизонтальной линии
            if self.adjacent_cells_cords[2][1] == 5 and (
                    self.adjacent_cells_cords[6][1] or (self.adjacent_cells_cords[4] is None or self.adjacent_cells_cords[0] is None)):
                self.offset = 0
            # начало линии
            if (self.adjacent_cells_cords[0] is not None and self.adjacent_cells_cords[0][1]) or \
                    (self.adjacent_cells_cords[1] is not None and not self.adjacent_cells_cords[1][1] and not
                    self.adjacent_cells_cords[0][1]):
                self.len_line = self.len_line_const
                if self.adjacent_cells_cords[0][1]:
                    self.len_line += self.offset
                else:
                    self.len_line -= self.offset
            self.result.append((self.rect.x + self.len_line, self.rect.y + self.offset))
            self.len_line = 0
            # конец линии
            if (self.adjacent_cells_cords[4] is not None and self.adjacent_cells_cords[4][1]) or \
                    (self.adjacent_cells_cords[3] is not None and not self.adjacent_cells_cords[3][1] and not
                    self.adjacent_cells_cords[4][1]):
                self.len_line = self.len_line_const
                if self.adjacent_cells_cords[4][1]:
                    self.len_line += self.offset
                else:
                    self.len_line -= self.offset

            self.result.append((self.rect.x + self.rect.width - self.len_line, self.rect.y + self.offset))
            self.len_line = 0
            self.offset = self.const_offset
            self.__draw_line(self.result)

    def __draw_bottom_line(self):

        if self.adjacent_cells_cords[6] is not None and self.adjacent_cells_cords[6][1]:
            # отрисовка нижней горизонтальной линии
            if self.adjacent_cells_cords[6][1] == 5 and (
                    self.adjacent_cells_cords[2][1] or (self.adjacent_cells_cords[4] is None or self.adjacent_cells_cords[0] is None)):
                self.offset = 0
            # начало линии
            if (self.adjacent_cells_cords[0] is not None and self.adjacent_cells_cords[0][1]) or \
                    (self.adjacent_cells_cords[7] is not None and not self.adjacent_cells_cords[7][1] and not
                    self.adjacent_cells_cords[0][1]):
                self.len_line = self.len_line_const
                if self.adjacent_cells_cords[0][1] == 5:
                    self.len_line += self.const_offset
                elif self.adjacent_cells_cords[0][1]:
                    self.len_line += self.offset
                else:
                    self.len_line -= self.offset
            self.result.append((self.rect.x + self.len_line, self.rect.y + self.rect.height - self.offset))
            self.len_line = 0

            # конец линии
            if (self.adjacent_cells_cords[4] is not None and self.adjacent_cells_cords[4][1]) or \
                    (self.adjacent_cells_cords[5] is not None and not self.adjacent_cells_cords[5][1] and not
                    self.adjacent_cells_cords[4][1]):
                self.len_line = self.len_line_const
                if self.adjacent_cells_cords[4][1] == 5:
                    self.len_line += self.const_offset
                elif self.adjacent_cells_cords[4][1]:
                    self.len_line += self.offset
                else:
                    self.len_line -= self.offset

            self.result.append((self.rect.x + self.rect.width - self.len_line, self.rect.y + self.rect.height - self.offset))
            self.len_line = 0
            self.offset = self.const_offset
            self.__draw_line(self.result)

    def __draw_line(self, cords):
        pg.draw.line(self.surface_map, (10, 10, 200), *cords, 3)
        cords.clear()


    def __check_wall_edge(self, index_1, index_2):
        if self.adjacent_cells_cords[index_1] is not None and self.adjacent_cells_cords[index_2] is not None:
            if (self.adjacent_cells_cords[index_2][1]) or \
                    (not self.adjacent_cells_cords[index_1][1] and not self.adjacent_cells_cords[index_2][1]):
                return True
        return False




