"""Offline validation of cytochrome P450 broadened-handle sourcing."""

from __future__ import annotations

import json
import unittest

from catalytic_earth.cytochrome_p450_sourcing import (
    FAMILIES,
    build_cytochrome_p450_sourcing,
)

_ROWS = {
    # P450 keyword + heme + O2 reaction participant.
    "CP0001": (
        "1.14.14.1",
        ["Cytochrome P450", "Monooxygenase", "Oxidoreductase"],
        "RH + O2 + reduced [NADPH--hemoprotein reductase] = ROH + H2O + oxidized [NADPH--hemoprotein reductase]",
        "heme b",
    ),
    # Monooxygenase keyword + heme + O2 reaction participant, no P450 keyword.
    "CP0002": (
        "1.14.13.70",
        ["Monooxygenase"],
        "a substrate + O2 + NADPH + H(+) = a hydroxylated substrate + H2O + NADP(+)",
        "heme",
    ),
    # Heme peroxidase control: should not enter P450; it may match the existing heme
    # peroxidase fingerprint and therefore be held as off-target by the P450 runner.
    "PX0001": (
        "1.11.1.7",
        ["Peroxidase"],
        "2 phenolic donor + H2O2 = 2 phenoxy radical donor + 2 H2O",
        "heme b",
    ),
    # Flavin monooxygenase control: oxygenase but no heme.
    "FX0001": (
        "1.14.14.3",
        ["Monooxygenase"],
        "reduced flavin + O2 + substrate = oxidized flavin + hydroxylated substrate",
        "FAD",
    ),
    # EC 1.14 + heme but no P450/monooxygenase/O2 mechanism handle: EC alone must hold.
    "NX0001": (
        "1.14.99.1",
        ["Oxidoreductase"],
        "a donor + an acceptor = products",
        "heme",
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
        "length": 410,
        "sequence": "M" + "A" * 409,
        "ec_numbers": [ec],
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _entry_record(accession):
    ec, keywords, reaction, cofactor = _ROWS[accession]
    ligand_id = "CHEBI:60344" if "heme" in cofactor.lower() else "CHEBI:57692"
    binding_description = (
        "heme-thiolate proximal Cys ligand"
        if accession.startswith("CP")
        else "cofactor binding site"
    )
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "sequence_length": 410,
        "keywords": keywords,
        "active_site_features": [
            {
                "feature_type": "Active site",
                "begin": 130,
                "end": 130,
                "description": "oxygen activation network",
                "ligand_name": None,
                "ligand_id": None,
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
        ],
        "binding_site_features": [
            {
                "feature_type": "Binding site",
                "begin": 360,
                "end": 360,
                "description": binding_description,
                "ligand_name": cofactor,
                "ligand_id": ligand_id,
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
        ],
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
        "cofactor_comments": [
            {
                "cofactors": [
                    {
                        "name": cofactor,
                        "cross_reference": {"id": ligand_id},
                        "evidence": [{"evidence_code": "ECO:0000269"}],
                    }
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


class CytochromeP450SourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_cytochrome_p450_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-12T23:57:53Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_family_is_cytochrome_p450(self):
        self.assertEqual(FAMILIES, ("cytochrome_p450_monooxygenase",))

    def test_fetches_and_routes_target_family(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 5)
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 2)
        self.assertEqual(audit["counts"]["off_target_fingerprint_matches_held"], 2)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 1)

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"cytochrome_p450_monooxygenase": 2},
        )
        for label in audit["applied_labels"]:
            self.assertEqual(label["fingerprint_id"], "cytochrome_p450_monooxygenase")
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

    def test_p450_axes_are_mechanism_not_ec(self):
        audit = self._run()
        labels = {label["entry_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(labels), {"uniprot:CP0001", "uniprot:CP0002"})
        axes = labels["uniprot:CP0001"]["evidence"]["source_trust_tier"][
            "mechanism_corroborator_axes_present"
        ]
        self.assertIn("cofactor_or_cosubstrate", axes)
        self.assertIn("rhea_reaction_or_participant_pattern", axes)
        self.assertIn("domain_or_family_profile", axes)

    def test_non_peroxidase_and_no_heme_controls_do_not_enter_p450(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertNotIn("uniprot:PX0001", admitted_ids)
        self.assertNotIn("uniprot:FX0001", admitted_ids)
        self.assertNotIn("uniprot:NX0001", admitted_ids)
        self.assertEqual(
            audit["counts"]["off_target_fingerprint_counts"],
            {"flavin_monooxygenase": 1, "heme_peroxidase_oxidase": 1},
        )

    def test_sequence_provenance_and_floor_projection(self):
        audit = self._run()
        proj = audit["floor_projection"]["cytochrome_p450_monooxygenase"]
        self.assertEqual(
            proj["deploy_missing_active_site_context"],
            "heme_thiolate_oxygen_cosubstrate",
        )
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
        self.assertTrue(g["non_peroxidase_guard"])
        self.assertTrue(g["off_target_fingerprint_matches_held"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("sam_methyltransferase",))


if __name__ == "__main__":
    unittest.main()
