from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.structure import (
    build_geometry_features,
    ligand_context_from_atoms,
    pairwise_distances,
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
HETATM 6 FE FE HEM A 501 1.8 2.2 0.0 FE HEM A 501
HETATM 7 C C1 HEM A 501 2.2 2.4 0.2 C1 HEM A 501
HETATM 8 O O HOH A 700 0.5 0.5 0.5 O HOH A 700
#
"""


class StructureTests(unittest.TestCase):
    def test_parse_and_select_residue_atoms(self) -> None:
        atoms = parse_atom_site_loop(SAMPLE_CIF)
        self.assertEqual(len(atoms), 8)
        asp_atoms = select_residue_atoms(atoms, chain_name="A", resid=7, code="Asp")
        self.assertEqual(len(asp_atoms), 3)
        self.assertEqual(residue_centroid(asp_atoms), {"x": 0.667, "y": 0.333, "z": 0.0})

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
        self.assertGreaterEqual(context["proximal_ligands"][0]["instance_count"], 1)

    def test_build_geometry_features_with_mock_fetcher(self) -> None:
        graph = {
            "nodes": [
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
        self.assertEqual(features["entries"][0]["resolved_residue_count"], 2)
        self.assertEqual(features["entries"][0]["ligand_context"]["ligand_codes"], ["HEM"])


if __name__ == "__main__":
    unittest.main()
