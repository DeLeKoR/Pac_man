import ctypes
import pygame as pg

#размер экрана пользователя
DISPLAY_WIDTH = ctypes.windll.user32.GetSystemMetrics(0)
DISPLAY_HEIGHT = ctypes.windll.user32.GetSystemMetrics(1)

SCREEN_SIZE = (DISPLAY_HEIGHT-DISPLAY_HEIGHT/10, DISPLAY_HEIGHT-DISPLAY_HEIGHT/10)

BG_COLOR = (5, 5, 20)

