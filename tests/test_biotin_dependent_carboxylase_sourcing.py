"""Offline validation of biotin-dependent carboxylase broadened-handle sourcing."""

from __future__ import annotations

import unittest

from catalytic_earth.biotin_dependent_carboxylase_sourcing import (
    FAMILIES,
    build_biotin_dependent_carboxylase_sourcing,
)

_ROWS = {
    "BC0001": (
        ["6.4.1.2"],
        ["Biotin", "Ligase"],
        ["Biotin", "Mg(2+)"],
        "Acetyl-CoA carboxylase",
        "acetyl-CoA + ATP + hydrogencarbonate = malonyl-CoA + ADP + phosphate",
        "Binding site",
        "ATP",
    ),
    "BC0002": (
        ["6.3.4.14"],
        ["Biotin", "Ligase"],
        [],
        "Biotin carboxylase",
        "ATP + hydrogencarbonate + biotin = ADP + carboxybiotin + phosphate",
        "Modified residue",
        "N6-biotinyl-L-lysine",
    ),
    "BC0003": (
        ["6.4.1.3"],
        ["Biotin", "Ligase"],
        ["Biotin"],
        "Propionyl-CoA carboxylase",
        "propionyl-CoA + ATP + hydrogencarbonate = methylmalonyl-CoA + ADP + phosphate",
        "Binding site",
        "Biotin",
    ),
    # Alternate floor-closure supply: search-row scope lacks a biotin/name filter,
    # but the fetched entry still carries non-EC biotin mechanism evidence.
    "BC0004": (
        ["6.4.1.8"],
        ["Ligase"],
        ["Biotin"],
        "Acetophenone carboxylase",
        "acetophenone + ATP + hydrogencarbonate = acetophenone-carboxylate + ADP + phosphate",
        "Binding site",
        "Biotin",
    ),
    # EC + carboxylase text only: hold because EC/name without biotin evidence is insufficient.
    "NX0001": (
        ["6.4.1.2"],
        ["Ligase"],
        [],
        "Acetyl-CoA carboxylase-like protein",
        "acetyl-CoA + ATP + hydrogencarbonate = malonyl-CoA + ADP + phosphate",
        "",
        "",
    ),
    # Boundary rows.
    "KN0001": (
        ["6.4.1.2", "2.7.1.1"],
        ["Biotin", "Kinase"],
        ["Biotin"],
        "Biotin carboxylase kinase boundary",
        "ATP + hydrogencarbonate + biotin = ADP + carboxybiotin + phosphate",
        "Binding site",
        "Biotin",
    ),
    "HD0001": (
        ["6.4.1.2", "3.1.1.1"],
        ["Biotin", "Ligase"],
        ["Biotin"],
        "Biotin carboxylase hydrolase boundary",
        "ATP + hydrogencarbonate + biotin = ADP + carboxybiotin + phosphate",
        "Binding site",
        "Biotin",
    ),
    "PL0001": (
        ["6.4.1.2"],
        ["Biotin", "Ligase"],
        ["Biotin", "pyridoxal 5'-phosphate"],
        "PLP biotin carboxylase boundary",
        "ATP + hydrogencarbonate + biotin = ADP + carboxybiotin + phosphate",
        "Binding site",
        "Biotin",
    ),
    "BL0001": (
        ["6.3.4.15"],
        ["Biotin", "Ligase"],
        ["Biotin"],
        "Biotin--[acetyl-CoA-carboxylase] ligase",
        "biotin + L-lysyl-[protein] + ATP = N(6)-biotinyl-L-lysyl-[protein] + AMP + diphosphate + H(+)",
        "Binding site",
        "Biotin",
    ),
}


