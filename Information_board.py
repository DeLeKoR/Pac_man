from Setting import *

class Information_board:
    def __init__(self, screen):
        self.screen = screen

        self.color = (240, 240, 240)

        self.font = pg.font.Font("Fonts/dpix_8pt.ttf", 32)
        self.text_Score = self.font.render(f' Score:', True, self.color)

        picture = pg.image.load(PAC_MAN_IMG_PASS)
        self.texture = pg.transform.scale(picture, (40, 40))

        self.size = (SCREEN_SIZE[0]-PLAY_BOARD_SIZE[0], SCREEN_SIZE[1])
        self.surface = pg.Surface(self.size)
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.topleft = ((PLAY_BOARD_SIZE[0], 0))

    def draw_board(self, fps, lives, level, score):
        self.surface.fill((10, 10, 20))

        text_score = self.font.render(f' {score[0]}', True, self.color)
        text_fps = self.font.render(f'{int(fps)}', True, self.color)
        text_level = self.font.render(f'Level: {level}', True, self.color)
        # отрисовка счётчика
        self.surface.blit(self.text_Score, (0, 0))
        self.surface.blit(text_score, (0, text_score.get_size()[1]))
        # отрисовка жизней
        for i in range(lives[0]):
            self.surface.blit(self.texture, (self.surface_rect.width - self.texture.get_size()[0] - 5,self.texture.get_size()[1]*i + 5*(i+1)))
        # отрисовка фпс
        self.surface.blit(text_fps, (0, self.surface_rect.height - text_fps.get_size()[1]))
        # отрисовка уровня
        self.surface.blit(text_level, (text_level.get_size()[0]/2, self.surface_rect.height-text_level.get_size()[1]))

        self.screen.blit(self.surface, self.surface_rect)
