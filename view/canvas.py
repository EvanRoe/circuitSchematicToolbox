import tkinter as tk

from model.circuit import Circuit
from model.component import Component
from model.attributes import GridPoint

CELL_PX = 20
MARGIN_PX = 20

GRID_COLOUR = '#d9d9d9'
SYMBOL_COLOUR = '#000000'
BACKGROUND_COLOUR = '#ffffff'


class CircuitCanvas(tk.Canvas):
    def __init__(self, parent: tk.Tk, circuit: Circuit, width: int=800, height: int=600, cell_px: int=CELL_PX) -> None:
        super().__init__(parent, width=width, height=height, bg=BACKGROUND_COLOUR)
        self.width = width
        self.height = height
        self.cell_px = cell_px
        self.circuit = circuit
        self.armed_kind = ''
        
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

    def draw_component(self, component: Component) -> None:
        self._draw_symbol(component)
        self._draw_terminals(component)
        self._draw_label(component)

    def _draw_symbol(self, component: Component) -> None:
        self.draw_shapes(component.symbol_shapes(), component.position)

    def _draw_terminals(self, component: Component) -> None:
        for _, point in component.get_terminal_positions().items():
            x, y = self.grid_to_pixel(point.col, point.row)
            r = 3
            self.create_oval(x - r, y - r, x + r, y + r, fill=SYMBOL_COLOUR, tags=('symbol', 'terminal'))

    def _draw_label(self, component: Component) -> None:
        x, y = self.grid_to_pixel(component.position.col, component.position.row - 0.8)
        self.create_text(x, y, text=component.label.text, tags='symbol')


    def redraw(self) -> None:
        self.clear()
        for component in self.circuit.components.values():
            self.draw_component(component)
        self.tag_raise('readout')

    def on_motion(self, event: tk.Event) -> None:
        col, row = self.pixel_to_grid(event.x, event.y)
        self.itemconfig(self.readout_text, text=f"col:{col}, row:{row}")

    def on_click(self, event: tk.Event) -> None:
        if self.armed_kind == '':
            return
        col, row = self.pixel_to_grid(event.x, event.y)
        self.circuit.add_component(self.armed_kind, GridPoint(col, row))
        self.redraw()

    def clear(self) -> None:
        self.delete('symbol')


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Circuit Schematic Toolbox")

    canvas = CircuitCanvas(root)
    canvas.pack(pady=10)
    root.mainloop()