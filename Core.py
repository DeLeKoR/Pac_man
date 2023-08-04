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
    clock.tick(60)
    pg.display.update()
