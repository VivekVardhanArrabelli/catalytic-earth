from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.progress import (
    WorkEntry,
    append_work_entry,
    build_progress_report,
    load_work_entries,
)


class ProgressTests(unittest.TestCase):
    def test_log_round_trip_and_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "progress.jsonl"
            entry = WorkEntry.create(
                stage="v0",
                task="test progress logging",
                minutes=12,
                artifacts=["work/status.md"],
                evidence=["tests pass"],
                expectation_update="timeline adjusted from evidence",
            )
            append_work_entry(entry, path)
            entries = load_work_entries(path)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0].minutes, 12)

            report = build_progress_report(entries)
            self.assertIn("Estimated/planned time: 12 minutes", report)
            self.assertIn("timeline adjusted", report)

    def test_negative_minutes_rejected(self) -> None:
        with self.assertRaises(ValueError):
            WorkEntry.create(stage="v0", task="bad", minutes=-1, artifacts=[], evidence=[])

    def test_measured_time_from_start_end(self) -> None:
        entry = WorkEntry.create(
            stage="ops",
            task="measured",
            minutes=0,
            artifacts=[],
            evidence=[],
            time_mode="measured",
            started_at="2026-05-09T10:00:00+00:00",
            ended_at="2026-05-09T10:34:00+00:00",
        )
        self.assertEqual(entry.measured_minutes, 34.0)
        report = build_progress_report([entry])
        self.assertIn("Measured elapsed time: 34.0 minutes", report)


if __name__ == "__main__":
    unittest.main()
