"""
@file favourites.py
@brief The favourites functionality.
@author Evan Roe
@date 2026-10-21
"""
from __future__ import annotations
from pathlib import Path

from model.circuit import Circuit
from storage.serialisation import save_json, load_json

FAVOURITES_DIR = Path.home() / '.circuit_designer' / 'favourites'
INVALID_NAME_CHARS = set('\\/:*?"<>|')


def _favourite_path(name: str, folder: Path) -> Path:
    """The path for a favourite, with a usable name."""
    stripped_name = name.strip()
    if not stripped_name or any(c in INVALID_NAME_CHARS for c in stripped_name):
        raise ValueError(f"{stripped_name!r} was an invalid name.")
    return folder / f'{stripped_name}.json'

def list_favourites(folder: Path = FAVOURITES_DIR) -> list[str]:
    """Names of all saved favourites alphabetically."""
    if not folder.is_dir():
        return []
    return sorted(path.stem for path in folder.glob('*.json'))

def favourite_exists(name: str, folder: Path = FAVOURITES_DIR) -> bool:
    """Returns whether the given favourite exists."""
    return _favourite_path(name, folder).exists()

def save_favourite(circuit: Circuit, name: str, folder: Path = FAVOURITES_DIR) -> None:
    """Save the circuit with the favourite name to the folder."""
    folder.mkdir(parents=True, exist_ok=True)
    path = _favourite_path(name, folder)
    save_json(circuit, path)

def load_favourite(name: str, circuit: Circuit, folder: Path = FAVOURITES_DIR) -> None:
    """Load a favourite from the name"""
    path = _favourite_path(name, folder)
    load_json(path, circuit)