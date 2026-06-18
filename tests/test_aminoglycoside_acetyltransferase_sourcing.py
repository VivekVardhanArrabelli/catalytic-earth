"""Offline validation of aminoglycoside acetyltransferase (AAC) sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.aminoglycoside_acetyltransferase_sourcing import (
    FAMILIES,
    build_aminoglycoside_acetyltransferase_sourcing,
)

_ROWS = {
    "AAC001": (
        ["2.3.1.82"],
        "Aminoglycoside N(6')-acetyltransferase",
        ["Antibiotic resistance", "Acetyltransferase"],
        [],
        "acetyl-CoA + kanamycin = CoA + N(6')-acetylkanamycin",
        "Active site",
        "GNAT acetyl-CoA binding general base of the aminoglycoside acetyltransferase",
    ),
    "AAC002": (
        ["2.3.1.81"],
        "Gentamicin 3-N-acetyltransferase",
        ["Acetyltransferase", "Antibiotic resistance"],
        [],
        "acetyl-CoA + gentamicin = CoA + 3-N-acetylgentamicin",
        "Binding site",
        "acetyl-CoA binding site in the aminoglycoside acetyltransferase GNAT fold",
    ),
    # AAC name only, no acetyl-CoA reaction corroboration: held.
    "EC0001": (
        ["2.3.1.81"],
        "Aminoglycoside acetyltransferase-like protein",
        ["Acetyltransferase"],
        [],
        "",
        "",
        "",
    ),
    # Generic CoA acyltransferase (no aminoglycoside acceptor): routes off-target to coa_acyltransferase.
    "COA001": (
        ["2.3.1.16"],
        "Acetyl-CoA C-acyltransferase",
        ["Acyltransferase"],
        [],
        "acetyl-CoA + an acyl-CoA = CoA + a 3-oxoacyl-CoA",
        "Active site",
        "thiolase acetyl-CoA acyltransferase active site",
    ),
    # Bifunctional acetyltransferase-phosphotransferase: held (both family boundaries trip).
    "BIF001": (
        ["2.3.1.81"],
        "Bifunctional aminoglycoside acetyltransferase-phosphotransferase",
        ["Antibiotic resistance"],
        [],
        "acetyl-CoA + gentamicin = CoA + N-acetylgentamicin",
        "Active site",
        "bifunctional resistance enzyme active site",
    ),
}

_QUERY_ORDER = ("EC0001", "AAC001", "AAC002", "COA001", "BIF001")


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
            "begin": 90,
            "end": 90,
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


class AminoglycosideAcetyltransferaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_aminoglycoside_acetyltransferase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-17T21:00:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_aminoglycoside_acetyltransferase(self):
        self.assertEqual(FAMILIES, ("aminoglycoside_acetyltransferase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 2)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 1)
        # The generic acetyl-CoA C-acyltransferase routes off-target (to coa_acyltransferase).
        self.assertGreaterEqual(audit["counts"]["off_target_fingerprint_matches_held"], 1)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"aminoglycoside_acetyltransferase": 2},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "aminoglycoside_acetyltransferase")
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

    def test_floor_projection_and_deploy_context(self):
        audit = self._run()
        proj = audit["floor_projection"]["aminoglycoside_acetyltransferase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "acetyl_coa_aminoglycoside_gnat_n_acetyl_transfer_context",
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
        self.assertTrue(g["aminoglycoside_acetyltransferase_handles_scope_admission_only"])
        self.assertTrue(g["ec_never_a_counted_corroborator"])
        self.assertTrue(g["coa_acyltransferase_aph_ant_metal_flavin_boundary_guard"])
        self.assertEqual(audit["fetch_failure_count"], 0)
