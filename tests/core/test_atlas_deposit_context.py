"""Regression tests for generic, source-reviewed mmCIF deposit contexts."""

from __future__ import annotations

import copy
import gzip
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from catalytic_earth.atlas_assembly_context import project_assembly
from catalytic_earth.atlas_deposit_context import (
    _component_comparisons,
    _reaction_state_comparisons,
    REVIEW_DECISION,
    REVIEW_SCHEMA_VERSION,
    build_deposit_context,
    canonical_json_bytes,
    check_deposit_context,
)
from catalytic_earth.atlas_primary_source_check import parse_mmcif_categories
from catalytic_earth.canonical_hash import canonical_file_sha256


SYNTHETIC_CIF = """data_TEST
_entry.id TEST
_struct.entry_id TEST
_struct.title 'TEST STRUCTURE WITH BOUND INHIBITOR'
_struct_keywords.entry_id TEST
_struct_keywords.pdbx_keywords 'TRANSITION STATE ANALOG'
_exptl.entry_id TEST
_exptl.method 'X-RAY DIFFRACTION'
_refine.entry_id TEST
_refine.ls_d_res_high 3.0
_chem_comp.id TSA
_chem_comp.type non-polymer
_chem_comp.name 'DECLARED INHIBITOR'
_chem_comp.formula 'C2 H2 O2'
_pdbx_nonpoly_scheme.asym_id D
_pdbx_nonpoly_scheme.entity_id 3
_pdbx_nonpoly_scheme.mon_id TSA
_pdbx_nonpoly_scheme.ndb_seq_num 1
_pdbx_nonpoly_scheme.pdb_seq_num 400
_pdbx_nonpoly_scheme.auth_seq_num 400
_pdbx_nonpoly_scheme.pdb_mon_id TSA
_pdbx_nonpoly_scheme.auth_mon_id BAR
_pdbx_nonpoly_scheme.pdb_strand_id A
_pdbx_nonpoly_scheme.pdb_ins_code .
_pdbx_unobs_or_zero_occ_residues.PDB_model_num 1
_pdbx_unobs_or_zero_occ_residues.auth_asym_id A
_pdbx_unobs_or_zero_occ_residues.auth_comp_id GLU
_pdbx_unobs_or_zero_occ_residues.auth_seq_id 218
_struct_site_gen.site_id AC1
_struct_site_gen.label_comp_id LYS
_struct_site_gen.label_asym_id A
_struct_site_gen.label_seq_id 168
_struct_site_gen.auth_comp_id LYS
_struct_site_gen.auth_asym_id A
_struct_site_gen.auth_seq_id 168
_struct_site_gen.pdbx_auth_ins_code ?
_struct_site_gen.symmetry 1_555
_struct_site_gen.details ?
_pdbx_struct_assembly.id 1
_pdbx_struct_assembly.details author_defined_assembly
_pdbx_struct_assembly.oligomeric_details dimeric
_pdbx_struct_assembly.oligomeric_count 2
_pdbx_struct_assembly_gen.assembly_id 1
_pdbx_struct_assembly_gen.oper_expression 1
_pdbx_struct_assembly_gen.asym_id_list A,D
loop_
_pdbx_struct_oper_list.id
_pdbx_struct_oper_list.type
_pdbx_struct_oper_list.name
_pdbx_struct_oper_list.symmetry_operation
_pdbx_struct_oper_list.matrix[1][1]
_pdbx_struct_oper_list.matrix[1][2]
_pdbx_struct_oper_list.matrix[1][3]
_pdbx_struct_oper_list.vector[1]
_pdbx_struct_oper_list.matrix[2][1]
_pdbx_struct_oper_list.matrix[2][2]
_pdbx_struct_oper_list.matrix[2][3]
_pdbx_struct_oper_list.vector[2]
_pdbx_struct_oper_list.matrix[3][1]
_pdbx_struct_oper_list.matrix[3][2]
_pdbx_struct_oper_list.matrix[3][3]
_pdbx_struct_oper_list.vector[3]
1 identity 1_555 x,y,z 1 0 0 0 0 1 0 0 0 0 1 0
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_alt_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_entity_id
_atom_site.label_seq_id
_atom_site.pdbx_PDB_ins_code
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.occupancy
_atom_site.B_iso_or_equiv
_atom_site.pdbx_formal_charge
_atom_site.auth_seq_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_atom_id
_atom_site.pdbx_PDB_model_num
HETATM 1 O O7 . TSA D 3 . ? 0 0 0 1.00 10.0 ? 400 BAR A O7 1
ATOM 2 N NZ . LYS A 1 168 ? 3 0 0 1.00 11.0 ? 168 LYS A NZ 1
#
"""


