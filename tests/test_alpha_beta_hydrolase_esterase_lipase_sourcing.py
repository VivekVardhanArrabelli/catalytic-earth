"""Offline validation of alpha/beta hydrolase esterase/lipase sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.alpha_beta_hydrolase_esterase_lipase_sourcing import (
    FAMILIES,
    build_alpha_beta_hydrolase_esterase_lipase_sourcing,
)

_ROWS = {
    "ABH001": (
        ["3.1.1.1"],
        "Alpha/beta hydrolase esterase",
        ["Esterase"],
        "a carboxylic ester + H2O = an alcohol + a carboxylate",
        [
            "Catalytic serine nucleophile of an alpha/beta hydrolase esterase",
            "Catalytic histidine of the Ser-His-Asp triad",
            "Catalytic aspartate acid of the Ser-His-Asp triad",
        ],
    ),
    "ABH002": (
        ["3.1.1.3"],
        "Triacylglycerol lipase alpha/beta hydrolase",
        ["Lipase"],
        "triacylglycerol + H2O = diacylglycerol + a fatty acid",
        [
            "Catalytic serine nucleophile",
            "Catalytic histidine base",
            "Catalytic glutamate acid of the Ser-His-Glu triad",
        ],
    ),
    # EC/name only: hold because EC/name cannot be counted corroborators alone.
    "EC0001": (
        ["3.1.1.1"],
        "Carboxylesterase-like protein",
        ["Esterase"],
        "",
        [],
    ),
    # Glycoside hydrolase boundary: off-target, not forced into the esterase split.
    "GH0001": (
        ["3.2.1.4"],
        "Glycoside hydrolase esterase boundary",
        ["Glycosidase"],
        "a glycoside + H2O = a sugar + an alcohol",
        ["Catalytic glutamate acid/base"],
    ),
    # Protease/amidase side-EC row: held.
    "PR0001": (
        ["3.1.1.1", "3.4.21.1"],
        "Serine protease esterase boundary",
        ["Esterase"],
        "a carboxylic ester + H2O = an alcohol + a carboxylate",
        [
            "Catalytic serine nucleophile",
            "Catalytic histidine base",
            "Catalytic aspartate acid",
        ],
    ),
}

_QUERY_ORDER = ("EC0001", "ABH001", "ABH002", "GH0001", "PR0001")


def _sequence(accession: str) -> str:
    seed = (accession * 80)[:430]
    return "M" + "".join("A" if c.isdigit() else c for c in seed)


def _search_record(accession: str) -> dict:
    ec, name, keywords, _, _ = _ROWS[accession]
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


def _active_features(descriptions: list[str]) -> list[dict]:
    features = []
    for i, description in enumerate(descriptions, start=101):
        features.append(
            {
                "feature_type": "Active site",
                "begin": i,
                "end": i,
                "description": description,
                "ligand_name": None,
                "ligand_id": None,
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
        )
    return features


def _entry_record(accession: str) -> dict:
    ec, _, keywords, reaction, feature_descriptions = _ROWS[accession]
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
        "active_site_features": _active_features(feature_descriptions),
        "binding_site_features": [],
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


class AlphaBetaHydrolaseEsteraseLipaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_alpha_beta_hydrolase_esterase_lipase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-14T21:20:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_alpha_beta_hydrolase_esterase_lipase(self):
        self.assertEqual(FAMILIES, ("alpha_beta_hydrolase_esterase_lipase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 2)
        self.assertEqual(audit["counts"]["disambiguation_hold_count"], 3)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 0)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"alpha_beta_hydrolase_esterase_lipase": 2},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "alpha_beta_hydrolase_esterase_lipase")
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
            self.assertIn(
                "active_site_motif_or_residue_role",
                tier["mechanism_corroborator_axes_present"],
            )
            self.assertIn(
                "rhea_reaction_or_participant_pattern",
                tier["mechanism_corroborator_axes_present"],
            )

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["alpha_beta_hydrolase_esterase_lipase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "ser_his_acid_ester_hydrolysis_context",
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
        self.assertTrue(g["protease_amidase_glycoside_metal_hydrolase_boundary_guard"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_record_window_limits_entry_fetch_scope(self):
        audit = self._run(record_offset_per_lane=1, record_limit_per_lane=2)
        self.assertEqual(audit["counts"]["record_offset_per_lane"], 1)
        self.assertEqual(audit["counts"]["record_limit_per_lane"], 2)
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 2)
        self.assertEqual(
            [label["entry_id"] for label in audit["applied_labels"]],
            ["uniprot:ABH001", "uniprot:ABH002"],
        )
        for lane in audit["lane_summaries"]:
            self.assertEqual(lane["record_offset_per_lane"], 1)
            self.assertEqual(lane["record_limit_per_lane"], 2)

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("ser_his_acid_hydrolase",))


if __name__ == "__main__":
    unittest.main()
