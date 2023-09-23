from Setting import *
from Basic_func import *
from Text_points import *
from Entity import *

class Pac_man(Entity):
    def __init__(self, cell, screen, cells, enemies):
        super().__init__(screen, cell, cells)
        picture = pg.image.load(PAC_MAN_IMG_PASS)
        self.pac_man = pg.transform.scale(picture, self.size)
        self.enemies = enemies
        self.loc_speed = self.speed

    def draw_pac_man(self):
        self.draw(self.pac_man)

    def eat_point(self, score, numbers):
        cell = get_cell(self.rect.center, self.cells)
        if (cell is not None and ((cell.rect.centerx - self.speed / 2 <= self.centerx <= cell.rect.centerx + self.speed / 2)
                    and (cell.rect.centery - self.speed / 2 <= self.centery <= cell.rect.centery + self.speed / 2))):

            if cell.point is not None:
                numbers.add(Number(cell))
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
                numbers.add(Number(cell))
                cell.meal.kill()
                score[0] += cell.meal.value
                cell.meal = None

    def interaction(self, restart, lives, enemy):
        """Определение соприкосновения пакмена с призраком"""
        if self.cell.cord == enemy.cell.cord:
            if enemy.mode_now == 'scare':
                enemy.kill_mode()
            elif enemy.mode_now == "attack":
                if lives[0]:
                    restart(0)
                    lives[0] -= 1
                else:
                    restart(1)
