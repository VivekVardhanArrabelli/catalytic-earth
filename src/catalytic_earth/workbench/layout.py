"""Deterministic two-dimensional layout for source-depiction graphs.

The packaged transformation query returns chemical graphs without depiction
coordinates: each atom carries only ``atom_id``, ``element``, ``formal_charge``
and ``stereochemistry``. The positions produced here are therefore *computed*
from graph topology alone.

A computed layout is a drawing convenience. It is not measured geometry, not
the original source-panel depiction coordinates, and not a molecular
conformation. Every consumer of this module must label it as computed. Where
the packaged data does retain original source depiction coordinates (the
``x2``/``y2`` annotations on source fragments), those are passed through
separately by :mod:`catalytic_earth.workbench.adapter` and are never mixed
into these computed positions.

The layout is fully deterministic: seeding is by sorted atom identifier, and
no random number generator is used. The same graph always yields the same
coordinates.
"""

from __future__ import annotations

import math
from typing import Any, Iterable

__all__ = ["compute_layout", "LAYOUT_SEMANTICS"]

LAYOUT_SEMANTICS: dict[str, Any] = {
    "basis": "graph_topology_only",
    "coordinates_are_measured_geometry": False,
    "coordinates_are_source_depiction": False,
    "determinism": "sorted_atom_id_seeding_no_rng",
    "kind": "computed_2d_layout",
    "method": "per_component_force_directed_then_packed",
    "note": (
        "Positions are a computed drawing of the depicted graph. They are not "
        "experimentally measured geometry, not a molecular conformation, and "
        "not the original source-panel depiction coordinates."
    ),
    "union_bond_basis": (
        "Layout uses the union of before-panel and after-panel bonds so that a "
        "single shared frame can show both states. This is a drawing choice and "
        "asserts no chemistry."
    ),
}

_ITERATIONS = 320
_IDEAL = 1.0


def _components(atom_ids: list[str], adjacency: dict[str, set[str]]) -> list[list[str]]:
    """Split atoms into connected components, preserving sorted order."""
    seen: set[str] = set()
    out: list[list[str]] = []
    for start in atom_ids:
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        group: list[str] = []
        while stack:
            node = stack.pop()
            group.append(node)
            for neighbour in sorted(adjacency.get(node, ())):
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
        out.append(sorted(group, key=atom_ids.index))
    return out


def _layout_component(
    nodes: list[str], adjacency: dict[str, set[str]]
) -> dict[str, list[float]]:
    """Force-directed placement of one connected component."""
    count = len(nodes)
    if count == 1:
        return {nodes[0]: [0.0, 0.0]}
    # Deterministic seeding: evenly spaced on a circle, ordered by atom id.
    radius = _IDEAL * math.sqrt(count) / 2.0 + _IDEAL
    position = {
        node: [
            radius * math.cos(2.0 * math.pi * index / count),
            radius * math.sin(2.0 * math.pi * index / count),
        ]
        for index, node in enumerate(nodes)
    }
    area = _IDEAL * _IDEAL * count
    optimal = math.sqrt(area / count)
    temperature = radius / 2.0
    cooling = temperature / (_ITERATIONS + 1)

    for _ in range(_ITERATIONS):
        displacement = {node: [0.0, 0.0] for node in nodes}
        for i in range(count):
            a = nodes[i]
            ax, ay = position[a]
            for j in range(i + 1, count):
                b = nodes[j]
                bx, by = position[b]
                dx, dy = ax - bx, ay - by
                distance = math.hypot(dx, dy) or 1e-6
                force = (optimal * optimal) / distance
                ux, uy = dx / distance, dy / distance
                displacement[a][0] += ux * force
                displacement[a][1] += uy * force
                displacement[b][0] -= ux * force
                displacement[b][1] -= uy * force
        for a in nodes:
            ax, ay = position[a]
            for b in adjacency.get(a, ()):  # each edge visited from both ends
                if b not in position:
                    continue
                bx, by = position[b]
                dx, dy = ax - bx, ay - by
                distance = math.hypot(dx, dy) or 1e-6
                force = (distance * distance) / optimal
                displacement[a][0] -= (dx / distance) * force
                displacement[a][1] -= (dy / distance) * force
        for node in nodes:
            dx, dy = displacement[node]
            distance = math.hypot(dx, dy) or 1e-6
            step = min(distance, temperature)
            position[node][0] += (dx / distance) * step
            position[node][1] += (dy / distance) * step
        temperature = max(temperature - cooling, 1e-4)
    return {node: [round(x, 4), round(y, 4)] for node, (x, y) in position.items()}


def _bounds(points: Iterable[list[float]]) -> tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), min(ys), max(xs), max(ys)


def compute_layout(
    atoms: list[dict[str, Any]],
    bond_sets: list[list[dict[str, Any]]],
) -> dict[str, Any]:
    """Compute deterministic positions for ``atoms``.

    ``bond_sets`` holds one or more bond lists (typically the before-panel and
    after-panel bonds). Their union defines connectivity for layout purposes so
    that both panel states can share one frame.
    """
    atom_ids = [str(atom["atom_id"]) for atom in atoms]
    index = {atom_id: position for position, atom_id in enumerate(atom_ids)}
    adjacency: dict[str, set[str]] = {atom_id: set() for atom_id in atom_ids}
    for bonds in bond_sets:
        for bond in bonds:
            first, second = (str(value) for value in bond["atom_ids"])
            if first in adjacency and second in adjacency:
                adjacency[first].add(second)
                adjacency[second].add(first)

    ordered = sorted(atom_ids, key=lambda value: index[value])
    groups = _components(ordered, adjacency)

    placed: list[dict[str, list[float]]] = []
    for group in groups:
        placed.append(_layout_component(group, adjacency))

    # Normalise each component to the origin, then pack left to right in rows.
    boxes = []
    for coordinates in placed:
        min_x, min_y, max_x, max_y = _bounds(coordinates.values())
        for key in coordinates:
            coordinates[key] = [
                coordinates[key][0] - min_x,
                coordinates[key][1] - min_y,
            ]
        boxes.append((max_x - min_x, max_y - min_y))

    gap = 1.6
    total_width = sum(width for width, _ in boxes) + gap * max(len(boxes) - 1, 0)
    row_limit = max(total_width / 1.7, max((w for w, _ in boxes), default=1.0))

    positions: dict[str, list[float]] = {}
    cursor_x = 0.0
    cursor_y = 0.0
    row_height = 0.0
    for coordinates, (width, height) in zip(placed, boxes):
        if cursor_x > 0.0 and cursor_x + width > row_limit:
            cursor_x = 0.0
            cursor_y += row_height + gap
            row_height = 0.0
        for key, (x, y) in coordinates.items():
            positions[key] = [round(x + cursor_x, 4), round(y + cursor_y, 4)]
        cursor_x += width + gap
        row_height = max(row_height, height)

    min_x, min_y, max_x, max_y = _bounds(positions.values())
    return {
        "component_count": len(groups),
        "components": [sorted(group) for group in groups],
        "positions": positions,
        "semantics": dict(LAYOUT_SEMANTICS),
        "viewbox": {
            "height": round(max_y - min_y, 4),
            "min_x": round(min_x, 4),
            "min_y": round(min_y, 4),
            "width": round(max_x - min_x, 4),
        },
    }
