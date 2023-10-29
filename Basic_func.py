from Setting import dir_select_cells, folder_all_ghosts, folder_eyes, folder_scare, GHOST_SIZE
import os
import pygame as pg


def get_cell(cords, cells):
    """Возвращает клетку по пикселям"""
    for cell in cells:
        if cell.rect.collidepoint(cords):
            return cell


def get_cell_by_cord(cords, cells) -> object:
    """Возвращает клетку по её координатам"""
    if 0 > cords[0] <= 28 or 0 > cords[1] <= 31:
        return None
    for cell in cells:
        if cell.cord == cords:
            return cell
        
def check_cell(cords):
    """Проверяет является ли клетка местом, где призраку нужно сделать выбор в какую сторону пойти"""
    if cords[1] in dir_select_cells.keys():
            if cords[0] in dir_select_cells[cords[1]]:
                return True
    return False

def check_number_in_gap(num, gap:tuple):
    if gap[0] <= num < gap[1]:
       return True
    return False

def sing_number(number) -> int:
    """Возвращает -1, 0, 1 в зависимости от знака числа"""
    return 0 if not number else -1 if number < 0 else 1

################################ ФУНКЦИИ ДЛЯ ПРИЗРАКОВ #####################################

def get_name_move(move):
    """Возращает left, right, top, down в зависимости от знака числа"""
    if move[0]:
        return "left" if move[0] < 0 else "right"
    elif move[1]:
        return "top" if move[1] < 0 else "down"
    else:
        return "down"
    
def load_ghost_images(ghost_color):
    """Загрузка всех изображений призрака в словарь"""
    images_ghost = {"down": [], "left": [], "right": [], "top": [], "scare": []}
    folder_ghost = os.path.join(folder_all_ghosts, f"{ghost_color}_ghost") # получаем путь папки, содержащей изображения нужного призрака
    for dir in ("down", "left", "right", "top"):
        for i in range(2):
            img = pg.image.load(os.path.join(folder_ghost, f"{ghost_color}_{dir}_{i}.png"))
            images_ghost[dir].append(pg.transform.scale(img, GHOST_SIZE))
        # загружаем изображения глаз призрака
        img_eyes = pg.image.load(os.path.join(folder_eyes, f"look_{dir}.png"))
        images_ghost[dir].append(pg.transform.scale(img_eyes, GHOST_SIZE))
    # получаем изображения испуганного призрака
    for color in ("blue", "white"):
        for i in range(2):
            img = pg.image.load(os.path.join(folder_scare, f"{color}_scare_{i}.png"))
            images_ghost["scare"].append(pg.transform.scale(img, GHOST_SIZE))
            
    return images_ghost


