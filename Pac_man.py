from Setting import *

class Pac_man:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.textures = []
        self.create_image()
        self.rect = self.textures[0].get_rect()

    def create_image(self):
        picture = pg.image.load(PAC_MAN_IMG_PASS)
        pac_man = pg.transform.scale(picture, PAC_MAN_SIZE)
        self.textures.append(pac_man)


    def move(self, x: int = 0, y: int = 0):
        if len(self.textures) < 2:
            if self.x < 0 + PAC_MAN_SIZE[0]:
                self.create_image()
            elif self.x > SCREEN_SIZE[0] - PAC_MAN_SIZE[0]:
                self.create_image()
            elif self.y < 0 + PAC_MAN_SIZE[1]:
                self.create_image()
            elif self.y > SCREEN_SIZE[1] - PAC_MAN_SIZE[1]:
                self.create_image()
        else:
            if self.x < 0 - PAC_MAN_SIZE[0]:
                self.x = SCREEN_SIZE[0] - PAC_MAN_SIZE[0]
                self.textures.pop(1)
            elif self.x > SCREEN_SIZE[0]:
                self.x = 0
                self.textures.pop(1)
            if self.y < 0 - PAC_MAN_SIZE[1]:
                self.y = SCREEN_SIZE[1] - PAC_MAN_SIZE[1]
                self.textures.pop(1)
            elif self.y > SCREEN_SIZE[1]:
                self.y = 0
                self.textures.pop(1)

        self.x += x
        self.y += y
        self.rect.x, self.rect.y = self.x, self.y

    def draw(self):
        self.screen.blit(self.textures[0], (self.x, self.y))
        if len(self.textures) > 1:
            if PAC_MAN_SIZE[1] < self.y < SCREEN_SIZE[1]-PAC_MAN_SIZE[1]:
                if self.x < 0 + PAC_MAN_SIZE[0]:
                    self.screen.blit(self.textures[1], (self.x + SCREEN_SIZE[0], self.y))
                else:
                    self.screen.blit(self.textures[1], (self.x - SCREEN_SIZE[0], self.y))
            else:
                if self.y < 0 + PAC_MAN_SIZE[1]:
                    self.screen.blit(self.textures[1], (self.x, self.y + SCREEN_SIZE[1]))
                else:
                    self.screen.blit(self.textures[1], (self.x, self.y - SCREEN_SIZE[1]))


