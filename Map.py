from Setting import *

class Map:
    def __init__(self, screen):
        self.screen = screen
        picture = pg.image.load(MAP_IMG_PASS)
        self.map = pg.transform.scale(picture, SCREEN_SIZE)

    def draw(self):
        self.screen.blit(self.map, (0, 0))