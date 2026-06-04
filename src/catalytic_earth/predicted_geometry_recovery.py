"""Leakage-safe in-distribution predicted-apo recovery harness.

The headline degradation (clean experimental 45/45 -> AlphaFoldDB predicted
23/45 primary) is a heldout number, and the heldout read is one-shot. This
harness reproduces the SAME degradation-and-recovery question on the
in-distribution rows, which are never the one-shot benchmark, so the method can
be developed to convergence before any heldout read is spent.

For each in-distribution atlas row it scores the hand mechanism router three
ways and compares:

1. experimental geometry  (holo; the upper baseline)
2. predicted-apo geometry (AlphaFoldDB; no cofactor in the active site)
3. cofactor-fused geometry (predicted-apo + the sequence cofactor-presence
   channel injected into ligand_context, exactly where the experimental
   ligand context used to plug in)

The router classifies active-site geometry against the eight mechanism
fingerprint templates, so there is no per-row self-match: the experimental minus
predicted delta isolates the coordinate-source (apo) cost, and the fused minus
predicted delta isolates the recovery, with any template-membership optimism
cancelling in the deltas.

Honesty guardrail: the cofactor channel was fit on the train split, so its
predictions are in-sample for train rows. The headline recovery is therefore
reported on the **calibration** rows (out-of-sample for the channel); train rows
are reported separately as an in-sample reference only. Heldout rows are never
scored here.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .geometry_retrieval import run_geometry_retrieval
from .predicted_geometry_robustness import (
    HAND_ROUTER_THRESHOLD,
    build_alphafold_predicted_geometry_features,
    _hand_router_rows,
    _target_manifest_row_selection,
)
from .sequence_cofactor_channel import (
    _fused_geometry_features,
    _sequence_supported_suppression_rows,
)


DEFAULT_STAGED_ATLAS_DIR = (
    "artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/"
    "atlas_in_distribution"
)
DEFAULT_ALPHAFOLD_VERSION = "6"


def staged_cif_fetcher(staged_dir: Path, *, version_tag: str = "v6"):
    """Return a fetcher reading local AlphaFoldDB CIFs from a staged directory.

    The network path to AlphaFoldDB returns HTTP 403 in this environment, so the
    predicted coordinates are read from the already-staged atlas bundle. The
    fetcher matches the ``build_alphafold_predicted_geometry_features`` contract:
    ``fetch(accession, version=...) -> (text, meta)``.
    """

    staged_dir = Path(staged_dir)

    def fetch(accession: str, *, version: str = "auto", timeout: int = 30):
        cleaned = str(accession).strip()
        path = staged_dir / f"afdb_{cleaned}_{version_tag}.cif"
        if not path.exists():
            raise RuntimeError(f"no staged predicted CIF for {cleaned} at {path}")
        text = path.read_text(encoding="utf-8")
        return text, {
            "backend": "staged_local_alphafold",
            "accession": cleaned,
            "staged_path": str(path),
        }

    return fetch


# --- Context-reconstruction adapters -------------------------------------
# The harness is parameterized by the reconstruction context type. An adapter
# pair plugs a sequence -> active-site-context channel into the router: a fusion
# adapter injects the channel's predictions into the predicted geometry, and a
# suppression adapter abstains calls whose required context the channel does not
# support. The defaults below are the cofactor instantiation (the demonstrated
# case). A new context type (substrate, PTM, interface, an ion outside the
# current cofactor classes, ...) supplies its own adapter pair of the same shape
# and reuses everything else in this module unchanged.


def _default_context_fusion(
    predicted_geometry: dict[str, Any], channel: dict[str, Any]
) -> dict[str, Any]:
    """Cofactor fusion adapter: inject predicted cofactor families into ligand_context."""
    return _fused_geometry_features(
        predicted_geometry=predicted_geometry, cofactor_channel=channel
    )


def _default_unsupported_suppression(
    rows: list[dict[str, Any]], channel: dict[str, Any]
) -> list[dict[str, Any]]:
    """Cofactor suppression adapter: abstain calls needing an unsupported cofactor family."""
    return _sequence_supported_suppression_rows(rows=rows, cofactor_channel=channel)


def write_in_distribution_predicted_geometry_recovery(
    *,
    label_manifest_path: Path,
    graph_path: Path,
    experimental_geometry_features_path: Path,
    split_manifest_path: Path,
    reconstruction_channel_path: Path,
    staged_atlas_dir: Path,
    out_path: Path,
    report_path: Path | None = None,
    context_label: str = "cofactor",
    threshold: float = HAND_ROUTER_THRESHOLD,
    alphafold_version: str = DEFAULT_ALPHAFOLD_VERSION,
) -> dict[str, Any]:
    audit = build_in_distribution_predicted_geometry_recovery(
        label_manifest=_load_json(label_manifest_path),
        graph=_load_json(graph_path),
        experimental_geometry_features=_load_json(experimental_geometry_features_path),
        split_manifest=_load_json(split_manifest_path),
        reconstruction_channel=_load_json(reconstruction_channel_path),
        staged_atlas_dir=Path(staged_atlas_dir),
        context_label=context_label,
        threshold=threshold,
        alphafold_version=alphafold_version,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_recovery_report(audit), encoding="utf-8")
    return audit


def build_in_distribution_predicted_geometry_recovery(
    *,
    label_manifest: dict[str, Any],
    graph: dict[str, Any],
    experimental_geometry_features: dict[str, Any],
    split_manifest: dict[str, Any],
    reconstruction_channel: dict[str, Any],
    staged_atlas_dir: Path,
    context_label: str = "cofactor",
    fuse_context=_default_context_fusion,
    suppress_unsupported=_default_unsupported_suppression,
    threshold: float = HAND_ROUTER_THRESHOLD,
    alphafold_version: str = DEFAULT_ALPHAFOLD_VERSION,
) -> dict[str, Any]:
    target_rows, _excluded = _target_manifest_row_selection(
        label_manifest=label_manifest,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        split_assignment="in_distribution",
        max_rows=0,
    )
    atlas_rows = [
        row
        for row in target_rows
        if (row.get("fingerprint_id") or row.get("mechanism_fingerprint_id"))
    ]

    predicted_geometry = build_alphafold_predicted_geometry_features(
        label_manifest_rows=atlas_rows,
        graph=graph,
        experimental_geometry_features=experimental_geometry_features,
        alphafold_version=alphafold_version,
        fetcher=staged_cif_fetcher(Path(staged_atlas_dir)),
    )
    predicted_retrieval = run_geometry_retrieval(predicted_geometry)
    fused_geometry = fuse_context(predicted_geometry, reconstruction_channel)
    fused_retrieval = run_geometry_retrieval(fused_geometry)
    experimental_retrieval = run_geometry_retrieval(experimental_geometry_features)

    # No wave1 heldout masks are used: in-distribution rows fall back to their
    # benchmark_role, and passing an empty audit guarantees no heldout leakage.
    empty_wave_audit: dict[str, Any] = {}
    exp_rows = _hand_router_rows(
        target_rows=atlas_rows,
        predicted_geometry=experimental_geometry_features,
        predicted_retrieval=experimental_retrieval,
        wave1_audit=empty_wave_audit,
        threshold=threshold,
    )
    apo_rows = _hand_router_rows(
        target_rows=atlas_rows,
        predicted_geometry=predicted_geometry,
        predicted_retrieval=predicted_retrieval,
        wave1_audit=empty_wave_audit,
        threshold=threshold,
    )
    fused_rows = _hand_router_rows(
        target_rows=atlas_rows,
        predicted_geometry=fused_geometry,
        predicted_retrieval=fused_retrieval,
        wave1_audit=empty_wave_audit,
        threshold=threshold,
    )
    suppressed_rows = suppress_unsupported(fused_rows, reconstruction_channel)

    split_by_entry = _split_assignment(split_manifest)
    per_entry = _per_entry_transitions(
        exp_rows=exp_rows,
        apo_rows=apo_rows,
        fused_rows=fused_rows,
        suppressed_rows=suppressed_rows,
        split_by_entry=split_by_entry,
    )
    readouts = _readouts_by_split(per_entry)

    return {
        "artifact_id": "v3_in_distribution_predicted_geometry_recovery_current702_20260604",
        "schema_version": "in_distribution_predicted_geometry_recovery.v1",
        "created_utc": _utc_now_iso(),
        "status": "complete",
        "guardrails": {
            "split_assignment_scored": "in_distribution",
            "heldout_rows_scored": False,
            "heldout_labels_read": False,
            "context_label": context_label,
            "reconstruction_channel_input": (
                "sequence-derived active-site context presence only"
            ),
            "experimental_ligands_used_for_fused_surface": False,
            "router_against_fingerprint_templates_no_per_row_self_match": True,
            "headline_recovery_is_out_of_sample_calibration_only": True,
            "global_threshold_changed": False,
            "production_scoring_changed": False,
        },
        "scope": {
            "threshold": threshold,
            "alphafold_version": alphafold_version,
            "context_label": context_label,
            "atlas_target_row_count": len(atlas_rows),
            "predicted_geometry_ok_count": sum(
                1
                for entry in predicted_geometry.get("entries", [])
                if entry.get("status") == "ok"
            ),
            "staged_atlas_dir": str(staged_atlas_dir),
            "reconstruction_channel_artifact_id": reconstruction_channel.get("artifact_id"),
        },
        "interpretation": (
            "Calibration is the honest out-of-sample readout. Read "
            "experimental_correct -> apo_correct as the in-distribution analog of "
            "the heldout 45->23 drop, and apo_correct -> fused_correct as the "
            f"sequence {context_label} reconstruction-channel recovery."
        ),
        "readouts_by_split": readouts,
        "per_entry": per_entry,
    }


def _per_entry_transitions(
    *,
    exp_rows: list[dict[str, Any]],
    apo_rows: list[dict[str, Any]],
    fused_rows: list[dict[str, Any]],
    suppressed_rows: list[dict[str, Any]],
    split_by_entry: dict[str, str],
) -> list[dict[str, Any]]:
    exp_by = {row["entry_id"]: row for row in exp_rows}
    apo_by = {row["entry_id"]: row for row in apo_rows}
    fused_by = {row["entry_id"]: row for row in fused_rows}
    suppressed_by = {row["entry_id"]: row for row in suppressed_rows}
    rows: list[dict[str, Any]] = []
    for entry_id, exp in sorted(exp_by.items(), key=lambda item: _entry_sort_key(item[0])):
        apo = apo_by.get(entry_id, {})
        fused = fused_by.get(entry_id, {})
        suppressed = suppressed_by.get(entry_id, {})
        exp_correct = bool(exp.get("exact_label_match"))
        apo_correct = bool(apo.get("exact_label_match"))
        fused_correct = bool(fused.get("exact_label_match"))
        suppressed_correct = bool(suppressed.get("exact_label_match"))
        rows.append(
            {
                "entry_id": entry_id,
                "embedding_split": split_by_entry.get(entry_id),
                "true_fingerprint_id": exp.get("true_fingerprint_id"),
                "experimental": _surface_cell(exp),
                "apo": _surface_cell(apo),
                "fused": _surface_cell(fused),
                "fused_suppressed": _surface_cell(suppressed),
                "experimental_correct": exp_correct,
                "apo_correct": apo_correct,
                "fused_correct": fused_correct,
                "fused_suppressed_correct": suppressed_correct,
                "apo_lost_primary": exp_correct and not apo_correct,
                "fused_recovered": exp_correct and not apo_correct and fused_correct,
                "fused_regressed": apo_correct and not fused_correct,
            }
        )
    return rows


def _surface_cell(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "called_fingerprint_id": row.get("called_fingerprint_id"),
        "top1_fingerprint_id": row.get("top1_fingerprint_id"),
        "top1_score": row.get("top1_score"),
        "abstained": row.get("abstained"),
        "exact_label_match": row.get("exact_label_match"),
    }


def _readouts_by_split(per_entry: list[dict[str, Any]]) -> dict[str, Any]:
    splits: dict[str, list[dict[str, Any]]] = {}
    for row in per_entry:
        splits.setdefault(str(row.get("embedding_split") or "uncovered"), []).append(row)
    readouts: dict[str, Any] = {}
    for split, rows in sorted(splits.items()):
        n = len(rows)
        exp_c = sum(1 for r in rows if r["experimental_correct"])
        apo_c = sum(1 for r in rows if r["apo_correct"])
        fused_c = sum(1 for r in rows if r["fused_correct"])
        supp_c = sum(1 for r in rows if r["fused_suppressed_correct"])
        apo_lost = sum(1 for r in rows if r["apo_lost_primary"])
        recovered = sum(1 for r in rows if r["fused_recovered"])
        regressed = sum(1 for r in rows if r["fused_regressed"])
        readouts[split] = {
            "row_count": n,
            "is_out_of_sample_for_cofactor_channel": split in {"calibration", "uncovered"},
            "experimental_correct": exp_c,
            "apo_correct": apo_c,
            "fused_correct": fused_c,
            "fused_suppressed_correct": supp_c,
            "apo_primary_drop": exp_c - apo_c,
            "apo_lost_primary_rows": apo_lost,
            "fused_recovered_rows": recovered,
            "fused_regressed_rows": regressed,
            "net_fused_gain_over_apo": fused_c - apo_c,
            "recovery_fraction_of_apo_loss": (
                round(recovered / apo_lost, 4) if apo_lost else None
            ),
        }
    return readouts


def _split_assignment(split_manifest: dict[str, Any]) -> dict[str, str]:
    assignment: dict[str, str] = {}
    for record in split_manifest.get("split_records", []):
        if not isinstance(record, dict):
            continue
        entry_id = record.get("entry_id")
        split = record.get("assigned_embedding_split")
        if entry_id and split:
            assignment[str(entry_id)] = str(split)
    return assignment


def _recovery_report(audit: dict[str, Any]) -> str:
    scope = audit["scope"]
    lines = [
        "# In-Distribution Predicted-Apo Recovery (leakage-safe)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Leakage-safe analog of the heldout 45/45 -> predicted 23/45 drop, scored on",
        "in-distribution rows. Calibration is the honest out-of-sample readout for the",
        "cofactor channel; train is an in-sample reference only; heldout is never read.",
        "",
        f"- Atlas target rows: {scope['atlas_target_row_count']}; predicted-geometry ok:",
        f"  {scope['predicted_geometry_ok_count']}; threshold {scope['threshold']}.",
        f"- Reconstruction context: {scope['context_label']}; channel:",
        f"  {scope['reconstruction_channel_artifact_id']}.",
        "",
        "## Recovery by split",
        "",
        "| Split | OOS? | N | exp ok | apo ok | apo drop | fused ok | recovered/lost | regressed |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | :---: | ---: |",
    ]
    for split, r in audit["readouts_by_split"].items():
        lines.append(
            f"| {split} | {'yes' if r['is_out_of_sample_for_cofactor_channel'] else 'no'} | "
            f"{r['row_count']} | {r['experimental_correct']} | {r['apo_correct']} | "
            f"{r['apo_primary_drop']} | {r['fused_correct']} | "
            f"{r['fused_recovered_rows']}/{r['apo_lost_primary_rows']} | "
            f"{r['fused_regressed_rows']} |"
        )
    lines.extend(
        [
            "",
            "## How to read",
            "",
            "- `apo drop` = experimental-correct minus apo-correct (the coordinate-source cost).",
            "- `recovered/lost` = apo-lost primaries that the cofactor-fused router brings back.",
            "- `regressed` = rows correct under apo that fusion breaks (the over-opening cost).",
            "- The calibration row is the deployment-honest estimate; train over-states recovery",
            "  because the channel was fit on those rows.",
            "",
        ]
    )
    return "\n".join(lines)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _entry_sort_key(entry_id: str) -> tuple[str, int, str]:
    prefix, _, suffix = str(entry_id).partition(":")
    digits = "".join(ch for ch in suffix if ch.isdigit())
    return (prefix, int(digits) if digits else -1, suffix)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
