"""Offline validation of dihydrofolate-reductase sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.dihydrofolate_reductase_sourcing import (
    FAMILIES,
    build_dihydrofolate_reductase_sourcing,
)

# accession -> (ec, protein_name, keywords, reaction, feature_type, feature_description)
_ROWS = {
    "DHFR001": (
        ["1.5.1.3"],
        "Dihydrofolate reductase",
        ["Oxidoreductase", "One-carbon metabolism"],
        "(6S)-5,6,7,8-tetrahydrofolate + NADP(+) = 7,8-dihydrofolate + NADPH + H(+)",
        "Binding site",
        "NADP binding",
    ),
    "DHFR002": (
        ["1.5.1.3"],
        "Dihydrofolate reductase",
        ["Oxidoreductase"],
        "(6S)-5,6,7,8-tetrahydrofolate + NADP(+) = 7,8-dihydrofolate + NADPH + H(+)",
        "Active site",
        "folate-binding pocket",
    ),
    # A DHFR-named row with EC scope but NO folate-reduction reaction: held (reaction is the hard
    # anchor).
    "EC0001": (
        ["1.5.1.3"],
        "Putative dihydrofolate reductase",
        ["Oxidoreductase"],
        "",
        "",
        "",
    ),
    # Bifunctional DHFR-thymidylate synthase (EC 1.5.1.3 + 2.1.1.45): the non-1.5.1.3 side EC holds
    # the multi-mechanism row.
    "BIFN001": (
        ["1.5.1.3", "2.1.1.45"],
        "Bifunctional dihydrofolate reductase-thymidylate synthase",
        ["Oxidoreductase", "Methyltransferase"],
        "(6S)-5,6,7,8-tetrahydrofolate + NADP(+) = 7,8-dihydrofolate + NADPH + H(+)",
        "Binding site",
        "NADP binding",
    ),
    # Methylenetetrahydrofolate reductase (EC 1.5.1.20, off-scope for 1.5.1.3): held.
    "MTHFR01": (
        ["1.5.1.20"],
        "Methylenetetrahydrofolate reductase",
        ["Oxidoreductase", "FAD"],
        "5-methyltetrahydrofolate + NADP(+) = 5,10-methylenetetrahydrofolate + NADPH + H(+)",
        "Binding site",
        "FAD binding",
    ),
    # Dihydrofolate synthase (EC 6.3.2.12, folate ligation not reduction): off-scope, held.
    "DHFS001": (
        ["6.3.2.12"],
        "Dihydrofolate synthase",
        ["Ligase"],
        "7,8-dihydropteroate + ATP + L-glutamate = 7,8-dihydrofolate + ADP + phosphate",
        "Binding site",
        "ATP binding",
    ),
}

_QUERY_ORDER = ("EC0001", "DHFR001", "DHFR002", "BIFN001", "MTHFR01", "DHFS001")


def _sequence(accession: str) -> str:
    seed = (accession * 80)[:430]
    return "M" + "".join("A" if c.isdigit() else c for c in seed)


def _search_record(accession: str) -> dict:
    ec, name, keywords, _, _, _ = _ROWS[accession]
    seq = _sequence(accession)
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": name,
        "organism": f"Organism {accession}",
        "length": len(seq),
        "sequence": seq,
        "ec_numbers": ec,
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
        "keywords": keywords,
    }


def _feature(feature_type: str, description: str) -> list[dict]:
    if not feature_type:
        return []
    return [
        {
            "feature_type": feature_type,
            "begin": 27,
            "end": 27,
            "description": description,
            "ligand_name": description if feature_type != "Active site" else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession: str) -> dict:
    ec, _, keywords, reaction, feature_type, feature_description = _ROWS[accession]
    active_features = _feature(feature_type, feature_description) if feature_type == "Active site" else []
    binding_features = _feature(feature_type, feature_description) if feature_type == "Binding site" else []
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
        "sequence_length": len(_sequence(accession)),
        "keywords": keywords,
        "active_site_features": active_features,
        "binding_site_features": binding_features,
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": catalytic,
        "cofactor_comments": [],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query: str, size: int) -> dict:
    records = [_search_record(a) for a in _QUERY_ORDER]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records[:size]}


def _fake_entry_fetcher(accession: str) -> dict:
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number: str, limit: int) -> dict:
    return {"metadata": {"url": "test://rhea"}, "records": []}


class DihydrofolateReductaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_dihydrofolate_reductase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-27T00:00:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_dihydrofolate_reductase(self):
        self.assertEqual(FAMILIES, ("dihydrofolate_reductase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 6)
        # The two monofunctional DHFRs corroborate.
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 2)
        # EC0001 (no reaction), BIFN001 (side EC), MTHFR01 / DHFS001 (off-scope) are held.
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 2)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"dihydrofolate_reductase": 2},
        )

    def test_bifunctional_dhfr_ts_is_held(self):
        audit = self._run()
        admitted_ids = {label["entry_id"].split(":", 1)[1] for label in audit["applied_labels"]}
        self.assertNotIn("BIFN001", admitted_ids)

    def test_off_scope_folate_enzymes_are_held(self):
        # MTHFR (EC 1.5.1.20) and dihydrofolate synthase (EC 6.3.2.12) are off-scope for EC 1.5.1.3.
        audit = self._run()
        admitted_ids = {label["entry_id"].split(":", 1)[1] for label in audit["applied_labels"]}
        self.assertNotIn("MTHFR01", admitted_ids)
        self.assertNotIn("DHFS001", admitted_ids)

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "dihydrofolate_reductase")
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
            self.assertIn(
                "rhea_reaction_or_participant_pattern",
                tier["mechanism_corroborator_axes_present"],
            )

    def test_floor_projection_and_deploy_context(self):
        audit = self._run()
        proj = audit["floor_projection"]["dihydrofolate_reductase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "nadph_dihydrofolate_reduction_pterin_protonation_context",
        )
        self.assertEqual(proj["combined_before"], 0)
        self.assertEqual(proj["admitted_this_run"], 2)
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
        self.assertTrue(g["dihydrofolate_reductase_handles_scope_admission_only"])
        self.assertTrue(g["ec_never_a_counted_corroborator"])
        self.assertTrue(g["folate_synthase_mthfr_thymidylate_synthase_side_ec_boundary_guard"])
        self.assertEqual(audit["fetch_failure_count"], 0)
