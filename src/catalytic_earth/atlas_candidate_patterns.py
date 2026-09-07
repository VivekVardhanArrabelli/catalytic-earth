"""Atom-variable joins over literal unreviewed candidate events.

Variables bind only to panel-local atom identifiers in a candidate's retained
before graph.  The query does not turn those locators into physical atom maps,
canonical participants, or mechanistic equivalence classes.
"""

from __future__ import annotations

import copy
import re
from typing import Any

from .atlas_candidate_events import (
    _ELEMENTS,
    canonical_bytes,
    validate_candidate_event_catalog,
)


SCHEMA_VERSION = "catalytic-earth.candidate-pattern-query.v1"

_SUPPORTS = {"after_graph_confirmed", "source_arrow_only", "any"}
_VARIABLE = re.compile(r"[A-Za-z][A-Za-z0-9_]{0,31}")
_CLAUSE_KEYS = {"kind", "elements", "variables", "before", "after"}
_MAX_UNIQUE_CLAUSES = 8
_MAX_VARIABLES = 12
_MAX_SEARCH_WORK = 100_000


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _object(value: Any, label: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{label} must be an object")
    return value


def _array(value: Any, label: str) -> list[Any]:
    _require(isinstance(value, list), f"{label} must be an array")
    return value


def _string(value: Any, label: str) -> str:
    _require(isinstance(value, str) and value != "", f"{label} must be a nonempty string")
    return value


def _integer(value: Any, label: str) -> int:
    _require(type(value) is int, f"{label} must be an integer")
    return value


def _normalize_clause(value: Any, index: int) -> dict[str, Any]:
    label = f"clauses[{index}]"
    clause = _object(value, label)
    _require(set(clause) == _CLAUSE_KEYS, f"{label} fields differ")
    kind = _string(clause["kind"], f"{label}.kind")
    _require(kind in {"bond", "charge"}, f"{label}.kind is unsupported")
    elements = _array(clause["elements"], f"{label}.elements")
    variables = _array(clause["variables"], f"{label}.variables")
    length = 2 if kind == "bond" else 1
    _require(
        len(elements) == length and len(variables) == length,
        f"{label} element and variable arity differs from its kind",
    )

    pairs: list[tuple[str, str]] = []
    for position, (raw_element, raw_variable) in enumerate(zip(elements, variables)):
        element = _string(raw_element, f"{label}.elements[{position}]")
        variable = _string(raw_variable, f"{label}.variables[{position}]")
        _require(element in _ELEMENTS, f"{label} uses an invalid exact element token")
        _require(_VARIABLE.fullmatch(variable) is not None, f"{label} uses an invalid variable name")
        pairs.append((element, variable))
    if kind == "bond":
        _require(pairs[0][1] != pairs[1][1], f"{label} repeats one variable in a bond")
        pairs.sort()

    before = _integer(clause["before"], f"{label}.before")
    after = _integer(clause["after"], f"{label}.after")
    _require(before != after, f"{label} is a no-op")
    if kind == "bond":
        _require(
            before in {0, 1, 2, 3} and after in {0, 1, 2, 3},
            f"{label} bond values are unsupported",
        )
    return {
        "kind": kind,
        "elements": [pair[0] for pair in pairs],
        "variables": [pair[1] for pair in pairs],
        "before": before,
        "after": after,
    }


def _normalize_clauses(value: Any) -> list[dict[str, Any]]:
    rows = _array(value, "clauses")
    _require(bool(rows), "at least one pattern clause is required")
    unique: dict[bytes, dict[str, Any]] = {}
    for index, raw in enumerate(rows):
        clause = _normalize_clause(raw, index)
        unique[canonical_bytes(clause)] = clause
    _require(
        len(unique) <= _MAX_UNIQUE_CLAUSES,
        f"pattern query exceeds {_MAX_UNIQUE_CLAUSES} unique clauses",
    )
    clauses = [unique[key] for key in sorted(unique)]

    variable_elements: dict[str, str] = {}
    for clause in clauses:
        for variable, element in zip(clause["variables"], clause["elements"]):
            previous = variable_elements.setdefault(variable, element)
            _require(
                previous == element,
                f"variable {variable} is assigned more than one element",
            )
    _require(
        len(variable_elements) <= _MAX_VARIABLES,
        f"pattern query exceeds {_MAX_VARIABLES} variables",
    )
    return clauses


class _WorkBudget:
    def __init__(self) -> None:
        self.used = 0

    def spend(self, amount: int = 1) -> None:
        self.used += amount
        if self.used > _MAX_SEARCH_WORK:
            raise ValueError(
                f"pattern query exceeds the {_MAX_SEARCH_WORK}-unit search work budget"
            )


def _signature_clause(clause: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": clause["kind"],
        "elements": clause["elements"],
        "before": clause["before"],
        "after": clause["after"],
    }


def _event_options(
    clause: dict[str, Any],
    events: list[dict[str, Any]],
    atom_elements: dict[str, str],
    budget: _WorkBudget,
) -> list[tuple[dict[str, str], dict[str, Any]]]:
    expected_signature = _signature_clause(clause)
    options: list[tuple[dict[str, str], dict[str, Any]]] = []
    for event in events:
        budget.spend()
        if event["signature"] != expected_signature:
            continue
        atom_ids = event["source_edit"]["atom_ids"]
        if clause["kind"] == "charge":
            atom_id = atom_ids[0]
            _require(atom_elements.get(atom_id) == clause["elements"][0], "catalog charge witness element differs")
            options.append(({clause["variables"][0]: atom_id}, event))
            budget.spend()
            continue

        orientations = (atom_ids, list(reversed(atom_ids)))
        seen: set[tuple[tuple[str, str], ...]] = set()
        for oriented_ids in orientations:
            if [atom_elements.get(atom_id) for atom_id in oriented_ids] != clause["elements"]:
                continue
            binding = dict(zip(clause["variables"], oriented_ids))
            key = tuple(sorted(binding.items()))
            if key not in seen:
                seen.add(key)
                options.append((binding, event))
                budget.spend()
    return options


def _merge_bindings(
    current: dict[str, str], option: dict[str, str]
) -> dict[str, str] | None:
    result = dict(current)
    atom_to_variable = {atom_id: variable for variable, atom_id in result.items()}
    for variable, atom_id in option.items():
        if variable in result:
            if result[variable] != atom_id:
                return None
            continue
        if atom_id in atom_to_variable and atom_to_variable[atom_id] != variable:
            return None
        result[variable] = atom_id
        atom_to_variable[atom_id] = variable
    return result


def _candidate_bindings(
    row: dict[str, Any],
    clauses: list[dict[str, Any]],
    support: str,
    budget: _WorkBudget,
) -> list[dict[str, Any]]:
    eligible = [
        event for event in row["events"]
        if support == "any" or event["support"] == support
    ]
    if not eligible:
        return []
    atoms = {
        atom["atom_id"]: atom["element"]
        for atom in row["candidate"]["source_panels"]["before_graph"]["atoms"]
    }
    options_by_clause = [
        _event_options(clause, eligible, atoms, budget) for clause in clauses
    ]
    if any(not options for options in options_by_clause):
        return []

    # Each state retains one concrete witness per processed clause.  Equivalent
    # final atom assignments are grouped later, preserving all witness choices.
    states: list[tuple[dict[str, str], tuple[dict[str, Any], ...]]] = [({}, ())]
    for options in options_by_clause:
        next_states = []
        for bindings, witnesses in states:
            for option, event in options:
                budget.spend()
                merged = _merge_bindings(bindings, option)
                if merged is not None:
                    next_states.append((merged, (*witnesses, event)))
        states = next_states
        if not states:
            return []

    grouped: dict[
        tuple[tuple[str, str], ...],
        list[dict[str, dict[str, Any]]],
    ] = {}
    for bindings, witnesses in states:
        key = tuple(sorted(bindings.items()))
        per_clause = grouped.setdefault(key, [dict() for _ in clauses])
        for index, event in enumerate(witnesses):
            per_clause[index].setdefault(event["event_id"], event)

    result = []
    for key in sorted(grouped):
        per_clause = grouped[key]
        result.append({
            "atom_bindings": dict(key),
            "clause_witnesses": [
                {
                    "clause": copy.deepcopy(clause),
                    "events": copy.deepcopy(list(per_clause[index].values())),
                }
                for index, clause in enumerate(clauses)
            ],
        })
    return result


def query_candidate_patterns(
    value: dict[str, Any],
    *,
    clauses: list[dict[str, Any]],
    mcsa_id: str | None = None,
    support: str = "after_graph_confirmed",
) -> dict[str, Any]:
    """Join literal event clauses through injective before-panel variables."""

    summary = validate_candidate_event_catalog(value)
    normalized = _normalize_clauses(clauses)
    _require(isinstance(support, str) and support in _SUPPORTS, "support filter is unsupported")
    if mcsa_id is not None:
        _require(isinstance(mcsa_id, str), "mcsa_id must be a string or null")
        mcsa_id = mcsa_id.strip().upper()
        _require(re.fullmatch(r"M[0-9]{4}", mcsa_id) is not None, "mcsa_id must be an exact M-CSA identifier")

    budget = _WorkBudget()
    matches = []
    for row in value["candidates"]:
        if mcsa_id is not None and row["candidate"]["source_binding"]["record_id"] != mcsa_id:
            continue
        bindings = _candidate_bindings(row, normalized, support, budget)
        if bindings:
            matches.append({
                "candidate_row": copy.deepcopy(row),
                "bindings": bindings,
            })

    return {
        "schema_version": SCHEMA_VERSION,
        "catalog_id": summary["catalog_id"],
        "catalog_sha256": summary["catalog_sha256"],
        "status": "unreviewed",
        "provenance": copy.deepcopy(value["provenance"]),
        "filters": {
            "clauses": normalized,
            "mcsa_id": mcsa_id,
            "support": support,
        },
        "query_semantics": {
            "clause_combination": "all_clauses_within_one_candidate",
            "support_filter_application": "before_variable_join",
            "variable_scope": "before_graph_source_node_identifiers",
            "different_variables_are_injective": True,
            "bond_endpoint_orientation": "all_element_compatible_orientations",
            "clauses_require_one_shared_event": False,
            "bindings_imply_physical_atom_identity": False,
            "bindings_imply_canonical_participant_correspondence": False,
            "shared_pattern_implies_mechanism_equivalence": False,
            "empty_result": "no_matching_candidate_pattern_not_absence_of_chemistry",
        },
        "candidate_count": len(matches),
        "binding_count": sum(len(match["bindings"]) for match in matches),
        "matches": matches,
    }


__all__ = ["SCHEMA_VERSION", "query_candidate_patterns"]
