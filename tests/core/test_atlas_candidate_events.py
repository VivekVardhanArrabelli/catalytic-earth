from __future__ import annotations

import copy
import hashlib
import re
import unittest

from catalytic_earth.atlas_candidate_events import (
    build_candidate_event_catalog,
    canonical_bytes,
    query_candidate_events,
    validate_candidate_event_catalog,
)
from scripts.build_atlas_candidate_events import build


CC_ADD = {"kind": "bond", "elements": ["C", "C"], "before": 0, "after": 1}
C_NEUTRALIZE = {"kind": "charge", "elements": ["C"], "before": -1, "after": 0}
OH_ADD = {"kind": "bond", "elements": ["O", "H"], "before": 0, "after": 1}


class CandidateEventTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Build from the frozen scan and retained source snapshots so these
        # expectations exercise the source-derived catalog, not a hand fixture.
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
    def binding_tuples(result):
        return [
            (
                match["candidate_row"]["candidate"]["source_binding"]["record_id"],
                match["candidate_row"]["candidate"]["source_binding"]["mechanism_id"],
                match["candidate_row"]["candidate"]["source_binding"]["before_step_id"],
            )
            for match in result["matches"]
        ]

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
            return [CandidateEventTests.rename_atom_ids(item) for item in value]
        if isinstance(value, dict):
            return {
                key: CandidateEventTests.rename_atom_ids(item)
                for key, item in value.items()
            }
        return value

    def test_source_derived_catalog_retains_every_edit_and_scope(self):
        summary = validate_candidate_event_catalog(self.catalog)
        self.assertEqual(summary["candidate_count"], 12)
        self.assertEqual(summary["event_count"], 86)
        self.assertEqual(
            summary["support_counts"],
            {"after_graph_confirmed": 65, "source_arrow_only": 21},
        )
        self.assertEqual(sum(
            len(row["candidate"]["source_flow_bindings"])
            for row in self.catalog["candidates"]
        ), 43)
        self.assertFalse(self.catalog["scope"]["events_are_reviewed_evidence"])
        self.assertFalse(
            self.catalog["scope"]["shared_signature_implies_mechanism_equivalence"]
        )

        for row in self.catalog["candidates"]:
            candidate = row["candidate"]
            edits = candidate["proposed_graph_edits"]
            self.assertEqual(row["event_count"], len(edits))
            self.assertEqual(row["event_count"], len(row["events"]))
            self.assertEqual(
                row["candidate_sha256"],
                hashlib.sha256(canonical_bytes(candidate)).hexdigest(),
            )
            self.assertEqual(
                [event["edit_id"] for event in row["events"]],
                [edit["edit_id"] for edit in edits],
            )
            self.assertEqual(
                [event["source_edit"] for event in row["events"]], edits
            )
            self.assertEqual(candidate["status"], "unreviewed")
            self.assertFalse(candidate["scope_effect"]["reviewed_evidence"])
            self.assertFalse(candidate["scope_effect"]["physical_atom_map"])
            self.assertFalse(candidate["scope_effect"]["experimentally_validated"])
            self.assertTrue(candidate["scope_effect"]["opaque_annotations_preserved"])

    def test_real_queries_require_all_clauses_inside_one_candidate(self):
        cc = query_candidate_events(self.catalog, clauses=[CC_ADD])
        self.assertEqual(
            self.binding_tuples(cc),
            [("M0219", 1, 2), ("M0219", 1, 4)],
        )
        self.assertEqual(cc["matched_witness_count"], 2)

        narrowed = query_candidate_events(
            self.catalog, clauses=[CC_ADD, C_NEUTRALIZE]
        )
        self.assertEqual(self.binding_tuples(narrowed), [("M0219", 1, 2)])
        self.assertEqual(narrowed["matched_witness_count"], 2)

        # M0106 has these literal signatures in different adjacent-panel
        # candidates. They must not join through their shared record context.
        false_join = query_candidate_events(
            self.catalog,
            mcsa_id="m0106",
            support="any",
            clauses=[
                {"kind": "bond", "elements": ["C", "H"], "before": 0, "after": 1},
                OH_ADD,
            ],
        )
        self.assertEqual(false_join["candidate_count"], 0)
        self.assertEqual(false_join["matches"], [])
        self.assertEqual(false_join["filters"]["mcsa_id"], "M0106")
        self.assertEqual(
            false_join["query_semantics"]["clause_combination"],
            "all_clauses_within_one_candidate",
        )
        self.assertFalse(false_join["query_semantics"]["clauses_imply_shared_atoms"])
        self.assertEqual(
            false_join["query_semantics"]["empty_result"],
            "no_matching_candidate_event_not_absence_of_chemistry",
        )

    def test_support_filters_preserve_duplicate_signature_witnesses(self):
        confirmed = query_candidate_events(self.catalog)
        self.assertEqual(confirmed["candidate_count"], 12)
        self.assertEqual(confirmed["selected_support_event_count"], 65)
        self.assertEqual(confirmed["matched_witness_count"], 0)

        arrow_rows = query_candidate_events(
            self.catalog, clauses=[OH_ADD], support="source_arrow_only"
        )
        self.assertEqual(arrow_rows["candidate_count"], 4)
        self.assertEqual(arrow_rows["matched_witness_count"], 5)
        m0212 = next(
            match for match in arrow_rows["matches"]
            if match["candidate_row"]["candidate"]["source_binding"]["record_id"] == "M0212"
        )
        self.assertEqual(
            m0212["candidate_row"]["candidate"]["source_binding"]["before_step_id"], 15
        )
        witnesses = m0212["clause_witnesses"][0]["events"]
        self.assertEqual([event["edit_id"] for event in witnesses], ["e2", "e5"])
        self.assertTrue(all(event["support"] == "source_arrow_only" for event in witnesses))

        any_rows = query_candidate_events(self.catalog, clauses=[OH_ADD], support="any")
        self.assertEqual(any_rows["candidate_count"], 6)
        self.assertEqual(any_rows["matched_witness_count"], 7)
        confirmed_rows = query_candidate_events(self.catalog, clauses=[OH_ADD])
        self.assertEqual(
            self.binding_tuples(confirmed_rows),
            [("M0219", 1, 2), ("M0219", 1, 4)],
        )

    def test_duplicate_and_reversed_bond_clauses_have_set_semantics(self):
        normalized = query_candidate_events(
            self.catalog,
            clauses=[
                {"kind": "bond", "elements": ["C", "C"], "before": 0, "after": 1},
                {"kind": "bond", "elements": ["C", "C"], "before": 0, "after": 1},
            ],
        )
        reversed_elements = query_candidate_events(
            self.catalog,
            clauses=[{"kind": "bond", "elements": ["O", "C"], "before": 2, "after": 1}],
        )
        forward_elements = query_candidate_events(
            self.catalog,
            clauses=[{"kind": "bond", "elements": ["C", "O"], "before": 2, "after": 1}],
        )
        self.assertEqual(normalized["filters"]["clauses"], [CC_ADD])
        self.assertEqual(
            self.binding_tuples(reversed_elements), self.binding_tuples(forward_elements)
        )

    def test_atom_id_and_row_order_changes_do_not_change_event_queries(self):
        candidates, provenance = self.catalog_inputs()
        candidates.reverse()
        provenance["candidate_contexts"].reverse()
        reordered = build_candidate_event_catalog(candidates, provenance=provenance)

        target = next(
            index for index, candidate in enumerate(candidates)
            if candidate["source_binding"]["record_id"] == "M0219"
            and candidate["source_binding"]["before_step_id"] == 2
        )
        candidates[target] = self.rename_atom_ids(candidates[target])
        self.rebind_candidate(provenance, target, candidates[target])
        renamed = build_candidate_event_catalog(candidates, provenance=provenance)

        baseline = query_candidate_events(
            self.catalog, clauses=[CC_ADD, C_NEUTRALIZE]
        )
        for changed in (reordered, renamed):
            result = query_candidate_events(changed, clauses=[CC_ADD, C_NEUTRALIZE])
            self.assertEqual(set(self.binding_tuples(result)), set(self.binding_tuples(baseline)))
            self.assertEqual(result["matched_witness_count"], baseline["matched_witness_count"])
        self.assertNotEqual(canonical_bytes(renamed), canonical_bytes(self.catalog))

    def test_event_index_is_sensitive_to_source_candidate_chemistry(self):
        candidates, provenance = self.catalog_inputs()
        target = next(
            index for index, candidate in enumerate(candidates)
            if candidate["source_binding"]["record_id"] == "M0219"
            and candidate["source_binding"]["before_step_id"] == 2
        )
        for graph_name in ("before_graph", "after_graph"):
            atom = next(
                row for row in candidates[target]["source_panels"][graph_name]["atoms"]
                if row["atom_id"] == "a10"
            )
            atom["element"] = "N"
        self.rebind_candidate(provenance, target, candidates[target])
        changed = build_candidate_event_catalog(candidates, provenance=provenance)
        signatures = {
            event["edit_id"]: event["signature"]
            for event in changed["candidates"][target]["events"]
        }
        self.assertEqual(signatures["e11"]["elements"], ["C", "N"])
        self.assertEqual(signatures["e12"]["elements"], ["N"])
        self.assertEqual(
            query_candidate_events(
                changed, clauses=[CC_ADD, C_NEUTRALIZE]
            )["candidate_count"],
            0,
        )

        for field, replacement in (
            ("elements", ["C", "N"]),
            ("before", 1),
            ("after", 2),
        ):
            stale = copy.deepcopy(self.catalog)
            stale["candidates"][5]["events"][10]["signature"][field] = replacement
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_candidate_event_catalog(stale)

    def test_query_result_is_a_deep_copy_of_catalog_and_context(self):
        original = canonical_bytes(self.catalog)
        result = query_candidate_events(self.catalog, clauses=[CC_ADD])
        result["provenance"]["context_scan"]["path"] = "changed.json"
        result["matches"][0]["candidate_row"]["source_context"]["source_scope"] = "changed"
        result["matches"][0]["eligible_support_events"][0]["source_edit"]["atom_ids"][0] = "changed"
        result["matches"][0]["clause_witnesses"][0]["events"].clear()
        self.assertEqual(canonical_bytes(self.catalog), original)

    def test_invalid_clauses_and_filters_fail_as_value_errors(self):
        invalid_clauses = [
            {"kind": [], "elements": ["C", "C"], "before": 0, "after": 1},
            {"kind": {}, "elements": ["C", "C"], "before": 0, "after": 1},
            {"kind": "bond", "elements": ["C"], "before": 0, "after": 1},
            {"kind": "charge", "elements": ["C", "O"], "before": -1, "after": 0},
            {"kind": "bond", "elements": ["R", "C"], "before": 0, "after": 1},
            {"kind": "bond", "elements": ["*", "C"], "before": 0, "after": 1},
            {"kind": "bond", "elements": ["Qq", "C"], "before": 0, "after": 1},
            {"kind": "bond", "elements": ["c", "C"], "before": 0, "after": 1},
            {"kind": "bond", "elements": ["C", "C"], "before": True, "after": 1},
            {"kind": "bond", "elements": ["C", "C"], "before": "NaN", "after": 1},
            {"kind": "bond", "elements": ["C", "C"], "before": 0, "after": 4},
            {"kind": "charge", "elements": ["C"], "before": 0, "after": 0},
        ]
        for clause in invalid_clauses:
            with self.subTest(clause=clause), self.assertRaises(ValueError):
                query_candidate_events(self.catalog, clauses=[clause])
        for clauses in ({}, "bond"):
            with self.subTest(clauses=clauses), self.assertRaises(ValueError):
                query_candidate_events(self.catalog, clauses=clauses)
        for support in (True, "reviewed"):
            with self.subTest(support=support), self.assertRaises(ValueError):
                query_candidate_events(self.catalog, support=support)
        for mcsa_id in (True, "M0219-any"):
            with self.subTest(mcsa_id=mcsa_id), self.assertRaises(ValueError):
                query_candidate_events(self.catalog, mcsa_id=mcsa_id)
        with self.assertRaises(ValueError):
            canonical_bytes(float("nan"))

    def test_catalog_tampering_scope_promotion_and_context_false_join_reject(self):
        for mutate in (
            lambda value: value.__setitem__("event_count", value["event_count"] + 1),
            lambda value: value["candidates"][0]["events"][0]["signature"].__setitem__("after", 2),
            lambda value: value["candidates"][0]["candidate"]["source_binding"].__setitem__("record_id", "M0219"),
        ):
            changed = copy.deepcopy(self.catalog)
            mutate(changed)
            with self.assertRaises(ValueError):
                validate_candidate_event_catalog(changed)

        candidates, provenance = self.catalog_inputs()
        candidates[0]["scope_effect"]["physical_atom_map"] = True
        self.rebind_candidate(provenance, 0, candidates[0])
        with self.assertRaisesRegex(ValueError, "scope"):
            build_candidate_event_catalog(candidates, provenance=provenance)

        candidates, provenance = self.catalog_inputs()
        provenance["candidate_contexts"][0]["source_context"]["record_binding"][
            "mcsa_id"
        ] = "M0219"
        provenance["candidate_contexts"][0]["source_context_sha256"] = hashlib.sha256(
            canonical_bytes(provenance["candidate_contexts"][0]["source_context"])
        ).hexdigest()
        with self.assertRaisesRegex(ValueError, "record differs"):
            build_candidate_event_catalog(candidates, provenance=provenance)


if __name__ == "__main__":
    unittest.main()
