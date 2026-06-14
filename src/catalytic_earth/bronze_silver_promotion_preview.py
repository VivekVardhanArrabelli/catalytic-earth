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
from .structure import parse_atom_site_loop

DEFAULT_EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")

# The deferred geometry confirmation degrades on APO coordinates -- the documented
# Problem-2 finding: predicted-apo loses the cofactor, the router drops 45/45 ->
# 23/45, and the geometry inverse-gate ABSTAINS on 100% of apo structures. The
# binding axis is therefore COFACTOR PRESENCE in the coordinates, NOT experimental
# vs predicted provenance -- an experimental PDB can be apo too (and in this
# registry 103/104 coordinate-bearing rows are apo). So confirmability is decided
# by whether the annotated cofactor is actually present in the coordinates.
#
# Annotated cofactor name (substring) -> candidate PDB HETATM comp ids.
COFACTOR_NAME_TO_PDB_COMP: dict[str, frozenset[str]] = {
    "zn": frozenset({"ZN"}),
    "mn": frozenset({"MN", "MN3"}),
    "mg": frozenset({"MG"}),
    "fe(3": frozenset({"FE"}),
    "fe(2": frozenset({"FE2"}),
    "fe cation": frozenset({"FE", "FE2"}),
    "ni": frozenset({"NI"}),
    "ca": frozenset({"CA"}),
    "co(2": frozenset({"CO", "3CO"}),
    "cu": frozenset({"CU", "CU1"}),
    "fad": frozenset({"FAD"}),
    "fmn": frozenset({"FMN"}),
    "pyridoxal": frozenset({"PLP", "PMP"}),
    "heme c": frozenset({"HEC"}),
    "heme b": frozenset({"HEM"}),
    "heme": frozenset({"HEM", "HEC"}),
    "s-adenosyl-l-methionine": frozenset({"SAM"}),
    "adenosylcobalamin": frozenset({"B12", "COB", "CNC"}),
    "[4fe-4s]": frozenset({"SF4"}),
    "[2fe-2s]": frozenset({"FES"}),
    "[3fe-4s]": frozenset({"F3S"}),
    "chloride": frozenset({"CL"}),
}
_NON_COFACTOR_HET = frozenset({"HOH", "DOD", "WAT"})


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> list[dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _structure_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("structure_provenance", {}) or {}


def _mechanism_evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("mechanism_evidence", {}) or {}


def expected_cofactor_comp_ids(row: dict[str, Any]) -> set[str]:
    """Candidate PDB HETATM comp ids for the row's annotated cofactor(s)."""
    out: set[str] = set()
    for cofactor in _mechanism_evidence(row).get("cofactors") or []:
        name = (cofactor.get("name") or "").lower()
        for key, comps in COFACTOR_NAME_TO_PDB_COMP.items():
            if key in name:
                out |= set(comps)
    return out


def _hetatm_comp_ids(coordinate_path: str) -> set[str]:
    atoms = parse_atom_site_loop(Path(coordinate_path).read_text(encoding="utf-8"))
    return {
        a.get("label_comp_id")
        for a in atoms
        if a.get("group_PDB") == "HETATM"
        and a.get("label_comp_id") not in _NON_COFACTOR_HET
    }


def structure_confirmability(
    row: dict[str, Any], *, _het_cache: dict[str, set[str]] | None = None
) -> str:
    """Whether the deferred geometry confirmation can actually run for this row.

    ``holo``  -- coordinates contain the annotated cofactor (gate is meetable), OR a
                 sha-pinned ``holo_pdb_confirmation`` from an experimental PDB records the
                 annotated cofactor present (the experimental coordinate is regeneratable
                 from the PDB id, so the determination -- not the bulky file -- is stored).
    ``apo``   -- coordinates exist but the cofactor is absent (the gate abstains;
                 covers BOTH experimental-apo and predicted-apo -- the degradation
                 regime). Needs cofactor fusion before confirmation.
    ``none``  -- no usable coordinates staged.
    """
    # An experimental-PDB holo confirmation (recorded by holo_structure_promotion) is
    # authoritative: the annotated cofactor was found as a HETATM in a sha-pinned PDB
    # entry. The mmCIF is regeneratable from the PDB id, so the determination is honoured
    # without requiring the (uncommitted) file locally.
    holo_conf = _structure_provenance(row).get("holo_pdb_confirmation") or {}
    if (
        holo_conf.get("status") == "holo_experimental_coordinate_confirmed"
        and holo_conf.get("cofactor_comp_ids_present")
    ):
        return "holo"

    path = _structure_provenance(row).get("coordinate_path")
    if not path or not Path(path).exists():
        return "none"
    expected = expected_cofactor_comp_ids(row)
    if not expected:
        # no cofactor to look for (e.g. cofactorless ser_his) -- coordinates exist
        # but cofactor-presence is not the right confirmation axis for this row
        return "apo"
    try:
        if _het_cache is not None and path in _het_cache:
            hets = _het_cache[path]
        else:
            hets = _hetatm_comp_ids(path)
            if _het_cache is not None:
                _het_cache[path] = hets
    except Exception:  # pragma: no cover - defensive
        return "none"
    return "holo" if (hets & expected) else "apo"


def assess_promotion(
    row: dict[str, Any],
    centroids: dict[str, list[float]],
    *,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    _het_cache: dict[str, set[str]] | None = None,
) -> dict[str, Any]:
    """Promotion decision for one bronze seed label (non-destructive)."""
    chem = assess_row_against_centroids(row, centroids)
    fp = row.get("fingerprint_id")
    confirmability = structure_confirmability(row, _het_cache=_het_cache)
    agrees = chem["chemistry_agrees_with_label"]
    cohesion = chem["own_cohesion"] or 0.0

    # ser_his is cofactorless: its structural confirmation is the Ser-His-Asp triad
    # (runnable on apo too -- no cofactor needed), not cofactor presence.
    triad_confirmed = None
    has_coordinates = bool(_structure_provenance(row).get("coordinate_path")) and Path(
        _structure_provenance(row)["coordinate_path"]
    ).exists()
    if fp == "ser_his_acid_hydrolase" and has_coordinates:
        triad = assess_ser_his_candidate(row)
        triad_confirmed = triad.get("decision") == "assign_ser_his"

    if agrees is False:
        decision = "review_chemistry_disagrees"
    elif cohesion < cohesion_threshold:
        decision = "hold_low_chemistry_cohesion"
    elif fp == "ser_his_acid_hydrolase":
        if triad_confirmed:
            decision = "silver_ready_pending_geometry_run"
        elif not has_coordinates:
            decision = "blocked_pending_structure"
        else:
            decision = "hold_triad_not_confirmed"
    elif confirmability == "holo":
        # annotated cofactor is present in the coordinates -> the geometry
        # confirmation is meetable (NOT abstaining on apo)
        decision = "silver_ready_pending_geometry_run"
    elif confirmability == "apo":
        # cofactor absent (experimental-apo OR predicted-apo) -> the gate abstains;
        # needs cofactor fusion before confirmation -- the documented degradation
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

    het_cache: dict[str, set[str]] = {}
    decisions = [
        assess_promotion(
            row, centroids, cohesion_threshold=cohesion_threshold, _het_cache=het_cache
        )
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
                "the annotated cofactor is actually PRESENT in the coordinates (true "
                "holo, where the geometry gate is meetable), OR ser_his with a "
                "confirmed Ser-His-Asp triad"
            ),
            "confirmability_axis": (
                "cofactor PRESENCE in coordinates, NOT experimental-vs-predicted "
                "provenance: the documented Problem-2 degradation is apo cofactor-loss "
                "(45/45 -> 23/45; geometry inverse-gate abstains on 100% of apo). "
                "Experimental-apo and predicted-apo are both 'apo' here -- in this "
                "registry 103/104 coordinate-bearing rows are apo"
            ),
            "gating_audit_not_run_here": (
                "geometry_inverse_gate_confirmation abstains on apo coordinates; it is "
                "NOT run or faked -- silver_ready rows are staged for that "
                "confirmation as a separate authorized step"
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
