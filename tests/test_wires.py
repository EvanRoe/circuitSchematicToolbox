"""
@file test_wires.py
@brief Test file for the wires model.
@author Evan Roe
@date 2026-10-10
"""
import pytest

from model.circuit import Circuit
from model.wire import WireSegment
from model.attributes import GridPoint
from controller.stack import CommandStack
from controller.commands import AddWireCommand, RemoveWireCommand

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
