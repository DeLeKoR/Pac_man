from Setting import *
from Map import *
from Enemies import *
from Pac_man import *
from Basic_func import *
from Information_board import *
import os

class Game:
    def __init__(self, screen, fps: int = 0, activ=True):
        self.activ = activ
        self.screen = screen
        self.fps = fps
        self.tick = 0
        self.old_tick = 0
        self.pause = True
        self.entity_pause = True
        self.lives = [3]
        self.score = [0]
        self.level = 1
        self.map = Map(self.screen, self.level)
        self.enemies = pg.sprite.Group()
        self.cord_red = (14, 11)
        self.first_points = len(self.map.points) # общее кол-во точек на карте
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells, self.enemies, self.stop_entity)
        self.create_enemies()
        if not os.path.isfile('max_score.txt'):
            self.save_max_score()
        self.info_board = Information_board(self.screen, self.read_max_score)

    def draw_frame(self):
        self.screen.fill(BG_COLOR)
        self.map.draw_map()
        if self.entity_pause:
            self.pac_man.draw_pac_man()
        for enemy in self.enemies:
            if (enemy.kill_ghost and self.entity_pause) or not enemy.kill_ghost or self.entity_pause:
                enemy.draw_enemy()
        self.info_board.draw_board(self.fps, self.lives, self.level, self.score)

    def create_frame(self):
        if self.map.check_points():
            self.restart(2)
            self.level += 1
            self.map.level += 1
        if self.entity_pause:
            self.pac_man.move()
            self.pac_man.eat_point(self.score, self.map.add_number)
            self.update_ghosts()
        else:
            self.stop_entity()
        self.map.create_meal()

    def create_enemies(self): 
        for color_type, cords, retreat, point_limit, time_limit in zip(ghosts_colors, cords_ghosts, retreat_cords, points_limit, times_limit):
            all_images = load_ghost_images(color_type)
            group_images = all_images["down"]
            cell = get_cell_by_cord(cords, self.map.cells)
            ghost = Ghost(cell, self.map.cells, self.screen, group_images, all_images, color_type, retreat, True, self.pac_man, point_limit, time_limit)
            self.enemies.add(ghost)

    def update_ghosts(self):
        for enemy in self.enemies:
            if enemy.activity:
                if not enemy.kill_ghost and (enemy.cell.cord == (5, 14) or enemy.cell.cord == (22, 14) or (enemy.future_cell is None and enemy.cell.type == 2)):
                    enemy.ghost_in_tunnel()
                self.pac_man.interaction(self.restart, self.lives, enemy, self.score, self.map.add_number) # проверяем взаимодействие пакмана с призраком
                if enemy.mode_now == "attack":
                    if enemy.color_type == "red":
                        self.cord_red = enemy.cell.cord
                    enemy.count_target_ghosts(self.cord_red)

                elif enemy.kill_ghost and enemy.future_cell is not None and enemy.future_cell.cord == enemy.target:
                    enemy.ghost_in_house = True
                    enemy.target = start_points[0]
                    enemy.move_future = [0, enemy.speed]
                    enemy.move()
                enemy.update_image()
                enemy.update()
            else:
                if (self.first_points - len(self.map.points) >= enemy.point_limit) or (pg.time.get_ticks() - self.pac_man.time_eat) / 1000 >= enemy.time_limit: # если кол-во точек, которых съел пакман, превышает лимит, то призрак должен начать двигаться
                    enemy.start_move()
                    enemy.activity = True
                    self.first_points = len(self.map.points)

    def stop_entity(self):
        """Останавливает призраков с пакманом на промежуток времени"""
        self.tick = pg.time.get_ticks()
        if self.entity_pause:
            self.old_tick = self.tick
            self.entity_pause ^= True
        if self.tick - self.old_tick > 900:
            self.entity_pause ^= True

    def restart(self, ask: int = 0):
        """
        Перезапускает игру
        False = перезапуск призраков и пакмена
        True = полный перезапуск игры
        """
        if ask == 1 or ask == 2:
            self.map = Map(self.screen, self.level)
        if ask == 1:
            if int(self.read_max_score()) < self.score[0]:
                self.save_max_score()
            self.info_board = Information_board(self.screen, self.read_max_score)
            self.level = 1
            self.score = [0]
            self.lives = [2]
        self.enemies.empty()
        self.cord_red = (14, 11)
        self.first_points = len(self.map.points)
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells, self.enemies, self.stop_entity)
        self.create_enemies()

    def save_max_score(self):
        """Сохраняет текущий результат"""
        with open('max_score.txt', 'w', encoding='UTF-8') as file:
            file.write(str(*self.score))

    def read_max_score(self) -> str:
        """Возвращает строку с максимальным результатом"""
        with open('max_score.txt', 'r', encoding='UTF-8') as file:
            return str(file.read())




