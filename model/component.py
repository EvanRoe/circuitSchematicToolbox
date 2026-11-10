"""
@file component.py
@brief Defines the component class.
@author Evan Roe
@date 2026-10-03
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from model.attributes import Label, GridPoint, Orientation, Terminal, rotate_offset

class Component(ABC):
    """The base class for all components."""
    kind: str
    display_name: str
    prefix: str
    default_unit: str
    default_value: int = 0

    def __init__(self, id: str, label: Label, position: GridPoint, orientation: Orientation = Orientation.DEGREE_0):
        """Constructs a Component with its id, label, position, and orientation."""
        self.id = id
        self.label = label
        self.position = position
        self.orientation = orientation
        self.terminals: list[Terminal]

    def get_terminal_positions(self) -> dict[str, GridPoint]:
        """Returns the terminal positions of this component."""
        terminal_positions = {}
        comp_x = self.position.col
        comp_y = self.position.row

        for term in self.terminals:
            row_rot, col_rot = rotate_offset(term.row_offset, term.col_offset, self.orientation)
            positions = GridPoint(row=round(comp_y + row_rot), col=round(comp_x + col_rot))
            terminal_positions[term.name] = positions
        return terminal_positions

    def rotated_shapes(self) -> list[tuple]:
        """Rotates the symbol_shapes() to the component's Orientation."""
        shapes = self.symbol_shapes()
        new_shapes = []
        for shape in shapes:
            kind, x1, y1, x2, y2 = shape
            y1_rot, x1_rot = rotate_offset(y1, x1, self.orientation)
            y2_rot, x2_rot = rotate_offset(y2, x2, self.orientation)
            new_shapes.append((kind, x1_rot, y1_rot, x2_rot, y2_rot))
        return new_shapes

    def to_dict(self) -> dict:
        """Converts the Component into a dict for saving and loading."""
        data = {
            'id': self.id,
            'kind': self.kind,
            'position': self.position.to_dict(),
            'orientation': self.orientation,
            'label': self.label.to_dict(),
        }
        return data

    @staticmethod
    def from_dict(data: dict) -> Component:
        """Returns the specific Component from the saved dict."""
        cls = COMPONENT_REGISTRY[data['kind']]
        return cls(
            id=data['id'],
            label=Label.from_dict(data['label']),
            position=GridPoint.from_dict(data['position']),
            orientation=Orientation(data['orientation']),
            )

    @abstractmethod
    def symbol_shapes(self) -> list[tuple]:
        ...




class Resistor(Component):
    """Represents an electrical resistor."""
    kind = 'resistor'
    display_name = 'Resistor'
    prefix = 'R'
    default_unit = 'Ω'

    def __init__(self, id: str, label: Label, position: GridPoint, orientation: Orientation = Orientation.DEGREE_0):
        """Constructs a Resistor using its id, label, position, and orientation."""
        super().__init__(id, label, position, orientation)
        self.terminals = [Terminal(name="left", row_offset=0, col_offset=-2), Terminal(name="right", row_offset=0, col_offset=2)]

    def symbol_shapes(self):
        """Holds the component shapes to draw it."""
        resistor_shapes = [
            ('line', -2.0, 0.0, -1.0, 0.0),
            ('rect', -1.0, -0.4, 1.0, 0.4),
            ('line', 1.0, 0.0, 2.0, 0.0),
        ]
        return resistor_shapes

class Capacitor(Component):
    """Represents an electrical capacitor."""
    kind = 'capacitor'
    display_name = 'Capacitor'
    prefix = 'C'
    default_unit = 'F'

    def __init__(self, id: str, label: Label, position: GridPoint, orientation: Orientation = Orientation.DEGREE_0):
        """Constructs a Capacitor using its id, label, position, and orientation."""
        super().__init__(id, label, position, orientation)
        self.terminals = [Terminal(name="pos", row_offset=0, col_offset=-1), Terminal(name="neg", row_offset=0, col_offset=1)]

    def symbol_shapes(self):
        """Holds the component shapes to draw it."""
        capacitor_shapes = [
            ('line', -1.0, 0.0, -0.2, 0.0),
            ('line', -0.2, -0.5, -0.2, 0.5),
            ('line', 0.2, -0.5, 0.2, 0.5),
            ('line', 0.2, 0.0, 1.0, 0.0),
        ]
        return capacitor_shapes


COMPONENT_REGISTRY: dict[str, type[Component]] = {
    'resistor': Resistor,
    'capacitor': Capacitor,
}

