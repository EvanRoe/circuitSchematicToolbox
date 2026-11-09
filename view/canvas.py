"""
@file canvas.py
@brief Creates the canvas for the circuit.
@author Evan Roe
@date 2026-10-03
"""
import tkinter as tk

from model.circuit import Circuit
from model.component import Component
from model.attributes import GridPoint
from model.wire import WireSegment
from model.nets import junction_points

CELL_PX = 20
MARGIN_PX = 20
WIRE_WIDTH_PX = 2
JUNCTION_RADIUS_PX = 4
TERMINAL_RADIUS_PX = 3

GRID_COLOUR = '#d9d9d9'
SYMBOL_COLOUR = '#000000'
BACKGROUND_COLOUR = '#ffffff'
GHOST_COLOUR = '#3399ff'


class CircuitCanvas(tk.Canvas):
    """Represents the tkinter canvas that the circuit sits on."""
    def __init__(self, parent: tk.Tk, circuit: Circuit, width: int=800, height: int=600, cell_px: int=CELL_PX) -> None:
        """Constructs a CircuitCanvas on its parent, which includes the circuit."""
        super().__init__(parent, width=width, height=height, bg=BACKGROUND_COLOUR)
        self.width = width
        self.height = height
        self.cell_px = cell_px
        self.circuit = circuit

        self._draw_grid()
        self._build_readout()


    def grid_to_pixel(self, row: float, col: float) -> tuple[float, float]:
        """Returns the pixel location given the grid location."""
        x = col * self.cell_px +  MARGIN_PX
        y = row * self.cell_px + MARGIN_PX
        return (x, y)

    def pixel_to_grid(self, x: float, y: float) -> GridPoint:
        """Returns the grid location given the pixel location."""
        row = round((y - MARGIN_PX) / self.cell_px)
        col = round((x - MARGIN_PX) / self.cell_px)
        return GridPoint(row=row, col=col)

    def _build_readout(self) -> None:
        """Builds the mouse location readout in the bottom left of the canvas."""
        rows = (self.height - 2 * MARGIN_PX) // self.cell_px
        x1, y1 = self.grid_to_pixel(rows - 1, 0)
        x2, y2 = self.grid_to_pixel(rows, 5)
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
        """Draws the grid on the canvas."""
        rows = (self.height - 2 * MARGIN_PX) // self.cell_px
        cols = (self.width - 2 * MARGIN_PX) // self.cell_px
        

        for c in range(cols + 1):
            x1, y1 = self.grid_to_pixel(0, c)
            x2, y2 = self.grid_to_pixel(rows, c)
            self.create_line(x1, y1, x2, y2, fill=GRID_COLOUR, tags='grid')
        for r in range(rows + 1):
            x1, y1 = self.grid_to_pixel(r, 0)
            x2, y2 = self.grid_to_pixel(r, cols)
            self.create_line(x1, y1, x2, y2, fill=GRID_COLOUR, tags='grid')

    def draw_shapes(self, shapes: list[tuple], position: GridPoint, colour: str=SYMBOL_COLOUR) -> None:
        """Draws the shapes given as a list of tuples and the position."""
        for kind, sx1, sy1, sx2, sy2 in shapes:
            x1, y1 = self.grid_to_pixel(position.row + sy1, position.col + sx1)
            x2, y2 = self.grid_to_pixel(position.row + sy2, position.col + sx2)

            if kind == 'line':
                self.create_line(x1, y1, x2, y2, fill=colour, tags='symbol')
            elif kind == 'rect':
                self.create_rectangle(x1, y1, x2, y2, outline=colour, tags='symbol')

    def draw_component(self, component: Component) -> None:
        """Calls the different draw methods to draw the given component."""
        self._draw_symbol(component)
        self._draw_terminals(component)
        self._draw_label(component)

    def _draw_symbol(self, component: Component) -> None:
        """Calls the draw_shapes() method using the given component."""
        self.draw_shapes(component.symbol_shapes(), component.position)

    def _draw_terminals(self, component: Component) -> None:
        """Draws the terminals of the given component."""
        for _, point in component.get_terminal_positions().items():
            x, y = self.grid_to_pixel(point.row, point.col)
            self.create_oval(
                x - TERMINAL_RADIUS_PX,
                y - TERMINAL_RADIUS_PX,
                x + TERMINAL_RADIUS_PX,
                y + TERMINAL_RADIUS_PX,
                fill=SYMBOL_COLOUR,
                tags=('symbol', 'terminal')
                )

    def _draw_label(self, component: Component) -> None:
        """Depicts the label of the given component."""
        x, y = self.grid_to_pixel(component.position.row - 0.8, component.position.col)
        self.create_text(x, y, text=component.label.text, tags='symbol')

    def draw_wire(self, wire: WireSegment) -> None:
        """Draws a wire segment."""
        x1, y1 = self.grid_to_pixel(row=wire.start.row, col=wire.start.col)
        x2, y2 = self.grid_to_pixel(row=wire.end.row, col=wire.end.col)
        self.create_line(x1, y1, x2, y2, width=WIRE_WIDTH_PX, fill=SYMBOL_COLOUR, tags=('symbol', 'wire'))

    def _draw_junctions(self) -> None:
        """Draws a dot at every junction."""
        junctions = junction_points(self.circuit)
        for junction in junctions:
            x, y = self.grid_to_pixel(row=junction.row, col=junction.col)
            self.create_oval(
                x - JUNCTION_RADIUS_PX,
                y - JUNCTION_RADIUS_PX,
                x + JUNCTION_RADIUS_PX,
                y + JUNCTION_RADIUS_PX,
                fill=SYMBOL_COLOUR,
                tags=('symbol', 'junction'),
                )

    def draw_ghost_wires(self, pairs: list[tuple[GridPoint, GridPoint]]) -> None:
        """Shows a temporary preview of the wire placement to be added."""
        self.clear_ghost()
        for start, end in pairs:
            x1, y1 = self.grid_to_pixel(start.row, start.col)
            x2, y2 = self.grid_to_pixel(end.row, end.col)
            self.create_line(
                x1, y1, x2, y2, fill=GHOST_COLOUR, dash=(4, 2), width=WIRE_WIDTH_PX, tags='ghost')

    def clear_ghost(self) -> None:
        """Clears the ghost preview."""
        self.delete('ghost')


    def redraw(self) -> None:
        """Redraws the circuit after a change."""
        self.clear()
        for wire in self.circuit.wires.values():
            self.draw_wire(wire)
        for component in self.circuit.components.values():
            self.draw_component(component)
        self._draw_junctions()
        self.tag_raise('readout')


    def clear(self) -> None:
        """Clears the components off the canvas."""
        self.delete('symbol')


if __name__ == "__main__":
    pass