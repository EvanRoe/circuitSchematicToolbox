from model.component import Component
from model.node import Node

class Circuit():
    def __init__(self, components: list[Component], nodes: list[Node], counters: int):
        self.components = components
        self.nodes = nodes
        self.counters = counters

    def add_component(self, new_component: Component):
        self.components.append(new_component)

    def remove_component(self, gone_component: Component):
        self.components.remove(gone_component)

    def add_node(self, new_node: Node):
        self.nodes.append(new_node)

    def connect_terminal(self):
        pass

    def to_netlist(self) -> str:
        netlist = ""
        for component in self.components:
            netlist = netlist + component.to_netlist_entry + "\n"
        return netlist

    