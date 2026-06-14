"""Audit the silver-ready queue for geometry-confirmation runnability.

The bronze->silver promotion preview intentionally stops at
``silver_ready_pending_geometry_run``. Those rows have independent chemistry support and
true holo evidence, but silver tier changes still require the separate geometry
confirmation gate. This module checks whether silver-ready rows have the remaining
material needed to run that gate without fabricating residue mappings.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .bronze_silver_promotion_preview import (
    DEFAULT_EXPANSION_REGISTRY_PATH,
    build_bronze_silver_promotion_preview,
)
from .mechanism_representation_loop import DEFAULT_PROMOTION_COHESION
from .registry_io import load_json

ARTIFACT_ID = "v3_silver_geometry_confirmation_audit_current702"
SCHEMA_VERSION = "silver_geometry_confirmation_audit.v1"
DEFAULT_OUT = Path("artifacts/v3_silver_geometry_confirmation_audit_current702.json")
DEFAULT_REPORT = Path("work/silver_geometry_confirmation_audit_current702.md")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _structure_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return (row.get("evidence") or {}).get("structure_provenance") or {}


def _mechanism_evidence(row: dict[str, Any]) -> dict[str, Any]:
    return (row.get("evidence") or {}).get("mechanism_evidence") or {}


def _active_site_residues(row: dict[str, Any]) -> list[dict[str, Any]]:
    residues = _mechanism_evidence(row).get("active_site_residues") or []
    return [residue for residue in residues if isinstance(residue, dict)]


def _exact_residue_positions(row: dict[str, Any]) -> list[int]:
    positions: list[int] = []
    for residue in _active_site_residues(row):
        if not residue.get("exact"):
            continue
        try:
            positions.append(int(residue["position"]))
        except (KeyError, TypeError, ValueError):
            continue
    return sorted(set(positions))


def _explicit_structure_positions(row: dict[str, Any]) -> list[dict[str, Any]]:
    positions: list[dict[str, Any]] = []
    for residue in _active_site_residues(row):
        for position in residue.get("structure_positions") or []:
            if isinstance(position, dict):
                positions.append(position)
    return positions


def _local_coordinate_path(row: dict[str, Any]) -> Path | None:
    raw = _structure_provenance(row).get("coordinate_path")
    if not raw:
        return None
    path = Path(str(raw))
    return path if path.exists() else None


def _holo_confirmation(row: dict[str, Any]) -> dict[str, Any]:
    confirmation = _structure_provenance(row).get("holo_pdb_confirmation") or {}
    return confirmation if isinstance(confirmation, dict) else {}


def _row_audit(
    row: dict[str, Any],
    promotion_decision: dict[str, Any],
    *,
    min_exact_residues: int,
) -> dict[str, Any]:
    structure = _structure_provenance(row)
    confirmation = _holo_confirmation(row)
    exact_positions = _exact_residue_positions(row)
    structure_positions = _explicit_structure_positions(row)
    local_coordinate = _local_coordinate_path(row)
    pdb_ids = sorted({str(value).upper() for value in structure.get("pdb_ids") or [] if value})
    holo_pdb_id = str(confirmation.get("pdb_id") or "").upper() or None

    blockers: list[str] = []
    if confirmation.get("status") != "holo_experimental_coordinate_confirmed":
        blockers.append("missing_recorded_holo_pdb_confirmation")
    if len(exact_positions) < min_exact_residues:
        blockers.append("insufficient_exact_active_site_residues")
    if not structure_positions:
        blockers.append("missing_explicit_pdb_residue_mapping")
    if local_coordinate is None:
        blockers.append("missing_local_holo_coordinate_file")

    decision = (
        "ready_for_geometry_confirmation_run"
        if not blockers
        else "blocked_before_geometry_confirmation"
    )
    return {
        "entry_id": row.get("entry_id"),
        "fingerprint_id": row.get("fingerprint_id"),
        "tier": row.get("tier"),
        "promotion_preview_decision": promotion_decision.get("decision"),
        "decision": decision,
        "blockers": blockers,
        "holo_pdb_id": holo_pdb_id,
        "pdb_ids": pdb_ids,
        "cofactor_comp_ids_present": confirmation.get("cofactor_comp_ids_present") or [],
        "local_coordinate_path": str(local_coordinate) if local_coordinate else None,
        "local_coordinate_path_recorded": bool(structure.get("coordinate_path")),
        "local_coordinate_path_exists": local_coordinate is not None,
        "exact_active_site_residue_count": len(exact_positions),
        "exact_active_site_positions": exact_positions[:50],
        "explicit_structure_position_count": len(structure_positions),
        "chemistry_cohesion": promotion_decision.get("chemistry_cohesion"),
        "geometry_confirmation_run": False,
        "tier_changed": False,
        "recommended_next_action": (
            "materialize a local holo coordinate and explicit PDB chain/residue mappings, "
            "then run the geometry confirmation gate"
            if blockers
            else "run the geometry confirmation gate; apply silver only for passing rows"
        ),
    }


def build_silver_geometry_confirmation_audit(
    expansion_payload: list[dict[str, Any]],
    *,
    created_utc: str | None = None,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    min_exact_residues: int = 2,
) -> dict[str, Any]:
    """Build a non-destructive audit of geometry-confirmation runnability."""
    created = created_utc or _utc_now_iso()
    promotion = build_bronze_silver_promotion_preview(
        expansion_payload,
        cohesion_threshold=cohesion_threshold,
    )
    promotion_by_entry = {
        row["entry_id"]: row
        for row in promotion.get("silver_ready_preview", [])
        if isinstance(row, dict) and row.get("entry_id")
    }
    rows_by_entry = {
        row.get("entry_id"): row
        for row in expansion_payload
        if isinstance(row, dict) and row.get("entry_id")
    }
    row_audits = [
        _row_audit(
            rows_by_entry[entry_id],
            promotion_by_entry[entry_id],
            min_exact_residues=min_exact_residues,
        )
        for entry_id in sorted(promotion_by_entry)
        if entry_id in rows_by_entry
    ]
    decision_counts = Counter(row["decision"] for row in row_audits)
    blocker_counts = Counter(blocker for row in row_audits for blocker in row["blockers"])
    by_fingerprint: dict[str, Counter[str]] = {}
    for row in row_audits:
        fp = str(row.get("fingerprint_id") or "__missing_fingerprint__")
        by_fingerprint.setdefault(fp, Counter())[str(row["decision"])] += 1

    ready_rows = [
        row for row in row_audits if row["decision"] == "ready_for_geometry_confirmation_run"
    ]
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "ok" if ready_rows else "blocked_no_rows_runnable",
        "non_destructive": True,
        "what": (
            "Audit the silver_ready_pending_geometry_run queue for the remaining "
            "material required by the separate geometry confirmation gate. This does "
            "not run/fake geometry scoring and does not flip tiers."
        ),
        "policy": {
            "silver_ready_source": "bronze_silver_promotion_preview",
            "cohesion_threshold": cohesion_threshold,
            "min_exact_active_site_residues": min_exact_residues,
            "requires_recorded_holo_pdb_confirmation": True,
            "requires_local_holo_coordinate_file": True,
            "requires_explicit_pdb_chain_residue_mapping": True,
            "uniprot_sequence_positions_are_not_treated_as_pdb_residue_mapping": True,
            "silver_tier_change_requires_separate_geometry_confirmation_pass": True,
        },
        "counts": {
            "expansion_rows": len(expansion_payload),
            "seed_rows": promotion.get("seed_labels", 0),
            "silver_ready_input_rows": len(row_audits),
            "ready_for_geometry_confirmation_run": len(ready_rows),
            "blocked_before_geometry_confirmation": int(
                decision_counts.get("blocked_before_geometry_confirmation", 0)
            ),
            "silver_flips_applied": 0,
        },
        "promotion_preview_decision_counts": promotion.get("decision_counts", {}),
        "decision_counts": dict(sorted(decision_counts.items())),
        "blocker_counts": dict(sorted(blocker_counts.items())),
        "decision_counts_by_fingerprint": {
            fp: dict(sorted(counter.items())) for fp, counter in sorted(by_fingerprint.items())
        },
        "ready_rows": ready_rows[:100],
        "blocked_examples": [
            row
            for row in row_audits
            if row["decision"] == "blocked_before_geometry_confirmation"
        ][:100],
        "guardrails": {
            "registry_written": False,
            "tier_changed": False,
            "geometry_confirmation_run_or_faked": False,
            "annotation_only_silver_promotion": False,
            "predictive_evidence_changed": False,
        },
        "next_action": (
            "Backfill/materialize local holo PDB coordinates and explicit PDB residue "
            "mappings for the silver-ready rows, then run this audit again before any "
            "silver tier apply."
            if not ready_rows
            else "Run the geometry confirmation gate on ready_rows and apply silver only "
            "to rows that pass."
        ),
        "rows": row_audits,
    }


def summarize_audit(audit: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in audit.items() if key != "rows"}


def _report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    lines = [
        "# Silver Geometry Confirmation Audit",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Checks whether `silver_ready_pending_geometry_run` rows are actually runnable by",
        "the separate geometry confirmation gate. This is non-destructive: it does not",
        "run/fake geometry scoring, write the registry, or flip tiers.",
        "",
        "## Result",
        "",
        f"- Silver-ready input rows: {counts['silver_ready_input_rows']}.",
        f"- Ready for geometry confirmation run: "
        f"{counts['ready_for_geometry_confirmation_run']}.",
        f"- Blocked before geometry confirmation: "
        f"{counts['blocked_before_geometry_confirmation']}.",
        f"- Silver flips applied: {counts['silver_flips_applied']}.",
        "",
        "## Blockers",
        "",
        "| blocker | count |",
        "| --- | ---: |",
    ]
    for blocker, count in audit["blocker_counts"].items():
        lines.append(f"| {blocker} | {count} |")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "- Recorded holo PDB confirmation, a local holo coordinate file, and explicit",
            "  PDB chain/residue mappings are required before geometry confirmation can",
            "  run. UniProt sequence positions alone are not treated as PDB residue",
            "  mappings.",
            "- Silver tier changes remain a separate authorized apply step after the",
            "  geometry gate passes.",
            "",
            "## Next Action",
            "",
            f"- {audit['next_action']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_silver_geometry_confirmation_audit(
    *,
    out_path: Path = DEFAULT_OUT,
    report_path: Path | None = DEFAULT_REPORT,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    min_exact_residues: int = 2,
) -> dict[str, Any]:
    expansion = load_json(Path(expansion_registry_path))
    if not isinstance(expansion, list):
        raise ValueError(f"{expansion_registry_path} must be a registry list")
    audit = build_silver_geometry_confirmation_audit(
        expansion,
        cohesion_threshold=cohesion_threshold,
        min_exact_residues=min_exact_residues,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(summarize_audit(audit), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
