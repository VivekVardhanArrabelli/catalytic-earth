"""Offline validation of the NAD(P)-dehydrogenase + glycosyltransferase sourcing runner.

No network: the UniProt/Rhea fetchers are injected with synthetic payloads shaped exactly
like `adapters.normalize_uniprot_tsv` / `normalize_uniprot_entry_json` output (incl. the new
`keywords` field), so the full chain (fetch -> broadened mechanism-corroborator/EC
disambiguation -> novelty gate -> per-family cap guard -> preview) is exercised end to end and
the routing / leakage / trust-tier guardrails are asserted.
"""

from __future__ import annotations

import json
import unittest

from catalytic_earth.nad_glycosyltransferase_subfamily_sourcing import (
    CONFUSABLE_FAMILIES,
    FAMILIES,
    build_nad_glycosyltransferase_subfamily_sourcing,
)

# accession -> (EC, keywords, reaction text). Genuine NAD(P) dehydrogenase + glycosyltransferase
# rows, plus controls: an EC 1.1.1 row with NO NAD cosubstrate (held), and an EC 2.4 row with
# neither a sugar-nucleotide donor nor the keyword (held).
_ROWS = {
    # NAD(P) cosubstrate read from BOTH the Rhea reaction participant and the NAD keyword.
    "ND0001": ("1.1.1.1", ["NAD", "Oxidoreductase"], "an alcohol + NAD(+) = an aldehyde + NADH + H(+)"),
    # NADP read only from the reaction participant (no nicotinamide keyword) -- cosubstrate path.
    "ND0002": ("1.1.1.21", ["Oxidoreductase"], "D-glucose + NADP(+) = D-glucono-1,5-lactone + NADPH"),
    # Glycosyltransferase: sugar-nucleotide donor (Rhea) + Glycosyltransferase keyword.
    "GT0001": (
        "2.4.1.1",
        ["Glycosyltransferase", "Transferase"],
        "UDP-alpha-D-glucose + phosphate = alpha-D-glucose 1-phosphate + UDP",
    ),
    # Glycosyltransferase admitted by the KEYWORD alone (reaction text lacks an explicit donor).
    "GT0002": ("2.4.1.17", ["Glycosyltransferase"], "a substrate + a sugar donor = a glycoside"),
    # EC 1.1.1 but NO NAD(P) cosubstrate (flavin-style) -> held (no mechanism corroboration).
    "NX0001": ("1.1.1.1", ["Oxidoreductase"], "a substrate + O2 = a product + H2O2"),
    # EC 2.4 but neither a nucleotide-sugar donor nor the keyword -> held.
    "NX0002": ("2.4.2.1", ["Transferase"], "a nucleoside + phosphate = a base + alpha-D-ribose"),
}

_NAD_ACCESSIONS = {"ND0001", "ND0002", "NX0001"}
_GLYCO_ACCESSIONS = {"GT0001", "GT0002", "NX0002"}


