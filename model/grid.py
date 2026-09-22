GRID_CELL_WIDTH = 20
GRID_CELL_HEIGHT = 20
CANVAS_OFFSET_X = 50
CANVAS_OFFSET_Y = 50
GRID_UNIT_SIZE = 1.0 # cm in CircuiTikz

def grid_to_pixel(col: int, row: int) -> tuple[int, int]:
    pixel_x = col * GRID_CELL_WIDTH + CANVAS_OFFSET_X
    pixel_y = row * GRID_CELL_HEIGHT + CANVAS_OFFSET_Y
    return (pixel_x, pixel_y)

def pixel_to_grid(pixel_x: int, pixel_y: int) -> tuple[int, int]:
    col = (pixel_x - CANVAS_OFFSET_X) / GRID_CELL_WIDTH
    row = (pixel_y - CANVAS_OFFSET_Y) / GRID_CELL_HEIGHT
    return (col, row)

def grid_to_circuitikz(col: int, row: int) -> tuple[int, int]:
    pass