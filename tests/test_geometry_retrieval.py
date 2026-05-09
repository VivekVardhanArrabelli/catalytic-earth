from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.geometry_retrieval import (
    compactness_score,
    cofactor_context_score,
    cofactor_evidence_level,
    counterevidence_penalty,
    distance_summary,
    mechanistic_coherence_score,
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
        self.assertEqual(score["mechanistic_coherence_score"], 1.0)
        self.assertGreater(score["score"], 0.7)

    def test_ser_his_score_penalizes_missing_serine_nucleophile(self) -> None:
        entry = {
            "residues": [
                {"code": "SER", "roles": ["hydrogen bond donor"]},
                {"code": "HIS", "roles": ["proton acceptor"]},
                {"code": "ASP", "roles": ["electrostatic stabiliser"]},
            ],
            "pairwise_distances_angstrom": [{"distance": 6}],
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
        self.assertEqual(mechanistic_coherence_score(fingerprint, entry["residues"]), 0.0)
        score = score_entry_against_fingerprint(entry, fingerprint)
        self.assertLess(score["score"], 0.7)

    def test_ser_his_coherence_requires_histidine_base(self) -> None:
        residues = [
            {"code": "SER", "roles": ["nucleophile"]},
            {"code": "LYS", "roles": ["proton acceptor", "proton donor"]},
            {"code": "GLU", "roles": ["proton acceptor", "proton donor"]},
        ]
        fingerprint = {"id": "ser_his_acid_hydrolase"}
        self.assertEqual(mechanistic_coherence_score(fingerprint, residues), 0.0)

    def test_metal_context_outscores_heme_without_heme_evidence(self) -> None:
        residue_codes = ["ASP", "HIS", "HIS"]
        residue_roles = {"metal ligand"}
        metal = {"id": "metal_dependent_hydrolase", "cofactors": ["Zn2+"]}
        heme = {"id": "heme_peroxidase_oxidase", "cofactors": ["heme"]}
        self.assertGreater(
            cofactor_context_score(metal, residue_codes, residue_roles),
            cofactor_context_score(heme, residue_codes, residue_roles),
        )
        self.assertEqual(cofactor_evidence_level(metal, residue_roles), "role_inferred")
        self.assertEqual(
            cofactor_evidence_level(metal, set(), {"cofactor_families": ["metal_ion"]}),
            "ligand_supported",
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
        self.assertEqual(
            cofactor_evidence_level(heme, residue_roles, ligand_context),
            "ligand_supported",
        )

    def test_heme_context_ignores_family_dependent_oxidant_placeholder(self) -> None:
        heme = {
            "id": "heme_peroxidase_oxidase",
            "cofactors": ["heme", "H2O2 or O2 depending on family"],
        }
        self.assertEqual(
            cofactor_context_score(heme, ["HIS"], set(), {"cofactor_families": ["heme"]}),
            1.0,
        )

    def test_plp_context_prefers_ligand_over_lysine_only(self) -> None:
        fingerprint = {"id": "plp_dependent_enzyme", "cofactors": ["pyridoxal phosphate"]}
        lysine_only = cofactor_context_score(fingerprint, ["LYS"], set(), {})
        ligand_supported = cofactor_context_score(
            fingerprint,
            ["LYS"],
            set(),
            {"cofactor_families": ["plp"]},
        )
        self.assertLess(lysine_only, 0.2)
        self.assertEqual(ligand_supported, 1.0)

    def test_cobalamin_ligand_context_is_supported(self) -> None:
        fingerprint = {"id": "adenosylcobalamin_radical_mutase", "cofactors": ["adenosylcobalamin"]}
        ligand_context = {"cofactor_families": ["cobalamin"]}
        self.assertEqual(
            cofactor_context_score(fingerprint, ["HIS", "TYR"], {"radical stabiliser"}, ligand_context),
            1.0,
        )
        self.assertEqual(
            cofactor_evidence_level(fingerprint, set(), ligand_context),
            "ligand_supported",
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

    def test_role_inferred_metal_hydrolase_penalizes_low_pocket_support(self) -> None:
        fingerprint = {"id": "metal_dependent_hydrolase"}
        residues = [
            {"code": "HIS", "roles": ["metal ligand"]},
            {"code": "GLU", "roles": ["metal ligand", "proton acceptor"]},
            {"code": "GLU", "roles": ["metal ligand", "proton donor"]},
        ]
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="role_inferred",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.12,
            ),
            1.0,
        )
        self.assertEqual(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="role_inferred",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.18,
            ),
            1.0,
        )

    def test_metal_hydrolase_penalizes_transfer_or_redox_context(self) -> None:
        fingerprint = {"id": "metal_dependent_hydrolase"}
        residues = [
            {"code": "ASP", "roles": ["metal ligand"]},
            {"code": "HIS", "roles": ["metal ligand", "single electron donor"]},
        ]
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="ligand_supported",
                ligand_context={"ligand_codes": ["ATP"], "cofactor_families": ["metal_ion"]},
                substrate_pocket_score_value=0.2,
            ),
            1.0,
        )
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="ligand_supported",
                ligand_context={"ligand_codes": ["CU"], "cofactor_families": ["metal_ion"]},
                substrate_pocket_score_value=0.2,
            ),
            1.0,
        )

    def test_metal_hydrolase_penalizes_heme_only_context(self) -> None:
        self.assertLess(
            counterevidence_penalty(
                fingerprint={"id": "metal_dependent_hydrolase"},
                residues=[{"code": "HIS", "roles": ["metal ligand"]}],
                cofactor_evidence="role_inferred",
                ligand_context={"ligand_codes": ["HEM"], "cofactor_families": ["heme"]},
                substrate_pocket_score_value=0.2,
            ),
            1.0,
        )

    def test_metal_hydrolase_penalizes_cobalamin_only_context(self) -> None:
        self.assertLess(
            counterevidence_penalty(
                fingerprint={"id": "metal_dependent_hydrolase"},
                residues=[{"code": "HIS", "roles": ["metal ligand"]}],
                cofactor_evidence="role_inferred",
                ligand_context={"ligand_codes": ["B12"], "cofactor_families": ["cobalamin"]},
                substrate_pocket_score_value=0.2,
            ),
            1.0,
        )

    def test_metal_supported_site_penalizes_ser_his_assignment(self) -> None:
        entry = {
            "residues": [
                {"code": "SER", "roles": ["nucleophile"]},
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "ASP", "roles": ["metal ligand"]},
                {"code": "GLU", "roles": ["metal ligand"]},
                {"code": "HIS", "roles": ["metal ligand"]},
            ],
            "ligand_context": {"cofactor_families": ["metal_ion"]},
            "pocket_context": {
                "nearby_residue_count": 4,
                "descriptors": {
                    "hydrophobic_fraction": 0.25,
                    "polar_fraction": 0.4,
                    "positive_fraction": 0.1,
                    "negative_fraction": 0.2,
                    "aromatic_fraction": 0.0,
                    "sulfur_fraction": 0.0,
                    "charge_balance": -0.1,
                },
            },
            "pairwise_distances_angstrom": [{"distance": 6}],
        }
        metal = {
            "id": "metal_dependent_hydrolase",
            "name": "Metal-dependent hydrolase",
            "cofactors": ["Zn2+"],
            "active_site_signature": [
                {"role": "metal_ligand", "residue": "His/Asp/Glu/Cys"},
                {"role": "water_activator", "residue": "His/Asp/Glu"},
                {"role": "leaving_group_stabilizer", "residue": "variable"},
            ],
        }
        ser_his = {
            "id": "ser_his_acid_hydrolase",
            "name": "Ser-His-Asp/Glu hydrolase triad",
            "active_site_signature": [
                {"role": "nucleophile", "residue": "Ser"},
                {"role": "general_base", "residue": "His"},
                {"role": "acid_or_orienter", "residue": "Asp/Glu"},
            ],
        }
        self.assertLess(
            score_entry_against_fingerprint(entry, ser_his)["counterevidence_penalty"],
            1.0,
        )
        self.assertGreater(
            score_entry_against_fingerprint(entry, metal)["score"],
            score_entry_against_fingerprint(entry, ser_his)["score"],
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
