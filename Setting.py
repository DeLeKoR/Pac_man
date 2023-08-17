import pygame as pg
import os

# позволяем ОС самостоятельно выстроить путь к ассетам игры
game_folder = os.path.dirname(__file__)
images_folder = os.path.join(game_folder, "images")

# настройка экрана
SCREEN_SIZE = 800, 800
BG_COLOR = (5, 5, 20)

# настройка пак мана и карты 
PAC_MAN_IMG_PASS = os.path.join(images_folder, "Pac_man.png")
MAP_IMG_PASS = os.path.join(images_folder, "pac_man_map.jpeg")
PAC_MAN_SIZE = (40, 40)

# Настройска призраков
blue_ghost = pg.image.load(os.path.join(images_folder, "blue_ghost.png"))
red_ghost = pg.image.load(os.path.join(images_folder, "red_ghost.png"))
pink_ghost = pg.image.load(os.path.join(images_folder, "pink_ghost.png"))
jelow_ghost = pg.image.load(os.path.join(images_folder, "jelow_ghost.png"))

GHOST_SIZE = (45, 45)

# общие настройки 
SPEED = 3