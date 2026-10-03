from abc import ABC, abstractmethod

from model.attributes import GridPoint
from model.circuit import Circuit

class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...


class AddComponentCommand(Command):
    def __init__(self, circuit: Circuit, kind: str, position: GridPoint) -> None:
        self.circuit = circuit
        self.kind = kind
        self.position = position
        self.component = None

    def execute(self) -> None:
        if self.component is None:
            self.component = self.circuit.add_component(self.kind, self.position)
        else:
            self.circuit.insert_component(self.component)


    def undo(self) -> None:
        if self.component is not None:
            self.circuit.remove_component(self.component.id)




class RemoveComponentCommand(Command):
    def __init__(self, circuit: Circuit, component_id: str) -> None:
        self.circuit = circuit
        self.component_id = component_id
        self.component = None

    def execute(self) -> None:
        self.component = self.circuit.components[self.component_id]
        self.circuit.remove_component(self.component_id)

    def undo(self) -> None:
        if self.component is not None:
            self.circuit.insert_component(self.component)