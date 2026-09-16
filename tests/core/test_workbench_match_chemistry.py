"""Checks for the matched-chemistry projection.

The viewer must draw what the matcher actually returned: the retained source
panels, the assignment's own atoms, and the edits that witness each clause. It
must not synthesise a graph, place an atom the record does not place, or let a
pattern match read as reviewed evidence.
"""

from __future__ import annotations

import unittest

from catalytic_earth.workbench.adapter import AdapterError, match_chemistry_view

CANDIDATE = "panel-context-candidate:M0219:mechanism-1:steps-2-3"
CC_ADD = {
    "kind": "bond", "elements": ["C", "C"], "variables": ["x", "y"],
    "before": 0, "after": 1,
}
C_NEUTRALIZE_X = {
    "kind": "charge", "elements": ["C"], "variables": ["x"],
    "before": -1, "after": 0,
}


class ProjectionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.view = match_chemistry_view([CC_ADD, C_NEUTRALIZE_X], CANDIDATE)

    def test_both_retained_panels_are_projected(self) -> None:
        for side in ("before", "after"):
            panel = self.view["panels"][side]
            self.assertTrue(panel["atoms"], side)
            self.assertTrue(panel["bonds"], side)

    def test_coordinates_are_retained_not_computed(self) -> None:
        for side in ("before", "after"):
            semantics = self.view["panels"][side]["coordinate_semantics"]
            self.assertEqual(
                semantics["kind"], "retained_source_panel_depiction_coordinates"
            )
            self.assertIn("not measured molecular geometry", semantics["note"])

    def test_no_atom_is_given_an_invented_position(self) -> None:
        for side in ("before", "after"):
            panel = self.view["panels"][side]
            placed = set(panel["coordinates"])
            listed = {atom["atom_id"] for atom in panel["atoms"]}
            unplaced = set(panel["unplaced_atom_ids"])
            # Every atom is either placed from the record or reported unplaced.
            self.assertEqual(placed | unplaced, listed, side)
            self.assertEqual(placed & unplaced, set(), side)

    def test_the_assignment_comes_from_the_matcher(self) -> None:
        self.assertEqual(
            self.view["assignment"]["atom_bindings"], {"x": "a10", "y": "a28"}
        )
        self.assertEqual(self.view["assignment"]["of"], 1)

    def test_each_clause_names_its_witness_edits(self) -> None:
        witnesses = self.view["clause_witnesses"]
        self.assertEqual(len(witnesses), 2)
        for witness in witnesses:
            self.assertTrue(witness["edits"])
            for edit in witness["edits"]:
                self.assertTrue(edit["edit_id"])
                self.assertIn(
                    edit["support"], {"after_graph_confirmed", "source_arrow_only"}
                )

    def test_witness_edits_touch_the_bound_atoms(self) -> None:
        bound = set(self.view["assignment"]["atom_bindings"].values())
        for witness in self.view["clause_witnesses"]:
            for edit in witness["edits"]:
                self.assertTrue(
                    bound & set(edit["atom_ids"]),
                    f"{edit['edit_id']} does not touch the assignment",
                )

    def test_every_edit_carries_its_support_state(self) -> None:
        self.assertTrue(self.view["edits"])
        for edit in self.view["edits"]:
            self.assertIn(
                edit["support"], {"after_graph_confirmed", "source_arrow_only"}
            )
            self.assertIsInstance(edit["after_graph_verified"], bool)
            self.assertIsInstance(edit["is_witness"], bool)

    def test_the_candidate_is_not_presented_as_reviewed(self) -> None:
        provenance = self.view["provenance"]
        self.assertEqual(provenance["review_status"], "unreviewed")
        self.assertIn("not one of the reviewed", provenance["not_a_reviewed_transformation"])
        self.assertFalse(self.view["scope_effect"]["experimentally_validated"])
        self.assertFalse(self.view["scope_effect"]["reviewed_evidence"])
        self.assertFalse(self.view["scope_effect"]["physical_atom_map"])

    def test_correspondence_is_carried_with_its_meaning(self) -> None:
        correspondence = self.view["correspondence"]
        self.assertTrue(correspondence["method"])
        self.assertEqual(
            correspondence["interpretation"],
            "project_unreviewed_panel_alignment_not_physical_atom_map",
        )

    def test_coverage_and_opaque_context_survive(self) -> None:
        self.assertIn("mapped_node_count", self.view["coverage"])
        self.assertIn("before", self.view["opaque_source_context"])
        self.assertIn("after", self.view["opaque_source_context"])


class AssignmentSelectionTest(unittest.TestCase):
    def test_symmetric_assignments_are_selectable_and_labelled(self) -> None:
        # The bond-only query returns several assignments per candidate.
        first = match_chemistry_view([CC_ADD], CANDIDATE, binding_index=0)
        self.assertGreater(first["assignment"]["of"], 1)
        second = match_chemistry_view(
            [CC_ADD], CANDIDATE, binding_index=first["assignment"]["of"] - 1
        )
        self.assertNotEqual(
            first["assignment"]["atom_bindings"], second["assignment"]["atom_bindings"]
        )
        self.assertIn("not more evidence", first["assignment_semantics"]["note"])

    def test_an_assignment_outside_the_returned_set_is_refused(self) -> None:
        with self.assertRaises(AdapterError):
            match_chemistry_view([CC_ADD, C_NEUTRALIZE_X], CANDIDATE, binding_index=99)
        with self.assertRaises(AdapterError):
            match_chemistry_view([CC_ADD, C_NEUTRALIZE_X], CANDIDATE, binding_index=-1)

    def test_a_candidate_outside_the_result_is_refused(self) -> None:
        with self.assertRaises(AdapterError):
            match_chemistry_view([CC_ADD, C_NEUTRALIZE_X], "no-such-candidate")

    def test_a_query_with_no_match_cannot_be_viewed(self) -> None:
        disjoint = [
            {"kind": "bond", "elements": ["C", "O"], "variables": ["x", "y"],
             "before": 2, "after": 1},
            C_NEUTRALIZE_X,
        ]
        with self.assertRaises(AdapterError):
            match_chemistry_view(disjoint, CANDIDATE)

    def test_clause_values_are_still_validated_here(self) -> None:
        with self.assertRaises(AdapterError):
            match_chemistry_view([dict(CC_ADD, before=0.9)], CANDIDATE)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
