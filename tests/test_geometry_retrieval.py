from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.geometry_retrieval import (
    compactness_score,
    cofactor_context_score,
    distance_summary,
    run_geometry_retrieval,
    score_entry_against_fingerprint,
    substrate_pocket_score,
)


class GeometryRetrievalTests(unittest.TestCase):
    def test_compactness_score(self) -> None:
        self.assertEqual(compactness_score([]), 0.0)
        self.assertEqual(compactness_score([{"distance": 5.0}]), 1.0)
        self.assertEqual(compactness_score([{"distance": 30.0}]), 0.0)

    def test_distance_summary(self) -> None:
        summary = distance_summary([{"distance": 4}, {"distance": 10}, {"distance": 20}])
        self.assertEqual(summary["median"], 10)
        self.assertEqual(summary["count"], 3)

    def test_score_ser_his_acid_fingerprint(self) -> None:
        entry = {
            "residues": [
                {"code": "SER", "roles": ["nucleophile"]},
                {"code": "HIS", "roles": ["general base"]},
                {"code": "ASP", "roles": ["acid"]},
            ],
            "pairwise_distances_angstrom": [{"distance": 6}, {"distance": 8}, {"distance": 10}],
        }
        fingerprint = {
            "id": "ser_his_acid_hydrolase",
            "name": "Ser-His-Asp/Glu hydrolase triad",
            "active_site_signature": [
                {"role": "nucleophile", "residue": "Ser"},
                {"role": "general_base", "residue": "His"},
                {"role": "acid_or_orienter", "residue": "Asp/Glu"},
            ],
        }
        score = score_entry_against_fingerprint(entry, fingerprint)
        self.assertEqual(score["residue_match_fraction"], 1.0)
        self.assertGreater(score["score"], 0.7)

    def test_metal_context_outscores_heme_without_heme_evidence(self) -> None:
        residue_codes = ["ASP", "HIS", "HIS"]
        residue_roles = {"metal ligand"}
        metal = {"id": "metal_dependent_hydrolase", "cofactors": ["Zn2+"]}
        heme = {"id": "heme_peroxidase_oxidase", "cofactors": ["heme"]}
        self.assertGreater(
            cofactor_context_score(metal, residue_codes, residue_roles),
            cofactor_context_score(heme, residue_codes, residue_roles),
        )

    def test_heme_ligand_context_outscores_metal_when_heme_is_observed(self) -> None:
        residue_codes = ["ASP", "HIS", "HIS"]
        residue_roles = set()
        ligand_context = {"cofactor_families": ["heme"]}
        metal = {"id": "metal_dependent_hydrolase", "cofactors": ["Zn2+"]}
        heme = {"id": "heme_peroxidase_oxidase", "cofactors": ["heme"]}
        self.assertGreater(
            cofactor_context_score(heme, residue_codes, residue_roles, ligand_context),
            cofactor_context_score(metal, residue_codes, residue_roles, ligand_context),
        )

    def test_substrate_pocket_score_prefers_polar_for_metal_hydrolase(self) -> None:
        polar_pocket = {
            "nearby_residue_count": 4,
            "descriptors": {
                "hydrophobic_fraction": 0.1,
                "polar_fraction": 0.5,
                "positive_fraction": 0.1,
                "negative_fraction": 0.3,
                "aromatic_fraction": 0.0,
                "sulfur_fraction": 0.0,
                "charge_balance": -0.2,
            },
        }
        hydrophobic_pocket = {
            "nearby_residue_count": 4,
            "descriptors": {
                "hydrophobic_fraction": 0.8,
                "polar_fraction": 0.1,
                "positive_fraction": 0.0,
                "negative_fraction": 0.0,
                "aromatic_fraction": 0.1,
                "sulfur_fraction": 0.0,
                "charge_balance": 0.0,
            },
        }
        metal = {"id": "metal_dependent_hydrolase"}
        self.assertGreater(
            substrate_pocket_score(metal, polar_pocket),
            substrate_pocket_score(metal, hydrophobic_pocket),
        )

    def test_run_geometry_retrieval(self) -> None:
        artifact = run_geometry_retrieval(
            {
                "entries": [
                    {
                        "entry_id": "m_csa:1",
                        "pdb_id": "1ABC",
                        "status": "ok",
                        "resolved_residue_count": 3,
                        "residues": [
                            {"code": "SER", "roles": ["nucleophile"]},
                            {"code": "HIS", "roles": ["base"]},
                            {"code": "ASP", "roles": ["acid"]},
                        ],
                        "ligand_context": {"cofactor_families": ["metal_ion"]},
                        "pocket_context": {
                            "nearby_residue_count": 3,
                            "descriptors": {
                                "hydrophobic_fraction": 0.3333,
                                "polar_fraction": 0.6667,
                                "positive_fraction": 0.3333,
                                "negative_fraction": 0.3333,
                                "aromatic_fraction": 0.0,
                                "sulfur_fraction": 0.0,
                                "charge_balance": 0.0,
                            },
                        },
                        "pairwise_distances_angstrom": [{"distance": 6}],
                    }
                ]
            },
            top_k=3,
        )
        self.assertEqual(artifact["metadata"]["entry_count"], 1)
        self.assertEqual(len(artifact["results"][0]["top_fingerprints"]), 3)


if __name__ == "__main__":
    unittest.main()
