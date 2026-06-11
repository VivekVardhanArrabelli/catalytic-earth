"""Offline validation of the Stage-1 hole-sourcing runner.

No network: the UniProt/Rhea fetchers are injected with synthetic payloads shaped
exactly like `adapters.normalize_uniprot_tsv` / `normalize_uniprot_entry_json`
output, so the full chain (fetch -> cofactor/EC disambiguation -> novelty gate ->
preview) is exercised end to end and the routing/guardrails are asserted.
"""

from __future__ import annotations

import unittest

from catalytic_earth.stage1_hole_sourcing import (
    SOURCEABLE_FINGERPRINTS,
    SOURCEABLE_HOLES,
    build_stage1_hole_sourcing,
)


def _search_record(accession, ec_numbers, name):
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_name": f"{accession}_TEST",
        "protein_name": name,
        "organism": f"Organism {accession}",
        "length": 400,
        "sequence": "M" + "A" * 399,
        "ec_numbers": ec_numbers,
        "pdb_ids": [],
        "alphafold_ids": [accession],
        "reviewed": "reviewed",
        "evidence_level": "protein_cross_reference",
    }


def _entry_record(accession, *, cofactor_names, sam_binding=False, rhea_id="RHEA:1"):
    binding = []
    if sam_binding:
        binding.append(
            {
                "feature_type": "Binding site",
                "begin": 120,
                "end": 120,
                "description": "",
                "ligand_name": "S-adenosyl-L-methionine",
                "ligand_id": "ChEBI:CHEBI:59789",
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
        )
    return {
        "source": "uniprot",
        "accession": accession,
        "entry_type": "UniProtKB reviewed (Swiss-Prot)",
        "sequence_length": 400,
        "active_site_features": [
            {
                "feature_type": "Active site",
                "begin": 100,
                "end": 100,
                "description": "",
                "ligand_name": None,
                "ligand_id": None,
                "evidence": [{"evidence_code": "ECO:0000269"}],
                "cross_references": [],
            }
        ],
        "binding_site_features": binding,
        "metal_binding_features": [],
        "site_features": [],
        "modified_residue_features": [],
        "cross_link_features": [],
        "catalytic_activity_comments": [
            {
                "reaction": f"reaction for {accession}",
                "ec_number": ec_numbers_first(accession),
                "cross_references": [{"database": "Rhea", "id": rhea_id}],
                "evidence": [{"evidence_code": "ECO:0000269"}],
            }
        ],
        "cofactor_comments": [
            {
                "cofactors": [
                    {
                        "name": name,
                        "cross_reference": {"database": "ChEBI", "id": "CHEBI:0"},
                        "evidence": [{"evidence_code": "ECO:0000269"}],
                    }
                    for name in cofactor_names
                ]
            }
        ]
        if cofactor_names
        else [],
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


_EC_BY_ACCESSION = {
    "RS0001": "2.8.4.3",
    "CB0001": "5.4.99.2",
    "NM0001": "3.1.1.1",
    "FM0001": "1.14.13.8",
}


def ec_numbers_first(accession):
    return _EC_BY_ACCESSION.get(accession)


# Three fresh accessions: a genuine radical-SAM (Fe-S + SAM), a genuine cobalamin
# mutase (adenosylcobalamin + EC 5.4.99), and a non-matching esterase (no cofactor).
_SEARCH_RECORDS = [
    _search_record("RS0001", ["2.8.4.3"], "Radical SAM test enzyme"),
    _search_record("CB0001", ["5.4.99.2"], "Methylmalonyl-CoA mutase test"),
    _search_record("NM0001", ["3.1.1.1"], "Carboxylesterase test"),
]
_ENTRY_RECORDS = {
    "RS0001": _entry_record(
        "RS0001", cofactor_names=["[4Fe-4S] cluster"], sam_binding=True, rhea_id="RHEA:111"
    ),
    "CB0001": _entry_record(
        "CB0001", cofactor_names=["adenosylcobalamin"], rhea_id="RHEA:222"
    ),
    "NM0001": _entry_record("NM0001", cofactor_names=[], rhea_id="RHEA:333"),
}


def _fake_query_fetcher(query, size):
    # Return all three records on the first lane only; cross-lane dedup keeps each
    # accession fetched once regardless of how many lanes match.
    if "2.8.4" in query:
        records = _SEARCH_RECORDS
    else:
        records = []
    return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}


def _fake_entry_fetcher(accession):
    return {"metadata": {"url": f"test://{accession}"}, "record": _ENTRY_RECORDS[accession]}


def _fake_rhea_fetcher(ec_number, limit):
    return {"metadata": {"url": "test://rhea"}, "records": []}


class Stage1HoleSourcingTest(unittest.TestCase):
    def _run(self, **kwargs):
        kwargs.setdefault("holes", ("radical_sam_enzyme", "cobalamin_radical_rearrangement"))
        return build_stage1_hole_sourcing(
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-10T00:00:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
            **kwargs,
        )

    def test_fetches_and_routes_all_three_rows(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["fetched_candidate_rows"], 3)
        # RS + CB disambiguate to bronze; NM (no cofactor) is held.
        self.assertEqual(audit["counts"]["disambiguated_bronze_labels"], 2)
        self.assertGreaterEqual(audit["counts"]["disambiguation_hold_count"], 1)

    def test_novelty_admits_both_fresh_holes(self):
        audit = self._run()
        self.assertEqual(audit["counts"]["novelty_admitted_labels"], 2)
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"],
            {"cobalamin_radical_rearrangement": 1, "radical_sam_enzyme": 1},
        )

    def test_admitted_labels_are_bronze_and_leakage_safe(self):
        audit = self._run()
        by_fp = {label["fingerprint_id"]: label for label in audit["applied_labels"]}
        self.assertEqual(set(by_fp), {"radical_sam_enzyme", "cobalamin_radical_rearrangement"})
        for label in audit["applied_labels"]:
            self.assertEqual(label["tier"], "bronze")
            self.assertEqual(label["review_status"], "automation_curated")
            self.assertEqual(label["label_type"], "seed_fingerprint")
            self.assertTrue(label["entry_id"].startswith("uniprot:"))
            # EC / name / prose are excluded context, never predictive features.
            self.assertEqual(label["evidence"]["predictive_evidence"], [])
            for excluded in ("ec_label", "protein_name", "uniprot_prose"):
                self.assertIn(excluded, label["evidence"]["excluded_context"])

    def test_floor_projection_counts_admitted(self):
        audit = self._run()
        rs = audit["floor_projection"]["radical_sam_enzyme"]
        self.assertEqual(rs["combined_before"], 0)
        self.assertEqual(rs["admitted_this_run"], 1)
        self.assertEqual(rs["projected_combined"], 1)
        self.assertFalse(rs["floor_reached"])

    def test_guardrails_non_destructive(self):
        audit = self._run()
        g = audit["guardrails"]
        self.assertFalse(g["curated_registry_written"])
        self.assertTrue(g["frozen_current702_benchmark_preserved"])
        self.assertFalse(g["predictive_features_use_ec_name_or_prose"])
        self.assertTrue(g["novelty_gated_against_both_registries"])
        self.assertEqual(
            audit["status"],
            "non_destructive_preview_pending_explicit_registry_merge_authorization",
        )

    def test_existing_ortholog_is_throttled_not_reimported(self):
        # Seed the expansion registry with an RS ortholog sharing the cluster key
        # (same fingerprint, EC, organism, length). The novelty gate must not admit
        # a second near-duplicate beyond the per-cluster cap when no new chemistry.
        existing = []
        for i in range(3):
            existing.append(
                {
                    "entry_id": f"uniprot:RSDUP{i}",
                    "fingerprint_id": "radical_sam_enzyme",
                    "label_type": "seed_fingerprint",
                    "tier": "bronze",
                    "evidence": {
                        "source_provenance": {
                            "organism": "Organism RS0001",
                            "sequence_length": 400,
                        },
                        "mechanism_evidence": {
                            "ec_numbers": ["2.8.4.3"],
                            "reaction_equations": [{"rhea_id": "RHEA:111"}],
                        },
                    },
                }
            )
        audit = build_stage1_hole_sourcing(
            holes=("radical_sam_enzyme",),
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=existing,
            created_utc="2026-06-10T00:00:00Z",
            query_fetcher=_fake_query_fetcher,
            entry_fetcher=_fake_entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
        )
        # RS0001 shares the cluster key and brings no new reaction (RHEA:111 already
        # present) -> throttled, not admitted.
        admitted_ids = [label["entry_id"] for label in audit["applied_labels"]]
        self.assertNotIn("uniprot:RS0001", admitted_ids)
        self.assertGreaterEqual(audit["counts"]["novelty_throttled_or_rejected"], 1)

    def test_ser_his_is_rejected_as_unsourceable_here(self):
        with self.assertRaises(ValueError):
            self._run(holes=("ser_his_acid_hydrolase",))

    def test_sourceable_holes_excludes_ser_his(self):
        self.assertIn("radical_sam_enzyme", SOURCEABLE_HOLES)
        self.assertIn("cobalamin_radical_rearrangement", SOURCEABLE_HOLES)
        self.assertNotIn("ser_his_acid_hydrolase", SOURCEABLE_HOLES)

    def test_sourceable_fingerprints_cover_holes_and_under_floor(self):
        # The runner now sources the two holes AND the three under-floor cofactor
        # fingerprints; ser_his (cofactorless) is still excluded.
        for fingerprint in (
            "radical_sam_enzyme",
            "cobalamin_radical_rearrangement",
            "flavin_monooxygenase",
            "heme_peroxidase_oxidase",
            "flavin_dehydrogenase_reductase",
        ):
            self.assertIn(fingerprint, SOURCEABLE_FINGERPRINTS)
        self.assertNotIn("ser_his_acid_hydrolase", SOURCEABLE_FINGERPRINTS)

    def test_under_floor_flavin_monooxygenase_routes_to_bronze(self):
        # A genuine flavin monooxygenase (FAD + EC 1.14.13) disambiguates to the
        # flavin_monooxygenase under-floor fingerprint via the same engine/guardrails.
        search = _search_record("FM0001", ["1.14.13.8"], "Flavin monooxygenase test")
        entry = _entry_record("FM0001", cofactor_names=["FAD"], rhea_id="RHEA:444")

        def query_fetcher(query, size):
            records = [search] if "1.14.13" in query else []
            return {"metadata": {"url": "test://uniprot", "query": query}, "records": records}

        def entry_fetcher(accession):
            return {"metadata": {"url": f"test://{accession}"}, "record": entry}

        audit = build_stage1_hole_sourcing(
            holes=("flavin_monooxygenase",),
            max_records_per_lane=10,
            current_manifest_payload={"rows": []},
            frozen_benchmark_payload=[],
            expansion_payload=[],
            created_utc="2026-06-10T00:00:00Z",
            query_fetcher=query_fetcher,
            entry_fetcher=entry_fetcher,
            rhea_fetcher=_fake_rhea_fetcher,
        )
        self.assertEqual(
            audit["counts"]["admitted_fingerprint_counts"], {"flavin_monooxygenase": 1}
        )
        label = audit["applied_labels"][0]
        self.assertEqual(label["fingerprint_id"], "flavin_monooxygenase")
        self.assertEqual(label["tier"], "bronze")
        self.assertEqual(label["evidence"]["predictive_evidence"], [])


if __name__ == "__main__":
    unittest.main()
