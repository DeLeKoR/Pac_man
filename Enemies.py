from Setting import *
from Entity import Entity
from Basic_func import get_cell_by_cord

class Ghost(Entity):
    def __init__(self, cell, cells, screen, image, color_type, start_point, retreat_cell, ghost_in_house):
        super().__init__(screen, cell, cells)
        picture = pg.image.load(image)
        self.image = pg.transform.scale(picture, self.size)
        self.start_cords = cell.cord
        self.activity = act_ghosts # активность призрака
        self.ghost_in_house = ghost_in_house # равен True, если призрак в доме
        self.color_type = color_type
        self.start_point = start_point # целевая клетка
        self.retreat_cell = retreat_cell # целевая клетка отступления

    def update(self):
        if self.activity and self.ghost_in_house:
            self.start_move()
        elif self.activity and not self.ghost_in_house and self.color_type != "red":
            self.change_direction()
        if self.activity:
            self.move()
            
    def start_move(self):
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
            print(self.move_future)
            self.ghost_in_house = False
            self.move_future = (-SPEED, 0)

    def change_direction(self):
        "Изменяет направление призрака, если впереди него стена"
        cords_next = (self.future_cell.cord[0] + self.move_future[0], self.future_cell.cord[1] + self.move_future[1])
        print(self.cell.cord, self.future_cell.cord, cords_next)
        next_cell = get_cell_by_cord(cords_next, self.cells)
        if not next_cell.type:
            cell = self.found_cell()
            self.move_future = (cell.cord[0] - self.future_cell.cord[0], cell.cord[1] - self.future_cell.cord[1]) 

    def found_cell(self):
        for _ in range(2):
            if self.move_now[1] > 1 or self.move_now[1] < 1:
               cell_1 = self.future_cell.cord[0], self.future_cell.cord[1] + 1
               cell_2 = self.future_cell.cord[0], self.future_cell.cord[1] - 1
            elif self.move_now[0] > 1 or self.move_now[0] < 1:
                cell_1 = self.future_cell.cord[0] + 1, self.future_cell.cord[1] 
                cell_2 = self.future_cell.cord[0] - 1, self.future_cell.cord[1] 
        
        return self.check_cells((cell_1, cell_2))
    
    def check_cells(self, list_cords):
        for cord in list_cords:
            cell = get_cell_by_cord(cord, self.cells)
            if cell.type:
                return cell

