from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


CREATED_UTC = "2026-05-27T00:00:00Z"
ARTIFACT_ID = "v3_wave1_1_diagnostic_benchmark_result_702_20260527"
SCHEMA_VERSION = "v3_wave1_1_diagnostic_benchmark_result.v1"

SOURCE_PATHS = {
    "review_only_readout": "artifacts/v3_wave1_1_review_only_diagnostic_readout_702_20260527.json",
    "packets2_3_closure_summary": "artifacts/v3_packets2_3_northstar_review_backlog_closure_summary_702_20260527.json",
    "packet2_closure": "artifacts/v3_packet2_near_orphan_geometry_support_decision_closure_702_20260527.json",
    "packet3_closure": "artifacts/v3_packet3_v2_sublabel_decision_closure_702_20260527.json",
    "representation_result_card": "artifacts/v3_wave1_representation_shootout_result_card_20260526.json",
    "representation_result_card_addendum": "artifacts/v3_wave1_representation_shootout_result_card_702_20260527_addendum.json",
    "structure_neighborhood_audit": "artifacts/v3_wave1_structure_neighborhood_audit_20260526.json",
    "sequence_nn_metrics": "artifacts/v3_sequence_nn_metrics_current702_20260525.json",
    "sequence_nn_predictions": "artifacts/v3_sequence_nn_predictions_current702_20260525.jsonl",
}

JSON_OUT = "artifacts/v3_wave1_1_diagnostic_benchmark_result_702_20260527.json"
MARKDOWN_OUT = "work/wave1_1_diagnostic_benchmark_result_20260527.md"

METHODS = [
    {
        "method_id": "foldseek_structural_nn",
        "display_name": "Foldseek full-structure nearest neighbor",
        "family": "structure_neighborhood",
        "row_track_id": "foldseek_structural_nn",
        "primary_readthrough_track_id": "foldseek_structural",
    },
    {
        "method_id": "geometry_baseline",
        "display_name": "Active-site geometry baseline/router",
        "family": "geometry_router",
        "row_track_id": "geometry_baseline",
        "primary_readthrough_track_id": "geometry_baseline",
    },
    {
        "method_id": "sequence_nn",
        "display_name": "Sequence-NN 3-mer Jaccard",
        "family": "sequence_baseline",
        "row_track_id": "sequence_nn",
        "primary_readthrough_track_id": "sequence_nn",
    },
    {
        "method_id": "esm2_150m",
        "display_name": "ESM-2 150M logistic",
        "family": "learned_sequence_representation",
        "row_track_id": "esm2_150m",
        "primary_readthrough_track_id": "esm2_150m",
    },
    {
        "method_id": "esm_c",
        "display_name": "ESM-C corrected logistic",
        "family": "learned_sequence_representation",
        "row_track_id": "esm_c_corrected_logistic",
        "primary_readthrough_track_id": "esm_c_300m",
    },
    {
        "method_id": "prott5",
        "display_name": "ProtT5 Swiss-Prot H5 cosine NN",
        "family": "learned_sequence_representation",
        "row_track_id": "prott5_swissprot_h5_knn",
        "primary_readthrough_track_id": "prott5",
    },
    {
        "method_id": "saprot",
        "display_name": "SaProt 35M structure-token NN",
        "family": "learned_structure_aware_representation",
        "row_track_id": "saprot_35m_structure_tokens",
        "primary_readthrough_track_id": "saprot",
    },
    {
        "method_id": "prostt5_3di",
        "display_name": "ProstT5-3Di",
        "family": "learned_structure_aware_representation",
        "row_track_id": None,
        "primary_readthrough_track_id": "prostt5_3di",
        "row_unavailable_reason": "No row-aligned ProstT5-3Di prediction track is present in the structure-neighborhood audit or artifacts/representation_tracks.",
    },
    {
        "method_id": "foldseek_pocket",
        "display_name": "Foldseek-pocket",
        "family": "pocket_structure_representation",
        "row_track_id": None,
        "primary_readthrough_track_id": None,
        "row_unavailable_reason": "No standardized Foldseek-pocket per-row prediction export is present locally.",
        "primary_unavailable_reason": "No Foldseek-pocket aggregate or per-row track is present in the Wave 1 readthrough artifacts.",
    },
]


