from Setting import *

class Number(pg.sprite.Sprite):
    def __init__(self, cell, value=None):
        super().__init__()
        self.color = (153, 217, 140)
        font = pg.font.Font("Fonts/pixel-cyr-normal.ttf", 22)
        if value is None:
            if cell.point is not None:
                self.value = cell.point.value
            elif cell.meal is not None:
                self.value = cell.meal.value
        else:
            self.value = value
        self.text = font.render(f'{self.value}', True, self.color)
        self.rect = self.text.get_rect()
        self.rect.center = cell.rect.center
        self.cord = (cell.rect.centerx - self.rect.width/2, cell.rect.centery - self.rect.height/2)
        self.alfa = 254
        self.offset = 0

    def draw(self, surface_map):
        surface_map.blit(self.text, (self.cord[0], self.cord[1]-self.offset))
        self.offset += 0.4
        self.text.set_alpha(self.alfa)
        self.alfa -= 5