def _search_record(accession):
    ec, _, _, protein_name, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": protein_name,
        "organism": f"Organism {accession}",
        "length": 360,
        "sequence": "M" + "A" * 359,
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
            "begin": 91,
            "end": 91,
            "description": description,
            "ligand_name": description if feature_type != "Active site" else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession):
    ec, keywords, cofactors, protein_name, reaction, feature_type, feature_description = _ROWS[
        accession
    ]
    features = _feature(feature_type, feature_description)
    active_features = features if feature_type == "Active site" else []
    binding_features = features if feature_type == "Binding site" else []
    modified_features = features if feature_type == "Modified residue" else []
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
        "protein_name": protein_name,
        "sequence_length": 360,
        "keywords": keywords,
        "active_site_features": active_features,
        "binding_site_features": binding_features,
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": modified_features,
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
    if query == "(reviewed:true) AND (ec:6.4.1.*)":
        accessions = ["BC0004"]
    elif "rhea:" in query and "keyword:Biotin" not in query and "protein_name:biotin" not in query:
        accessions = ["BC0004"]
    elif "6.3.4" in query:
        accessions = ["BC0002", "BL0001"]
    else:
        accessions = [a for a in sorted(_ROWS) if a not in {"BC0002", "BC0004"}]
    records = [_search_record(a) for a in accessions]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class BiotinDependentCarboxylaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_biotin_dependent_carboxylase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T06:45:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            cap_ceiling=150,
            **kwargs,
        )

    def test_family_is_biotin_dependent_carboxylase(self):
        self.assertEqual(FAMILIES, ("biotin_dependent_carboxylase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 8)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 3)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 5)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 0)

    def test_rhea_first_floor_closure_lane_is_optional_and_non_predictive(self):
        audit = self._run(include_floor_closure_lanes=True)
        self.assertEqual(audit["counts"]["lanes_queried"], 3)
        self.assertTrue(audit["counts"]["rhea_first_floor_closure_lanes_enabled"])
        self.assertTrue(audit["guardrails"]["rhea_first_floor_closure_source_lane_enabled"])
        self.assertEqual(
            audit["lane_summaries"][0]["lane_id"],
            "biotin_carboxylase_reviewed_rhea_carboxylation_floor_closure",
        )
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 8)
        for label in audit["applied_labels"]:
            self.assertEqual(label["evidence"]["predictive_evidence"], [])

    def test_alternate_floor_closure_lanes_are_optional_and_still_mechanism_gated(self):
        audit = self._run(include_alternate_floor_closure_lanes=True)
        self.assertEqual(audit["counts"]["lanes_queried"], 5)
        self.assertTrue(audit["counts"]["alternate_floor_closure_lanes_enabled"])
        self.assertTrue(audit["guardrails"]["alternate_floor_closure_source_lanes_enabled"])
        self.assertEqual(
            audit["lane_summaries"][0]["lane_id"],
            "biotin_carboxylase_reviewed_rhea_carboxylation_no_name_filter",
        )
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertIn("uniprot:BC0004", admitted_ids)
        for label in audit["applied_labels"]:
            self.assertEqual(label["evidence"]["predictive_evidence"], [])

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"biotin_dependent_carboxylase": 3},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "biotin_dependent_carboxylase")
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

    def test_axes_are_mechanism_not_ec(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:BC0001", "uniprot:BC0002", "uniprot:BC0003"})
        axes = labels["uniprot:BC0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)
        self.assertNotIn("ec_scope_hint", axes)

    def test_boundary_controls_do_not_enter_family(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        for accession in ("NX0001", "KN0001", "HD0001", "PL0001", "BL0001"):
            self.assertNotIn(f"uniprot:{accession}", admitted_ids)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["biotin_dependent_carboxylase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "biotinyl_lysine_atp_hydrogencarbonate_context",
        )
        self.assertEqual(proj["cap_ceiling"], 150)
        self.assertTrue(proj["chemistry_confusable"])
        for label in audit["applied_labels"]:
            seq = label["evidence"]["sequence_provenance"]
            self.assertEqual(seq["sequence_length"], 360)
            self.assertEqual(seq["source"], "reviewed_uniprot")


if __name__ == "__main__":
    unittest.main()
