from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest

from catalytic_earth.atlas_partial_panels import (
    comparison_payload_sha256,
    derive_partial_panel_coverage,
    validate_panel_comparisons,
)
from catalytic_earth.atlas_transformations import (
    replay_graph_edits,
    validate_transformations,
)


ROOT = Path(__file__).resolve().parents[2]
COMPARISONS = ROOT / "data/atlas/panel_comparisons/m0173/comparisons.json"
ATLAS10 = ROOT / "src/catalytic_earth/atlas_data/atlas10_kernel.json"
M0173_TRANSFORMATIONS = ROOT / "data/atlas/transformations/m0173/transformations.json"
M0187_TRANSFORMATIONS = ROOT / "data/atlas/transformations/m0187/transformations.json"


def _repin_review(value: dict) -> None:
    value["review"]["status"] = "accepted"
    value["review"]["reviewed_payload_sha256"] = comparison_payload_sha256(value)


def _row(value: dict) -> dict:
    [row] = value["comparisons"]
    return row


def _atom(graph: dict, atom_id: str) -> dict:
    return next(item for item in graph["atoms"] if item["atom_id"] == atom_id)


def _edit(row: dict, edit_id: str) -> dict:
    return next(item for item in row["proposed_graph_edits"] if item["edit_id"] == edit_id)


def _project_graph(graph: dict, atom_ids: set[str], suffix: str) -> dict:
    return {
        "graph_id": f"{graph['graph_id']}:{suffix}",
        "atom_id_scope": graph["atom_id_scope"],
        "atoms": [item for item in graph["atoms"] if item["atom_id"] in atom_ids],
        "bonds": [
            item for item in graph["bonds"] if set(item["atom_ids"]) <= atom_ids
        ],
    }


def _records(value):
    if isinstance(value, dict):
        if isinstance(value.get("record_id"), str):
            yield value
        for item in value.values():
            yield from _records(item)
    elif isinstance(value, list):
        for item in value:
            yield from _records(item)


class PartialPanelComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.value = json.loads(COMPARISONS.read_text(encoding="utf-8"))
        cls.atlas10 = json.loads(ATLAS10.read_text(encoding="utf-8"))

    def reviewed_copy(self) -> dict:
        value = copy.deepcopy(self.value)
        _repin_review(value)
        return value

    def validate(
        self,
        value: dict,
        *,
        atlas10: dict | None = None,
        repo_root: Path | None = None,
    ) -> dict:
        return validate_panel_comparisons(
            value,
            atlas10_bundle=self.atlas10 if atlas10 is None else atlas10,
            repo_root=repo_root,
        )

    def test_real_partial_comparison_replays_only_retained_core(self) -> None:
        value = self.reviewed_copy()
        summary = self.validate(value, repo_root=ROOT)
        self.assertEqual(summary["comparison_count"], 1)
        self.assertEqual(summary["record_count"], 1)

        row = _row(value)
        coverage = row["coverage"]
        self.assertEqual(
            (
                coverage["before_node_count"],
                coverage["after_node_count"],
                coverage["mapped_node_count"],
            ),
            (50, 42, 40),
        )
        self.assertEqual(set(coverage["replayed_edit_ids"]), {"e4", "e5", "e6"})
        self.assertEqual(
            set(coverage["after_graph_unverified_edit_ids"]), {"e1", "e2", "e3"}
        )
        self.assertEqual(
            set(coverage["source_flow_covered_edit_ids"]),
            {"e1", "e2", "e3", "e4", "e5", "e6"},
        )
        self.assertEqual(set(coverage["source_flow_ids"]), {"o24", "o25", "o26"})
        self.assertEqual(
            (
                coverage["full_before_formal_charge"],
                coverage["full_after_formal_charge"],
                coverage["projected_before_formal_charge"],
                coverage["projected_after_formal_charge"],
            ),
            (-1, 0, 0, 0),
        )
        self.assertTrue(coverage["projection_replays_exactly"])
        self.assertFalse(coverage["full_panel_replay_asserted"])

        mapping = row["correspondence"]["atom_map"]
        before_ids = {item["before_atom_id"] for item in mapping}
        after_ids = {item["after_atom_id"] for item in mapping}
        before = _project_graph(
            row["source_panels"]["before_graph"], before_ids, "retained-core"
        )
        after = _project_graph(
            row["source_panels"]["after_graph"], after_ids, "retained-core"
        )
        replayed = [
            item
            for item in row["proposed_graph_edits"]
            if item["edit_id"] in coverage["replayed_edit_ids"]
        ]
        self.assertTrue(replay_graph_edits(before, replayed, after, mapping))

    def test_unmatched_inventories_and_boundary_edges_are_exact(self) -> None:
        row = _row(self.reviewed_copy())
        coverage = row["coverage"]
        self.assertEqual(
            set(coverage["unmatched_before_atom_ids"]),
            {"a4", "a5", "a6", "a7", "a8", "a9", "a12", "a13", "a14", "a50"},
        )
        self.assertEqual(set(coverage["unmatched_after_atom_ids"]), {"a6", "a7"})
        self.assertEqual(
            {
                (frozenset(item["atom_ids"]), item["order"])
                for item in coverage["before_boundary_bonds"]
            },
            {(frozenset(("a3", "a4")), 1), (frozenset(("a21", "a50")), 1)},
        )
        self.assertEqual(coverage["after_boundary_bonds"], [])

        abstentions = {item["abstention_id"] for item in row["mandatory_abstentions"]}
        self.assertIn("water_hydrogen_correspondence", abstentions)
        self.assertIn("released_peptide_after_graph", abstentions)
        self.assertTrue(row["scope_effect"]["retained_projection_replay"])
        self.assertTrue(
            all(
                not enabled
                for key, enabled in row["scope_effect"].items()
                if key != "retained_projection_replay"
            )
        )

    def test_water_redraw_cannot_be_promoted_into_locator_map(self) -> None:
        changed = self.reviewed_copy()
        mapping = _row(changed)["correspondence"]["atom_map"]
        mapping.append({"before_atom_id": "a13", "after_atom_id": "a7"})
        _repin_review(changed)
        with self.assertRaises(ValueError):
            self.validate(changed)

    def test_unverified_source_edits_cannot_be_promoted_to_replay(self) -> None:
        changed = self.reviewed_copy()
        coverage = _row(changed)["coverage"]
        coverage["after_graph_unverified_edit_ids"].remove("e1")
        coverage["replayed_edit_ids"].append("e1")
        _repin_review(changed)
        with self.assertRaises(ValueError):
            self.validate(changed)

    def test_boundary_edge_and_edit_preconditions_are_derived(self) -> None:
        missing_boundary = self.reviewed_copy()
        _row(missing_boundary)["coverage"]["before_boundary_bonds"] = [
            item
            for item in _row(missing_boundary)["coverage"]["before_boundary_bonds"]
            if set(item["atom_ids"]) != {"a3", "a4"}
        ]

        wrong_precondition = self.reviewed_copy()
        _edit(_row(wrong_precondition), "e1")["atom_ids"] = ["a3", "a5"]

        for label, changed in (
            ("boundary", missing_boundary),
            ("edit_precondition", wrong_precondition),
        ):
            with self.subTest(label=label):
                _repin_review(changed)
                with self.assertRaises(ValueError):
                    self.validate(changed)

    def test_source_arrow_endpoint_edits_cannot_be_omitted(self) -> None:
        for removed_ids in ({"e2"}, {"e1", "e2"}):
            with self.subTest(removed_ids=sorted(removed_ids)):
                changed = self.reviewed_copy()
                row = _row(changed)
                row["proposed_graph_edits"] = [
                    item
                    for item in row["proposed_graph_edits"]
                    if item["edit_id"] not in removed_ids
                ]
                for flow in row["source_flow_bindings"]:
                    flow["edit_ids"] = [
                        item for item in flow["edit_ids"] if item not in removed_ids
                    ]
                row["source_flow_bindings"] = [
                    item for item in row["source_flow_bindings"] if item["edit_ids"]
                ]
                row["coverage"] = derive_partial_panel_coverage(
                    row["source_panels"]["before_graph"],
                    row["source_panels"]["after_graph"],
                    row["correspondence"]["atom_map"],
                    row["proposed_graph_edits"],
                    row["source_flow_bindings"],
                )
                _repin_review(changed)

                # Removing e2 hides the source-depicted N4-H50 target while
                # leaving the three-edit retained projection unchanged.
                with self.assertRaises(ValueError):
                    self.validate(changed, repo_root=ROOT)

    def test_coherent_wrong_core_charge_fails_retained_after_panel(self) -> None:
        changed = self.reviewed_copy()
        row = _row(changed)
        _edit(row, "e6")["after"] = 1
        _atom(row["source_panels"]["after_graph"], "a4")["formal_charge"] = 1
        row["coverage"]["full_after_formal_charge"] = 1
        row["coverage"]["projected_after_formal_charge"] = 1
        _repin_review(changed)

        self.validate(changed)
        with self.assertRaises(ValueError):
            self.validate(changed, repo_root=ROOT)

    def test_coordinated_missing_unmatched_node_fails_full_raw_panel(self) -> None:
        changed = self.reviewed_copy()
        row = _row(changed)
        before = row["source_panels"]["before_graph"]
        before["atoms"] = [item for item in before["atoms"] if item["atom_id"] != "a7"]
        before["bonds"] = [
            item for item in before["bonds"] if "a7" not in item["atom_ids"]
        ]
        row["source_panels"]["before_nodes"] = [
            item
            for item in row["source_panels"]["before_nodes"]
            if item["atom_id"] != "a7"
        ]
        coverage = row["coverage"]
        coverage["before_node_count"] = 49
        coverage["unmatched_before_atom_ids"].remove("a7")
        coverage["full_before_formal_charge"] = 0
        _repin_review(changed)

        self.validate(changed)
        with self.assertRaises(ValueError):
            self.validate(changed, repo_root=ROOT)

    def test_compiled_flow_and_claim_cannot_replace_raw_step_2_arrow(self) -> None:
        changed = self.reviewed_copy()
        row = _row(changed)
        atlas10 = copy.deepcopy(self.atlas10)
        record = next(
            item
            for item in _records(atlas10)
            if item.get("record_id") == row["record_binding"]["record_id"]
        )
        proposal = next(
            item
            for item in record["mechanism_proposals"]
            if item["proposal_id"] == row["proposal_binding"]["proposal_id"]
        )
        step = next(
            item
            for item in proposal["mechanism_steps"]
            if item["source_step_id"] == row["state_pair"]["before"]["source_step_id"]
        )
        next(item for item in step["electron_flows"] if item["flow_id"] == "o24")[
            "flow_id"
        ] = "o99"
        for edit in row["proposed_graph_edits"]:
            if edit["source_flow_id"] == "o24":
                edit["source_flow_id"] = "o99"
        next(item for item in row["source_flow_bindings"] if item["flow_id"] == "o24")[
            "flow_id"
        ] = "o99"
        row["coverage"] = derive_partial_panel_coverage(
            row["source_panels"]["before_graph"],
            row["source_panels"]["after_graph"],
            row["correspondence"]["atom_map"],
            row["proposed_graph_edits"],
            row["source_flow_bindings"],
        )
        _repin_review(changed)

        self.validate(changed, atlas10=atlas10)
        with self.assertRaises(ValueError):
            self.validate(changed, atlas10=atlas10, repo_root=ROOT)

    def test_missing_evidence_cannot_be_rewritten_as_physical_or_complete(self) -> None:
        row = _row(self.reviewed_copy())
        unsupported = [
            key for key, enabled in row["scope_effect"].items() if not enabled
        ]
        for key in unsupported:
            with self.subTest(scope=key):
                changed = self.reviewed_copy()
                _row(changed)["scope_effect"][key] = True
                _repin_review(changed)
                with self.assertRaises(ValueError):
                    self.validate(changed)

        changed = self.reviewed_copy()
        _row(changed)["mandatory_abstentions"] = [
            item
            for item in _row(changed)["mandatory_abstentions"]
            if item["abstention_id"] != "released_peptide_after_graph"
        ]
        _repin_review(changed)
        with self.assertRaises(ValueError):
            self.validate(changed)

    def test_existing_complete_transformation_sets_remain_byte_identical(self) -> None:
        expected = {
            M0173_TRANSFORMATIONS: "b4150239ea101e22046d416c685bdf88a01a047b0c6b6d376f206a551644d82c",
            M0187_TRANSFORMATIONS: "02135996931cd366945fad1773b1ca067f13cb609a17a56862ebfc91f5d28fa3",
        }
        for path, digest in expected.items():
            with self.subTest(path=path.name):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)
                summary = validate_transformations(
                    json.loads(path.read_text(encoding="utf-8")),
                    atlas10_bundle=self.atlas10,
                    repo_root=ROOT,
                )
                self.assertEqual(summary["transformation_count"], 1)


if __name__ == "__main__":
    unittest.main()
