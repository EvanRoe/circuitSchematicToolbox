import tkinter as tk
from tkinter import ttk
from collections.abc import Callable

from model.component import COMPONENT_REGISTRY

class ComponentPalette(ttk.Frame):
    def __init__(self, parent: tk.Misc, on_pick: Callable[[str], None]) -> None:
        super().__init__(parent)
        for kind, cls in COMPONENT_REGISTRY.items():
            ttk.Button(
                self,
                text=cls.display_name,
                command=lambda k=kind: on_pick(k),
            ).pack(fill='x', padx=4, pady=2)