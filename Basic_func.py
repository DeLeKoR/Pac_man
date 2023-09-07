from Setting import dir_select_cells

def get_cell(cords, cells):
    """находит клетку по пикселям(которые не пиксели)"""
    for cell in cells:
        if cell.rect.collidepoint(cords):
            return cell


def get_cell_by_cord(cords, cells):
    """находит клетку по её кординатам"""
    for cell in cells:
        if cell.cord == cords:
            return cell
        
def check_cell(cords):
    """Проверяет является ли клетка местом, где призраку нужно сделать выбор в какую сторону пойти"""
    if cords[1] in dir_select_cells.keys():
            if cords[0] in dir_select_cells[cords[1]]:
                return True
    return False