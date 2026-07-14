from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas50_phase_a import (
    PHASE_RELATIVE,
    build_phase_a_outputs,
    canonical_json_bytes,
    validate_blocker_report,
    validate_candidate_matrix,
    validate_crosswalk,
    validate_inherited_baseline,
    validate_phase_a_package,
    validate_proposal,
)


ROOT = Path(__file__).resolve().parents[2]
PHASE = ROOT / PHASE_RELATIVE


def _load(name: str) -> dict:
    return json.loads((PHASE / name).read_text(encoding="utf-8"))


class Atlas50PhaseATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = json.loads(
            (ROOT / "data/registries/mechanism_fingerprints.json").read_text(
                encoding="utf-8"
            )
        )
        cls.crosswalk = _load("crosswalk_draft.json")
        cls.matrix = _load("candidate_matrix.json")
        cls.proposal = _load("proposed_panel.json")
        cls.blockers = _load("blocker_report.json")

    def test_repository_package_is_byte_current_and_fail_closed(self) -> None:
        summary = validate_phase_a_package(ROOT)

        self.assertEqual(summary["crosswalk_rows"], 57)
        self.assertEqual(summary["candidate_rows"], 40)
        self.assertEqual(summary["proposed_additions"], 37)
        self.assertEqual(summary["proposed_total"], 47)
        self.assertEqual(summary["blockers"], 3)
        self.assertEqual(summary["projection_percentage"], 94.0)
        self.assertEqual(summary["reviewed_crosswalk_rows"], 0)
        self.assertEqual(summary["compiled_follow_on_mechanisms"], 0)
        self.assertEqual(summary["gpu_hours"], 0)

    def test_all_57_registry_rows_remain_explicitly_unreviewed(self) -> None:
        counts = validate_crosswalk(self.crosswalk, self.registry)

        self.assertEqual(len(self.crosswalk["rows"]), 57)
        self.assertEqual(
            [row["fingerprint_id"] for row in self.crosswalk["rows"]],
            [row["id"] for row in self.registry],
        )
        self.assertEqual({row["review_status"] for row in self.crosswalk["rows"]}, {"unreviewed"})
        self.assertEqual(counts["exact_duplicate"], 1)
        self.assertEqual(counts["genuinely_missing_concept"], 0)
        for row in self.crosswalk["rows"]:
            self.assertEqual(len(row["source_links"]), 13)
            for link in row["source_links"].values():
                self.assertTrue(link["records"] or link["uris"] or link["gap_reason"])
                self.assertEqual(
                    link["mapping_assertion"], "none_unreviewed_candidate_only"
                )

    def test_candidate_matrix_preserves_gaps_abstention_and_blockers(self) -> None:
        validate_candidate_matrix(self.matrix)

        excluded = [
            row for row in self.matrix["rows"] if row["decision"] == "exclude_blocked"
        ]
        self.assertEqual(
            [row["source_identity"]["mcsa_id"] for row in excluded],
            ["M0212", "M0753", "M0970"],
        )
        non_detailed = [
            row
            for row in self.matrix["rows"]
            if row["source_identity"]["annotation_level"] == "non_detailed"
        ]
        self.assertEqual(
            [row["source_identity"]["mcsa_id"] for row in non_detailed],
            ["M0767", "M0851", "M0935"],
        )
        for row in non_detailed:
            abstentions = row["expected_object_tiers"]["mandatory_abstentions"]
            self.assertGreaterEqual(len(abstentions), 2)
            self.assertFalse(row["mechanism_compiled"])

    def test_proposal_is_projection_not_section_10_2_completion(self) -> None:
        validate_proposal(self.proposal)
        validate_blocker_report(self.blockers, self.matrix)

        projection = self.proposal["representation_projection"]
        self.assertEqual(projection["denominator_case_count"], 50)
        self.assertEqual(
            projection["projected_representable_without_family_specific_ad_hoc_fields"],
            47,
        )
        self.assertEqual(projection["projected_percentage"], 94.0)
        self.assertFalse(projection["final_section_10_2_result"])
        self.assertEqual(self.proposal["proposed_panel"]["shortfall_from_50"], 3)
        self.assertFalse(self.proposal["proposed_panel"]["forty_additions_emitted"])

    def test_inherited_atlas_and_registry_objects_are_unchanged(self) -> None:
        summary = validate_inherited_baseline(ROOT)

        self.assertEqual(summary["scopes"], 9)
        self.assertEqual(summary["inherited_files"], 96)
        self.assertEqual(summary["protected_registries"], 4)

    def test_builder_is_deterministic_against_committed_outputs(self) -> None:
        expected = build_phase_a_outputs(ROOT)

        for filename, value in expected.items():
            self.assertEqual((PHASE / filename).read_bytes(), canonical_json_bytes(value))

    def test_review_status_cannot_be_upgraded_by_edit(self) -> None:
        changed = copy.deepcopy(self.crosswalk)
        changed["rows"][0]["review_status"] = "reviewed"

        with self.assertRaisesRegex(ValueError, "cannot be reviewed"):
            validate_crosswalk(changed, self.registry)

    def test_compiled_mechanism_fields_are_rejected(self) -> None:
        changed = copy.deepcopy(self.matrix)
        changed["rows"][0]["mechanism_steps"] = [{"invented": True}]

        with self.assertRaisesRegex(ValueError, "prohibited compiled fields"):
            validate_candidate_matrix(changed)

    def test_projection_cannot_be_promoted_to_final_result(self) -> None:
        changed = copy.deepcopy(self.proposal)
        changed["representation_projection"]["final_section_10_2_result"] = True

        with self.assertRaisesRegex(ValueError, "cannot claim final"):
            validate_proposal(changed)

    def test_inherited_atlas10_hash_cannot_change(self) -> None:
        changed = copy.deepcopy(self.proposal)
        changed["inherited_atlas10"]["selection_sha256"] = "0" * 64

        with self.assertRaisesRegex(ValueError, "changed Atlas-10 hash"):
            validate_proposal(changed)

    def test_blocker_cannot_be_resolved_for_convenience(self) -> None:
        changed = copy.deepcopy(self.blockers)
        changed["blockers"][0]["convenience_choice_made"] = True

        with self.assertRaisesRegex(ValueError, "cannot be resolved by convenience"):
            validate_blocker_report(changed, self.matrix)


if __name__ == "__main__":
    unittest.main()
