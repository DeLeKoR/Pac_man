def get_cell(cords, cells):
    for cell in cells:
        if cell.rect.collidepoint(cords):
            return cell


def get_cell_by_cord(cords, cells):
    for cell in cells:
        if cell.cord == cords:
            return cell