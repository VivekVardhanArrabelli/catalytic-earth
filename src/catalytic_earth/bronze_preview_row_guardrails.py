"""Guardrail audits for non-destructive bronze preview rows."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .external_source_ingestion import _utc_now_iso

SCHEMA_VERSION = "bronze_preview_row_guardrails.v1"

_REQUIRED_EXCLUDED_CONTEXT = {
    "ec_label",
    "protein_name",
    "uniprot_prose",
    "source_annotation",
    "target_family_lane",
}


def _read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _problem(row_id: str, field: str, detail: str) -> dict[str, str]:
    return {"entry_id": row_id, "field": field, "detail": detail}


def audit_bronze_preview_rows(
    preview_payload: dict[str, Any],
    *,
    preview_path: str | None = None,
    expected_fingerprint: str | None = None,
    expected_source_tier: str | None = None,
    created_utc: str | None = None,
) -> dict[str, Any]:
    """Audit preview ``applied_labels`` before any registry apply."""
    created = created_utc or _utc_now_iso()
    labels = list(preview_payload.get("applied_labels", []))
    problem_rows: list[dict[str, str]] = []
    axes = Counter()
    fingerprints = Counter()
    source_tiers = Counter()

    for label in labels:
        entry_id = str(label.get("entry_id", "<missing>"))
        fingerprint = label.get("fingerprint_id")
        fingerprints[str(fingerprint)] += 1
        evidence = label.get("evidence") or {}
        tier = evidence.get("source_trust_tier") or {}
        source_tier = tier.get("source_tier")
        if source_tier:
            source_tiers[str(source_tier)] += 1
        mechanism_axes = list(tier.get("mechanism_corroborator_axes_present") or [])
        axes.update(mechanism_axes)

        if not entry_id.startswith("uniprot:"):
            problem_rows.append(_problem(entry_id, "entry_id", "entry id is not in uniprot namespace"))
        if label.get("tier") != "bronze":
            problem_rows.append(_problem(entry_id, "tier", "new preview row is not bronze tier"))
        if label.get("review_status") != "automation_curated":
            problem_rows.append(
                _problem(entry_id, "review_status", "new preview row is not automation_curated")
            )
        if expected_fingerprint and fingerprint != expected_fingerprint:
            problem_rows.append(
                _problem(
                    entry_id,
                    "fingerprint_id",
                    f"expected {expected_fingerprint}, observed {fingerprint}",
                )
            )
        if expected_source_tier and source_tier != expected_source_tier:
            problem_rows.append(
                _problem(
                    entry_id,
                    "source_trust_tier",
                    f"expected {expected_source_tier}, observed {source_tier}",
                )
            )
        if evidence.get("predictive_evidence") != []:
            problem_rows.append(
                _problem(entry_id, "predictive_evidence", "predictive evidence must remain empty")
            )
        missing_context = sorted(
            _REQUIRED_EXCLUDED_CONTEXT - set(evidence.get("excluded_context") or [])
        )
        if missing_context:
            problem_rows.append(
                _problem(
                    entry_id,
                    "excluded_context",
                    "missing required excluded context: " + ", ".join(missing_context),
                )
            )
        if "ec_scope_hint" in mechanism_axes:
            problem_rows.append(
                _problem(
                    entry_id,
                    "source_trust_tier",
                    "ec_scope_hint appears as counted mechanism axis",
                )
            )
        if not mechanism_axes:
            problem_rows.append(
                _problem(entry_id, "source_trust_tier", "no counted mechanism axes present")
            )
        if tier.get("meets_n_of_m") is not True:
            problem_rows.append(
                _problem(entry_id, "source_trust_tier", "source trust tier did not meet n-of-m")
            )
        import_gate = set(evidence.get("import_gate_evidence") or [])
        if "current702_accession_sequence_duplicate_screen_clear" not in import_gate:
            problem_rows.append(
                _problem(
                    entry_id,
                    "import_gate_evidence",
                    "missing current702 accession/sequence duplicate screen clearance",
                )
            )

    counts = {
        "preview_applied_label_rows": len(labels),
        "problem_rows": len(problem_rows),
        "fingerprint_counts": dict(sorted(fingerprints.items())),
        "source_tier_counts": dict(sorted(source_tiers.items())),
        "mechanism_axis_counts": dict(sorted(axes.items())),
    }
    return {
        "artifact_id": "v3_bronze_preview_row_guardrails",
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "preview_path": preview_path,
        "status": "row_guardrail_audit_passed" if not problem_rows else "row_guardrail_audit_failed",
        "counts": counts,
        "guardrails": {
            "registry_written": False,
            "frozen_current702_benchmark_written": False,
            "preview_only_no_labels_created": True,
            "ec_name_query_handles_scope_admission_only": True,
            "predictive_evidence_required_empty": True,
        },
        "problem_rows": problem_rows,
        "next_action": (
            "Apply is allowed only if this audit has 0 problem rows and the preview also passes "
            "dedup, novelty, cap, source-trust, leakage, and batch-size gates."
        ),
    }


def render_bronze_preview_row_guardrails_report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    lines = [
        "# Bronze Preview Row Guardrail Audit",
        "",
        f"Run: {audit['created_utc']}",
        f"Preview: `{audit.get('preview_path')}`",
        "",
        "## Result",
        "",
        f"- Status: `{audit['status']}`.",
        f"- Preview applied rows audited: {counts['preview_applied_label_rows']}.",
        f"- Problem rows: {counts['problem_rows']}.",
        f"- Fingerprints: {counts['fingerprint_counts']}.",
        f"- Source tiers: {counts['source_tier_counts']}.",
        f"- Mechanism axes: {counts['mechanism_axis_counts']}.",
        "",
        "## Guardrails",
        "",
        f"- Registry written: {audit['guardrails']['registry_written']}.",
        f"- Frozen current702 written: {audit['guardrails']['frozen_current702_benchmark_written']}.",
        f"- Predictive evidence required empty: {audit['guardrails']['predictive_evidence_required_empty']}.",
    ]
    if audit["problem_rows"]:
        lines.extend(["", "## Problems", ""])
        for row in audit["problem_rows"][:50]:
            lines.append(f"- `{row['entry_id']}` `{row['field']}`: {row['detail']}")
    lines.extend(["", "## Next Action", "", f"- {audit['next_action']}"])
    return "\n".join(lines) + "\n"


def write_bronze_preview_row_guardrails(
    *,
    preview_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    expected_fingerprint: str | None = None,
    expected_source_tier: str | None = None,
) -> dict[str, Any]:
    preview_path = Path(preview_path)
    audit = audit_bronze_preview_rows(
        _read_json(preview_path),
        preview_path=str(preview_path),
        expected_fingerprint=expected_fingerprint,
        expected_source_tier=expected_source_tier,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_bronze_preview_row_guardrails_report(audit), encoding="utf-8")
    return audit
