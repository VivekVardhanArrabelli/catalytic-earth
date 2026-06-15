"""Offline validation of metal-independent phosphodiesterase sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.metal_independent_phosphodiesterase_sourcing import (
    FAMILIES,
    build_metal_independent_phosphodiesterase_sourcing,
)

_ROWS = {
    "PDE001": (
        ["3.1.4.17"],
        "Cyclic nucleotide phosphodiesterase",
        ["Hydrolase"],
        [],
        "3',5'-cyclic AMP + H2O = AMP + H(+)",
        "Active site",
        "Catalytic histidine general acid/base in the phosphodiesterase active site",
    ),
    "PDE002": (
        ["3.1.4.17"],
        "cAMP phosphodiesterase",
        ["Hydrolase"],
        [],
        "3',5'-cyclic GMP + H2O = GMP + H(+)",
        "Binding site",
        "Cyclic nucleotide substrate binding site in the phosphodiesterase pocket",
    ),
    # EC/name only: hold because EC/name cannot be counted corroborators alone.
    "EC0001": (
        ["3.1.4.17"],
        "Cyclic nucleotide phosphodiesterase-like protein",
        ["Hydrolase"],
        [],
        "",
        "",
        "",
    ),
    # Metal-dependent phosphodiesterase boundary: off-target, not forced into this split.
    "MET0001": (
        ["3.1.4.1"],
        "Metal-dependent phosphodiesterase nuclease",
        ["Hydrolase", "Metal-binding"],
        ["Mg(2+)"],
        "3',5'-cyclic AMP + H2O = AMP + H(+)",
        "Binding site",
        "Magnesium metal-binding phosphodiesterase active site",
    ),
    # Phosphomonoesterase boundary: held outside the phosphodiesterase lane.
    "PHOS0001": (
        ["3.1.3.1"],
        "Cyclic nucleotide phosphatase",
        ["Hydrolase"],
        [],
        "phosphomonoester + H2O = alcohol + phosphate",
        "Active site",
        "Catalytic phosphatase active site",
    ),
    "TPDE001": (
        ["3.1.4.17"],
        "Cyclic nucleotide phosphodiesterase",
        ["Hydrolase"],
        [],
        "3',5'-cyclic AMP + H2O = AMP + H(+)",
        "Active site",
        "Catalytic histidine general acid/base in the phosphodiesterase active site",
    ),
}

_QUERY_ORDER = ("EC0001", "PDE001", "PDE002", "MET0001", "PHOS0001")


def _sequence(accession: str) -> str:
    seed = (accession * 80)[:430]
    return "M" + "".join("A" if c.isdigit() else c for c in seed)


def _search_record(accession: str) -> dict:
    ec, name, keywords, _, _, _, _ = _ROWS[accession]
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
        "reviewed": "unreviewed" if accession.startswith("T") else "reviewed",
        "evidence_level": "protein_cross_reference",
        "keywords": keywords,
    }


def _feature(feature_type: str, description: str) -> list[dict]:
    if not feature_type:
        return []
    return [
        {
            "feature_type": feature_type,
            "begin": 88,
            "end": 88,
            "description": description,
            "ligand_name": description if feature_type != "Active site" else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession: str) -> dict:
    ec, _, keywords, cofactors, reaction, feature_type, feature_description = _ROWS[accession]
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
        "entry_type": (
            "UniProtKB unreviewed (TrEMBL)"
            if accession.startswith("T")
            else "UniProtKB reviewed (Swiss-Prot)"
        ),
        "sequence_length": len(_sequence(accession)),
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


def _fake_query_fetcher(query: str, size: int) -> dict:
    order = ("TPDE001",) if "reviewed:false" in query else _QUERY_ORDER
    records = [_search_record(a) for a in order]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records[:size]}


def _fake_entry_fetcher(accession: str) -> dict:
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number: str, limit: int) -> dict:
    return {"metadata": {"url": "test://rhea"}, "records": []}


class MetalIndependentPhosphodiesteraseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_metal_independent_phosphodiesterase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-15T18:45:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_metal_independent_phosphodiesterase(self):
        self.assertEqual(FAMILIES, ("metal_independent_phosphodiesterase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 2)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 1)
        self.assertGreaterEqual(audit["counts"]["off_target_fingerprint_matches_held"], 1)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"metal_independent_phosphodiesterase": 2},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "metal_independent_phosphodiesterase")
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
            self.assertIn("domain_or_family_profile", tier["mechanism_corroborator_axes_present"])

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["metal_independent_phosphodiesterase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "metal_independent_phosphodiester_hydrolysis_context",
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
        self.assertTrue(g["metal_independent_pde_handles_scope_admission_only"])
        self.assertTrue(g["metal_absence_is_boundary_filter_not_counted_evidence"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_record_window_limits_entry_fetch_scope(self):
        audit = self._run(record_offset_per_lane=1, record_limit_per_lane=2)
        self.assertEqual(audit["counts"]["record_offset_per_lane"], 1)
        self.assertEqual(audit["counts"]["record_limit_per_lane"], 2)
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 2)
        self.assertEqual(
            [label["entry_id"] for label in audit["applied_labels"]],
            ["uniprot:PDE001", "uniprot:PDE002"],
        )
        for lane in audit["lane_summaries"]:
            self.assertEqual(lane["record_offset_per_lane"], 1)
            self.assertEqual(lane["record_limit_per_lane"], 2)

    def test_lane_filter_limits_query_surface(self):
        audit = self._run(lane_ids=("metal_independent_pde_hydrolase_non_metal",))
        self.assertEqual(audit["counts"]["lanes_queried"], 1)
        self.assertEqual(
            audit["counts"]["lane_ids"],
            ["metal_independent_pde_hydrolase_non_metal"],
        )

        with self.assertRaises(ValueError):
            self._run(lane_ids=("not_a_lane",))

    def test_unreviewed_tier2_lane_requires_source_tier_2(self):
        with self.assertRaises(ValueError):
            self._run(only_unreviewed_tier2_lanes=True)

    def test_unreviewed_tier2_lane_is_three_axis_and_leakage_safe(self):
        audit = self._run(
            only_unreviewed_tier2_lanes=True,
            source_tier="source_tier_2",
        )
        self.assertEqual(audit["counts"]["lanes_queried"], 2)
        self.assertEqual(audit["counts"]["source_trust_tier"], "source_tier_2")
        self.assertTrue(audit["counts"]["only_unreviewed_tier2_lanes_enabled"])
        self.assertTrue(audit["guardrails"]["only_unreviewed_tier2_source_lanes_enabled"])
        self.assertTrue(
            audit["guardrails"]["source_tier_2_requires_three_independent_mechanism_axes"]
        )
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"metal_independent_phosphodiesterase": 1},
        )
        label = audit["applied_labels"][0]
        self.assertEqual(label["entry_id"], "uniprot:TPDE001")
        self.assertEqual(label["evidence"]["predictive_evidence"], [])
        tier = label["evidence"]["source_trust_tier"]
        self.assertEqual(tier["source_tier"], "source_tier_2")
        self.assertGreaterEqual(len(tier["mechanism_corroborator_axes_present"]), 3)
        self.assertNotIn("ec_scope_hint", tier["mechanism_corroborator_axes_present"])

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("glycoside_hydrolase",))


if __name__ == "__main__":
    unittest.main()
