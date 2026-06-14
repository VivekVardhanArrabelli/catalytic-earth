"""Offline validation of the Stage-2 metal-hydrolase sub-family sourcing runner.

No network: the UniProt/Rhea fetchers are injected with synthetic payloads shaped
exactly like `adapters.normalize_uniprot_tsv` / `normalize_uniprot_entry_json`
output, so the full chain (fetch -> metal/EC disambiguation -> novelty gate ->
cap guard -> preview) is exercised end to end and the routing/guardrails asserted.
"""

from __future__ import annotations

import json
import unittest

from catalytic_earth.stage2_hydrolase_subfamily_sourcing import (
    SUBFAMILIES,
    build_stage2_hydrolase_subfamily_sourcing,
)

# accession -> (EC, cofactor names). One genuine row per sub-family, plus a metal-less
# peptidase EC that must be HELD (no metal corroboration).
_ROWS = {
    "MP0001": ("3.4.24.7", ["Zn(2+)"]),     # metallopeptidase
    "PE0001": ("3.1.4.1", ["Mg(2+)"]),      # metallophosphoesterase_nuclease
    "PM0001": ("3.1.3.1", ["Zn(2+)"]),      # metallophosphomonoesterase
    "AD0001": ("3.5.2.6", ["Zn(2+)"]),      # metallo_amidohydrolase_deaminase
    "NX0001": ("3.4.24.7", []),             # peptidase EC but NO metal -> held
}


