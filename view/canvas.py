import tkinter as tk
from tkinter import ttk

from model.circuit import Circuit
from model.attributes import GridPoint

CELL_PX = 20
MARGIN_PX = 20

GRID_COLOUR = '#d9d9d9'
SYMBOL_COLOUR = '#000000'
BACKGROUND_COLOUR = '#ffffff'

RESISTOR_SHAPES = [
    ('line', -2.0, 0.0, -1.0, 0.0),
    ('rect', -1.0, -0.4, 1.0, 0.4),
    ('line', 1.0, 0.0, 2.0, 0.0),
]

CAPACITOR_SHAPES = [
    ('line', -2.0, 0.0, -1.0, 0.0),
    ('line', -1.0, -0.5, -1.0, 0.5),
    ('line', 0.0, -0.5, 0.0, 0.5),
    ('line', 0.0, 0.0, 1.0, 0.0),
]


SHAPES = {
    'resistor': RESISTOR_SHAPES,
    'capacitor': CAPACITOR_SHAPES,
}

class CircuitCanvas(tk.Canvas):
    def __init__(self, parent: tk.Tk, circuit: Circuit, width: int=800, height: int=600, cell_px: int=CELL_PX) -> None:
        super().__init__(parent, width=width, height=height, bg=BACKGROUND_COLOUR)
        self.width = width
        self.height = height
        self.cell_px = cell_px
        self.circuit = circuit
        
        self.bind('<Motion>', self.on_motion)
        self.bind('<Button-1>', self.on_click)

        self._draw_grid()
        self._build_readout()

        

    def grid_to_pixel(self, col: float, row: float) -> tuple[int, int]:
        x = col * self.cell_px +  MARGIN_PX
        y = row * self.cell_px + MARGIN_PX
        return (x, y)

    def pixel_to_grid(self, x: int, y: int) -> tuple[int, int]:
        col = round((x - MARGIN_PX) / self.cell_px)
        row = round((y - MARGIN_PX) / self.cell_px)
        return (col, row)

    def _build_readout(self) -> None:
        rows = (self.height - 2 * MARGIN_PX) // self.cell_px
        x1, y1 = self.grid_to_pixel(0, rows - 1)
        x2, y2 = self.grid_to_pixel(4, rows)
        self.create_rectangle(
            x1, y1, x2, y2,
            fill='#cce5ff',
            outline=SYMBOL_COLOUR,
            tags='readout',
        )
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        self.readout_text = self.create_text(
            cx, cy,
            tags='readout',
            anchor='center',
        )

    def _draw_grid(self) -> None:
        cols = (self.width - 2 * MARGIN_PX) // self.cell_px
        rows = (self.height - 2 * MARGIN_PX) // self.cell_px

        for c in range(cols + 1):
            x1, y1 = self.grid_to_pixel(c, 0)
            x2, y2 = self.grid_to_pixel(c, rows)
            self.create_line(x1, y1, x2, y2, fill=GRID_COLOUR, tags='grid')
        for r in range(rows + 1):
            x1, y1 = self.grid_to_pixel(0, r)
            x2, y2 = self.grid_to_pixel(cols, r)
            self.create_line(x1, y1, x2, y2, fill=GRID_COLOUR, tags='grid')

    def draw_shapes(self, shapes: list[tuple], position: GridPoint, colour: str=SYMBOL_COLOUR) -> None:
        for kind, sx1, sy1, sx2, sy2 in shapes:
            x1, y1 = self.grid_to_pixel(position.col + sx1, position.row + sy1)
            x2, y2 = self.grid_to_pixel(position.col + sx2, position.row + sy2)
            
            if kind == 'line':
                self.create_line(x1, y1, x2, y2, fill=colour, tags='symbol')
            elif kind == 'rect':
                self.create_rectangle(x1, y1, x2, y2, outline=colour, tags='symbol')

    def redraw(self) -> None:
        self.clear()
        for component in self.circuit.components.values():
            self.draw_shapes(SHAPES[component.kind], component.position)
        self.tag_raise('readout')

    def on_motion(self, event: tk.Event) -> None:
        col, row = self.pixel_to_grid(event.x, event.y)
        self.itemconfig(self.readout_text, text=f"col:{col}, row:{row}")

    def on_click(self, event: tk.Event) -> None:
        col, row = self.pixel_to_grid(event.x, event.y)
        self.circuit.add_component('resistor', GridPoint(col, row))
        print(self.circuit.components)
        if self.circuit.counter['resistor'] == 5:
            self.circuit.remove_component('R2')
        self.redraw()

    def clear(self) -> None:
        self.delete('symbol')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Circuit Schematic Toolbox")

    canvas = CircuitCanvas(root)
    canvas.pack(pady=10)
    canvas.draw_shapes(RESISTOR_SHAPES, 5, 5)
    canvas.draw_shapes(CAPACITOR_SHAPES, 10, 10)
    root.mainloop()