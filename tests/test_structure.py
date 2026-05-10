from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.structure import (
    build_geometry_features,
    ligand_context_from_atoms,
    missing_position_detail,
    pairwise_distances,
    pocket_context_from_atoms,
    parse_atom_site_loop,
    residue_centroid,
    select_residue_atoms,
)


SAMPLE_CIF = """data_test
#
loop_
_atom_site.group_PDB
_atom_site.id
_atom_site.type_symbol
_atom_site.label_atom_id
_atom_site.label_comp_id
_atom_site.label_asym_id
_atom_site.label_seq_id
_atom_site.Cartn_x
_atom_site.Cartn_y
_atom_site.Cartn_z
_atom_site.auth_atom_id
_atom_site.auth_comp_id
_atom_site.auth_asym_id
_atom_site.auth_seq_id
ATOM 1 N N ASP A 7 0.0 0.0 0.0 N ASP A 7
ATOM 2 C CA ASP A 7 1.0 0.0 0.0 CA ASP A 7
ATOM 3 C C ASP A 7 1.0 1.0 0.0 C ASP A 7
ATOM 4 N N CYS A 70 0.0 4.0 0.0 N CYS A 70
ATOM 5 C CA CYS A 70 0.0 5.0 0.0 CA CYS A 70
ATOM 6 N N LYS A 8 2.0 0.0 0.0 N LYS A 8
ATOM 7 C CA LYS A 8 2.5 0.2 0.0 CA LYS A 8
ATOM 8 N N PHE A 9 2.0 1.5 0.0 N PHE A 9
ATOM 9 C CA PHE A 9 2.8 1.8 0.0 CA PHE A 9
ATOM 10 N N THR A 147 30.0 0.0 0.0 N THR A 164
ATOM 11 C CA THR A 147 30.5 0.0 0.0 CA THR A 164
ATOM 12 N N CYS A 164 34.0 0.0 0.0 N CYS A 181
ATOM 13 C CA CYS A 164 34.5 0.0 0.0 CA CYS A 181
HETATM 6 FE FE HEM A 501 1.8 2.2 0.0 FE HEM A 501
HETATM 7 C C1 HEM A 501 2.2 2.4 0.2 C1 HEM A 501
HETATM 8 O O HOH A 700 0.5 0.5 0.5 O HOH A 700
HETATM 9 N N1 FAD A 900 20.0 20.0 20.0 N1 FAD A 900
#
"""


