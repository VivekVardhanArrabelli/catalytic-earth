from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from catalytic_earth.atlas_transformations import (
    apply_graph_edits,
    replay_graph_edits,
    transformation_payload_sha256,
    validate_transformations,
)


ROOT = Path(__file__).resolve().parents[2]
TRANSFORMATIONS = ROOT / "data/atlas/transformations/m0173/transformations.json"
ATLAS10 = ROOT / "src/catalytic_earth/atlas_data/atlas10_kernel.json"


def _repin_review(value: dict) -> None:
    value["review"]["reviewed_payload_sha256"] = transformation_payload_sha256(value)


def _row(value: dict) -> dict:
    [row] = value["transformations"]
    return row


def _atom(graph: dict, atom_id: str) -> dict:
    return next(item for item in graph["atoms"] if item["atom_id"] == atom_id)


def _edit(row: dict, *, operation: str, atom_ids: set[str]) -> dict:
    return next(
        item
        for item in row["panel_correspondence"]["graph_edits"]
        if item["operation"] == operation and set(item["atom_ids"]) == atom_ids
    )


def _remove_atom(graph: dict, atom_id: str) -> None:
    graph["atoms"] = [item for item in graph["atoms"] if item["atom_id"] != atom_id]
    graph["bonds"] = [
        item for item in graph["bonds"] if atom_id not in item["atom_ids"]
    ]


def _records(value):
    if isinstance(value, dict):
        if isinstance(value.get("record_id"), str):
            yield value
        for item in value.values():
            yield from _records(item)
    elif isinstance(value, list):
        for item in value:
            yield from _records(item)


