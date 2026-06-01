from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REFERENCE_RE = re.compile(r"`((?:artifacts|work|docs|src|tests|data)/[^`\s]+)`")
DEFAULT_CURRENT_DOCS = [
    Path("docs/artifact_index.md"),
    Path("docs/project_state.md"),
    Path("docs/decision_log.md"),
    Path("docs/agent_runbook.md"),
]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _ignore_reason(path_text: str) -> str | None:
    if "*" in path_text:
        return "glob_pattern"
    if "<" in path_text or ">" in path_text:
        return "template_placeholder"
    return None


def build_current_docs_artifact_reference_check(
    *,
    doc_paths: list[Path],
) -> dict[str, Any]:
    checked = []
    ignored = []
    missing = []
    for doc_path in doc_paths:
        text = Path(doc_path).read_text(encoding="utf-8")
        for match in REFERENCE_RE.finditer(text):
            raw = match.group(1).rstrip(".,;:")
            checked_path = raw.split("::", 1)[0]
            reason = _ignore_reason(checked_path)
            if reason:
                ignored.append(
                    {"doc": str(doc_path), "reference": raw, "reason": reason}
                )
                continue
            exists = Path(checked_path).exists()
            record = {
                "doc": str(doc_path),
                "reference": raw,
                "checked_path": checked_path,
                "exists": exists,
            }
            checked.append(record)
            if not exists:
                missing.append(
                    {
                        "doc": str(doc_path),
                        "reference": raw,
                        "checked_path": checked_path,
                    }
                )
    return {
        "artifact_id": "v3_current_docs_artifact_reference_check_current702_20260601",
        "schema_version": "current_docs_artifact_reference_check.v1",
        "created_utc": _utc_now_iso(),
        "status": (
            "current_docs_artifact_references_passed"
            if not missing
            else "current_docs_artifact_references_missing_paths"
        ),
        "scope": (
            "Checks current durable docs for backtick-referenced repo paths, "
            "excluding intentional globs and template placeholders."
        ),
        "docs_checked": [str(path) for path in doc_paths],
        "guardrails": {
            "docs_only_reference_check": True,
            "artifacts_modified_by_check": False,
            "labels_registries_ontologies_changed": False,
            "production_thresholds_changed": False,
        },
        "counts": {
            "references_checked": len(checked),
            "ignored_references": len(ignored),
            "missing_references": len(missing),
        },
        "missing_references": missing,
        "ignored_references": ignored,
        "sample_checked_references": checked[:40],
        "interpretation": {
            "headline": (
                f"{len(missing)} missing concrete references across current docs "
                "after excluding templates/globs."
            ),
            "next_action": (
                "Keep this check focused on durable current docs; work/handoff.md "
                "intentionally contains historical paths and globs."
            ),
        },
    }


def _render_current_docs_artifact_reference_check(audit: dict[str, Any]) -> str:
    lines = [
        "# Current Docs Artifact Reference Check - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- References checked: {audit['counts']['references_checked']}",
        f"- Ignored references: {audit['counts']['ignored_references']}",
        f"- Missing references: {audit['counts']['missing_references']}",
        "",
        "## Missing References",
        "",
    ]
    if audit["missing_references"]:
        lines.extend(["| doc | reference |", "| --- | --- |"])
        for row in audit["missing_references"]:
            lines.append(f"| {row['doc']} | `{row['reference']}` |")
    else:
        lines.append("- None")
    lines += [
        "",
        "## Interpretation",
        "",
        f"- {audit['interpretation']['headline']}",
        f"- {audit['interpretation']['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_current_docs_artifact_reference_check(
    *,
    doc_paths: list[Path] | None,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    audit = build_current_docs_artifact_reference_check(
        doc_paths=doc_paths or DEFAULT_CURRENT_DOCS
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            _render_current_docs_artifact_reference_check(audit),
            encoding="utf-8",
        )
    return audit
