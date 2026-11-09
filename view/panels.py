"""
@file panels.py
@brief The display panels for tab buttons.
@author Evan Roe
@date 2026-10-03
"""
import tkinter as tk
from tkinter import ttk
from collections.abc import Callable

from model.component import COMPONENT_REGISTRY
from model.wire import WireSegment

FILE_ACTIONS = [
    ('new', 'New'),
    ('open', 'Open...'),
    ('save', 'Save...'),
]

class FilePanel(ttk.Frame):
    """The file tab in the GUI, listing file options."""
    def __init__(self, parent: tk.Misc, on_pick: Callable[[str], None]) -> None:
        """Constructs a FilePanel on its parents with the buttons calling functions."""
        super().__init__(parent)

        for kind, display_name in FILE_ACTIONS:
            ttk.Button(
                self,
                text=display_name,
                command=lambda k=kind: on_pick(k),
            ).pack(fill='x', padx=4, pady=2)

class ComponentPanel(ttk.Frame):
    """The component tab in the GUI, listing available components to place."""
    def __init__(self, parent: tk.Misc, on_pick: Callable[[str], None]) -> None:
        """Constructs a ComponentPanel on its parent and the button function."""
        super().__init__(parent)
        for kind, cls in COMPONENT_REGISTRY.items():
            ttk.Button(
                self,
                text=cls.display_name,
                command=lambda k=kind: on_pick(k),
            ).pack(fill='x', padx=4, pady=2)
        ttk.Separator(self).pack(fill='x', pady=4)
        ttk.Button(self, text='Wire', command=lambda: on_pick(WireSegment.kind)).pack(fill='x', padx=4, pady=2)

class FavouritesPanel(ttk.Frame):
    """The favourites tab in the GUI, listing saved favourite circuits."""
    def __init__(self, parent: tk.Misc, on_save: Callable[[], None], on_load: Callable[[str], None]) -> None:
        """Constructs a FavouritesPanel on its parent and the buttons call the given functions."""
        super().__init__(parent)
        self.on_load = on_load
        ttk.Button(self, text='Load', command=self._load_selected).pack(
            side='bottom', fill='x', padx=4, pady=(0, 4),
        )
        ttk.Button(self, text='Save current...', command=on_save).pack(
            side='bottom', fill='x', padx=4, pady=4,
        )

        self.listbox = tk.Listbox(self, exportselection=False)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox.pack(side='top', expand=True, fill='both', padx=4, pady=4)
        self.listbox.bind('<Double-Button-1>', lambda event: self._load_selected())
        self.listbox.config(yscrollcommand=scrollbar.set)


    def set_names(self, names: list[str]) -> None:
        """Deletes then sets the names of the favourites."""
        self.listbox.delete(0, tk.END)
        for name in names:
            self.listbox.insert(tk.END, name)

    def _load_selected(self) -> None:
        """Loads the favourite selected from the listbox."""
        row_nums = self.listbox.curselection()
        if not row_nums:
            return
        self.on_load(self.listbox.get(row_nums[0]))
