from Setting import *

class BlueGhost(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(blue_ghost)
        self.rect = self.image.get_rect()

class RedGhost(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(red_ghost)
        self.rect = self.image.get_rect()

class PinkGhost(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pink_ghost)
        self.rect = self.image.get_rect()

class JelowGhost(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(jelow_ghost)
        self.rect = self.image.get_rect()
