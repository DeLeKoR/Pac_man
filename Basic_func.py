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

def sing_number(number) -> int:
    """Возвращает -1, 0, 1 в зависимости от знака числа"""
    return 0 if not number else -1 if number < 0 else 1
