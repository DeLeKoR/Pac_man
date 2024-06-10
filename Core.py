from Game_core import *
from Main_menu import *
import sys

class Core:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Pac_man')

        self.screen = pg.display.set_mode(SCREEN_SIZE)
        self.clock = pg.time.Clock()

        self.main_screen = Main_menu(self.screen, self.change_game_mod, self.quite_game)
        self.game = Game(self.screen, activ=False)

        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.quite_game()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.change_game_mod()
            if self.game.activ:
                self.update_game(events)
            elif self.main_screen.activ:
                self.main_screen.draw()
                self.main_screen.button_update()

            self.clock.tick(FPS)
            pg.display.update()

    def change_game_mod(self):
        self.game.activ ^= True
        self.game.restart(True)
        self.main_screen.activ ^= True

    def update_game(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if self.game.pause:
                    if event.key == pg.K_w or event.key == pg.K_UP:
                        self.game.pac_man.move_future = [0, -self.game.pac_man.speed]
                    elif event.key == pg.K_s or event.key == pg.K_DOWN:
                        self.game.pac_man.move_future = [0, self.game.pac_man.speed]
                    elif event.key == pg.K_a or event.key == pg.K_LEFT:
                        self.game.pac_man.move_future = [-self.game.pac_man.speed, 0]
                    elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                        self.game.pac_man.move_future = [self.game.pac_man.speed, 0]
                if event.key == pg.K_ESCAPE:
                    self.game.pause ^= True
        if self.game.pause:
            self.game.fps = self.clock.get_fps()
            self.game.create_frame()
        self.game.draw_frame()

    def quite_game(self):
        pg.quit()
        sys.exit()


if __name__ == '__main__':
    core = Core()


