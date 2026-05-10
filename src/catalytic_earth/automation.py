from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class AutomationLockResult:
    acquired: bool
    lock_dir: Path
    status: str
    age_seconds: float | None = None
    started_at: str | None = None

    def as_dict(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "acquired": self.acquired,
            "lock_dir": str(self.lock_dir),
            "status": self.status,
        }
        if self.age_seconds is not None:
            payload["age_seconds"] = self.age_seconds
        if self.started_at is not None:
            payload["started_at"] = self.started_at
        pid = _read_optional_text(self.lock_dir / "pid")
        if pid is not None:
            payload["pid"] = pid
        return payload


def acquire_automation_lock(
    lock_dir: Path,
    *,
    started_at: str,
    stale_after_seconds: float = 90 * 60,
    worktree_dirty: bool = False,
    now: datetime | None = None,
) -> AutomationLockResult:
    """Acquire an atomic directory lock, honoring stale-lock recovery rules."""
    lock_dir = Path(lock_dir)
    try:
        lock_dir.mkdir(parents=False)
    except FileExistsError:
        current_time = now or datetime.now(timezone.utc)
        mtime = datetime.fromtimestamp(lock_dir.stat().st_mtime, tz=timezone.utc)
        age_seconds = (current_time - mtime).total_seconds()
        prior_started_at = _read_started_at(lock_dir)
        if age_seconds < stale_after_seconds:
            return AutomationLockResult(
                acquired=False,
                lock_dir=lock_dir,
                status="active_lock_present",
                age_seconds=round(age_seconds, 3),
                started_at=prior_started_at,
            )
        if worktree_dirty:
            return AutomationLockResult(
                acquired=False,
                lock_dir=lock_dir,
                status="stale_lock_dirty_worktree_requires_recovery",
                age_seconds=round(age_seconds, 3),
                started_at=prior_started_at,
            )
        shutil.rmtree(lock_dir)
        lock_dir.mkdir(parents=False)
        _write_lock_files(lock_dir, started_at)
        return AutomationLockResult(
            acquired=True,
            lock_dir=lock_dir,
            status="stale_lock_replaced",
            age_seconds=round(age_seconds, 3),
            started_at=started_at,
        )
    _write_lock_files(lock_dir, started_at)
    return AutomationLockResult(
        acquired=True,
        lock_dir=lock_dir,
        status="acquired",
        started_at=started_at,
    )


def inspect_automation_lock(
    lock_dir: Path,
    *,
    stale_after_seconds: float = 90 * 60,
    now: datetime | None = None,
) -> AutomationLockResult:
    lock_dir = Path(lock_dir)
    if not lock_dir.exists():
        return AutomationLockResult(
            acquired=False,
            lock_dir=lock_dir,
            status="unlocked",
        )
    current_time = now or datetime.now(timezone.utc)
    mtime = datetime.fromtimestamp(lock_dir.stat().st_mtime, tz=timezone.utc)
    age_seconds = round((current_time - mtime).total_seconds(), 3)
    status = "stale_lock_present" if age_seconds >= stale_after_seconds else "active_lock_present"
    return AutomationLockResult(
        acquired=False,
        lock_dir=lock_dir,
        status=status,
        age_seconds=age_seconds,
        started_at=_read_started_at(lock_dir),
    )


def release_automation_lock(lock_dir: Path) -> None:
    shutil.rmtree(lock_dir)


def _write_lock_files(lock_dir: Path, started_at: str) -> None:
    (lock_dir / "started_at").write_text(f"{started_at}\n", encoding="utf-8")
    (lock_dir / "pid").write_text(f"{os.getpid()}\n", encoding="utf-8")


def _read_started_at(lock_dir: Path) -> str | None:
    return _read_optional_text(lock_dir / "started_at")


def _read_optional_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8").strip() or None
    except FileNotFoundError:
        return None
