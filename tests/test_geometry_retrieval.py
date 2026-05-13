from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.geometry_retrieval import (
    COUNTEREVIDENCE_POLICY,
    COUNTEREVIDENCE_POLICY_VERSION,
    audit_geometry_retrieval_leakage_policy,
    compactness_score,
    counterevidence_assessment,
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

    def test_counterevidence_policy_records_rule_provenance(self) -> None:
        rule_ids = [rule.rule_id for rule in COUNTEREVIDENCE_POLICY]
        self.assertEqual(len(rule_ids), len(set(rule_ids)))
        self.assertGreater(len(rule_ids), 40)

        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "CYS", "roles": ["metal ligand", "radical stabilizer"]},
                {"code": "ASN", "roles": ["activator"]},
            ],
            cofactor_evidence="role_inferred",
            ligand_context={"ligand_codes": [], "cofactor_families": []},
            substrate_pocket_score_value=0.2,
        )
        self.assertEqual(assessment["policy_version"], COUNTEREVIDENCE_POLICY_VERSION)
        self.assertEqual(
            assessment["penalty_details"],
            [
                {
                    "reason": "role_inferred_metal_radical_transfer_roles",
                    "penalty": 0.68,
                }
            ],
        )
        self.assertEqual(
            assessment["policy_hits"],
            [
                {
                    "rule_id": "metal_dependent_hydrolase:role_inferred_metal_radical_transfer_roles",
                    "reason": "role_inferred_metal_radical_transfer_roles",
                    "penalty": 0.68,
                    "evidence_fields": ["cofactor_evidence", "residue_roles"],
                    "evidence_role": "counterevidence_only_not_predictive_evidence",
                    "leakage_flags": [],
                    "policy_version": COUNTEREVIDENCE_POLICY_VERSION,
                }
            ],
        )
        text_assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[{"code": "HIS", "roles": ["metal ligand"]}],
            cofactor_evidence="role_inferred",
            ligand_context={"ligand_codes": [], "cofactor_families": []},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=["A methylcobalamin methyl transfer reaction."],
        )
        text_hits = {
            hit["reason"]: hit for hit in text_assessment["policy_hits"]
        }
        self.assertEqual(
            text_hits["methylcobalamin_transfer_context_for_metal_hydrolase"][
                "leakage_flags"
            ],
            ["mechanism_text_review_context_only"],
        )

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
        self.assertLess(score["counterevidence_penalty"], 1.0)
        self.assertLess(score["score"], 0.7)

    def test_ser_his_coherence_requires_histidine_base(self) -> None:
        residues = [
            {"code": "SER", "roles": ["nucleophile"]},
            {"code": "LYS", "roles": ["proton acceptor", "proton donor"]},
            {"code": "GLU", "roles": ["proton acceptor", "proton donor"]},
        ]
        fingerprint = {"id": "ser_his_acid_hydrolase"}
        self.assertEqual(mechanistic_coherence_score(fingerprint, residues), 0.0)

    def test_ser_his_coherence_accepts_mcsa_role_synonyms(self) -> None:
        residues = [
            {"code": "SER", "roles": ["covalent catalysis"]},
            {"code": "HIS", "roles": ["proton shuttle (general acid/base)"]},
            {"code": "ASP", "roles": ["modifies pKa"]},
        ]
        fingerprint = {"id": "ser_his_acid_hydrolase"}
        self.assertEqual(mechanistic_coherence_score(fingerprint, residues), 1.0)

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

    def test_cobalamin_fingerprint_matches_role_aliases_and_motif_residues(self) -> None:
        entry = {
            "residues": [
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "TYR", "roles": ["radical stabiliser"]},
                {"code": "ARG", "roles": ["electrostatic stabiliser"]},
            ],
            "ligand_context": {"cofactor_families": ["cobalamin"], "ligand_codes": ["B12"]},
            "pairwise_distances_angstrom": [{"distance": 7}, {"distance": 8}, {"distance": 9}],
        }
        fingerprint = {
            "id": "cobalamin_radical_rearrangement",
            "name": "Adenosylcobalamin radical rearrangement",
            "cofactors": ["adenosylcobalamin"],
            "active_site_signature": [
                {"role": "cobalamin_ligand", "residue": "His"},
                {"role": "radical_stabilizer", "residue": "Tyr/Asp/Glu/Arg"},
                {"role": "substrate_orienter", "residue": "polar_or_charged_residue"},
            ],
        }
        score = score_entry_against_fingerprint(entry, fingerprint)
        self.assertEqual(score["cofactor_evidence_level"], "ligand_supported")
        self.assertEqual(score["residue_match_fraction"], 1.0)
        self.assertGreater(score["role_match_fraction"], 0.6)
        self.assertGreater(score["score"], 0.8)

    def test_cobalamin_fingerprint_penalizes_absent_cofactor_context(self) -> None:
        self.assertLess(
            counterevidence_penalty(
                fingerprint={"id": "cobalamin_radical_rearrangement"},
                residues=[
                    {"code": "HIS", "roles": ["metal ligand"]},
                    {"code": "TYR", "roles": ["radical stabiliser"]},
                ],
                cofactor_evidence="absent",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.5,
            ),
            0.5,
        )

    def test_plp_absent_context_requires_covalent_lysine_anchor(self) -> None:
        fingerprint = {"id": "plp_dependent_enzyme"}
        loose_lysine = [{"code": "LYS", "roles": ["hydrogen bond donor"]}]
        anchored_lysine = [{"code": "LYS", "roles": ["covalently attached"]}]
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=loose_lysine,
                cofactor_evidence="absent",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.2,
            ),
            1.0,
        )
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=anchored_lysine,
                cofactor_evidence="absent",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.2,
            ),
            1.0,
        )
        self.assertGreater(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=anchored_lysine,
                cofactor_evidence="absent",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.2,
            ),
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=loose_lysine,
                cofactor_evidence="absent",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.2,
            ),
        )

    def test_flavin_fingerprints_penalize_absent_flavin_context(self) -> None:
        self.assertLess(
            counterevidence_penalty(
                fingerprint={"id": "flavin_dehydrogenase_reductase"},
                residues=[{"code": "TYR", "roles": ["electron transfer"]}],
                cofactor_evidence="absent",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.5,
            ),
            1.0,
        )

    def test_flavin_dehydrogenase_uses_fe_s_single_electron_support(self) -> None:
        fingerprint = {
            "id": "flavin_dehydrogenase_reductase",
            "cofactors": ["FAD", "FMN"],
            "active_site_signature": [
                {"role": "flavin_binder", "residue": "basic_or_polar_motif"},
                {"role": "redox_acid_base", "residue": "His/Glu/Cys/Tyr/Arg"},
                {"role": "electron_transfer_path", "residue": "aromatic_or_redox_residue"},
            ],
        }
        residue_roles = {"single electron donor", "single electron relay"}
        ligand_context = {"cofactor_families": ["fe_s_cluster"]}
        self.assertGreater(
            cofactor_context_score(fingerprint, ["GLN", "TYR"], residue_roles, ligand_context),
            0.0,
        )
        self.assertGreater(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=[
                    {
                        "code": "GLN",
                        "roles": ["single electron donor", "single electron relay"],
                    }
                ],
                cofactor_evidence="absent",
                ligand_context=ligand_context,
                substrate_pocket_score_value=0.5,
            ),
            0.6,
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
        hydrophobic_assessment = counterevidence_assessment(
            fingerprint=fingerprint,
            residues=residues,
            cofactor_evidence="role_inferred",
            ligand_context={"cofactor_families": []},
            substrate_pocket_score_value=0.12,
            pocket_context={
                "descriptors": {
                    "hydrophobic_fraction": 0.55,
                    "polar_fraction": 0.18,
                    "negative_fraction": 0.02,
                },
            },
        )
        self.assertEqual(hydrophobic_assessment["penalty"], 0.70)
        self.assertIn(
            "role_inferred_metal_hydrophobic_low_pocket_support",
            hydrophobic_assessment["reasons"],
        )

    def test_role_inferred_metal_hydrolase_requires_water_activation_support(self) -> None:
        fingerprint = {"id": "metal_dependent_hydrolase"}
        weak_role_only_site = [
            {"code": "ASP", "roles": ["metal ligand"]},
            {"code": "SER", "roles": ["metal ligand"]},
            {"code": "ARG", "roles": ["electrostatic stabiliser"]},
        ]
        acid_base_supported_site = [
            {"code": "ASP", "roles": ["metal ligand"]},
            {"code": "HIS", "roles": ["proton acceptor", "proton donor"]},
            {"code": "GLU", "roles": ["increase acidity", "increase basicity"]},
        ]
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=weak_role_only_site,
                cofactor_evidence="role_inferred",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.2,
                compactness_score_value=0.5,
            ),
            0.75,
        )
        self.assertEqual(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=acid_base_supported_site,
                cofactor_evidence="role_inferred",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.2,
                compactness_score_value=0.5,
            ),
            1.0,
        )
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=acid_base_supported_site,
                cofactor_evidence="role_inferred",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.2,
                compactness_score_value=0.1,
            ),
            0.75,
        )
        phosphate_hydrolysis = counterevidence_assessment(
            fingerprint=fingerprint,
            residues=weak_role_only_site,
            cofactor_evidence="role_inferred",
            ligand_context={"cofactor_families": []},
            substrate_pocket_score_value=0.2,
            compactness_score_value=0.5,
            mechanism_text_snippets=[
                "A divalent cation coordinates the gamma-phosphate and water hydrolyses the phosphopolynucleotide substrate."
            ],
        )
        self.assertEqual(phosphate_hydrolysis["penalty"], 0.88)
        self.assertIn(
            "role_inferred_metal_phosphate_hydrolysis_text_support",
            phosphate_hydrolysis["reasons"],
        )

    def test_role_inferred_metal_hydrolase_penalizes_aromatic_positive_pocket(self) -> None:
        fingerprint = {"id": "metal_dependent_hydrolase"}
        residues = [
            {"code": "HIS", "roles": ["metal ligand"]},
            {"code": "GLU", "roles": ["metal ligand", "proton acceptor"]},
        ]
        pocket_context = {
            "nearby_residue_count": 5,
            "descriptors": {
                "aromatic_fraction": 0.24,
                "positive_fraction": 0.15,
            },
        }
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="role_inferred",
                ligand_context={"cofactor_families": []},
                substrate_pocket_score_value=0.18,
                pocket_context=pocket_context,
            ),
            1.0,
        )
        self.assertEqual(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="ligand_supported",
                ligand_context={"cofactor_families": ["metal_ion"]},
                substrate_pocket_score_value=0.18,
                pocket_context=pocket_context,
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
                ligand_context={"ligand_codes": ["SAM"], "cofactor_families": ["metal_ion", "sam"]},
                substrate_pocket_score_value=0.2,
            ),
            1.0,
        )
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="ligand_supported",
                ligand_context={"ligand_codes": ["GDP"], "cofactor_families": ["metal_ion"]},
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
            0.75,
        )
        apc_assessment = counterevidence_assessment(
            fingerprint=fingerprint,
            residues=residues,
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["APC", "MG"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
        )
        self.assertEqual(apc_assessment["penalty"], 0.68)
        self.assertIn("nucleotide_transfer_ligand_context", apc_assessment["reasons"])
        self.assertIn(
            {"reason": "nucleotide_transfer_ligand_context", "penalty": 0.68},
            apc_assessment["penalty_details"],
        )
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="ligand_supported",
                ligand_context={"ligand_codes": ["CU1", "ZN"], "cofactor_families": ["metal_ion"]},
                substrate_pocket_score_value=0.2,
            ),
            0.75,
        )
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="role_inferred",
                ligand_context={"ligand_codes": ["CUB", "MCN"], "cofactor_families": []},
                substrate_pocket_score_value=0.2,
            ),
            0.75,
        )
        self.assertLess(
            counterevidence_penalty(
                fingerprint=fingerprint,
                residues=residues,
                cofactor_evidence="ligand_supported",
                ligand_context={"ligand_codes": ["MG", "DAD"], "cofactor_families": ["metal_ion"]},
                substrate_pocket_score_value=0.2,
            ),
            0.75,
        )

    def test_metal_hydrolase_penalizes_hydrogenase_and_nonhydrolytic_iron_context(self) -> None:
        fingerprint = {"id": "metal_dependent_hydrolase"}
        hydrogenase_site = [
            {"code": "CYS", "roles": ["metal ligand", "proton donor"]},
            {"code": "CYS", "roles": ["metal ligand"]},
            {"code": "GLU", "roles": ["proton acceptor"]},
        ]
        nonheme_iron_site = [
            {"code": "HIS", "roles": ["metal ligand"]},
            {"code": "HIS", "roles": ["metal ligand"]},
            {"code": "GLU", "roles": ["metal ligand"]},
            {"code": "SER", "roles": ["steric role"]},
        ]
        hydrogenase = counterevidence_assessment(
            fingerprint=fingerprint,
            residues=hydrogenase_site,
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["FCO", "NI"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
        )
        self.assertLess(hydrogenase["penalty"], 0.75)
        self.assertIn("metal_redox_ligand_context", hydrogenase["reasons"])

        oxygenase = counterevidence_assessment(
            fingerprint=fingerprint,
            residues=nonheme_iron_site,
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["FE"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.14,
            pocket_context={
                "descriptors": {
                    "aromatic_fraction": 0.25,
                    "positive_fraction": 0.04,
                },
            },
        )
        self.assertLess(oxygenase["penalty"], 0.75)
        self.assertIn(
            "nonheme_iron_aromatic_low_pocket_without_water_activation",
            oxygenase["reasons"],
        )

        supported_hydrolase = counterevidence_penalty(
            fingerprint=fingerprint,
            residues=[
                {"code": "CYS", "roles": ["metal ligand"]},
                {"code": "GLU", "roles": ["proton acceptor", "proton donor"]},
                {"code": "HIS", "roles": ["metal ligand"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["FE"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.14,
            pocket_context={
                "descriptors": {
                    "aromatic_fraction": 0.25,
                    "positive_fraction": 0.04,
                },
            },
        )
        self.assertEqual(supported_hydrolase, 1.0)

    def test_metal_hydrolase_penalizes_carbon_transfer_ligand_context(self) -> None:
        base_args = {
            "fingerprint": {"id": "metal_dependent_hydrolase"},
            "residues": [
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "ASP", "roles": ["metal ligand"]},
            ],
            "cofactor_evidence": "ligand_supported",
            "substrate_pocket_score_value": 0.2,
        }
        self.assertLess(
            counterevidence_penalty(
                **base_args,
                ligand_context={"ligand_codes": ["PGH", "ZN"], "cofactor_families": ["metal_ion"]},
            ),
            1.0,
        )
        self.assertLess(
            counterevidence_penalty(
                **base_args,
                ligand_context={"ligand_codes": ["ICT", "MG"], "cofactor_families": ["metal_ion"]},
            ),
            1.0,
        )
        self.assertLess(
            counterevidence_penalty(
                **base_args,
                ligand_context={"ligand_codes": ["U5P", "ZN"], "cofactor_families": ["metal_ion"]},
            ),
            1.0,
        )
        self.assertLess(
            counterevidence_penalty(
                **base_args,
                ligand_context={"ligand_codes": ["APG", "MG"], "cofactor_families": ["metal_ion"]},
            ),
            0.70,
        )
        self.assertLess(
            counterevidence_penalty(
                **base_args,
                ligand_context={"ligand_codes": ["SEP", "ZN"], "cofactor_families": ["metal_ion"]},
            ),
            0.70,
        )
        for ligand_code in ("G16", "TPP"):
            with self.subTest(ligand_code=ligand_code):
                self.assertLess(
                    counterevidence_penalty(
                        **base_args,
                        ligand_context={
                            "ligand_codes": [ligand_code, "MG"],
                            "cofactor_families": ["metal_ion"],
                        },
                    ),
                    0.70,
                )
        kcx_carboxyltransfer = counterevidence_assessment(
            **base_args,
            ligand_context={
                "ligand_codes": ["KCX", "MG", "ZN"],
                "cofactor_families": ["metal_ion"],
            },
        )
        self.assertEqual(kcx_carboxyltransfer["penalty"], 0.68)
        self.assertIn(
            "biotin_carboxyltransfer_mixed_metal_context",
            kcx_carboxyltransfer["reasons"],
        )
        self.assertEqual(
            counterevidence_penalty(
                **base_args,
                ligand_context={"ligand_codes": ["KCX", "ZN"], "cofactor_families": ["metal_ion"]},
            ),
            1.0,
        )
        self.assertEqual(
            counterevidence_penalty(
                **base_args,
                ligand_context={"ligand_codes": ["PO4", "ZN"], "cofactor_families": ["metal_ion"]},
            ),
            1.0,
        )

    def test_ligand_supported_metal_hydrolase_requires_residue_role_support(self) -> None:
        weak_metal = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "THR", "roles": ["nucleophile"]},
                {"code": "ASP", "roles": ["electrostatic stabiliser"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["MG"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
        )
        self.assertEqual(weak_metal["penalty"], 0.70)
        self.assertIn(
            "ligand_supported_metal_without_metal_ligand_roles",
            weak_metal["reasons"],
        )

        hydrophobic_low_pocket = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "ASP", "roles": ["metal ligand"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["MG"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.08,
            pocket_context={
                "descriptors": {
                    "hydrophobic_fraction": 0.56,
                    "polar_fraction": 0.12,
                    "negative_fraction": 0.03,
                },
            },
        )
        self.assertEqual(hydrophobic_low_pocket["penalty"], 0.70)
        self.assertIn(
            "ligand_supported_metal_hydrophobic_low_pocket_support",
            hydrophobic_low_pocket["reasons"],
        )

    def test_role_inferred_metal_hydrolase_penalizes_covalent_cleavage_roles(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "TYR", "roles": ["nucleophile"]},
                {"code": "ASP", "roles": ["metal ligand", "nucleofuge"]},
                {"code": "GLU", "roles": ["metal ligand"]},
            ],
            cofactor_evidence="role_inferred",
            ligand_context={"ligand_codes": [], "cofactor_families": []},
            substrate_pocket_score_value=0.2,
        )
        self.assertEqual(assessment["penalty"], 0.68)
        self.assertIn("role_inferred_metal_covalent_cleavage_roles", assessment["reasons"])

    def test_role_inferred_metal_hydrolase_penalizes_radical_transfer_roles(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "TYR", "roles": ["radical stabiliser"]},
                {"code": "ASN", "roles": ["activator"]},
            ],
            cofactor_evidence="role_inferred",
            ligand_context={"ligand_codes": [], "cofactor_families": []},
            substrate_pocket_score_value=0.2,
        )
        self.assertEqual(assessment["penalty"], 0.68)
        self.assertIn("role_inferred_metal_radical_transfer_roles", assessment["reasons"])
        self.assertEqual(
            assessment["penalty_details"],
            [
                {
                    "reason": "role_inferred_metal_radical_transfer_roles",
                    "penalty": 0.68,
                }
            ],
        )

    def test_role_inferred_metal_hydrolase_penalizes_structure_only_manganese_decarboxylase(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "HIS", "roles": ["metal ligand"]},
                {
                    "code": "ARG",
                    "roles": ["electrostatic stabiliser", "hydrogen bond donor"],
                },
                {"code": "GLU", "roles": ["metal ligand", "proton donor"]},
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "GLU", "roles": ["metal ligand"]},
            ],
            cofactor_evidence="role_inferred",
            ligand_context={
                "ligand_codes": [],
                "cofactor_families": [],
                "structure_ligand_codes": ["MN", "TRS"],
                "structure_cofactor_families": ["metal_ion"],
            },
            substrate_pocket_score_value=0.2,
        )
        self.assertEqual(assessment["penalty"], 0.68)
        self.assertIn(
            "structure_only_manganese_decarboxylase_context",
            assessment["reasons"],
        )

    def test_metal_hydrolase_penalizes_nonheme_biopterin_hydroxylase_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "SER", "roles": ["hydrogen bond donor"]},
                {"code": "GLU", "roles": ["metal ligand"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={
                "ligand_codes": ["FE"],
                "cofactor_families": ["metal_ion"],
                "structure_ligand_codes": ["FE", "HBI"],
                "structure_cofactor_families": ["metal_ion"],
            },
            substrate_pocket_score_value=0.14,
            pocket_context={
                "descriptors": {
                    "aromatic_fraction": 0.28,
                    "positive_fraction": 0.04,
                }
            },
        )
        self.assertEqual(assessment["penalty"], 0.64)
        self.assertIn("nonheme_iron_biopterin_hydroxylase_context", assessment["reasons"])

    def test_metal_hydrolase_penalizes_prenyl_carbocation_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "ASP", "roles": ["metal ligand"]},
                {"code": "ASP", "roles": ["metal ligand"]},
                {"code": "LYS", "roles": ["electrostatic stabiliser"]},
            ],
            cofactor_evidence="role_inferred",
            ligand_context={"ligand_codes": [], "cofactor_families": []},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "The diphosphate product remains associated while a carbocation "
                "intermediate reacts with isopentenyl diphosphate."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.58)
        self.assertIn("nonhydrolytic_prenyl_carbocation_text_context", assessment["reasons"])

    def test_metal_hydrolase_penalizes_farnesyltransferase_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "ASP", "roles": ["metal ligand"]},
                {"code": "CYS", "roles": ["metal ligand"]},
                {"code": "HIS", "roles": ["metal ligand"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["ZN", "FII"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "Protein farnesyltransferase positions the prenyl donor for transfer."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.58)
        self.assertIn("nonhydrolytic_metal_transfer_ligand_context", assessment["reasons"])
        self.assertIn("nonhydrolytic_prenyl_carbocation_text_context", assessment["reasons"])

    def test_metal_hydrolase_penalizes_nad_redox_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "CYS", "roles": ["metal ligand"]},
                {"code": "HIS", "roles": ["metal ligand", "proton relay"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["ZN", "NAD"], "cofactor_families": ["metal_ion", "nad"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "The alcohol substrate is oxidised by hydride transfer to NAD+."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.62)
        self.assertIn("metal_bound_nad_redox_text_context", assessment["reasons"])

    def test_metal_hydrolase_penalizes_nonhydrolytic_isomerase_lyase_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "ASP", "roles": ["metal ligand"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["MG"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "The cycloisomerase reaction proceeds through an enolate and "
                "finishes with epimerisation of the bound substrate."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.62)
        self.assertIn("nonhydrolytic_isomerase_lyase_text_context", assessment["reasons"])

    def test_metal_hydrolase_penalizes_nonhydrolytic_hydratase_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "GLU", "roles": ["metal ligand", "proton acceptor"]},
                {"code": "LYS", "roles": ["electrostatic stabiliser"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["MG"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "Phosphopyruvate hydratase performs reversible dehydration and hydration "
                "during inter-conversion of 2-PGA and PEP."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.62)
        self.assertIn(
            "nonhydrolytic_hydratase_dehydratase_text_context",
            assessment["reasons"],
        )
        carbonate_dehydratase = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "GLU", "roles": ["proton acceptor"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["ZN"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "Carbonate dehydratase uses zinc-bound hydroxide to attack carbon dioxide, "
                "forming bicarbonate before water is deprotonated."
            ],
        )
        self.assertNotIn(
            "nonhydrolytic_hydratase_dehydratase_text_context",
            carbonate_dehydratase["reasons"],
        )

    def test_metal_hydrolase_penalizes_alpha_ketoglutarate_hydroxylation_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "ASP", "roles": ["metal ligand"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["NI"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "JmjC demethylase catalyses alpha-ketoglutarate-dependent hydroxylation "
                "to form demethylated lysine and formaldehyde."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.55)
        self.assertIn(
            "nonhydrolytic_alpha_ketoglutarate_hydroxylation",
            assessment["reasons"],
        )

    def test_metal_hydrolase_penalizes_aminoacyl_ligase_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "CYS", "roles": ["metal ligand"]},
                {"code": "LYS", "roles": ["electrostatic stabiliser"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["ZN"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "Methionine-tRNA ligase forms an aminoacyl adenylate with ATP "
                "before transferring the amino acid to tRNA."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.58)
        self.assertIn("aminoacyl_ligase_not_metal_hydrolysis", assessment["reasons"])

    def test_metal_hydrolase_penalizes_glycosidase_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "ASP", "roles": ["metal ligand"]},
                {"code": "GLU", "roles": ["proton shuttle (general acid/base)"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["CA"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "Isoamylase is a glycosidase with Asp/Glu glycosyl hydrolase chemistry."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.58)
        self.assertIn("glycosidase_not_metal_hydrolase_seed", assessment["reasons"])

    def test_mechanism_text_does_not_boost_plp_score(self) -> None:
        entry_with_text = {
            "mechanism_text_snippets": [
                "The enzyme proceeds through transaldimination and an external aldimine."
            ],
            "residues": [
                {"code": "TYR", "roles": ["proton shuttle (general acid/base)"]},
                {"code": "ASP", "roles": ["electrostatic stabiliser"]},
            ],
            "ligand_context": {"ligand_codes": ["LLP"], "cofactor_families": ["plp"]},
            "pocket_context": {"nearby_residue_count": 1, "descriptors": {"polar_fraction": 0.3}},
            "pairwise_distances_angstrom": [{"distance": 14.5}],
        }
        fingerprint = {
            "id": "plp_dependent_enzyme",
            "name": "Pyridoxal phosphate dependent enzyme",
            "cofactors": ["pyridoxal phosphate"],
            "active_site_signature": [
                {"role": "plp_anchor", "residue": "Lys"},
                {"role": "acid_base", "residue": "Asp/Glu/His/Tyr"},
                {"role": "phosphate_binder", "residue": "Gly/Ser/Thr-rich motif"},
            ],
        }
        entry_without_text = dict(entry_with_text)
        entry_without_text["mechanism_text_snippets"] = []
        score_with_text = score_entry_against_fingerprint(entry_with_text, fingerprint)
        score_without_text = score_entry_against_fingerprint(entry_without_text, fingerprint)
        self.assertEqual(score_with_text["score"], score_without_text["score"])
        self.assertEqual(score_with_text["plp_ligand_anchor_score"], 0.67)
        self.assertGreaterEqual(score_with_text["score"], 0.42)
        self.assertFalse(score_with_text["text_or_label_fields_used_for_score"])

    def test_geometry_retrieval_records_text_free_scoring_policy(self) -> None:
        entry = {
            "entry_id": "example:1",
            "entry_name": "PLP review context only",
            "mechanism_text_snippets": [
                "A PLP external aldimine aligns the sulfur atom for C-S bond cleavage "
                "during beta-elimination."
            ],
            "residues": [
                {"code": "TYR", "roles": ["proton shuttle (general acid/base)"]},
                {"code": "ASP", "roles": ["electrostatic stabiliser"]},
                {"code": "ARG", "roles": ["electrostatic stabiliser"]},
            ],
            "ligand_context": {"ligand_codes": ["LLP"], "cofactor_families": ["plp"]},
            "pocket_context": {"nearby_residue_count": 50, "descriptors": {"polar_fraction": 0.32}},
            "pairwise_distances_angstrom": [{"distance": 14.5}],
        }
        fingerprint = {
            "id": "plp_dependent_enzyme",
            "name": "Pyridoxal phosphate dependent enzyme",
            "cofactors": ["pyridoxal phosphate"],
            "active_site_signature": [
                {"role": "plp_anchor", "residue": "Lys"},
                {"role": "acid_base", "residue": "Asp/Glu/His/Tyr"},
                {"role": "phosphate_binder", "residue": "Gly/Ser/Thr-rich motif"},
            ],
        }
        retrieval = run_geometry_retrieval({"entries": [entry]}, top_k=20)
        metadata = retrieval["metadata"]
        self.assertEqual(
            metadata["blocker_removed"],
            "text_leakage_mitigation_geometry_retrieval",
        )
        self.assertFalse(metadata["leakage_policy"]["text_or_label_fields_used_for_score"])
        self.assertIn(
            "mechanism_text_snippets",
            metadata["leakage_policy"]["excluded_predictive_fields"],
        )
        self.assertIn(
            "local_plp_ligand_anchor_context",
            metadata["predictive_evidence_sources"],
        )
        plp_hit = next(
            hit
            for hit in retrieval["results"][0]["top_fingerprints"]
            if hit["fingerprint_id"] == "plp_dependent_enzyme"
        )
        self.assertFalse(plp_hit["text_or_label_fields_used_for_score"])
        self.assertEqual(plp_hit["plp_ligand_anchor_score"], 1.0)

    def test_geometry_retrieval_leakage_policy_audit_rejects_predictive_text(
        self,
    ) -> None:
        clean = run_geometry_retrieval(
            {
                "entries": [
                    {
                        "entry_id": "example:1",
                        "entry_name": "Text review context",
                        "mechanism_text_snippets": ["Text stays review-only."],
                        "residues": [{"code": "LYS", "roles": ["plp anchor"]}],
                        "ligand_context": {
                            "ligand_codes": ["LLP"],
                            "cofactor_families": ["plp"],
                        },
                    }
                ]
            }
        )
        self.assertTrue(
            audit_geometry_retrieval_leakage_policy(clean)["metadata"][
                "guardrail_clean"
            ]
        )

        leaky = dict(clean)
        leaky["metadata"] = dict(clean["metadata"])
        leaky["metadata"]["predictive_evidence_sources"] = [
            "mechanism_text_snippets"
        ]
        leaky["results"] = [dict(clean["results"][0])]
        leaky["results"][0]["top_fingerprints"] = [
            dict(clean["results"][0]["top_fingerprints"][0])
        ]
        leaky["results"][0]["top_fingerprints"][0][
            "text_or_label_fields_used_for_score"
        ] = True
        audit = audit_geometry_retrieval_leakage_policy(leaky)
        self.assertFalse(audit["metadata"]["guardrail_clean"])
        self.assertIn(
            "geometry_retrieval_leakage_prone_predictive_source",
            audit["metadata"]["blockers"],
        )
        self.assertIn(
            "geometry_retrieval_hit_uses_text_or_label_score",
            audit["metadata"]["blockers"],
        )

    def test_ser_his_hydrolase_penalizes_phosphoryl_transfer_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "ser_his_acid_hydrolase"},
            residues=[
                {"code": "SER", "roles": ["hydrogen bond donor"]},
                {"code": "HIS", "roles": ["proton acceptor"]},
                {"code": "ASP", "roles": ["nucleophile"]},
            ],
            cofactor_evidence="not_required",
            ligand_context={"ligand_codes": [], "cofactor_families": []},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "The phosphomutase mechanism forms a phosphorylated aspartate "
                "and proceeds through a metaphosphate intermediate."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.55)
        self.assertIn("ser_his_phosphoryl_transfer_text_context", assessment["reasons"])

    def test_ser_his_hydrolase_penalizes_acyl_transfer_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "ser_his_acid_hydrolase"},
            residues=[
                {"code": "SER", "roles": ["nucleophile", "covalently attached"]},
                {"code": "HIS", "roles": ["proton acceptor", "proton donor"]},
                {"code": "GLN", "roles": ["hydrogen bond donor"]},
            ],
            cofactor_evidence="not_required",
            ligand_context={"ligand_codes": [], "cofactor_families": []},
            substrate_pocket_score_value=0.8,
            mechanism_text_snippets=[
                "Malonyl-CoA-acyl carrier protein transacylase performs acyl transfer "
                "through a tetrahedral intermediate."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.55)
        self.assertIn("ser_his_acyl_transfer_not_hydrolysis", assessment["reasons"])

    def test_flavin_dehydrogenase_penalizes_tpp_carboligation_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "flavin_dehydrogenase_reductase"},
            residues=[
                {"code": "GLU", "roles": ["proton acceptor"]},
                {"code": "PHE", "roles": ["steric role"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["FAD"], "cofactor_families": ["flavin"]},
            substrate_pocket_score_value=0.5,
            mechanism_text_snippets=[
                "Acetolactate synthase uses thiamine diphosphate carboligation "
                "before any indirect FAD/O2 cycle."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.45)
        self.assertIn(
            "thiamine_carboligation_not_local_flavin_redox",
            assessment["reasons"],
        )

    def test_flavin_monooxygenase_penalizes_tpp_carboligation_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "flavin_monooxygenase"},
            residues=[
                {"code": "GLN", "roles": ["hydrogen bond donor"]},
                {"code": "LYS", "roles": ["electrostatic stabiliser"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["FAD"], "cofactor_families": ["flavin"]},
            substrate_pocket_score_value=0.5,
            mechanism_text_snippets=[
                "Acetolactate synthase uses thiamine diphosphate carbon-carbon condensation."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.45)
        self.assertIn(
            "thiamine_carboligation_not_flavin_oxygenation",
            assessment["reasons"],
        )

    def test_metal_hydrolase_penalizes_zinc_methyltransfer_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "CYS", "roles": ["metal ligand"]},
                {"code": "CYS", "roles": ["metal ligand"]},
            ],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["ZN"], "cofactor_families": ["metal_ion"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "The zinc ion stabilises the methyl acceptor thiolate for methyl transfer."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.55)
        self.assertIn("zinc_methyltransfer_not_hydrolysis", assessment["reasons"])

    def test_cobalamin_radical_penalizes_methylcobalamin_transfer_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "cobalamin_radical_rearrangement"},
            residues=[{"code": "HIS", "roles": ["metal ligand"]}],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["COB"], "cofactor_families": ["cobalamin"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "Methylcobalamin catalysis uses heterolytic Co-C bond cleavage for methyl transfer."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.45)
        self.assertIn(
            "methylcobalamin_transfer_not_radical_rearrangement",
            assessment["reasons"],
        )

    def test_metal_hydrolase_penalizes_methylcobalamin_transfer_text_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[{"code": "HIS", "roles": ["metal ligand"]}],
            cofactor_evidence="role_inferred",
            ligand_context={"ligand_codes": ["COB"], "cofactor_families": ["cobalamin"]},
            substrate_pocket_score_value=0.2,
            mechanism_text_snippets=[
                "Methylcobalamin catalysis uses heterolytic Co-C bond cleavage for methyl transfer."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.45)
        self.assertIn(
            "methylcobalamin_transfer_context_for_metal_hydrolase",
            assessment["reasons"],
        )

    def test_plp_seed_penalizes_non_plp_aldolase_schiff_base_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "plp_dependent_enzyme"},
            residues=[
                {"code": "LYS", "roles": ["covalently attached", "electron pair donor"]},
                {"code": "ASP", "roles": ["hydrogen bond acceptor"]},
            ],
            cofactor_evidence="absent",
            ligand_context={"ligand_codes": ["13P"], "cofactor_families": []},
            substrate_pocket_score_value=0.2,
        )
        self.assertEqual(assessment["penalty"], 0.60)
        self.assertIn("non_plp_aldolase_schiff_base_context", assessment["reasons"])
        self.assertIn("absent_plp_ligand_with_lysine_anchor", assessment["reasons"])

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

    def test_metal_hydrolase_penalizes_histidine_only_metal_site(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "metal_dependent_hydrolase"},
            residues=[
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "HIS", "roles": ["metal ligand"]},
                {"code": "PHE", "roles": ["steric role"]},
            ],
            cofactor_evidence="role_inferred",
            ligand_context={"ligand_codes": [], "cofactor_families": []},
            substrate_pocket_score_value=0.2,
        )
        self.assertEqual(assessment["penalty"], 0.68)
        self.assertIn("role_inferred_histidine_only_metal_site", assessment["reasons"])

    def test_heme_fingerprint_penalizes_molybdenum_center_context(self) -> None:
        self.assertLess(
            counterevidence_penalty(
                fingerprint={"id": "heme_peroxidase_oxidase"},
                residues=[
                    {"code": "CYS", "roles": ["metal ligand"]},
                    {"code": "HIS", "roles": ["metal ligand"]},
                    {"code": "TYR", "roles": ["proton relay"]},
                ],
                cofactor_evidence="ligand_supported",
                ligand_context={
                    "ligand_codes": ["HEM", "MO", "MTE"],
                    "cofactor_families": ["heme"],
                },
                substrate_pocket_score_value=0.3,
            ),
            0.64,
        )

    def test_heme_fingerprint_penalizes_absent_heme_context(self) -> None:
        self.assertLess(
            counterevidence_penalty(
                fingerprint={"id": "heme_peroxidase_oxidase"},
                residues=[
                    {"code": "HIS", "roles": ["hydrogen bond donor"]},
                    {"code": "TYR", "roles": ["proton relay"]},
                ],
                cofactor_evidence="absent",
                ligand_context={"ligand_codes": [], "cofactor_families": []},
                substrate_pocket_score_value=0.4,
            ),
            0.66,
        )

    def test_flavin_monooxygenase_penalizes_missing_reductant_context(self) -> None:
        self.assertLess(
            counterevidence_penalty(
                fingerprint={"id": "flavin_monooxygenase"},
                residues=[{"code": "SER", "roles": ["proton relay"]}],
                cofactor_evidence="ligand_supported",
                ligand_context={"ligand_codes": ["FAD"], "cofactor_families": ["flavin"]},
                substrate_pocket_score_value=0.5,
            ),
            counterevidence_penalty(
                fingerprint={"id": "flavin_dehydrogenase_reductase"},
                residues=[{"code": "SER", "roles": ["proton relay"]}],
                cofactor_evidence="ligand_supported",
                ligand_context={"ligand_codes": ["FAD"], "cofactor_families": ["flavin"]},
                substrate_pocket_score_value=0.5,
            ),
        )

    def test_flavin_retrieval_separates_monooxygenase_substrate_from_dehydrogenase(self) -> None:
        monooxygenase_context = {
            "ligand_codes": ["FAD", "PHB"],
            "cofactor_families": ["flavin"],
        }
        monooxygenase_penalty = counterevidence_penalty(
            fingerprint={"id": "flavin_monooxygenase"},
            residues=[{"code": "TYR", "roles": ["proton donor"]}],
            cofactor_evidence="ligand_supported",
            ligand_context=monooxygenase_context,
            substrate_pocket_score_value=0.4,
        )
        dehydrogenase = counterevidence_assessment(
            fingerprint={"id": "flavin_dehydrogenase_reductase"},
            residues=[{"code": "TYR", "roles": ["proton donor"]}],
            cofactor_evidence="ligand_supported",
            ligand_context=monooxygenase_context,
            substrate_pocket_score_value=0.4,
        )
        self.assertEqual(monooxygenase_penalty, 1.0)
        self.assertLess(dehydrogenase["penalty"], 0.6)
        self.assertIn(
            "flavin_monooxygenase_substrate_without_electron_transfer_context",
            dehydrogenase["reasons"],
        )

    def test_flavin_dehydrogenase_penalizes_nonflavin_fe_s_metal_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "flavin_dehydrogenase_reductase"},
            residues=[{"code": "HIS", "roles": ["single electron donor"]}],
            cofactor_evidence="absent",
            ligand_context={
                "ligand_codes": ["FES", "FE"],
                "cofactor_families": ["fe_s_cluster", "metal_ion"],
            },
            substrate_pocket_score_value=0.5,
        )
        self.assertLess(assessment["penalty"], 0.6)
        self.assertIn("nonheme_iron_fe_s_without_flavin_context", assessment["reasons"])

        molybdenum = counterevidence_assessment(
            fingerprint={"id": "flavin_dehydrogenase_reductase"},
            residues=[{"code": "CYS", "roles": ["single electron donor"]}],
            cofactor_evidence="absent",
            ligand_context={"ligand_codes": ["MGD", "FES"], "cofactor_families": ["fe_s_cluster"]},
            substrate_pocket_score_value=0.5,
        )
        self.assertLess(molybdenum["penalty"], 0.6)
        self.assertIn("molybdenum_center_without_flavin_context", molybdenum["reasons"])

        fe_s_only = counterevidence_assessment(
            fingerprint={"id": "flavin_dehydrogenase_reductase"},
            residues=[{"code": "CYS", "roles": ["single electron relay"]}],
            cofactor_evidence="absent",
            ligand_context={"ligand_codes": ["SF4"], "cofactor_families": ["fe_s_cluster"]},
            substrate_pocket_score_value=0.5,
        )
        self.assertEqual(fe_s_only["penalty"], 0.63)
        self.assertIn("fe_s_single_electron_partial_flavin_context", fe_s_only["reasons"])

    def test_flavin_dehydrogenase_penalizes_flavin_mutase_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "flavin_dehydrogenase_reductase"},
            residues=[{"code": "ARG", "roles": ["electrostatic stabiliser"]}],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["FAD"], "cofactor_families": ["flavin"]},
            substrate_pocket_score_value=0.5,
            mechanism_text_snippets=[
                "UDP-galactopyranose mutase uses reduced FAD with UDP-Galp and loss of UDP."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.55)
        self.assertIn("flavin_mutase_not_dehydrogenase_reductase", assessment["reasons"])

    def test_heme_fingerprint_penalizes_heme_dehydratase_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "heme_peroxidase_oxidase"},
            residues=[{"code": "HIS", "roles": ["metal ligand"]}],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["HEM"], "cofactor_families": ["heme"]},
            substrate_pocket_score_value=0.5,
            mechanism_text_snippets=[
                "A heme-bound aldoxime dehydratase carries out a dehydration reaction."
            ],
        )
        self.assertEqual(assessment["penalty"], 0.55)
        self.assertIn("heme_dehydratase_not_peroxidase_oxidase", assessment["reasons"])

    def test_flavin_monooxygenase_penalizes_nad_only_context(self) -> None:
        self.assertLess(
            counterevidence_penalty(
                fingerprint={"id": "flavin_monooxygenase"},
                residues=[{"code": "LYS", "roles": ["electrostatic stabiliser"]}],
                cofactor_evidence="ligand_supported",
                ligand_context={"ligand_codes": ["NAD"], "cofactor_families": ["nad"]},
                substrate_pocket_score_value=0.5,
            ),
            0.75,
        )
        assessment = counterevidence_assessment(
            fingerprint={"id": "flavin_monooxygenase"},
            residues=[{"code": "LYS", "roles": ["electrostatic stabiliser"]}],
            cofactor_evidence="ligand_supported",
            ligand_context={"ligand_codes": ["NAD"], "cofactor_families": ["nad"]},
            substrate_pocket_score_value=0.5,
        )
        self.assertIn("nad_only_or_nonflavin_context", assessment["reasons"])

    def test_ser_his_hydrolase_penalizes_nonhydrolytic_electrophile_context(self) -> None:
        assessment = counterevidence_assessment(
            fingerprint={"id": "ser_his_acid_hydrolase"},
            residues=[
                {"code": "SER", "roles": ["nucleophile", "covalently attached"]},
                {"code": "HIS", "roles": ["proton acceptor", "proton donor"]},
                {"code": "GLU", "roles": ["electrophile"]},
            ],
            cofactor_evidence="not_required",
            ligand_context={"ligand_codes": [], "cofactor_families": []},
            substrate_pocket_score_value=0.7,
        )
        self.assertEqual(assessment["penalty"], 0.45)
        self.assertIn(
            "ser_his_nonhydrolytic_electrophile_without_leaving_group",
            assessment["reasons"],
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
                        "entry_name": "Example hydrolase",
                        "pdb_id": "1ABC",
                        "status": "ok",
                        "mechanism_text_count": 1,
                        "mechanism_text_snippets": [
                            "Serine attacks the substrate in a compact acid-base site."
                        ],
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
        self.assertEqual(artifact["results"][0]["entry_name"], "Example hydrolase")
        self.assertEqual(artifact["results"][0]["mechanism_text_count"], 1)
        self.assertEqual(
            artifact["results"][0]["mechanism_text_snippets"],
            ["Serine attacks the substrate in a compact acid-base site."],
        )
        self.assertEqual(len(artifact["results"][0]["top_fingerprints"]), 3)


if __name__ == "__main__":
    unittest.main()
