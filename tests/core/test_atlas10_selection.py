from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas10_selection import (
    FOLLOW_ON_CASE_IDS,
    FROZEN_SELECTION_SHA256,
    validate_atlas10_selection,
)


ROOT = Path(__file__).resolve().parents[2]
SELECTION = ROOT / "data/atlas/atlas10_selection.json"


class Atlas10SelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.selection = json.loads(SELECTION.read_text(encoding="utf-8"))

    def _case(self, payload: dict, case_id: str) -> dict:
        return next(case for case in payload["follow_on_cases"] if case["case_id"] == case_id)

    def test_repository_selection_is_the_frozen_seven_case_extension(self) -> None:
        summary = validate_atlas10_selection(self.selection)

        self.assertEqual(summary["inherited_cases"], 3)
        self.assertEqual(summary["follow_on_cases"], 7)
        self.assertEqual(summary["total_cases"], 10)
        self.assertEqual(summary["authoritative_source_handles"], 45)
        self.assertEqual(summary["documented_rhea_gaps"], 3)
        self.assertEqual(summary["mandatory_detail_abstentions"], 1)
        self.assertEqual(summary["new_assay_candidates"], 0)
        self.assertEqual(summary["gpu_hours_max"], 0)
        self.assertEqual(summary["selection_sha256"], FROZEN_SELECTION_SHA256)
        self.assertEqual(
            tuple(case["case_id"] for case in self.selection["follow_on_cases"]),
            FOLLOW_ON_CASE_IDS,
        )

    def test_selection_cannot_authorize_registry_mutation(self) -> None:
        changed = copy.deepcopy(self.selection)
        changed["registry_mutation_permitted"] = True

        with self.assertRaisesRegex(ValueError, "registry mutation"):
            validate_atlas10_selection(changed)

    def test_inherited_atlas3_hash_and_cases_are_immutable(self) -> None:
        changed = copy.deepcopy(self.selection)
        changed["inherited_selection"]["selection_sha256"] = "0" * 64

        with self.assertRaisesRegex(ValueError, "frozen Atlas-3"):
            validate_atlas10_selection(changed)

        changed = copy.deepcopy(self.selection)
        changed["all_case_ids"][0] = "atlas3.rewritten"
        with self.assertRaisesRegex(ValueError, "preserve Atlas-3"):
            validate_atlas10_selection(changed)

    def test_cyclophilin_non_detailed_source_cannot_be_upgraded(self) -> None:
        changed = copy.deepcopy(self.selection)
        cyclophilin = self._case(
            changed, "atlas10.cyclophilin-a-human.isomerization"
        )
        cyclophilin["source_mechanism_contract"]["annotation_level"] = "detailed_direct"
        cyclophilin["source_mechanism_contract"]["step_detail_policy"] = (
            "compile_source_steps"
        )

        with self.assertRaisesRegex(ValueError, "source-granularity contract"):
            validate_atlas10_selection(changed)

        changed = copy.deepcopy(self.selection)
        cyclophilin = self._case(
            changed, "atlas10.cyclophilin-a-human.isomerization"
        )
        mcsa = next(
            handle
            for handle in cyclophilin["source_handles"]
            if handle["source_id"] == "M-CSA"
        )
        mcsa["applicability"] = "direct"
        with self.assertRaisesRegex(ValueError, "frozen authoritative set"):
            validate_atlas10_selection(changed)

    def test_subtilisin_engineered_structure_cannot_be_called_direct(self) -> None:
        changed = copy.deepcopy(self.selection)
        subtilisin = self._case(
            changed, "atlas10.subtilisin-bpn-bacillus.serine-protease"
        )
        engineered = next(
            handle
            for handle in subtilisin["source_handles"]
            if handle["record_id"] == "1S01"
        )
        engineered["applicability"] = "direct"

        with self.assertRaisesRegex(ValueError, "cannot be marked direct"):
            validate_atlas10_selection(changed)

        changed = copy.deepcopy(self.selection)
        subtilisin = self._case(
            changed, "atlas10.subtilisin-bpn-bacillus.serine-protease"
        )
        subtilisin["source_handles"] = [
            handle for handle in subtilisin["source_handles"] if handle["record_id"] != "1SUP"
        ]
        with self.assertRaisesRegex(ValueError, "frozen authoritative set"):
            validate_atlas10_selection(changed)

    def test_rhea_source_gap_cannot_be_replaced_with_an_invented_record(self) -> None:
        changed = copy.deepcopy(self.selection)
        lysozyme = self._case(
            changed, "atlas10.hewl-chicken.covalent-glycosidase"
        )
        rhea = next(
            handle for handle in lysozyme["source_handles"] if handle["source_id"] == "Rhea"
        )
        rhea.update(
            {
                "record_id": "RHEA:99999",
                "uri": "https://www.rhea-db.org/rhea/99999",
                "evidence_role": "net_reaction",
                "applicability": "direct",
            }
        )

        with self.assertRaisesRegex(ValueError, "frozen authoritative set"):
            validate_atlas10_selection(changed)

    def test_relationship_pairs_and_query_bindings_are_frozen(self) -> None:
        changed = copy.deepcopy(self.selection)
        changed["relationship_groups"][0]["case_ids"].reverse()

        with self.assertRaisesRegex(ValueError, "frozen pair"):
            validate_atlas10_selection(changed)

        changed = copy.deepcopy(self.selection)
        changed["query_contracts"][1]["relationship_group_id"] = (
            "atlas10.relationship.convergent-serine-proteases"
        )
        with self.assertRaisesRegex(ValueError, "query_id differs"):
            validate_atlas10_selection(changed)

    def test_no_new_assay_candidate_and_case_budgets_fit_phase(self) -> None:
        changed = copy.deepcopy(self.selection)
        changed["follow_on_cases"][0]["assay_candidate"] = True

        with self.assertRaisesRegex(ValueError, "assay_candidate differs"):
            validate_atlas10_selection(changed)

        changed = copy.deepcopy(self.selection)
        changed["phase_compute_budget"]["cpu_hours_max"] = 41
        with self.assertRaisesRegex(ValueError, "ceilings exceed"):
            validate_atlas10_selection(changed)


if __name__ == "__main__":
    unittest.main()
