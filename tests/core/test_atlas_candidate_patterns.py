from __future__ import annotations

import copy
import hashlib
import re
import unittest

from catalytic_earth.atlas_candidate_events import (
    build_candidate_event_catalog,
    canonical_bytes,
)
from catalytic_earth.atlas_candidate_patterns import query_candidate_patterns
from scripts.build_atlas_candidate_events import build


CC_ADD = {
    "kind": "bond",
    "elements": ["C", "C"],
    "variables": ["x", "y"],
    "before": 0,
    "after": 1,
}
C_NEUTRALIZE_X = {
    "kind": "charge",
    "elements": ["C"],
    "variables": ["x"],
    "before": -1,
    "after": 0,
}


class CandidatePatternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = build()

    def catalog_inputs(self):
        candidates = [copy.deepcopy(row["candidate"]) for row in self.catalog["candidates"]]
        contexts = []
        for row, binding in zip(
            self.catalog["candidates"],
            self.catalog["provenance"]["candidate_context_bindings"],
        ):
            context = copy.deepcopy(binding)
            context["source_context"] = copy.deepcopy(row["source_context"])
            contexts.append(context)
        provenance = {
            key: copy.deepcopy(self.catalog["provenance"][key])
            for key in (
                "context_scan",
                "source_draft_bundles",
                "catalog_implementation_sha256",
            )
        }
        provenance["candidate_contexts"] = contexts
        return candidates, provenance

    @staticmethod
    def source_binding(match):
        return match["candidate_row"]["candidate"]["source_binding"]

    @staticmethod
    def binding_key(match, binding):
        source = CandidatePatternTests.source_binding(match)
        return (
            source["record_id"],
            source["mechanism_id"],
            source["before_step_id"],
            tuple(sorted(binding["atom_bindings"].items())),
            tuple(
                sorted(
                    event["edit_id"]
                    for witness in binding["clause_witnesses"]
                    for event in witness["events"]
                )
            ),
        )

    @staticmethod
    def all_binding_keys(result):
        return {
            CandidatePatternTests.binding_key(match, binding)
            for match in result["matches"]
            for binding in match["bindings"]
        }

    @staticmethod
    def rebind_candidate(provenance, index, candidate):
        provenance["candidate_contexts"][index]["candidate_sha256"] = hashlib.sha256(
            canonical_bytes(candidate)
        ).hexdigest()

    @staticmethod
    def rename_atom_ids(value):
        if isinstance(value, str) and re.fullmatch(r"a[0-9]+", value):
            return "renamed_" + value
        if isinstance(value, list):
            return [CandidatePatternTests.rename_atom_ids(item) for item in value]
        if isinstance(value, dict):
            return {
                key: CandidatePatternTests.rename_atom_ids(item)
                for key, item in value.items()
            }
        return value

    def test_shared_atom_positive_and_disjoint_negative(self):
        positive = query_candidate_patterns(
            self.catalog, clauses=[CC_ADD, C_NEUTRALIZE_X]
        )
        self.assertEqual(positive["candidate_count"], 1)
        self.assertEqual(positive["binding_count"], 1)
        match = positive["matches"][0]
        self.assertEqual(
            (
                self.source_binding(match)["record_id"],
                self.source_binding(match)["mechanism_id"],
                self.source_binding(match)["before_step_id"],
            ),
            ("M0219", 1, 2),
        )
        binding = match["bindings"][0]
        self.assertEqual(binding["atom_bindings"], {"x": "a10", "y": "a28"})
        self.assertEqual(
            {
                witness["clause"]["kind"]: [
                    event["edit_id"] for event in witness["events"]
                ]
                for witness in binding["clause_witnesses"]
            },
            {"bond": ["e11"], "charge": ["e12"]},
        )

        disjoint = query_candidate_patterns(
            self.catalog,
            clauses=[
                {
                    "kind": "bond",
                    "elements": ["C", "O"],
                    "variables": ["x", "y"],
                    "before": 2,
                    "after": 1,
                },
                C_NEUTRALIZE_X,
            ],
        )
        self.assertEqual(disjoint["candidate_count"], 0)
        self.assertEqual(disjoint["binding_count"], 0)
        self.assertEqual(disjoint["matches"], [])
        self.assertFalse(disjoint["query_semantics"]["bindings_imply_physical_atom_identity"])

    def test_homoelement_orientations_endpoint_reversal_and_clause_sets(self):
        cc = query_candidate_patterns(self.catalog, clauses=[CC_ADD])
        self.assertEqual(cc["candidate_count"], 2)
        self.assertEqual(cc["binding_count"], 4)
        step2 = next(
            match for match in cc["matches"]
            if self.source_binding(match)["before_step_id"] == 2
        )
        self.assertEqual(
            {tuple(sorted(binding["atom_bindings"].items())) for binding in step2["bindings"]},
            {
                (("x", "a10"), ("y", "a28")),
                (("x", "a28"), ("y", "a10")),
            },
        )

        reversed_cc = copy.deepcopy(CC_ADD)
        reversed_cc["variables"] = ["y", "x"]
        self.assertEqual(
            canonical_bytes(query_candidate_patterns(self.catalog, clauses=[reversed_cc])),
            canonical_bytes(cc),
        )
        co = {
            "kind": "bond",
            "elements": ["C", "O"],
            "variables": ["carbon", "oxygen"],
            "before": 2,
            "after": 1,
        }
        reversed_co = {
            **co,
            "elements": ["O", "C"],
            "variables": ["oxygen", "carbon"],
        }
        self.assertEqual(
            canonical_bytes(query_candidate_patterns(self.catalog, clauses=[co])),
            canonical_bytes(query_candidate_patterns(self.catalog, clauses=[reversed_co])),
        )

        repeated = query_candidate_patterns(
            self.catalog, clauses=[CC_ADD, C_NEUTRALIZE_X, copy.deepcopy(CC_ADD)]
        )
        single = query_candidate_patterns(
            self.catalog, clauses=[CC_ADD, C_NEUTRALIZE_X]
        )
        self.assertEqual(canonical_bytes(repeated), canonical_bytes(single))

    def test_variables_are_injective_and_never_cross_candidates(self):
        no_alias = query_candidate_patterns(
            self.catalog,
            clauses=[
                C_NEUTRALIZE_X,
                {
                    **C_NEUTRALIZE_X,
                    "variables": ["y"],
                },
            ],
            mcsa_id="M0219",
        )
        self.assertEqual(no_alias["binding_count"], 0)

        # These signatures occur in separate M0106 adjacent-panel candidates.
        # A record-level source context cannot join their variables or events.
        no_cross_candidate = query_candidate_patterns(
            self.catalog,
            mcsa_id="m0106",
            support="any",
            clauses=[
                {
                    "kind": "bond",
                    "elements": ["C", "H"],
                    "variables": ["carbon", "proton"],
                    "before": 0,
                    "after": 1,
                },
                {
                    "kind": "bond",
                    "elements": ["O", "H"],
                    "variables": ["oxygen", "proton"],
                    "before": 0,
                    "after": 1,
                },
            ],
        )
        self.assertEqual(no_cross_candidate["candidate_count"], 0)
        self.assertEqual(no_cross_candidate["filters"]["mcsa_id"], "M0106")
        self.assertEqual(
            no_cross_candidate["query_semantics"]["clause_combination"],
            "all_clauses_within_one_candidate",
        )

        self_bond = {**CC_ADD, "variables": ["x", "x"]}
        with self.assertRaises(ValueError):
            query_candidate_patterns(self.catalog, clauses=[self_bond])

    def test_support_filter_precedes_join_and_retains_witness_multiplicity(self):
        transfer = [
            {
                "kind": "bond",
                "elements": ["N", "H"],
                "variables": ["base", "proton"],
                "before": 1,
                "after": 0,
            },
            {
                "kind": "charge",
                "elements": ["N"],
                "variables": ["base"],
                "before": 1,
                "after": 0,
            },
        ]
        any_support = query_candidate_patterns(
            self.catalog, clauses=transfer, mcsa_id="M0106", support="any"
        )
        self.assertEqual(any_support["candidate_count"], 1)
        self.assertEqual(any_support["binding_count"], 1)
        self.assertEqual(
            {event["support"]
             for witness in any_support["matches"][0]["bindings"][0]["clause_witnesses"]
             for event in witness["events"]},
            {"after_graph_confirmed", "source_arrow_only"},
        )
        for support in ("after_graph_confirmed", "source_arrow_only"):
            with self.subTest(support=support):
                result = query_candidate_patterns(
                    self.catalog, clauses=transfer, mcsa_id="M0106", support=support
                )
                self.assertEqual(result["binding_count"], 0)

        oh_add = [{
            "kind": "bond",
            "elements": ["O", "H"],
            "variables": ["oxygen", "hydrogen"],
            "before": 0,
            "after": 1,
        }]
        arrow_only = query_candidate_patterns(
            self.catalog,
            clauses=oh_add,
            mcsa_id="M0212",
            support="source_arrow_only",
        )
        self.assertEqual(arrow_only["candidate_count"], 1)
        self.assertEqual(arrow_only["binding_count"], 2)
        self.assertEqual(
            {
                witness["events"][0]["edit_id"]
                for binding in arrow_only["matches"][0]["bindings"]
                for witness in binding["clause_witnesses"]
            },
            {"e2", "e5"},
        )
        self.assertEqual(
            query_candidate_patterns(
                self.catalog,
                clauses=oh_add,
                mcsa_id="M0212",
                support="after_graph_confirmed",
            )["binding_count"],
            0,
        )

    def test_atom_renaming_and_row_reordering_preserve_pattern_semantics(self):
        baseline = query_candidate_patterns(
            self.catalog, clauses=[CC_ADD, C_NEUTRALIZE_X]
        )
        candidates, provenance = self.catalog_inputs()
        candidates.reverse()
        provenance["candidate_contexts"].reverse()
        for candidate in candidates:
            candidate["proposed_graph_edits"].reverse()
        for index, candidate in enumerate(candidates):
            self.rebind_candidate(provenance, index, candidate)
        reordered = build_candidate_event_catalog(candidates, provenance=provenance)
        reordered_result = query_candidate_patterns(
            reordered, clauses=[CC_ADD, C_NEUTRALIZE_X]
        )
        self.assertEqual(
            self.all_binding_keys(reordered_result), self.all_binding_keys(baseline)
        )

        target = next(
            index for index, candidate in enumerate(candidates)
            if candidate["source_binding"]["record_id"] == "M0219"
            and candidate["source_binding"]["before_step_id"] == 2
        )
        candidates[target] = self.rename_atom_ids(candidates[target])
        self.rebind_candidate(provenance, target, candidates[target])
        renamed = build_candidate_event_catalog(candidates, provenance=provenance)
        renamed_result = query_candidate_patterns(
            renamed, clauses=[CC_ADD, C_NEUTRALIZE_X]
        )
        self.assertEqual(renamed_result["candidate_count"], baseline["candidate_count"])
        self.assertEqual(renamed_result["binding_count"], baseline["binding_count"])
        renamed_binding = renamed_result["matches"][0]["bindings"][0]["atom_bindings"]
        self.assertEqual(
            {name: atom.removeprefix("renamed_") for name, atom in renamed_binding.items()},
            {"x": "a10", "y": "a28"},
        )

    def test_full_candidate_context_is_copied_without_promoting_scope(self):
        original = canonical_bytes(self.catalog)
        result = query_candidate_patterns(
            self.catalog, clauses=[CC_ADD, C_NEUTRALIZE_X]
        )
        match = result["matches"][0]
        candidate_id = match["candidate_row"]["candidate_id"]
        source_row = next(
            row for row in self.catalog["candidates"]
            if row["candidate_id"] == candidate_id
        )
        self.assertEqual(match["candidate_row"], source_row)
        candidate = match["candidate_row"]["candidate"]
        self.assertEqual(candidate["status"], "unreviewed")
        self.assertFalse(candidate["scope_effect"]["physical_atom_map"])
        self.assertFalse(candidate["scope_effect"]["reviewed_evidence"])
        self.assertTrue(candidate["scope_effect"]["opaque_annotations_preserved"])

        match["candidate_row"]["source_context"]["source_scope"] = "changed"
        match["bindings"][0]["atom_bindings"]["x"] = "changed"
        match["bindings"][0]["clause_witnesses"][0]["events"].clear()
        result["provenance"]["context_scan"]["path"] = "changed.json"
        self.assertEqual(canonical_bytes(self.catalog), original)

    def test_invalid_clauses_filters_and_limits_raise_without_partial_results(self):
        invalid_clauses = [
            [],
            [{**CC_ADD, "kind": []}],
            [{**CC_ADD, "variables": ["x"]}],
            [{**CC_ADD, "variables": ["x", "x"]}],
            [{**CC_ADD, "variables": ["", "y"]}],
            [{**CC_ADD, "variables": [True, "y"]}],
            [{**CC_ADD, "elements": ["R", "C"]}],
            [{**CC_ADD, "elements": ["*", "C"]}],
            [{**CC_ADD, "elements": ["Qq", "C"]}],
            [{**CC_ADD, "elements": ["c", "C"]}],
            [{**CC_ADD, "before": True}],
            [{**CC_ADD, "after": "NaN"}],
            [{**CC_ADD, "before": 1, "after": 1}],
            [CC_ADD, {**C_NEUTRALIZE_X, "elements": ["N"]}],
        ]
        for clauses in invalid_clauses:
            with self.subTest(clauses=clauses), self.assertRaises(ValueError):
                query_candidate_patterns(self.catalog, clauses=clauses)
        for clauses in (None, {}, "bond"):
            with self.subTest(clauses=clauses), self.assertRaises(ValueError):
                query_candidate_patterns(self.catalog, clauses=clauses)
        for support in (True, "reviewed"):
            with self.subTest(support=support), self.assertRaises(ValueError):
                query_candidate_patterns(self.catalog, clauses=[CC_ADD], support=support)
        for mcsa_id in (True, "M0219-any"):
            with self.subTest(mcsa_id=mcsa_id), self.assertRaises(ValueError):
                query_candidate_patterns(self.catalog, clauses=[CC_ADD], mcsa_id=mcsa_id)

        bond_states = [
            (before, after)
            for before in range(4)
            for after in range(4)
            if before != after
        ]
        too_many_clauses = [
            {**CC_ADD, "before": before, "after": after}
            for before, after in bond_states[:9]
        ]
        with self.assertRaisesRegex(ValueError, "eight|8"):
            query_candidate_patterns(self.catalog, clauses=too_many_clauses)
        too_many_variables = [
            {
                **CC_ADD,
                "variables": [f"x{2 * index}", f"x{2 * index + 1}"],
            }
            for index in range(7)
        ]
        with self.assertRaisesRegex(ValueError, "twelve|12"):
            query_candidate_patterns(self.catalog, clauses=too_many_variables)

    def test_search_budget_raises_instead_of_returning_a_partial_match_set(self):
        candidates, provenance = self.catalog_inputs()
        target = next(
            index for index, candidate in enumerate(candidates)
            if candidate["source_binding"]["record_id"] == "M0219"
            and candidate["source_binding"]["before_step_id"] == 2
        )
        candidate = candidates[target]
        template_before = {
            "element": "C", "formal_charge": -1, "stereochemistry": None
        }
        template_after = {
            "element": "C", "formal_charge": 0, "stereochemistry": None
        }
        template_edit = next(
            edit for edit in candidate["proposed_graph_edits"]
            if edit["edit_id"] == "e12"
        )
        for index in range(320):
            atom_id = f"budget_atom_{index}"
            candidate["source_panels"]["before_graph"]["atoms"].append(
                {"atom_id": atom_id, **template_before}
            )
            candidate["source_panels"]["after_graph"]["atoms"].append(
                {"atom_id": atom_id, **template_after}
            )
            candidate["proposed_graph_edits"].append({
                **copy.deepcopy(template_edit),
                "edit_id": f"budget_edit_{index}",
                "atom_ids": [atom_id],
            })
        self.rebind_candidate(provenance, target, candidate)
        expanded = build_candidate_event_catalog(candidates, provenance=provenance)
        with self.assertRaisesRegex(ValueError, "budget|limit"):
            query_candidate_patterns(
                expanded,
                mcsa_id="M0219",
                clauses=[
                    C_NEUTRALIZE_X,
                    {**C_NEUTRALIZE_X, "variables": ["y"]},
                ],
            )


if __name__ == "__main__":
    unittest.main()
