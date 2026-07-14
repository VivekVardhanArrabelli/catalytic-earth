from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ATLAS_ROOT = ROOT / "data/atlas/atlas10"


class Atlas10ComparatorAndReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.baseline = json.loads(
            (ATLAS_ROOT / "comparator/unintegrated_source_stack.json").read_text(
                encoding="utf-8"
            )
        )
        cls.comparison = json.loads(
            (ATLAS_ROOT / "comparator/atlas_vs_unintegrated.json").read_text(
                encoding="utf-8"
            )
        )
        cls.manifest = json.loads(
            (ATLAS_ROOT / "review/packet_manifest.json").read_text(encoding="utf-8")
        )
        cls.ledger = json.loads(
            (ATLAS_ROOT / "review/review_attempts.json").read_text(encoding="utf-8")
        )

    def test_baseline_used_no_atlas_output_and_same_frozen_source_budget(self) -> None:
        self.assertEqual(self.baseline["input_bindings"]["atlas_outputs_used"], [])
        self.assertEqual(
            self.baseline["same_source_budget"]["external_requests_acquisition"], 64
        )
        self.assertEqual(self.baseline["same_source_budget"]["external_requests_replay"], 0)
        self.assertFalse(self.baseline["same_source_budget"]["network_used_during_replay"])
        self.assertEqual(len(self.baseline["unintegrated_case_source_rows"]), 7)

    def test_comparator_does_not_fabricate_timing_or_accuracy(self) -> None:
        timing = self.comparison["measurements"]["elapsed_human_minutes"]
        self.assertIsNone(timing["baseline"])
        self.assertIsNone(timing["atlas"])
        self.assertIsNone(timing["speedup_claim"])
        self.assertIsNone(
            self.comparison["measurements"]["applicability_errors"]["atlas"]
        )
        completeness = self.comparison["measurements"]["query_answer_completeness"]
        self.assertEqual(completeness["baseline_mean_fraction"], 0.6875)
        self.assertEqual(completeness["atlas_mean_fraction"], 1.0)
        self.assertIn("not biological correctness", completeness["interpretation"])

    def test_review_packet_hashes_and_count_match_manifest(self) -> None:
        self.assertEqual(self.manifest["packet_count"], 7)
        self.assertGreaterEqual(self.manifest["packet_count"], 5)
        self.assertLessEqual(self.manifest["packet_count"], 10)
        for row in self.manifest["packets"]:
            json_path = ROOT / row["json_path"]
            markdown_path = ROOT / row["markdown_path"]
            self.assertEqual(hashlib.sha256(json_path.read_bytes()).hexdigest(), row["json_sha256"])
            self.assertEqual(
                hashlib.sha256(markdown_path.read_bytes()).hexdigest(),
                row["markdown_sha256"],
            )

    def test_unattempted_review_ledger_claims_no_outreach_or_review(self) -> None:
        self.assertEqual(self.ledger["status"], "external_review_attempt_gate_pending")
        self.assertEqual(len(self.ledger["attempts"]), 7)
        for attempt in self.ledger["attempts"]:
            self.assertEqual(
                attempt["status"], "not_attempted_missing_reviewer_channel"
            )
            self.assertIsNone(attempt["attempted_at"])
            self.assertIsNone(attempt["channel"])
            self.assertIsNone(attempt["recipient"])
            self.assertIsNone(attempt["request_reference"])
            self.assertFalse(attempt["independent_review_completed"])

    def test_cyclophilin_review_packet_preserves_zero_steps(self) -> None:
        row = next(
            item
            for item in self.manifest["packets"]
            if item["case_id"] == "atlas10.cyclophilin-a-human.isomerization"
        )
        packet = json.loads((ROOT / row["json_path"]).read_text(encoding="utf-8"))
        self.assertEqual(packet["source_proposals"][0]["steps"], [])
        self.assertEqual(
            packet["source_proposals"][0]["scheme_retrieval_issues"][0]["status"],
            "source_link_missing_http_404",
        )
        self.assertTrue(packet["detail_abstention"]["required"])


if __name__ == "__main__":
    unittest.main()
