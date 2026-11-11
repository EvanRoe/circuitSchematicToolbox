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
        self.terminals = [Terminal(name="a", row_offset=0, col_offset=-1), Terminal(name="b", row_offset=0, col_offset=1)]

    def symbol_shapes(self):
        """Holds the component shapes to draw it."""
        resistor_shapes = [
            ('line', -1.0, 0.0, -0.5, 0.0),
            ('rect', -0.5, -0.3, 0.5, 0.3),
            ('line', 0.5, 0.0, 1.0, 0.0),
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
        self.terminals = [Terminal(name="a", row_offset=0, col_offset=-1), Terminal(name="b", row_offset=0, col_offset=1)]

    def symbol_shapes(self):
        """Holds the component shapes to draw it."""
        capacitor_shapes = [
            ('line', -1.0, 0.0, -0.2, 0.0),
            ('line', -0.2, -0.5, -0.2, 0.5),
            ('line', 0.2, -0.5, 0.2, 0.5),
            ('line', 0.2, 0.0, 1.0, 0.0),
        ]
        return capacitor_shapes

class Inductor(Component):
    """Represents an inductor."""
    kind = 'inductor'
    display_name = 'Inductor'
    prefix = 'L'
    default_unit = 'H'

    def __init__(self, id: str, label: Label, position: GridPoint, orientation: Orientation = Orientation.DEGREE_0):
        """Constructs a Inductor using its id, label, position, and orientation."""
        super().__init__(id, label, position, orientation)
        self.terminals = [Terminal(name="a", row_offset=0, col_offset=-1), Terminal(name="b", row_offset=0, col_offset=1)]

    def symbol_shapes(self):
        """Holds the component shapes to draw it."""
        inductor_shapes = [
            ('line', -1.0, 0.0, -0.5, 0.0),
            ('rect', -0.5, -0.3, 0.5, 0.3),
            ('fillrect', -0.5, -0.3, 0.5, 0.3),
            ('line', 0.5, 0.0, 1.0, 0.0),
        ]
        return inductor_shapes

class VoltageSource(Component):
    """Represents a voltage source."""
    kind = 'voltage_source'
    display_name = 'Voltage Source'
    prefix = 'V'
    default_unit = 'V'

    def __init__(self, id: str, label: Label, position: GridPoint, orientation: Orientation = Orientation.DEGREE_0):
        """Constructs a VoltageSource using its id, label, position, and orientation."""
        super().__init__(id, label, position, orientation)
        self.terminals = [Terminal(name="neg", row_offset=0, col_offset=-1), Terminal(name="pos", row_offset=0, col_offset=1)]

    def symbol_shapes(self):
        """Holds the component shapes to draw it."""
        voltage_source_shapes = [
            ('line', -1.0, 0.0, -0.6, 0.0),
            ('oval', -0.6, -0.6, 0.6, 0.6),
            ('line', -0.48, 0.0, -0.2, 0.0),
            ('line', 0.2, 0.0, 0.48, 0.0),
            ('line', 0.34, 0.14, 0.34, -0.14),
            ('line', 0.6, 0.0, 1.0, 0.0),
        ]
        return voltage_source_shapes 


class CurrentSource(Component):
    """Represents an current source."""
    kind = 'current_source'
    display_name = 'Current Source'
    prefix = 'I'
    default_unit = 'A'

    def __init__(self, id: str, label: Label, position: GridPoint, orientation: Orientation = Orientation.DEGREE_0):
        """Constructs a CurrentSource using its id, label, position, and orientation."""
        super().__init__(id, label, position, orientation)
        self.terminals = [Terminal(name="neg", row_offset=0, col_offset=-1), Terminal(name="pos", row_offset=0, col_offset=1)]

    def symbol_shapes(self):
        """Holds the component shapes to draw it."""
        current_source_shapes = [
            ('line', -1.0, 0.0, -0.6, 0.0),
            ('oval', -0.6, -0.6, 0.6, 0.6),
            ('arrow', -0.4, 0.0, 0.4, 0.0),
            ('line', 0.6, 0.0, 1.0, 0.0),
        ]
        return current_source_shapes 


class Diode(Component):
    """Represents a diode."""
    kind = 'diode'
    display_name = 'Diode'
    prefix = 'D'
    default_unit = ''

    def __init__(self, id: str, label: Label, position: GridPoint, orientation: Orientation = Orientation.DEGREE_0):
        """Constructs a Diode using its id, label, position, and orientation."""
        super().__init__(id, label, position, orientation)
        self.terminals = [Terminal(name="cathode", row_offset=0, col_offset=-1), Terminal(name="anode", row_offset=0, col_offset=1)]

    def symbol_shapes(self):
        """Holds the component shapes to draw it."""
        diode_shapes = [
            ('line', -1.0, 0.0, -0.5, 0.0),
            ('line', -0.5, 0.5, -0.5, -0.5),
            ('line', -0.5, 0.5, 0.5, 0.0),
            ('line', -0.5, -0.5, 0.5, 0.0),
            ('line', 0.5, 0.5, 0.5, -0.5),
            ('line', 0.5, 0.0, 1.0, 0.0),
        ]
        return diode_shapes 

class Ground(Component):
    """Represents ground reference."""
    kind = 'ground'
    display_name = 'Ground'
    prefix = 'GND'
    default_unit = ''

    def __init__(self, id: str, label: Label, position: GridPoint, orientation: Orientation = Orientation.DEGREE_0):
        """Constructs a Ground using its id, label, position, and orientation."""
        super().__init__(id, label, position, orientation)
        self.terminals = [Terminal(name="gnd", row_offset=0, col_offset=0)]

    def symbol_shapes(self):
        """Holds the component shapes to draw it."""
        ground_shapes = [
            ('line', 0.0, 0.0, 0.0, 0.9),
            ('line', -0.9, 0.3, 0.9, 0.3),
            ('line', -0.6, 0.6, 0.6, 0.6),
            ('line', -0.3, 0.9, 0.3, 0.9),
        ]
        return ground_shapes 


COMPONENT_REGISTRY: dict[str, type[Component]] = {
    'resistor': Resistor,
    'capacitor': Capacitor,
    'inductor': Inductor,
    'voltage_source': VoltageSource,
    'current_source': CurrentSource,
    'diode': Diode,
    'ground': Ground,
}