class StructureTests(unittest.TestCase):
    def test_parse_and_select_residue_atoms(self) -> None:
        atoms = parse_atom_site_loop(SAMPLE_CIF)
        self.assertEqual(len(atoms), 17)
        asp_atoms = select_residue_atoms(atoms, chain_name="A", resid=7, code="Asp")
        self.assertEqual(len(asp_atoms), 3)
        self.assertEqual(residue_centroid(asp_atoms), {"x": 0.667, "y": 0.333, "z": 0.0})
        detail = missing_position_detail(
            atoms,
            {"residue_node_id": "x", "chain_name": "A", "resid": 7, "code": "GLU"},
        )
        self.assertEqual(detail["observed_codes_at_position"], ["ASP"])

    def test_select_residue_atoms_matches_label_or_auth_numbering(self) -> None:
        atoms = parse_atom_site_loop(SAMPLE_CIF)
        cys_atoms = select_residue_atoms(atoms, chain_name="A", resid=164, code="Cys")
        self.assertEqual(len(cys_atoms), 2)
        self.assertEqual({atom["auth_seq_id"] for atom in cys_atoms}, {"181"})
        detail = missing_position_detail(
            atoms,
            {"residue_node_id": "x", "chain_name": "A", "resid": 164, "code": "GLU"},
        )
        self.assertEqual(detail["observed_codes_at_position"], ["CYS", "THR"])

    def test_pairwise_distances(self) -> None:
        distances = pairwise_distances(
            [
                {"residue_node_id": "a", "ca": {"x": 0, "y": 0, "z": 0}},
                {"residue_node_id": "b", "ca": {"x": 3, "y": 4, "z": 0}},
            ]
        )
        self.assertEqual(distances[0]["distance"], 5.0)

    def test_ligand_context_filters_water_and_infers_heme(self) -> None:
        atoms = parse_atom_site_loop(SAMPLE_CIF)
        context = ligand_context_from_atoms(
            atoms,
            [
                {"ca": {"x": 1.0, "y": 0.0, "z": 0.0}},
                {"ca": {"x": 0.0, "y": 5.0, "z": 0.0}},
            ],
        )
        self.assertEqual(context["ligand_codes"], ["HEM"])
        self.assertIn("heme", context["cofactor_families"])
        self.assertEqual(context["structure_ligand_codes"], ["HEM", "FAD"])
        self.assertIn("flavin", context["structure_cofactor_families"])
        self.assertGreaterEqual(context["proximal_ligands"][0]["instance_count"], 1)

    def test_ligand_context_infers_cobalamin_codes(self) -> None:
        context = ligand_context_from_atoms(
            [
                {
                    "group_PDB": "HETATM",
                    "auth_comp_id": "B12",
                    "label_comp_id": "B12",
                    "auth_asym_id": "A",
                    "label_asym_id": "A",
                    "auth_seq_id": "500",
                    "label_seq_id": "500",
                    "Cartn_x": 1.0,
                    "Cartn_y": 0.0,
                    "Cartn_z": 0.0,
                }
            ],
            [{"ca": {"x": 0.0, "y": 0.0, "z": 0.0}}],
        )
        self.assertEqual(context["ligand_codes"], ["B12"])
        self.assertIn("cobalamin", context["cofactor_families"])

    def test_ligand_context_infers_plp_variants(self) -> None:
        for ligand_code in ("PLV", "PDD", "5PA"):
            with self.subTest(ligand_code=ligand_code):
                context = ligand_context_from_atoms(
                    [
                        {
                            "group_PDB": "HETATM",
                            "auth_comp_id": ligand_code,
                            "label_comp_id": ligand_code,
                            "auth_asym_id": "A",
                            "label_asym_id": "A",
                            "auth_seq_id": "600",
                            "label_seq_id": "600",
                            "Cartn_x": 1.0,
                            "Cartn_y": 0.0,
                            "Cartn_z": 0.0,
                        }
                    ],
                    [{"ca": {"x": 0.0, "y": 0.0, "z": 0.0}}],
                )
                self.assertEqual(context["ligand_codes"], [ligand_code])
                self.assertIn("plp", context["cofactor_families"])

    def test_ligand_context_does_not_treat_alkali_ions_as_metal_cofactors(self) -> None:
        active_site = [{"ca": {"x": 0.0, "y": 0.0, "z": 0.0}}]
        alkali_atoms = [
            {
                "group_PDB": "HETATM",
                "auth_comp_id": code,
                "label_comp_id": code,
                "auth_asym_id": "A",
                "label_asym_id": "A",
                "auth_seq_id": str(index),
                "label_seq_id": str(index),
                "Cartn_x": float(index),
                "Cartn_y": 0.0,
                "Cartn_z": 0.0,
            }
            for index, code in enumerate(["K", "NA"], start=1)
        ]
        alkali_context = ligand_context_from_atoms(alkali_atoms, active_site)
        self.assertEqual(alkali_context["ligand_codes"], ["K", "NA"])
        self.assertEqual(alkali_context["cofactor_families"], [])

        magnesium_context = ligand_context_from_atoms(
            [
                *alkali_atoms,
                {
                    "group_PDB": "HETATM",
                    "auth_comp_id": "MG",
                    "label_comp_id": "MG",
                    "auth_asym_id": "A",
                    "label_asym_id": "A",
                    "auth_seq_id": "3",
                    "label_seq_id": "3",
                    "Cartn_x": 3.0,
                    "Cartn_y": 0.0,
                    "Cartn_z": 0.0,
                },
            ],
            active_site,
        )
        self.assertEqual(magnesium_context["cofactor_families"], ["metal_ion"])

    def test_pocket_context_summarizes_nearby_residue_classes(self) -> None:
        atoms = parse_atom_site_loop(SAMPLE_CIF)
        context = pocket_context_from_atoms(
            atoms,
            [
                {"chain_name": "A", "resid": 7, "ca": {"x": 1.0, "y": 0.0, "z": 0.0}},
                {"chain_name": "A", "resid": 70, "ca": {"x": 0.0, "y": 5.0, "z": 0.0}},
            ],
        )
        self.assertEqual(context["nearby_residue_count"], 2)
        self.assertEqual(context["residue_code_counts"], {"LYS": 1, "PHE": 1})
        self.assertGreater(context["descriptors"]["aromatic_fraction"], 0.0)
        self.assertGreater(context["descriptors"]["positive_fraction"], 0.0)

    def test_build_geometry_features_with_mock_fetcher(self) -> None:
        graph = {
            "nodes": [
                {
                    "id": "m_csa:1",
                    "type": "m_csa_entry",
                    "name": "Example hydrolase",
                },
                {
                    "id": "m_csa:1:mechanism:1",
                    "type": "mechanism_text",
                    "text": "A concise mechanism sentence that helps label review.",
                },
                {
                    "id": "m_csa:1:residue:1",
                    "type": "catalytic_residue",
                    "roles": ["acid"],
                    "structure_positions": [
                        {"pdb_id": "1ABC", "chain_name": "A", "code": "ASP", "resid": 7}
                    ],
                },
                {
                    "id": "m_csa:1:residue:2",
                    "type": "catalytic_residue",
                    "roles": ["nucleophile"],
                    "structure_positions": [
                        {"pdb_id": "1ABC", "chain_name": "A", "code": "CYS", "resid": 70}
                    ],
                },
            ],
            "edges": [],
        }
        features = build_geometry_features(graph, max_entries=1, cif_fetcher=lambda _: SAMPLE_CIF)
        self.assertEqual(features["metadata"]["entries_with_pairwise_geometry"], 1)
        self.assertEqual(features["metadata"]["entries_with_inferred_cofactors"], 1)
        self.assertEqual(features["metadata"]["entries_with_structure_ligands"], 1)
        self.assertEqual(features["metadata"]["entries_with_structure_inferred_cofactors"], 1)
        self.assertEqual(features["metadata"]["entries_with_pocket_context"], 1)
        self.assertEqual(features["entries"][0]["entry_name"], "Example hydrolase")
        self.assertEqual(features["entries"][0]["mechanism_text_count"], 1)
        self.assertEqual(
            features["entries"][0]["mechanism_text_snippets"],
            ["A concise mechanism sentence that helps label review."],
        )
        self.assertEqual(features["entries"][0]["resolved_residue_count"], 2)
        self.assertEqual(features["entries"][0]["missing_position_details"], [])
        self.assertEqual(features["entries"][0]["ligand_context"]["ligand_codes"], ["HEM"])
        self.assertEqual(features["entries"][0]["pocket_context"]["nearby_residue_count"], 2)

    def test_build_geometry_features_uses_numeric_mcsa_order(self) -> None:
        graph = {"nodes": [], "edges": []}
        for entry_id in ["m_csa:1", "m_csa:10", "m_csa:2"]:
            graph["nodes"].extend(
                [
                    {
                        "id": f"{entry_id}:residue:1",
                        "type": "catalytic_residue",
                        "roles": ["acid"],
                        "structure_positions": [
                            {
                                "pdb_id": "1ABC",
                                "chain_name": "A",
                                "code": "ASP",
                                "resid": 7,
                            }
                        ],
                    },
                    {
                        "id": f"{entry_id}:residue:2",
                        "type": "catalytic_residue",
                        "roles": ["nucleophile"],
                        "structure_positions": [
                            {
                                "pdb_id": "1ABC",
                                "chain_name": "A",
                                "code": "CYS",
                                "resid": 70,
                            }
                        ],
                    },
                ]
            )

        features = build_geometry_features(graph, max_entries=3, cif_fetcher=lambda _: SAMPLE_CIF)

        self.assertEqual(
            [entry["entry_id"] for entry in features["entries"]],
            ["m_csa:1", "m_csa:2", "m_csa:10"],
        )


if __name__ == "__main__":
    unittest.main()
