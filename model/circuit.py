from model.component import Component, COMPONENT_REGISTRY
from model.node import Node
from model.attributes import GridPoint, Label

class Circuit():
    def __init__(self, components: dict[str, Component]=None, nodes: dict[str, Node]=None) -> None:
        self.components = components if components is not None else {}
        self.nodes = nodes if nodes is not None else {}
        self.counter = {}

    def add_component(self, kind: str, position: GridPoint) -> Component:
        self.counter[kind] = self.counter.get(kind, 0) + 1

        prefix = COMPONENT_REGISTRY[kind].prefix
        name = f'{prefix}{self.counter[kind]}'
        comp_unit = COMPONENT_REGISTRY[kind].default_unit
        new_label = Label(text=name, unit=comp_unit)
        
        new_component = COMPONENT_REGISTRY[kind](name, new_label, position)
        self.components[name] = new_component
        return new_component

    def remove_component(self, gone_id: int) -> None:
        del self.components[gone_id]

    def insert_component(self, component: Component) -> None:
        self.components[component.id] = component

    def add_node(self, new_node: Node) -> None:
        self.nodes.append(new_node)

    def connect_terminal(self) -> None:
        pass

    def component_at(self, point: GridPoint) -> Component | None:
        for component in self.components.values():
            points = component.get_terminal_positions().values()
            cols = [p.col for p in points]
            rows = [p.row for p in points]
            if min(cols) <= point.col <= max(cols) and min(rows) <= point.row <= max(rows):
                return component
        return None

    def terminal_at(self, point: GridPoint) -> tuple[Component, str] | None:
        for component in self.components.values():
            for name, terminal in component.get_terminal_positions().items():
                if point == terminal:
                    return (component, name)
        return None
            


    def to_netlist(self) -> str:
        netlist = ""
        for component in self.components:
            netlist = netlist + component.to_netlist_entry() + "\n"
        return netlist


if __name__ == "__main__":
    lab = Label()
    pos = GridPoint(3, 6)
    comp = COMPONENT_REGISTRY['resistor'](1, lab, pos)
    comps = {'R1': comp}
    circ = Circuit(components=comps)
    pos2 = GridPoint(8, 8)
    pos3 = GridPoint(10, 10)
    circ.add_component('resistor', pos2)
    circ.add_component('capacitor', pos3)
    pos4 = GridPoint(9, 10)
    circ.terminal_at(pos4)