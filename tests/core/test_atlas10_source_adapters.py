from __future__ import annotations

import json
import unittest
from pathlib import Path

from catalytic_earth.atlas10_source_adapters import (
    parse_mcsa_scheme_flows,
    read_atlas10_mcsa_snapshot,
    read_atlas10_rhea_snapshot,
)


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = ROOT / "data/atlas/atlas10/sources"


class Atlas10SourceAdapterTests(unittest.TestCase):
    def test_direct_rhea_macromolecule_and_reactive_parts_both_resolve(self) -> None:
        reaction = read_atlas10_rhea_snapshot(
            SOURCE_ROOT / "rhea/RHEA_16237.json",
            "RHEA:16237",
            selected_participant_ids={
                "CHEBI:83834",
                "CHEBI:83833",
                "RHEA-COMP:10747",
                "RHEA-COMP:10748",
            },
        )
        self.assertEqual(reaction["source_status"], "direct_record")
        self.assertEqual(len(reaction["participants"]), 2)
        self.assertTrue(
            all(item["participant_type"] == "macromolecule" for item in reaction["participants"])
        )

    def test_zero_row_query_stays_a_gap(self) -> None:
        reaction = read_atlas10_rhea_snapshot(
            SOURCE_ROOT / "rhea/EC_3_4_21_4.query-gap.json",
            "EC:3.4.21.4",
            selected_participant_ids={"CHEBI:15377", "CHEBI:90799", "CHEBI:59869"},
        )
        self.assertEqual(reaction["source_status"], "documented_query_gap")
        self.assertIsNone(reaction["source_record_id"])
        self.assertEqual(reaction["participants"], [])

    def test_all_detailed_non_product_steps_preserve_source_curved_arrows(self) -> None:
        flow_count = 0
        step_count = 0
        for path in sorted((SOURCE_ROOT / "mcsa").glob("M*.json")):
            entry = read_atlas10_mcsa_snapshot(path, path.stem)
            for mechanism in entry["mechanisms"]:
                if not mechanism["is_detailed"]:
                    continue
                for step in mechanism["steps"]:
                    if step["is_product"]:
                        continue
                    parsed = parse_mcsa_scheme_flows(
                        entry["scheme_index"][(mechanism["mechanism_id"], step["step_id"])]
                    )
                    self.assertEqual(parsed["scheme_status"], "source_curved_arrows_preserved")
                    self.assertGreater(len(parsed["electron_flows"]), 0)
                    step_count += 1
                    flow_count += len(parsed["electron_flows"])
        self.assertEqual(step_count, 21)
        self.assertEqual(flow_count, 61)

    def test_cyclophilin_non_detailed_scheme_404_never_becomes_a_step(self) -> None:
        entry = read_atlas10_mcsa_snapshot(SOURCE_ROOT / "mcsa/M0189.json", "M0189")
        mechanism = entry["mechanisms"][0]
        self.assertIs(mechanism["is_detailed"], False)
        parsed = parse_mcsa_scheme_flows(entry["scheme_index"][(1, 1)])
        self.assertEqual(parsed["scheme_status"], "source_link_missing_http_404")
        self.assertEqual(parsed["electron_flows"], [])


if __name__ == "__main__":
    unittest.main()
