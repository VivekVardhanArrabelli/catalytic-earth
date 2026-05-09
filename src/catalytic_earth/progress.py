from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .sources import PROJECT_ROOT


DEFAULT_LOG = PROJECT_ROOT / "work" / "progress_log.jsonl"
DEFAULT_REPORT = PROJECT_ROOT / "work" / "status.md"


@dataclass(frozen=True)
class WorkEntry:
    timestamp: str
    stage: str
    task: str
    minutes: int
    artifacts: list[str]
    evidence: list[str]
    time_mode: str = "estimate"
    started_at: str | None = None
    ended_at: str | None = None
    measured_minutes: float | None = None
    scope_adjustment: str | None = None
    expectation_update: str | None = None
    commit: str | None = None
    notes: str | None = None

    @classmethod
    def create(
        cls,
        stage: str,
        task: str,
        minutes: int,
        artifacts: list[str],
        evidence: list[str],
        time_mode: str = "estimate",
        started_at: str | None = None,
        ended_at: str | None = None,
        measured_minutes: float | None = None,
        scope_adjustment: str | None = None,
        expectation_update: str | None = None,
        commit: str | None = None,
        notes: str | None = None,
    ) -> "WorkEntry":
        if minutes < 0:
            raise ValueError("minutes must be non-negative")
        if not stage.strip():
            raise ValueError("stage is required")
        if not task.strip():
            raise ValueError("task is required")
        if time_mode not in {"estimate", "measured", "corrected"}:
            raise ValueError("time_mode must be estimate, measured, or corrected")
        started = _clean_optional(started_at)
        ended = _clean_optional(ended_at)
        derived_measured = measured_minutes
        if started and ended:
            derived_measured = _elapsed_minutes(started, ended)
        if derived_measured is not None and derived_measured < 0:
            raise ValueError("measured_minutes must be non-negative")
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(),
            stage=stage.strip(),
            task=task.strip(),
            minutes=minutes,
            artifacts=[item.strip() for item in artifacts if item.strip()],
            evidence=[item.strip() for item in evidence if item.strip()],
            time_mode=time_mode,
            started_at=started,
            ended_at=ended,
            measured_minutes=round(derived_measured, 3) if derived_measured is not None else None,
            scope_adjustment=_clean_optional(scope_adjustment),
            expectation_update=_clean_optional(expectation_update),
            commit=_clean_optional(commit),
            notes=_clean_optional(notes),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WorkEntry":
        return cls(
            timestamp=str(data["timestamp"]),
            stage=str(data["stage"]),
            task=str(data["task"]),
            minutes=int(data["minutes"]),
            artifacts=list(data.get("artifacts", [])),
            evidence=list(data.get("evidence", [])),
            time_mode=str(data.get("time_mode", "estimate")),
            started_at=data.get("started_at"),
            ended_at=data.get("ended_at"),
            measured_minutes=(
                float(data["measured_minutes"]) if data.get("measured_minutes") is not None else None
            ),
            scope_adjustment=data.get("scope_adjustment"),
            expectation_update=data.get("expectation_update"),
            commit=data.get("commit"),
            notes=data.get("notes"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "stage": self.stage,
            "task": self.task,
            "minutes": self.minutes,
            "artifacts": self.artifacts,
            "evidence": self.evidence,
            "time_mode": self.time_mode,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "measured_minutes": self.measured_minutes,
            "scope_adjustment": self.scope_adjustment,
            "expectation_update": self.expectation_update,
            "commit": self.commit,
            "notes": self.notes,
        }


def append_work_entry(entry: WorkEntry, path: Path = DEFAULT_LOG) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        json.dump(entry.to_dict(), handle, sort_keys=True)
        handle.write("\n")


def load_work_entries(path: Path = DEFAULT_LOG) -> list[WorkEntry]:
    if not path.exists():
        return []
    entries: list[WorkEntry] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                entries.append(WorkEntry.from_dict(json.loads(line)))
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
                raise ValueError(f"invalid progress log line {line_number}: {exc}") from exc
    return entries


def build_progress_report(entries: list[WorkEntry]) -> str:
    estimated_minutes = sum(entry.minutes for entry in entries if entry.time_mode != "measured")
    measured_minutes = sum(entry.measured_minutes or 0 for entry in entries if entry.time_mode == "measured")
    by_stage: dict[str, int] = defaultdict(int)
    measured_by_stage: dict[str, float] = defaultdict(float)
    artifact_count = 0
    evidence_count = 0
    adjustments: list[str] = []
    expectation_updates: list[str] = []

    for entry in entries:
        if entry.time_mode == "measured":
            measured_by_stage[entry.stage] += entry.measured_minutes or 0
        else:
            by_stage[entry.stage] += entry.minutes
        artifact_count += len(entry.artifacts)
        evidence_count += len(entry.evidence)
        if entry.scope_adjustment:
            adjustments.append(f"- {entry.timestamp}: {entry.scope_adjustment}")
        if entry.expectation_update:
            expectation_updates.append(f"- {entry.timestamp}: {entry.expectation_update}")

    lines = [
        "# Catalytic Earth Status",
        "",
        "Generated from `work/progress_log.jsonl`.",
        "",
        "## Time",
        "",
        f"- Entries: {len(entries)}",
        f"- Measured elapsed time: {measured_minutes:.1f} minutes ({measured_minutes / 60:.2f} hours)",
        f"- Estimated/planned time: {estimated_minutes} minutes ({estimated_minutes / 60:.2f} hours)",
        "- Note: entries before timing instrumentation are estimates, not clock measurements.",
    ]

    if by_stage or measured_by_stage:
        lines.extend(["", "## Time By Stage", ""])
        for stage, minutes in sorted(measured_by_stage.items()):
            lines.append(f"- {stage}: {minutes:.1f} measured minutes ({minutes / 60:.2f} hours)")
        for stage, minutes in sorted(by_stage.items()):
            lines.append(f"- {stage}: {minutes} estimated minutes ({minutes / 60:.2f} hours)")

    lines.extend(
        [
            "",
            "## Progress Counters",
            "",
            f"- Artifact references logged: {artifact_count}",
            f"- Evidence references logged: {evidence_count}",
        ]
    )

    if entries:
        lines.extend(["", "## Recent Entries", ""])
        for entry in entries[-8:]:
            lines.append(f"### {entry.timestamp} - {entry.stage}")
            lines.append("")
            lines.append(f"- Task: {entry.task}")
            lines.append(f"- Time mode: {entry.time_mode}")
            if entry.time_mode == "measured":
                lines.append(f"- Measured minutes: {entry.measured_minutes}")
                if entry.started_at and entry.ended_at:
                    lines.append(f"- Started: {entry.started_at}")
                    lines.append(f"- Ended: {entry.ended_at}")
            else:
                lines.append(f"- Estimated/planned minutes: {entry.minutes}")
            if entry.artifacts:
                lines.append(f"- Artifacts: {', '.join(entry.artifacts)}")
            if entry.evidence:
                lines.append(f"- Evidence: {', '.join(entry.evidence)}")
            if entry.commit:
                lines.append(f"- Commit: `{entry.commit}`")
            if entry.notes:
                lines.append(f"- Notes: {entry.notes}")
            lines.append("")

    if expectation_updates:
        lines.extend(["## Expectation Updates", "", *expectation_updates, ""])

    if adjustments:
        lines.extend(["## Scope Adjustments", "", *adjustments, ""])

    if not entries:
        lines.extend(["", "No work entries logged yet.", ""])

    return "\n".join(lines).rstrip() + "\n"


def write_progress_report(
    log_path: Path = DEFAULT_LOG,
    report_path: Path = DEFAULT_REPORT,
) -> str:
    report = build_progress_report(load_work_entries(log_path))
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    return report


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _elapsed_minutes(started_at: str, ended_at: str) -> float:
    started = _parse_iso_datetime(started_at)
    ended = _parse_iso_datetime(ended_at)
    return (ended - started).total_seconds() / 60


def _parse_iso_datetime(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed
