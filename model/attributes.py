"""
@file attributes.py
@brief Holds the component dataclasses.
@author Evan Roe
@date 2026-10-03
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum


class Orientation(IntEnum):
    """Possible component orientations."""
    DEGREE_0 = 0
    DEGREE_90 = 90
    DEGREE_180 = 180
    DEGREE_270 = 270


@dataclass(frozen=True, order=True, kw_only=True)
class GridPoint():
    """Canvas grid column and row."""
    row: int 
    col: int

    def to_dict(self) -> dict:
        """Converts a GridPoint to a dict for circuit saving and loading."""
        return {'row': self.row, 'col': self.col}

    @classmethod
    def from_dict(cls, data: dict) -> GridPoint:
        """Returns a GridPoint from the saved dict."""
        return cls(row=data['row'], col=data['col'])


@dataclass(kw_only=True)
class Terminal():
    """Component terminal with its offset from the component."""
    name: str
    row_offset: int
    col_offset: int

@dataclass
class Label():
    """Component label with its text and value."""
    value: float
    unit: str
    text: str = ''
    
    def display(self) -> str:
        """Concatenates the value and unit into one variable."""
        full_value = f"{self.value}{self.unit}"
        return full_value

    def to_dict(self) -> dict:
        """Converts a Label to a dict for circuit saving and loading."""
        return {'text': self.text, 'value': self.value, 'unit': self.unit}

    @classmethod
    def from_dict(cls, data: dict) -> Label:
        """Returns a Label from the saved dict."""
        return cls(text=data['text'], value=data['value'], unit=data['unit'])

