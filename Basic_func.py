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