def _search_record(accession):
    ec, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": f"Metal hydrolase test {accession}",
        "organism": f"Organism {accession}",
        "length": 400,
        "sequence": "M" + "A" * 399,
        "ec_numbers": [ec],
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _entry_record(accession):
    ec, cofactor_names = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "sequence_length": 400,
        "active_site_features": [
            {
                "feature_type": "Active site",
                "begin": 100,
                "end": 100,
                "description": "",
                "ligand_name": None,
                "ligand_id": None,
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
        ],
        "binding_site_features": [],
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": [
            {
                "reaction": f"reaction for {accession}",
                "ec_number": ec,
                "cross_references": [{"database": "Rhea", "id": f"RHEA:{accession}"}],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        ],
        "cofactor_comments": [
            {
                "cofactors": [
                    {
                        "name": name,
                        "cross_reference": {"database": "ChEBI", "id": "CHEBI:0"},
                        "evidence": [{"evidence_code": "ECO:0000269"}],
                    }
                    for name in cofactor_names
                ]
            }
        ]
        if cofactor_names
        else [],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query, size):
    # Return all rows on the first lane (the metallopeptidase 3.4.24 lane); cross-lane
    # dedup keeps each accession fetched once regardless of how many lanes match.
    if "3.4.24" in query:
        records = [_search_record(a) for a in _ROWS]
    else:
        records = []
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class Stage2SubfamilySourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_stage2_hydrolase_subfamily_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-11T00:00:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_fetches_and_routes_four_subfamilies(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        # four metal rows disambiguate; the metal-less peptidase is held.
        self.assertEqual(audit["counts"]["disambiguated_bronze_labels"], 4)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 1)

    def test_admitted_fingerprint_counts(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {
                "metallo_amidohydrolase_deaminase": 1,
                "metallopeptidase": 1,
                "metallophosphoesterase_nuclease": 1,
                "metallophosphomonoesterase": 1,
            },
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        by_fp = {label["fingerprint_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(by_fp), set(SUBFAMILIES))
        for label in audit["applied_labels"]:
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["review_status"], "automation_curated")
            self.assertEqual(label["label_type"], "seed_fingerprint")
            self.assertTrue(label["entry_id"].startswith("uniprot:"))
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            for excluded in ("ec_label", "protein_name", "uniprot_prose", "target_family_lane"):
                self.assertIn(excluded, label["evidence"]["excluded_context"])

    def test_admitted_labels_carry_deploy_input_sequence_provenance(self):
        # Source-time wiring: the deploy-input sequence is recorded natively under
        # evidence.sequence_provenance (the model input), NOT as a predictive feature.
        audit = self._run()
        for label in audit["applied_labels"]:
            provenance = label["evidence"]["sequence_provenance"]
            accession = label["entry_id"].split(":", 1)[1]
            self.assertEqual(provenance["source_accession"], accession)
            self.assertEqual(provenance["source"], "reviewed_uniprot")
            self.assertEqual(provenance["sequence"], "M" + "A" * 399)
            self.assertEqual(provenance["sequence_length"], 400)
            self.assertEqual(len(provenance["sequence_sha256"]), 64)
            # The sequence never leaks into the predictive/excluded channels.
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            self.assertNotIn(
                "sequence", json.dumps(label["evidence"]["excluded_context"])
            )

    def test_floor_projection_counts_admitted(self):
        audit = self._run()
        proj = audit["floor_projection"]["metallopeptidase"]
        self.assertEqual(proj["combined_before"], 0)
        self.assertEqual(proj["admitted_this_run"], 1)
        self.assertEqual(proj["projected_combined"], 1)
        self.assertFalse(proj["floor_reached"])
        self.assertFalse(proj["projected_over_cap"])

    def test_guardrails_non_destructive_and_split_metadata(self):
        audit = self._run()
        g = audit["guardrails"]
        self.assertFalse(g["curated_registry_written"])
        self.assertTrue(g["frozen_current702_benchmark_preserved"])
        self.assertFalse(g["predictive_features_use_ec_name_or_prose"])
        self.assertTrue(g["novelty_gated_against_both_registries"])
        self.assertTrue(g["no_new_labels_added_to_coarse_umbrella"])
        self.assertEqual(g["deploy_missing_active_site_context_per_subfamily"], "metal")
        self.assertEqual(audit["split_of"], "metal_dependent_hydrolase")

    def test_metal_less_peptidase_is_held(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertNotIn("uniprot:NX0001", admitted_ids)

    def test_reaction_aware_caps_default_off_is_backcompat(self):
        # Default flag off: effective_cap equals the flat cap_ceiling and the
        # admitted set is byte-identical to the historical behavior.
        baseline = self._run()
        audit = self._run()
        self.assertFalse(audit["guardrails"]["reaction_aware_caps_enabled"])
        self.assertIsNone(audit["guardrails"]["reaction_cap_rate"])
        self.assertIsNone(audit["guardrails"]["per_reaction_cap_at_admission"])
        proj = audit["floor_projection"]["metallopeptidase"]
        self.assertEqual(proj["effective_cap"], proj["cap_ceiling"])
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            baseline["counts"]["admitted_fingerprint_counts"],
        )

    def test_reaction_aware_caps_opt_in_surfaces_diversity_earned_cap(self):
        # Opt-in: each newly-sourced single-reaction subfamily earns only the floor.
        audit = self._run(reaction_aware_caps=True, reaction_cap_rate=8)
        self.assertTrue(audit["guardrails"]["reaction_aware_caps_enabled"])
        self.assertEqual(audit["guardrails"]["reaction_cap_rate"], 8)
        for proj in audit["floor_projection"].values():
            # one synthetic reaction per row -> floor-bounded cap, well above the
            # single admitted label so nothing is wrongly trimmed.
            self.assertEqual(proj["effective_cap"], 100)
            self.assertGreaterEqual(proj["distinct_reactions"], 1)
            self.assertFalse(proj["projected_over_effective_cap"])

    def test_per_reaction_cap_is_threaded_to_admission(self):
        audit = self._run(per_reaction_cap=12)
        self.assertEqual(audit["guardrails"]["per_reaction_cap_at_admission"], 12)

    def test_unknown_subfamily_rejected(self):
        with self.assertRaises(ValueError):
            self._run(subfamilies=("metal_dependent_hydrolase",))

    def test_subfamilies_are_the_four_v2_splits(self):
        self.assertEqual(
            set(SUBFAMILIES),
            {
                "metallopeptidase",
                "metallophosphoesterase_nuclease",
                "metallophosphomonoesterase",
                "metallo_amidohydrolase_deaminase",
            },
        )


if __name__ == "__main__":
    unittest.main()
