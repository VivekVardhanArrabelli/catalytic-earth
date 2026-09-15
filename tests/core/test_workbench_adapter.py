"""Offline checks for the Mechanism Workbench adapter and layout.

These tests assert that the Workbench reports what the packaged queries
actually return, and that its honesty labels survive the interface. They add
no scientific claim and regenerate no packaged data.
"""

from __future__ import annotations

import unittest

from catalytic_earth.workbench.adapter import (
    AdapterError,
    evidence_view,
    mechanism_list,
    pattern_query,
    sites_view,
    transformation_view,
)
from catalytic_earth.workbench.layout import compute_layout

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
CO_ORDER_DROP = {
    "kind": "bond",
    "elements": ["C", "O"],
    "variables": ["x", "y"],
    "before": 2,
    "after": 1,
}


class LayoutTest(unittest.TestCase):
    def test_layout_is_deterministic_and_total(self) -> None:
        view = transformation_view("M0187")
        atoms = view["before_graph"]["atoms"]
        bonds = [view["before_graph"]["bonds"], view["after_graph"]["bonds"]]
        first = compute_layout(atoms, bonds)
        second = compute_layout(atoms, bonds)
        self.assertEqual(first["positions"], second["positions"])
        self.assertEqual(
            sorted(first["positions"]), sorted(atom["atom_id"] for atom in atoms)
        )

    def test_layout_never_claims_measured_geometry(self) -> None:
        semantics = transformation_view("M0187")["layout"]["semantics"]
        self.assertFalse(semantics["coordinates_are_measured_geometry"])
        self.assertFalse(semantics["coordinates_are_source_depiction"])
        self.assertEqual(semantics["basis"], "graph_topology_only")
        self.assertIn("not experimentally measured geometry", semantics["note"])


class TransformationViewTest(unittest.TestCase):
    def test_both_mechanisms_use_the_same_code_path(self) -> None:
        self.assertEqual(
            {entry["mcsa_id"] for entry in mechanism_list()["mechanisms"]},
            {"M0187", "M0173"},
        )
        for mcsa_id in ("M0187", "M0173"):
            view = transformation_view(mcsa_id)
            self.assertEqual(view["mechanism"]["mcsa_id"], mcsa_id)
            self.assertTrue(view["edits"])
            self.assertTrue(view["before_graph"]["atoms"])
            self.assertTrue(view["after_graph"]["atoms"])

    def test_edits_match_the_packaged_query(self) -> None:
        from catalytic_earth.atlas_transformation_query import query_transformations
        from catalytic_earth.core_cli import verified_transformations
        import json
        from catalytic_earth.core_cli import ATLAS10_KERNEL, _resource_bytes

        bundle = json.loads(_resource_bytes(ATLAS10_KERNEL))
        for mcsa_id in ("M0187", "M0173"):
            packaged = query_transformations(
                verified_transformations(mcsa_id), atlas10_bundle=bundle, mcsa_id=mcsa_id
            )["transformations"][0]["panel_correspondence"]["graph_edits"]
            served = transformation_view(mcsa_id)["edits"]
            self.assertEqual(len(served), len(packaged))
            for served_edit, packaged_edit in zip(served, packaged):
                for key, value in packaged_edit.items():
                    self.assertEqual(served_edit[key], value)

    def test_replay_is_labelled_symbolic_not_a_trajectory(self) -> None:
        semantics = transformation_view("M0187")["replay_semantics"]
        self.assertIn("molecular_dynamics_trajectory", semantics["not"])
        self.assertIn("observed_turnover", semantics["not"])
        self.assertIn("not a molecular trajectory", semantics["note"])

    def test_abstentions_and_boundaries_reach_the_interface(self) -> None:
        view = transformation_view("M0187")
        self.assertTrue(view["abstentions"])
        self.assertTrue(view["representation_boundaries"])
        self.assertTrue(view["source_bindings"])
        self.assertFalse(view["review"]["human_review_performed"])

    def test_unknown_mechanism_is_refused(self) -> None:
        with self.assertRaises(AdapterError):
            transformation_view("M9999")


