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
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(),
            stage=stage.strip(),
            task=task.strip(),
            minutes=minutes,
            artifacts=[item.strip() for item in artifacts if item.strip()],
            evidence=[item.strip() for item in evidence if item.strip()],
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
    total_minutes = sum(entry.minutes for entry in entries)
    by_stage: dict[str, int] = defaultdict(int)
    artifact_count = 0
    evidence_count = 0
    adjustments: list[str] = []
    expectation_updates: list[str] = []

    for entry in entries:
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
        f"- Total logged time: {total_minutes} minutes ({total_minutes / 60:.2f} hours)",
    ]

    if by_stage:
        lines.extend(["", "## Time By Stage", ""])
        for stage, minutes in sorted(by_stage.items()):
            lines.append(f"- {stage}: {minutes} minutes ({minutes / 60:.2f} hours)")

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
            lines.append(f"- Minutes: {entry.minutes}")
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
