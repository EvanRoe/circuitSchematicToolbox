from dataclasses import dataclass, field

from model.attributes import GridPoint
from model.circuit import Circuit

class UnionFind:
    """Disjoint-set structure over GridPoints."""
    def __init__(self) -> None:
        """Constructs a UnionFind and initialises the parent dict."""
        self._parent: dict[GridPoint, GridPoint] = {}

    def add(self, point: GridPoint) -> None:
        """Add point to _parent with itself as its own parent."""
        if point not in self._parent:
            self._parent[point] = point


    def find(self, point: GridPoint) -> GridPoint:
        """Find root of _parent from a starting point, and return the root."""
        while self._parent[point] != point:
            point = self._parent[point]
        return point
        

    def union(self, a: GridPoint, b: GridPoint) -> None:
        """Find both roots and if different, point root of b to root of a."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a != root_b:
            self._parent[root_b] = root_a

    @property
    def points(self) -> set[GridPoint]:
        """Returns the set of GridPoints added to the UnionFind."""
        return set(self._parent)



@dataclass
class Net:
    """One set of electrically connected points that is only derived, not stored."""
    points: set[GridPoint] = field(default_factory=set)
    terminals: set[tuple[str, str]] = field(default_factory=set)
    wire_ids: set[str] = field(default_factory=set)


def extract_nets(circuit: Circuit) -> list[Net]:
    uf = UnionFind()
    for component in circuit.components.values():
        terminals = component.get_terminal_positions()
        for terminal in terminals.values():
            uf.add(terminal)

    for wire in circuit.wires.values():
        uf.add(wire.start)
        uf.add(wire.end)
        uf.union(wire.start, wire.end)

    nets: dict[GridPoint, Net] = {}

    for point in uf.points:
        root = uf.find(point)
        net = nets.setdefault(root, Net())
        net.points.add(point)

    for component in circuit.components.values():
        for name, position in component.get_terminal_positions().items():
            root = uf.find(position)
            nets[root].terminals.add((component.id, name))

    for wire in circuit.wires.values():
        root = uf.find(wire.start)
        nets[root].wire_ids.add(wire.id)

    return list(nets.values())