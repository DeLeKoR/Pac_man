from Setting import *
from Entity import Entity
from Basic_func import get_cell_by_cord, sing_number
import random

class Ghost(Entity):
    def __init__(self, cell, cells, screen, image, color_type, retreat_cell, ghost_in_house, pac_man):
        super().__init__(screen, cell, cells)
        picture_ghost = pg.image.load(image) 
        picture_scared_ghost = pg.image.load(scared_ghost) 
        self.size = (55, 45)
        self.base_image = pg.transform.scale(picture_ghost, self.size) # основное изображение призрака
        self.scared_image = pg.transform.scale(picture_scared_ghost, self.size)  # изображение испуганного призрака
        self.image = self.base_image # текущее изибражение
        self.start_cords = cell.cord # начальное положение призрака
        self.ghost_in_house = ghost_in_house # равен True, если призрак в доме
        self.color_type = color_type # тип цвета призрака
        self.retreat_cell = retreat_cell # целевая клетка отступления
        self.target = None # целевая клетка призрака
        self.speed = 1.6
        self.pac_man = pac_man
        self.mode_now = "run"
        self.mode_first = "attack"
        self.times_modes = [7, 20, 7, 20, 5, 20, 5]
        self.index_mode = 0
        self.kill_ghost = False
        self.start_move()

    def start_move(self):
        """Приводит призраков в движение"""
        if self.color_type == "red":
            self.speed = SPEED_GHOST
            self.move_future = (-self.speed, 0)
            self.move_now = (-self.speed, 0)
            self.target = self.retreat_cell
            self.ghost_in_house = False
            self.start_cords = start_points[0]
        else:
            self.target = start_points[0]
            self.create_move(self.target, self.cell.cord)
        self.move()
        self.start_time = pg.time.get_ticks()

    def draw_enemy(self):
        self.draw(self.image)

    def update(self):
        if not self.ghost_in_house:
            if not self.kill_ghost:
                self.check_time()
            if self.check_future_cell():
                self.select_direction()
            else:
                self.change_direction()
        elif self.ghost_in_house:
            self.move_in_home()
        self.move()

    # ИЗМЕНЕНИЕ РЕЖИМОВ У ПРИЗРАКОВ

    def check_time(self):
        """Проверка времени действия текущего режима"""
        end_time = pg.time.get_ticks()
        different = (end_time - self.start_time) / 1000

        if self.mode_now != "scare" and self.index_mode < len(self.times_modes):
            time_mode = self.times_modes[self.index_mode]
            if different >= time_mode:
                self.index_mode += 1
                self.change_mode()
        elif self.mode_now == "scare":
            if different >= 5:
                self.change_mode()

    def change_mode(self):
        """Изменяет режим у призрака"""
        self.mode_now, self.mode_first = self.mode_first, self.mode_now 
        if self.mode_first == "scare":
            self.scare_mode_off()
        if self.mode_now == "run":
            self.target = self.retreat_cell

        self.move_future = self.move_now[0] * (-1), self.move_now[1] * (-1)     
        self.start_time = pg.time.get_ticks()
    
    def scare_mode_on(self):
        """Режим испуга призрака"""
        if self.mode_now != "scare":
            self.image = self.scared_image
            self.mode_first = self.mode_now
            self.mode_now = "scare"
            self.speed = 1.6
        self.start_time = pg.time.get_ticks()

    def scare_mode_off(self):
        self.image = self.base_image
        self.speed = SPEED_GHOST
        if self.mode_now == "run":
            self.mode_first = "attack"
        else:
            self.mode_first = "run"

    def kill_mode(self):
        """Режим, который срабатывает, когда призрака съедает пак ман"""
        # меняем изображение призрака
        self.target = start_points[1]
        self.kill_ghost = True
        self.speed = 3.2
    # ОПРЕДЕЛЕНИЕ ЦЕЛЕВОЙ КЛЕТКИ У ПРИЗРАКОВ В РЕЖИМЕ АТАКИ
    
    def count_target_ghosts(self, cord_red):
        """Определяет какому призраку нужно изменить целевую клетку"""  
        move = sing_number(self.pac_man.move_now[0]), sing_number(self.pac_man.move_now[1]) # получаем направление пак мана
        pacman_cord = self.pac_man.cell.cord

        if self.color_type == "red":
            self.count_target_red(pacman_cord)
        elif self.color_type == "blue":
            self.count_target_blue(move, pacman_cord, cord_red)    
        elif self.color_type == "pink":
            self.count_target_pink(move, pacman_cord)
        elif self.color_type == "yellow":
            self.count_target_yellow(pacman_cord)

    def count_target_red(self, cord):
        self.target = cord

    def count_target_pink(self, move, cord):
        self.target = cord[0] + 4 * move[0], cord[1] + 4 * move[1] # получаем координаты клетки на 4 клетки перед пак маном

    def count_target_blue(self, move, cord, cord_red):
        front_cell = cord[0] + 2 * move[0], cord[1] + 2 * move[1] # получаем координаты клетки на 2 клетки перед пак маном
        dif_x = abs(front_cell[0] - cord_red[0])
        dif_y = abs(front_cell[1] - cord_red[1])
        x, y = dif_x * 2 + cord_red[0], dif_y * 2 + cord_red[1]
        self.target = (x, y)
    
    def count_target_yellow(self, cord):
        distance = self.count_distance(self.cell.cord, cord) # получаем растояние от призрака до пак мана
        if distance >= 8:
            self.target = self.pac_man.cell.cord
        else:
            self.target = self.retreat_cell

    # ВЫВОД ПРИЗРАКОВ ИЗ ИХ ДОМА

    def move_in_home(self):
        "Перемещает призраков в их доме"
        if not self.kill_ghost:
            self.get_out()
        else:
            self.get_into()
    
    def get_out(self):
        "Заставляет призраков выйти из дома"
        if self.future_cell.cord == start_points[0]:
            self.target = start_points[1]
            self.move_future = (0, -self.speed)
        elif self.future_cell.cord == start_points[1]:
            self.target = start_points[2]
            self.move_future = (-self.speed, 0)
        elif self.future_cell.cord == start_points[2]:
            self.ghost_in_house = False
            self.target = self.retreat_cell
            self.speed = SPEED_GHOST

    def get_into(self):
        "Заставляет призраков войти в дом"
        if self.future_cell.cord == start_points[0] and self.future_cell.cord != self.start_cords:
            self.target = self.start_cords
            self.create_move(self.target, self.future_cell.cord)
        elif self.future_cell.cord == self.start_cords:
            self.kill_ghost = False
            self.image = self.base_image
            self.target = start_points[0]
            self.speed = 1.6
            self.create_move(self.target, self.cell.cord)

    # ФУНКЦИИ, ИЗМЕНЯЮЩИЕ НАПРАВЛЕНИЕ У ПРИЗРАКА, КОГДА ОН ДВИЖИТСЯ ПО ЛАБИРИНТУ

    def check_future_cell(self):
        """Проверяет является ли передняя клетка местом, где призраку нужно сделать выбор в какую сторону пойти"""
        if self.future_cell is not None:
            if self.future_cell.place_select:
                return True
        return False
    
    def create_move(self, target, cell):
        move_x = sing_number(target[0] - cell[0]) 
        move_y = sing_number(target[1] - cell[1])
        self.move_future = (move_x * self.speed, move_y * self.speed) # определяем направление
        
    def change_direction(self):
        "Изменяет направление призрака, если впереди него стена"
        try:
            next_cell = self.get_next_cell()
            if not next_cell.type:
                side_cells_cord = self.get_side_cells() # получаем клетки, расположенные по бокам от целевой
                cells = self.filter_cells(side_cells_cord) # получаем клеки, по которым призрак сможет идти 
                self.create_move(cells[0].cord, self.future_cell.cord)
        except AttributeError:
            pass

    def select_direction(self):
        """Выбирает в какую сторону лабиринта пойти призраку"""
        next_cell = self.get_next_cell()
        side_cells = self.get_side_cells()
        list_cells = self.filter_cells((next_cell, *side_cells))
        if self.mode_now != "scare" or self.kill_ghost:
            cell = self.choose_cell(list_cells)
        else:
            cell = random.choice(list_cells)

        self.create_move(cell.cord, self.future_cell.cord)
        
    def get_next_cell(self):
        """Возращает клетку, рассположенную впереди клетки, к которой призрак движется"""
        move_x, move_y = sing_number(self.move_future[0]), sing_number(self.move_future[1])
        cords = (self.future_cell.cord[0] + move_x, self.future_cell.cord[1] + move_y)
        return get_cell_by_cord(cords, self.cells) 

    def get_side_cells(self):
        """Находит клетки, расположенные по бокам от передней клетки"""
        result = []
        for side in (-1, 1):
            move_x, move_y = sing_number(self.move_now[0]), sing_number(self.move_now[1]) # получаем направление призрака
            cord = self.future_cell.cord[0] + move_y * side, self.future_cell.cord[1] + move_x * side # координаты боковой клетки
            cell = get_cell_by_cord(cord, self.cells)
            result.append(cell)
        return result

    def filter_cells(self, list_cells):
        """Фильтует клетки, на которых стоит стена, и возращает список клеток по которым можно ходить"""
        return [cell for cell in list_cells if cell.type]
    
    def choose_cell(self, list_cells):
        list_distances = []
        for cell in list_cells:
            distance = self.count_distance(cell.cord, self.target)
            list_distances.append(distance)
        min_distance = min(list_distances)
        index = list_distances.index(min_distance)
        return list_cells[index] 

    def count_distance(self, cord_1, cord_2):
        """Находит расстояние от одной точки до другой"""
        if cord_1[0] == cord_2[0]:
            d = abs(cord_1[1] - cord_2[1])
        elif cord_1[1] == cord_2[1]:
            d = abs(cord_1[0] - cord_2[0])
        else:
            x, y = cord_1[0] - cord_2[0], cord_1[1] - cord_2[1]
            d = (x ** 2 + y ** 2) ** 0.5
        return round(d, 2)