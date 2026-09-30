import tkinter as tk
from tkinter import ttk

from view.canvas import CircuitCanvas
from model.circuit import Circuit

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

        self.panels = {
            key: PlaceholderPanel(self.side_frame, text=label)
            for key, label in TABS
        }

    def _build_canvas(self) -> None:
        self.canvas = CircuitCanvas(self.root)
        self.canvas.pack(side='left', expand=True, fill='both')

    def show_panel(self, key: str) -> None:
        if self.current_panel is not None:
            self.current_panel.pack_forget()
        self.panels[key].pack(expand=True, fill='both')
        self.current_panel = self.panels[key]

class PlaceholderPanel(ttk.Frame):
    def __init__(self, parent, text=""):
        super().__init__(parent)
        ttk.Label(self, text=text).pack(padx=10, pady=10)



