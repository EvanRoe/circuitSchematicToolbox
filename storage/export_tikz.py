"""
@file export_tikz.py
@brief Handles the circuit to LaTeX export.
@author Evan Roe
@date 2026-11-15
"""
from pathlib import Path

from model.attributes import GridPoint
from model.circuit import Circuit
from model.component import Component
from model.nets import junction_points

PACKAGE_OPTIONS = 'european'
PICTURE_OPTIONS = 'scale=0.5'

HEADER = [
    r'\documentclass[border=4pt]{standalone}',
    rf'\usepackage[{PACKAGE_OPTIONS}]{{circuitikz}}',
    r'\begin{document}',
    rf'\begin{{circuitikz}}[{PICTURE_OPTIONS}]',
]
FOOTER = [r'\end{circuitikz}', r'\end{document}']

LATEX_SPECIAL = {
    '\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
    '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
    '^': r'\textasciicircum{}', 'Ω': r'$\Omega$',
}
LATEX_TABLE = str.maketrans(LATEX_SPECIAL)

def char_convert(text: str) -> str:
    """Converts non-latex characters to equivalents."""
    return text.translate(LATEX_TABLE)

def tikz_point(point: GridPoint) -> str:
    """Converts a GridPoint to a Tikz coordinate."""
    return f'({point.col}, {-point.row})'

def component_convert(component: Component) -> str:
    """Converts a component into LateX format."""
    points = list(component.get_terminal_positions().values())

    if len(points) == 2:
        options = [component.tikz_element]
        label = char_convert(component.label.text)
        options.append(f'l={{{label}}}')

        if component.has_value:
            value = char_convert(component.label.display())
            options.append(f'a={{{value}}}')

        joined = ', '.join(options)
        start, end = points
        return rf'\draw {tikz_point(start)} to[{joined}] {tikz_point(end)};'
    if len(points) == 1:
        return rf'\draw {tikz_point(points[0])} node[{component.tikz_element}] {{}};'

    raise ValueError(f'{component.id}: cannot export a {len(points)}-terminal component')
    
def circuit_to_circuitikz(circuit: Circuit) -> str:
    """Converts a circuit to a .tex document."""
    lines = list(HEADER)
    for component in sorted(circuit.components.values(), key=lambda c: c.id):
        lines.append(component_convert(component))
    for wire in sorted(circuit.wires.values(), key=lambda w: w.id):
        lines.append(rf'\draw {tikz_point(wire.start)} -- {tikz_point(wire.end)};')
    for node in sorted(junction_points(circuit)):
        lines.append(rf'\draw {tikz_point(node)} node[circ] {{}};')
    lines += FOOTER
    return '\n'.join(lines) + '\n'

def save_tikz(path: str, text: str) -> None:
    """Saves the tex text to disk at path."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)



