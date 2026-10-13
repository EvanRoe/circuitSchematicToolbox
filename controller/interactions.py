"""
@file interactions.py
@brief User interactions with the GUI.
@author Evan Roe
@date 2026-10-03
"""
import tkinter as tk


from controller.commands import AddComponentCommand, RemoveComponentCommand, AddWireCommand, SplitWireCommand, CompositeCommand
from controller.stack import CommandStack
from view.canvas import CircuitCanvas
from model.wire import WireSegment, route_l
from model.circuit import Circuit
from model.attributes import GridPoint

class InteractionController:
    """The controller that binds the interactions and runs the commands."""
    def __init__(self, circuit: Circuit, stack: CommandStack, canvas: CircuitCanvas) -> None:
        """Constructs an InteractionController using the circuit, the command stack, and the GUI canvas."""
        self.circuit = circuit
        self.stack = stack
        self.canvas = canvas

        self.armed_kind: str | None = None
        self.wire_start: GridPoint | None = None
        self.is_horizontal: bool | None = None

        self.canvas.bind('<Motion>', self.on_motion)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Button-3>', self.on_right_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

    def on_motion(self, event: tk.Event) -> None:
        """On mouse motion, updates the location of the mouse in the canvas grid."""
        point = self.canvas.pixel_to_grid(event.x, event.y)
        self._update_readout(point)

    def on_click(self, event: tk.Event) -> None:
        """On left click, either start a wire or place the armed component."""
        if self.armed_kind is None:
            return
        point = self.canvas.pixel_to_grid(event.x, event.y)
        if self.armed_kind == WireSegment.kind:
            self.wire_start = point
            return
        self.stack.execute(AddComponentCommand(self.circuit, self.armed_kind, point))
        self.canvas.redraw()

    def _update_readout(self, point: GridPoint) -> None:
        """Helper function to update the mouse location readout."""
        self.canvas.itemconfig(self.canvas.readout_text, text=f"row:{point.row}, col:{point.col}")


    def on_drag(self, event: tk.Event) -> None:
        """Updates the wire ghost preview while mouse drags."""
        point = self.canvas.pixel_to_grid(event.x, event.y)
        self._update_readout(point)
        if self.wire_start is None:
            return
        self.is_horizontal = abs(self.wire_start.row - point.row) <= abs(self.wire_start.col - point.col)
        point_pairs = route_l(self.wire_start, point, self.is_horizontal)
        self.canvas.draw_ghost_wires(point_pairs)

    def on_release(self, event: tk.Event) -> None:
        """After left click release, finish the wire."""
        if self.wire_start is None:
            return
        start = self.wire_start
        self.canvas.clear_ghost()

        end = self.canvas.pixel_to_grid(event.x, event.y)
        self.is_horizontal = abs(start.row - end.row) <= abs(start.col - end.col)
        horizontal = self.is_horizontal

        point_pairs = route_l(self.wire_start, end, horizontal)
        self.wire_start = None
        self.is_horizontal = None

        if point_pairs is None:
            return
        points = {point for pair in point_pairs for point in pair}
        commands = [SplitWireCommand(self.circuit, point) for point in points]
        commands += [AddWireCommand(self.circuit, a, b) for a, b in point_pairs]
        comp_command = CompositeCommand(commands)
        self.stack.execute(comp_command)
        self.canvas.redraw()
        

    def on_right_click(self, event: tk.Event) -> None:
        """On right click, if there is a component there, opens a menu to interact with the component."""
        point = self.canvas.pixel_to_grid(event.x, event.y)
        component = self.circuit.component_at(point)
        if component is not None:
            menu = tk.Menu(self.canvas, tearoff=0)
            menu.add_command(label='Remove', command= lambda: self.remove(component.id))
            menu.tk_popup(event.x_root, event.y_root)

    def remove(self, component_id: str) -> None:
        """Helper function in the right click menu to remove a component."""
        self.stack.execute(RemoveComponentCommand(self.circuit, component_id))
        self.canvas.redraw()

    def cancel(self, event=None) -> None:
        """Escape: Abandon the drag in progress and disarm."""
        self.canvas.clear_ghost()
        self.wire_start = None
        self.is_horizontal = None
        self.armed_kind = None
        self.canvas.config(cursor='')