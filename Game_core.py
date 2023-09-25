from Setting import *
from Map import *
from Enemies import *
from Pac_man import *
from Basic_func import *
from Information_board import *

class Game:
    def __init__(self, screen, fps: int = 0):
        self.screen = screen
        self.fps = fps
        self.pause = True
        self.lives = [3]
        self.score = [0]
        self.level = 1
        self.map = Map(self.screen)
        self.enemies = pg.sprite.Group()
        self.cord_red = (14, 11)
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells, self.enemies)
        self.create_enemies()
        self.info_board = Information_board(self.screen)

    def draw_frame(self):
        self.map.draw_map()
        # self.pac_man.draw_pac_man()
        # for enemy in self.enemies:
        #     enemy.draw_enemy()
        self.info_board.draw_board(self.fps, self.lives, self.level, self.score)

    def create_frame(self):
        # if self.map.check_points():
        #     self.restart(2)
        #     self.level += 1
        # self.pac_man.move()
        # self.pac_man.eat_point(self.score, self.map.numbers)
        # self.pac_man.interaction(self.restart, self.lives)
        # self.update_ghosts()
        self.map.create_meal()

    def create_enemies(self): 
        for color_type, image, cords, retreat in zip(ghosts_colors, images_ghosts, cords_ghosts, retreat_cords):
            cell = get_cell_by_cord(cords, self.map.cells)
            ghost = Ghost(cell, self.map.cells, self.screen, image, color_type, retreat, True, self.pac_man)
            self.enemies.add(ghost)

    def update_ghosts(self):
        for enemy in self.enemies:
            if enemy.mode_now == "attack": 
                if enemy.color_type == "red":
                    self.cord_red = enemy.cell.cord
                enemy.count_target_ghosts(self.cord_red) 
            enemy.update()

    def restart(self, ask: int = 0):
        """
        Перезапускает игру
        False = перезапуск призраков и пакмена
        True = полный перезапуск игры
        """
        if ask == 1 or ask == 2:
            self.map = Map(self.screen)
        if ask == 1:
            self.info_board = Information_board(self.screen)
            self.level = 1
            self.score = [0]
            self.lives = [2]
        self.enemies.empty()
        self.cord_red = (14, 11)
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells, self.enemies)
        self.create_enemies()


