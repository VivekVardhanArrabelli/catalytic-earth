from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Callable


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
        atom_presence = _focus_atom_presence(structure_path, focus_pair)
        missing_fields = _missing_fields(
            geometry, structure_id, structure_path, focus_pair, atom_presence
        )
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
            "focus_atom_selection_verified": atom_presence.get("both_present")
            if atom_presence
            else False,
            "focus_atom_selection_presence": atom_presence or None,
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
            "rows_with_verified_focus_atoms": sum(
                1 for row in rows if row.get("focus_atom_selection_verified")
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


def select_mcsa_pymol_materialization_tranche(
    *,
    blocker_report: dict[str, Any],
    max_rows: int = 25,
    tranche_id: str = "next",
    source_blocker_report_path: str | None = None,
) -> dict[str, Any]:
    candidates = [
        row
        for row in blocker_report.get("next_structure_materialization_candidates", [])
        if isinstance(row, dict)
    ][:max_rows]
    rows: list[dict[str, Any]] = []
    for row in candidates:
        rows.append(
            {
                "rank": row.get("rank"),
                "entry_id": row.get("entry_id"),
                "entry_name": row.get("entry_name"),
                "structure_id": row.get("structure_id"),
                "target_fingerprint_id": row.get("target_fingerprint_id"),
                "exact_measured_distance_angstrom": row.get(
                    "exact_measured_distance_angstrom"
                ),
                "missing_fields": list(row.get("missing_fields", []))
                if isinstance(row.get("missing_fields"), list)
                else [],
                "selection_reason": (
                    f"{tranche_id} bounded tranche from the prior remaining-blocker "
                    "report: highest-priority blocked rows with exact CA pair/distance "
                    "and missing local structure path"
                ),
                "next_action": (
                    "materialize PDB mmCIF into a committed review-only structure "
                    "directory and rerun the PyMOL queue"
                ),
            }
        )

    return {
        "metadata": {
            "artifact_id": f"v3_mcsa_pymol_{tranche_id}_materialization_tranche_selection",
            "method": f"mcsa_pymol_{tranche_id}_structure_materialization_tranche_selection",
            "created_at": _now_iso(),
            "review_only": True,
            "ready_for_label_import": False,
            "import_ready_candidate_count": 0,
            "countable_label_candidate_count": 0,
            "new_external_rows_frozen": 0,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "artifact_upload_or_removal_performed": False,
            "selected_row_count": len(rows),
            "selected_entry_ids": [str(row.get("entry_id")) for row in rows],
            "selected_structure_ids": [str(row.get("structure_id")) for row in rows],
            "selection_policy": (
                "freeze the next structure-materialization candidates named by the "
                "prior blocker report before fetching or rescoring"
            ),
            "source_blocker_report": source_blocker_report_path,
        },
        "rows": rows,
    }


def materialize_mcsa_pymol_structure_tranche(
    *,
    selection: dict[str, Any],
    coordinate_output_dir: Path,
    source_selection_artifact: str | None = None,
    tranche_id: str = "next",
    fetcher: Callable[[str], bytes] | None = None,
) -> dict[str, Any]:
    coordinate_output_dir.mkdir(parents=True, exist_ok=True)
    fetch = fetcher or _download_bytes
    rows: list[dict[str, Any]] = []

    for selected in selection.get("rows", []):
        if not isinstance(selected, dict):
            continue
        structure_id = str(selected.get("structure_id") or "").upper()
        url = f"https://files.rcsb.org/download/{structure_id}.cif"
        local_path = coordinate_output_dir / f"pdb_{structure_id}.cif"
        row = {
            **selected,
            "coordinate_source_url": url,
            "local_structure_path": str(local_path),
        }
        try:
            data = local_path.read_bytes() if local_path.exists() else fetch(url)
            if not data:
                raise ValueError("download returned no bytes")
            data = _normalize_mmcif_bytes(data)
            local_path.write_bytes(data)
            text = data.decode("utf-8", errors="replace")
            first_line = text.splitlines()[0] if text.splitlines() else ""
            if not first_line.startswith("data_"):
                raise ValueError("downloaded coordinate file is not an mmCIF data block")
            row.update(
                {
                    "coordinate_normalized": True,
                    "materialization_status": "materialized",
                    "sha256": sha256(data).hexdigest(),
                    "size_bytes": len(data),
                    "first_line": first_line,
                }
            )
        except Exception as exc:  # pragma: no cover - exact network failures vary.
            row.update(
                {
                    "materialization_status": "failed",
                    "error": str(exc),
                    "sha256": None,
                    "size_bytes": 0,
                    "first_line": None,
                }
            )
        rows.append(row)

    materialized = [
        row for row in rows if row.get("materialization_status") == "materialized"
    ]
    failed = [row for row in rows if row.get("materialization_status") == "failed"]
    return {
        "metadata": {
            "artifact_id": f"v3_mcsa_pymol_{tranche_id}_materialization_tranche",
            "method": f"mcsa_pymol_{tranche_id}_selected_pdb_coordinate_materialization",
            "created_at": _now_iso(),
            "review_only": True,
            "ready_for_label_import": False,
            "import_ready_candidate_count": 0,
            "countable_label_candidate_count": 0,
            "new_external_rows_frozen": 0,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "artifact_upload_or_removal_performed": False,
            "removal_allowed": False,
            "selected_row_count": len(rows),
            "materialized_count": len(materialized),
            "failed_count": len(failed),
            "materialized_entry_ids": [
                str(row.get("entry_id")) for row in materialized
            ],
            "materialized_structure_ids": [
                str(row.get("structure_id")) for row in materialized
            ],
            "coordinate_output_dir": str(coordinate_output_dir),
            "fetch_source": "RCSB PDB mmCIF download endpoint",
            "source_selection_artifact": source_selection_artifact,
            "coordinate_normalization": "utf8_line_trailing_whitespace_stripped_lf",
            "policy": (
                "Bounded review-only coordinate staging for M-CSA PyMOL inspection; "
                "no labels, registries, production scores, upload, removal, or "
                "countable imports are authorized."
            ),
        },
        "rows": rows,
    }


def build_mcsa_pymol_remaining_blocker_report(
    *,
    queue: dict[str, Any],
    source_queue_path: str | None = None,
    max_next_tranche_rows: int = 25,
    max_exact_blocker_sample: int = 25,
    tranche_id: str = "next",
) -> dict[str, Any]:
    rows = [
        row for row in queue.get("rows", []) if isinstance(row, dict)
    ]
    blocked = [row for row in rows if not row.get("pymol_ready")]
    next_candidates: list[dict[str, Any]] = []
    structure_id_blockers: list[dict[str, Any]] = []
    exact_pair_blockers: list[dict[str, Any]] = []

    for row in blocked:
        missing = set(row.get("missing_fields", []))
        common = _blocker_row_common(row)
        if (
            "missing_structure_path" in missing
            and "missing_structure_id" not in missing
            and "missing_exact_ca_atom_pair" not in missing
            and "missing_exact_distance" not in missing
            and len(next_candidates) < max_next_tranche_rows
        ):
            next_candidates.append(
                {
                    **common,
                    "next_action": (
                        "materialize PDB mmCIF into a committed review-only structure "
                        "directory and rerun the PyMOL queue"
                    ),
                }
            )
        if "missing_structure_id" in missing:
            structure_id_blockers.append(
                {
                    **common,
                    "exact_blocker": (
                        "geometry artifact has no PDB id; needs source graph/PDB "
                        "mapping repair before PyMOL staging"
                    ),
                }
            )
        if (
            "missing_exact_ca_atom_pair" in missing
            or "missing_exact_distance" in missing
        ) and len(exact_pair_blockers) < max_exact_blocker_sample:
            exact_pair_blockers.append(
                {
                    **common,
                    "exact_blocker": (
                        "geometry artifact lacks a resolved CA atom pair/distance "
                        "for the visual focus; needs residue/atom mapping repair "
                        "before PyMOL readiness"
                    ),
                }
            )

    metadata = dict(queue.get("metadata", {}))
    missing_counts = metadata.get("missing_field_counts", {})
    return {
        "metadata": {
            "artifact_id": f"v3_mcsa_pymol_remaining_blocker_report_after_{tranche_id}_materialization",
            "method": f"mcsa_pymol_remaining_readiness_blocker_report_after_{tranche_id}_tranche",
            "created_at": _now_iso(),
            "review_only": True,
            "ready_for_label_import": False,
            "import_ready_candidate_count": 0,
            "countable_label_candidate_count": 0,
            "new_external_rows_frozen": 0,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "artifact_upload_or_removal_performed": False,
            "removal_allowed": False,
            "source_queue": source_queue_path,
            "total_review_rows_scanned": metadata.get("total_review_rows_scanned"),
            "pymol_ready_count": metadata.get("pymol_ready_count"),
            "rows_with_verified_focus_atoms": metadata.get(
                "rows_with_verified_focus_atoms"
            ),
            "blocked_count": metadata.get("blocked_count"),
            "next_tranche_candidate_count": len(next_candidates),
            "missing_field_counts": missing_counts,
            "missing_structure_id_count": int(missing_counts.get("missing_structure_id", 0))
            if isinstance(missing_counts, dict)
            else 0,
            "missing_exact_pair_or_distance_count": max(
                int(missing_counts.get("missing_exact_ca_atom_pair", 0)),
                int(missing_counts.get("missing_exact_distance", 0)),
            )
            if isinstance(missing_counts, dict)
            else 0,
            "decision": (
                "human_review_ready_rows_or_continue_bounded_structure_materialization; "
                "no labels or imports authorized"
            ),
        },
        "next_structure_materialization_candidates": next_candidates,
        "structure_id_mapping_blockers": structure_id_blockers,
        "exact_atom_pair_mapping_blockers_sample": exact_pair_blockers,
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
    atom_presence: dict[str, Any] | None = None,
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
            if atom_presence and not atom_presence.get(f"{side}_present"):
                missing.append(f"missing_{side}_structure_atom")
    return sorted(set(missing))


def _focus_atom_presence(
    structure_path: Path | None, focus_pair: dict[str, Any] | None
) -> dict[str, Any]:
    if structure_path is None or not focus_pair:
        return {}
    atoms = _load_structure_atom_keys(structure_path)
    presence = {
        side: _atom_key(focus_pair["atom_pair"][side]) in atoms
        for side in ("left", "right")
    }
    return {
        "structure_path": str(structure_path),
        "left_present": presence["left"],
        "right_present": presence["right"],
        "both_present": presence["left"] and presence["right"],
        "match_policy": (
            "structure file must contain the requested atom name, residue name, "
            "chain id, and residue number using PDB fixed fields or mmCIF "
            "auth/label atom-site fields"
        ),
    }


def _load_structure_atom_keys(path: Path) -> set[tuple[str, str, str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    suffix = path.suffix.lower()
    if suffix in {".pdb", ".ent"}:
        return _pdb_atom_keys(text)
    return _mmcif_atom_keys(text)


def _atom_key(atom: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(atom.get("atom_name") or "").strip().upper(),
        str(atom.get("residue_name") or "").strip().upper(),
        str(atom.get("chain_name") or "").strip(),
        str(atom.get("residue_number") or "").strip(),
    )


def _pdb_atom_keys(text: str) -> set[tuple[str, str, str, str]]:
    keys: set[tuple[str, str, str, str]] = set()
    for line in text.splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            continue
        atom_name = line[12:16].strip().upper()
        residue_name = line[17:20].strip().upper()
        chain_name = line[21:22].strip()
        residue_number = line[22:26].strip()
        if atom_name and residue_name and residue_number:
            keys.add((atom_name, residue_name, chain_name, residue_number))
    return keys


def _mmcif_atom_keys(text: str) -> set[tuple[str, str, str, str]]:
    keys: set[tuple[str, str, str, str]] = set()
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() != "loop_":
            index += 1
            continue
        field_index = index + 1
        fields: list[str] = []
        while field_index < len(lines) and lines[field_index].startswith("_atom_site."):
            fields.append(lines[field_index].strip())
            field_index += 1
        if not fields:
            index += 1
            continue
        row_index = field_index
        while row_index < len(lines):
            line = lines[row_index].strip()
            if (
                not line
                or line.startswith("#")
                or line == "loop_"
                or line.startswith("_")
                or line.startswith("data_")
            ):
                break
            values = _split_cif_row(line)
            if len(values) >= len(fields):
                row = dict(zip(fields, values))
                keys.update(_atom_keys_from_mmcif_row(row))
            row_index += 1
        index = row_index
    return keys


def _split_cif_row(line: str) -> list[str]:
    try:
        return shlex.split(line)
    except ValueError:
        return line.split()


def _atom_keys_from_mmcif_row(row: dict[str, str]) -> set[tuple[str, str, str, str]]:
    atom_names = _clean_cif_values(
        row.get("_atom_site.label_atom_id"), row.get("_atom_site.auth_atom_id")
    )
    residue_names = _clean_cif_values(
        row.get("_atom_site.label_comp_id"), row.get("_atom_site.auth_comp_id")
    )
    chain_names = _clean_cif_values(
        row.get("_atom_site.auth_asym_id"), row.get("_atom_site.label_asym_id")
    )
    residue_numbers = _clean_cif_values(
        row.get("_atom_site.auth_seq_id"), row.get("_atom_site.label_seq_id")
    )
    return {
        (atom_name.upper(), residue_name.upper(), chain_name, residue_number)
        for atom_name in atom_names
        for residue_name in residue_names
        for chain_name in chain_names
        for residue_number in residue_numbers
    }


def _clean_cif_values(*values: str | None) -> set[str]:
    cleaned = {
        str(value).strip().strip("'\"")
        for value in values
        if value not in {None, "", ".", "?"}
    }
    return {value for value in cleaned if value}


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


def _blocker_row_common(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "rank": row.get("rank"),
        "entry_id": row.get("entry_id"),
        "entry_name": row.get("entry_name"),
        "structure_id": row.get("structure_id"),
        "target_fingerprint_id": row.get("target_fingerprint_id"),
        "exact_measured_distance_angstrom": row.get("exact_measured_distance_angstrom"),
        "missing_fields": list(row.get("missing_fields", []))
        if isinstance(row.get("missing_fields"), list)
        else [],
    }


def _download_bytes(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


def _normalize_mmcif_bytes(data: bytes) -> bytes:
    text = data.decode("utf-8", errors="replace")
    lines = [line.rstrip(" \t") for line in text.splitlines()]
    normalized = "\n".join(lines)
    if normalized or text.endswith(("\n", "\r")):
        normalized += "\n"
    return normalized.encode("utf-8")


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
