"""Regression tests for operator-qualified biological-assembly projection."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from catalytic_earth.atlas_assembly_context import project_assembly


REPO = Path(__file__).resolve().parents[2]
SIX_HA3_CIF = REPO / "data/atlas/study_context/6ha3/6HA3.cif"
SIX_HA3_SPEC = REPO / "data/atlas/assembly_context/6ha3/spec.json"


def _atom_row(
    atom_id: str,
    atom_name: str,
    *,
    alt_id: str = ".",
    label_asym_id: str = "A",
    label_seq_id: str = "10",
    insertion_code: str = "?",
    auth_seq_id: str = "10",
    model_id: str = "1",
    occupancy: str = "1.00",
    xyz: tuple[str, str, str] = ("1", "2", "3"),
) -> str:
    return " ".join(
        [
            "ATOM",
            atom_id,
            "O",
            atom_name,
            alt_id,
            "GLU",
            label_asym_id,
            "1",
            label_seq_id,
            insertion_code,
            *xyz,
            occupancy,
            "10.0",
            "?",
            auth_seq_id,
            "GLU",
            "X",
            atom_name,
            model_id,
        ]
    )


def _synthetic_cif(
    atom_rows: list[str],
    *,
    asym_id_list: str = "A",
    oper_expression: str = "(1)(2)",
) -> str:
    return (
        """data_TEST
_entry.id TEST
_pdbx_struct_assembly.id 1
_pdbx_struct_assembly.details author_defined_assembly
_pdbx_struct_assembly_gen.assembly_id 1
_pdbx_struct_assembly_gen.oper_expression '"""
        + oper_expression
        + "'\n_pdbx_struct_assembly_gen.asym_id_list "
        + asym_id_list
        + """
_pdbx_struct_assembly_auth_evidence.id 1
_pdbx_struct_assembly_auth_evidence.assembly_id 1
_pdbx_struct_assembly_auth_evidence.experimental_support none
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
1 transform translate-x-10 x+10,y,z 1 0 0 10 0 1 0 0 0 0 1 0
2 transform rotate-z-90 -y,x,z 0 -1 0 0 1 0 0 0 0 0 1 0
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
"""
        + "\n".join(atom_rows)
        + "\n#\n"
    )


def _selection(
    *,
    selection_id: str = "site",
    operator_ids: list[str] | None = None,
    label_asym_id: str = "A",
    auth_seq_id: str = "10",
    model_id: str = "1",
    atom_names: list[str] | None = None,
) -> dict:
    return {
        "selection_id": selection_id,
        "operator_ids": operator_ids or ["1", "2"],
        "model_id": model_id,
        "label_asym_id": label_asym_id,
        "auth_seq_id": auth_seq_id,
        "label_comp_id": "GLU",
        "atom_names": atom_names or ["OE1"],
    }


def _spec(selections: list[dict], distance_pairs: list[dict] | None = None) -> dict:
    return {
        "pdb_id": "TEST",
        "assembly_id": "1",
        "selections": selections,
        "distance_pairs": distance_pairs or [],
    }