class SiteViewTest(unittest.TestCase):
    def test_m0187_changed_atoms_carry_no_direct_site_label(self) -> None:
        view = sites_view("M0187")
        self.assertEqual(view["changed_source_atom_count"], 7)
        self.assertEqual(view["resolved_source_atom_count"], 0)
        self.assertTrue(all(atom["site_id"] is None for atom in view["atoms"]))

    def test_m0173_resolves_only_explicitly_labelled_atoms(self) -> None:
        view = sites_view("M0173")
        self.assertEqual(view["changed_source_atom_count"], 5)
        self.assertEqual(view["resolved_source_atom_count"], 2)
        resolved = {
            atom["source_atom_id"]: atom["site_id"]
            for atom in view["atoms"]
            if atom["site_id"]
        }
        self.assertEqual(resolved, {"a44": "P35049:S204", "a21": "P35049:H65"})

    def test_numbering_systems_stay_distinct(self) -> None:
        atom = next(a for a in sites_view("M0173")["atoms"] if a["source_atom_id"] == "a44")
        context = atom["protein_structure_context"]
        mapping = context["pdb_residue_mappings"][0]
        # UniProt natural position, PDB author position and mmCIF label position
        # are three different numbers for the same residue.
        self.assertEqual(context["sequence_position"], 204)
        self.assertEqual(mapping["author_position"], 195)
        self.assertEqual(mapping["label_position"], 180)
        self.assertEqual(atom["deposited_atom_identity"]["status"], "not_asserted")


