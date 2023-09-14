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
            if game.pause:
                if event.key == pg.K_w or event.key == pg.K_UP:
                    game.pac_man.move_future = (0, -SPEED)
                elif event.key == pg.K_s or event.key == pg.K_DOWN:
                    game.pac_man.move_future = (0, SPEED)
                elif event.key == pg.K_a or event.key == pg.K_LEFT:
                    game.pac_man.move_future = (-SPEED, 0)
                elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                    game.pac_man.move_future = (SPEED, 0)
            if event.key == pg.K_ESCAPE:
                game.pause ^= True
    if game.pause:
        game.fps = clock.get_fps()
        game.create_frame()
    game.draw_frame()

    clock.tick(FPS)
    pg.display.update()
