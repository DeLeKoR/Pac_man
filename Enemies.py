from Setting import *
from Entity import Entity
from Basic_func import get_cell_by_cord, sing_number
import random

class Ghost(Entity):
    def __init__(self, cell, cells, screen, image, color_type, retreat_cell, ghost_in_house, pac_man, limit_point):
        super().__init__(screen, cell, cells)
        self.base_image = pg.transform.scale(pg.image.load(image), self.size) # основное изображение призрака
        self.scared_ghost = pg.transform.scale(pg.image.load(scared_ghost), self.size)  # изображение испуганного призрака
        self.white_ghost = pg.transform.scale(pg.image.load(white_ghost), self.size)  # изображение белого от испуга призрака
        self.ghost_eyes = pg.transform.scale(pg.image.load(ghost_eyes), self.size) # изображение глаз призрака
        self.list_scare_imgs = [self.scared_ghost, self.white_ghost]   # изображения испуганного призрака
        self.start_time_img = 0    # время, когда у спрайта меняется изображение
        self.image = self.base_image  # текущее изибражение
        self.value = 200  # ценность призрака
        self.activity = False
        self.point_limit = limit_point    # число, которое должен набрать игрок, чтобы запустить призраков
        self.start_cords = cell.cord    # начальное положение призрака
        self.ghost_in_house = ghost_in_house    # равен True, если призрак в доме
        self.color_type = color_type    # тип цвета призрака
        self.retreat_cell = retreat_cell    # целевая клетка отступления
        self.target = None  # целевая клетка призрака
        self.pac_man = pac_man
        self.mode_now = "run"
        self.mode_first = "attack"
        self.times_modes = [7, 20, 7, 20, 5, 20, 5]
        self.start_time_mode = 0
        self.time_mode_scare = 5 # время действия режима испуга
        self.index_mode = 0
        self.kill_ghost = False

    def start_move(self):
        """Приводит призраков в движение"""
        if self.color_type == "red":
            self.speed = 2.5
            self.move_future = [-self.speed, 0]
            self.move_now = [-self.speed, 0]
            self.target = self.retreat_cell
            self.ghost_in_house = False
            self.start_cords = start_points[0]
            self.start_time_mode = pg.time.get_ticks()
        else:
            self.target = start_points[0]
            self.speed = 1
            self.create_future_move(self.target, self.cell.cord)
        self.update_move()
        self.move()

    def draw_enemy(self):
        self.draw(self.image)

    def update(self):
        if not self.ghost_in_house:
            if self.check_future_cell():
                self.select_direction()
            else:
                self.turn_other_direction()
        elif self.ghost_in_house:
            self.move_in_home()
        self.move()

    # ИЗМЕНЕНИЕ РЕЖИМОВ У ПРИЗРАКОВ

    def check_time(self):
        """Проверка времени действия текущего режима"""
        end_time = pg.time.get_ticks()
        different = (end_time - self.start_time_mode) / 1000

        if self.mode_now != "scare" and self.index_mode < len(self.times_modes):
            time_mode = self.times_modes[self.index_mode]
            if different >= time_mode:
                self.index_mode += 1
                return True
        elif self.mode_now == "scare":
            if different >= 5:
                return True
        return False

    def change_mode(self):
        """Изменяет режим у призрака"""
        if self.mode_now == "scare":
            self.scare_mode_off()

        elif self.mode_now != "scare" and not self.ghost_in_house:
            self.mode_now, self.mode_first = self.mode_first, self.mode_now
            self.move_future = [self.move_now[0] * (-1), self.move_now[1] * (-1)]

        if self.mode_now == "run":
            self.target = self.retreat_cell

        self.start_time_mode = pg.time.get_ticks()

    def scare_mode_on(self):
        """Режим испуга призрака"""
        if self.mode_now != "scare":
            self.image = self.scared_ghost
            self.mode_first = self.mode_now
            self.mode_now = "scare"
            self.speed = 1.7
            self.update_move()
            self.move_future = [self.move_now[0] * (-1), self.move_now[1] * (-1)]

        self.start_time_mode = pg.time.get_ticks()

    def scare_mode_off(self):
        self.mode_now, self.mode_first = self.mode_first, self.mode_now
        self.image = self.base_image
        if not self.ghost_in_house:
            self.speed = 2.5
            self.update_move()
        if self.mode_now == "run":
            self.mode_first = "attack"
        else:
            self.mode_first = "run"

    def kill_mode(self):
        """Режим, который срабатывает, когда призрака съедает пак ман"""
        self.image = self.ghost_eyes # меняем изображение спрайта призрака
        self.target = start_points[1]
        self.kill_ghost = True
        self.speed = 3.5
        self.update_move()
        self.move_future = [sing_number(self.move_future[0]) * self.speed, sing_number(self.move_future[1]) * self.speed]
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
            self.move_future = [0, -self.speed]
        elif self.future_cell.cord == start_points[1]:
            self.target = start_points[2]
            self.move_future = [-self.speed, 0]
        elif self.future_cell.cord == start_points[2]:
            self.change_mode()
            self.ghost_in_house = False
            self.speed = 2.5
            self.update_move()
            self.move_future = [-self.speed, 0]

    def get_into(self):
        "Заставляет призраков войти в дом"
        if self.future_cell.cord == start_points[0] and self.future_cell.cord != self.start_cords:
            self.target = self.start_cords
            self.create_future_move(self.target, self.future_cell.cord)
        elif self.future_cell.cord == self.start_cords:
            self.kill_ghost = False
            self.image = self.base_image
            self.target = start_points[0]
            self.speed = 1
            self.update_move()
            self.create_future_move(self.target, self.cell.cord)

    # ДВИЖЕНИЕ ПРИЗРАКА В ТУНЕЛЕ

    def ghost_in_tunnel(self):
        """Изменяет скорость у призрака, если он в тунеле"""
        if self.future_cell is not None:
            if self.future_cell.type == 2:
                self.speed = 1.4
            elif self.future_cell.type == 1:
                if self.mode_now != "scare":
                    self.speed = 2.5
                else:
                    self.speed = 1.7
        else:
            self.speed = 1.4
        self.update_move()
        self.move_future = [sing_number(self.move_future[0]) * self.speed, sing_number(self.move_future[1]) * self.speed]

    # ФУНКЦИИ, ИЗМЕНЯЮЩИЕ НАПРАВЛЕНИЕ У ПРИЗРАКА, КОГДА ОН ДВИЖИТСЯ ПО ЛАБИРИНТУ

    def check_future_cell(self):
        """Проверяет является ли передняя клетка местом, где призраку нужно сделать выбор в какую сторону пойти"""
        if self.future_cell is not None:
            if self.future_cell.place_select:
                return True
        return False

    def create_future_move(self, target, cell):
        move_x = sing_number(target[0] - cell[0]) * self.speed
        move_y = sing_number(target[1] - cell[1]) * self.speed
        self.move_future = [move_x, move_y] # определяем направление

    def turn_other_direction(self):
        "Изменяет направление призрака, если впереди него стена"
        if self.future_cell is not None:
            next_cell = self.get_next_cell()
            if next_cell is not None and not next_cell.type:
                if not self.kill_ghost and self.check_time():
                    self.change_mode()
                    return
                side_cells_cord = self.get_side_cells() # получаем клетки, расположенные по бокам от целевой
                cells = self.filter_cells(side_cells_cord) # получаем клеки, по которым призрак сможет идти
                self.create_future_move(cells[0].cord, self.future_cell.cord)

    def select_direction(self):
        """Выбирает в какую сторону лабиринта пойти призраку"""
        if not self.kill_ghost and self.check_time():
            self.change_mode()
            return
        next_cell = self.get_next_cell()
        side_cells = self.get_side_cells()
        list_cells = self.filter_cells((next_cell, *side_cells))
        if self.mode_now != "scare" or self.kill_ghost:
            cell = self.choose_cell(list_cells)
        else:
            cell = random.choice(list_cells)

        self.create_future_move(cell.cord, self.future_cell.cord)
        
    def get_next_cell(self):
        """Возращает клетку, рассположенную впереди клетки, к которой призрак движется"""
        move_x, move_y = sing_number(self.move_future[0]), sing_number(self.move_future[1])
        cords = (self.future_cell.cord[0] + move_x, self.future_cell.cord[1] + move_y)
        return get_cell_by_cord(cords, self.cells) 

    def get_side_cells(self):
        """Находит клетки, расположенные по бокам от передней клетки"""
        result = []
        move_x, move_y = sing_number(self.move_now[0]), sing_number(self.move_now[1])  # получаем направление призрака
        for side in (-1, 1):
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