class EvidenceViewTest(unittest.TestCase):
    def test_h297n_endpoints_stay_separate(self) -> None:
        view = evidence_view("H297N")
        self.assertEqual(view["matched_observation_count"], 4)
        by_id = {entry["observation_id"]: entry for entry in view["observations"]}

        racemization = by_id["H297N-racemization"]
        self.assertEqual(racemization["endpoint"]["kind"], "turnover")
        self.assertEqual(racemization["result"]["result_class"], "not_detected")

        s_exchange = by_id["H297N-S-exchange"]
        self.assertEqual(s_exchange["endpoint"]["kind"], "isotope_exchange")
        self.assertEqual(s_exchange["result"]["result_class"], "measured")

        r_exchange = by_id["H297N-R-exchange"]
        self.assertEqual(r_exchange["endpoint"]["kind"], "isotope_exchange")
        self.assertEqual(r_exchange["result"]["result_class"], "not_detected")

        # Exchange nondetection for R-mandelate is not the racemization result.
        self.assertNotEqual(
            racemization["endpoint"]["kind"], r_exchange["endpoint"]["kind"]
        )

    def test_fold_value_belongs_to_a_named_comparison(self) -> None:
        observation = next(
            entry
            for entry in evidence_view("H297N")["observations"]
            if entry["observation_id"] == "H297N-S-exchange"
        )
        self.assertEqual(observation["result"]["value"], 3.3)
        self.assertEqual(observation["result"]["unit"], "fold")
        # Not an absolute rate and not a generic activity score: it is a
        # relation against a stated comparator, under stated conditions.
        self.assertEqual(
            observation["result"]["reported_relation"], "fold_lower_than_wild_type"
        )
        self.assertEqual(observation["comparator_variant_id"], "WT")
        conditions = {entry["name"]: entry["value"] for entry in observation["conditions"]}
        self.assertEqual(conditions["pD"], 7.5)
        self.assertEqual(conditions["solvent"], "D2O")

    def test_detection_floors_stay_unknown(self) -> None:
        for observation in evidence_view("H297N")["observations"]:
            if observation["result"]["result_class"] == "not_detected":
                self.assertIsNone(observation["result"]["detection_limit"])
                self.assertIsNone(observation["result"]["value"])

    def test_endpoint_filter_narrows_without_inventing_rows(self) -> None:
        filtered = evidence_view("H297N", "isotope_exchange")
        self.assertEqual(filtered["matched_observation_count"], 2)
        self.assertEqual(
            {entry["endpoint"]["kind"] for entry in filtered["observations"]},
            {"isotope_exchange"},
        )

    def test_fragment_relations_report_their_own_resolution(self) -> None:
        view = evidence_view("H297N")
        relations = {entry["source_atom_id"]: entry for entry in view["relations"]}
        self.assertEqual(view["relation_counts"]["total"], 3)

        his297 = relations["a58"]
        self.assertEqual(his297["site_id"], "P11444:H297")
        self.assertEqual(len(his297["functional_evidence"]["matched_observations"]), 4)

        # The Glu317 step-1 relation remains unresolved.
        self.assertIsNone(relations["a63"]["site_id"])

        # Lys166 resolves to a site but carries no matched H297N observation:
        # it is reference-site context, not a matched control.
        lys166 = relations["a19"]
        self.assertEqual(lys166["site_id"], "P11444:K166")
        self.assertEqual(lys166["functional_evidence"]["matched_observations"], [])
        self.assertEqual(
            lys166["functional_evidence"]["relationship"],
            "reference_site_context_not_exact_assayed_construct",
        )

    def test_retained_depiction_coordinates_are_labelled_as_depiction(self) -> None:
        his297 = next(
            entry
            for entry in evidence_view("H297N")["relations"]
            if entry["source_atom_id"] == "a58"
        )
        retained = his297["retained_depiction_coordinates"]
        self.assertEqual(len(retained["coordinates"]), len(his297["atoms"]))
        self.assertEqual(
            retained["semantics"]["kind"], "retained_source_panel_depiction_coordinates"
        )
        self.assertIn("not measured molecular geometry", retained["semantics"]["note"])

    def test_reference_structure_is_not_a_mutant_structure(self) -> None:
        his297 = next(
            entry
            for entry in evidence_view("H297N")["relations"]
            if entry["source_atom_id"] == "a58"
        )
        structures = his297["protein_structure_context"]["structures"]
        self.assertTrue(structures)
        for structure in structures:
            # The available coordinate context is a reference structure with
            # its own declared limitation, not an H297N mutant structure.
            self.assertTrue(structure["limitation"])
            self.assertIn("static_structure", structure["context_flags"])
        self.assertEqual(
            his297["deposited_atom_identity"]["status"], "not_asserted"
        )


class PatternQueryTest(unittest.TestCase):
    def test_shared_atom_query_matches_one_candidate(self) -> None:
        result = pattern_query([CC_ADD, C_NEUTRALIZE_X])
        self.assertEqual(result["candidate_count"], 1)
        self.assertEqual(result["binding_count"], 1)
        self.assertEqual(result["status"], "unreviewed")
        bindings = result["matches"][0]["bindings"][0]["atom_bindings"]
        self.assertEqual(bindings, {"x": "a10", "y": "a28"})

    def test_disjoint_atom_query_returns_no_match(self) -> None:
        result = pattern_query([CO_ORDER_DROP, C_NEUTRALIZE_X])
        self.assertEqual(result["candidate_count"], 0)
        self.assertEqual(result["binding_count"], 0)
        self.assertEqual(result["matches"], [])

    def test_symmetry_raises_assignments_not_candidates(self) -> None:
        result = pattern_query([CC_ADD])
        self.assertEqual(result["candidate_count"], 2)
        self.assertEqual(result["binding_count"], 4)

    def test_invalid_queries_are_refused(self) -> None:
        with self.assertRaises(AdapterError):
            pattern_query([])
        with self.assertRaises(AdapterError):
            pattern_query([{"kind": "bond", "elements": ["C"], "variables": ["x"],
                            "before": 0, "after": 1}])
        with self.assertRaises(AdapterError):
            pattern_query([CC_ADD], support="not_a_support_level")
        with self.assertRaises(AdapterError):
            pattern_query([dict(CC_ADD, before="x")])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
