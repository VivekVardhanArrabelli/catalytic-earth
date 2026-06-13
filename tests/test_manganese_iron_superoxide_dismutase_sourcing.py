"""Offline validation of Mn/Fe superoxide dismutase broadened-handle sourcing."""

from __future__ import annotations

import unittest

from catalytic_earth.manganese_iron_superoxide_dismutase_sourcing import (
    FAMILIES,
    build_manganese_iron_superoxide_dismutase_sourcing,
)

_ROWS = {
    "FE0001": (
        ["1.15.1.1"],
        "Superoxide dismutase [Fe]",
        ["Superoxide dismutase", "Metal-binding"],
        "2 superoxide + 2 H(+) = H2O2 + O2",
        "Metal binding",
        "Iron",
    ),
    "MN0001": (
        ["1.15.1.1"],
        "Superoxide dismutase [Mn]",
        ["Superoxide dismutase", "Metal-binding"],
        "2 superoxide + 2 H(+) = H2O2 + O2",
        "Metal binding",
        "Manganese",
    ),
    "EC0001": (
        ["1.15.1.1"],
        "Superoxide dismutase [Mn]",
        ["Superoxide dismutase"],
        "",
        "Metal binding",
        "Manganese",
    ),
    "CU0001": (
        ["1.15.1.1"],
        "Superoxide dismutase [Cu-Zn]",
        ["Superoxide dismutase"],
        "2 superoxide + 2 H(+) = H2O2 + O2",
        "Metal binding",
        "Copper",
    ),
    "HE0001": (
        ["1.15.1.1"],
        "Peroxidase-like superoxide dismutase boundary",
        ["Superoxide dismutase"],
        "2 superoxide + 2 H(+) = H2O2 + O2",
        "Binding site",
        "heme b",
    ),
    "SR0001": (
        ["1.15.1.1"],
        "Superoxide reductase",
        ["Superoxide dismutase"],
        "2 superoxide + 2 H(+) = H2O2 + O2",
        "Metal binding",
        "Iron",
    ),
    "NS0001": (
        ["1.15.1.1"],
        "Superoxide dismutase [Mn]",
        ["Superoxide dismutase"],
        "2 superoxide + 2 H(+) = H2O2 + O2",
        "",
        "",
    ),
}


def _search_record(accession):
    ec, protein_name, _, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": protein_name,
        "organism": f"Organism {accession}",
        "length": 210,
        "sequence": "M" + accession[0] * 209,
        "ec_numbers": ec,
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _feature(feature_type, ligand):
    if not feature_type:
        return []
    return [
        {
            "feature_type": feature_type,
            "begin": 83,
            "end": 83,
            "description": ligand,
            "ligand_name": ligand,
            "ligand_id": None,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]


def _entry_record(accession):
    ec, protein_name, keywords, reaction, feature_type, ligand = _ROWS[accession]
    features = _feature(feature_type, ligand)
    metal_features = features if feature_type == "Metal binding" else []
    binding_features = features if feature_type == "Binding site" else []
    catalytic = []
    if reaction:
        catalytic.append(
            {
                "reaction": reaction,
                "ec_number": ec[0],
                "cross_references": [{"database": "Rhea", "id": "RHEA:20696"}],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        )
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "protein_name": protein_name,
        "sequence_length": 210,
        "keywords": keywords,
        "active_site_features": [],
        "binding_site_features": binding_features,
        "metal_binding_features": metal_features,
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": catalytic,
        "cofactor_comments": [{"name": ligand}] if ligand else [],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query, size):
    records = [_search_record(accession) for accession in sorted(_ROWS)]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class ManganeseIronSuperoxideDismutaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_manganese_iron_superoxide_dismutase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-13T15:30:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            cap_ceiling=250,
            **kwargs,
        )

    def test_family_is_mn_fe_sod(self):
        self.assertEqual(FAMILIES, ("manganese_iron_superoxide_dismutase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 7)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 0)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 5)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"manganese_iron_superoxide_dismutase": 2},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "manganese_iron_superoxide_dismutase")
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
        self.assertEqual(set(labels), {"uniprot:FE0001", "uniprot:MN0001"})
        axes = labels["uniprot:MN0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("active_site_motif_or_residue_role", axes)
        self.assertIn("domain_or_family_profile", axes)


if __name__ == "__main__":
    unittest.main()
