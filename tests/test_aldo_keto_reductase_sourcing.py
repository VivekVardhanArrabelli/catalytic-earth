"""Offline validation of aldo-keto reductase (AKR) sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.aldo_keto_reductase_sourcing import (
    FAMILIES,
    build_aldo_keto_reductase_sourcing,
)

_ROWS = {
    "AKR001": (
        ["1.1.1.21"],
        "Aldo-keto reductase family 1 member B1 (Aldose reductase)",
        ["NADP", "Oxidoreductase"],
        [],
        "D-glucose + NADPH + H(+) = D-sorbitol + NADP(+)",
        "Active site",
        "Tyr-Lys-His-Asp catalytic tetrad of the aldo-keto reductase",
    ),
    "AKR002": (
        ["1.1.1.21"],
        "Aldo-keto reductase",
        ["NADP", "Oxidoreductase"],
        [],
        "an aldehyde + NADPH + H(+) = a primary alcohol + NADP(+)",
        "Binding site",
        "NADP binding site in the aldo-keto reductase TIM barrel",
    ),
    # AKR name only, no NADP reaction corroboration: held.
    "EC0001": (
        ["1.1.1.21"],
        "Aldo-keto reductase-like protein",
        ["NADP"],
        [],
        "",
        "",
        "",
    ),
    # SDR boundary: SDR-named row must route off-target (to SDR), not AKR.
    "SDR001": (
        ["1.1.1.100"],
        "Short-chain dehydrogenase/reductase SDR",
        ["NAD", "NADP", "Oxidoreductase"],
        [],
        "secondary alcohol + NAD(+) = ketone + NADH + H(+)",
        "Active site",
        "Ser-Tyr-Lys catalytic tetrad in the SDR active site",
    ),
    # Flavin/oxidase boundary: AKR-named oxidase with FAD is held, not AKR.
    "FAD001": (
        ["1.1.1.21"],
        "Aldo-keto reductase-like oxidase",
        ["NADP", "Oxidase"],
        ["FAD"],
        "an aldehyde + NADPH + H(+) = a primary alcohol + NADP(+)",
        "Active site",
        "FAD-binding oxidase active site",
    ),
}

_QUERY_ORDER = ("EC0001", "AKR001", "AKR002", "SDR001", "FAD001")


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


class AldoKetoReductaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_aldo_keto_reductase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-17T20:30:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_aldo_keto_reductase(self):
        self.assertEqual(FAMILIES, ("aldo_keto_reductase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 2)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 1)
        # The SDR-named row routes off-target (to short_chain_dehydrogenase_reductase).
        self.assertGreaterEqual(audit["counts"]["off_target_fingerprint_matches_held"], 1)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"aldo_keto_reductase": 2},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "aldo_keto_reductase")
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
        proj = audit["floor_projection"]["aldo_keto_reductase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "nadp_akr_tyr_lys_his_asp_tim_barrel_hydride_transfer_context",
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
        self.assertTrue(g["aldo_keto_reductase_handles_scope_admission_only"])
        self.assertTrue(g["ec_never_a_counted_corroborator"])
        self.assertTrue(g["sdr_mdr_aldh_flavin_metal_redox_boundary_guard"])
        self.assertEqual(audit["fetch_failure_count"], 0)
