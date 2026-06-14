"""Offline validation of HAD-like phosphatase sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.had_like_phosphatase_sourcing import (
    FAMILIES,
    build_had_like_phosphatase_sourcing,
)

_ROWS = {
    "HP0001": (
        ["3.1.3.3"],
        "HAD-like phosphoserine phosphatase",
        ["Phosphatase"],
        ["magnesium"],
        "O-phospho-L-serine + H2O = L-serine + phosphate",
        "Active site",
        "Catalytic Asp nucleophile of the HAD family phosphatase",
    ),
    "HP0002": (
        ["3.1.3.18"],
        "Haloacid dehalogenase-like phosphoglycolate phosphatase",
        ["Phosphatase"],
        ["magnesium"],
        "2-phosphoglycolate + H2O = glycolate + phosphate",
        "Binding site",
        "Mg(2+) binding site in the HAD active site",
    ),
    # EC-only: hold because EC cannot be a counted corroborator.
    "EC0001": (
        ["3.1.3.3"],
        "Uncharacterized EC 3.1.3 enzyme",
        [],
        [],
        "",
        "",
        "",
    ),
    # Existing metal phosphomonoesterase boundary: routed off-target, not forced into HAD.
    "MP0001": (
        ["3.1.3.1"],
        "Alkaline phosphatase",
        ["Phosphatase", "Metal-binding"],
        ["zinc"],
        "phosphomonoester + H2O = alcohol + phosphate",
        "Binding site",
        "Zinc binding",
    ),
    # Phosphodiesterase/nuclease side-EC boundary: hold.
    "PD0001": (
        ["3.1.3.1", "3.1.4.1"],
        "HAD-like phosphodiesterase boundary enzyme",
        ["Phosphatase"],
        ["magnesium"],
        "phosphomonoester + H2O = alcohol + phosphate",
        "Binding site",
        "Mg(2+) binding site",
    ),
}

_QUERY_ORDER = ("EC0001", "HP0001", "HP0002", "MP0001", "PD0001")


def _sequence(accession: str) -> str:
    seed = (accession * 80)[:430]
    return "M" + "".join("A" if c.isdigit() else c for c in seed)


def _search_record(accession: str) -> dict:
    ec, name, _, _, _, _, _ = _ROWS[accession]
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
    }


def _feature(feature_type: str, description: str) -> list[dict]:
    if not feature_type:
        return []
    return [
        {
            "feature_type": feature_type,
            "begin": 140,
            "end": 140,
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
    records = [_search_record(a) for a in _QUERY_ORDER]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records[:size]}


def _fake_entry_fetcher(accession: str) -> dict:
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number: str, limit: int) -> dict:
    return {"metadata": {"url": "test://rhea"}, "records": []}


class HadLikePhosphataseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_had_like_phosphatase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-14T19:20:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_had_like_phosphatase(self):
        self.assertEqual(FAMILIES, ("had_like_phosphatase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 2)
        self.assertEqual(audit["counts"]["disambiguation_hold_count"], 1)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 2)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"had_like_phosphatase": 2},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "had_like_phosphatase")
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
            self.assertIn("domain_or_family_profile", tier["mechanism_corroborator_axes_present"])

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["had_like_phosphatase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "mg_aspartyl_phosphoenzyme_phosphomonoester_hydrolysis_context",
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
        self.assertTrue(g["protein_phosphatase_metal_phosphatase_pde_boundary_guard"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_record_window_limits_entry_fetch_scope(self):
        audit = self._run(record_offset_per_lane=1, record_limit_per_lane=2)
        self.assertEqual(audit["counts"]["record_offset_per_lane"], 1)
        self.assertEqual(audit["counts"]["record_limit_per_lane"], 2)
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 2)
        self.assertEqual(
            [label["entry_id"] for label in audit["applied_labels"]],
            ["uniprot:HP0001", "uniprot:HP0002"],
        )
        for lane in audit["lane_summaries"]:
            self.assertEqual(lane["record_offset_per_lane"], 1)
            self.assertEqual(lane["record_limit_per_lane"], 2)

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("metallophosphomonoesterase",))


if __name__ == "__main__":
    unittest.main()