def _search_record(accession):
    ec, _, _ = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": f"Test enzyme {accession}",
        "organism": f"Organism {accession}",
        "length": 350,
        "sequence": "M" + "A" * 349,
        "ec_numbers": [ec],
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _entry_record(accession):
    ec, keywords, reaction = _ROWS[accession]
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "sequence_length": 350,
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
        "binding_site_features": [
            {
                "feature_type": "Binding site",
                "begin": 15,
                "end": 20,
                "description": "Rossmann / donor binding",
                "ligand_name": None,
                "ligand_id": None,
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
        "cofactor_comments": [],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _fake_query_fetcher(query, size):
    # Return NAD rows on any EC 1.1.1 lane; glyco rows on any EC 2.4 lane. Cross-lane dedup
    # keeps each accession fetched once regardless of how many lanes match.
    if "1.1.1" in query:
        accessions = _NAD_ACCESSIONS
    elif "2.4" in query:
        accessions = _GLYCO_ACCESSIONS
    else:
        accessions = set()
    records = [_search_record(a) for a in sorted(accessions)]
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _entry_record(accession)}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class NadGlycosyltransferaseSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        return build_nad_glycosyltransferase_subfamily_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-12T00:00:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_families_are_the_two_broadened_handle_families(self):
        self.assertEqual(set(FAMILIES), {"nad_p_dehydrogenase", "glycosyltransferase"})

    def test_fetches_and_routes_both_families(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 6)
        # Four mechanism-corroborated rows (2 NAD + 2 glyco); the two controls are held.
        self.assertEqual(audit["counts"]["mechanism_corroborated_bronze_labels"], 4)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 2)

    def test_admitted_fingerprint_counts(self):
        audit = self._run()
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"glycosyltransferase": 2, "nad_p_dehydrogenase": 2},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        by_fp = {label["fingerprint_id"] for label in audit["applied_labels"]}
        self.assertEqual(by_fp, set(FAMILIES))
        for label in audit["applied_labels"]:
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["review_status"], "automation_curated")
            self.assertEqual(label["label_type"], "seed_fingerprint")
            self.assertTrue(label["entry_id"].startswith("uniprot:"))
            # Predictive features stay empty; the broadened handles are scope/admission only.
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            for excluded in ("ec_label", "protein_name", "uniprot_prose", "target_family_lane"):
                self.assertIn(excluded, label["evidence"]["excluded_context"])
            # The broadened mechanism axes are recorded as scope/admission evidence only.
            tier = label["evidence"]["source_trust_tier"]
            self.assertEqual(tier["source_tier"], "source_tier_0")
            self.assertTrue(tier["meets_n_of_m"])
            self.assertGreaterEqual(len(tier["mechanism_corroborator_axes_present"]), 1)
            # EC is recognized as a scope hint but never counted as a corroborator.
            self.assertNotIn("ec_scope_hint", tier["mechanism_corroborator_axes_present"])

    def test_nad_p_admitted_via_cosubstrate_axis(self):
        audit = self._run()
        nad_labels = [
            label
            for label in audit["applied_labels"]
            if label["fingerprint_id"] == "nad_p_dehydrogenase"
        ]
        self.assertEqual(len(nad_labels), 2)
        for label in nad_labels:
            axes = label["evidence"]["source_trust_tier"]["mechanism_corroborator_axes_present"]
            self.assertIn("cofactor_or_cosubstrate", axes)
            self.assertIn("rhea_reaction_or_participant_pattern", axes)

    def test_glycosyltransferase_admitted_via_donor_or_keyword(self):
        audit = self._run()
        glyco_ids = {
            label["entry_id"]
            for label in audit["applied_labels"]
            if label["fingerprint_id"] == "glycosyltransferase"
        }
        # GT0001 (donor + keyword) and GT0002 (keyword only) both admit.
        self.assertEqual(glyco_ids, {"uniprot:GT0001", "uniprot:GT0002"})

    def test_controls_without_mechanism_corroboration_held(self):
        audit = self._run()
        admitted_ids = {label["entry_id"] for label in audit["applied_labels"]}
        self.assertNotIn("uniprot:NX0001", admitted_ids)  # EC 1.1.1, no NAD cosubstrate
        self.assertNotIn("uniprot:NX0002", admitted_ids)  # EC 2.4, no donor / no keyword

    def test_admitted_labels_carry_deploy_input_sequence_provenance(self):
        audit = self._run()
        for label in audit["applied_labels"]:
            provenance = label["evidence"]["sequence_provenance"]
            accession = label["entry_id"].split(":", 1)[1]
            self.assertEqual(provenance["source_accession"], accession)
            self.assertEqual(provenance["source"], "reviewed_uniprot")
            self.assertEqual(len(provenance["sequence_sha256"]), 64)
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            self.assertNotIn("sequence", json.dumps(label["evidence"]["excluded_context"]))

    def test_per_family_cap_is_confusable_aware(self):
        audit = self._run()
        caps = audit["guardrails"]["per_fingerprint_cap_ceiling_enforced_per_family"]
        self.assertEqual(caps["nad_p_dehydrogenase"], 150)  # confusable -> 150
        self.assertEqual(caps["glycosyltransferase"], 250)  # not confusable -> 250
        self.assertIn("nad_p_dehydrogenase", CONFUSABLE_FAMILIES)
        self.assertNotIn("glycosyltransferase", CONFUSABLE_FAMILIES)

    def test_floor_projection_records_deploy_missing_context(self):
        audit = self._run()
        nad = audit["floor_projection"]["nad_p_dehydrogenase"]
        glyco = audit["floor_projection"]["glycosyltransferase"]
        self.assertEqual(nad["deploy_missing_active_site_context"], "nad_p_cosubstrate")
        self.assertEqual(
            glyco["deploy_missing_active_site_context"], "sugar_nucleotide_donor"
        )
        self.assertEqual(nad["combined_before"], 0)
        self.assertEqual(nad["admitted_this_run"], 2)
        self.assertFalse(nad["projected_over_cap"])

    def test_guardrails_non_destructive_and_leakage_safe(self):
        audit = self._run()
        g = audit["guardrails"]
        self.assertFalse(g["curated_registry_written"])
        self.assertTrue(g["frozen_current702_benchmark_preserved"])
        self.assertFalse(g["predictive_features_use_ec_name_keyword_cosubstrate_or_prose"])
        self.assertTrue(g["broadened_handles_never_predictive_features"])
        self.assertTrue(g["ec_never_a_counted_corroborator"])
        self.assertTrue(g["novelty_gated_against_both_registries"])

    def test_unknown_family_rejected(self):
        with self.assertRaises(ValueError):
            self._run(families=("metallopeptidase",))


if __name__ == "__main__":
    unittest.main()
