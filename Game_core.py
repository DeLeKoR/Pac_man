from Setting import *
from Map import *
from Enemy import *
from Pac_man import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.map = Map()
        self.pac_man = Pac_man()
        self.enemies = pg.sprite.Group()
        self.create_enemies()

    def create_frame(self):
        pass

    def create_enemies(self):
        pass


