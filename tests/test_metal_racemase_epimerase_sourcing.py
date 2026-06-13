"""Offline validation of non-PLP racemase/epimerase broadened-handle sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.metal_racemase_epimerase_sourcing import (
    FAMILIES,
    build_metal_racemase_epimerase_non_plp_sourcing,
)

_ROWS = {
    "MR0001": (
        ["5.1.3.3"],
        ["Isomerase"],
        [],
        "Galactose mutarotase (Aldose 1-epimerase)",
        "alpha-D-galactose = beta-D-galactose",
        "Active site",
        "general acid/base residue",
    ),
    "MR0002": (
        ["5.1.99.4"],
        ["Isomerase"],
        [],
        "Alpha-methylacyl-CoA racemase",
        "a (2S)-2-methylacyl-CoA = a (2R)-2-methylacyl-CoA",
        "Binding site",
        "substrate binding pocket",
    ),
    # EC + Isomerase only: hold because EC/keyword alone is insufficient.
    "NX0001": (["5.1.3.3"], ["Isomerase"], [], "Test isomerase", "", "", ""),
    # PLP and side-EC rows are boundary rows.
    "PL0001": (
        ["5.1.1.1"],
        ["Isomerase"],
        ["pyridoxal 5'-phosphate"],
        "Alanine racemase",
        "L-alanine = D-alanine",
        "Binding site",
        "pyridoxal phosphate binding",
    ),
    "SE0001": (
        ["5.1.3.3", "2.5.1.18"],
        ["Isomerase"],
        [],
        "Dual-function epimerase transferase",
        "alpha-D-galactose = beta-D-galactose",
        "Active site",
        "general acid/base residue",
    ),
}


def _search_record(accession):
    ec, _, _, protein_name, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": protein_name,
        "organism": f"Organism {accession}",
        "length": 330,
        "sequence": "M" + "A" * 329,
        "ec_numbers": ec,
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _feature(feature_type, description):
    if not feature_type:
        return []
    return [
        {
            "feature_type": feature_type,
            "begin": 120,
            "end": 120,
            "description": description,
            "ligand_name": description if feature_type != "Active site" else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession):
    ec, keywords, cofactors, protein_name, reaction, feature_type, feature_description = _ROWS[
        accession
    ]
    active_features = (
        _feature(feature_type, feature_description) if feature_type == "Active site" else []
    )
    binding_features = (
        _feature(feature_type, feature_description) if feature_type == "Binding site" else []
    )
    catalytic = []
    if reaction:
        catalytic.append(
            {
                "reaction": reaction,
                "ec_number": ec[0],
                "cross_references": [{"database": "Rhea", "id": f"RHEA:{accession}"}],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        )
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "protein_name": protein_name,
        "sequence_length": 330,
        "keywords": keywords,
        "active_site_features": active_features,
        "binding_site_features": binding_features,
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": catalytic,
        "cofactor_comments": [
            {
                "cofactors": [
                    {
                        "name": name,
                        "cross_reference": {"id": None},
                        "evidence": [{"evidence_code": "ECO:0000269"}],
                    }
                    for name in cofactors
                ]
            }
        ],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query, size):
    records = [_search_record(a) for a in sorted(_ROWS)]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class MetalRacemaseEpimeraseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_metal_racemase_epimerase_non_plp_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T03:40:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            cap_ceiling=150,
            **kwargs,
        )

    def test_family_is_metal_racemase_epimerase_non_plp(self):
        self.assertEqual(FAMILIES, ("metal_racemase_epimerase_non_plp",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["disambiguation_hold_count"], 3)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 0)

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"metal_racemase_epimerase_non_plp": 2},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "metal_racemase_epimerase_non_plp")
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["review_status"], "automation_curated")
            self.assertTrue(label["entry_id"].startswith("uniprot:"))
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            for excluded in ("ec_label", "protein_name", "uniprot_prose", "target_family_lane"):
                self.assertIn(excluded, label["evidence"]["excluded_context"])
            tier = label["evidence"]["source_trust_tier"]
            self.assertEqual(tier["source_tier"], "source_tier_0")
            self.assertTrue(tier["meets_n_of_m"])
            self.assertNotIn("ec_scope_hint", tier["mechanism_corroborator_axes_present"])

    def test_axes_are_mechanism_not_ec(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:MR0001", "uniprot:MR0002"})
        axes = labels["uniprot:MR0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_ec_only_plp_and_side_ec_controls_do_not_enter_family(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        for accession in ("NX0001", "PL0001", "SE0001"):
            self.assertNotIn(f"uniprot:{accession}", admitted_ids)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["metal_racemase_epimerase_non_plp"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "racemase_epimerase_proton_shift_context",
        )
        self.assertEqual(proj["combined_before"], 0)
        self.assertEqual(proj["admitted_this_run"], 2)
        self.assertTrue(proj["chemistry_confusable"])
        self.assertEqual(proj["cap_ceiling"], 150)
        for label in audit["applied_labels"]:
            provenance = label["evidence"]["sequence_provenance"]
            accession = label["entry_id"].split(":", 1)[1]
            self.assertEqual(provenance["source_accession"], accession)
            self.assertEqual(len(provenance["sequence_sha256"]), 64)
            self.assertNotIn("sequence", json.dumps(label["evidence"]["excluded_context"]))

    def test_guardrails_non_destructive(self):
        audit = self._run()
        g = audit["guardrails"]
        self.assertFalse(g["curated_registry_written"])
        self.assertTrue(g["frozen_current702_benchmark_preserved"])
        self.assertTrue(g["plp_and_side_ec_boundary_guard"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("copper_oxidoreductase",))


if __name__ == "__main__":
    unittest.main()
