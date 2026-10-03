"""
@file attributes.py
@brief Holds the component dataclasses.
@author Evan Roe
@date 2026-10-03
"""
from dataclasses import dataclass
from enum import Enum, auto


class Orientation(Enum):
    """Possible component orientations."""
    DEGREE_0 = auto()
    DEGREE_90 = auto()
    DEGREE_180 = auto()
    DEGREE_270 = auto()

@dataclass
class GridPoint():
    """Canvas grid column and row."""
    col: int
    row: int

@dataclass
class Terminal():
    """Component terminal with its offset from the component."""
    name: str
    col_offset: int
    row_offset: int

@dataclass
class Label():
    """Component label with its text and value."""
    text: str = ''
    value: float = 0.0
    unit: str = ''

    def display(self) -> str:
        """Concatenates the value and unit into one variable."""
        full_value = f"{self.value}{self.unit}"
        return full_value

