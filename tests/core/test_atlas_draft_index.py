"""Focused tests for exact Atlas source-participant indexing."""

from __future__ import annotations

import copy
import hashlib
import unittest
from pathlib import Path

from catalytic_earth.atlas_draft_index import (
    match_source_participants,
    materialize_source_drafts,
    normalize_chebi_id,
)
from catalytic_earth.atlas_drafts import build_source_drafts, canonical_json_bytes


ROOT = Path(__file__).resolve().parents[2]


def _record(bundle: dict, mcsa_id: str) -> dict:
    return next(record for record in bundle["records"] if record["mcsa_id"] == mcsa_id)


def _record_id(bundle: dict, mcsa_id: str) -> str:
    return _record(bundle, mcsa_id)["record_id"]


class AtlasDraftIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bundle = build_source_drafts(ROOT)

    def test_normalize_chebi_id_is_exact_and_canonical(self) -> None:
        for value in ("16526", "CHEBI:16526", "chebi:16526", " chebi:016526 "):
            self.assertEqual(normalize_chebi_id(value), "CHEBI:16526")
        for value in (
            "",
            "0",
            "CHEBI:0",
            "-16526",
            "CHEBI_16526",
            "CHEBI:16526.0",
            "16526 OR 1=1",
            "CHEBI:16526' OR 1=1 --",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_chebi_id(value)
        for value in (None, 16526):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_chebi_id(value)  # type: ignore[arg-type]

    def test_materializer_preserves_source_rows_and_only_two_tables(self) -> None:
        connection = materialize_source_drafts(self.bundle)
        try:
            tables = connection.execute(
                "SELECT name FROM sqlite_master WHERE type = ? ORDER BY name", ("table",)
            ).fetchall()
            self.assertEqual(tables, [("participants",), ("records",)])
            self.assertEqual(
                connection.execute(
                    "SELECT record_id FROM records ORDER BY source_order"
                ).fetchall(),
                [(record["record_id"],) for record in self.bundle["records"]],
            )
            actual = connection.execute(
                """
                SELECT p.record_id, p.source_row_index, p.source_compound_token,
                       p.normalized_chebi_id, p.name, p.side, p.source_count
                FROM participants AS p
                JOIN records AS r ON r.record_id = p.record_id
                ORDER BY r.source_order, p.source_row_index
                """
            ).fetchall()
            expected = [
                (
                    record["record_id"],
                    participant["source_row_index"],
                    participant["source_compound_token"],
                    participant["normalized_chebi_id"],
                    participant["name"],
                    participant["side"],
                    participant["source_count"],
                )
                for record in self.bundle["records"]
                for participant in record["reaction_context"]["participants"]
            ]
            self.assertEqual(actual, expected)
        finally:
            connection.close()

    def test_carbon_dioxide_product_matches_exact_source_rows(self) -> None:
        result = match_source_participants(self.bundle, products=("16526",))
        self.assertEqual(result["filters"]["products"], ["CHEBI:16526"])
        self.assertEqual(
            list(result["matches"]),
            [_record_id(self.bundle, "M0106"), _record_id(self.bundle, "M0107")],
        )
        for rows in result["matches"].values():
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["normalized_chebi_id"], "CHEBI:16526")
            self.assertEqual(rows[0]["name"], "carbon dioxide")
            self.assertEqual(rows[0]["side"], "right")
            self.assertEqual(rows[0]["source_count"], 1)

    def test_ammonium_side_distinguishes_nitrogenase_and_hisf(self) -> None:
        reactant = match_source_participants(self.bundle, reactants=["chebi:28938"])
        self.assertEqual(list(reactant["matches"]), [_record_id(self.bundle, "M0753")])
        self.assertEqual(
            [(row["side"], row["source_count"]) for row in next(iter(reactant["matches"].values()))],
            [("left", 1)],
        )

        product = match_source_participants(self.bundle, products=["28938"])
        self.assertEqual(list(product["matches"]), [_record_id(self.bundle, "M0212")])
        self.assertEqual(
            [(row["side"], row["source_count"]) for row in next(iter(product["matches"].values()))],
            [("right", 2)],
        )

    def test_all_clauses_match_within_one_record_and_respect_sides(self) -> None:
        nitrogenase = match_source_participants(
            self.bundle, reactants=["15377"], products=["28938"]
        )
        self.assertEqual(list(nitrogenase["matches"]), [_record_id(self.bundle, "M0212")])
        self.assertEqual(
            [row["source_row_index"] for row in next(iter(nitrogenase["matches"].values()))],
            [7, 10],
        )

        hisf = match_source_participants(
            self.bundle, reactants=["28938"], products=["15377"]
        )
        self.assertEqual(list(hisf["matches"]), [_record_id(self.bundle, "M0753")])

        cross_record = match_source_participants(
            self.bundle, reactants=["17245"], products=["83111"]
        )
        self.assertEqual(cross_record["matches"], {})

        wrong_side = match_source_participants(
            self.bundle, participants=["17997"], reactants=["28938"]
        )
        self.assertEqual(wrong_side["matches"], {})

    def test_filters_deduplicate_and_rows_are_a_source_ordered_union(self) -> None:
        original = copy.deepcopy(self.bundle)
        result = match_source_participants(
            self.bundle,
            participants=["30616", "chebi:030616", "CHEBI:30616"],
            reactants=["15377"],
            products=["28938"],
        )
        self.assertEqual(result["filters"]["participants"], ["CHEBI:30616"])
        rows = result["matches"][_record_id(self.bundle, "M0212")]
        self.assertEqual([row["source_row_index"] for row in rows], [5, 7, 10])
        self.assertEqual(self.bundle, original)

    def test_empty_filters_return_every_record_without_rows(self) -> None:
        result = match_source_participants(self.bundle)
        self.assertEqual(
            list(result["matches"]), [record["record_id"] for record in self.bundle["records"]]
        )
        self.assertTrue(all(rows == [] for rows in result["matches"].values()))

    def test_filter_containers_and_sql_like_values_fail_closed(self) -> None:
        for value in ("CHEBI:16526", None):
            with self.subTest(value=value), self.assertRaisesRegex(
                ValueError, "list or tuple"
            ):
                match_source_participants(self.bundle, participants=value)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            match_source_participants(self.bundle, products=["16526) OR 1=1 --"])

    def test_unmapped_source_rows_are_stored_but_cannot_identifier_match(self) -> None:
        bundle = copy.deepcopy(self.bundle)
        record = _record(bundle, "M0106")
        carbon_dioxide = next(
            participant
            for participant in record["reaction_context"]["participants"]
            if participant["normalized_chebi_id"] == "CHEBI:16526"
        )
        carbon_dioxide["source_compound_token"] = "X00676"
        carbon_dioxide["normalized_chebi_id"] = None
        projection = {
            "reaction_context": record["reaction_context"],
            "mechanism_proposals": record["mechanism_proposals"],
            "source_residue_assertions": record["source_residue_assertions"],
        }
        record["provenance"]["source_projection_sha256"] = hashlib.sha256(
            canonical_json_bytes(projection)
        ).hexdigest()

        connection = materialize_source_drafts(bundle)
        try:
            self.assertEqual(
                connection.execute(
                    """
                    SELECT source_compound_token, normalized_chebi_id, source_count
                    FROM participants WHERE record_id = ? AND source_row_index = ?
                    """,
                    (record["record_id"], carbon_dioxide["source_row_index"]),
                ).fetchone(),
                ("X00676", None, 1),
            )
        finally:
            connection.close()

        result = match_source_participants(bundle, products=["16526"])
        self.assertEqual(list(result["matches"]), [_record_id(bundle, "M0107")])


if __name__ == "__main__":
    unittest.main()
