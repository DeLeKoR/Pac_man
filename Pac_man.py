from Setting import *
from Basic_func import *
from Entity import *

class Pac_man(Entity):
    def __init__(self, cell, screen, cells, enemies):
        super().__init__(screen, cell, cells)
        picture = pg.image.load(PAC_MAN_IMG_PASS)
        self.pac_man = pg.transform.scale(picture, self.size)
        self.enemies = enemies

    def draw_pac_man(self):
        self.draw(self.pac_man)

    def eat_point(self, score):
        cell = get_cell(self.rect.center, self.cells)
        if cell is not None and ((cell.rect.centerx - SPEED/2 <= self.rect.centerx <= cell.rect.centerx + SPEED/2)
                    and (cell.rect.centery - SPEED/2 <= self.rect.centery <= cell.rect.centery + SPEED/2)) and cell.point is not None:
            score[0] += cell.point.value
            if cell.point.type == 3:
                for enemy in self.enemies:
                    enemy.scare_mode_on()
            cell.point.kill()
            cell.point = None
        if cell is not None and ((cell.rect.centerx - SPEED/2 <= self.rect.centerx <= cell.rect.centerx + SPEED/2)
                    and (cell.rect.centery - SPEED/2 <= self.rect.centery <= cell.rect.centery + SPEED/2)) and cell.meal is not None:
            cell.meal.kill()
            score[0] += cell.meal.value
            cell.meal = None

    def interaction(self, restart, lives):
        """Определение соприкосновения пакмена с призраком"""
        for enemy in self.enemies:
            if self.cell.cord == enemy.cell.cord:
                if enemy.mode_now == 'scare':
                    enemy.kill_mode()
                elif enemy.mode_now == "attack":
                    if lives[0]:
                        restart(0)
                        lives[0] -= 1
                    else:
                        restart(1)
