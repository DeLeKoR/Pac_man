from Setting import *

class Number(pg.sprite.Sprite):
    def __init__(self, obj):
        super().__init__()
        self.color = (153, 217, 140)
        font = pg.font.Font("Fonts/pixel-cyr-normal.ttf", 22)
        if isinstance(obj, object):
            if obj.point is not None:
                self.value = obj.point.value
            elif obj.meal is not None:
                self.value = obj.meal.value
        elif isinstance(obj, int):
            self.value = obj
        self.text = font.render(f'{self.value}', True, self.color)
        self.rect = self.text.get_rect()
        self.rect.center = obj.rect.center
        self.cord = (obj.rect.centerx - self.rect.width / 2, obj.rect.centery - self.rect.height / 2)
        self.alfa = 254
        self.offset = 0

    def draw(self, surface_map):
        surface_map.blit(self.text, (self.cord[0], self.cord[1]-self.offset))
        self.offset += 0.4
        self.text.set_alpha(self.alfa)
        self.alfa -= 5
