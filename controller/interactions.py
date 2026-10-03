import tkinter as tk

from model.circuit import Circuit
from controller.commands import AddComponentCommand
from controller.stack import CommandStack
from view.canvas import CircuitCanvas
from model.attributes import GridPoint

class InteractionController:
    def __init__(self, circuit: Circuit, stack: CommandStack, canvas: CircuitCanvas) -> None:
        self.circuit = circuit
        self.stack = stack
        self.canvas = canvas

        self.armed_kind = ''

        self.canvas.bind('<Motion>', self.on_motion)
        self.canvas.bind('<Button-1>', self.on_click)
        #self.canvas.bind('<Button-3>', self.on_right_click)


    def on_motion(self, event: tk.Event) -> None:
        col, row = self.canvas.pixel_to_grid(event.x, event.y)
        self.canvas.itemconfig(self.canvas.readout_text, text=f"col:{col}, row:{row}")

    def on_click(self, event: tk.Event) -> None:
        if self.armed_kind == '':
            return
        col, row = self.canvas.pixel_to_grid(event.x, event.y)
        self.stack.execute(AddComponentCommand(self.circuit, self.armed_kind, GridPoint(col, row)))
        self.canvas.redraw()