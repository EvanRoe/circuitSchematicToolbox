"""
@file commands.py
@brief Commands for the GUI.
@author Evan Roe
@date 2026-10-03
"""
from abc import ABC, abstractmethod


from model.attributes import GridPoint
from model.circuit import Circuit


class Command(ABC):
    """The base class for all commands."""
    @abstractmethod
    def execute(self) -> None:
        ...

    @abstractmethod
    def undo(self) -> None:
        ...


class AddComponentCommand(Command):
    """Command that adds a component to the circuit from a kind and position."""
    def __init__(self, circuit: Circuit, kind: str, position: GridPoint) -> None:
        """Construct an AddComponentCommand with the circuit, and kind and position of the component."""
        self.circuit = circuit
        self.kind = kind
        self.position = position
        self.component = None

    def execute(self) -> None:
        """Runs the adding of a component on the circuit and stores it."""
        if self.component is None:
            self.component = self.circuit.add_component(self.kind, self.position)
        else:
            self.circuit.insert_component(self.component)


    def undo(self) -> None:
        """Undoes the command using the stored component from execute()."""
        if self.component is not None:
            self.circuit.remove_component(self.component.id)




class RemoveComponentCommand(Command):
    """Command that removes a component from the circuit from its id."""
    def __init__(self, circuit: Circuit, component_id: str) -> None:
        """Constructs a RemoveComponentCommand with the circuit and the component id."""
        self.circuit = circuit
        self.component_id = component_id
        self.component = None

    def execute(self) -> None:
        """Runs the removing of a component from the circuit and stores it."""
        self.component = self.circuit.components[self.component_id]
        self.circuit.remove_component(self.component_id)

    def undo(self) -> None:
        """Adds the component back to the circuit."""
        if self.component is not None:
            self.circuit.insert_component(self.component)