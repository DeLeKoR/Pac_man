from Setting import *
from Entity import Entity

class Ghost(Entity, pg.sprite.Sprite):
    def __init__(self, cell, cells, screen, ghost_image):
        super().__init__(screen, cell, cells)
        pg.sprite.Sprite.__init__(self)
        picture = pg.image.load(ghost_image)
        self.image = pg.transform.scale(picture, self.size)
        self.image.set_colorkey((0, 0, 0))
