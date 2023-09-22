from Setting import *
from Basic_func import *
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

    def eat_point(self, score):
        cell = get_cell(self.rect.center, self.cells)
        if (cell is not None and ((cell.rect.centerx - self.speed / 2 <= self.centerx <= cell.rect.centerx + self.speed / 2)
                    and (cell.rect.centery - self.speed / 2 <= self.centery <= cell.rect.centery + self.speed / 2))):

            if cell.point is not None:
                score[0] += cell.point.value
                if cell.point.type == 3:
                    for enemy in self.enemies:
                        enemy.scare_mode_on()
                cell.point.kill()
                cell.point = None
                self.speed = self.loc_speed*0.9
                self.update_move()
            else:
                self.speed = self.loc_speed
                self.update_move()

            if cell.meal is not None:
                cell.meal.kill()
                score[0] += cell.meal.value
                cell.meal = None

    def interaction(self, restart, lives):
        """Определение соприкосновения пакмена с призраком"""
        for enemy in self.enemies:
            if self.rect.colliderect(enemy):
                if enemy.mode_now == 'scare':
                    pass # сюда вписать функцию для съедения призрака
                else:
                    if lives[0]:
                        restart(0)
                        lives[0] -= 1
                    else:
                        restart(1)
