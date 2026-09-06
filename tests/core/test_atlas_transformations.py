from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from catalytic_earth.atlas_transformations import (
    apply_graph_edits,
    replay_graph_edits,
    transformation_payload_sha256,
    validate_transformations,
)


ROOT = Path(__file__).resolve().parents[2]
TRANSFORMATIONS = ROOT / "data/atlas/transformations/m0187/transformations.json"
ATLAS10 = ROOT / "src/catalytic_earth/atlas_data/atlas10_kernel.json"


def _repin_review(value: dict) -> None:
    value["review"]["reviewed_payload_sha256"] = transformation_payload_sha256(value)


def _transformation(value: dict) -> dict:
    [row] = value["transformations"]
    return row


def _edit(row: dict, edit_id: str) -> dict:
    return next(
        item
        for item in row["panel_correspondence"]["graph_edits"]
        if item["edit_id"] == edit_id
    )


def _atom(graph: dict, atom_id: str) -> dict:
    return next(item for item in graph["atoms"] if item["atom_id"] == atom_id)


def _replace_atom_token(value, left: str, right: str):
    """Rename panel-local locators throughout project-authored claim layers."""

    if isinstance(value, dict):
        return {
            key: _replace_atom_token(item, left, right)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_replace_atom_token(item, left, right) for item in value]
    if value == left:
        return right
    if value == right:
        return left
    return value


class TransformationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.value = json.loads(TRANSFORMATIONS.read_text(encoding="utf-8"))
        cls.atlas10 = json.loads(ATLAS10.read_text(encoding="utf-8"))

    def validate(self, value: dict, *, repo_root: Path | None = None) -> dict:
        return validate_transformations(
            value,
            atlas10_bundle=self.atlas10,
            repo_root=repo_root,
        )

    def reviewed_copy(self) -> dict:
        value = copy.deepcopy(self.value)
        _repin_review(value)
        return value

    def test_reviewed_primitive_replays_all_declared_changes(self) -> None:
        value = self.reviewed_copy()
        summary = self.validate(value, repo_root=ROOT)
        self.assertEqual(summary["transformation_count"], 1)
        self.assertEqual(summary["record_count"], 1)

        row = _transformation(value)
        panel = row["panel_correspondence"]
        edits = panel["graph_edits"]
        self.assertEqual(len(edits), 9)
        self.assertEqual(
            {item["operation"] for item in edits},
            {
                "add_bond",
                "remove_bond",
                "set_bond_order",
                "set_formal_charge",
                "set_stereochemistry",
            },
        )
        self.assertTrue(
            replay_graph_edits(
                panel["before_graph"],
                edits,
                panel["after_graph"],
                panel["replay"]["atom_map"],
            )
        )
        applied = apply_graph_edits(panel["before_graph"], edits)
        self.assertEqual(_atom(applied, "a58")["formal_charge"], 1)
        self.assertEqual(_atom(applied, "a63")["formal_charge"], -1)
        self.assertIsNone(_atom(applied, "a9")["stereochemistry"])
        self.assertEqual(panel["replay"]["raw_kekule_map_count"], 1)
        self.assertEqual(panel["replay"]["chemical_topology_map_count"], 2)
        self.assertEqual(len(panel["chemical_map_alternatives"]), 2)
        self.assertFalse(row["scope_effect"]["canonical_product_correspondence"])
        self.assertFalse(row["scope_effect"]["complete_racemization_path"])

    def test_edit_to_arrow_assignment_cannot_be_rewritten(self) -> None:
        for coordinated in (False, True):
            with self.subTest(coordinated=coordinated):
                changed = self.reviewed_copy()
                row = _transformation(changed)
                panel = row["panel_correspondence"]
                _edit(row, "e1")["source_flow_id"] = "o40"
                if coordinated:
                    by_flow = {
                        item["flow_id"]: item
                        for item in panel["source_flow_bindings"]
                    }
                    by_flow["o37"]["edit_ids"].remove("e1")
                    by_flow["o40"]["edit_ids"].append("e1")
                _repin_review(changed)
                with self.assertRaises(ValueError):
                    self.validate(changed, repo_root=ROOT)

    def test_canonical_atom_meaning_cannot_be_permuted(self) -> None:
        changed = self.reviewed_copy()
        correspondence = _transformation(changed)["canonical_input_correspondence"]
        for alternative in correspondence["map_alternatives"]:
            for mapping in alternative["canonical_to_before"]:
                if mapping["canonical_atom_id"] == "8":
                    mapping["canonical_atom_id"] = "9"
                elif mapping["canonical_atom_id"] == "9":
                    mapping["canonical_atom_id"] = "8"
        for item in correspondence["invariant_reactive_core"]:
            if item["canonical_atom_id"] == "8":
                item["canonical_atom_id"] = "9"
            elif item["canonical_atom_id"] == "9":
                item["canonical_atom_id"] = "8"
        _repin_review(changed)
        with self.assertRaises(ValueError):
            self.validate(changed, repo_root=ROOT)

    def test_input_stereochemistry_and_raw_identifier_are_source_bound(self) -> None:
        changed_stereo = self.reviewed_copy()
        row = _transformation(changed_stereo)
        panel = row["panel_correspondence"]
        _atom(panel["before_graph"], "a9")["stereochemistry"] = "S"
        _edit(row, "e9")["before"] = "S"
        panel["stereochemistry"]["before_assignment"] = "S"

        changed_label = self.reviewed_copy()
        _transformation(changed_label)["canonical_input_correspondence"][
            "raw_source_labels"
        ] = ["chebi:32382"]

        for label, changed in (
            ("stereochemistry", changed_stereo),
            ("raw_identifier", changed_label),
        ):
            with self.subTest(label=label):
                _repin_review(changed)
                with self.assertRaises(ValueError):
                    self.validate(changed, repo_root=ROOT)

    def test_correlated_audit_repin_cannot_rewrite_raw_mrv_identifier(self) -> None:
        changed = self.reviewed_copy()
        _transformation(changed)["canonical_input_correspondence"][
            "raw_source_labels"
        ] = ["chebi:17757"]
        _transformation(changed)["canonical_input_correspondence"][
            "rejected_participant_matches"
        ] = [
            {
                "participant_id": "CHEBI:17757",
                "chirality_sensitive_match_count": 0,
            }
        ]
        audit_binding = next(
            item
            for item in changed["source_bindings"]
            if item["artifact_kind"] == "computational_audit_result"
        )

        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            for binding in changed["source_bindings"]:
                source = ROOT / binding["path"]
                target = temp_root / binding["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)

            audit_path = temp_root / audit_binding["path"]
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            for step in audit["steps"]:
                if step["step_id"] in (1, 2):
                    for atom in step["ligand_atoms"]:
                        if atom.get("raw_label") == "chebi:17756":
                            atom["raw_label"] = "chebi:17757"
            audit["complete_panel_canonical_participant_matches"]["1"][
                "CHEBI:17757:chiral"
            ] = {"count": 0, "source_atom_maps": []}
            audit_path.write_text(
                json.dumps(audit, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            audit_binding["sha256"] = hashlib.sha256(
                audit_path.read_bytes()
            ).hexdigest()
            _repin_review(changed)

            # The claim and its computational audit agree on the false label,
            # while the retained MRV remains the decisive counter-witness. The
            # alternative false label still satisfies the generic
            # selected-versus-rejected conflict shape.
            self.validate(changed)
            with self.assertRaises(ValueError):
                self.validate(changed, repo_root=temp_root)

    def test_rhea_directional_child_cannot_be_replaced(self) -> None:
        changed = self.reviewed_copy()
        reaction = _transformation(changed)["canonical_reaction_binding"]
        reaction["directed_id"] = "RHEA:13947"
        reaction["directed_direction_code"] = "RL"
        _repin_review(changed)
        with self.assertRaises(ValueError):
            self.validate(changed, repo_root=ROOT)

    def test_swapped_r_and_s_reference_is_rejected(self) -> None:
        changed = self.reviewed_copy()
        canonical = _transformation(changed)["canonical_input_correspondence"]
        canonical["participant_id"] = "CHEBI:17756"
        canonical["participant_structure_binding_id"] = (
            "official:Rhea:CHEBI:17756:mol"
        )
        canonical["rejected_participant_matches"] = [
            {
                "participant_id": "CHEBI:32382",
                "chirality_sensitive_match_count": 0,
            }
        ]
        audit_binding = next(
            item
            for item in changed["source_bindings"]
            if item["artifact_kind"] == "computational_audit_result"
        )

        with tempfile.TemporaryDirectory() as directory:
            temp_root = Path(directory)
            for binding in changed["source_bindings"]:
                source = ROOT / binding["path"]
                target = temp_root / binding["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            audit_path = temp_root / audit_binding["path"]
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            matches = audit["complete_panel_canonical_participant_matches"]["1"]
            matches["CHEBI:17756:chiral"] = copy.deepcopy(
                matches["CHEBI:32382:chiral"]
            )
            matches["CHEBI:32382:chiral"] = {
                "count": 0,
                "source_atom_maps": [],
            }
            audit_path.write_text(
                json.dumps(audit, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            audit_binding["sha256"] = hashlib.sha256(
                audit_path.read_bytes()
            ).hexdigest()
            _repin_review(changed)

            with self.assertRaises(ValueError):
                self.validate(changed, repo_root=temp_root)

    def test_coherent_wrong_proton_transfer_or_charge_fails_raw_panels(self) -> None:
        wrong_transfer = self.reviewed_copy()
        row = _transformation(wrong_transfer)
        panel = row["panel_correspondence"]
        _edit(row, "e4")["atom_ids"] = ["a64", "a65"]
        bond = next(
            item
            for item in panel["after_graph"]["bonds"]
            if set(item["atom_ids"]) == {"a10", "a65"}
        )
        bond["atom_ids"] = ["a64", "a65"]

        wrong_charge = self.reviewed_copy()
        row = _transformation(wrong_charge)
        panel = row["panel_correspondence"]
        _edit(row, "e7")["after"] = 1
        _atom(panel["after_graph"], "a63")["formal_charge"] = 1

        for label, changed in (
            ("proton_transfer", wrong_transfer),
            ("formal_charge", wrong_charge),
        ):
            with self.subTest(label=label):
                _repin_review(changed)
                # The false edit and false after graph agree with each other.
                false_panel = _transformation(changed)["panel_correspondence"]
                self.assertTrue(
                    replay_graph_edits(
                        false_panel["before_graph"],
                        false_panel["graph_edits"],
                        false_panel["after_graph"],
                        false_panel["replay"]["atom_map"],
                    )
                )
                with self.assertRaises(ValueError):
                    self.validate(changed, repo_root=ROOT)

    def test_symmetry_alternatives_must_be_distinct(self) -> None:
        canonical_duplicate = self.reviewed_copy()
        canonical = _transformation(canonical_duplicate)[
            "canonical_input_correspondence"
        ]
        duplicate = copy.deepcopy(canonical["map_alternatives"][0])
        duplicate["map_id"] = canonical["map_alternatives"][1]["map_id"]
        canonical["map_alternatives"][1] = duplicate

        chemical_duplicate = self.reviewed_copy()
        maps = _transformation(chemical_duplicate)["panel_correspondence"][
            "chemical_map_alternatives"
        ]
        duplicate = copy.deepcopy(maps[0])
        duplicate["map_id"] = maps[1]["map_id"]
        maps[1] = duplicate

        for label, changed in (
            ("canonical", canonical_duplicate),
            ("chemical_topology", chemical_duplicate),
        ):
            with self.subTest(label=label):
                _repin_review(changed)
                with self.assertRaises(ValueError):
                    self.validate(changed)

    def test_panel_local_locator_renaming_is_not_source_identity_proof(self) -> None:
        changed = self.reviewed_copy()
        changed["transformations"][0] = _replace_atom_token(
            changed["transformations"][0], "a8", "a9"
        )
        _repin_review(changed)
        # Renaming every project-authored occurrence must not turn panel-local
        # locator tokens into independent atom-identity evidence.
        with self.assertRaises(ValueError):
            self.validate(changed, repo_root=ROOT)

    def test_product_and_complete_path_abstentions_cannot_be_promoted(self) -> None:
        for scope_key in (
            "canonical_product_correspondence",
            "net_reaction_atom_map",
            "complete_racemization_path",
            "inferred_return_step",
        ):
            with self.subTest(scope_key=scope_key):
                changed = self.reviewed_copy()
                _transformation(changed)["scope_effect"][scope_key] = True
                _repin_review(changed)
                with self.assertRaises(ValueError):
                    self.validate(changed)

    def test_h67_representation_boundary_cannot_be_erased(self) -> None:
        changed = self.reviewed_copy()
        row = _transformation(changed)
        row["mandatory_abstentions"] = [
            item
            for item in row["mandatory_abstentions"]
            if item["abstention_id"] != "step2_explicit_h67_lineage"
        ]
        panel = row["panel_correspondence"]
        panel["representation_boundaries"] = [
            item
            for item in panel["representation_boundaries"]
            if item["boundary_id"] != "lys166_h67_explicitness"
        ]
        _repin_review(changed)
        with self.assertRaises(ValueError):
            self.validate(changed, repo_root=ROOT)


if __name__ == "__main__":
    unittest.main()