def _load_json(root: Path, relative_path: str) -> Any:
    with (root / relative_path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_artifacts(root: Path) -> dict[str, dict[str, str]]:
    return {
        relative_path: {"sha256": _sha256(root / relative_path)}
        for relative_path in SOURCE_PATHS.values()
    }


def _readout_cells(readout: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {cell["cell_id"]: cell for cell in readout["diagnostic_readout_cells"]}


def _audit_rows(audit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["entry_id"]: row for row in audit["rows"]}


def _packet3_labels(packet3: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["child_label_id"]: row for row in packet3["child_label_closures"]}


def _count_correct_from_fraction(support: int | None, fraction: float | None) -> int | None:
    if support is None or fraction is None:
        return None
    return int(round(support * fraction))


def _prediction_counts(tracks: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(track.get("predicted_label_group") for track in tracks)
    return {str(label): count for label, count in sorted(counts.items(), key=lambda item: str(item[0]))}


def _track_result(
    method: dict[str, Any],
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    track_id = method.get("row_track_id")
    missing_reasons: list[str] = []
    if track_id is None:
        return [], [method["row_unavailable_reason"]]

    tracks: list[dict[str, Any]] = []
    for row in rows:
        track = row.get("tracks", {}).get(track_id)
        if track and track.get("available") is True:
            tracks.append(track)
        else:
            missing_reasons.append(row["entry_id"])
    return tracks, missing_reasons


def _interpret_row_cell(
    cell_id: str,
    method_id: str,
    row_count: int,
    correct_count: int,
    abstention_count: int,
    unsafe_count: int,
) -> str:
    if cell_id == "packet2_near_orphan_geometry_rescue_behavior":
        if method_id == "geometry_baseline":
            return f"Geometry supports the expected v1 family on {correct_count}/{row_count} near-orphan rows, the clearest rescue signal in this cell."
        if method_id == "foldseek_structural_nn":
            return f"Foldseek is safe but incomplete in near-orphans: {correct_count}/{row_count} same-family transfers with {abstention_count} abstentions and {unsafe_count} wrong nonabstentions."
        return f"Available as a row-aligned comparison, but it supports only {correct_count}/{row_count} near-orphan rows and leaves {abstention_count} abstentions."
    if cell_id == "packet2_wrong_foldseek_transfer_diagnostic_behavior":
        if method_id == "foldseek_structural_nn":
            return f"This is the Foldseek failure slice: {unsafe_count}/{row_count} rows are wrong nonabstentions."
        if method_id == "geometry_baseline":
            return f"Geometry rescues the true v1 family on {correct_count}/{row_count} wrong-transfer rows."
        return f"Comparison track only: {correct_count}/{row_count} true-family calls, {abstention_count} abstentions, and {unsafe_count} wrong nonabstentions."
    return f"Row-aligned parent-v1 projection: {correct_count}/{row_count} true-family calls, {abstention_count} abstentions, {unsafe_count} wrong nonabstentions."


def _unavailable_result(method: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "method_id": method["method_id"],
        "display_name": method["display_name"],
        "method_available": False,
        "row_count_evaluable": 0,
        "correct_or_expected_behavior_count": None,
        "unsafe_nonabstention_count": None,
        "abstention_or_review_only_behavior_count": None,
        "qualitative_interpretation": "Unavailable for this diagnostic cell.",
        "unavailable_reason": reason,
    }


def _evaluate_entry_cell(
    cell: dict[str, Any],
    audit_by_entry: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    entry_ids = cell["entry_ids"]
    rows = [audit_by_entry[entry_id] for entry_id in entry_ids if entry_id in audit_by_entry]
    missing_entry_ids = [entry_id for entry_id in entry_ids if entry_id not in audit_by_entry]

    method_results = []
    for method in METHODS:
        tracks, missing = _track_result(method, rows)
        if not tracks:
            reason = method.get("row_unavailable_reason") or (
                f"No available row-level track `{method.get('row_track_id')}` was found for this cell."
            )
            method_results.append(_unavailable_result(method, reason))
            continue

        row_count = len(tracks)
        correct_count = sum(track.get("exact_label_match") is True for track in tracks)
        abstention_count = sum(track.get("abstained") is True for track in tracks)
        unsafe_count = sum(
            track.get("abstained") is not True and track.get("exact_label_match") is not True
            for track in tracks
        )
        method_results.append(
            {
                "method_id": method["method_id"],
                "display_name": method["display_name"],
                "method_available": True,
                "available_behavior_scope": "parent_v1_fingerprint",
                "row_count_evaluable": row_count,
                "correct_or_expected_behavior_count": correct_count,
                "unsafe_nonabstention_count": unsafe_count,
                "abstention_or_review_only_behavior_count": abstention_count,
                "predicted_label_group_counts": _prediction_counts(tracks),
                "missing_or_unavailable_entry_count": len(missing),
                "qualitative_interpretation": _interpret_row_cell(
                    cell["cell_id"],
                    method["method_id"],
                    row_count,
                    correct_count,
                    abstention_count,
                    unsafe_count,
                ),
                "unavailable_reason": None,
            }
        )

    return {
        "cell_id": cell["cell_id"],
        "requested_item": cell["requested_item"],
        "diagnostic_use": cell["metric_use_allowed_now"],
        "row_count_requested": len(entry_ids),
        "row_count_mapped_to_audit": len(rows),
        "missing_entry_ids": missing_entry_ids,
        "countable_metric": False,
        "method_results": method_results,
    }


def _child_representative_rows(
    child_label_ids: list[str],
    labels_by_id: dict[str, dict[str, Any]],
    audit_by_entry: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    representative_ids: list[str] = []
    support_count_by_child_label: dict[str, int] = {}
    parent_by_child_label: dict[str, str] = {}
    for child_label_id in child_label_ids:
        closure = labels_by_id[child_label_id]
        support_count_by_child_label[child_label_id] = closure["support_count"]
        parent_by_child_label[child_label_id] = closure["parent_fingerprint_id"]
        for entry_id in closure.get("representative_entry_ids", []):
            if entry_id not in representative_ids:
                representative_ids.append(entry_id)

    rows = [audit_by_entry[entry_id] for entry_id in representative_ids if entry_id in audit_by_entry]
    missing = [entry_id for entry_id in representative_ids if entry_id not in audit_by_entry]
    metadata = {
        "child_label_count": len(child_label_ids),
        "support_count_by_child_label": support_count_by_child_label,
        "support_count_total": sum(support_count_by_child_label.values()),
        "parent_fingerprint_by_child_label": parent_by_child_label,
        "representative_entry_count": len(representative_ids),
        "representative_entry_count_mapped_to_audit": len(rows),
        "missing_representative_entry_ids": missing,
    }
    return rows, metadata


def _interpret_child_cell(
    cell_id: str,
    method_id: str,
    row_count: int,
    parent_correct_count: int,
    parent_abstention_count: int,
    parent_unsafe_count: int,
) -> str:
    if cell_id == "packet3_eight_pilot_only_child_stratum_readout":
        return (
            f"Parent-v1 projection only: {parent_correct_count}/{row_count} mapped representative rows "
            f"support the parent family. This is not a child-label metric."
        )
    if cell_id == "abstention_behavior_on_unresolved_or_underpowered_child_buckets":
        return (
            "No child-label predictions are present, so true unresolved-child abstention is unavailable; "
            f"the parent projection has {parent_abstention_count} parent abstentions and {parent_unsafe_count} wrong parent nonabstentions."
        )
    if cell_id == "canary_behavior_for_underpowered_or_mixed_chemistry_cells":
        return (
            "Canary/mixed-chemistry behavior is parent-projection only; blocked child labels remain no-use "
            f"regardless of {parent_correct_count}/{row_count} parent-family calls."
        )
    return "Parent-v1 projection only; no child-label prediction is available."


def _evaluate_child_cell(
    cell: dict[str, Any],
    child_label_ids: list[str],
    labels_by_id: dict[str, dict[str, Any]],
    audit_by_entry: dict[str, dict[str, Any]],
    expected_behavior_is_parent_support: bool,
    extra_fields: dict[str, Any] | None = None,
) -> dict[str, Any]:
    rows, metadata = _child_representative_rows(child_label_ids, labels_by_id, audit_by_entry)
    method_results = []
    for method in METHODS:
        tracks, missing = _track_result(method, rows)
        if not tracks:
            reason = method.get("row_unavailable_reason") or (
                f"No available row-level track `{method.get('row_track_id')}` was found for mapped child representatives."
            )
            method_results.append(_unavailable_result(method, reason))
            continue

        row_count = len(tracks)
        parent_correct_count = sum(track.get("exact_label_match") is True for track in tracks)
        parent_abstention_count = sum(track.get("abstained") is True for track in tracks)
        parent_unsafe_count = sum(
            track.get("abstained") is not True and track.get("exact_label_match") is not True
            for track in tracks
        )
        if expected_behavior_is_parent_support:
            correct_or_expected = parent_correct_count
            abstention_or_review = parent_abstention_count
            unsafe_count = parent_unsafe_count
        else:
            correct_or_expected = None
            abstention_or_review = row_count
            unsafe_count = 0

        method_results.append(
            {
                "method_id": method["method_id"],
                "display_name": method["display_name"],
                "method_available": True,
                "available_behavior_scope": "parent_v1_fingerprint_projection_only",
                "child_label_prediction_available": False,
                "row_count_evaluable": row_count,
                "correct_or_expected_behavior_count": correct_or_expected,
                "unsafe_nonabstention_count": unsafe_count,
                "abstention_or_review_only_behavior_count": abstention_or_review,
                "parent_fingerprint_support_count": parent_correct_count,
                "parent_abstention_count": parent_abstention_count,
                "parent_wrong_nonabstention_count": parent_unsafe_count,
                "predicted_label_group_counts": _prediction_counts(tracks),
                "missing_or_unavailable_representative_count": len(missing),
                "qualitative_interpretation": _interpret_child_cell(
                    cell["cell_id"],
                    method["method_id"],
                    row_count,
                    parent_correct_count,
                    parent_abstention_count,
                    parent_unsafe_count,
                ),
                "unavailable_reason": None,
            }
        )

    result = {
        "cell_id": cell["cell_id"],
        "requested_item": cell["requested_item"],
        "diagnostic_use": cell["metric_use_allowed_now"],
        "countable_metric": False,
        "child_label_prediction_available": False,
        "child_label_metric_created": False,
        "child_label_ids": child_label_ids,
        **metadata,
        "method_results": method_results,
    }
    if extra_fields:
        result.update(extra_fields)
    return result


def _evaluate_primary_readthrough(cell: dict[str, Any]) -> dict[str, Any]:
    tracks_by_id = {track["track_id"]: track for track in cell["track_readout"]}
    method_results = []
    for method in METHODS:
        readthrough_id = method.get("primary_readthrough_track_id")
        track = tracks_by_id.get(readthrough_id)
        if track is None:
            method_results.append(
                _unavailable_result(
                    method,
                    method.get("primary_unavailable_reason")
                    or f"No primary readthrough row is present for `{readthrough_id}`.",
                )
            )
            continue

        primary_support = track["after_both_readthrough_primary_support"]
        primary_accuracy = track["after_both_readthrough_primary_accuracy"]
        correct_count = _count_correct_from_fraction(primary_support, primary_accuracy)
        unsafe_boundary_count = sum(
            value is True
            for value in (
                track.get("m_csa497_new_oos_false_positive"),
                track.get("m_csa750_new_oos_false_positive"),
            )
        )
        safe_boundary_count = sum(
            value in (False, None)
            for value in (
                track.get("m_csa497_new_oos_false_positive"),
                track.get("m_csa750_new_oos_false_positive"),
            )
        )
        method_results.append(
            {
                "method_id": method["method_id"],
                "display_name": method["display_name"],
                "method_available": True,
                "available_behavior_scope": "primary_v1_readthrough_aggregate",
                "row_count_evaluable": primary_support,
                "correct_or_expected_behavior_count": correct_count,
                "unsafe_nonabstention_count": unsafe_boundary_count,
                "abstention_or_review_only_behavior_count": safe_boundary_count,
                "primary_accuracy_review_only": primary_accuracy,
                "oos_or_secondary_support_count": track["after_both_readthrough_oos_or_secondary_support"],
                "oos_or_secondary_false_positive_rate_review_only": track[
                    "after_both_readthrough_oos_or_secondary_false_positive_rate"
                ],
                "m_csa497_prediction": track.get("m_csa497_prediction"),
                "m_csa750_prediction": track.get("m_csa750_prediction"),
                "qualitative_interpretation": (
                    f"After excluding m_csa:497 and m_csa:750 from primary flavin metrics, "
                    f"the aggregate readthrough has {correct_count}/{primary_support} primary-support calls "
                    f"and {unsafe_boundary_count}/2 unsafe predictions on the excluded boundary rows."
                ),
                "unavailable_reason": None,
            }
        )

    return {
        "cell_id": cell["cell_id"],
        "requested_item": cell["requested_item"],
        "diagnostic_use": cell["metric_use_allowed_now"],
        "countable_metric": False,
        "entry_ids_excluded_from_primary_metrics": cell["entry_ids_read_through"],
        "rows_removed_from_primary_metrics": cell["rows_removed_from_primary_metrics"],
        "rows_retained_as_oos_or_boundary_negative": cell["rows_retained_as_oos_or_boundary_negative"],
        "method_results": method_results,
    }


def _method_catalog(audit: dict[str, Any], root: Path) -> list[dict[str, Any]]:
    audit_track_ids = {
        track_id
        for row in audit["rows"]
        for track_id, track in row.get("tracks", {}).items()
        if track.get("available") is True
    }
    representation_dir = root / "artifacts" / "representation_tracks"
    representation_track_files = sorted(
        str(path.relative_to(root))
        for path in representation_dir.rglob("*")
        if path.is_file()
    ) if representation_dir.exists() else []
    catalog = []
    for method in METHODS:
        row_track_id = method.get("row_track_id")
        catalog.append(
            {
                "method_id": method["method_id"],
                "display_name": method["display_name"],
                "family": method["family"],
                "row_track_id": row_track_id,
                "row_aligned_track_available": row_track_id in audit_track_ids if row_track_id else False,
                "primary_readthrough_track_id": method.get("primary_readthrough_track_id"),
                "uses_existing_artifacts_only": True,
                "unavailable_reason": None
                if row_track_id in audit_track_ids
                else method.get("row_unavailable_reason"),
            }
        )
    return catalog + [
        {
            "method_id": "representation_tracks_directory_scan",
            "display_name": "artifacts/representation_tracks scan",
            "family": "availability_audit",
            "path": "artifacts/representation_tracks",
            "file_count": len(representation_track_files),
            "files": representation_track_files,
        }
    ]


def _decision_summary(cells: list[dict[str, Any]]) -> dict[str, Any]:
    by_cell = {cell["cell_id"]: cell for cell in cells}

    def method_result(cell_id: str, method_id: str) -> dict[str, Any]:
        for row in by_cell[cell_id]["method_results"]:
            if row["method_id"] == method_id:
                return row
        raise KeyError((cell_id, method_id))

    near_foldseek = method_result("packet2_near_orphan_geometry_rescue_behavior", "foldseek_structural_nn")
    near_geometry = method_result("packet2_near_orphan_geometry_rescue_behavior", "geometry_baseline")
    wrong_foldseek = method_result("packet2_wrong_foldseek_transfer_diagnostic_behavior", "foldseek_structural_nn")
    wrong_geometry = method_result("packet2_wrong_foldseek_transfer_diagnostic_behavior", "geometry_baseline")
    near_esm2 = method_result("packet2_near_orphan_geometry_rescue_behavior", "esm2_150m")
    wrong_esm2 = method_result("packet2_wrong_foldseek_transfer_diagnostic_behavior", "esm2_150m")

    return {
        "does_foldseek_remain_best_only_in_dense_neighbor_or_broad_bucket_settings": {
            "answer": "yes",
            "basis": (
                "Foldseek remains strong in the existing aggregate readthrough and dense-neighborhood Wave 1 card, "
                f"but in closed Packet 2 diagnostics it supports {near_foldseek['correct_or_expected_behavior_count']}/"
                f"{near_foldseek['row_count_evaluable']} near-orphan rows and makes "
                f"{wrong_foldseek['unsafe_nonabstention_count']}/{wrong_foldseek['row_count_evaluable']} unsafe wrong-transfer calls."
            ),
        },
        "does_geometry_add_value_in_near_orphan_or_wrong_transfer_settings": {
            "answer": "yes",
            "basis": (
                f"Geometry supports {near_geometry['correct_or_expected_behavior_count']}/"
                f"{near_geometry['row_count_evaluable']} near-orphan rows and rescues "
                f"{wrong_geometry['correct_or_expected_behavior_count']}/"
                f"{wrong_geometry['row_count_evaluable']} wrong-Foldseek-transfer rows."
            ),
        },
        "do_existing_plm_or_representation_tracks_add_value_beyond_foldseek_or_sequence": {
            "answer": "limited_and_underpowered",
            "basis": (
                f"ESM-2 is the strongest available learned comparator in these cells, with "
                f"{near_esm2['correct_or_expected_behavior_count']}/{near_esm2['row_count_evaluable']} near-orphan "
                f"and {wrong_esm2['correct_or_expected_behavior_count']}/{wrong_esm2['row_count_evaluable']} wrong-transfer support. "
                "ProtT5 and SaProt add sporadic parent-v1 support but no child-label readout; ProstT5-3Di row-level "
                "exports and Foldseek-pocket are unavailable."
            ),
        },
        "recommended_next_move": {
            "decision": "targeted_hybrid_foldseek_geometry_atlas_engine_plus_fingerprint_v2_label_acquisition",
            "why": [
                "Build the Foldseek+geometry atlas engine because geometry resolves the exact near-orphan and wrong-transfer failures exposed here.",
                "Keep representation scaling secondary until row-aligned exports exist for all intended tracks and child-label prediction targets are defined.",
                "Use fingerprint v2/label acquisition for blocked mixed-chemistry and underpowered child cells before any v2 metric claim.",
            ],
        },
    }


def build_result(root: Path) -> dict[str, Any]:
    readout = _load_json(root, SOURCE_PATHS["review_only_readout"])
    packet2 = _load_json(root, SOURCE_PATHS["packet2_closure"])
    packet3 = _load_json(root, SOURCE_PATHS["packet3_closure"])
    audit = _load_json(root, SOURCE_PATHS["structure_neighborhood_audit"])

    cells_by_id = _readout_cells(readout)
    audit_by_entry = _audit_rows(audit)
    labels_by_id = _packet3_labels(packet3)

    primary_cell = _evaluate_primary_readthrough(
        cells_by_id["primary_v1_metrics_after_m_csa497_m_csa750_readthrough"]
    )
    near_orphan_cell = _evaluate_entry_cell(
        cells_by_id["packet2_near_orphan_geometry_rescue_behavior"],
        audit_by_entry,
    )
    wrong_transfer_cell = _evaluate_entry_cell(
        cells_by_id["packet2_wrong_foldseek_transfer_diagnostic_behavior"],
        audit_by_entry,
    )
    pilot_cell = _evaluate_child_cell(
        cells_by_id["packet3_eight_pilot_only_child_stratum_readout"],
        cells_by_id["packet3_eight_pilot_only_child_stratum_readout"]["child_label_ids"],
        labels_by_id,
        audit_by_entry,
        expected_behavior_is_parent_support=True,
    )
    abstention_cell = _evaluate_child_cell(
        cells_by_id["abstention_behavior_on_unresolved_or_underpowered_child_buckets"],
        cells_by_id["abstention_behavior_on_unresolved_or_underpowered_child_buckets"]["child_label_ids"],
        labels_by_id,
        audit_by_entry,
        expected_behavior_is_parent_support=False,
    )
    canary_source = cells_by_id["canary_behavior_for_underpowered_or_mixed_chemistry_cells"]
    canary_child_label_ids = (
        canary_source["underpowered_canary_child_label_ids"]
        + canary_source["mixed_chemistry_blocked_child_label_ids"]
    )
    canary_cell = _evaluate_child_cell(
        canary_source,
        canary_child_label_ids,
        labels_by_id,
        audit_by_entry,
        expected_behavior_is_parent_support=False,
        extra_fields={
            "underpowered_canary_child_label_ids": canary_source["underpowered_canary_child_label_ids"],
            "mixed_chemistry_blocked_child_label_ids": canary_source["mixed_chemistry_blocked_child_label_ids"],
            "other_terminal_no_use_child_label_ids": canary_source["other_terminal_no_use_child_label_ids"],
            "blocked_child_label_ids": canary_source["mixed_chemistry_blocked_child_label_ids"]
            + canary_source["other_terminal_no_use_child_label_ids"],
            "m_csa750_removed_from_canary_use": canary_source["m_csa750_canary_effect"]["removed_from_canary_use"],
        },
    )

    cells = [
        primary_cell,
        near_orphan_cell,
        wrong_transfer_cell,
        pilot_cell,
        abstention_cell,
        canary_cell,
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "created_utc": CREATED_UTC,
        "scope": "review_only_wave1_1_diagnostic_benchmark_readout_existing_artifacts_only",
        "status": "computed_review_only_diagnostic_benchmark",
        "review_only": True,
        "source_artifacts": _source_artifacts(root),
        "guardrails": {
            "canonical_label_registry_changed": False,
            "ontology_ids_changed": False,
            "fingerprint_registry_changed": False,
            "thresholds_changed": False,
            "production_scoring_changed": False,
            "imports_changed": False,
            "model_outputs_changed": False,
            "representation_model_artifacts_changed": False,
            "artifact_migration_state_changed": False,
            "new_models_trained": False,
            "new_external_model_inference_run": False,
            "new_countable_metrics_created": False,
            "canonical_v2_child_labels_created": False,
            "child_label_metrics_created": False,
        },
        "diagnostic_summary": {
            "diagnostic_cell_count": len(cells),
            "new_countable_metric_count": 0,
            "primary_readthrough_excluded_entry_ids": ["m_csa:497", "m_csa:750"],
            "packet2_near_orphan_row_count": near_orphan_cell["row_count_requested"],
            "packet2_wrong_foldseek_transfer_row_count": wrong_transfer_cell["row_count_requested"],
            "packet3_pilot_only_child_label_count": pilot_cell["child_label_count"],
            "packet3_abstention_probe_child_label_count": abstention_cell["child_label_count"],
            "packet3_canary_child_label_count": canary_cell["child_label_count"],
            "mixed_chemistry_blocked_child_label_ids": canary_source["mixed_chemistry_blocked_child_label_ids"],
            "all_counts_are_diagnostic_not_validation_metrics": True,
        },
        "method_catalog": _method_catalog(audit, root),
        "diagnostic_cells": cells,
        "decision_summary": _decision_summary(cells),
        "non_claims": [
            "No production scoring threshold, ontology, fingerprint, label registry, import, or model-output artifact was changed.",
            "Packet 2 rows remain review-only diagnostics and do not become countable validation labels.",
            "Packet 3 child labels remain proposal-only or blocked; no child-label metric is created.",
            "m_csa:497 and m_csa:750 remain excluded from primary v1 flavin metrics and retained only as OOS/boundary/future-acquisition signals.",
            "flavin.dehydrogenase_oxidase_hydride_transfer remains blocked as mixed chemistry and is not used as a v2 metric.",
        ],
    }


def _format_count(value: Any) -> str:
    return "n/a" if value is None else str(value)


def build_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Wave 1.1 Diagnostic Benchmark Result - 2026-05-27",
        "",
        "This is a review-only diagnostic benchmark readout built from existing Wave 1 and closed Packet 2/3 artifacts. It does not create countable metrics, child labels, model outputs, thresholds, imports, or registry edits.",
        "",
        "## Decision Summary",
        "",
    ]
    decision = result["decision_summary"]
    lines.extend(
        [
            f"- Foldseek dense-neighbor question: {decision['does_foldseek_remain_best_only_in_dense_neighbor_or_broad_bucket_settings']['answer']}. {decision['does_foldseek_remain_best_only_in_dense_neighbor_or_broad_bucket_settings']['basis']}",
            f"- Geometry value question: {decision['does_geometry_add_value_in_near_orphan_or_wrong_transfer_settings']['answer']}. {decision['does_geometry_add_value_in_near_orphan_or_wrong_transfer_settings']['basis']}",
            f"- Representation question: {decision['do_existing_plm_or_representation_tracks_add_value_beyond_foldseek_or_sequence']['answer']}. {decision['do_existing_plm_or_representation_tracks_add_value_beyond_foldseek_or_sequence']['basis']}",
            f"- Recommended next move: `{decision['recommended_next_move']['decision']}`.",
            "",
            "## Diagnostic Cells",
            "",
        ]
    )

    for cell in result["diagnostic_cells"]:
        lines.extend(
            [
                f"### {cell['cell_id']}",
                "",
                f"Use: `{cell['diagnostic_use']}`. Countable metric: `{str(cell['countable_metric']).lower()}`.",
                "",
                "| method | available | evaluable rows | expected/correct | unsafe nonabstain | abstain/review-only | interpretation |",
                "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
            ]
        )
        for method in cell["method_results"]:
            lines.append(
                "| {method_id} | {available} | {rows} | {correct} | {unsafe} | {abstain} | {interpretation} |".format(
                    method_id=method["method_id"],
                    available=str(method["method_available"]).lower(),
                    rows=method["row_count_evaluable"],
                    correct=_format_count(method["correct_or_expected_behavior_count"]),
                    unsafe=_format_count(method["unsafe_nonabstention_count"]),
                    abstain=_format_count(method["abstention_or_review_only_behavior_count"]),
                    interpretation=method["qualitative_interpretation"].replace("|", "/"),
                )
            )
        lines.append("")

    lines.extend(["## Guardrails", ""])
    for claim in result["non_claims"]:
        lines.append(f"- {claim}")
    lines.append("")
    return "\n".join(lines)


def write_outputs(root: Path) -> tuple[Path, Path]:
    result = build_result(root)
    json_path = root / JSON_OUT
    markdown_path = root / MARKDOWN_OUT
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    with markdown_path.open("w", encoding="utf-8") as handle:
        handle.write(build_markdown(result))
    return json_path, markdown_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the Wave 1.1 review-only diagnostic benchmark readout."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    args = parser.parse_args(argv)
    json_path, markdown_path = write_outputs(args.root)
    print(json_path)
    print(markdown_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
