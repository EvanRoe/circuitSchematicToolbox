"""
@file wire.py
@brief Holds the WireSegment class.
@author Evan Roe
@date 2026-10-07
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar

from model.attributes import GridPoint

@dataclass(frozen=True)
class WireSegment():
    """The class that defines the wires between two grids."""
    kind: ClassVar[str] = 'wire'
    prefix: ClassVar[str] = 'W'
    id: str
    start: GridPoint
    end: GridPoint

    def __post_init__(self) -> None:
        """Validation function to check correctness of wire initialisation."""
        if self.start == self.end:
            raise ValueError("Start and end are the same point.")
        elif self.start > self.end:
            raise ValueError("Start and end in wrong order.")
        elif self.start.col != self.end.col and self.start.row != self.end.row:
            raise ValueError("Would create a diagonal wire.")

    @property
    def is_horizontal(self) -> bool:
        """Helper function to determine if the wire is horizontal."""
        return self.start.row == self.end.row

    def contains(self, point: GridPoint) -> bool:
        """True if the point lies on the segment, endpoints included."""
        return on_segment(point, self.start, self.end)

    def to_dict(self) -> dict:
        """Converts the WireSegment into a dict for circuit saving."""
        wire_dict = {
            'id': self.id,
            'start': self.start.to_dict(),
            'end': self.end.to_dict(),
        }
        return wire_dict

    @classmethod
    def from_dict(cls, data: dict) -> WireSegment:
        """Creates a WireSegment from a dict holding its information."""
        start = GridPoint.from_dict(data['start'])
        end = GridPoint.from_dict(data['end'])
        new_wire = cls(id=data['id'], start=start, end=end)
        return new_wire


def route_l(start: GridPoint, end: GridPoint, horizontal_first: bool) -> list[tuple[GridPoint, GridPoint]]:
    """Returns point pairs for wire path (2 pairs for L-shaped wire)."""
    if start == end:
        return []
    elif start.row == end.row or start.col == end.col:
        return [(start, end)]
    elif horizontal_first:
        return [
            (start, GridPoint(row=start.row, col=end.col)),
            (GridPoint(row=start.row, col=end.col), end)
            ]
    else:
        return [
            (start, GridPoint(row=end.row, col=start.col)),
            (GridPoint(row=end.row, col=start.col), end)
            ]

def on_segment(point: GridPoint, a: GridPoint, b: GridPoint) -> bool:
    """True if point lies on the straight segment a-b, ends included."""
    if a.row == b.row:                                    
        return (point.row == a.row
                and min(a.col, b.col) <= point.col <= max(a.col, b.col))
    return (point.col == a.col                            
            and min(a.row, b.row) <= point.row <= max(a.row, b.row))


def split_at_points(a: GridPoint, b: GridPoint, candidates: set[GridPoint]) -> list[tuple[GridPoint, GridPoint]]:
    """Breaks the straight segment a-b at any candidate points strictly inside it."""
    inside = {p for p in candidates if on_segment(p, a, b) and p != a and p != b}
    stops = sorted({a, b} | inside)
    return list(zip(stops, stops[1:]))
