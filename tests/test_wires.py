import pytest

from model.circuit import Circuit
from model.wire import WireSegment
from model.attributes import GridPoint
from controller.stack import CommandStack
from controller.commands import AddWireCommand, RemoveWireCommand

def setup_test() -> tuple[WireSegment, Circuit]:
    wire = WireSegment('W1', GridPoint(3, 5), GridPoint(3, 9))
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
        circuit.add_wire(GridPoint(3, 4), GridPoint(2, 5))
    assert circuit.counter.get('wire', 0) == 0

def test_wire_ordered_ends():
    _, circuit = setup_test()
    wire = circuit.add_wire(GridPoint(5, 3), GridPoint(2, 3))
    assert wire.start == GridPoint(2, 3)

def test_contains_function():
    wire, _ = setup_test()
    assert wire.contains(GridPoint(3, 5))
    assert wire.contains(GridPoint(3, 9))
    assert wire.contains(GridPoint(3, 6)) 
    assert not wire.contains(GridPoint(3, 1)) 
    assert not wire.contains(GridPoint(4, 6)) 

def test_wire_from_to_dict():
    wire, _ = setup_test()
    wire_dict = wire.to_dict()
    assert WireSegment.from_dict(wire_dict) == wire

def test_add_wire_command_undo_redo():
    circuit = Circuit()
    stack = CommandStack()
    command = AddWireCommand(circuit, GridPoint(3, 5), GridPoint(3, 9))
    stack.execute(command)
    wire = command.wire                     
    assert circuit.wires['W1'] is wire
    stack.undo()
    assert not circuit.wires
    stack.redo()
    assert circuit.wires['W1'] is wire

def test_remove_wire_command_undo_redo():
    circuit = Circuit()
    _ = circuit.add_wire(GridPoint(3, 5), GridPoint(3, 9))
    stack = CommandStack()
    command = RemoveWireCommand(circuit, 'W1')
    stack.execute(command)
    wire = command.wire                     
    assert not circuit.wires
    stack.undo()
    assert circuit.wires['W1'] is wire
    stack.redo()
    assert not circuit.wires
