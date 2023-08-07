from Game_core import *
import sys

pg.init()
pg.display.set_caption('Pac_man')

screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

game = Game(screen)

while True:
    screen.fill(BG_COLOR)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                game.pac_man_move = (0, -2)
            elif event.key == pg.K_s:
                game.pac_man_move = (0, 2)
            elif event.key == pg.K_a:
                game.pac_man_move = (-2, 0)
            elif event.key == pg.K_d:
                game.pac_man_move = (2, 0)


    game.create_frame()
    game.draw_frame()

    clock.tick(60)
    pg.display.update()
