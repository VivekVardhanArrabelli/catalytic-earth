"""Exact SQLite participant lookup for validated Atlas source drafts.

This module indexes source-reported participant identifiers and reaction sides.
It deliberately performs no chemical-equivalence, ontology, salt, charge, or
protonation inference.
"""

from __future__ import annotations

import re
import sqlite3
from collections.abc import Iterable
from typing import Any

from .atlas_drafts import validate_source_drafts


_CHEBI_RE = re.compile(r"(?:CHEBI:)?([0-9]+)", re.IGNORECASE)


def normalize_chebi_id(value: str) -> str:
    """Return ``CHEBI:<positive integer>`` for an exact supported spelling."""

    if not isinstance(value, str):
        raise ValueError("ChEBI identifier must be text")
    match = _CHEBI_RE.fullmatch(value.strip())
    if match is None:
        raise ValueError(f"invalid ChEBI identifier: {value!r}")
    number = int(match.group(1))
    if number <= 0:
        raise ValueError(f"ChEBI identifier must be positive: {value!r}")
    return f"CHEBI:{number}"


def _normalized_filter(values: Iterable[str], name: str) -> list[str]:
    if not isinstance(values, (list, tuple)):
        raise ValueError(f"{name} must be a list or tuple of ChEBI identifiers")
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = normalize_chebi_id(value)
        if normalized not in seen:
            output.append(normalized)
            seen.add(normalized)
    return output


def materialize_source_drafts(bundle: dict[str, Any]) -> sqlite3.Connection:
    """Validate and materialize source records and participant rows in memory.

    The caller owns and must close the returned connection. ``source_order`` and
    ``source_row_index`` preserve the order of the validated source bundle.
    """

    validate_source_drafts(bundle)
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute(
            """
            CREATE TABLE records (
                record_id TEXT PRIMARY KEY,
                source_order INTEGER NOT NULL UNIQUE,
                case_id TEXT NOT NULL,
                mcsa_id TEXT NOT NULL UNIQUE
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE participants (
                record_id TEXT NOT NULL,
                source_row_index INTEGER NOT NULL,
                source_compound_token TEXT NOT NULL,
                normalized_chebi_id TEXT,
                name TEXT NOT NULL,
                side TEXT NOT NULL CHECK (side IN ('left', 'right')),
                source_count INTEGER NOT NULL CHECK (source_count > 0),
                PRIMARY KEY (record_id, source_row_index),
                FOREIGN KEY (record_id) REFERENCES records(record_id)
            )
            """
        )
        record_rows = []
        participant_rows = []
        for source_order, record in enumerate(bundle["records"], 1):
            record_id = record["record_id"]
            record_rows.append(
                (record_id, source_order, record["case_id"], record["mcsa_id"])
            )
            participant_rows.extend(
                (
                    record_id,
                    participant["source_row_index"],
                    participant["source_compound_token"],
                    participant["normalized_chebi_id"],
                    participant["name"],
                    participant["side"],
                    participant["source_count"],
                )
                for participant in record["reaction_context"]["participants"]
            )
        with connection:
            connection.executemany(
                """
                INSERT INTO records(record_id, source_order, case_id, mcsa_id)
                VALUES (?, ?, ?, ?)
                """,
                record_rows,
            )
            connection.executemany(
                """
                INSERT INTO participants(
                    record_id, source_row_index, source_compound_token,
                    normalized_chebi_id, name, side, source_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                participant_rows,
            )
        return connection
    except Exception:
        connection.close()
        raise


def _exists_clause(side: str | None) -> str:
    side_clause = "" if side is None else f" AND candidate.side = '{side}'"
    return (
        "EXISTS (SELECT 1 FROM participants AS candidate "
        "WHERE candidate.record_id = records.record_id "
        f"AND candidate.normalized_chebi_id = ?{side_clause})"
    )


def _row_match_clause(values: list[str], side: str | None) -> tuple[str, list[str]]:
    if not values:
        return "", []
    placeholders = ", ".join("?" for _ in values)
    identifier_clause = f"normalized_chebi_id IN ({placeholders})"
    if side is not None:
        identifier_clause = f"(side = '{side}' AND {identifier_clause})"
    return identifier_clause, values


def match_source_participants(
    bundle: dict[str, Any],
    *,
    participants: Iterable[str] = (),
    reactants: Iterable[str] = (),
    products: Iterable[str] = (),
) -> dict[str, Any]:
    """Match exact ChEBI identifiers with all clauses scoped to one record."""

    filters = {
        "participants": _normalized_filter(participants, "participants"),
        "reactants": _normalized_filter(reactants, "reactants"),
        "products": _normalized_filter(products, "products"),
    }
    connection = materialize_source_drafts(bundle)
    try:
        if not any(filters.values()):
            record_ids = connection.execute(
                "SELECT record_id FROM records ORDER BY source_order"
            )
            return {
                "filters": filters,
                "matches": {record_id: [] for (record_id,) in record_ids},
            }

        requirements: list[str] = []
        requirement_parameters: list[str] = []
        for name, side in (
            ("participants", None),
            ("reactants", "left"),
            ("products", "right"),
        ):
            for identifier in filters[name]:
                requirements.append(_exists_clause(side))
                requirement_parameters.append(identifier)
        qualifying_sql = (
            "SELECT record_id FROM records WHERE "
            + " AND ".join(requirements)
            + " ORDER BY source_order"
        )
        qualifying_ids = [
            record_id
            for (record_id,) in connection.execute(
                qualifying_sql, requirement_parameters
            )
        ]

        row_clauses: list[str] = []
        row_parameters: list[str] = []
        for name, side in (
            ("participants", None),
            ("reactants", "left"),
            ("products", "right"),
        ):
            clause, parameters = _row_match_clause(filters[name], side)
            if clause:
                row_clauses.append(clause)
                row_parameters.extend(parameters)

        matches: dict[str, list[dict[str, Any]]] = {}
        row_sql = (
            "SELECT source_row_index, source_compound_token, normalized_chebi_id, "
            "name, side, source_count FROM participants "
            "WHERE record_id = ? AND ("
            + " OR ".join(row_clauses)
            + ") ORDER BY source_row_index"
        )
        for record_id in qualifying_ids:
            rows = connection.execute(
                row_sql, [record_id, *row_parameters]
            ).fetchall()
            matches[record_id] = [
                {
                    "source_row_index": row[0],
                    "source_compound_token": row[1],
                    "normalized_chebi_id": row[2],
                    "name": row[3],
                    "side": row[4],
                    "source_count": row[5],
                }
                for row in rows
            ]
        return {"filters": filters, "matches": matches}
    finally:
        connection.close()
