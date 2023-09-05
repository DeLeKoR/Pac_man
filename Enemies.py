from Setting import *
from Entity import Entity
from Basic_func import get_cell_by_cord
import random

class Ghost(Entity):
    def __init__(self, cell, cells, screen, image, color_type, retreat_cell, ghost_in_house, pac_man):
        super().__init__(screen, cell, cells)
        picture_ghost = pg.image.load(image)
        picture_scared_ghost = pg.image.load(scared_ghost)
        self.base_image = pg.transform.scale(picture_ghost, self.size) # основное изображение у призрака
        self.scared_image = pg.transform.scale(picture_scared_ghost, (50, 40)) # изображение призрака, когда он испуган 
        self.image = self.base_image
        self.start_cords = cell.cord
        self.ghost_in_house = ghost_in_house # равен True, если призрак в доме
        self.color_type = color_type
        self.retreat_cell = retreat_cell # целевая клетка отступления
        self.target = None # целевая клетка призрака
        self.pac_man = pac_man
        self.mode_now = "run"
        self.mode_first = "attack"
        self.times_modes = [7, 20, 7, 20, 5, 20, 5, 40]
        self.index_mode = 0
        self.start_move()

    def start_move(self):
        """Приводит призраков в движение"""
        if self.color_type == "red":
            self.move_future = (-SPEED, 0)
            self.move_now = (-SPEED, 0)
            self.target = self.retreat_cell
            self.ghost_in_house = False
        else:
            self.target = start_points[0]
        self.activity = True 
        self.start_time = pg.time.get_ticks()
        self.move()

    def draw_enemy(self):
        self.draw(self.image)

    def update(self):
        self.check_time()
        if self.mode_now == "attack":
            self.target = self.pac_man.cell.cord
        if not self.ghost_in_house:
            if self.check_future_cell():
                self.select_direction()
            else:
                self.change_direction()
        elif self.ghost_in_house:
            self.get_out()
        self.move()

    # ИЗМЕНЕНИЕ РЕЖИМОВ У ПРИЗРАКОВ

    def check_time(self):
        """Проверка времени действия текущего режима"""
        current_time = pg.time.get_ticks()
        different = (current_time - self.start_time) / 1000
        if self.mode_now != "scare":
            time_mode = self.times_modes[self.index_mode]
            if different >= time_mode:
                if time_mode != self.times_modes[-1]:
                    self.index_mode += 1
                elif time_mode == self.times_modes[-1]:
                    self.index_mode = 0
                self.change_mode()
        else:
            if different >= 10:
                self.change_mode()

    def change_mode(self):
        """Изменяет режим у призрака"""
        self.mode_now, self.mode_first = self.mode_first, self.mode_now 
        if self.mode_first == "scare":
            self.image = self.base_image
            if self.mode_now == "run":
                self.mode_first = "attack"
            else:
                self.mode_first = "run"
        if self.mode_now == "run":
            self.target = self.retreat_cell
            
        self.move_future = self.move_now[0] * (-1), self.move_now[1] * (-1)     
        self.start_time = pg.time.get_ticks()
    
    def scare_mode(self):
        """Режим испуга призрака"""
        self.image = self.scared_image
        self.mode_first = self.mode_now
        self.mode_now = "scare"
        self.start_time = pg.time.get_ticks()

    # ВЫВОД ПРИЗРАКОВ ИЗ ИХ ДОМА

    def get_out(self):
        "Заставляет призраков выйти из дома"
        dif_cords = (self.target[0] - self.cell.cord[0], self.target[1] - self.cell.cord[1]) # определяем направление

        if dif_cords[0] > 0 and self.cell.cord == self.start_cords:
            self.move_future = (SPEED, 0)

        elif dif_cords[0] < 0 and self.cell.cord == self.start_cords:
            self.move_future = (-SPEED, 0)
        
        elif dif_cords[0] == 0 and self.cell.cord == self.start_cords:
            self.move_future = (0, -SPEED)
            self.target = start_points[1]

        elif dif_cords[0] > 0 and self.cell.cord[0] + 1 == self.target[0]:
            self.move_future = (0, -SPEED)
            self.target = start_points[1]
        
        elif dif_cords[0] < 0 and self.cell.cord[0] - 1 == self.target[0]:
            self.move_future = (0, -SPEED)
            self.target = start_points[1]
        
        elif self.cell.cord[1] - 1 == self.target[1]:
            self.ghost_in_house = False
            self.target = self.retreat_cell
            random_move = random.choice((SPEED, -SPEED))
            self.move_future = (-random_move, 0)

    # ФУНКЦИИ, ИЗМЕНЯЮЩИЕ НАПРАВЛЕНИЕ У ПРИЗРАКА, КОГДА ОН ДВИЖИТСЯ ПО ЛАБИРИНТУ

    def check_future_cell(self):
        """Проверяет является ли передняя клетка местом, где призраку нужно сделать выбор в какую сторону пойти"""
        if self.future_cell is not None:
            x, y = self.future_cell.cord
            if y in dir_select_cells.keys():
                if x in dir_select_cells[y]:
                    return True
        return False
    
    def change_direction(self):
        "Изменяет направление призрака, если впереди него стена"
        try:
            next_cell = self.get_next_cell()
            if not next_cell.type:
                side_cells_cord = self.get_side_cells() # получаем клетоки, расположенные по бокам от целевой
                cells = self.filter_cells(side_cells_cord) # получаем клеки, по которым призрак сможет идти 
                self.move_future = (cells[0].cord[0] - self.future_cell.cord[0], cells[0].cord[1] - self.future_cell.cord[1]) 
        except AttributeError:
            pass

    def select_direction(self):
        """Выбирает в какую сторону лабиринта пойти призраку"""
        next_cell = self.get_next_cell()
        side_cells = self.get_side_cells()
        list_cells = self.filter_cells((next_cell, *side_cells))
        if self.mode_now != "scare":
            cell = self.choose_cell(list_cells)
        else:
            cell = random.choice(list_cells)
        self.move_future = (cell.cord[0] - self.future_cell.cord[0], cell.cord[1] - self.future_cell.cord[1])
    
    def get_next_cell(self):
        """Возращает клетку, рассположенную впереди клетки, к которой призрак движется"""
        next_cell = (self.future_cell.cord[0] + self.move_future[0], self.future_cell.cord[1] + self.move_future[1])
        return get_cell_by_cord(next_cell, self.cells)
    
    def get_side_cells(self):
        """Находит клетоки, расположенные по бокам от передней клетки"""
        if self.move_now[1] > 0 or self.move_now[1] < 0:
            cell_1 = self.future_cell.cord[0] + 1, self.future_cell.cord[1]
            cell_2 = self.future_cell.cord[0] - 1, self.future_cell.cord[1] 
        elif self.move_now[0] > 0 or self.move_now[0] < 0:
            cell_1 = self.future_cell.cord[0], self.future_cell.cord[1] + 1
            cell_2 = self.future_cell.cord[0], self.future_cell.cord[1] - 1

        return get_cell_by_cord(cell_1, self.cells), get_cell_by_cord(cell_2, self.cells)
    
    def filter_cells(self, list_cells):
        """Фильтует клетки, на которых стоит стена, и возращает список клеток по которым можно ходить"""
        new_list_cells = []
        for cell in list_cells:
            if cell.type:
                new_list_cells.append(cell)
        return new_list_cells
    
    def choose_cell(self, list_cells):
        list_distances = self.count_distance(list_cells)
        min_distance = min(list_distances)
        index = list_distances.index(min_distance)
        return list_cells[index] 

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
                d = (x ** 2 + y ** 2) ** 0.5
            list_distances.append(round(d, 2)) 
        return list_distances


