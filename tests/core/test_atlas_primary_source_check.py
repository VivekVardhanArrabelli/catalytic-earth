from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest

from catalytic_earth import atlas_primary_source_check as CHECK
from catalytic_earth.atlas_primary_evidence import (
    canonical_annotation_payload_sha256,
    validate_primary_evidence,
)
from catalytic_earth.canonical_hash import canonical_file_sha256


REPO = Path(__file__).resolve().parents[2]
CASES = {
    "plp": (
        "data/atlas/source_drafts/batches/plp-pyruvoyl/review/primary_evidence_annotations.json",
        "data/atlas/source_drafts/batches/plp-pyruvoyl/records.json",
    ),
    "aldolase": (
        "data/atlas/source_drafts/batches/aldolase-transketolase/review/primary_evidence_annotations.json",
        "data/atlas/source_drafts/batches/aldolase-transketolase/records.json",
    ),
}


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _annotation(sidecar: dict, annotation_id: str) -> dict:
    return next(row for row in sidecar["annotations"] if row["annotation_id"] == annotation_id)


def _copy_case(tmp_path: Path, case: str) -> tuple[dict, dict, Path]:
    sidecar_path, bundle_path = CASES[case]
    sidecar = _read_json(REPO / sidecar_path)
    bundle = _read_json(REPO / bundle_path)
    for binding in sidecar["source_bindings"]:
        source = REPO / binding["path"]
        target = tmp_path / binding["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return sidecar, bundle, tmp_path


def _projection(sidecar: dict, annotation: dict, root: Path) -> tuple[dict, dict, Path]:
    binding_id = annotation["projection_binding"]["binding_id"]
    binding = next(row for row in sidecar["source_bindings"] if row["binding_id"] == binding_id)
    path = root / binding["path"]
    return _read_json(path), binding, path


def _repin(sidecar: dict, projection: dict, binding: dict, path: Path) -> None:
    _write_json(path, projection)
    binding["sha256"] = canonical_file_sha256(path)
    sidecar["review"]["annotation_payload_sha256"] = canonical_annotation_payload_sha256(sidecar)


def _walk(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


class PrimaryStructureSourceAuditTests(unittest.TestCase):
    def test_real_retained_structures_rederive_exact_declared_facts(self) -> None:
        plp_sidecar = _read_json(REPO / CASES["plp"][0])
        aldolase_sidecar = _read_json(REPO / CASES["aldolase"][0])
        plp = CHECK.audit_primary_structure_evidence(plp_sidecar, REPO)
        aldolase = CHECK.audit_primary_structure_evidence(aldolase_sidecar, REPO)
        self.assertEqual(
            [(row["pdb_id"], row["structure_instance_count"]) for row in plp["annotations"]],
            [("1PYA", 1), ("1PWH", 4), ("1L6G", 2)],
        )
        self.assertEqual(
            [row["connection_inventory_row_count"] for row in plp["annotations"]],
            [0, 26, 4],
        )
        self.assertEqual(aldolase["annotations"][0]["pdb_id"], "2QUT")
        self.assertEqual(aldolase["annotations"][0]["structure_instance_count"], 4)
        self.assertEqual(aldolase["annotations"][0]["attachment_count"], 4)
        self.assertEqual(aldolase["annotations"][0]["bond_and_atom_check_count"], 2)

    def test_correlated_attachment_endpoint_repin_is_rejected_by_raw_cif(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, bundle, root = _copy_case(Path(directory), "aldolase")
            annotation = _annotation(sidecar, "m0222.2qut.13p-protein-covalent-enamine-context")
            projection, binding, path = _projection(sidecar, annotation, root)
            for document in (annotation, projection):
                for value in _walk(document):
                    if isinstance(value, dict) and value.get("connection_id") == "covale1":
                        endpoint = value.get("protein_endpoint")
                        if isinstance(endpoint, dict):
                            endpoint["label_asym_id"] = "B"
                            endpoint["atom_author_chain_id"] = "B"
            _repin(sidecar, projection, binding, path)
            validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            with self.assertRaisesRegex(ValueError, "endpoints differ"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_correlated_three_instance_repin_cannot_drop_a_raw_instance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, bundle, root = _copy_case(Path(directory), "aldolase")
            annotation = _annotation(sidecar, "m0222.2qut.13p-protein-covalent-enamine-context")
            projection, binding, path = _projection(sidecar, annotation, root)
            for document in (annotation, projection):
                body = document["claim"] if "claim" in document else document
                body["structure_instances"] = body["structure_instances"][1:]
                body["protein_attachments"] = body["protein_attachments"][1:]
                for index, attachment in enumerate(body["protein_attachments"]):
                    attachment["observed_instance_index"] = index
                for observation in body["chemical_observations"]:
                    if observation["observation_kind"] == "deposited_modeled_instance_atom_inventory":
                        observation["modeled_instance_indices"] = [0, 1, 2]
                excerpt = document["projection_excerpt"] if "claim" in document else document
                excerpt["support_edges"] = [
                    edge for edge in excerpt["support_edges"]
                    if edge["edge_id"] != "edge:2qut-covale1"
                ]
                for edge in excerpt["support_edges"]:
                    values = edge["extracted_values"]
                    if edge["edge_kind"] == "deposited_structure_state":
                        values["structure_instances"] = values["structure_instances"][1:]
                    elif edge["edge_kind"] == "deposited_covalent_connection":
                        values["observed_instance_index"] -= 1
                    elif edge["edge_kind"] == "deposited_modeled_instance_atom_inventory":
                        values["modeled_instance_indices"] = [0, 1, 2]
                excerpt["locators"] = [
                    locator for locator in excerpt["locators"]
                    if locator["locator_id"] != "locator:2qut-covale1"
                ]
                for locator in excerpt["locators"]:
                    values = locator["extracted_values"]
                    if "structure_instances" in values:
                        values["structure_instances"] = values["structure_instances"][1:]
                    if "modeled_instance_indices" in values:
                        values["modeled_instance_indices"] = [0, 1, 2]
            _repin(sidecar, projection, binding, path)
            validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            with self.assertRaisesRegex(ValueError, "structure instances differ"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_correlated_fictitious_dictionary_omission_repin_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, bundle, root = _copy_case(Path(directory), "aldolase")
            annotation = _annotation(sidecar, "m0222.2qut.13p-protein-covalent-enamine-context")
            projection, binding, path = _projection(sidecar, annotation, root)
            for document in (annotation, projection):
                for value in _walk(document):
                    if isinstance(value, dict) and value.get("source_atom_ids") == ["C2", "O2"]:
                        value["source_atom_ids"] = ["C2", "ZZ"]
                        value["source_bond_order_code"] = "sing"
                    if isinstance(value, dict) and value.get("omitted_atom_ids") == ["O2"]:
                        value["omitted_atom_ids"] = ["ZZ"]
            _repin(sidecar, projection, binding, path)
            validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            with self.assertRaisesRegex(ValueError, "dictionary bond differs|not a dictionary atom"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_real_alternative_dictionary_bond_cannot_replace_omitted_o2(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, bundle, root = _copy_case(Path(directory), "aldolase")
            annotation = _annotation(sidecar, "m0222.2qut.13p-protein-covalent-enamine-context")
            projection, binding, path = _projection(sidecar, annotation, root)
            for document in (annotation, projection):
                for value in _walk(document):
                    if isinstance(value, dict) and value.get("source_atom_ids") == ["C2", "O2"]:
                        value["source_atom_ids"] = ["C2", "C3"]
                        value["source_bond_order_code"] = "sing"
                    if isinstance(value, dict) and value.get("omitted_atom_ids") == ["O2"]:
                        value["omitted_atom_ids"] = ["C3"]
            _repin(sidecar, projection, binding, path)
            validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            with self.assertRaisesRegex(ValueError, "absent from every modeled instance"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_omitted_atom_must_itself_exist_in_component_dictionary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, bundle, root = _copy_case(Path(directory), "aldolase")
            annotation = _annotation(sidecar, "m0222.2qut.13p-protein-covalent-enamine-context")
            projection, binding, path = _projection(sidecar, annotation, root)
            for document in (annotation, projection):
                for value in _walk(document):
                    if isinstance(value, dict) and value.get("omitted_atom_ids") == ["O2"]:
                        value["omitted_atom_ids"] = ["O2", "ZZ"]
            _repin(sidecar, projection, binding, path)
            validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            with self.assertRaisesRegex(ValueError, "not a dictionary atom"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_correlated_plv_connection_count_repin_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, bundle, root = _copy_case(Path(directory), "plp")
            annotation = _annotation(sidecar, "m0186.1pwh.plv-bound-adduct")
            projection, binding, path = _projection(sidecar, annotation, root)
            for document in (annotation, projection):
                for value in _walk(document):
                    if (
                        isinstance(value, dict)
                        and value.get("queried_component_id") == "PLV"
                        and value.get("struct_conn_row_count") == 26
                    ):
                        value["struct_conn_row_count"] = 4
            _repin(sidecar, projection, binding, path)
            validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            with self.assertRaisesRegex(ValueError, "inventory differs"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_correlated_component_description_repin_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, bundle, root = _copy_case(Path(directory), "plp")
            annotation = _annotation(sidecar, "m0213.1l6g.pdd-bound-analogue")
            projection, binding, path = _projection(sidecar, annotation, root)
            old = "N-(5'-PHOSPHOPYRIDOXYL)-D-ALANINE"
            new = "Repinned but absent component description"
            for document in (annotation, projection):
                for value in _walk(document):
                    if isinstance(value, dict):
                        for key, item in list(value.items()):
                            if item == old:
                                value[key] = new
            _repin(sidecar, projection, binding, path)
            validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            with self.assertRaisesRegex(ValueError, "component description differs"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_pdd_atom_author_and_source_author_numbers_cannot_be_collapsed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, bundle, root = _copy_case(Path(directory), "plp")
            annotation = _annotation(sidecar, "m0213.1l6g.pdd-bound-analogue")
            projection, binding, path = _projection(sidecar, annotation, root)
            for document in (annotation, projection):
                for value in _walk(document):
                    if (
                        isinstance(value, dict)
                        and value.get("label_component_id") == "PDD"
                        and value.get("label_asym_id") == "D"
                        and value.get("atom_author_residue_number") == 1390
                    ):
                        value["atom_author_residue_number"] = 390
            _repin(sidecar, projection, binding, path)
            validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            with self.assertRaisesRegex(ValueError, "structure instances differ"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_correlated_protein_entity_context_repin_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, bundle, root = _copy_case(Path(directory), "plp")
            annotation = _annotation(sidecar, "m0186.1pwh.plv-bound-adduct")
            projection, binding, path = _projection(sidecar, annotation, root)
            annotation["claim"]["structure_context"]["protein_entity_ids"] = ["99"]
            projection["structure_context"]["protein_entity_ids"] = ["99"]
            _repin(sidecar, projection, binding, path)
            validate_primary_evidence(sidecar, bundle=bundle, repo_root=root)
            with self.assertRaisesRegex(ValueError, "protein entity"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_primary_source_hash_is_checked_before_mmcif_parse(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sidecar, _, root = _copy_case(Path(directory), "aldolase")
            annotation = _annotation(sidecar, "m0222.2qut.13p-protein-covalent-enamine-context")
            evidence = next(
                row for row in annotation["evidence"]
                if row["source_kind"] == "primary_structure_record"
            )
            binding = next(
                row for row in sidecar["source_bindings"]
                if row["binding_id"] == evidence["source_binding_id"]
            )
            (root / binding["path"]).write_text(
                "data_2QUT\nloop_\n_atom_site.id\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "hash differs"):
                CHECK.audit_primary_structure_evidence(sidecar, root)

    def test_parser_handles_wrapped_rows_quotes_and_semicolon_text(self) -> None:
        tables = CHECK._parse_mmcif_categories(
            """data_TEST
_entry.id TEST
_struct_site.details
;first line
_looks_like_a_tag
;
loop_
_chem_comp.id
_chem_comp.type
_chem_comp.name
X 'non-polymer'
"_quoted_name_beginning_with_underscore"
#
"""
        )
        self.assertEqual(tables["_entry"], [{"id": "TEST"}])
        self.assertEqual(
            tables["_struct_site"], [{"details": "first line\n_looks_like_a_tag"}]
        )
        self.assertEqual(
            tables["_chem_comp"],
            [{"id": "X", "type": "non-polymer", "name": "_quoted_name_beginning_with_underscore"}],
        )

    def test_parser_fails_closed_on_malformed_relevant_syntax(self) -> None:
        cases = [
            (
                "data_X\nloop_\n_atom_site.id\n_atom_site.label_atom_id\n1\n",
                "incomplete row",
            ),
            ("data_X\n_entry.id\n;unterminated\n", "no text-field terminator"),
            ("data_X\ndata_Y\n", "exactly one data block"),
        ]
        for text, message in cases:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    CHECK._parse_mmcif_categories(text)

    def test_connection_inventory_rejects_missing_relevant_columns(self) -> None:
        annotation = {
            "projection_excerpt": {
                "support_edges": [
                    {
                        "edge_kind": "deposited_connection_inventory",
                        "extracted_values": {
                            "queried_component_id": "PLV",
                            "attachment_context": "absent_from_deposited_struct_conn",
                            "struct_conn_row_count": 1,
                            "matching_component_row_count": 0,
                            "connected_component_ids": ["K"],
                        },
                    }
                ]
            }
        }
        tables = {"_struct_conn": [{"id": "metalc1", "ptnr1_label_comp_id": "K"}]}
        with self.assertRaisesRegex(ValueError, "lacks fields"):
            CHECK._audit_connection_inventory(annotation, tables)


if __name__ == "__main__":
    unittest.main()
