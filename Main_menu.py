from Setting import *

class Main_menu():
    def __init__(self, screen, replace, quite):
        self.replace = replace
        self.quite = quite
        self.activ = True
        self.screen = screen
        self.buttons = pg.sprite.Group()
        self.font = pg.font.Font('Fonts/Phosphate.ttc', 128)
        self.maintext = self.font.render('Pacman', True, (250, 250, 250))
        self.create_buttons()

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.maintext, (SCREEN_SIZE[0]/2 - self.maintext.get_rect().centerx, 50))

    def create_buttons(self):
        new_game = Button(self.screen, 32, (300, 400), 'Новая игра', (200, 200, 200), (250, 250, 250), self.replace)
        exit_game = Button(self.screen, 32, (300, 450), 'Выйти из игры', (200, 200, 200), (250, 250, 250), self.quite)
        self.buttons.add(new_game, exit_game)
        for button in self.buttons:
            button.rect.centerx = SCREEN_SIZE[0]/2

    def button_update(self):
        for button in self.buttons:
            button.draw()
            button.tup()


class Button(pg.sprite.Sprite):
    def __init__(self, screen, size_text: int, cords: tuple | list, text, color, hover_color, func):
        super().__init__()
        self.func = func
        self.screen = screen
        self.size_text = size_text
        self.cords = cords
        self.text = text
        self.color = color
        self.font = pg.font.Font('Fonts/pixel-cyr-normal.ttf', self.size_text)
        self.hover_color = hover_color
        text = self.font.render(self.text, True, self.color)
        self.rect = pg.rect.Rect(*self.cords, *text.get_rect().size)


    def draw(self):
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            text = self.font.render(self.text, True, self.hover_color)
            text_rect = text.get_rect(center=self.rect.center)
            self.screen.blit(text, text_rect)
        else:
            text = self.font.render(self.text, True, self.color)
            text_rect = text.get_rect(center=self.rect.center)
            self.screen.blit(text, text_rect)

    def tup(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if pg.mouse.get_pressed()[0]:
                self.func()

