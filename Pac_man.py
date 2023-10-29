from Setting import *
from Basic_func import *
from Text_points import *
from Entity import *

class Pac_man(Entity):
    def __init__(self, cell, screen, cells, enemies, stop_entity):
        super().__init__(screen, cell, cells)
        self.picture = [pg.image.load(f'images/Pac_man_{x}.png') for x in range(3)]
        for index, image in enumerate(self.picture):
            self.picture[index] = pg.transform.scale(image, self.size)
        self.pac_man = self.picture[0]
        self.stop_entity = stop_entity
        self.enemies = enemies
        self.loc_speed = self.speed
        self.direction = 0
        self.__directions = [{1: 0, -1: 2}, {1: 1, -1: 3}]
        self.__counter = 0
        self.__index = 0
        self.__offset = -1

    def draw_pac_man(self):
        if self.moving:
            if self.__counter % 4 == 0:
                if self.__index == 2:
                    self.__offset *= -1
                elif self.__index == 0:
                    self.pac_man = self.picture[self.__index]
                    self.__offset *= -1
                self.pac_man = self.picture[self.__index]
                self.__index += self.__offset
                self.change_direction()
            self.__counter += 1
        else:
            self.__index = 0
            self.__offset = -1
            self.pac_man = self.picture[self.__index]
        self.draw(self.pac_man)

    def change_direction(self):
        for index, i in enumerate(self.move_now):
            if i:
                self.direction = self.__directions[index][sing_number(i)]
        self.pac_man = pg.transform.rotate(self.pac_man, -90*self.direction)

    def eat_point(self, score, number):
        cell = get_cell(self.rect.center, self.cells)
        if (cell is not None and ((cell.rect.centerx - self.speed / 2 <= self.centerx <= cell.rect.centerx + self.speed / 2)
                    and (cell.rect.centery - self.speed / 2 <= self.centery <= cell.rect.centery + self.speed / 2))):

            if cell.point is not None:
                number(cell)
                score[0] += cell.point.value
                if cell.point.type == 3:
                    for enemy in self.enemies:
                        if not enemy.ghost_in_house:
                            enemy.scare_mode_on()
                cell.point.kill()
                cell.point = None
                self.speed = self.loc_speed*0.9
                self.update_move()
            else:
                self.speed = self.loc_speed
                self.update_move()

            if cell.meal is not None:
                number(cell, size=28)
                cell.meal.kill()
                score[0] += cell.meal.value
                cell.meal = None

    def interaction(self, restart, lives, enemy, score, number):
        """Определение соприкосновения пакмена с призраком"""
        if self.touch_rect.colliderect(enemy.touch_rect):
            if enemy.mode_now == 'scare':
                if not enemy.kill_ghost:
                    self.stop_entity()
                    score[0] += enemy.value
                    number(enemy.cell, enemy.value, 30)
                enemy.kill_mode()
            else:
                if lives[0]:
                    restart(0)
                    lives[0] -= 1
                else:
                    restart(1)
