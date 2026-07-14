from __future__ import annotations

import unittest

from catalytic_earth.lineage_quarantine import assert_lineage_edge_accounted_for


class LineageQuarantineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.quarantine = {
            "rows": [
                {
                    "artifact_path": "artifacts/downstream.json",
                    "edge_id": "input",
                    "source_path": "artifacts/upstream.json",
                    "recorded_source_sha256": "a" * 64,
                    "observed_source_sha256": "b" * 64,
                    "release_eligible": False,
                    "disposition": "historical_only_regenerate_do_not_rehash",
                }
            ]
        }

    def test_current_edge_needs_no_quarantine(self) -> None:
        status = assert_lineage_edge_accounted_for(
            self.quarantine,
            artifact_path="artifacts/current.json",
            edge_id="input",
            source_path="artifacts/source.json",
            recorded_sha256="c" * 64,
            observed_sha256="c" * 64,
        )
        self.assertEqual(status, "current")

    def test_exact_historical_edge_is_quarantined(self) -> None:
        status = assert_lineage_edge_accounted_for(
            self.quarantine,
            artifact_path="artifacts/downstream.json",
            edge_id="input",
            source_path="artifacts/upstream.json",
            recorded_sha256="a" * 64,
            observed_sha256="b" * 64,
        )
        self.assertEqual(status, "quarantined")

    def test_unaccounted_mismatch_fails_closed(self) -> None:
        with self.assertRaisesRegex(AssertionError, "unaccounted lineage mismatch"):
            assert_lineage_edge_accounted_for(
                self.quarantine,
                artifact_path="artifacts/downstream.json",
                edge_id="input",
                source_path="artifacts/upstream.json",
                recorded_sha256="a" * 64,
                observed_sha256="d" * 64,
            )


if __name__ == "__main__":
    unittest.main()
