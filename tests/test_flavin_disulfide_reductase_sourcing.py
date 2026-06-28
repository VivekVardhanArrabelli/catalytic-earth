"""Offline validation of flavin-dependent disulfide-reductase sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.flavin_disulfide_reductase_sourcing import (
    FAMILIES,
    build_flavin_disulfide_reductase_sourcing,
)

# accession -> (ec, protein_name, keywords, reaction, feature_type, feature_description, has_fad)
_ROWS = {
    "GR0001": (
        ["1.8.1.7"],
        "Glutathione reductase",
        ["Oxidoreductase", "FAD", "NADP"],
        "2 glutathione + NADP(+) = glutathione disulfide + NADPH + H(+)",
        "Active site",
        "redox-active cysteine pair",
        True,
    ),
    "TRX0001": (
        ["1.8.1.9"],
        "Thioredoxin reductase",
        ["Oxidoreductase", "FAD"],
        "[thioredoxin]-dithiol + NADP(+) = [thioredoxin]-disulfide + NADPH + H(+)",
        "Binding site",
        "FAD binding site",
        True,
    ),
    "LPD0001": (
        ["1.8.1.4"],
        "Dihydrolipoyl dehydrogenase",
        ["Oxidoreductase", "FAD"],
        "(R)-dihydrolipoamide + NAD(+) = (R)-lipoamide + NADH + H(+)",
        "Active site",
        "redox-active disulfide",
        True,
    ),
    # Sulfite reductase (EC 1.8.1.2, FAD flavoprotein) reduces sulfite, NOT a disulfide, so the
    # disulfide-substrate reaction anchor is absent (and the name is boundary-guarded): it must NOT
    # route to flavin_disulfide_reductase. It is a flavoprotein in scope 1.8.1, so it routes
    # off-target to flavin_dehydrogenase_reductase.
    "SIR0001": (
        ["1.8.1.2"],
        "Sulfite reductase [NADPH] flavoprotein alpha-component",
        ["Oxidoreductase", "FAD"],
        "hydrogen sulfide + 3 NADP(+) + 3 H2O = sulfite + 3 NADPH + 3 H(+)",
        "Active site",
        "siroheme-binding site",
        True,
    ),
    # A disulfide-reductase reaction + name but NO annotated FAD cofactor: the FAD hard anchor is
    # absent, so the row is held (no flavin -> neither the disulfide nor the flavin rule fires).
    "NOFAD001": (
        ["1.8.1.7"],
        "Putative glutathione reductase",
        ["Oxidoreductase"],
        "2 glutathione + NADP(+) = glutathione disulfide + NADPH + H(+)",
        "",
        "",
        False,
    ),
    # NAD(P)H:quinone reductase (EC 1.6.5.2, FAD) reduces a quinone, not a disulfide: routes
    # off-target to flavin_dehydrogenase_reductase (unchanged behaviour).
    "QRED001": (
        ["1.6.5.2"],
        "NAD(P)H dehydrogenase [quinone]",
        ["Oxidoreductase", "FAD"],
        "a quinone + NADPH + H(+) = a quinol + NADP(+)",
        "Binding site",
        "FAD binding site",
        True,
    ),
}

_QUERY_ORDER = ("NOFAD001", "GR0001", "TRX0001", "LPD0001", "SIR0001", "QRED001")


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
            "begin": 44,
            "end": 44,
            "description": description,
            "ligand_name": description if feature_type != "Active site" else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession: str) -> dict:
    ec, _, keywords, reaction, feature_type, feature_description, has_fad = _ROWS[accession]
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
    cofactor_comments = []
    if has_fad:
        cofactor_comments.append(
            {
                "cofactors": [
                    {
                        "name": "FAD",
                        "cross_reference": {"database": "ChEBI", "id": "CHEBI:57692"},
                        "evidence": [{"evidence_code": "ECO:0000269"}],
                    }
                ]
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


class FlavinDisulfideReductaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_flavin_disulfide_reductase_sourcing(
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

    def test_family_is_flavin_disulfide_reductase(self):
        self.assertEqual(FAMILIES, ("flavin_disulfide_reductase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 6)
        # The three FAD disulfide reductases corroborate (glutathione / thioredoxin / lipoamide).
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 3)
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 3)
        # NOFAD001 (no FAD cofactor) is held; FAD is the hard anchor.
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 1)
        # Sulfite reductase and quinone reductase route off-target to flavin_dehydrogenase_reductase.
        self.assertGreaterEqual(audit["counts"]["off_target_fingerprint_matches_held"], 2)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"flavin_disulfide_reductase": 3},
        )

    def test_sulfite_reductase_not_pulled_into_family(self):
        # SIR0001 is an EC 1.8.1.2 FAD flavoprotein, but it reduces sulfite (no disulfide substrate)
        # and is boundary-guarded by name, so it must not be admitted to flavin_disulfide_reductase.
        audit = self._run()
        admitted_ids = {label["entry_id"].split(":", 1)[1] for label in audit["applied_labels"]}
        self.assertNotIn("SIR0001", admitted_ids)

    def test_missing_fad_cofactor_is_held(self):
        # NOFAD001 has the disulfide reaction + name but no annotated FAD; the FAD hard anchor is
        # absent so it must not be admitted (mechanism-not-name discipline).
        audit = self._run()
        admitted_ids = {label["entry_id"].split(":", 1)[1] for label in audit["applied_labels"]}
        self.assertNotIn("NOFAD001", admitted_ids)

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "flavin_disulfide_reductase")
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
            self.assertIn("cofactor_or_cosubstrate", tier["mechanism_corroborator_axes_present"])

    def test_floor_projection_and_deploy_context(self):
        audit = self._run()
        proj = audit["floor_projection"]["flavin_disulfide_reductase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "fad_redox_active_disulfide_nadph_disulfide_reduction_context",
        )
        self.assertEqual(proj["combined_before"], 0)
        self.assertEqual(proj["admitted_this_run"], 3)
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
        self.assertTrue(g["flavin_disulfide_reductase_handles_scope_admission_only"])
        self.assertTrue(g["ec_never_a_counted_corroborator"])
        self.assertTrue(g["sulfite_reductase_glutaredoxin_peroxidase_side_ec_boundary_guard"])
        self.assertEqual(audit["fetch_failure_count"], 0)
