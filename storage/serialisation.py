"""
@file serialisation.py
@brief Handles saving and loading circuits.
@author Evan Roe
@date 2026-10-04
"""
import json
from pathlib import Path

from model.circuit import Circuit
from model.component import Component

FORMAT_VERSION = 1


def circuit_to_dict(circuit: Circuit) -> dict:
    """Converts a Circuit into plain JSON-compatible data."""
    return {
        'format_version': FORMAT_VERSION,
        'counter': circuit.counter,
        'components': [c.to_dict() for c in circuit.components.values()],
    }

def circuit_from_dict(data: dict, circuit: Circuit) -> None:
    """Fills an existing Circuit from saved data, replacing its contents."""
    version = data.get('format_version')
    if version != FORMAT_VERSION:
        raise ValueError(f"Unsupported file format version: {version}")
    
    components = {}
    for entry in data['components']:
        component = Component.from_dict(entry)
        if component.id in components:
            raise ValueError(f"Duplicate component id {component.id!r} in file")
        components[component.id] = component

    counter = {str(kind): int(count) for kind, count in data['counter'].items()}

    circuit.clear()
    for component in components.values():
        circuit.insert_component(component)
    circuit.counter.update(counter)
    

def save_json(circuit: Circuit, path: Path) -> None:
    """Write a circuit to disk as JSON."""
    data = circuit_to_dict(circuit)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path: Path, circuit: Circuit) -> None:
    """Load a circuit from disk into an existing Circuit."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    circuit_from_dict(data, circuit)