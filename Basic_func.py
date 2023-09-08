from Setting import dir_select_cells

def get_cell(cords, cells):
    """Возвращает клетку по пикселям"""
    for cell in cells:
        if cell.rect.collidepoint(cords):
            return cell


def get_cell_by_cord(cords, cells) -> object:
    """Возвращает клетку по её координатам"""
    for cell in cells:
        if cell.cord == cords:
            return cell
        
def check_cell(cords):
    """Проверяет является ли клетка местом, где призраку нужно сделать выбор в какую сторону пойти"""
    if cords[1] in dir_select_cells.keys():
            if cords[0] in dir_select_cells[cords[1]]:
                return True
    return False

def sing_number(number) -> int:
    """Возвращает -1, 0, 1 в зависимости от знака числа"""
    return 0 if not number else -1 if number < 0 else 1
