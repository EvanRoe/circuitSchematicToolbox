"""
@file interactions.py
@brief User interactions with the GUI.
@author Evan Roe
@date 2026-10-03
"""
import tkinter as tk

from model.circuit import Circuit
from controller.commands import AddComponentCommand, RemoveComponentCommand
from controller.stack import CommandStack
from view.canvas import CircuitCanvas
from model.attributes import GridPoint

class InteractionController:
    """The controller that binds the interactions and runs the commands."""
    def __init__(self, circuit: Circuit, stack: CommandStack, canvas: CircuitCanvas) -> None:
        """Constructs an InteractionController using the circuit, the command stack, and the GUI canvas."""
        self.circuit = circuit
        self.stack = stack
        self.canvas = canvas

        self.armed_kind = ''

        self.canvas.bind('<Motion>', self.on_motion)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Button-3>', self.on_right_click)


    def on_motion(self, event: tk.Event) -> None:
        """On mouse motion, updates the location of the mouse in the canvas grid."""
        col, row = self.canvas.pixel_to_grid(event.x, event.y)
        self.canvas.itemconfig(self.canvas.readout_text, text=f"col:{col}, row:{row}")

    def on_click(self, event: tk.Event) -> None:
        """On left click, adds the chosen component to the canvas at that click location."""
        if self.armed_kind == '':
            return
        col, row = self.canvas.pixel_to_grid(event.x, event.y)
        self.stack.execute(AddComponentCommand(self.circuit, self.armed_kind, GridPoint(col, row)))
        self.canvas.redraw()

    def on_right_click(self, event: tk.Event) -> None:
        """On right click, if there is a component there, opens a menu to interact with the component."""
        col, row = self.canvas.pixel_to_grid(event.x, event.y)
        component = self.circuit.component_at(GridPoint(col, row))
        if component is not None:
            menu = tk.Menu(self.canvas, tearoff=0)
            menu.add_command(label='Remove', command= lambda: self.remove(component.id))
            menu.tk_popup(event.x_root, event.y_root)

    def remove(self, component_id: str) -> None:
        """Helper function in the right click menu to remove a component."""
        self.stack.execute(RemoveComponentCommand(self.circuit, component_id))
        self.canvas.redraw()