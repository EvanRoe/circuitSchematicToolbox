"""
@file test_rotation.py
@brief Tests the rotation of components.
@author Evan Roe
@date 2026-11-10
"""

from model.attributes import GridPoint, Orientation, rotate_offset
from model.circuit import Circuit
from model.component import Component
from controller.commands import RotateComponentCommand
from controller.stack import CommandStack


def make_component(
    kind: str = 'resistor',
    row: int = 5,
    col: int = 5,
    orientation: Orientation = Orientation.DEGREE_0,
) -> tuple[Circuit, Component]:
    circuit = Circuit()
    component = circuit.add_component(kind, GridPoint(row=row, col=col))
    component.orientation = orientation
    return circuit, component

def test_resistor_at_90_is_vertical():
    _, resistor = make_component(orientation=Orientation.DEGREE_90)
    terminals = resistor.get_terminal_positions()
    assert terminals == {
        'left': GridPoint(row=3, col=5),
        'right': GridPoint(row=7, col=5),
    }
        
def test_rotate_offset():
    assert rotate_offset(0, 1, Orientation.DEGREE_0) == (0, 1)
    assert rotate_offset(0, 1, Orientation.DEGREE_90) == (1, 0)
    assert rotate_offset(0, 1, Orientation.DEGREE_180) == (0, -1)
    assert rotate_offset(0, 1, Orientation.DEGREE_270) == (-1, 0)

def test_four_times_90_returns_original_position():
    x, y = rotate_offset(-1, 2, Orientation.DEGREE_90)
    x, y = rotate_offset(x, y, Orientation.DEGREE_90)
    x, y = rotate_offset(x, y, Orientation.DEGREE_90)
    x, y = rotate_offset(x, y, Orientation.DEGREE_90)
    assert (x, y) == (-1, 2)

def test_rotated_cw_wraps_360():
    assert Orientation.DEGREE_270.rotated_cw() == Orientation.DEGREE_0

def test_rotated_shapes_90():
    _, resistor = make_component(orientation=Orientation.DEGREE_90)
    rects = [s for s in resistor.rotated_shapes() if s[0] == 'rect']
    assert len(rects) == 1
    _, x1, y1, x2, y2 = rects[0]
    assert abs(y2 - y1) > abs(x2 - x1) 

def test_rotate_component_command():
    circuit, resistor = make_component()
    stack = CommandStack()

    stack.execute(RotateComponentCommand(circuit, resistor.id))
    assert resistor.orientation == Orientation.DEGREE_90

    stack.undo()
    assert resistor.orientation == Orientation.DEGREE_0

    stack.redo()
    assert resistor.orientation == Orientation.DEGREE_90











