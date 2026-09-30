from dataclasses import dataclass
from enum import Enum, auto


class Orientation(Enum):
    DEGREE_0 = auto()
    DEGREE_90 = auto()
    DEGREE_180 = auto()
    DEGREE_270 = auto()

@dataclass
class GridPoint():
    col: int
    row: int

@dataclass
class Terminal():
    name: str
    col_offset: int
    row_offset: int

@dataclass
class Label():
    text: str = ""
    value: float = 0.0
    unit: str = ""

