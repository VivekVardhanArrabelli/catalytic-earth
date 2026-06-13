"""Offline validation of CoA acyltransferase broadened-handle sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.coa_acyltransferase_sourcing import (
    FAMILIES,
    build_coa_acyltransferase_sourcing,
)

_ROWS = {
    "CA0001": (
        ["2.3.1.48"],
        ["Acyltransferase", "Transferase"],
        "acetyl-CoA + L-carnitine = CoA + O-acetyl-L-carnitine",
        "CoA binding",
        "Binding site",
    ),
    "CA0002": (
        ["2.3.1.225"],
        ["Acyltransferase"],
        "malonyl-CoA + acyl-carrier protein = CoA + malonyl-[acyl-carrier protein]",
        "catalytic His active-site base",
        "Active site",
    ),
    # EC 2.3.1 + Acyltransferase but no CoA/Rhea or active-site handle: EC/keyword alone holds.
    "NX0001": (
        ["2.3.1.48"],
        ["Acyltransferase"],
        "a donor + an acceptor = products",
        "",
        "",
    ),
    # Multi-EC hydrolase boundary row from the scout: explicit side-EC guard must hold.
    "HY0001": (
        ["2.3.1.48", "3.1.1.4"],
        ["Acyltransferase"],
        "acetyl-CoA + water = CoA + acetate",
        "CoA binding",
        "Binding site",
    ),
    # Off-target row should be held by the CoA wrapper, not imported through this lane.
    "GT0001": (
        ["2.4.1.1"],
        ["Glycosyltransferase"],
        "UDP-glucose + acceptor = UDP + glycosylated acceptor",
        "UDP-glucose binding",
        "Binding site",
    ),
}


def _search_record(accession):
    ec, _, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": f"Test enzyme {accession}",
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
            "ligand_name": "CoA" if "CoA" in description else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession):
    ec, keywords, reaction, feature_description, feature_type = _ROWS[accession]
    active_features = _feature(feature_type, feature_description) if feature_type == "Active site" else []
    binding_features = _feature(feature_type, feature_description) if feature_type == "Binding site" else []
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "sequence_length": 330,
        "keywords": keywords,
        "active_site_features": active_features,
        "binding_site_features": binding_features,
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": [
            {
                "reaction": reaction,
                "ec_number": ec[0],
                "cross_references": [{"database": "Rhea", "id": f"RHEA:{accession}"}],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        ],
        "cofactor_comments": [],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query, size):
    records = [_search_record(a) for a in sorted(_ROWS)]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class CoaAcyltransferaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_coa_acyltransferase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T01:22:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_coa_acyltransferase(self):
        self.assertEqual(FAMILIES, ("coa_acyltransferase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["disambiguation_hold_count"], 2)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 1)
        self.assertEqual(
            audit["counts"]["off_target_fingerprint_counts"],
            {"glycosyltransferase": 1},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"coa_acyltransferase": 2},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "coa_acyltransferase")
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

    def test_coa_axes_are_mechanism_not_ec(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:CA0001", "uniprot:CA0002"})
        axes = labels["uniprot:CA0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)

    def test_ec_only_and_hydrolase_controls_do_not_enter_family(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertNotIn("uniprot:NX0001", admitted_ids)
        self.assertNotIn("uniprot:HY0001", admitted_ids)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["coa_acyltransferase"]
        self.assertEqual(proj["deploy_missing_active_site_context"], "coa_acyl_coa_donor")
        self.assertEqual(proj["combined_before"], 0)
        self.assertEqual(proj["admitted_this_run"], 2)
        for label in audit["applied_labels"]:
            provenance = label["evidence"]["sequence_provenance"]
            accession = label["entry_id"].split(":", 1)[1]
            self.assertEqual(provenance["source_accession"], accession)
            self.assertEqual(len(provenance["sequence_sha256"]), 64)
            self.assertNotIn("sequence", json.dumps(label["evidence"]["excluded_context"]))

    def test_record_window_processes_slice_before_entry_fetch(self):
        audit = self._run(record_offset_per_lane=2, record_limit_per_lane=2)
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 2)
        self.assertEqual(audit["counts"]["record_offset_per_lane"], 2)
        self.assertEqual(audit["counts"]["record_limit_per_lane"], 2)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 0)
        self.assertEqual(audit["counts"]["disambiguation_hold_count"], 1)
        self.assertEqual(
            audit["counts"]["off_target_fingerprint_counts"],
            {"glycosyltransferase": 1},
        )
        lane = audit["lane_summaries"][0]
        self.assertEqual(lane["record_offset_per_lane"], 2)
        self.assertEqual(lane["record_limit_per_lane"], 2)

    def test_guardrails_non_destructive(self):
        audit = self._run()
        g = audit["guardrails"]
        self.assertFalse(g["curated_registry_written"])
        self.assertTrue(g["frozen_current702_benchmark_preserved"])
        self.assertTrue(g["hydrolase_side_ec_guard"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("sam_methyltransferase",))


if __name__ == "__main__":
    unittest.main()
