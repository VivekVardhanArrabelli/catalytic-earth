"""Offline validation of copper oxidoreductase broadened-handle sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.copper_oxidoreductase_sourcing import (
    FAMILIES,
    build_copper_oxidoreductase_sourcing,
)

_ROWS = {
    "CU0001": (
        ["1.10.3.2"],
        ["Copper", "Oxidoreductase"],
        ["Cu(2+)"],
        "4 hydroquinone + O2 = 4 benzosemiquinone + 2 H2O",
        "Binding site",
        "type-1 copper binding histidine",
    ),
    "CU0002": (
        ["1.4.3.21"],
        ["Copper", "Oxidoreductase", "TPQ"],
        ["Cu cation", "L-topaquinone residue"],
        "methylamine + O2 + H2O = formaldehyde + H2O2 + NH4(+)",
        "Active site",
        "topaquinone and copper amine oxidase active site",
    ),
    # EC + Copper keyword only: hold because EC/keyword alone is insufficient.
    "NX0001": (
        ["1.10.3.2"],
        ["Copper"],
        [],
        "",
        "",
        "",
    ),
    # Hydrolase and glycosyltransferase side EC rows are boundary rows.
    "HD0001": (
        ["1.10.3.2", "3.1.1.1"],
        ["Copper", "Oxidoreductase"],
        ["Cu(2+)"],
        "a donor + O2 = product + H2O",
        "Binding site",
        "copper binding",
    ),
    "GT0001": (
        ["1.10.3.2", "2.4.1.1"],
        ["Copper", "Oxidoreductase", "Glycosyltransferase"],
        ["Cu(2+)"],
        "a donor + O2 = product + H2O",
        "Binding site",
        "copper binding",
    ),
    # Heme/flavin/Mo boundary rows stay held even when the copper keyword is present.
    "HM0001": (
        ["1.10.3.2"],
        ["Copper", "Oxidoreductase"],
        ["heme b"],
        "a donor + O2 = product + H2O",
        "Binding site",
        "heme binding",
    ),
    "FV0001": (
        ["1.10.3.2"],
        ["Copper", "Oxidoreductase"],
        ["FAD"],
        "a donor + O2 = product + H2O",
        "Binding site",
        "FAD binding",
    ),
    "MO0001": (
        ["1.10.3.2"],
        ["Copper", "Oxidoreductase", "Molybdenum"],
        ["Mo-bis(molybdopterin guanine dinucleotide)"],
        "a donor + O2 = product + H2O",
        "Binding site",
        "molybdopterin binding",
    ),
}


def _search_record(accession):
    ec, _, _, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": f"Test copper enzyme {accession}",
        "organism": f"Organism {accession}",
        "length": 430,
        "sequence": "M" + "A" * 429,
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
            "begin": 210,
            "end": 210,
            "description": description,
            "ligand_name": description if feature_type != "Active site" else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession):
    ec, keywords, cofactors, reaction, feature_type, feature_description = _ROWS[accession]
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
        "sequence_length": 430,
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


def _fake_query_fetcher(query, size):
    records = [_search_record(a) for a in sorted(_ROWS)]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class CopperOxidoreductaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_copper_oxidoreductase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T03:20:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_copper_oxidoreductase(self):
        self.assertEqual(FAMILIES, ("copper_oxidoreductase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 8)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["disambiguation_hold_count"], 4)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 2)
        self.assertEqual(
            audit["counts"]["off_target_fingerprint_counts"],
            {"glycosyltransferase": 1, "molybdopterin_oxidoreductase": 1},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"copper_oxidoreductase": 2},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "copper_oxidoreductase")
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

    def test_copper_axes_are_mechanism_not_ec(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:CU0001", "uniprot:CU0002"})
        axes = labels["uniprot:CU0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)

    def test_ec_only_and_boundary_controls_do_not_enter_family(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        for accession in ("NX0001", "HD0001", "GT0001", "HM0001", "FV0001", "MO0001"):
            self.assertNotIn(f"uniprot:{accession}", admitted_ids)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["copper_oxidoreductase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "copper_redox_metal_center_context",
        )
        self.assertEqual(proj["combined_before"], 0)
        self.assertEqual(proj["admitted_this_run"], 2)
        self.assertFalse(proj["chemistry_confusable"])
        self.assertEqual(proj["cap_ceiling"], 250)
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
        self.assertTrue(g["heme_flavin_molybdopterin_hydrolase_glyco_boundary_guard"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_record_window_limits_entry_fetch_scope(self):
        audit = self._run(record_offset_per_lane=1, record_limit_per_lane=2)
        self.assertEqual(audit["counts"]["record_offset_per_lane"], 1)
        self.assertEqual(audit["counts"]["record_limit_per_lane"], 2)
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 2)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 1)
        self.assertEqual(
            [label["entry_id"] for label in audit["applied_labels"]],
            ["uniprot:CU0002"],
        )
        for lane in audit["lane_summaries"]:
            self.assertEqual(lane["record_offset_per_lane"], 1)
            self.assertEqual(lane["record_limit_per_lane"], 2)

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("molybdopterin_oxidoreductase",))


if __name__ == "__main__":
    unittest.main()
