"""Offline validation of cysteine (thiol) protease sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.cysteine_protease_sourcing import (
    FAMILIES,
    build_cysteine_protease_sourcing,
)

# tuple = (ec, protein_name, keywords, reaction, feature_type, feature_description, metal_cofactor)
_ROWS = {
    "CYS001": (
        ["3.4.22.15"],
        "Cathepsin L1",
        ["Hydrolase", "Protease", "Thiol protease"],
        "",
        "Active site",
        "Nucleophile",
        None,
    ),
    "CYS002": (
        ["3.4.22.56"],
        "Caspase-3",
        ["Hydrolase", "Protease"],
        "",
        "Active site",
        "Nucleophile; for catalytic activity",
        None,
    ),
    # EC 3.4.22 with neither an active site nor a recognizable family handle: held.
    "EC0001": (
        ["3.4.22.15"],
        "Uncharacterized protein",
        ["Hydrolase"],
        "",
        "",
        "",
        None,
    ),
    # Protease inhibitor (cystatin) carrying the EC scope but no catalysis: boundary-held.
    "INH001": (
        ["3.4.22.15"],
        "Cysteine protease inhibitor cystatin-B",
        ["Protease inhibitor"],
        "",
        "Active site",
        "Nucleophile",
        None,
    ),
    # Serine protease (EC 3.4.21): must NOT route to cysteine_protease.
    "SER001": (
        ["3.4.21.4"],
        "Trypsin-1",
        ["Hydrolase", "Serine protease"],
        "",
        "Active site",
        "Charge relay system",
        None,
    ),
    # Metallopeptidase (EC 3.4.24, catalytic Zn): off-target to metallopeptidase.
    "ZN001": (
        ["3.4.24.27"],
        "Thermolysin",
        ["Hydrolase", "Metalloprotease"],
        "",
        "Active site",
        "Proton acceptor",
        "Zn(2+)",
    ),
}

_QUERY_ORDER = ("EC0001", "CYS001", "CYS002", "INH001", "SER001", "ZN001")


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
            "begin": 33,
            "end": 33,
            "description": description,
            "ligand_name": description if feature_type != "Active site" else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _metal_feature(metal: str) -> list[dict]:
    return [
        {
            "feature_type": "Binding site",
            "begin": 140,
            "end": 140,
            "description": "catalytic metal",
            "ligand_name": metal,
            "ligand_id": "ChEBI:CHEBI:29105",
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession: str) -> dict:
    ec, _, keywords, reaction, feature_type, feature_description, metal = _ROWS[accession]
    active_features = _feature(feature_type, feature_description) if feature_type == "Active site" else []
    binding_features = _feature(feature_type, feature_description) if feature_type == "Binding site" else []
    metal_features = _metal_feature(metal) if metal else []
    cofactor_comments = [{"cofactors": [{"name": metal, "cross_reference": {"id": "CHEBI:29105"}}]}] if metal else []
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
        "metal_binding_features": metal_features,
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": catalytic,
        "cofactor_comments": cofactor_comments,
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query: str, size: int) -> dict:
    records = [_search_record(a) for a in _QUERY_ORDER]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records[:size]}


def _fake_entry_fetcher(accession: str) -> dict:
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number: str, limit: int) -> dict:
    return {"metadata": {"url": "test://rhea"}, "records": []}


class CysteineProteaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_cysteine_protease_sourcing(
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

    def test_family_is_cysteine_protease(self):
        self.assertEqual(FAMILIES, ("cysteine_protease",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 6)
        # Only the two catalytic-Cys cysteine proteases corroborate.
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 2)
        # EC0001 (no active site / no family) and INH001 (inhibitor) are held.
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 2)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"cysteine_protease": 2},
        )

    def test_serine_and_metallo_proteases_not_admitted(self):
        audit = self._run()
        admitted_ids = {label["entry_id"].split(":", 1)[1] for label in audit["applied_labels"]}
        self.assertNotIn("SER001", admitted_ids)  # serine protease (3.4.21)
        self.assertNotIn("ZN001", admitted_ids)  # metallopeptidase (3.4.24)
        self.assertNotIn("INH001", admitted_ids)  # protease inhibitor

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "cysteine_protease")
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
            # The catalytic active site is the hard mechanism anchor for the cofactor-free protease.
            self.assertIn(
                "active_site_motif_or_residue_role",
                tier["mechanism_corroborator_axes_present"],
            )

    def test_floor_projection_and_deploy_context(self):
        audit = self._run()
        proj = audit["floor_projection"]["cysteine_protease"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "cys_his_thiol_protease_peptide_bond_hydrolysis_context",
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
        self.assertTrue(g["cysteine_protease_handles_scope_admission_only"])
        self.assertTrue(g["ec_never_a_counted_corroborator"])
        self.assertTrue(g["serine_aspartic_metallo_protease_inhibitor_boundary_guard"])
        self.assertEqual(audit["fetch_failure_count"], 0)
