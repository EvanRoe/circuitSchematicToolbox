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
        component_x = self.position.col
        component_y = self.position.row
        for term in self.terminals:
            positions = GridPoint
            positions.col = component_x + term.col_offset
            positions.row = component_y + term.row_offset
            terminal_positions[term.name] = positions

    @abstractmethod
    def to_netlist_entry() -> str:
        ...

            


class Resistor(Component):
    def __init__(self, id, label, position, orientation = Orientation.DEGREE_0):
        super().__init__(id, label, position)
        self.terminals = [Terminal("left", -2, 0), Terminal("right", 2, 0)]

    def get_terminal_positions(self):
        return super().get_terminal_positions()

    def to_netlist_entry(self):
        entry = "R" + self.id + " " + self.label.value + self.label.unit
        return entry

class VoltageSource(Component):
    def __init__(self, id, label, position, orientation = Orientation.DEGREE_0):
        super().__init__(id, label, position)
        self.terminals = [Terminal("pos", -2, 0), Terminal("neg", 2, 0)]

    def get_terminal_positions(self):
        return super().get_terminal_positions()

    def to_netlist_entry(self):
            entry = "V" + self.id + " " + str(self.label.value) + self.label.unit
            return entry


COMPONENT_REGISTRY = {
    'resistor': Resistor,
    'voltage_source': VoltageSource,
}

