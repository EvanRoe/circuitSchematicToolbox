from model.component import Component, COMPONENT_REGISTRY
from model.node import Node
from model.attributes import GridPoint, Label

class Circuit():
    def __init__(self, components: dict[str, Component]=None, nodes: dict[str, Node]=None) -> None:
        self.components = components if components is not None else {}
        self.nodes = nodes if nodes is not None else {}
        self.counter = {}

    def add_component(self, kind: str, position: GridPoint) -> None:
        self.counter[kind] = self.counter.get(kind, 0) + 1

        prefix = COMPONENT_REGISTRY[kind].prefix
        name = f'{prefix}{self.counter[kind]}'
        comp_unit = COMPONENT_REGISTRY[kind].default_unit
        new_label = Label(text=name, unit=comp_unit)
        
        new_component = COMPONENT_REGISTRY[kind](name, new_label, position)
        self.components[name] = new_component

    def remove_component(self, gone_id: int) -> None:
        del self.components[gone_id]
        

    def add_node(self, new_node: Node) -> None:
        self.nodes.append(new_node)

    def connect_terminal(self) -> None:
        pass

    def to_netlist(self) -> str:
        netlist = ""
        for component in self.components:
            netlist = netlist + component.to_netlist_entry() + "\n"
        return netlist

    