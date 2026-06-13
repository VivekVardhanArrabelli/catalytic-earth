"""Offline validation of glycoside hydrolase broadened-handle sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.glycoside_hydrolase_sourcing import (
    FAMILIES,
    build_glycoside_hydrolase_sourcing,
)

_ROWS = {
    "GH0001": (
        ["3.2.1.4"],
        ["Glycosidase"],
        "Endoglucanase",
        "cellulose + H2O = cellooligosaccharides",
        "Proton donor Glu nucleophile",
        "Active site",
    ),
    "GH0002": (
        ["3.2.1.23"],
        ["Glycosidase"],
        "Beta-galactosidase",
        "lactose + H2O = D-glucose + D-galactose",
        "Proton donor Glu",
        "Binding site",
    ),
    # Alternate name-lane supply: chitinase is already an accepted family-text
    # handle, but it is not named in the original source query.
    "GH0003": (
        ["3.2.1.14"],
        ["Hydrolase"],
        "Chitinase",
        "chitin + H2O = chitin oligosaccharides",
        "General acid/base Glu nucleophile",
        "Active site",
    ),
    # EC 3.2.1 + glycosidase text but no hydrolysis reaction or active-site handle: EC/keyword alone holds.
    "NX0001": (
        ["3.2.1.4"],
        ["Glycosidase"],
        "Endoglucanase-like",
        "cellulose binds substrate",
        "",
        "",
    ),
    # Multi-EC boundary row: transferase side signal must hold, not force the hydrolase label.
    "TR0001": (
        ["3.2.1.4", "2.4.1.1"],
        ["Glycosidase"],
        "Transglycosylase boundary",
        "cellulose + H2O = cellooligosaccharides",
        "Binding site",
        "Binding site",
    ),
    # Off-target row should be held by the glycoside hydrolase wrapper, not imported through this lane.
    "GT0001": (
        ["2.4.1.1"],
        ["Glycosyltransferase"],
        "Glycosyltransferase",
        "UDP-glucose + acceptor = UDP + glycosylated acceptor",
        "UDP-glucose binding",
        "Binding site",
    ),
    "TU0001": (
        ["3.2.1.4"],
        ["Glycosidase"],
        "Unreviewed endoglucanase",
        "cellulose + H2O = cellooligosaccharides",
        "Proton donor Glu nucleophile",
        "Active site",
    ),
}


def _search_record(accession):
    ec, _, protein_name, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": protein_name,
        "organism": f"Organism {accession}",
        "length": 330,
        "sequence": "M" + "A" * 329,
        "ec_numbers": ec,
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "unreviewed" if accession.startswith("TU") else "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _feature(feature_type, description):
    if not feature_type:
        return []
    return [
        {
            "feature_type": feature_type,
            "begin": 120,
            "end": 120,
            "description": description,
            "ligand_name": None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession):
    ec, keywords, protein_name, reaction, feature_description, feature_type = _ROWS[accession]
    active_features = _feature(feature_type, feature_description) if feature_type == "Active site" else []
    binding_features = _feature(feature_type, feature_description) if feature_type == "Binding site" else []
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": (
            "UniProtKB unreviewed (TrEMBL)"
            if accession.startswith("TU")
            else "UniProtKB reviewed (Swiss-Prot)"
        ),
        "protein_name": protein_name,
        "sequence_length": 330,
        "keywords": keywords,
        "active_site_features": active_features,
        "binding_site_features": binding_features,
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": [
            {
                "reaction": reaction,
                "ec_number": ec[0],
                "cross_references": [{"database": "Rhea", "id": f"RHEA:{accession}"}],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        ],
        "cofactor_comments": [],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query, size, max_pages=1):
    if "reviewed:false" in query:
        accessions = ["TU0001"]
    elif "protein_name:chitinase" in query:
        accessions = ["GH0003"]
    else:
        accessions = [a for a in sorted(_ROWS) if a not in {"GH0003", "TU0001"}]
    records = [_search_record(a) for a in accessions]
    return {
        "metadata": {"url": "test://uniprot", "query": query, "max_pages": max_pages},
        "records": records,
    }


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class GlycosideHydrolaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_glycoside_hydrolase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T01:40:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_glycoside_hydrolase(self):
        self.assertEqual(FAMILIES, ("glycoside_hydrolase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["disambiguation_hold_count"], 2)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 1)
        self.assertEqual(
            audit["counts"]["off_target_fingerprint_counts"],
            {"glycosyltransferase": 1},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"glycoside_hydrolase": 2},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "glycoside_hydrolase")
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

    def test_glycoside_hydrolase_axes_are_mechanism_not_ec(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:GH0001", "uniprot:GH0002"})
        axes = labels["uniprot:GH0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)

    def test_ec_only_and_side_ec_controls_do_not_enter_family(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertNotIn("uniprot:NX0001", admitted_ids)
        self.assertNotIn("uniprot:TR0001", admitted_ids)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["glycoside_hydrolase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "glycosidic_substrate_ordered_water_hydrolysis_context",
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

    def test_record_window_processes_slice_before_entry_fetch(self):
        audit = self._run(record_offset_per_lane=2, record_limit_per_lane=2)
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 2)
        self.assertEqual(audit["counts"]["record_offset_per_lane"], 2)
        self.assertEqual(audit["counts"]["record_limit_per_lane"], 2)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 0)
        self.assertEqual(audit["counts"]["disambiguation_hold_count"], 1)
        self.assertEqual(
            audit["counts"]["off_target_fingerprint_counts"],
            {"glycosyltransferase": 1},
        )
        lane = audit["lane_summaries"][0]
        self.assertEqual(lane["records_returned_by_query"], 5)
        self.assertEqual(lane["records_in_window_before_dedup"], 2)

    def test_query_pages_are_forwarded_when_requested(self):
        audit = self._run(query_pages_per_lane=2, record_limit_per_lane=1)
        self.assertEqual(audit["counts"]["query_pages_per_lane"], 2)
        self.assertEqual(audit["lane_summaries"][0]["records_returned_by_query"], 5)
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 1)

    def test_alternate_name_lane_is_optional_and_non_predictive(self):
        audit = self._run(include_alternate_name_lanes=True)
        self.assertEqual(audit["counts"]["lanes_queried"], 2)
        self.assertTrue(audit["counts"]["alternate_name_lanes_enabled"])
        self.assertTrue(audit["guardrails"]["alternate_name_source_lanes_enabled"])
        self.assertEqual(
            audit["lane_summaries"][0]["lane_id"],
            "glycoside_hydrolase_reviewed_chitinase_glucanase_name",
        )
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertIn("uniprot:GH0003", labels)
        self.assertEqual(labels["uniprot:GH0003"]["evidence"]["predictive_evidence"], [])

    def test_only_alternate_name_lane_skips_base_source_lane(self):
        audit = self._run(only_alternate_name_lanes=True)
        self.assertEqual(audit["counts"]["lanes_queried"], 1)
        self.assertFalse(audit["counts"]["alternate_name_lanes_enabled"])
        self.assertTrue(audit["counts"]["only_alternate_name_lanes_enabled"])
        self.assertTrue(audit["guardrails"]["only_alternate_name_source_lanes_enabled"])
        self.assertEqual(
            audit["lane_summaries"][0]["lane_id"],
            "glycoside_hydrolase_reviewed_chitinase_glucanase_name",
        )
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:GH0003"})
        self.assertEqual(labels["uniprot:GH0003"]["evidence"]["predictive_evidence"], [])

    def test_unreviewed_tier2_lane_requires_source_tier_2(self):
        with self.assertRaises(ValueError):
            self._run(only_unreviewed_tier2_lanes=True)

    def test_unreviewed_tier2_lane_is_three_axis_and_leakage_safe(self):
        audit = self._run(
            only_unreviewed_tier2_lanes=True,
            source_tier="source_tier_2",
        )
        self.assertEqual(audit["counts"]["lanes_queried"], 1)
        self.assertEqual(audit["counts"]["source_trust_tier"], "source_tier_2")
        self.assertTrue(audit["counts"]["only_unreviewed_tier2_lanes_enabled"])
        self.assertTrue(audit["guardrails"]["only_unreviewed_tier2_source_lanes_enabled"])
        self.assertTrue(
            audit["guardrails"]["source_tier_2_requires_three_independent_mechanism_axes"]
        )
        self.assertEqual(
            audit["lane_summaries"][0]["lane_id"],
            "glycoside_hydrolase_unreviewed_tier2_site_annotated",
        )
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"glycoside_hydrolase": 1},
        )
        label = audit["applied_labels"][0]
        self.assertEqual(label["entry_id"], "uniprot:TU0001")
        self.assertEqual(label["evidence"]["predictive_evidence"], [])
        tier = label["evidence"]["source_trust_tier"]
        self.assertEqual(tier["source_tier"], "source_tier_2")
        self.assertGreaterEqual(len(tier["mechanism_corroborator_axes_present"]), 3)
        self.assertNotIn("ec_scope_hint", tier["mechanism_corroborator_axes_present"])

    def test_guardrails_non_destructive(self):
        audit = self._run()
        g = audit["guardrails"]
        self.assertFalse(g["curated_registry_written"])
        self.assertTrue(g["frozen_current702_benchmark_preserved"])
        self.assertTrue(g["transferase_phosphorylase_lyase_side_ec_guard"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("sam_methyltransferase",))


if __name__ == "__main__":
    unittest.main()
