"""Offline validation of non-heme iron 2OG broadened-handle sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.non_heme_iron_2og_sourcing import (
    FAMILIES,
    build_non_heme_iron_2og_sourcing,
)

_ROWS = {
    "OG0001": (
        "1.14.11.2",
        ["Dioxygenase", "Oxidoreductase"],
        "L-proline + 2-oxoglutarate + O2 = trans-4-hydroxy-L-proline + succinate + CO2",
        "Fe(2+)",
    ),
    "OG0002": (
        "1.14.11.33",
        ["Dioxygenase"],
        "methylated DNA + 2-oxoglutarate + O2 = demethylated DNA + succinate + CO2 + formaldehyde",
        "iron",
    ),
    # EC 1.14.11 + iron but no 2OG/Dioxygenase mechanism handle: EC alone must hold.
    "NX0001": (
        "1.14.11.2",
        ["Oxidoreductase"],
        "a donor + an acceptor = products",
        "Fe(2+)",
    ),
    # Heme oxygenase/P450-like control should not enter non-heme 2OG.
    "HX0001": (
        "1.14.11.2",
        ["Dioxygenase", "Cytochrome P450"],
        "RH + O2 + 2-oxoglutarate = ROH + succinate + CO2",
        "heme b",
    ),
    # Flavin oxygenase control should not enter non-heme 2OG.
    "FX0001": (
        "1.14.11.2",
        ["Dioxygenase"],
        "substrate + 2-oxoglutarate + O2 = product + succinate + CO2",
        "FAD",
    ),
}


def _search_record(accession):
    ec, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": f"Test enzyme {accession}",
        "organism": f"Organism {accession}",
        "length": 360,
        "sequence": "M" + "A" * 359,
        "ec_numbers": [ec],
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _entry_record(accession):
    ec, keywords, reaction, cofactor = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "sequence_length": 360,
        "keywords": keywords,
        "active_site_features": [
            {
                "feature_type": "Active site",
                "begin": 180,
                "end": 180,
                "description": "2-His-1-carboxylate facial triad",
                "ligand_name": None,
                "ligand_id": None,
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
        ],
        "binding_site_features": [
            {
                "feature_type": "Binding site",
                "begin": 85,
                "end": 85,
                "description": "metal / 2-oxoglutarate binding",
                "ligand_name": cofactor,
                "ligand_id": None,
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
        ],
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": [
            {
                "reaction": reaction,
                "ec_number": ec,
                "cross_references": [{"database": "Rhea", "id": f"RHEA:{accession}"}],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        ],
        "cofactor_comments": [
            {
                "cofactors": [
                    {
                        "name": cofactor,
                        "cross_reference": {"id": None},
                        "evidence": [{"evidence_code": "ECO:0000269"}],
                    }
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


class NonHemeIron2ogSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_non_heme_iron_2og_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T00:17:04Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_non_heme_iron_2og(self):
        self.assertEqual(FAMILIES, ("non_heme_iron_2og_dioxygenase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["disambiguation_hold_count"], 2)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 1)
        self.assertEqual(
            audit["counts"]["off_target_fingerprint_counts"],
            {"cytochrome_p450_monooxygenase": 1},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"non_heme_iron_2og_dioxygenase": 2},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "non_heme_iron_2og_dioxygenase")
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

    def test_two_og_axes_are_mechanism_not_ec(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:OG0001", "uniprot:OG0002"})
        axes = labels["uniprot:OG0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)

    def test_ec_only_heme_and_flavin_controls_do_not_enter_family(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertNotIn("uniprot:NX0001", admitted_ids)
        self.assertNotIn("uniprot:HX0001", admitted_ids)
        self.assertNotIn("uniprot:FX0001", admitted_ids)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["non_heme_iron_2og_dioxygenase"]
        self.assertEqual(proj["deploy_missing_active_site_context"], "fe_ii_2og_o2_cosubstrate")
        self.assertEqual(proj["combined_before"], 0)
        self.assertEqual(proj["admitted_this_run"], 2)
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
        self.assertTrue(g["heme_flavin_peroxide_guard"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("cytochrome_p450_monooxygenase",))


if __name__ == "__main__":
    unittest.main()