class M0173TransformationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.value = json.loads(TRANSFORMATIONS.read_text(encoding="utf-8"))
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
        return validate_transformations(
            value,
            atlas10_bundle=self.atlas10 if atlas10 is None else atlas10,
            repo_root=repo_root,
        )

    def test_real_source_panel_primitive_replays_exact_six_edits(self) -> None:
        value = self.reviewed_copy()
        summary = self.validate(value, repo_root=ROOT)
        self.assertEqual(summary["transformation_count"], 1)
        self.assertEqual(summary["record_count"], 1)

        row = _row(value)
        self.assertEqual(row["record_binding"]["mcsa_id"], "M0173")
        panel = row["panel_correspondence"]
        before = panel["before_graph"]
        after = panel["after_graph"]
        edits = panel["graph_edits"]
        self.assertEqual((len(before["atoms"]), len(after["atoms"])), (50, 50))
        self.assertEqual((len(before["bonds"]), len(after["bonds"])), (42, 43))
        self.assertEqual(len(edits), 6)
        self.assertTrue(
            replay_graph_edits(before, edits, after, panel["replay"]["atom_map"])
        )

        applied = apply_graph_edits(before, edits)
        self.assertEqual(_atom(applied, "a10")["formal_charge"], -1)
        self.assertEqual(_atom(applied, "a21")["formal_charge"], 1)
        self.assertTrue(
            any(set(item["atom_ids"]) == {"a3", "a44"} for item in applied["bonds"])
        )
        self.assertTrue(
            any(set(item["atom_ids"]) == {"a21", "a50"} for item in applied["bonds"])
        )
        self.assertFalse(
            any(set(item["atom_ids"]) == {"a44", "a50"} for item in applied["bonds"])
        )
        self.assertTrue(
            all(
                atom["stereochemistry"] is None
                for graph in (before, after)
                for atom in graph["atoms"]
            )
        )

    def test_generic_peptide_tokens_and_aliases_remain_unresolved(self) -> None:
        value = self.reviewed_copy()
        self.validate(value, repo_root=ROOT)
        row = _row(value)
        context = row["source_context"]
        annotations = {
            item["atom_id"]: item
            for item in context["source_atom_annotations"]["rows"]
        }
        groups = context["source_r_groups"]

        self.assertEqual(set(groups["element_r_atom_ids"]), {"a9", "a11"})
        self.assertEqual(
            set(groups["alias_r_atom_ids"]),
            {"a28", "a30", "a33", "a35", "a38", "a40", "a46", "a48"},
        )
        self.assertEqual(annotations["a21"]["mrv_extra_label"], "res:His56A")
        self.assertEqual(annotations["a9"]["mrv_extra_label"], "chebi:90799")
        self.assertNotIn("a10", annotations)
        self.assertIsNone(annotations["a11"]["mrv_extra_label"])
        self.assertEqual(context["canonical_participant_correspondence"], "not_asserted")
        self.assertFalse(groups["expansion_asserted"])

    def test_coherent_false_bond_and_charge_replays_fail_raw_panels(self) -> None:
        wrong_bond = self.reviewed_copy()
        row = _row(wrong_bond)
        panel = row["panel_correspondence"]
        edit = _edit(row, operation="add_bond", atom_ids={"a3", "a44"})
        edit["atom_ids"] = ["a3", "a50"]
        bond = next(
            item
            for item in panel["after_graph"]["bonds"]
            if set(item["atom_ids"]) == {"a3", "a44"}
        )
        bond["atom_ids"] = ["a3", "a50"]

        wrong_charge = self.reviewed_copy()
        row = _row(wrong_charge)
        panel = row["panel_correspondence"]
        charge = _edit(row, operation="set_formal_charge", atom_ids={"a10"})
        charge["after"] = 1
        _atom(panel["after_graph"], "a10")["formal_charge"] = 1

        for label, changed in (("bond", wrong_bond), ("charge", wrong_charge)):
            with self.subTest(label=label):
                _repin_review(changed)
                changed_panel = _row(changed)["panel_correspondence"]
                self.assertTrue(
                    replay_graph_edits(
                        changed_panel["before_graph"],
                        changed_panel["graph_edits"],
                        changed_panel["after_graph"],
                        changed_panel["replay"]["atom_map"],
                    )
                )
                with self.assertRaises(ValueError):
                    self.validate(changed, repo_root=ROOT)

    def test_source_step_and_arrow_witness_cannot_be_reassigned(self) -> None:
        changed = self.reviewed_copy()
        row = _row(changed)
        flow = next(
            item
            for item in row["panel_correspondence"]["source_flow_bindings"]
            if item["flow_id"] == "o24"
        )
        flow["source_step_id"] = 2
        _repin_review(changed)
        with self.assertRaises(ValueError):
            self.validate(changed, repo_root=ROOT)

    def test_compiled_flow_and_claim_cannot_repin_away_from_raw_arrow(self) -> None:
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
        next(item for item in step["electron_flows"] if item["flow_id"] == "o25")[
            "flow_id"
        ] = "o99"
        panel = row["panel_correspondence"]
        for edit in panel["graph_edits"]:
            if edit["source_flow_id"] == "o25":
                edit["source_flow_id"] = "o99"
        next(
            item for item in panel["source_flow_bindings"] if item["flow_id"] == "o25"
        )["flow_id"] = "o99"
        _repin_review(changed)

        # The compiled view and authored claim now agree, but the retained MRV
        # still names the arrow o25. Repository validation must use that raw
        # counter-witness rather than accepting the coordinated rewrite.
        with self.assertRaises(ValueError):
            self.validate(changed, atlas10=atlas10, repo_root=ROOT)

    def test_coordinated_r_group_and_alias_rewrites_fail_raw_mrvs(self) -> None:
        changed_r = self.reviewed_copy()
        row = _row(changed_r)
        panel = row["panel_correspondence"]
        for graph in (panel["before_graph"], panel["after_graph"]):
            _atom(graph, "a9")["element"] = "C"
        row["source_context"]["source_r_groups"]["element_r_atom_ids"].remove("a9")

        changed_alias = self.reviewed_copy()
        annotations = _row(changed_alias)["source_context"][
            "source_atom_annotations"
        ]["rows"]
        next(item for item in annotations if item["atom_id"] == "a21")[
            "mrv_extra_label"
        ] = "res:His57A"

        for label, changed in (("element_R", changed_r), ("His_alias", changed_alias)):
            with self.subTest(label=label):
                _repin_review(changed)
                self.validate(changed)
                with self.assertRaises(ValueError):
                    self.validate(changed, repo_root=ROOT)

    def test_coordinated_missing_depiction_node_fails_raw_panel(self) -> None:
        changed = self.reviewed_copy()
        row = _row(changed)
        panel = row["panel_correspondence"]
        for graph in (panel["before_graph"], panel["after_graph"]):
            _remove_atom(graph, "a28")
        panel["replay"]["atom_map"] = [
            item
            for item in panel["replay"]["atom_map"]
            if item["before_atom_id"] != "a28" and item["after_atom_id"] != "a28"
        ]
        context = row["source_context"]
        context["source_atom_annotations"]["rows"] = [
            item
            for item in context["source_atom_annotations"]["rows"]
            if item["atom_id"] != "a28"
        ]
        context["source_r_groups"]["alias_r_atom_ids"].remove("a28")
        _repin_review(changed)

        self.validate(changed)
        with self.assertRaises(ValueError):
            self.validate(changed, repo_root=ROOT)

    def test_stereo_identity_and_path_promotions_are_rejected(self) -> None:
        stereo = self.reviewed_copy()
        for graph in (
            _row(stereo)["panel_correspondence"]["before_graph"],
            _row(stereo)["panel_correspondence"]["after_graph"],
        ):
            _atom(graph, "a3")["stereochemistry"] = "R"

        physical = self.reviewed_copy()
        _row(physical)["scope_effect"]["exact_physical_peptide_identity"] = True

        complete = self.reviewed_copy()
        _row(complete)["scope_effect"]["complete_mechanism_path"] = True

        canonical = self.reviewed_copy()
        _row(canonical)["canonical_input_correspondence"] = {"status": "asserted"}

        for label, changed in (
            ("stereochemistry", stereo),
            ("physical_peptide", physical),
            ("complete_path", complete),
            ("canonical_bridge", canonical),
        ):
            with self.subTest(label=label):
                _repin_review(changed)
                with self.assertRaises(ValueError):
                    self.validate(changed)


if __name__ == "__main__":
    unittest.main()
