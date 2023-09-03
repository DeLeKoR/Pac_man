from Setting import *
from Map import *
from Enemies import *
from Pac_man import *
from Basic_func import *
from Score_board import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.map = Map(self.screen)
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells)
        self.enemies = pg.sprite.Group()
        self.create_enemies()
        self.score_board = Score_board(self.screen)

    def draw_frame(self):
        self.map.draw_map()
        self.map.draw_points()
        self.map.update_meal()
        self.pac_man.draw_pac_man()
        self.enemies.draw(self.screen)
        self.score_board.draw_board()

    def create_frame(self):
        self.pac_man.eat_point(self.score_board.score)
        self.pac_man.move()
        self.enemies.update()
        self.map.create_meal()

    def create_enemies(self): 
        for color_type, image, cords, retreat in zip(ghosts_colors, images_ghosts, cords_ghosts, retreat_cords):
            cell = get_cell_by_cord(cords, self.map.cells)
            ghost = Ghost(cell, self.map.cells, self.screen, image, color_type, retreat, True, self.pac_man)
            self.enemies.add(ghost)


