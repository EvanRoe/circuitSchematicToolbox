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
            raise ValueError(f"Start and end are the same point.")
        elif self.start > self.end:
            raise ValueError(f"Start and end in wrong order.")
        elif self.start.col != self.end.col and self.start.row != self.end.row:
            raise ValueError(f"Would create a diagonal wire.")

    @property
    def is_horizontal(self) -> bool:
        """Helper function to determine if the wire is horizontal."""
        return self.start.row == self.end.row

    def contains(self, point: GridPoint) -> bool:
        """True if the point lies on the segment, endpoints included."""
        if self.is_horizontal:
            return self.start.row == point.row and (self.start.col <= point.col <= self.end.col)
        else:
            return self.start.col == point.col and (self.start.row <= point.row <= self.end.row)

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
        start = GridPoint.from_dict(data['start'])
        end = GridPoint.from_dict(data['end'])
        new_wire = cls(id=data['id'], start=start, end=end)
        return new_wire
