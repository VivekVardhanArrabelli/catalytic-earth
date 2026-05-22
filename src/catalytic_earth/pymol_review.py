from __future__ import annotations

import json
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_STRUCTURE_DIRS = (Path("artifacts/v3_foldseek_coordinates_1000"),)
READY_DECISIONS = {"accepted", "rejected", "skipped", "needs_more_evidence"}


def build_mcsa_pymol_expert_review_queue(
    *,
    expert_review_export: dict[str, Any],
    review_debt_summary: dict[str, Any],
    review_evidence_gaps: dict[str, Any],
    geometry_features: dict[str, Any],
    structure_dirs: list[Path] | None = None,
    max_rows: int | None = None,
    source_paths: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Build a source-bounded M-CSA visual review queue.

    The queue is intentionally conservative: a row is PyMOL-ready only when the
    committed artifacts provide a structure path, two mapped residues with CA
    atoms, and an exact measured CA distance from the geometry feature artifact.
    """

    review_items = [
        item
        for item in expert_review_export.get("review_items", [])
        if isinstance(item, dict) and isinstance(item.get("entry_id"), str)
    ]
    if max_rows is not None:
        review_items = review_items[:max_rows]
    debt_by_entry = _rows_by_entry(review_debt_summary.get("rows", []))
    gaps_by_entry = _rows_by_entry(review_evidence_gaps.get("rows", []))
    geometry_by_entry = _rows_by_entry(geometry_features.get("entries", []))
    paths = source_paths or {}
    rows: list[dict[str, Any]] = []

    for index, item in enumerate(review_items, start=1):
        entry_id = str(item["entry_id"])
        queue_context = _as_dict(item.get("queue_context"))
        debt_context = _as_dict(item.get("review_debt_context")) or debt_by_entry.get(
            entry_id, {}
        )
        gap_context = gaps_by_entry.get(entry_id, {})
        geometry = geometry_by_entry.get(entry_id, {})
        target_fingerprint_id = _first_present(
            debt_context.get("target_fingerprint_id"),
            gap_context.get("target_fingerprint_id"),
            queue_context.get("top1_fingerprint_id"),
            item.get("decision", {}).get("fingerprint_id")
            if isinstance(item.get("decision"), dict)
            else None,
        )
        structure_id = str(geometry.get("pdb_id") or "") or None
        structure_path = _find_structure_path(structure_id, structure_dirs)
        focus_pair = _select_focus_pair(geometry)
        missing_fields = _missing_fields(geometry, structure_id, structure_path, focus_pair)
        provenance = {
            "expert_review_export_path": paths.get("expert_review_export"),
            "review_debt_summary_path": paths.get("review_debt_summary"),
            "review_evidence_gaps_path": paths.get("review_evidence_gaps"),
            "geometry_features_path": paths.get("geometry_features"),
            "geometry_entry_status": geometry.get("status"),
            "focus_pair_selection_rule": (
                "longest current geometry-feature CA pair among resolved catalytic "
                "residues; this is visual-review focus evidence, not a production score"
            )
            if focus_pair
            else None,
        }
        row = {
            "rank": index,
            "entry_id": entry_id,
            "entry_name": item.get("entry_name") or geometry.get("entry_name"),
            "structure_id": structure_id,
            "structure_path": str(structure_path) if structure_path else None,
            "target_fingerprint_id": target_fingerprint_id,
            "review_reason": _review_reason(debt_context, gap_context, queue_context),
            "source_artifact_path": paths.get("expert_review_export"),
            "gap_reasons": sorted(
                {
                    str(reason)
                    for context in (debt_context, gap_context)
                    for reason in context.get("gap_reasons", [])
                    if isinstance(reason, str)
                }
            ),
            "counterevidence_reasons": sorted(
                {
                    str(reason)
                    for context in (debt_context, gap_context, queue_context)
                    for reason in context.get("counterevidence_reasons", [])
                    if isinstance(reason, str)
                }
            ),
            "catalytic_or_failed_residues": focus_pair.get("residues", [])
            if focus_pair
            else [],
            "exact_measured_distance_angstrom": focus_pair.get("distance_angstrom")
            if focus_pair
            else None,
            "heuristic_threshold_angstrom": None,
            "threshold_status": "not_available_in_input_artifacts",
            "focus_atom_pair": focus_pair.get("atom_pair") if focus_pair else None,
            "pymol_ready": not missing_fields,
            "missing_fields": missing_fields,
            "provenance": provenance,
            "countable_import_ready": False,
            "countable_import_blockers": [
                "visual_review_queue_only",
                "manual_decision_not_collected",
                "expert_review_import_preview_not_run",
                "label_factory_gates_not_run",
            ],
        }
        rows.append(row)

    counts = Counter(
        blocker
        for row in rows
        for blocker in row.get("missing_fields", [])
        if isinstance(blocker, str)
    )
    ready_rows = [row for row in rows if row.get("pymol_ready")]
    return {
        "metadata": {
            "method": "mcsa_pymol_expert_review_queue",
            "review_only": True,
            "ready_for_label_import": False,
            "import_ready_candidate_count": 0,
            "countable_label_candidate_count": 0,
            "new_external_rows_frozen": 0,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "artifact_upload_or_removal_performed": False,
            "source_paths": paths,
            "total_review_rows_scanned": len(rows),
            "rows_with_structure_paths": sum(1 for row in rows if row.get("structure_path")),
            "rows_with_exact_residue_atom_pairs": sum(
                1 for row in rows if row.get("focus_atom_pair")
            ),
            "rows_with_exact_distances": sum(
                1
                for row in rows
                if isinstance(row.get("exact_measured_distance_angstrom"), (int, float))
            ),
            "pymol_ready_count": len(ready_rows),
            "blocked_count": len(rows) - len(ready_rows),
            "missing_field_counts": dict(sorted(counts.items())),
            "ready_entry_ids": [str(row["entry_id"]) for row in ready_rows],
            "policy": (
                "This queue is a visual expert-review aid only. It imports 0 labels, "
                "edits no registries or fingerprints, and does not create countable "
                "label candidates."
            ),
        },
        "rows": rows,
    }


def write_mcsa_pymol_scripts(
    queue: dict[str, Any],
    *,
    out_dir: Path,
    max_rows: int | None = None,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ready_rows = [
        row
        for row in queue.get("rows", [])
        if isinstance(row, dict) and bool(row.get("pymol_ready"))
    ]
    if max_rows is not None:
        ready_rows = ready_rows[:max_rows]
    script_rows: list[dict[str, Any]] = []
    for row in ready_rows:
        script_path = out_dir / f"{_safe_name(str(row['entry_id']))}.pml"
        script_path.write_text(_pml_script(row), encoding="utf-8")
        row["pml_script_path"] = str(script_path)
        script_rows.append(
            {
                "entry_id": row["entry_id"],
                "structure_id": row.get("structure_id"),
                "pml_script_path": str(script_path),
            }
        )
    return {
        "metadata": {
            "method": "mcsa_pymol_script_generation",
            "review_only": True,
            "script_dir": str(out_dir),
            "ready_rows_seen": len(
                [
                    row
                    for row in queue.get("rows", [])
                    if isinstance(row, dict) and bool(row.get("pymol_ready"))
                ]
            ),
            "script_count": len(script_rows),
        },
        "rows": script_rows,
    }


def launch_mcsa_pymol_review(
    *,
    queue: dict[str, Any],
    out_path: Path,
    reviewer: str,
    dry_run: bool = False,
    no_launch: bool = False,
    max_rows: int | None = None,
    start_index: int = 0,
    pymol_bin: str = "pymol",
) -> dict[str, Any]:
    ready_rows = [
        row
        for row in queue.get("rows", [])
        if isinstance(row, dict) and bool(row.get("pymol_ready"))
    ]
    if start_index < 0:
        raise ValueError("start_index must be non-negative")
    selected = ready_rows[start_index:]
    if max_rows is not None:
        selected = selected[:max_rows]
    if not dry_run and not no_launch and shutil.which(pymol_bin) is None:
        raise RuntimeError(
            f"PyMOL executable not found: {pymol_bin}. Use --dry-run or --no-launch "
            "to exercise the review loop without launching PyMOL."
        )

    batch = _load_or_empty_decision_batch(
        out_path=out_path,
        queue=queue,
        reviewer=reviewer,
        dry_run=dry_run,
        no_launch=no_launch,
        pymol_bin=pymol_bin,
    )
    completed = {
        str(item.get("entry_id"))
        for item in batch.get("review_items", [])
        if isinstance(item, dict) and isinstance(item.get("entry_id"), str)
    }
    for row in selected:
        entry_id = str(row["entry_id"])
        if entry_id in completed:
            continue
        if dry_run:
            decision = "skipped"
            note = "dry_run_no_manual_review"
        else:
            if not no_launch:
                script_path = str(row.get("pml_script_path") or "")
                if not script_path:
                    raise RuntimeError(f"{entry_id}: missing pml_script_path")
                subprocess.run([pymol_bin, script_path], check=False)
            print(_terminal_context(row))
            decision = _prompt_decision()
            if decision == "quit":
                break
            note = input("Expert note (optional): ").strip()
        batch["review_items"].append(
            _decision_item(
                row=row,
                decision=decision,
                reviewer=reviewer,
                note=note,
                dry_run=dry_run,
            )
        )
        _write_json(out_path, _with_decision_counts(batch))
    batch = _with_decision_counts(batch)
    _write_json(out_path, batch)
    return batch


def validate_mcsa_pymol_decision_batch(batch: dict[str, Any]) -> dict[str, Any]:
    rows = batch.get("review_items", [])
    if not isinstance(rows, list):
        raise ValueError("review_items must be a list")
    bad_decisions: list[str] = []
    import_ready_rows: list[str] = []
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("review item must be an object")
        entry_id = str(row.get("entry_id") or "")
        decision = str(row.get("decision") or "")
        if decision not in READY_DECISIONS:
            bad_decisions.append(entry_id or "<missing-entry>")
        if bool(row.get("countable_import_ready")):
            import_ready_rows.append(entry_id or "<missing-entry>")
    if bad_decisions:
        raise ValueError(f"invalid decisions for entries: {bad_decisions}")
    if import_ready_rows:
        raise ValueError(f"PyMOL manual batch cannot be countable-ready: {import_ready_rows}")
    return {
        "metadata": {
            "method": "mcsa_pymol_manual_decision_batch_validation",
            "valid": True,
            "review_only": True,
            "ready_for_label_import": False,
            "review_item_count": len(rows),
            "import_ready_candidate_count": 0,
            "countable_label_candidate_count": 0,
            "countable_import_ready_count": 0,
            "new_external_rows_frozen": 0,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "artifact_upload_or_removal_performed": False,
        }
    }


def _rows_by_entry(rows: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        return {}
    return {
        str(row["entry_id"]): row
        for row in rows
        if isinstance(row, dict) and isinstance(row.get("entry_id"), str)
    }


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _first_present(*values: Any) -> Any:
    for value in values:
        if value is not None and value != "":
            return value
    return None


def _find_structure_path(
    structure_id: str | None, structure_dirs: list[Path] | None
) -> Path | None:
    if not structure_id:
        return None
    pdb_id = structure_id.upper()
    candidate_dirs = structure_dirs if structure_dirs is not None else list(DEFAULT_STRUCTURE_DIRS)
    names = [f"pdb_{pdb_id}.cif", f"{pdb_id}.cif", f"pdb_{pdb_id}.pdb", f"{pdb_id}.pdb"]
    for directory in candidate_dirs:
        for name in names:
            path = directory / name
            if path.exists():
                return path
    return None


def _select_focus_pair(geometry: dict[str, Any]) -> dict[str, Any] | None:
    residues = {
        str(residue.get("residue_node_id")): residue
        for residue in geometry.get("residues", [])
        if isinstance(residue, dict) and residue.get("residue_node_id")
    }
    pairs = [
        pair
        for pair in geometry.get("pairwise_distances_angstrom", [])
        if isinstance(pair, dict)
        and isinstance(pair.get("distance"), (int, float))
        and str(pair.get("left")) in residues
        and str(pair.get("right")) in residues
    ]
    pairs.sort(
        key=lambda pair: (
            float(pair["distance"]),
            str(pair.get("left")),
            str(pair.get("right")),
        ),
        reverse=True,
    )
    for pair in pairs:
        left = residues[str(pair["left"])]
        right = residues[str(pair["right"])]
        if not left.get("ca") or not right.get("ca"):
            continue
        left_residue = _residue_payload(left)
        right_residue = _residue_payload(right)
        return {
            "distance_angstrom": round(float(pair["distance"]), 3),
            "coordinate_type": "ca",
            "residues": [left_residue, right_residue],
            "atom_pair": {
                "left": {**left_residue, "atom_name": "CA"},
                "right": {**right_residue, "atom_name": "CA"},
                "distance_angstrom": round(float(pair["distance"]), 3),
                "distance_source_field": "pairwise_distances_angstrom",
            },
        }
    return None


def _residue_payload(residue: dict[str, Any]) -> dict[str, Any]:
    code = str(residue.get("code") or "").upper()
    return {
        "residue_node_id": residue.get("residue_node_id"),
        "chain_name": residue.get("chain_name"),
        "residue_name": code,
        "residue_number": residue.get("resid"),
        "roles": list(residue.get("roles", []))
        if isinstance(residue.get("roles"), list)
        else [],
    }


def _missing_fields(
    geometry: dict[str, Any],
    structure_id: str | None,
    structure_path: Path | None,
    focus_pair: dict[str, Any] | None,
) -> list[str]:
    missing: list[str] = []
    if not geometry:
        missing.append("missing_geometry_entry")
    if not structure_id:
        missing.append("missing_structure_id")
    if structure_id and structure_path is None:
        missing.append("missing_structure_path")
    if not focus_pair:
        missing.append("missing_exact_ca_atom_pair")
        missing.append("missing_exact_distance")
    else:
        for side in ("left", "right"):
            residue = focus_pair["atom_pair"][side]
            for field in ("chain_name", "residue_number", "residue_name", "atom_name"):
                if residue.get(field) in {None, ""}:
                    missing.append(f"missing_{side}_{field}")
    return sorted(set(missing))


def _review_reason(
    debt_context: dict[str, Any],
    gap_context: dict[str, Any],
    queue_context: dict[str, Any],
) -> str:
    pieces = []
    for context in (debt_context, gap_context):
        for reason in context.get("gap_reasons", []):
            if isinstance(reason, str):
                pieces.append(reason)
    for reason in queue_context.get("readiness_blockers", []):
        if isinstance(reason, str):
            pieces.append(reason)
    if not pieces and isinstance(debt_context.get("recommended_next_action"), str):
        pieces.append(debt_context["recommended_next_action"])
    if not pieces:
        pieces.append("expert_label_decision_needed")
    return "; ".join(dict.fromkeys(pieces))


def _pml_script(row: dict[str, Any]) -> str:
    object_name = _safe_name(str(row["entry_id"]))
    pair = row["focus_atom_pair"]
    left = pair["left"]
    right = pair["right"]
    left_sel = _residue_selection(object_name, left)
    right_sel = _residue_selection(object_name, right)
    left_atom = f"({left_sel} and name {left['atom_name']})"
    right_atom = f"({right_sel} and name {right['atom_name']})"
    distance = pair["distance_angstrom"]
    return "\n".join(
        [
            f'load "{row["structure_path"]}", {object_name}',
            "hide everything",
            f"show cartoon, {object_name}",
            f"color gray70, {object_name}",
            f"set cartoon_transparency, 0.8, {object_name}",
            f"select {object_name}_left, {left_sel}",
            f"select {object_name}_right, {right_sel}",
            f"show sticks, {object_name}_left or {object_name}_right",
            f"color tv_red, {object_name}_left",
            f"color tv_blue, {object_name}_right",
            f"distance {object_name}_distance, {left_atom}, {right_atom}",
            f"label {object_name}_distance, \"{distance:.3f} A\"",
            f"zoom {object_name}_left or {object_name}_right, 8",
            "set dash_width, 3",
            "set label_size, 18",
            "",
        ]
    )


def _residue_selection(object_name: str, residue: dict[str, Any]) -> str:
    chain = str(residue.get("chain_name") or "")
    resi = str(residue.get("residue_number") or "")
    resn = str(residue.get("residue_name") or "").upper()
    parts = [object_name]
    if chain:
        parts.append(f"chain {chain}")
    if resi:
        parts.append(f"resi {resi}")
    if resn:
        parts.append(f"resn {resn}")
    return " and ".join(parts)


def _safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_") or "row"


def _load_or_empty_decision_batch(
    *,
    out_path: Path,
    queue: dict[str, Any],
    reviewer: str,
    dry_run: bool,
    no_launch: bool,
    pymol_bin: str,
) -> dict[str, Any]:
    if out_path.exists():
        with out_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, dict):
            metadata = dict(payload.get("metadata", {}))
            metadata.update(
                {
                    "review_only": True,
                    "ready_for_label_import": False,
                    "import_ready_candidate_count": 0,
                    "countable_label_candidate_count": 0,
                    "new_external_rows_frozen": 0,
                    "curated_label_registry_edited": False,
                    "fingerprint_registry_edited": False,
                    "artifact_upload_or_removal_performed": False,
                }
            )
            payload["metadata"] = metadata
            return payload
    return {
        "metadata": {
            "method": "mcsa_pymol_manual_decision_batch",
            "review_only": True,
            "ready_for_label_import": False,
            "import_ready_candidate_count": 0,
            "countable_label_candidate_count": 0,
            "new_external_rows_frozen": 0,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "artifact_upload_or_removal_performed": False,
            "reviewer": reviewer,
            "reviewed_at": _now_iso(),
            "input_queue_method": queue.get("metadata", {}).get("method"),
            "dry_run": dry_run,
            "no_launch": no_launch,
            "pymol_bin": pymol_bin,
            "policy": (
                "Manual PyMOL decisions default to countable_import_ready=false. "
                "They must be converted through existing expert-review import "
                "previews and label-factory gates before any countable label action."
            ),
        },
        "review_items": [],
    }


def _decision_item(
    *,
    row: dict[str, Any],
    decision: str,
    reviewer: str,
    note: str,
    dry_run: bool,
) -> dict[str, Any]:
    if decision not in READY_DECISIONS:
        raise ValueError(f"invalid decision: {decision}")
    return {
        "entry_id": row["entry_id"],
        "entry_name": row.get("entry_name"),
        "structure_id": row.get("structure_id"),
        "structure_path": row.get("structure_path"),
        "decision": decision,
        "reviewer": reviewer,
        "reviewed_at": _now_iso(),
        "expert_note": note,
        "dry_run": dry_run,
        "visual_evidence": {
            "pml_script_path": row.get("pml_script_path"),
            "focus_atom_pair": row.get("focus_atom_pair"),
            "exact_measured_distance_angstrom": row.get("exact_measured_distance_angstrom"),
            "review_queue_rank": row.get("rank"),
        },
        "countable_import_ready": False,
        "countable_import_blockers": [
            "manual_visual_review_context_only",
            "expert_review_import_preview_not_run",
            "label_factory_gates_not_run",
        ],
    }


def _with_decision_counts(batch: dict[str, Any]) -> dict[str, Any]:
    counts = Counter(
        str(row.get("decision"))
        for row in batch.get("review_items", [])
        if isinstance(row, dict)
    )
    metadata = dict(batch.get("metadata", {}))
    metadata["decision_counts"] = dict(sorted(counts.items()))
    metadata["review_item_count"] = len(batch.get("review_items", []))
    metadata["countable_import_ready_count"] = sum(
        1
        for row in batch.get("review_items", [])
        if isinstance(row, dict) and bool(row.get("countable_import_ready"))
    )
    batch["metadata"] = metadata
    return batch


def _terminal_context(row: dict[str, Any]) -> str:
    return (
        f"[{row.get('rank')}] {row.get('entry_id')} {row.get('entry_name')}\n"
        f"target={row.get('target_fingerprint_id')} "
        f"distance={row.get('exact_measured_distance_angstrom')} "
        f"threshold={row.get('heuristic_threshold_angstrom')}\n"
        f"reason={row.get('review_reason')}"
    )


def _prompt_decision() -> str:
    prompt = "Decision [a]ccept/[r]eject/[s]kip/[m]ore evidence/[q]uit: "
    while True:
        raw = input(prompt).strip().lower()
        if raw in {"a", "accept", "accepted"}:
            return "accepted"
        if raw in {"r", "reject", "rejected"}:
            return "rejected"
        if raw in {"s", "skip", "skipped"}:
            return "skipped"
        if raw in {"m", "more", "needs_more_evidence"}:
            return "needs_more_evidence"
        if raw in {"q", "quit"}:
            return "quit"
        print("Enter a, r, s, m, or q.")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
