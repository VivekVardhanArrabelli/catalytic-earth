from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from catalytic_earth.automation import (
    acquire_automation_lock,
    default_automation_lock_dir,
    inspect_automation_lock,
    release_automation_lock,
)


class AutomationLockTests(unittest.TestCase):
    def test_atomic_lock_rejects_fresh_lock(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_dir = Path(tmpdir) / "run.lock"
            first = acquire_automation_lock(lock_dir, started_at="2026-05-10T00:00:00Z", owner_token="run-a")
            self.assertTrue(first.acquired)
            second = acquire_automation_lock(lock_dir, started_at="2026-05-10T00:01:00Z", owner_token="run-b")
            self.assertFalse(second.acquired)
            self.assertEqual(second.status, "active_lock_present")
            self.assertIn("pid", first.as_dict())
            with self.assertRaises(PermissionError):
                release_automation_lock(lock_dir, owner_token="run-b")
            self.assertTrue(lock_dir.exists())
            release_automation_lock(lock_dir, owner_token="run-a")
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
                owner_token="run-b",
                worktree_dirty=True,
            )
            self.assertFalse(result.acquired)
            self.assertEqual(result.status, "stale_lock_dirty_worktree_requires_recovery")
            self.assertTrue(lock_dir.exists())

    def test_old_clean_lock_is_never_stolen(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_dir = Path(tmpdir) / "run.lock"
            acquire_automation_lock(lock_dir, started_at="2026-05-10T00:00:00Z", owner_token="run-a")
            old = datetime.now(timezone.utc) - timedelta(hours=2)
            os.utime(lock_dir, (old.timestamp(), old.timestamp()))
            result = acquire_automation_lock(
                lock_dir,
                started_at="2026-05-10T02:00:00Z",
                owner_token="run-b",
                worktree_dirty=False,
            )
            self.assertFalse(result.acquired)
            self.assertEqual(result.status, "stale_lock_requires_recovery")
            self.assertEqual(result.owner_token, "run-a")
            self.assertEqual(
                (lock_dir / "started_at").read_text(encoding="utf-8").strip(),
                "2026-05-10T00:00:00Z",
            )

    def test_concurrent_processes_have_only_one_owner(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_dir = Path(tmpdir) / "run.lock"
            script = (
                "import sys; from pathlib import Path; "
                "from catalytic_earth.automation import acquire_automation_lock; "
                "r=acquire_automation_lock(Path(sys.argv[1]), started_at='now', "
                "owner_token=sys.argv[2]); sys.exit(0 if r.acquired else 3)"
            )
            env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
            processes = [subprocess.Popen([sys.executable, "-c", script, str(lock_dir), str(i)],
                                          env=env) for i in range(4)]
            results = [process.wait(timeout=20) for process in processes]
            self.assertEqual(sorted(results), [0, 3, 3, 3])

    def test_linked_worktree_uses_same_lock(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir) / "repo"
            linked = Path(tmpdir) / "linked"
            subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
            subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                            "-c", "commit.gpgsign=false", "commit", "--allow-empty", "-m", "seed"],
                           cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "worktree", "add", "--detach", str(linked)],
                           cwd=repo, check=True, capture_output=True)
            self.assertEqual(default_automation_lock_dir(repo), default_automation_lock_dir(linked))
            acquire_automation_lock(default_automation_lock_dir(repo), started_at="now", owner_token="main")
            result = acquire_automation_lock(default_automation_lock_dir(linked), started_at="now",
                                             owner_token="linked")
            self.assertFalse(result.acquired)


if __name__ == "__main__":
    unittest.main()
