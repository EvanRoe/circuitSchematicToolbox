import tkinter as tk
from tkinter import ttk

from view.canvas import CircuitCanvas
from model.circuit import Circuit
from view.palette import ComponentPalette
from controller.interactions import InteractionController
from controller.stack import CommandStack

SIDE_PANEL_WIDTH = 220

TABS = [
    ('file', 'File'),
    ('components', 'Components'),
    ('favourites', 'Favourites'),
]


class MainWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.panels = {}
        self.current_panel = None
        self.active_tab = tk.StringVar(value='file')
        ttk.Style().theme_use('clam')

        self.circuit = Circuit()
        self._build_top_bar()
        self._build_side_frame()
        self._build_canvas()

        self.stack = CommandStack()
        self.controller = InteractionController(self.circuit, self.stack, self.canvas)
        root.bind_all('<Control-z>', self.on_undo)
        root.bind_all('<Control-y>', self.on_redo)


        self.show_panel('file')

    def _build_top_bar(self) -> None:
        top_bar = ttk.Frame(self.root)
        top_bar.pack(side='top', fill='x')

        for key, label in TABS:
            tabs_button = ttk.Radiobutton(top_bar,
                                        text=label,
                                        style='Toolbutton',
                                        variable=self.active_tab,
                                        value=key,
                                        command=lambda k=key: self.show_panel(k),
                          )
            tabs_button.pack(side='left')

    def _build_side_frame(self) -> None:
        self.side_frame = ttk.Frame(self.root, width=SIDE_PANEL_WIDTH)
        self.side_frame.pack(side='right', fill='y')
        self.side_frame.pack_propagate(False)

        self.panels['file'] = PlaceholderPanel(
            self.side_frame,
            TABS[0][1],
        )
        self.panels['components'] = ComponentPalette(
            self.side_frame,
            on_pick=self.on_component_picked
        )
        self.panels['favourites'] = PlaceholderPanel(
            self.side_frame,
            TABS[2][1],
        )
            

    def _build_canvas(self) -> None:
        self.canvas = CircuitCanvas(self.root, self.circuit)
        self.canvas.pack(side='left', expand=True, fill='both')

    def show_panel(self, key: str) -> None:
        if self.current_panel is not None:
            self.current_panel.pack_forget()
        self.panels[key].pack(expand=True, fill='both')
        self.current_panel = self.panels[key]

    def on_component_picked(self, kind: str) -> None:
        self.controller.armed_kind = kind

    def on_undo(self, event=None) -> None:
        self.stack.undo()
        self.canvas.redraw()

    def on_redo(self, event=None) -> None:
        self.stack.redo()
        self.canvas.redraw()

class PlaceholderPanel(ttk.Frame):
    def __init__(self, parent: tk.Misc, text: str="") ->  None:
        super().__init__(parent)
        ttk.Label(self, text=text).pack(padx=10, pady=10)

