"""
@file circuit.py
@brief Defines the circuit class.
@author Evan Roe
@date 2026-10-03
"""
from model.component import Component, COMPONENT_REGISTRY
from model.node import Node
from model.attributes import GridPoint, Label

class Circuit():
    """Represents the collection of components."""
    def __init__(self, components: dict[str, Component] | None = None, nodes: dict[str, Node] | None = None) -> None:
        """Construct a Circuit, usually empty to start but can add components and nodes."""
        self.components = components if components is not None else {}
        self.nodes = nodes if nodes is not None else {}
        self.counter = {}

    def add_component(self, kind: str, position: GridPoint) -> Component:
        """Returns the component added using its kind and position, adds it to the counter dict."""
        cls = COMPONENT_REGISTRY[kind]
        self.counter[kind] = self.counter.get(kind, 0) + 1

        prefix = cls.prefix
        name = f'{prefix}{self.counter[kind]}'
        comp_unit = cls.default_unit
        new_label = Label(text=name, value=cls.default_value, unit=comp_unit)
        
        new_component = cls(name, new_label, position)
        self.components[name] = new_component
        return new_component

    def remove_component(self, component_id: str) -> None:
        """Removes the component from the class dict from its id."""
        if component_id not in self.components:
            raise KeyError(f"Component {component_id} does not exist")
        del self.components[component_id]
        

    def insert_component(self, component: Component) -> None:
        """Inserts a component using its id instead of creating a new one."""
        if component.id in self.components:
            raise KeyError(f"Component {component.id} already exists")
        self.components[component.id] = component

    def component_at(self, point: GridPoint) -> Component | None:
        """Returns the component if at the GridPoint position, otherwise None."""
        for component in self.components.values():
            points = component.get_terminal_positions().values()
            cols = [p.col for p in points]
            rows = [p.row for p in points]
            if min(cols) <= point.col <= max(cols) and min(rows) <= point.row <= max(rows):
                return component
        return None

    def terminal_at(self, point: GridPoint) -> tuple[Component, str] | None:
        """Returns the terminal if at the GridPoint position, otherwise None."""
        for component in self.components.values():
            for name, terminal in component.get_terminal_positions().items():
                if point == terminal:
                    return (component, name)
        return None

    def clear(self) -> None:
        self.components.clear()
        self.counter.clear()


    def to_netlist(self) -> str:
        return '\n'.join(c.to_netlist_entry() for c in self.components.values())


if __name__ == "__main__":
    pass