def _base_spec(source_sha256: str) -> dict:
    assembly_spec = {
        "pdb_id": "TEST",
        "assembly_id": "1",
        "selections": [
            {
                "selection_id": "ligand-oxygen",
                "operator_ids": ["1"],
                "model_id": "1",
                "label_asym_id": "D",
                "auth_seq_id": "400",
                "label_comp_id": "TSA",
                "atom_names": ["O7"],
            },
            {
                "selection_id": "lysine-nitrogen",
                "operator_ids": ["1"],
                "model_id": "1",
                "label_asym_id": "A",
                "auth_seq_id": "168",
                "label_comp_id": "LYS",
                "atom_names": ["NZ"],
            },
        ],
        "distance_pairs": [
            {
                "pair_id": "ligand-to-lysine",
                "left_selection_id": "ligand-oxygen",
                "right_selection_id": "lysine-nitrogen",
            }
        ],
    }
    return {
        "schema_version": "catalytic-earth.deposit-context-spec.v1",
        "packet_id": "test.deposit-context",
        "source_binding": {
            "path": "data/source.cif",
            "sha256": source_sha256,
        },
        "row_selections": [
            {
                "selection_id": "entry",
                "category": "_entry",
                "match": {"id": "TEST"},
                "expected_row_count": 1,
            },
            {
                "selection_id": "ligand-component",
                "category": "_chem_comp",
                "match": {"id": "TSA"},
                "expected_row_count": 1,
            },
            {
                "selection_id": "experiment",
                "category": "_exptl",
                "match": {"entry_id": "TEST"},
                "expected_row_count": 1,
            },
            {
                "selection_id": "refinement",
                "category": "_refine",
                "match": {"entry_id": "TEST"},
                "expected_row_count": 1,
            },
            {
                "selection_id": "unmodeled-residue",
                "category": "_pdbx_unobs_or_zero_occ_residues",
                "match": {"auth_seq_id": "218"},
                "expected_row_count": 1,
            },
            {
                "selection_id": "site-membership",
                "category": "_struct_site_gen",
                "match": {"site_id": "AC1"},
                "expected_row_count": 1,
            },
            {
                "selection_id": "keywords",
                "category": "_struct_keywords",
                "match": {},
                "expected_row_count": 1,
            },
        ],
        "assembly_spec": assembly_spec,
        "interpretation": {
            "assertions": [
                {
                    "assertion_id": "deposited-ligand",
                    "status": "deposited_source_assertion",
                    "statement": "The source deposits a separately identified inhibitor component.",
                    "supporting_selection_ids": ["entry", "ligand-component"],
                },
                {
                    "assertion_id": "distance-description",
                    "status": "computed_coordinate_description",
                    "statement": "This is a Euclidean distance in the declared assembly.",
                    "supporting_selection_ids": ["ligand-to-lysine"],
                },
                {
                    "assertion_id": "bounded-interpretation",
                    "status": "project_interpretation",
                    "statement": "The selected deposit does not identify a reacting state.",
                    "supporting_selection_ids": ["keywords", "ligand-component"],
                },
            ],
            "not_established": [
                "chemical equivalence to a reaction participant",
                "mechanism or catalytic-role applicability",
            ],
        },
    }


class AtlasDepositContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "data").mkdir()
        self.source = self.root / "data/source.cif"
        self.source.write_text(SYNTHETIC_CIF, encoding="utf-8")
        self.spec = _base_spec(canonical_file_sha256(self.source))

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def build(self, spec: dict | None = None) -> dict:
        return build_deposit_context(
            self.spec if spec is None else spec,
            source_path=self.source,
        )

    def test_raw_rows_and_existing_assembly_geometry_are_preserved(self) -> None:
        result = self.build()
        rows = {row["selection_id"]: row for row in result["row_selections"]}
        self.assertEqual(rows["ligand-component"]["rows"][0]["formula"], "C2 H2 O2")
        self.assertEqual(rows["refinement"]["rows"][0]["ls_d_res_high"], "3.0")
        self.assertEqual(rows["keywords"]["rows"][0]["pdbx_keywords"], "TRANSITION STATE ANALOG")
        self.assertEqual(result["selected_row_count"], 7)
        self.assertEqual(
            result["assembly_projection"],
            project_assembly(SYNTHETIC_CIF, self.spec["assembly_spec"]),
        )
        measurement = result["assembly_projection"]["distance_pairs"][0][
            "measurements"
        ][0]
        self.assertEqual(measurement["distance_angstrom"], 3.0)
        self.assertEqual(
            result["assembly_projection"]["scope"],
            "geometric candidates; no bond or joint-state inference",
        )
        self.assertIn(
            "reaction, mechanism, source-step, or catalytic-role applicability",
            result["claim_boundary"]["does_not_establish"],
        )

    def test_unsupported_category_and_absent_selector_field_fail_closed(self) -> None:
        unsupported = copy.deepcopy(self.spec)
        unsupported["row_selections"][0]["category"] = "_unsupported"
        with self.assertRaisesRegex(ValueError, "category is unsupported"):
            self.build(unsupported)

        absent = copy.deepcopy(self.spec)
        absent["row_selections"][0]["match"] = {"missing_field": "TEST"}
        with self.assertRaisesRegex(ValueError, "match field.*is absent"):
            self.build(absent)

    def test_row_counts_are_positive_and_exact(self) -> None:
        zero = copy.deepcopy(self.spec)
        zero["row_selections"][0]["expected_row_count"] = 0
        with self.assertRaisesRegex(ValueError, "positive integer"):
            self.build(zero)

        mismatch = copy.deepcopy(self.spec)
        mismatch["row_selections"][0]["expected_row_count"] = 2
        with self.assertRaisesRegex(ValueError, "selected 1 rows; expected 2"):
            self.build(mismatch)

    def test_duplicate_and_dangling_selection_ids_are_rejected(self) -> None:
        duplicate = copy.deepcopy(self.spec)
        duplicate["row_selections"][1]["selection_id"] = "entry"
        with self.assertRaisesRegex(ValueError, "row selection IDs repeat"):
            self.build(duplicate)

        cross_kind = copy.deepcopy(self.spec)
        cross_kind["assembly_spec"]["selections"][0]["selection_id"] = "entry"
        cross_kind["assembly_spec"]["distance_pairs"][0][
            "left_selection_id"
        ] = "entry"
        with self.assertRaisesRegex(ValueError, "repeat across row and assembly"):
            self.build(cross_kind)

        dangling = copy.deepcopy(self.spec)
        dangling["interpretation"]["assertions"][0][
            "supporting_selection_ids"
        ].append("undeclared")
        with self.assertRaisesRegex(ValueError, "undeclared selection IDs"):
            self.build(dangling)

    def test_assembly_is_optional_without_weakening_row_provenance(self) -> None:
        spec = copy.deepcopy(self.spec)
        del spec["assembly_spec"]
        spec["interpretation"]["assertions"] = [
            spec["interpretation"]["assertions"][0]
        ]
        result = self.build(spec)
        self.assertIsNone(result["assembly_projection"])
        self.assertEqual(
            result["claim_boundary"]["coordinate_geometry"], "not projected"
        )

    def test_source_review_requires_current_spec_projection_and_source_pins(self) -> None:
        packet = self.root / "data/packet"
        packet.mkdir()
        spec_path = packet / "spec.json"
        projection_path = packet / "projection.json"
        review_path = packet / "review.json"
        spec_path.write_bytes(canonical_json_bytes(self.spec))
        projection_path.write_bytes(canonical_json_bytes(self.build()))
        review = {
            "schema_version": REVIEW_SCHEMA_VERSION,
            "decision": REVIEW_DECISION,
            "reviewed_sha256": {
                "spec.json": canonical_file_sha256(spec_path),
                "projection.json": canonical_file_sha256(projection_path),
                "source": canonical_file_sha256(self.source),
            },
            "reviewers": [{"lane": "source"}],
        }
        review_path.write_bytes(canonical_json_bytes(review))
        checked = check_deposit_context(Path("data/packet"), self.root)
        self.assertEqual(checked["packet_id"], self.spec["packet_id"])

        review["reviewed_sha256"]["spec.json"] = "0" * 64
        review_path.write_bytes(canonical_json_bytes(review))
        with self.assertRaisesRegex(ValueError, "source-review pins are stale"):
            check_deposit_context(Path("data/packet"), self.root)

    def test_bound_source_hash_cannot_be_repointed(self) -> None:
        changed = copy.deepcopy(self.spec)
        changed["source_binding"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "source binding hash differs"):
            self.build(changed)


class ComponentDictionaryComparisonTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[2]
        self.spec = json.loads((root / "data/atlas/deposit_context/mandelate_1mdl/spec.json").read_text())
        self.source = root / self.spec["source_binding"]["path"]
        self.tables = parse_mmcif_categories(gzip.decompress(self.source.read_bytes()).decode())
        self.declarations = copy.deepcopy(self.spec["component_comparisons"])

    def compare(self):
        return _component_comparisons(self.declarations, self.tables)[0]

    def test_full_dictionary_stereo_match_does_not_transfer_site_context(self):
        result = build_deposit_context(self.spec, source_path=self.source,
            repo_root=Path(__file__).resolve().parents[2])["component_comparisons"][0]
        self.assertEqual(len(result["atom_map"]), 19)
        self.assertEqual(result["stereo_inversions"],
                         [{"left_atom_id": "C7", "right_atom_id": "C7", "left": "R", "right": "S"}])
        self.assertEqual(result["unchanged_stereocenters"], [])
        self.assertEqual([len(result[s]["dictionary_bonds"]) for s in ("left", "right")], [19, 19])
        self.assertEqual([len(result[s]["coordinate_atoms"]) for s in ("left", "right")], [11, 11])
        self.assertEqual([len(result[s]["dictionary_only_atom_ids"]) for s in ("left", "right")], [8, 8])
        self.assertEqual([len(result[s]["site_members"]) for s in ("left", "right")], [6, 13])
        self.assertEqual([len(result[s]["external_connections"]) for s in ("left", "right")], [0, 2])
        self.assertEqual(result["same_deposited_environment_comparison"]["status"], "refused")
        self.assertEqual(result["same_deposited_environment_comparison"]["physical_site_equivalence"], "not_established")

    def test_dictionary_hydrogens_cannot_be_dropped_to_force_a_match(self):
        del self.declarations[0]["atom_map"]["H7"]
        with self.assertRaisesRegex(ValueError, "complete dictionary bijection"):
            self.compare()

    def test_wrong_element_or_supplied_charge_cannot_be_hidden(self):
        atom = next(r for r in self.tables["_chem_comp_atom"] if r["comp_id"] == "RMN" and r["atom_id"] == "C7")
        for field, value in [("type_symbol", "N"), ("charge", "1")]:
            changed = copy.deepcopy(atom)
            atom[field] = value
            with self.assertRaisesRegex(ValueError, "atom properties differ|coordinate element"):
                self.compare()
            atom.clear()
            atom.update(changed)

    def test_bond_order_difference_is_not_stereochemical_equivalence(self):
        bond = next(r for r in self.tables["_chem_comp_bond"] if r["comp_id"] == "RMN" and r["value_order"] == "doub")
        bond["value_order"] = "sing"
        with self.assertRaisesRegex(ValueError, "bond graphs differ"):
            self.compare()

    def test_unknown_stereo_and_same_stereo_do_not_pass(self):
        atom = next(r for r in self.tables["_chem_comp_atom"] if r["comp_id"] == "RMN" and r["atom_id"] == "C7")
        atom["pdbx_stereo_config"] = "?"
        with self.assertRaisesRegex(ValueError, "stereochemistry is unspecified"):
            self.compare()
        atom["pdbx_stereo_config"] = "S"
        with self.assertRaisesRegex(ValueError, "no explicit stereo inversion"):
            self.compare()

    def test_cross_listed_site_member_does_not_make_the_anchor_interchangeable(self):
        self.assertTrue(any(r["site_id"] == "AC3" and r["label_comp_id"] == "RMN"
                            for r in self.tables["_struct_site_gen"]))
        self.declarations[0]["left"]["site_id"] = "AC3"
        with self.assertRaisesRegex(ValueError, "site belongs to another component"):
            self.compare()

    def test_coordinate_coverage_and_conformers_fail_explicitly(self):
        row = next(r for r in self.tables["_atom_site"] if r["label_comp_id"] == "RMN")
        row["label_alt_id"] = "A"
        with self.assertRaisesRegex(ValueError, "alternative conformer comparison"):
            self.compare()
        row["label_alt_id"] = "."
        self.tables["_atom_site"].remove(row)
        with self.assertRaisesRegex(ValueError, "lacks dictionary heavy atoms"):
            self.compare()

    def test_no_comparison_and_missing_model_are_not_accepted(self):
        with self.assertRaisesRegex(ValueError, "nonempty"):
            _component_comparisons([], self.tables)
        self.declarations[0]["right"]["model_id"] = "?"
        with self.assertRaisesRegex(ValueError, "nonmissing raw strings"):
            self.compare()

    def test_self_mapping_is_not_a_distinct_component_pair(self):
        self.declarations[0]["right"] = copy.deepcopy(self.declarations[0]["left"])
        with self.assertRaisesRegex(ValueError, "distinct component dictionaries"):
            self.compare()

    def test_wrong_coordinate_author_component_is_rejected(self):
        row = next(r for r in self.tables["_atom_site"] if r["label_comp_id"] == "RMN")
        row["auth_comp_id"] = "SMN"
        with self.assertRaisesRegex(ValueError, "instance numbering differs"):
            self.compare()

    def test_unchanged_centers_remain_visible_beside_an_inversion(self):
        for row in self.tables["_chem_comp_atom"]:
            if row["comp_id"] in {"RMN", "SMN"} and row["atom_id"] == "C1":
                row["pdbx_stereo_config"] = "R"
        result = self.compare()
        self.assertEqual(result["unchanged_stereocenters"], ["C1"])
        self.assertEqual(len(result["stereo_inversions"]), 1)
        self.assertNotIn("enantiomer", result["relation_scope"])

    def test_insertion_codes_cannot_anchor_another_instance(self):
        coordinate = next(r for r in self.tables["_atom_site"] if r["label_comp_id"] == "RMN")
        coordinate["pdbx_pdb_ins_code"] = "A"
        with self.assertRaisesRegex(ValueError, "instance numbering differs"):
            self.compare()
        coordinate["pdbx_pdb_ins_code"] = "?"
        site = next(r for r in self.tables["_struct_site"] if r["id"] == "AC2")
        site["pdbx_auth_ins_code"] = "A"
        with self.assertRaisesRegex(ValueError, "site belongs to another component instance"):
            self.compare()


class ReactionStateComparisonTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]
        self.spec = json.loads((self.root / "data/atlas/deposit_context/mandelate_1mdl/spec.json").read_text())
        self.source = self.root / self.spec["source_binding"]["path"]
        self.tables = parse_mmcif_categories(gzip.decompress(self.source.read_bytes()).decode())
        self.declarations = copy.deepcopy(self.spec["reaction_state_comparisons"])

    def compare(self):
        return _reaction_state_comparisons(self.declarations, self.tables, self.root)

    def test_reaction_locators_preserve_stereo_order_and_unknown_state(self):
        rmn, smn = self.compare()
        for result in (rmn, smn):
            self.assertEqual(result["identity_request"]["status"], "refused")
            self.assertEqual(result["identity_request"]["chemical_state_identity"], "not_established")
            self.assertTrue(result["canonical_symmetry_alternatives_preserved"])
            self.assertFalse(result["identity_request"]["productive_geometry_transfer"])
            self.assertEqual(len(result["source"]["canonical_input_correspondence"]["map_alternatives"]), 2)
            self.assertEqual([len(a["bond_order_differences"]) for a in result["map_alternatives"]], [0, 6])
            for alternative in result["map_alternatives"]:
                self.assertEqual(len(alternative["atom_map"]), 12)
                self.assertFalse(alternative["complete_dictionary_atom_bijection"])
                self.assertEqual(alternative["atom_map"]["a66"], "H7")
                self.assertEqual(len(alternative["unmapped_dictionary_atom_ids"]), 7)
                self.assertIn("HO2", alternative["unmapped_dictionary_atom_ids"])
                carboxylate = next(a for a in alternative["atom_property_comparisons"]
                                   if a["source_atom_id"] == "a11")
                self.assertEqual(carboxylate["source_formal_charge"], -1)
                self.assertIsNone(carboxylate["dictionary_charge_token"])
                self.assertIsNone(carboxylate["formal_charge_equal"])
        for result, expected in ((rmn, True), (smn, False)):
            alpha = next(a for a in result["map_alternatives"][0]["atom_property_comparisons"]
                         if a["source_atom_id"] == "a9")
            self.assertIs(alpha["assigned_stereochemistry_token_equal"], expected)
        self.assertEqual(rmn["component"]["selector"]["site_id"], "AC2")
        self.assertEqual(smn["component"]["selector"]["site_id"], "AC3")

    def test_explicit_hydrogen_cannot_be_cropped_or_omitted(self):
        self.declarations[0]["source"]["atom_ids"].remove("a66")
        with self.assertRaisesRegex(ValueError, "complete covalent component"):
            self.compare()
        self.declarations = copy.deepcopy(self.spec["reaction_state_comparisons"])
        del self.declarations[0]["map_alternatives"][0]["atom_map"]["a66"]
        with self.assertRaisesRegex(ValueError, "every selected source node"):
            self.compare()

    def test_wrong_oxygen_topology_and_duplicate_maps_fail(self):
        mapping = self.declarations[0]["map_alternatives"][0]["atom_map"]
        mapping["a12"], mapping["a11"] = mapping["a11"], mapping["a12"]
        with self.assertRaisesRegex(ValueError, "topology differs"):
            self.compare()
        self.declarations = copy.deepcopy(self.spec["reaction_state_comparisons"])
        mapping = self.declarations[0]["map_alternatives"][0]["atom_map"]
        mapping["a10"], mapping["a11"] = mapping["a11"], mapping["a10"]
        with self.assertRaisesRegex(ValueError, "non-aromatic bond orders differ"):
            self.compare()
        self.declarations = copy.deepcopy(self.spec["reaction_state_comparisons"])
        self.declarations[0]["map_alternatives"][1]["atom_map"] = copy.deepcopy(
            self.declarations[0]["map_alternatives"][0]["atom_map"])
        with self.assertRaisesRegex(ValueError, "maps repeat"):
            self.compare()

    def test_source_identity_and_before_after_cannot_be_repointed(self):
        for key, value, message in (("transformation_id", "wrong", "missing or ambiguous"),
                                    ("state", "after", "complete covalent component")):
            self.declarations = copy.deepcopy(self.spec["reaction_state_comparisons"])
            self.declarations[0]["source"][key] = value
            with self.assertRaisesRegex(ValueError, message):
                self.compare()
        self.declarations = copy.deepcopy(self.spec["reaction_state_comparisons"])
        self.declarations[0]["source"]["binding"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "source binding hash differs"):
            self.compare()

    def test_reviewed_symmetry_alternative_cannot_be_dropped(self):
        for declaration in self.declarations:
            declaration["map_alternatives"].pop()
        with self.assertRaisesRegex(ValueError, "every reviewed canonical symmetry alternative"):
            self.compare()

    def test_supplied_charge_is_compared_and_missing_charge_is_not_zero(self):
        atom = next(a for a in self.tables["_chem_comp_atom"]
                    if a["comp_id"] == "RMN" and a["atom_id"] == "O12")
        for token, expected in (("?", None), ("0", False), ("-1", True)):
            atom["charge"] = token
            result = self.compare()[0]
            comparison = next(a for a in result["map_alternatives"][0]["atom_property_comparisons"]
                              if a["source_atom_id"] == "a11")
            self.assertIs(comparison["formal_charge_equal"], expected)
            self.assertEqual(result["identity_request"]["status"], "refused")


if __name__ == "__main__":
    unittest.main()
