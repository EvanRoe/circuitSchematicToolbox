from abc import ABC, abstractmethod

from model.attributes import Label, GridPoint, Orientation, Terminal

class Component(ABC):
    def __init__(self, id: int, label: Label, position: GridPoint, orientation: Orientation = Orientation.DEGREE_0):
        self.id = id
        self.label = label
        self.position = position
        self.orientation = orientation
        self.terminals: list[Terminal]

    def get_terminal_positions(self) -> dict[str, GridPoint]:
        terminal_positions = {}
        comp_x = self.position.col
        comp_y = self.position.row

        for term in self.terminals:
            positions = GridPoint(comp_x + term.col_offset, comp_y + term.row_offset)
            terminal_positions[term.name] = positions
        return terminal_positions

    @abstractmethod
    def symbol_shapes(self) -> list[tuple]:
        ...

    @abstractmethod
    def to_netlist_entry(self) -> str:
        ...



class Resistor(Component):
    kind = 'resistor'
    prefix = 'R'
    default_unit = 'Ω'
    display_name = 'Resistor'

    def __init__(self, id, label, position, orientation = Orientation.DEGREE_0):
        super().__init__(id, label, position, orientation)
        self.terminals = [Terminal("left", -2, 0), Terminal("right", 2, 0)]


    def symbol_shapes(self):
        resistor_shapes = [
            ('line', -2.0, 0.0, -1.0, 0.0),
            ('rect', -1.0, -0.4, 1.0, 0.4),
            ('line', 1.0, 0.0, 2.0, 0.0),
        ]
        return resistor_shapes

    def to_netlist_entry(self):
        entry = f"R{self.id} {self.label.value}{self.label.unit}"
        return entry

class Capacitor(Component):
    kind = 'capacitor'
    prefix = 'C'
    default_unit = 'F'
    display_name = 'Capacitor'

    def __init__(self, id, label, position, orientation = Orientation.DEGREE_0):
        super().__init__(id, label, position, orientation)
        self.terminals = [Terminal("pos", -1, 0), Terminal("neg", 1, 0)]


    def symbol_shapes(self):
        capacitor_shapes = [
            ('line', -1.0, 0.0, -0.2, 0.0),
            ('line', -0.2, -0.5, -0.2, 0.5),
            ('line', 0.2, -0.5, 0.2, 0.5),
            ('line', 0.2, 0.0, 1.0, 0.0),
        ]
        return capacitor_shapes

    def to_netlist_entry(self):
            entry = f"C{self.id} {self.label.value}{self.label.unit}"
            return entry


COMPONENT_REGISTRY = {
    'resistor': Resistor,
    'capacitor': Capacitor,
}

