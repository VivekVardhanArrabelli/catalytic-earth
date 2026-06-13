"""Offline validation of PfkB/ribokinase-family broadened-handle sourcing."""

from __future__ import annotations

import unittest

from catalytic_earth.pfkb_ribokinase_family_sourcing import (
    FAMILIES,
    build_pfkb_ribokinase_family_sourcing,
)

_ROWS = {
    "RB0001": (
        ["2.7.1.15"],
        "Ribokinase",
        "ATP + D-ribose = ADP + D-ribose 5-phosphate + H(+)",
        "Binding site",
        "ATP",
    ),
    "AD0001": (
        ["2.7.1.20"],
        "Adenosine kinase",
        "ATP + adenosine = ADP + AMP + H(+)",
        "Binding site",
        "ATP",
    ),
    "EC0001": (
        ["2.7.1.15"],
        "Ribokinase-like protein",
        "",
        "Binding site",
        "ATP",
    ),
    "PK0001": (
        ["2.7.1.15", "2.7.11.1"],
        "Ribokinase protein kinase boundary",
        "ATP + D-ribose = ADP + D-ribose 5-phosphate + H(+)",
        "Binding site",
        "ATP",
    ),
    "PF0001": (
        ["2.7.1.11"],
        "ATP-dependent 6-phosphofructokinase",
        "ATP + D-fructose 6-phosphate = ADP + D-fructose 1,6-bisphosphate + H(+)",
        "Binding site",
        "ATP",
    ),
    "AS0001": (
        ["2.7.1.1"],
        "Hexokinase",
        "ATP + D-glucose = ADP + D-glucose 6-phosphate + H(+)",
        "Binding site",
        "ATP",
    ),
    "GH0001": (
        ["2.7.1.36"],
        "Mevalonate kinase",
        "ATP + (R)-mevalonate = ADP + (R)-5-phosphomevalonate + H(+)",
        "Binding site",
        "ATP",
    ),
    "DK0001": (
        ["2.7.1.21"],
        "Thymidine kinase",
        "ATP + thymidine = ADP + dTMP + H(+)",
        "Binding site",
        "ATP",
    ),
    "ND0001": (
        ["2.7.4.6"],
        "Nucleoside diphosphate kinase",
        "ATP + nucleoside diphosphate = ADP + nucleoside triphosphate",
        "Active site",
        "Pros-phosphohistidine intermediate",
    ),
}


def _search_record(accession):
    ec, protein_name, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": protein_name,
        "organism": f"Organism {accession}",
        "length": 160,
        "sequence": "M" + "A" * 159,
        "ec_numbers": ec,
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _feature(feature_type, description):
    return [
        {
            "feature_type": feature_type,
            "begin": 118,
            "end": 118,
            "description": description,
            "ligand_name": description if feature_type != "Active site" else None,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession):
    ec, protein_name, reaction, feature_type, feature_description = _ROWS[accession]
    features = _feature(feature_type, feature_description)
    active_features = features if feature_type == "Active site" else []
    binding_features = features if feature_type == "Binding site" else []
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
        "sequence_length": 160,
        "keywords": ["Kinase", "Transferase"],
        "active_site_features": active_features,
        "binding_site_features": binding_features,
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": catalytic,
        "cofactor_comments": [],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query, size):
    records = [_search_record(accession) for accession in sorted(_ROWS)]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class PfkbRibokinaseFamilySourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_pfkb_ribokinase_family_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T11:45:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            cap_ceiling=150,
            **kwargs,
        )

    def test_family_is_pfkb_ribokinase_family(self):
        self.assertEqual(FAMILIES, ("pfkb_ribokinase_family",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 9)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 2)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 5)
        self.assertEqual(
            audit["counts"]["off_target_fingerprint_counts"],
            {
                "askha_sugar_acetate_kinase": 1,
                "deoxynucleoside_kinase": 1,
                "ghmp_small_molecule_kinase": 1,
                "nucleoside_diphosphate_kinase": 1,
                "pfka_phosphofructokinase": 1,
            },
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"pfkb_ribokinase_family": 2},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "pfkb_ribokinase_family")
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["review_status"], "automation_curated")
            self.assertTrue(label["entry_id"].startswith("uniprot:"))
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            tier = label["evidence"]["source_trust_tier"]
            self.assertEqual(tier["source_tier"], "source_tier_0")
            self.assertTrue(tier["meets_n_of_m"])
            self.assertNotIn("ec_scope_hint", tier["mechanism_corroborator_axes_present"])

    def test_axes_are_mechanism_not_ec(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:AD0001", "uniprot:RB0001"})
        axes = labels["uniprot:RB0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)


if __name__ == "__main__":
    unittest.main()
