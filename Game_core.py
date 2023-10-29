from Setting import *
from Map import *
from Enemies import *
from Pac_man import *
from Basic_func import *
from Information_board import *

class Game:
    def __init__(self, screen, fps: int = 0):
        self.screen = screen
        self.fps = fps
        self.pause = True
        self.lives = [3]
        self.score = [0]
        self.level = 1
        self.map = Map(self.screen)
        self.enemies = pg.sprite.Group()
        self.cord_red = (14, 11)
        self.first_points = len(self.map.points) # кол-во точек на карте в момент, когда призрак активизируется
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells, self.enemies)
        self.create_enemies()
        self.info_board = Information_board(self.screen)

    def draw_frame(self):
        self.map.draw_map()
        self.pac_man.draw_pac_man()
        for enemy in self.enemies:
            enemy.draw_enemy()
        self.info_board.draw_board(self.fps, self.lives, self.level, self.score)

    def create_frame(self):
        if self.map.check_points():
            self.restart(2)
            self.level += 1
        self.pac_man.move()
        self.pac_man.eat_point(self.score, self.map.numbers)
        self.update_ghosts()
        self.map.create_meal()

    def create_enemies(self): 
        for color_type, image, cords, retreat, point_limit, time_limit in zip(ghosts_colors, images_ghosts, cords_ghosts, retreat_cords, points_limit, times_limit):
            all_images = load_ghost_images(color_type)
            group_images = all_images["down"]
            #image = group_images[1]
            cell = get_cell_by_cord(cords, self.map.cells)
            ghost = Ghost(cell, self.map.cells, self.screen, image, group_images, all_images, color_type, retreat, True, self.pac_man, point_limit, time_limit)
            self.enemies.add(ghost)

    def update_ghosts(self):
        for enemy in self.enemies:
            if enemy.color_type in ("blue", "yellow", "pink"):
                enemy.kill()
            if enemy.activity:
                if not enemy.kill_ghost and (enemy.cell.cord == (5, 14) or enemy.cell.cord == (22, 14) or (enemy.future_cell is None and enemy.cell.type == 2)):
                    enemy.ghost_in_tunnel()
                self.pac_man.interaction(self.restart, self.lives, enemy) # проверяем взаимодействие пакмана с призраком
                if enemy.mode_now == "attack":
                    if enemy.color_type == "red":
                        self.cord_red = enemy.cell.cord
                    enemy.count_target_ghosts(self.cord_red)
                elif enemy.mode_now == "scare" and not enemy.kill_ghost and not enemy.ghost_in_house:
                    time_now = pg.time.get_ticks() # получаем текущее время
                    action_time_mode = (time_now - enemy.start_time_mode) / 1000 # находим время действия режима
                    if (enemy.time_mode_scare - action_time_mode) <= 2 and (time_now / 1000 - enemy.start_time_img) >= 0.5:
                        # меняем изображение синего призрака на изображение белого (или наоборот)
                        enemy.list_scare_imgs = enemy.list_scare_imgs[::-1]
                        enemy.image = enemy.list_scare_imgs[0]
                        enemy.start_time_img = time_now / 1000

                elif enemy.kill_ghost and enemy.future_cell is not None and enemy.future_cell.cord == enemy.target:
                    enemy.ghost_in_house = True
                    enemy.target = start_points[0]
                    enemy.move_future = [0, enemy.speed]
                    enemy.move()
                enemy.update()
            else:
                if (self.first_points - len(self.map.points) >= enemy.point_limit) or (pg.time.get_ticks() - self.pac_man.time_eat) / 1000 >= enemy.time_limit: # если кол-во точек, которых съел пакман, превышает лимит, то призрак должен начать двигаться
                    enemy.start_move()
                    enemy.activity = True
                    self.first_points = len(self.map.points)

    def restart(self, ask: int = 0):
        """
        Перезапускает игру
        False = перезапуск призраков и пакмена
        True = полный перезапуск игры
        """
        if ask == 1 or ask == 2:
            self.map = Map(self.screen)
        if ask == 1:
            self.info_board = Information_board(self.screen)
            self.level = 1
            self.score = [0]
            self.lives = [2]
        self.enemies.empty()
        self.cord_red = (14, 11)
        self.first_points = len(self.map.points)
        self.pac_man = Pac_man(get_cell_by_cord((2, 14), self.map.cells), self.screen, self.map.cells, self.enemies)
        self.create_enemies()


