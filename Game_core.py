from Setting import *
from Map import *
from Enemies import *
from Pac_man import *
from Basic_func import *
from Score_board import *

class Game:
    def __init__(self, screen, fps: int = 0):
        self.screen = screen
        self.fps = fps
        self.pause = True
        self.lives = [3]
        self.map = Map(self.screen)
        self.enemies = pg.sprite.Group()
        self.cord_red = (14, 11)
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells, self.enemies)
        self.create_enemies()
        self.score_board = Score_board(self.screen)

    def draw_frame(self):
        self.map.draw_map()
        self.map.draw_points()
        self.map.update_meal()
        self.pac_man.draw_pac_man()
        for enemy in self.enemies:
            enemy.draw_enemy()
        self.score_board.draw_board(self.fps, self.lives)

    def create_frame(self):
        self.pac_man.move()
        self.pac_man.eat_point(self.score_board.score)
        self.pac_man.interaction(self.restart, self.lives)
        self.update_ghosts()
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
            elif enemy.kill_ghost and enemy.future_cell.cord == enemy.target:
                enemy.ghost_in_house = True
                enemy.target = start_points[0]
                enemy.move_future = (0, enemy.speed)
                enemy.move()
            enemy.update()

    def restart(self, ask: bool = False):
        """
        Перезапускает игру
        False = перезапуск призраков и пакмена
        True = полный перезапуск игры
        """
        if ask:
            self.lives = [3]
            self.map = Map(self.screen)
            self.score_board = Score_board(self.screen)
        self.enemies.empty()
        self.cord_red = (14, 11)
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells, self.enemies)
        self.create_enemies()


