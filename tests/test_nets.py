"""
@file test_nets.py
@brief Test file for the nets extraction from circuits.
@author Evan Roe
@date 2026-10-10
"""
import pytest

from model.nets import UnionFind, extract_nets
from model.circuit import Circuit
from model.attributes import GridPoint

def test_empty_circuit_means_no_nets():
    circuit = Circuit()
    assert not extract_nets(circuit)

def test_one_resistor_net():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(row=4, col=3))
    nets = extract_nets(circuit)
    assert len(nets) == 2
    assert all(len(net.terminals) == 1 for net in nets)
    assert all(len(net.wire_ids) == 0 for net in nets)

def test_two_resistors_one_wire():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(row=3, col=4))
    circuit.add_component('resistor', GridPoint(row=3, col=9))
    circuit.add_wire(GridPoint(row=3, col=6), GridPoint(row=3, col=7))
    nets = extract_nets(circuit)
    assert len(nets) == 3
    assert any(len(net.terminals) == 2 for net in nets)
    assert any(net.wire_ids == {'W1'} for net in nets)

def test_l_shaped_net():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(row=4, col=3))
    circuit.add_component('resistor', GridPoint(row=9, col=7))
    circuit.add_wire(GridPoint(row=4, col=5), GridPoint(row=4, col=9))
    circuit.add_wire(GridPoint(row=4, col=9), GridPoint(row=9, col=9))
    circuit.add_wire(GridPoint(row=4, col=1), GridPoint(row=9, col=1))
    circuit.add_wire(GridPoint(row=9, col=1), GridPoint(row=9, col=5))
    nets = extract_nets(circuit)
    assert len(nets) == 2
    assert any('W1' in net.wire_ids for net in nets)

def test_crossing_wires_different_nets():
    circuit = Circuit()
    circuit.add_wire(GridPoint(row=4, col=5), GridPoint(row=4, col=9))
    circuit.add_wire(GridPoint(row=3, col=7), GridPoint(row=7, col=7))
    nets = extract_nets(circuit)
    assert len(nets) == 2

def test_terminal_in_wire_not_in_same_net():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(row=9, col=7))
    circuit.add_wire(GridPoint(row=9, col=7), GridPoint(row=9, col=11))
    nets = extract_nets(circuit)
    assert len(nets) == 3

def test_removing_wire_splits_net():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(row=3, col=4))
    circuit.add_component('resistor', GridPoint(row=3, col=9))
    circuit.add_wire(GridPoint(row=3, col=6), GridPoint(row=3, col=7))
    nets = extract_nets(circuit)
    assert len(nets) == 3
    circuit.remove_wire('W1')
    nets = extract_nets(circuit)
    assert len(nets) == 4

def test_unionfind_basic_function():
    uf = UnionFind()
    point_a = GridPoint(row=2, col=1)
    uf.add(point_a)
    root = uf.find(point_a)
    assert root == point_a
    point_b = GridPoint(row=2, col=6)
    point_c = GridPoint(row=3, col=7)
    uf.add(point_b)
    uf.add(point_c)
    uf.union(point_a, point_b)
    assert uf.find(point_a) == uf.find(point_b)
    uf.add(point_b)
    assert uf.find(point_a) == uf.find(point_b)
    uf.union(point_b, point_c)
    assert uf.find(point_a) == uf.find(point_c)
    
    
    
    