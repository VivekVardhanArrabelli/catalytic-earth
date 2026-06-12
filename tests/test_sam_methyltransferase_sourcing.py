"""Offline validation of SAM methyltransferase broadened-handle sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.sam_methyltransferase_sourcing import (
    FAMILIES,
    build_sam_methyltransferase_sourcing,
)

_ROWS = {
    # SAM/SAH read from Rhea participant text plus Methyltransferase keyword.
    "SM0001": (
        "2.1.1.6",
        ["Methyltransferase", "Transferase"],
        "S-adenosyl-L-methionine + catechol = S-adenosyl-L-homocysteine + guaiacol + H(+)",
        False,
    ),
    # Keyword-only admission path: EC scopes the lane, keyword is the mechanism handle.
    "SM0002": (
        "2.1.1.37",
        ["Methyltransferase"],
        "a substrate + a methyl donor = a methylated product",
        False,
    ),
    # EC 2.1.1 but no SAM/SAH participant or methyltransferase keyword -> held.
    "NX0001": (
        "2.1.1.6",
        ["Transferase"],
        "a substrate + a folate methyl donor = a methylated product",
        False,
    ),
    # Fe-S + SAM row should not be imported as SAM methyltransferase. The existing
    # radical-SAM rule may identify it off-target, and this runner holds off-target matches.
    "RX0001": (
        "2.1.1.201",
        ["Methyltransferase", "S-adenosyl-L-methionine"],
        "S-adenosyl-L-methionine + a substrate = 5'-deoxyadenosine + a methylated product",
        True,
    ),
}


def _search_record(accession):
    ec, _, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": f"Test enzyme {accession}",
        "organism": f"Organism {accession}",
        "length": 320,
        "sequence": "M" + "A" * 319,
        "ec_numbers": [ec],
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _entry_record(accession):
    ec, keywords, reaction, fe_s = _ROWS[accession]
    if fe_s:
        ligand_name = "[4Fe-4S] cluster"
        ligand_id = "CHEBI:49883"
    elif accession == "SM0001":
        ligand_name = "S-adenosyl-L-methionine"
        ligand_id = "CHEBI:59789"
    else:
        ligand_name = None
        ligand_id = None
    binding_features = [
        {
            "feature_type": "Binding site",
            "begin": 20,
            "end": 25,
            "description": "SAM/SAH donor pocket",
            "ligand_name": ligand_name,
            "ligand_id": ligand_id,
            "evidence": [{"evidence_code": "ECO:0000269"}],
            "cross_references": [],
        }
    ]
    cofactor_comments = []
    if fe_s:
        cofactor_comments = [
            {
                "cofactors": [
                    {
                        "name": "S-adenosyl-L-methionine",
                        "cross_reference": {"id": "CHEBI:59789"},
                        "evidence": [{"evidence_code": "ECO:0000269"}],
                    }
                ]
            }
        ]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "sequence_length": 320,
        "keywords": keywords,
        "active_site_features": [
            {
                "feature_type": "Active site",
                "begin": 120,
                "end": 120,
                "description": "",
                "ligand_name": None,
                "ligand_id": None,
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
        ],
        "binding_site_features": binding_features,
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": [
            {
                "reaction": reaction,
                "ec_number": ec,
                "cross_references": [{"database": "Rhea", "id": f"RHEA:{accession}"}],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        ],
        "cofactor_comments": cofactor_comments,
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query, size):
    records = [_search_record(a) for a in sorted(_ROWS)]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class SamMethyltransferaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_sam_methyltransferase_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-12T23:09:11Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_sam_methyltransferase(self):
        self.assertEqual(FAMILIES, ("sam_methyltransferase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 4)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 1)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 1)

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"], {"sam_methyltransferase": 2}
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "sam_methyltransferase")
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

    def test_sam_sah_reaction_and_keyword_axes_admit(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:SM0001", "uniprot:SM0002"})
        axes_1 = labels["uniprot:SM0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("rhea_reaction_or_participant_pattern", axes_1)
        axes_2 = labels["uniprot:SM0002"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("domain_or_family_profile", axes_2)

    def test_no_fe_s_guard_holds_radical_sam_off_target(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertNotIn("uniprot:RX0001", admitted_ids)
        self.assertEqual(
            audit["counts"]["off_target_fingerprint_counts"], {"radical_sam_enzyme": 1}
        )

    def test_controls_without_mechanism_corroboration_held(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertNotIn("uniprot:NX0001", admitted_ids)

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["sam_methyltransferase"]
        self.assertEqual(proj["deploy_missing_active_site_context"], "sam_sah_methyl_donor")
        self.assertEqual(proj["combined_before"], 0)
        self.assertEqual(proj["admitted_this_run"], 2)
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
        self.assertTrue(g["no_fe_s_radical_sam_guard"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("glycosyltransferase",))


if __name__ == "__main__":
    unittest.main()
