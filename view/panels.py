"""
@file palette.py
@brief The component tab in the GUI.
@author Evan Roe
@date 2026-10-03
"""
import tkinter as tk
from tkinter import ttk
from collections.abc import Callable

from model.component import COMPONENT_REGISTRY

FILE_ACTIONS = [
    ('new', 'New'),
    ('open', 'Open...'),
    ('save', 'Save...'),
]

class FilePanel(ttk.Frame):
    """The file tab in the GUI."""
    def __init__(self, parent: tk.Misc, on_pick: Callable[[str], None]) -> None:
        super().__init__(parent)

        for kind, display_name in FILE_ACTIONS:
            ttk.Button(
                self,
                text=display_name,
                command=lambda k=kind: on_pick(k),
            ).pack(fill='x', padx=4, pady=2)

class ComponentPanel(ttk.Frame):
    """The component tab in the GUI."""
    def __init__(self, parent: tk.Misc, on_pick: Callable[[str], None]) -> None:
        """Constructs a ComponentPalette on its parent and the button function."""
        super().__init__(parent)
        for kind, cls in COMPONENT_REGISTRY.items():
            ttk.Button(
                self,
                text=cls.display_name,
                command=lambda k=kind: on_pick(k),
            ).pack(fill='x', padx=4, pady=2)

