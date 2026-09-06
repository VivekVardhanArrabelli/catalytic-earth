from __future__ import annotations

import contextlib
import copy
import io
import json
import unittest

from catalytic_earth.atlas_draft_query import query_source_drafts
from catalytic_earth.core_cli import (
    main,
    verified_primary_evidence,
    verified_source_drafts,
)


class SourceDraftQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = verified_source_drafts()

    def test_assembly_filter_distinguishes_fixed_from_cycling_components(self):
        fixed = query_source_drafts(self.bundle, assembly="fixed_multisubunit")
        cycling = query_source_drafts(self.bundle, assembly="cycle_coupled_association")
        self.assertEqual([r["mcsa_id"] for r in fixed["records"]], ["M0107"])
        self.assertEqual([r["mcsa_id"] for r in cycling["records"]], ["M0212"])

    def test_compact_result_preserves_hisf_scope_and_conflict(self):
        result = query_source_drafts(self.bundle, mcsa_id="m0753")
        record = result["records"][0]
        self.assertEqual(record["evidence_tier"], 1)
        self.assertTrue(any(a["clause_id"] == "resolved_aspartate_roles"
                            for a in record["mandatory_abstentions"]))
        self.assertIn("HisF", record["source_scope"])
        source = next(r for r in self.bundle["records"] if r["mcsa_id"] == "M0753")
        self.assertEqual(record["source_residue_assertions"], source["source_residue_assertions"])
        self.assertIn("source_step_count", record["mechanism_proposals"][0])
        self.assertNotIn("mechanism_steps", record["mechanism_proposals"][0])

    def test_step_expansion_does_not_mutate_shared_package(self):
        before = copy.deepcopy(self.bundle)
        full = query_source_drafts(self.bundle, mcsa_id="M0107", include_steps=True)
        compact = query_source_drafts(self.bundle, mcsa_id="M0107")
        for whole, brief in zip(full["records"][0]["mechanism_proposals"],
                                compact["records"][0]["mechanism_proposals"]):
            self.assertEqual(len(whole["mechanism_steps"]), brief["source_step_count"])
        self.assertEqual(before, self.bundle)

    def test_empty_result_is_not_a_source_absence_claim(self):
        result = query_source_drafts(self.bundle, mcsa_id="M9999")
        self.assertEqual(result["record_count"], 0)
        self.assertEqual(result["claim_boundary"], self.bundle["claim_boundary"])
        self.assertEqual(result["selection"], self.bundle["selection"])
        self.assertEqual(result["selection"]["record_ids"], ["M0106", "M0107", "M0212", "M0753"])
        self.assertEqual(result["selection"]["requested_operation"], "source_scoped_mechanism_draft")

    def test_cli_retrieves_carrier_chemistry_with_abstentions(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(["atlas-drafts", "--mcsa-id", "M0106", "--text", "lipoyl"])
        result = json.loads(output.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(result["record_count"], 1)
        clauses = {a["clause_id"] for a in result["records"][0]["mandatory_abstentions"]}
        self.assertTrue({"carrier_host_identity", "attachment_site", "structure_localization"} <= clauses)

    def test_participant_filter_finds_co2_records_without_proposal_duplication(self):
        result = query_source_drafts(
            self.bundle,
            participants=("CHEBI:16526",),
            products=("CHEBI:16526",),
        )

        self.assertEqual(
            [record["mcsa_id"] for record in result["records"]],
            ["M0106", "M0107"],
        )
        self.assertEqual(result["filters"]["participants"], ["CHEBI:16526"])
        self.assertEqual(result["filters"]["products"], ["CHEBI:16526"])
        for record in result["records"]:
            self.assertEqual(len(record["participant_matches"]), 1)
            self.assertEqual(
                record["participant_matches"][0]["normalized_chebi_id"],
                "CHEBI:16526",
            )
            self.assertEqual(record["participant_matches"][0]["side"], "right")
        codh = next(record for record in result["records"] if record["mcsa_id"] == "M0107")
        self.assertEqual(len(codh["mechanism_proposals"]), 2)
        self.assertEqual(
            query_source_drafts(
                self.bundle,
                reactants=("CHEBI:16526",),
            )["record_count"],
            0,
        )

    def test_reactant_and_product_filters_preserve_ammonium_direction(self):
        cases = (
            (
                {"participants": ("CHEBI:28938",)},
                [("M0212", "right", 2), ("M0753", "left", 1)],
            ),
            ({"reactants": ("CHEBI:28938",)}, [("M0753", "left", 1)]),
            ({"products": ("CHEBI:28938",)}, [("M0212", "right", 2)]),
        )
        for filters, expected in cases:
            with self.subTest(filters=filters):
                result = query_source_drafts(self.bundle, **filters)
                self.assertEqual(
                    [
                        (
                            record["mcsa_id"],
                            record["participant_matches"][0]["side"],
                            record["participant_matches"][0]["source_count"],
                        )
                        for record in result["records"]
                    ],
                    expected,
                )

    def test_all_chemical_clauses_must_match_within_one_source_record(self):
        result = query_source_drafts(
            self.bundle,
            participants=("CHEBI:16526", "CHEBI:28938"),
        )

        self.assertEqual(result["record_count"], 0)
        self.assertEqual(result["records"], [])
        self.assertEqual(result["selection"], self.bundle["selection"])
        self.assertEqual(result["claim_boundary"], self.bundle["claim_boundary"])
        self.assertEqual(
            result["filters"]["participants"],
            ["CHEBI:16526", "CHEBI:28938"],
        )
        semantics = result["query_semantics"]
        self.assertEqual(
            semantics["filter_combination"],
            "all_clauses_within_one_record",
        )
        self.assertIn("does_not_ground", semantics["proposal_applicability"])
        self.assertFalse(semantics["shared_participant_implies_reaction_equivalence"])

    def test_chemical_filters_intersect_with_existing_filters(self):
        result = query_source_drafts(
            self.bundle,
            participants=("CHEBI:16526",),
            reactants=("CHEBI:15377",),
            assembly="fixed_multisubunit",
            text="benzoquinones",
        )

        self.assertEqual([record["mcsa_id"] for record in result["records"]], ["M0107"])
        self.assertEqual(
            [match["source_row_index"] for match in result["records"][0]["participant_matches"]],
            [2, 3],
        )

    def test_compact_chemical_result_preserves_evidence_and_does_not_alias_bundle(self):
        before = copy.deepcopy(self.bundle)
        result = query_source_drafts(
            self.bundle,
            mcsa_id="M0106",
            participants=("CHEBI:83099", "CHEBI:15378"),
        )
        record = result["records"][0]
        source = next(item for item in self.bundle["records"] if item["mcsa_id"] == "M0106")

        self.assertEqual(
            [match["source_row_index"] for match in record["participant_matches"]],
            [3, 4],
        )
        self.assertEqual(record["source_residue_assertions"], source["source_residue_assertions"])
        self.assertEqual(record["mandatory_abstentions"], source["mandatory_abstentions"])
        self.assertNotIn("mechanism_steps", record["mechanism_proposals"][0])
        self.assertEqual(self.bundle, before)
        record["participant_matches"][0]["name"] = "changed in query result"
        self.assertEqual(self.bundle, before)

    def test_cli_repeated_chemical_filters_normalize_numeric_identifiers(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main([
                "atlas-drafts",
                "--participant", "16526",
                "--participant", "CHEBI:15377",
                "--product", "24646",
            ])
        result = json.loads(output.getvalue())

        self.assertEqual(code, 0)
        self.assertEqual([record["mcsa_id"] for record in result["records"]], ["M0107"])
        self.assertEqual(
            result["filters"]["participants"],
            ["CHEBI:16526", "CHEBI:15377"],
        )
        self.assertEqual(result["filters"]["products"], ["CHEBI:24646"])

    def test_cli_rejects_malformed_chemical_identifier(self):
        error = io.StringIO()
        with contextlib.redirect_stderr(error), self.assertRaises(SystemExit) as raised:
            main(["atlas-drafts", "--participant", "CHEBI:not-a-number"])

        self.assertEqual(raised.exception.code, 2)
        self.assertIn("CHEBI", error.getvalue())

    def test_exact_mechanism_component_label_spans_reviewed_batches(self):
        additional = verified_source_drafts("aldolase-transketolase")
        default_result = query_source_drafts(
            self.bundle,
            mechanism_components=("  Schiff Base Formed  ", "schiff base formed"),
        )
        additional_result = query_source_drafts(
            additional, mechanism_components=("schiff base formed",),
        )

        self.assertEqual(default_result["schema_version"],
                         "catalytic-earth.source-draft-query.v3")
        self.assertEqual(default_result["filters"]["mechanism_components"],
                         ["schiff base formed"])
        self.assertEqual([record["mcsa_id"] for record in default_result["records"]],
                         ["M0753"])
        self.assertEqual([record["mcsa_id"] for record in additional_result["records"]],
                         ["M0222"])
        for result in (default_result, additional_result):
            witness = result["records"][0]["mechanism_component_matches"]
            self.assertEqual(len(witness), 1)
            self.assertEqual(witness[0]["matched_labels"], ["schiff base formed"])
            self.assertEqual(
                witness[0]["raw_components_summary"],
                result["records"][0]["mechanism_proposals"][0]["components_summary"],
            )

    def test_all_component_labels_must_match_within_one_proposal(self):
        result = query_source_drafts(
            self.bundle,
            mcsa_id="M0107",
            mechanism_components=(
                "decoordination from a metal ion",
                "decarboxylation",
            ),
        )

        self.assertEqual(result["record_count"], 0)
        self.assertEqual(result["records"], [])
        self.assertEqual(
            result["query_semantics"]["mechanism_component_match_scope"],
            "all_requested_exact_source_labels_within_one_proposal",
        )

    def test_component_witness_does_not_drop_alternatives_or_ground_participants(self):
        before = copy.deepcopy(self.bundle)
        result = query_source_drafts(
            self.bundle,
            mcsa_id="M0107",
            products=("CHEBI:16526",),
            mechanism_components=("decoordination from a metal ion",),
        )

        self.assertEqual(result["record_count"], 1)
        record = result["records"][0]
        self.assertEqual(len(record["mechanism_proposals"]), 2)
        self.assertEqual(
            [match["source_mechanism_id"]
             for match in record["mechanism_component_matches"]],
            [2],
        )
        self.assertEqual(record["participant_matches"][0]["side"], "right")
        self.assertFalse(
            result["query_semantics"]["participant_match_grounds_matching_proposal"]
        )
        self.assertEqual(self.bundle, before)

    def test_component_matching_is_exact_and_witnesses_follow_source_order(self):
        exact = query_source_drafts(
            self.bundle,
            mcsa_id="M0106",
            mechanism_components=("proton transfer", "COFACTOR USED"),
        )
        substring = query_source_drafts(
            self.bundle,
            mcsa_id="M0106",
            mechanism_components=("proton",),
        )

        self.assertEqual(exact["filters"]["mechanism_components"],
                         ["proton transfer", "cofactor used"])
        self.assertEqual(
            exact["records"][0]["mechanism_component_matches"][0]["matched_labels"],
            ["cofactor used", "proton transfer"],
        )
        self.assertEqual(substring["record_count"], 0)
        self.assertFalse(
            exact["query_semantics"]["mechanism_component_implies_exact_reaction"]
        )
        self.assertEqual(
            exact["query_semantics"]["mechanism_component_step_localization"],
            "not_established",
        )

    def test_component_filter_rejects_non_sequences_and_non_labels(self):
        for invalid in (
            "proton transfer",
            None,
            ("",),
            ("proton transfer, electron relay",),
            (3,),
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                query_source_drafts(self.bundle, mechanism_components=invalid)

    def test_unused_component_filter_preserves_v1_and_v2_queries(self):
        self.assertEqual(
            query_source_drafts(self.bundle),
            query_source_drafts(self.bundle, mechanism_components=[]),
        )
        additional = verified_source_drafts("aldolase-transketolase")
        primary = verified_primary_evidence(
            "aldolase-transketolase", bundle=additional,
        )
        original_v2 = query_source_drafts(additional, primary_evidence=primary)
        explicit_empty_v2 = query_source_drafts(
            additional, primary_evidence=primary, mechanism_components=(),
        )
        self.assertEqual(original_v2["schema_version"],
                         "catalytic-earth.source-draft-query.v2")
        self.assertEqual(original_v2, explicit_empty_v2)


if __name__ == "__main__":
    unittest.main()
