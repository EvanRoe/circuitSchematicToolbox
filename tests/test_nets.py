"""
@file test_nets.py
@brief Test file for the nets extraction from circuits.
@author Evan Roe
@date 2026-10-10
"""
import pytest

from model.nets import UnionFind, Net, extract_nets
from model.circuit import Circuit
from model.attributes import GridPoint

def test_empty_circuit_means_no_nets():
    circuit = Circuit()
    assert not extract_nets(circuit)

def test_one_resistor_net():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(3, 4))
    nets = extract_nets(circuit)
    assert len(nets) == 2
    assert all(len(net.terminals) == 1 for net in nets)
    assert all(len(net.wire_ids) == 0 for net in nets)

def test_two_resistors_one_wire():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(4, 3))
    circuit.add_component('resistor', GridPoint(9, 3))
    circuit.add_wire(GridPoint(6, 3), GridPoint(7, 3))
    nets = extract_nets(circuit)
    assert len(nets) == 3
    assert len(nets[1].terminals) == 2
    assert nets[1].wire_ids == {'W1'}

def test_l_shaped_net():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(3, 4))
    circuit.add_component('resistor', GridPoint(7, 9))
    circuit.add_wire(GridPoint(5, 4), GridPoint(9, 4))
    circuit.add_wire(GridPoint(9, 4), GridPoint(9, 9))
    circuit.add_wire(GridPoint(1, 4), GridPoint(1, 9))
    circuit.add_wire(GridPoint(1, 9), GridPoint(5, 9))
    nets = extract_nets(circuit)
    assert len(nets) == 2
    assert any('W1' in net.wire_ids for net in nets)

def test_crossing_wires_different_nets():
    circuit = Circuit()
    circuit.add_wire(GridPoint(5, 4), GridPoint(9, 4))
    circuit.add_wire(GridPoint(7, 3), GridPoint(7, 7))
    nets = extract_nets(circuit)
    assert len(nets) == 2

def test_terminal_in_wire_not_in_same_net():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(7, 9))
    circuit.add_wire(GridPoint(7, 9), GridPoint(11, 9))
    nets = extract_nets(circuit)
    assert len(nets) == 3

def test_removing_wire_splits_net():
    circuit = Circuit()
    circuit.add_component('resistor', GridPoint(4, 3))
    circuit.add_component('resistor', GridPoint(9, 3))
    circuit.add_wire(GridPoint(6, 3), GridPoint(7, 3))
    nets = extract_nets(circuit)
    assert len(nets) == 3
    circuit.remove_wire('W1')
    nets = extract_nets(circuit)
    assert len(nets) == 4

def test_unionfind_basic_function():
    uf = UnionFind()
    point_a = GridPoint(1, 2)
    uf.add(point_a)
    root = uf.find(point_a)
    assert root == point_a
    point_b = GridPoint(6, 2)
    point_c = GridPoint(7, 3)
    uf.add(point_b)
    uf.add(point_c)
    uf.union(point_a, point_b)
    assert uf.find(point_a) == uf.find(point_b)
    uf.add(point_b)
    assert uf.find(point_a) == uf.find(point_b)
    uf.union(point_b, point_c)
    assert uf.find(point_a) == uf.find(point_c)
    
    
    
    