class AtlasAssemblyContextTests(unittest.TestCase):
    def test_6ha3_recovers_operator_qualified_partner_topology(self) -> None:
        outer = json.loads(SIX_HA3_SPEC.read_text(encoding="utf-8"))
        result = project_assembly(
            SIX_HA3_CIF.read_text(encoding="utf-8"),
            outer["assembly_spec"],
        )
        metadata = result["deposited_metadata"]
        self.assertEqual(
            metadata["assembly_record"]["oligomeric_details"], "dimeric"
        )
        self.assertEqual(
            metadata["assembly_generation_records"][0]["oper_expression"],
            "1,2",
        )
        self.assertEqual(
            metadata["assembly_author_evidence_records"][0][
                "experimental_support"
            ],
            "none",
        )
        self.assertEqual(
            [row["operator_id"] for row in result["operator_transforms"]],
            ["1", "2"],
        )

        selections = {row["selection_id"]: row for row in result["selections"]}
        partner_atoms = selections["partner-e366"]["atoms"]
        self.assertEqual(
            [row["transformed_xyz"] for row in partner_atoms],
            [[-5.808, 8.956, 4.816], [-7.491, 9.267, 6.233]],
        )
        self.assertTrue(
            all(row["operator_ids"] == ["2"] for row in partner_atoms)
        )
        self.assertEqual(
            selections["t6f-aminopyrimidine"]["atoms"][0]["label_atom_id"],
            "N1,",
        )

        pairs = {row["pair_id"]: row for row in result["distance_pairs"]}
        self.assertEqual(
            [
                row["distance_angstrom"]
                for row in pairs["partner-to-q160"]["measurements"]
            ],
            [2.804089, 3.906386],
        )
        self.assertEqual(
            [
                row["distance_angstrom"]
                for row in pairs["partner-to-cofactor"]["measurements"]
            ],
            [4.146952, 2.624954],
        )
        self.assertGreater(
            min(
                row["distance_angstrom"]
                for row in pairs["unexpanded-to-cofactor"]["measurements"]
            ),
            18.0,
        )
        self.assertEqual(
            result["scope"],
            "geometric candidates; no bond or joint-state inference",
        )
        bad_atom_name = deepcopy(outer["assembly_spec"])
        next(
            row
            for row in bad_atom_name["selections"]
            if row["selection_id"] == "t6f-aminopyrimidine"
        )["atom_names"] = ["N1"]
        with self.assertRaisesRegex(ValueError, "lacks selected atoms.*N1"):
            project_assembly(
                SIX_HA3_CIF.read_text(encoding="utf-8"), bad_atom_name
            )

    def test_product_operators_apply_right_to_left_and_retain_alternates(self) -> None:
        cif = _synthetic_cif(
            [
                _atom_row("1", "OE1", alt_id="A", occupancy="0.60"),
                _atom_row(
                    "2",
                    "OE1",
                    alt_id="B",
                    occupancy="0.40",
                    xyz=("2", "2", "3"),
                ),
                _atom_row("3", "OE1", model_id="2", xyz=("9", "9", "9")),
            ]
        )
        result = project_assembly(cif, _spec([_selection()]))
        selection = result["selections"][0]
        self.assertEqual(selection["operation_application_order"], ["2", "1"])
        self.assertEqual(
            [row["transformed_xyz"] for row in selection["atoms"]],
            [[8.0, 1.0, 3.0], [8.0, 2.0, 3.0]],
        )
        self.assertEqual(
            [
                (row["label_alt_id"], row["occupancy"], row["model_id"])
                for row in selection["atoms"]
            ],
            [("A", 0.6, "1"), ("B", 0.4, "1")],
        )

    def test_cross_residue_alternate_combinations_remain_unresolved(self) -> None:
        cif = _synthetic_cif(
            [
                _atom_row("1", "OE1", alt_id="A", occupancy="0.60"),
                _atom_row("2", "OE1", alt_id="B", occupancy="0.40"),
                _atom_row(
                    "3",
                    "OE2",
                    alt_id="A",
                    label_seq_id="11",
                    auth_seq_id="11",
                    occupancy="0.75",
                    xyz=("3", "2", "3"),
                ),
                _atom_row(
                    "4",
                    "OE2",
                    alt_id="B",
                    label_seq_id="11",
                    auth_seq_id="11",
                    occupancy="0.25",
                    xyz=("4", "2", "3"),
                ),
            ]
        )
        selections = [
            _selection(selection_id="left"),
            _selection(
                selection_id="right",
                auth_seq_id="11",
                atom_names=["OE2"],
            ),
        ]
        pairs = [
            {
                "pair_id": "alts",
                "left_selection_id": "left",
                "right_selection_id": "right",
            }
        ]
        result = project_assembly(cif, _spec(selections, pairs))
        measurements = result["distance_pairs"][0]["measurements"]
        self.assertEqual(len(measurements), 4)
        self.assertEqual(
            {
                (row["left_label_alt_id"], row["right_label_alt_id"])
                for row in measurements
            },
            {("A", "A"), ("A", "B"), ("B", "A"), ("B", "B")},
        )
        self.assertTrue(
            all(
                row["alternate_coexistence"]
                == "cross_residue_or_copy_alternate_coexistence_unresolved"
                for row in measurements
            )
        )

    def test_insertion_code_ambiguity_is_rejected(self) -> None:
        cif = _synthetic_cif(
            [
                _atom_row("1", "OE1", insertion_code="A"),
                _atom_row("2", "OE1", insertion_code="B"),
            ]
        )
        with self.assertRaisesRegex(ValueError, "ambiguous deposited residue"):
            project_assembly(cif, _spec([_selection()]))

    def test_selection_model_is_exact(self) -> None:
        cif = _synthetic_cif(
            [
                _atom_row("1", "OE1", model_id="1"),
                _atom_row("2", "OE1", model_id="2", xyz=("9", "9", "9")),
            ]
        )
        result = project_assembly(cif, _spec([_selection(model_id="2")]))
        atom = result["selections"][0]["atoms"][0]
        self.assertEqual(atom["model_id"], "2")
        self.assertEqual(atom["deposited_xyz"], [9.0, 9.0, 9.0])

    def test_unlisted_assembly_copy_is_rejected(self) -> None:
        cif = _synthetic_cif(
            [_atom_row("1", "OE1", label_asym_id="B")],
            asym_id_list="A",
        )
        spec = _spec([_selection(label_asym_id="B")])
        with self.assertRaisesRegex(ValueError, "not generated"):
            project_assembly(cif, spec)

    def test_operator_path_must_be_declared_by_generation_expression(self) -> None:
        cif = _synthetic_cif([_atom_row("1", "OE1")])
        spec = _spec([_selection(operator_ids=["2"])])
        with self.assertRaisesRegex(ValueError, "not generated"):
            project_assembly(cif, spec)

    def test_operator_range_is_bounded_before_expansion(self) -> None:
        cif = _synthetic_cif(
            [_atom_row("1", "OE1")],
            oper_expression="1-99999999999999999999",
        )
        with self.assertRaisesRegex(ValueError, "expands beyond"):
            project_assembly(cif, _spec([_selection()]))

    def test_deposited_atom_site_ids_are_globally_unique(self) -> None:
        cif = _synthetic_cif(
            [
                _atom_row("1", "OE1"),
                _atom_row(
                    "1",
                    "OE2",
                    label_seq_id="11",
                    auth_seq_id="11",
                ),
            ]
        )
        with self.assertRaisesRegex(ValueError, "atom-site IDs are ambiguous"):
            project_assembly(cif, _spec([_selection()]))

    def test_duplicate_atom_and_alternate_identity_is_rejected(self) -> None:
        cif = _synthetic_cif(
            [_atom_row("1", "OE1"), _atom_row("2", "OE1")]
        )
        with self.assertRaisesRegex(ValueError, "deposited atom identities"):
            project_assembly(cif, _spec([_selection()]))

    def test_extra_or_missing_spec_fields_fail_closed(self) -> None:
        cif = _synthetic_cif([_atom_row("1", "OE1")])
        spec = _spec([_selection()])
        altered = deepcopy(spec)
        altered["case_specific_switch"] = "6HA3"
        with self.assertRaisesRegex(ValueError, "fields differ"):
            project_assembly(cif, altered)


if __name__ == "__main__":
    unittest.main()
