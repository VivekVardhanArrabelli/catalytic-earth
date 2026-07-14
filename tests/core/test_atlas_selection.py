from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from catalytic_earth.atlas_selection import (
    CASE_EXPECTATIONS,
    SELECTION_AXES,
    validate_atlas3_selection,
)


ROOT = Path(__file__).resolve().parents[2]
SELECTION = ROOT / "data/atlas/atlas3_selection.json"


class AtlasSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.selection = json.loads(SELECTION.read_text(encoding="utf-8"))

    def test_repository_selection_is_the_frozen_three_case_kernel(self) -> None:
        summary = validate_atlas3_selection(self.selection)

        self.assertEqual(summary["cases"], 3)
        self.assertEqual(summary["authoritative_source_handles"], 18)
        self.assertEqual(summary["assay_candidates"], 1)
        self.assertEqual(summary["gpu_hours_max"], 0)
        self.assertEqual(
            summary["selection_sha256"],
            "d24361bb9fc000d39d7209c5538bd23df845a94aa2dce1fb38c18d56dd8e1ada",
        )
        self.assertEqual(
            [case["representation_axis"] for case in self.selection["cases"]],
            list(SELECTION_AXES),
        )
        self.assertEqual(
            {case["case_id"] for case in self.selection["cases"]},
            set(CASE_EXPECTATIONS),
        )

    def test_selection_cannot_authorize_registry_mutation(self) -> None:
        changed = copy.deepcopy(self.selection)
        changed["registry_mutation_permitted"] = True

        with self.assertRaisesRegex(ValueError, "registry mutation"):
            validate_atlas3_selection(changed)

    def test_frozen_authoritative_handle_cannot_be_swapped(self) -> None:
        changed = copy.deepcopy(self.selection)
        changed["cases"][0]["source_handles"][0]["record_id"] = "P22033"
        changed["cases"][0]["source_handles"][0]["uri"] = (
            "https://www.uniprot.org/uniprotkb/P22033/entry"
        )

        with self.assertRaisesRegex(ValueError, "frozen authoritative set"):
            validate_atlas3_selection(changed)

    def test_mn_sod_mcsa_handle_is_counterevidence_not_a_mechanism_transfer(self) -> None:
        changed = copy.deepcopy(self.selection)
        mn_sod = next(
            case
            for case in changed["cases"]
            if case["case_id"] == "atlas3.mnsod-ecoli.redox"
        )
        mcsa = next(
            handle for handle in mn_sod["source_handles"] if handle["source_id"] == "M-CSA"
        )
        mcsa["evidence_role"] = "source_mechanism"
        mcsa["applicability"] = "direct"

        with self.assertRaisesRegex(ValueError, "frozen authoritative set"):
            validate_atlas3_selection(changed)

    def test_assay_lane_is_candidate_only_and_unique(self) -> None:
        changed = copy.deepcopy(self.selection)
        changed["cases"][0]["assay_candidate"] = True

        with self.assertRaisesRegex(ValueError, "exactly one assay candidate"):
            validate_atlas3_selection(changed)

        changed = copy.deepcopy(self.selection)
        changed["assay_lane"]["materials_committed"] = True
        with self.assertRaisesRegex(ValueError, "materials_committed"):
            validate_atlas3_selection(changed)


if __name__ == "__main__":
    unittest.main()
