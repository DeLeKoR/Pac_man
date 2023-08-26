from Setting import *

class Score_board:
    def __init__(self, screen):
        self.screen = screen
        self.cord = (PLAY_BOARD_SIZE[0], 0)
        self.size = (SCREEN_SIZE[0]-PLAY_BOARD_SIZE[0], SCREEN_SIZE[1])
        self.rect = pg.Rect(*self.cord, *self.size)

    def draw_board(self):
        pg.draw.rect(self.screen,(10, 10, 10), self.rect)
