from Setting import *
from Entity import Entity
from Basic_func import get_cell_by_cord
import random

class Ghost(Entity):
    def __init__(self, cell, cells, screen, image, color_type, start_point, retreat_cell, ghost_in_house, pac_man):
        super().__init__(screen, cell, cells)
        picture = pg.image.load(image)
        self.image = pg.transform.scale(picture, self.size)
        self.start_cords = cell.cord
        self.activity = act_ghosts # активность призрака
        self.ghost_in_house = ghost_in_house # равен True, если призрак в доме
        self.color_type = color_type
        self.start_point = start_point # начальная клетка
        self.retreat_cell = retreat_cell # целевая клетка отступления
        self.target = self.retreat_cell # целевая клетка призрака
        self.pac_man = pac_man
        self.start_move()

    def start_move(self):
        """Приводит призраков в движение"""
        if self.color_type == "red":
            self.move_future = (-SPEED, 0)
            self.move_now = (-SPEED, 0)
        self.activity = True
        self.move()

    def update(self):
        if self.activity and self.ghost_in_house:
            self.get_out()
        elif self.activity and not self.ghost_in_house:
            if self.check_future_cell():
                self.select_direction()
            else:
                self.change_direction()
        if self.activity:
            self.move()

    def get_out(self):
        "Заставляет призраков выйти из дома"
        dif_cords = (self.start_point[0] - self.cell.cord[0], self.start_point[1] - self.cell.cord[1]) # определяем направление

        if dif_cords[0] > 0 and self.cell.cord == self.start_cords:
            self.move_future = (SPEED, 0)

        elif dif_cords[0] < 0 and self.cell.cord == self.start_cords:
            self.move_future = (-SPEED, 0)
        
        elif dif_cords[0] == 0 and self.cell.cord == self.start_cords:
            self.move_future = (0, -SPEED)
            self.start_point = start_points[1]

        elif dif_cords[0] > 0 and self.cell.cord[0] + 1 == self.start_point[0]:
            self.move_future = (0, -SPEED)
            self.start_point = start_points[1]
        
        elif dif_cords[0] < 0 and self.cell.cord[0] - 1 == self.start_point[0]:
            self.move_future = (0, -SPEED)
            self.start_point = start_points[1]
        
        elif self.cell.cord[1] - 1 == self.start_point[1]:
            self.ghost_in_house = False
            random_move = random.choice((SPEED, -SPEED))
            self.move_future = (-random_move, 0)

    def change_direction(self):
        "Изменяет направление призрака, если впереди него стена"
        next_cell = self.get_next_cell()
        if not next_cell.type:
            side_cells_cord = self.get_side_cells() # получаем координаты клеток, расположенные по бокам от целевой
            cells = self.filter_cells(side_cells_cord) # получаем клеки, по которым призрак сможет идти  
            self.move_future = (cells[0].cord[0] - self.future_cell.cord[0], cells[0].cord[1] - self.future_cell.cord[1]) 

    def get_side_cells(self):
        """Находит координаты клеток, расположенные по бокам от передней клетки"""
        if self.move_now[1] > 0 or self.move_now[1] < 0:
            cell_1 = self.future_cell.cord[0] + 1, self.future_cell.cord[1]
            cell_2 = self.future_cell.cord[0] - 1, self.future_cell.cord[1] 
        elif self.move_now[0] > 0 or self.move_now[0] < 0:
            cell_1 = self.future_cell.cord[0], self.future_cell.cord[1] + 1
            cell_2 = self.future_cell.cord[0], self.future_cell.cord[1] - 1

        return [cell_1, cell_2]
    
    def filter_cells(self, list_cords):
        """Фильтует клетки, на которых стоит стена, и возращает список клеток по которым можно ходить"""
        list_cells = []
        for cord in list_cords:
            cell = get_cell_by_cord(cord, self.cells)
            if cell.type:
                list_cells.append(cell)
        return list_cells

    def select_direction(self):
        """Выбирает в какую сторону лабиринта пойти призраку"""
        next_cell = self.get_next_cell().cord
        side_cells = self.get_side_cells()
        list_cells = self.filter_cells([next_cell, *side_cells])
        cell = self.choose_cell(list_cells)
        self.move_future = (cell.cord[0] - self.future_cell.cord[0], cell.cord[1] - self.future_cell.cord[1])

    def count_distance(self, list_cells):
        """Находит расстояние от одной клетки (к которой призрак должен повернуть) до целевой"""
        list_distances = []
        for cell in list_cells:
            if cell.cord[0] == self.target[0]:
                d = abs(cell.cord[1] - self.target[1])
            elif cell.cord[1] == self.target[1]:
                d = abs(cell.cord[0] - self.target[0])
            else:
                x, y = cell.cord[0] - self.target[0], cell.cord[1] - self.target[1]
                d = (x ** 2 + y ** 2)**0.5
            list_distances.append(round(d, 2)) 
        return list_distances

    def choose_cell(self, list_cells):
        list_distances = self.count_distance(list_cells)
        min_distance = min(list_distances)
        index = list_distances.index(min_distance)
        return list_cells[index] 

    def get_next_cell(self):
        """Возращает клетку, рассположенную впереди от клетки, к которой призрак движется"""
        cords_next = (self.future_cell.cord[0] + self.move_future[0], self.future_cell.cord[1] + self.move_future[1])
        return get_cell_by_cord(cords_next, self.cells)

    def check_future_cell(self):
        """Проверяет является ли передняя клетка местом, где призраку нужно сделать выбор в какую сторону пойти"""
        cord = self.future_cell.cord
        if cord[1] in dir_select_cells.keys():
            if cord[0] in dir_select_cells[cord[1]]:
                return True
        return False