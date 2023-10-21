from Setting import *

class Score_board:
    def __init__(self, screen):
        pg.font.init()
        self.font = pg.font.Font("Fonts/dpix_8pt.ttf", 32)
        picture = pg.image.load(PAC_MAN_IMG_PASS)
        self.texture = pg.transform.scale(picture, (40, 40))
        self.screen = screen
        self.cord = (PLAY_BOARD_SIZE[0], 0)
        self.size = (SCREEN_SIZE[0]-PLAY_BOARD_SIZE[0], SCREEN_SIZE[1])
        self.rect = pg.Rect(*self.cord, *self.size)
        self.score = [0]
        self.color = (240, 240, 240)

    def draw_board(self, fps, lives, level):
        pg.draw.rect(self.screen,(10, 10, 10), self.rect)

        text_Score = self.font.render(f' Score:', True, self.color)
        text_score = self.font.render(f' {self.score[0]}', True, self.color)
        text_fps = self.font.render(f'{int(fps)}', True, self.color)
        text_level = self.font.render(f'Level: {level}', True, self.color)

        # отрисовка счётчика
        self.screen.blit(text_Score, self.cord)
        self.screen.blit(text_score, (self.cord[0], self.cord[1] + text_score.get_size()[1]))
        # отрисовка жизней
        for i in range(lives[0]):
            self.screen.blit(self.texture, (SCREEN_SIZE[0]-self.texture.get_size()[0],self.texture.get_size()[1]*i + 5*(i+1)))
        # отрисовка фпс
        self.screen.blit(text_fps, (self.cord[0], SCREEN_SIZE[1] - text_fps.get_size()[1]))
        # отрисовка уровня
        self.screen.blit(text_level, (self.cord[0]+text_level.get_size()[0]/2, SCREEN_SIZE[1]-text_level.get_size()[1]))

