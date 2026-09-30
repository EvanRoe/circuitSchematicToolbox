from model.component import Component
from model.node import Node

class Circuit():
    def __init__(self, components: list[Component]=None, nodes: list[Node]=None) -> None:
        self.components = components if components is not None else []
        self.nodes = nodes if nodes is not None else []

    def add_component(self, new_component: Component) -> None:
        self.components.append(new_component)

    def remove_component(self, gone_component: Component) -> None:
        self.components.remove(gone_component)

    def add_node(self, new_node: Node) -> None:
        self.nodes.append(new_node)

    def connect_terminal(self) -> None:
        pass

    def to_netlist(self) -> str:
        netlist = ""
        for component in self.components:
            netlist = netlist + component.to_netlist_entry() + "\n"
        return netlist

    