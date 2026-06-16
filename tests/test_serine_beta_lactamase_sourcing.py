"""Offline validation of serine beta-lactamase sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.serine_beta_lactamase_sourcing import (
    FAMILIES,
    build_serine_beta_lactamase_sourcing,
)

_ROWS = {
    "SBL001": (
        ["3.5.2.6"],
        "Class A beta-lactamase",
        ["Beta-lactamase", "Hydrolase", "Antibiotic resistance"],
        [],
        "H2O + a beta-lactam = an opened beta-lactam carboxylate",
        "Active site",
        "Catalytic serine nucleophile in the class A beta-lactamase active site",
    ),
    "SBL002": (
        ["3.5.2.6"],
        "Class C beta-lactamase",
        ["Beta-lactamase", "Hydrolase"],
        [],
        "H2O + cephalosporin = cephalosporoate",
        "Binding site",
        "Ser/Lys/Glu beta-lactamase substrate-binding active-site context",
    ),
    # EC/name only: hold because EC/name cannot be counted corroborators alone.
    "EC0001": (
        ["3.5.2.6"],
        "Beta-lactamase-like protein",
        ["Hydrolase"],
        [],
        "",
        "",
        "",
    ),
    # Zinc/metallo beta-lactamase boundary: not a serine beta-lactamase.
    "MBL001": (
        ["3.5.2.7"],
        "Metallo-beta-lactamase",
        ["Beta-lactamase", "Metal-binding", "Hydrolase"],
        ["Zn(2+)"],
        "H2O + a beta-lactam = an opened beta-lactam carboxylate",
        "Metal binding",
        "Zinc-binding metallo-beta-lactamase active site",
    ),
    # PBP/DD-peptidase boundary: hold even with beta-lactam-like text.
    "PBP001": (
        ["3.4.16.4"],
        "Penicillin-binding protein transpeptidase",
        ["Cell wall biogenesis/degradation"],
        [],
        "peptidoglycan D-alanyl-D-alanine hydrolysis",
        "Active site",
        "Catalytic serine in a DD-peptidase transpeptidase active site",
    ),
    "TSBL001": (
        ["3.5.2.6"],
        "Class D beta-lactamase",
        ["Beta-lactamase", "Hydrolase", "Antibiotic resistance"],
        [],
        "H2O + imipenem = opened beta-lactam product",
        "Active site",
        "Carbamylated lysine and serine beta-lactamase active-site context",
    ),
}

_QUERY_ORDER = ("EC0001", "SBL001", "SBL002", "MBL001", "PBP001")


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
            "begin": 70,
            "end": 70,
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
    metal_features = _feature(feature_type, feature_description) if feature_type == "Metal binding" else []
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
        "metal_binding_features": metal_features,
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
    order = ("TSBL001",) if "reviewed:false" in query else _QUERY_ORDER
    records = [_search_record(a) for a in order]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records[:size]}


def _fake_entry_fetcher(accession: str) -> dict:
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number: str, limit: int) -> dict:
    return {"metadata": {"url": "test://rhea"}, "records": []}


class SerineBetaLactamaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_serine_beta_lactamase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-16T00:30:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_serine_beta_lactamase(self):
        self.assertEqual(FAMILIES, ("serine_beta_lactamase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 2)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 2)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"serine_beta_lactamase": 2},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "serine_beta_lactamase")
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["review_status"], "automation_curated")
            self.assertTrue(label["entry_id"].startswith("uniprot:"))
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            for excluded in ("ec_label", "protein_name", "uniprot_prose", "target_family_lane"):
                self.assertIn(excluded, label["evidence"]["excluded_context"])
            tier = label["evidence"]["source_trust_tier"]
            self.assertEqual(tier["source_tier"], "source_tier_0")
            self.assertTrue(tier["meets_n_of_m"])
            axes = set(tier["mechanism_corroborator_axes_present"])
            self.assertNotIn("ec_scope_hint", axes)
            self.assertIn("domain_or_family_profile", axes)
            self.assertIn("rhea_reaction_or_participant_pattern", axes)
            self.assertIn("active_site_motif_or_residue_role", axes)

    def test_tier2_requires_three_non_ec_axes(self):
        with self.assertRaises(ValueError):
            self._run(only_unreviewed_tier2_lanes=True)

        audit = self._run(only_unreviewed_tier2_lanes=True, source_tier="source_tier_2")
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 1)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 1)
        label = audit["applied_labels"][0]
        tier = label["evidence"]["source_trust_tier"]
        self.assertEqual(tier["source_tier"], "source_tier_2")
        self.assertGreaterEqual(len(tier["mechanism_corroborator_axes_present"]), 3)
        self.assertEqual(label["evidence"]["predictive_evidence"], [])

    def test_boundary_rows_do_not_become_sbl(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertEqual(admitted_ids, {"uniprot:SBL001", "uniprot:SBL002"})
        reasons = audit["counts"]["disambiguation_hold_reason_counts"]
        self.assertGreaterEqual(reasons.get("no_mechanism_corroboration", 0), 2)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["serine_beta_lactamase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "ser_lys_glu_beta_lactam_acyl_enzyme_hydrolysis_context",
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
        self.assertTrue(g["metallo_pbp_dd_peptidase_boundary_guard"])
        self.assertTrue(g["novelty_gated_against_both_registries"])


if __name__ == "__main__":
    unittest.main()
