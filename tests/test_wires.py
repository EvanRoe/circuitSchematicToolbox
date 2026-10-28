"""
@file test_wires.py
@brief Test file for the wires model.
@author Evan Roe
@date 2026-10-10
"""
import pytest

from model.circuit import Circuit
from model.wire import WireSegment, route_l
from model.nets import junction_points
from model.attributes import GridPoint
from controller.stack import CommandStack
from controller.commands import AddWireCommand, RemoveWireCommand, SplitWireCommand, CompositeCommand

def setup_test() -> tuple[WireSegment, Circuit]:
    wire = WireSegment('W1', GridPoint(row=5, col=3), GridPoint(row=9, col=3))
    circuit = Circuit()
    return (wire, circuit)

def test_circuit_wires_dict():
    old_wire, circuit = setup_test()
    wire = circuit.add_wire(old_wire.start, old_wire.end)
    assert wire.id == 'W1'
    assert circuit.wires['W1'] is wire
    assert circuit.counter['wire'] == 1

def test_diagonal_wire():
    _, circuit = setup_test()
    with pytest.raises(ValueError):
        circuit.add_wire(GridPoint(row=4, col=3), GridPoint(row=5, col=2))
    assert circuit.counter.get('wire', 0) == 0

def test_wire_ordered_ends():
    _, circuit = setup_test()
    wire = circuit.add_wire(GridPoint(row=3, col=5), GridPoint(row=3, col=2))
    assert wire.start == GridPoint(row=3, col=2)

def test_contains_function():
    wire, _ = setup_test()
    assert wire.contains(GridPoint(row=5, col=3))
    assert wire.contains(GridPoint(row=9, col=3))
    assert wire.contains(GridPoint(row=6, col=3)) 
    assert not wire.contains(GridPoint(row=1, col=3)) 
    assert not wire.contains(GridPoint(row=6, col=4)) 

def test_wire_from_to_dict():
    wire, _ = setup_test()
    wire_dict = wire.to_dict()
    assert WireSegment.from_dict(wire_dict) == wire

def test_add_wire_command_undo_redo():
    circuit = Circuit()
    stack = CommandStack()
    command = AddWireCommand(circuit, GridPoint(row=5, col=3), GridPoint(row=9, col=3))
    stack.execute(command)
    wire = command.wire                     
    assert circuit.wires['W1'] is wire
    stack.undo()
    assert not circuit.wires
    stack.redo()
    assert circuit.wires['W1'] is wire

def test_remove_wire_command_undo_redo():
    circuit = Circuit()
    _ = circuit.add_wire(GridPoint(row=5, col=3), GridPoint(row=9, col=3))
    stack = CommandStack()
    command = RemoveWireCommand(circuit, 'W1')
    stack.execute(command)
    wire = command.wire                     
    assert not circuit.wires
    stack.undo()
    assert circuit.wires['W1'] is wire
    stack.redo()
    assert not circuit.wires

def test_route_l_same_point():
    start = GridPoint(row=4, col=4)
    point_pairs = route_l(start, start, True)
    assert not point_pairs

def test_route_l_one_wire():
    start = GridPoint(row=4, col=4)
    end = GridPoint(row=4, col=8)
    start_vert = GridPoint(row=4, col=4)
    end_vert = GridPoint(row=8, col=4)
    point_pairs = route_l(start, end, True)
    point_pairs_vert = route_l(start_vert, end_vert, False)
    assert len(point_pairs) == 1
    assert len(point_pairs_vert) == 1

def test_route_l_function():
    start = GridPoint(row=4, col=4)
    end = GridPoint(row=8, col=8)
    point_pairs = route_l(start, end, True)
    point_pairs_vert = route_l(start, end, False)
    assert point_pairs != point_pairs_vert
    assert len(point_pairs) == 2
    assert len(point_pairs_vert) == 2
    
def test_wire_through():
    circuit = Circuit()
    _ = circuit.add_wire(GridPoint(row=5, col=3), GridPoint(row=9, col=3))
    point = GridPoint(row=7, col=3)
    wire_through = circuit.wire_through(point)
    assert wire_through
    point_endpoint = GridPoint(row=5, col=3)
    wire_through2 = circuit.wire_through(point_endpoint)
    assert not wire_through2
    point_off = GridPoint(row=5, col=5)
    wire_through3 = circuit.wire_through(point_off)
    assert not wire_through3

def test_split_wire_command():
    circuit = Circuit()
    og_wire = circuit.add_wire(GridPoint(row=5, col=3), GridPoint(row=9, col=3))
    point = GridPoint(row=7, col=3)
    command = SplitWireCommand(circuit, point)
    command.execute()
    assert len(circuit.wires.values()) == 2
    command.undo()
    assert og_wire in circuit.wires.values()

def test_composite_command():
    circuit = Circuit()
    command1 = AddWireCommand(circuit, GridPoint(row=5, col=3), GridPoint(row=9, col=3))
    command2 = AddWireCommand(circuit, GridPoint(row=9, col=3), GridPoint(row=9, col=5))
    comp_command = CompositeCommand([command1, command2])
    comp_command.execute()
    assert circuit.wires
    comp_command.undo()
    assert not circuit.wires
    comp_command.execute()
    assert circuit.wires

def test_wire_ending_mid_wire_splits_and_makes_junction():
    circuit = Circuit()
    circuit.add_wire(GridPoint(row=5, col=2), GridPoint(row=5, col=8))   
    mid = GridPoint(row=5, col=5)

    assert circuit.wire_through(mid) is not None                         
    commands = [SplitWireCommand(circuit, mid),
                AddWireCommand(circuit, mid, GridPoint(row=9, col=5))]
    CompositeCommand(commands).execute()

    assert 'W1' not in circuit.wires                                      
    assert mid in junction_points(circuit)                               