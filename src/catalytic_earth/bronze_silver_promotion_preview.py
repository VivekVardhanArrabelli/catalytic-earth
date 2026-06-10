"""Bronze->silver promotion preview -- the queue, not a fabricated confirmation.

Every expansion label is ``tier=bronze`` because structure/cofactor-fused geometry
confirmation was demoted from an entry gate to a deferred **bronze->silver promotion
signal** (2026-06-09). This module turns the representation loop's promotion triage
into an explicit, non-destructive promotion QUEUE: which bronze labels are ready for
that confirmation, which are blocked, and which must be reviewed first.

It is scrupulously honest about what it does NOT do. The gating geometry
confirmation is the ``geometry_inverse_gate_confirmation_on_holo_or_cofactor_fused_structure``
audit, and that audit **abstains on predicted-apo coordinates** (the cofactor is
absent -- the step-4 finding). So this preview does NOT run or fake that
confirmation and does NOT flip any tier. It stages the queue using only signals that
are actually checkable here:

- **Chemistry corroboration** (representation loop): the label's cofactor/ligand
  chemistry independently agrees with its assigned fingerprint (nearest centroid ==
  assigned). This is an INDEPENDENT axis from the original annotation-anchored
  scope assignment, so agreement is real corroboration. Leakage-safe: chemistry
  only, never EC/name/prose/label.
- **Structure confirmability**: whether the deferred geometry confirmation can even
  run -- ``holo`` (experimental coordinates present -> runnable), ``apo_only``
  (AFDB predicted -> the gate abstains, needs cofactor fusion), or ``none``.
- **Triad confirmation** for the cofactorless ``ser_his_acid_hydrolase`` (its
  structural confirmation is the Ser-His-Asp triad, which works on apo too).

Promotion decision per bronze seed label:

- ``silver_ready_pending_geometry_run`` -- chemistry-corroborated AND the geometry
  confirmation is runnable (holo structure), OR ser_his with a confirmed triad.
  These are proposed for silver *pending the actual confirmation run* (a separate
  authorized step, runnable where holo structures / backends exist -- e.g. locally).
- ``blocked_apo_needs_cofactor_fusion`` -- corroborated but only apo coordinates.
- ``blocked_pending_structure`` -- corroborated but no coordinates staged.
- ``review_chemistry_disagrees`` -- chemistry points at a different fingerprint;
  must be reviewed before any promotion.
- ``hold_low_chemistry_cohesion`` -- weak agreement.

NON-DESTRUCTIVE: writes no registry, flips no tier, emits the queue as a preview
artifact only. The tier change and the geometry confirmation run remain separate,
authorized steps.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .mechanism_representation_loop import (
    DEFAULT_PROMOTION_COHESION,
    assess_row_against_centroids,
    fingerprint_centroids,
)
from .ser_his_triad_locator import assess_ser_his_candidate

DEFAULT_EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")

# coordinate_status -> confirmability of the deferred geometry gate.
HOLO_STATUS = "experimental_pdb_coordinate_provenance_available"
APO_STATUS = "afdb_predicted_coordinate_provenance_available"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> list[dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _structure_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("structure_provenance", {}) or {}


def structure_confirmability(row: dict[str, Any]) -> str:
    """Whether the deferred geometry confirmation can run for this row."""
    prov = _structure_provenance(row)
    status = prov.get("coordinate_status")
    has_path = bool(prov.get("coordinate_path"))
    if status == HOLO_STATUS:
        return "holo"
    if status == APO_STATUS or has_path:
        return "apo_only"
    return "none"


def assess_promotion(
    row: dict[str, Any],
    centroids: dict[str, list[float]],
    *,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
) -> dict[str, Any]:
    """Promotion decision for one bronze seed label (non-destructive)."""
    chem = assess_row_against_centroids(row, centroids)
    fp = row.get("fingerprint_id")
    confirmability = structure_confirmability(row)
    agrees = chem["chemistry_agrees_with_label"]
    cohesion = chem["own_cohesion"] or 0.0

    # ser_his is cofactorless: its structural confirmation is the triad, runnable on
    # apo too. (No expansion ser_his today, but the path is wired.)
    triad_confirmed = None
    if fp == "ser_his_acid_hydrolase" and confirmability != "none":
        triad = assess_ser_his_candidate(row)
        triad_confirmed = triad.get("decision") == "assign_ser_his"

    if agrees is False:
        decision = "review_chemistry_disagrees"
    elif cohesion < cohesion_threshold:
        decision = "hold_low_chemistry_cohesion"
    elif triad_confirmed:
        decision = "silver_ready_pending_geometry_run"
    elif fp == "ser_his_acid_hydrolase":
        decision = "blocked_pending_structure" if confirmability == "none" else (
            "hold_low_chemistry_cohesion"
        )
    elif confirmability == "holo":
        decision = "silver_ready_pending_geometry_run"
    elif confirmability == "apo_only":
        decision = "blocked_apo_needs_cofactor_fusion"
    else:
        decision = "blocked_pending_structure"

    remaining_audits = list(
        row.get("evidence", {}).get("pending_promotion_audits", [])
    )
    return {
        "entry_id": row.get("entry_id"),
        "fingerprint_id": fp,
        "decision": decision,
        "chemistry_agrees_with_label": agrees,
        "chemistry_cohesion": cohesion,
        "nearest_fingerprint": chem["nearest_fingerprint"],
        "structure_confirmability": confirmability,
        "triad_confirmed": triad_confirmed,
        "remaining_promotion_audits": remaining_audits,
    }


def build_bronze_silver_promotion_preview(
    expansion: list[dict[str, Any]],
    *,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
) -> dict[str, Any]:
    seed = [r for r in expansion if r.get("label_type") == "seed_fingerprint"]
    centroids = fingerprint_centroids(seed)

    decisions = [
        assess_promotion(row, centroids, cohesion_threshold=cohesion_threshold)
        for row in seed
    ]
    decision_counts: Counter = Counter(d["decision"] for d in decisions)
    silver_ready = [d for d in decisions if d["decision"] == "silver_ready_pending_geometry_run"]

    by_fingerprint: dict[str, Counter] = {}
    for d in decisions:
        by_fingerprint.setdefault(d["fingerprint_id"], Counter())[d["decision"]] += 1

    return {
        "audit": "bronze_silver_promotion_preview",
        "created_utc": _utc_now_iso(),
        "status": "ok",
        "non_destructive": True,
        "policy": {
            "cohesion_threshold": cohesion_threshold,
            "silver_ready_definition": (
                "chemistry independently corroborates the assigned fingerprint AND "
                "the deferred geometry confirmation is runnable (holo structure), OR "
                "ser_his with a confirmed Ser-His-Asp triad"
            ),
            "gating_audit_not_run_here": (
                "geometry_inverse_gate_confirmation abstains on predicted-apo "
                "coordinates; it is NOT run or faked -- silver_ready rows are staged "
                "for that confirmation as a separate authorized step"
            ),
        },
        "seed_labels": len(seed),
        "decision_counts": dict(sorted(decision_counts.items())),
        "decision_counts_by_fingerprint": {
            fp: dict(sorted(c.items())) for fp, c in sorted(by_fingerprint.items())
        },
        "silver_ready_count": len(silver_ready),
        "silver_ready_preview": silver_ready,
        "review_queue": [
            d for d in decisions if d["decision"] == "review_chemistry_disagrees"
        ][:25],
        "guardrails": {
            "registry_written": False,
            "tier_changed": False,
            "geometry_confirmation_run_or_faked": False,
            "chemistry_corroboration_is_leakage_safe": True,
            "promotion_and_geometry_run_are_separate_authorized_steps": True,
        },
    }


def _report(audit: dict[str, Any]) -> str:
    dc = audit["decision_counts"]
    lines = [
        "# Bronze->Silver Promotion Preview",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Turns the representation loop's promotion triage into an explicit, "
        "non-destructive promotion QUEUE. It does NOT run or fake the deferred "
        "geometry confirmation (that gate abstains on predicted-apo coordinates) and "
        "flips no tier -- it stages which bronze labels are ready for that "
        "confirmation, which are blocked, and which need review first.",
        "",
        f"- Seed labels: {audit['seed_labels']}.",
        f"- **Silver-ready (pending the geometry-confirmation run): "
        f"{audit['silver_ready_count']}**.",
        "",
        "## Decision counts",
        "",
        "| decision | count |",
        "| --- | --- |",
    ]
    for decision, count in dc.items():
        lines.append(f"| {decision} | {count} |")
    lines.extend(
        [
            "",
            "## Per-fingerprint breakdown",
            "",
            "| fingerprint | decisions |",
            "| --- | --- |",
        ]
    )
    for fp, counts in audit["decision_counts_by_fingerprint"].items():
        lines.append(f"| {fp} | {counts} |")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            f"- Silver-ready: {audit['policy']['silver_ready_definition']}.",
            f"- Gating audit NOT run here: {audit['policy']['gating_audit_not_run_here']}.",
            "",
            "## Guardrails",
            "",
            f"- Registry written: {audit['guardrails']['registry_written']}.",
            f"- Tier changed: {audit['guardrails']['tier_changed']}.",
            f"- Geometry confirmation run or faked: "
            f"{audit['guardrails']['geometry_confirmation_run_or_faked']}.",
            "- Chemistry corroboration is leakage-safe; promotion + geometry run are "
            "separate authorized steps.",
            "",
        ]
    )
    return "\n".join(lines)


def write_bronze_silver_promotion_preview(
    *,
    out_path: Path,
    report_path: Path | None = None,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    audit = build_bronze_silver_promotion_preview(
        expansion, cohesion_threshold=cohesion_threshold
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
