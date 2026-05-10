from __future__ import annotations

import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.automation import (
    acquire_automation_lock,
    inspect_automation_lock,
    release_automation_lock,
)


class AutomationLockTests(unittest.TestCase):
    def test_atomic_lock_rejects_fresh_lock(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_dir = Path(tmpdir) / "run.lock"
            first = acquire_automation_lock(lock_dir, started_at="2026-05-10T00:00:00Z")
            self.assertTrue(first.acquired)
            second = acquire_automation_lock(lock_dir, started_at="2026-05-10T00:01:00Z")
            self.assertFalse(second.acquired)
            self.assertEqual(second.status, "active_lock_present")
            self.assertIn("pid", first.as_dict())
            release_automation_lock(lock_dir)
            self.assertFalse(lock_dir.exists())

    def test_status_distinguishes_stale_and_unlocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_dir = Path(tmpdir) / "run.lock"
            unlocked = inspect_automation_lock(lock_dir)
            self.assertEqual(unlocked.status, "unlocked")
            lock_dir.mkdir()
            (lock_dir / "started_at").write_text("2026-05-10T00:00:00Z\n", encoding="utf-8")
            old = datetime.now(timezone.utc) - timedelta(hours=2)
            os.utime(lock_dir, (old.timestamp(), old.timestamp()))
            stale = inspect_automation_lock(lock_dir)
            self.assertEqual(stale.status, "stale_lock_present")

    def test_stale_dirty_lock_requires_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_dir = Path(tmpdir) / "run.lock"
            lock_dir.mkdir()
            (lock_dir / "started_at").write_text("2026-05-10T00:00:00Z\n", encoding="utf-8")
            old = datetime.now(timezone.utc) - timedelta(hours=2)
            os.utime(lock_dir, (old.timestamp(), old.timestamp()))
            result = acquire_automation_lock(
                lock_dir,
                started_at="2026-05-10T02:00:00Z",
                worktree_dirty=True,
            )
            self.assertFalse(result.acquired)
            self.assertEqual(result.status, "stale_lock_dirty_worktree_requires_recovery")
            self.assertTrue(lock_dir.exists())

    def test_stale_clean_lock_is_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_dir = Path(tmpdir) / "run.lock"
            lock_dir.mkdir()
            old = datetime.now(timezone.utc) - timedelta(hours=2)
            os.utime(lock_dir, (old.timestamp(), old.timestamp()))
            result = acquire_automation_lock(
                lock_dir,
                started_at="2026-05-10T02:00:00Z",
                worktree_dirty=False,
            )
            self.assertTrue(result.acquired)
            self.assertEqual(result.status, "stale_lock_replaced")
            self.assertEqual(
                (lock_dir / "started_at").read_text(encoding="utf-8").strip(),
                "2026-05-10T02:00:00Z",
            )


if __name__ == "__main__":
    unittest.main()
