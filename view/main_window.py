"""
@file main_window.py
@brief The main window of the GUI.
@author Evan Roe
@date 2026-10-03
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from view.canvas import CircuitCanvas
from model.circuit import Circuit
from view.panels import FilePanel, ComponentPanel
from controller.interactions import InteractionController
from controller.stack import CommandStack
from storage.serialisation import load_json, save_json

SIDE_PANEL_WIDTH = 220

TABS = [
    ('file', 'File'),
    ('components', 'Components'),
    ('favourites', 'Favourites'),
]

FILE_TYPES = [
    ('Circuit files', '*.json'),
    ('All files', '*.*'),
]


class MainWindow:
    """Represents the main window of the tkinter GUI."""
    def __init__(self, root: tk.Tk) -> None:
        """Constructs a MainWindow on the tk root."""
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
        root.bind_all('<Control-Z>', self.on_undo)
        root.bind_all('<Control-y>', self.on_redo)
        root.bind_all('<Control-Y>', self.on_redo)


        self.show_panel('file')

    def _build_top_bar(self) -> None:
        """Builds the tab bar of the GUI."""
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
        """Builds the side frame that holds the tabs' contents."""
        self.side_frame = ttk.Frame(self.root, width=SIDE_PANEL_WIDTH)
        self.side_frame.pack(side='right', fill='y')
        self.side_frame.pack_propagate(False)

        self.panels['file'] = FilePanel(
            self.side_frame,
            on_pick=self.on_file_action,
        )
        self.panels['components'] = ComponentPanel(
            self.side_frame,
            on_pick=self.on_component_picked
        )
        self.panels['favourites'] = PlaceholderPanel(
            self.side_frame,
            TABS[2][1],
        )
            

    def _build_canvas(self) -> None:
        """Builds the canvas that holds the grid and circuit."""
        self.canvas = CircuitCanvas(self.root, self.circuit)
        self.canvas.pack(side='left', expand=True, fill='both')

    def show_panel(self, key: str) -> None:
        """Shows the panel based on the clicked/set tab."""
        if self.current_panel is not None:
            self.current_panel.pack_forget()
        self.panels[key].pack(expand=True, fill='both')
        self.current_panel = self.panels[key]

    def on_component_picked(self, kind: str) -> None:
        """Sets the chosen component in the panel."""
        self.controller.armed_kind = kind

    def on_undo(self, event=None) -> None:
        """Runs the undo command through the stack and redraws."""
        self.stack.undo()
        self.canvas.redraw()

    def on_redo(self, event=None) -> None:
        """Runs the redo command through the stack and redraws."""
        self.stack.redo()
        self.canvas.redraw()

    def on_file_action(self, action: str) -> None:
        """Executes the action chosen by the user from the file tab."""
        file_actions = {
            'new': self._new,
            'open': self._open,
            'save': self._save,
        }
        handler = file_actions[action]
        handler()

    def _new(self) -> None:
        """Starts a blank circuit."""
        self.circuit.clear()
        self._reset_editor()

    def _open(self) -> None:
        """Opens a saved schematic file."""
        path = filedialog.askopenfilename(filetypes=FILE_TYPES)
        if not path: return
        try:
            load_json(Path(path), self.circuit)
        except (OSError, ValueError, KeyError) as e:
            messagebox.showerror("Could not open file", str(e))
            return
        self._reset_editor()

    def _save(self) -> None:
        """Saves the current schematic file to disk."""
        path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=FILE_TYPES)
        if not path: return
        try:
            save_json(self.circuit, Path(path))
        except OSError as e:
            messagebox.showerror("Could not save file", str(e))

    def _reset_editor(self) -> None:
        """Called after a circuit clear to reset main editor attributes."""
        self.stack.clear()
        self.canvas.redraw()
        self.controller.armed_kind = ''


class PlaceholderPanel(ttk.Frame):
    def __init__(self, parent: tk.Misc, text: str="") ->  None:
        super().__init__(parent)
        ttk.Label(self, text=text).pack(padx=10, pady=10)

