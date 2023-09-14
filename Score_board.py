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

    def draw_board(self, fps, lives):
        pg.draw.rect(self.screen,(10, 10, 10), self.rect)
        text1 = self.font.render(f' Score:', True, self.color)
        text2 = self.font.render(f' {self.score[0]}', True, self.color)
        text3 = self.font.render(f'{int(fps)}', True, self.color)
        text_size = text2.get_size()
        self.screen.blit(text1, self.cord)
        self.screen.blit(text2, (self.cord[0], self.cord[1]+text_size[1]))
        self.screen.blit(text3, (self.cord[0], SCREEN_SIZE[1]-text3.get_size()[1]))
        for i in range(lives[0]):
            self.screen.blit(self.texture, (SCREEN_SIZE[0]-self.texture.get_size()[0]*(i+1), SCREEN_SIZE[1]-self.texture.get_size()[1]-5))

