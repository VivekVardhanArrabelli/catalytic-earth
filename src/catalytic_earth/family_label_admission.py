from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ADMISSION_STATES = {
    "countable_candidate",
    "review_only_evidence",
    "oos_hard_negative",
    "blocked_locator",
    "blocked_coordinate",
    "blocked_family_decision",
    "reject_preserve_signal",
}

COORDINATE_LOCATOR_CLASSES = {
    "accession_equivalence_or_matching_coordinate_required",
    "alternate_coordinate_fetch_approval_required",
}

DEFAULT_FAMILY_PANEL_EVIDENCE_PACKETS = [
    "artifacts/v3_family_panel_evidence_packet_glycyl_radical_or_thiamine_radical_lyase_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_thiol_disulfide_oxidoreductase_isomerase_boundary_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_lipoamide_or_sulfur_transfer_redox_boundary_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_flavin_monooxygenase_and_flavin_oxygen_transfer_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_cobalamin_and_radical_rearrangement_panel_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_near_orphan_glycoside_or_nucleoside_hydrolase_controls_current702_20260601.json",
]


def build_family_label_admission_pipeline(
    *,
    import_preview_blocker_gate_path: Path,
    expert_import_decision_packet_path: Path,
    countability_gate_preflight_path: Path | None = None,
    locator_human_decision_matrix_path: Path | None = None,
    family_set_expansion_targets_path: Path | None = None,
    accepted_import_preview_path: Path | None = None,
    label_factory_gate_readiness_path: Path | None = None,
    source_check_completion_reconciliation_path: Path | None = None,
    family_panel_evidence_packet_paths: list[Path] | None = None,
    created_utc: str | None = None,
) -> dict[str, Any]:
    created_utc = created_utc or datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    blocker_gate = _load_json(import_preview_blocker_gate_path)
    expert_packet = _load_json(expert_import_decision_packet_path)
    countability_gate = _load_optional_json(countability_gate_preflight_path)
    locator_matrix = _load_optional_json(locator_human_decision_matrix_path)
    expansion_targets = _load_optional_json(family_set_expansion_targets_path)
    accepted_preview = _load_optional_json(accepted_import_preview_path)
    label_factory_readiness = _load_optional_json(label_factory_gate_readiness_path)
    source_check_reconciliation = _load_optional_json(
        source_check_completion_reconciliation_path
    )
    evidence_packets = [
        _load_json(path) for path in (family_panel_evidence_packet_paths or [])
    ]

    row_blockers = _required_list(
        blocker_gate,
        "row_blockers",
        import_preview_blocker_gate_path,
    )
    expert_stubs = _required_list(
        expert_packet,
        "expert_import_decision_stubs",
        expert_import_decision_packet_path,
    )
    expert_by_entry = _index_by_entry_id(expert_stubs, "expert import stubs")
    row_entries = {str(row.get("entry_id")) for row in row_blockers}
    missing_expert_entries = sorted(row_entries - set(expert_by_entry))
    if missing_expert_entries:
        raise ValueError(
            "expert import decision packet is missing row stubs for: "
            + ", ".join(missing_expert_entries)
        )

    countability_by_entry = _index_optional_rows(
        countability_gate,
        "row_gate_status",
        "countability gate preflight",
    )
    locator_by_entry = _index_optional_rows(
        locator_matrix,
        "row_decisions",
        "locator human decision matrix",
    )
    source_check_by_entry = _index_optional_rows(
        source_check_reconciliation,
        "reconciliation_rows",
        "source check reconciliation",
    )
    source_check_artifact_by_entry = _index_optional_rows(
        source_check_reconciliation,
        "source_check_artifact_records",
        "source check artifact records",
    )
    source_check_detail_by_entry = _source_check_detail_by_entry(
        source_check_artifact_by_entry
    )
    evidence_by_entry = _evidence_by_entry(evidence_packets)
    family_manifest = _family_onboarding_manifest(expansion_targets, evidence_packets)

    row_admission_table: list[dict[str, Any]] = []
    for row in row_blockers:
        entry_id = str(row.get("entry_id"))
        expert_stub = expert_by_entry[entry_id]
        locator_row = locator_by_entry.get(entry_id)
        source_check_row = source_check_by_entry.get(entry_id)
        evidence = evidence_by_entry.get(entry_id, {})
        admission = classify_admission_state(
            row,
            expert_stub=expert_stub,
            locator_row=locator_row,
        )
        row_admission_table.append(
            {
                "entry_id": entry_id,
                "panel_id": row.get("panel_id"),
                "admission_state": admission["state"],
                "state_reason": admission["reason"],
                "allowed_next_action": _allowed_next_action(
                    row,
                    expert_stub=expert_stub,
                    locator_row=locator_row,
                    source_check_row=source_check_row,
                ),
                "allowed_next_action_class": admission["allowed_next_action_class"],
                "blocker_class": row.get("primary_blocker_class"),
                "gate_blockers": sorted(row.get("gate_blockers", [])),
                "gates": {
                    "ready_for_import_preview": bool(
                        row.get("ready_for_import_preview")
                    ),
                    "ready_for_label_factory_gate": bool(
                        row.get("ready_for_label_factory_gate")
                    ),
                    "countable_label_candidate": bool(
                        row.get("countable_label_candidate")
                    ),
                    "import_preview_candidate_if_accepted_now": bool(
                        expert_stub.get("import_preview_candidate_if_accepted_now")
                    ),
                    "research_gate_status": row.get("research_gate_status"),
                    "countability_preflight": _select_keys(
                        countability_by_entry.get(entry_id, {}),
                        [
                            "primary_score_complete",
                            "non_abstained_at_research_threshold",
                            "source_check_queue_rank",
                            "locator_resolution_class",
                            "locator_resolution_status",
                        ],
                    ),
                },
                "human_decision_provenance": _select_keys(
                    expert_stub,
                    [
                        "decision_context_sha256",
                        "review_status",
                        "default_decision",
                        "allowed_decisions",
                        "decision_field_to_update",
                        "review_status_field_to_update",
                        "recommended_review_status_after_decision",
                    ],
                ),
                "locator_provenance": _locator_provenance(row, locator_row),
                "source_check_provenance": {
                    "reconciliation": source_check_row,
                    "artifact_record": source_check_artifact_by_entry.get(entry_id),
                    "detail_preserved": _source_check_detail_summary(
                        source_check_detail_by_entry.get(entry_id)
                    ),
                },
                "evidence_preserved": _preserved_evidence(evidence),
                "raw_review_context": {
                    "import_preview_blocker_gate_row": row,
                    "expert_import_decision_stub": expert_stub,
                },
            }
        )

    state_counts = Counter(row["admission_state"] for row in row_admission_table)
    _validate_exact_one_state(row_admission_table)

    review_rows = [
        row
        for row in row_admission_table
        if row["admission_state"]
        in {"blocked_family_decision", "review_only_evidence"}
    ]
    import_preview_rows = [
        row
        for row in row_admission_table
        if row["admission_state"] == "countable_candidate"
    ]
    rejects_oos_rows = [
        row
        for row in row_admission_table
        if row["admission_state"] in {"oos_hard_negative", "reject_preserve_signal"}
        or _is_oos_signal(row)
    ]
    blocked_rows = [
        row
        for row in row_admission_table
        if row["admission_state"].startswith("blocked_")
    ]

    source_paths = [
        import_preview_blocker_gate_path,
        expert_import_decision_packet_path,
        countability_gate_preflight_path,
        locator_human_decision_matrix_path,
        family_set_expansion_targets_path,
        accepted_import_preview_path,
        label_factory_gate_readiness_path,
        source_check_completion_reconciliation_path,
        *(family_panel_evidence_packet_paths or []),
    ]

    artifact = {
        "artifact_id": "v3_family_label_admission_pipeline_current702_20260607",
        "schema_version": "1.0",
        "created_utc": created_utc,
        "scope": "current702_family_panel_admission",
        "status": "family_label_admission_pipeline_ready_review_only",
        "admission_states_contract": sorted(ADMISSION_STATES),
        "source_artifacts": _source_artifact_records(source_paths),
        "guardrails": {
            "review_only": True,
            "imports_or_promotions_performed": False,
            "labels_registries_ontologies_changed": False,
            "mechanism_fingerprints_changed": False,
            "production_scoring_changed": False,
            "thresholds_changed_or_selected": False,
            "model_weights_fit_or_refit": False,
            "heldout_evaluated_or_tuned": False,
            "lomo_or_spent_cofactor_heldout_rerun": False,
            "source_free_locators_fabricated": False,
            "provenance_fields_preserved_as_review_context_not_predictive_features": True,
        },
        "counts": {
            "candidate_rows_evaluated": len(row_admission_table),
            "panels_represented": len(
                {row.get("panel_id") for row in row_admission_table}
            ),
            "state_counts": {
                state: state_counts.get(state, 0)
                for state in sorted(ADMISSION_STATES)
            },
            "review_packet_rows": len(review_rows),
            "import_preview_rows": len(import_preview_rows),
            "rejects_oos_signal_rows": len(rejects_oos_rows),
            "blocked_rows": len(blocked_rows),
            "rows_with_evidence_packet_context": sum(
                1 for row in row_admission_table if row["evidence_preserved"]
            ),
            "rows_with_locator_provenance": sum(
                1 for row in row_admission_table if row["locator_provenance"]
            ),
            "rows_with_source_check_provenance": sum(
                1
                for row in row_admission_table
                if row["source_check_provenance"]["reconciliation"]
                or row["source_check_provenance"]["artifact_record"]
            ),
            "rows_with_source_check_detail_preserved": sum(
                1
                for row in row_admission_table
                if row["source_check_provenance"]["detail_preserved"]
            ),
        },
        "machinery_applied": [
            "family_panel_countability_gate_preflight",
            "family_panel_import_preview_blocker_gate",
            "family_panel_expert_import_decision_packet",
            "family_panel_evidence_packets",
            "source_check_completion_reconciliation",
            "source_free_locator_human_decision_matrix",
            "accepted_import_preview_blocker_check",
            "label_factory_gate_readiness_blocker_check",
        ],
        "family_onboarding_manifest": family_manifest,
        "row_admission_table": row_admission_table,
        "review_packet": {
            "rows": review_rows,
            "remaining_human_decision_needed": True,
            "decision_context_hash_required_before_application": True,
        },
        "import_preview": {
            "rows": import_preview_rows,
            "status": (
                "empty_no_gate_passing_rows"
                if not import_preview_rows
                else "ready_for_separate_review_only_import_preview"
            ),
            "accepted_import_preview_source_counts": (
                accepted_preview or {}
            ).get("counts"),
            "label_factory_gate_readiness_counts": (
                label_factory_readiness or {}
            ).get("counts"),
        },
        "rejects_oos_signal_packet": {
            "rows": rejects_oos_rows,
            "interpretation": (
                "Rows here preserve hard-negative, OOS, or rejected-review "
                "signal only; they do not create labels or predictive features."
            ),
        },
        "blocked_summary": {
            "blocked_rows": blocked_rows,
            "blocker_counts": dict(
                sorted(Counter(row["blocker_class"] for row in blocked_rows).items())
            ),
        },
        "decision": {
            "new_countable_labels_authorized": False,
            "label_import_authorized": False,
            "single_recommended_next_family_expansion_task": (
                "Resolve the accession-equivalence or matching-coordinate "
                "locator decision for mh_065 and mh_072 by providing frozen "
                "coordinates that map to Q79MP6/P0A6P9 or an explicitly "
                "approved remapped locator; then rerun the import-preview "
                "blocker gate."
            ),
            "human_decision_needed": (
                "Expert family-admission decisions remain required for the "
                "six import-preview-candidate-if-accepted rows, and locator "
                "policy decisions remain required for five mechanical blockers."
            ),
        },
    }
    return artifact


def classify_admission_state(
    row: dict[str, Any],
    *,
    expert_stub: dict[str, Any] | None = None,
    locator_row: dict[str, Any] | None = None,
) -> dict[str, str]:
    decision = str(
        row.get("decision")
        or (expert_stub or {}).get("decision")
        or (expert_stub or {}).get("default_decision")
        or ""
    )
    review_status = str(row.get("review_status") or (expert_stub or {}).get("review_status") or "")
    if decision.startswith("reject_") or review_status.startswith("rejected"):
        return _state(
            "reject_preserve_signal",
            "explicit reject/rejected review status preserves evidence without import",
            "preserve_reject_signal",
        )
    if bool(row.get("oos_hard_negative")) or row.get("primary_blocker_class") == "oos_hard_negative":
        return _state(
            "oos_hard_negative",
            "row is explicitly marked as an OOS hard negative",
            "preserve_oos_hard_negative_signal",
        )
    if bool(row.get("countable_label_candidate")) or bool(
        row.get("ready_for_label_factory_gate")
    ):
        return _state(
            "countable_candidate",
            "row has passed through import-preview/label-factory gate readiness",
            "run_separate_label_factory_gate_review",
        )

    blocker_class = row.get("primary_blocker_class")
    if blocker_class == "source_free_locator_or_primary_channel_missing":
        locator_class = row.get("locator_decision_class") or (
            locator_row or {}
        ).get("resolution_class")
        locator_status = row.get("locator_resolution_status") or (
            locator_row or {}
        ).get("resolution_status")
        if locator_class in COORDINATE_LOCATOR_CLASSES:
            return _state(
                "blocked_coordinate",
                f"coordinate or accession-equivalent mapping is unresolved: {locator_status}",
                "resolve_coordinate_or_mapping",
            )
        return _state(
            "blocked_locator",
            f"source-free locator or primary-channel policy is unresolved: {locator_status}",
            "resolve_source_free_locator_policy",
        )
    if blocker_class == "expert_family_admission_decision_required":
        return _state(
            "blocked_family_decision",
            "expert family-admission decision is required before import preview",
            "record_expert_family_admission_decision",
        )
    if blocker_class == "completed_source_check_review_only_no_promotion":
        return _state(
            "review_only_evidence",
            "source check completed but family promotion is explicitly not ready",
            "preserve_review_only_evidence",
        )
    return _state(
        "reject_preserve_signal",
        f"unrecognized admission blocker class {blocker_class!r}; fail closed",
        "preserve_signal_fail_closed",
    )


def render_family_label_admission_report(artifact: dict[str, Any]) -> str:
    counts = artifact["counts"]
    lines = [
        "# Family Label Admission Pipeline",
        "",
        f"Artifact: `{artifact['artifact_id']}`",
        f"Status: `{artifact['status']}`",
        "",
        "## Row States",
        "",
        "| State | Rows |",
        "| --- | ---: |",
    ]
    for state, count in counts["state_counts"].items():
        lines.append(f"| `{state}` | {count} |")
    lines.extend(
        [
            "",
            "## Admission Table",
            "",
            "| Entry | Panel | State | Next action class |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in artifact["row_admission_table"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["entry_id"]),
                    str(row["panel_id"]),
                    f"`{row['admission_state']}`",
                    str(row["allowed_next_action_class"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Preserved Evidence",
            "",
            "- Evidence packet context is preserved for "
            f"{counts['rows_with_evidence_packet_context']} rows.",
            "- Source-check provenance is preserved for "
            f"{counts['rows_with_source_check_provenance']} rows.",
            "- Source-check catalytic/locator detail is preserved for "
            f"{counts['rows_with_source_check_detail_preserved']} rows.",
            "- Locator provenance is preserved for "
            f"{counts['rows_with_locator_provenance']} rows.",
            "- Mechanism text, source prose, labels, IDs, accessions, "
            "coordinates, and provenance remain review context only, not "
            "predictive feature values.",
            "",
            "## Outputs",
            "",
            f"- Review packet rows: {counts['review_packet_rows']}",
            f"- Import-preview rows: {counts['import_preview_rows']}",
            f"- Reject/OOS-signal rows: {counts['rejects_oos_signal_rows']}",
            f"- Blocked rows: {counts['blocked_rows']}",
            "",
            "## Machinery",
            "",
        ]
    )
    for machine in artifact["machinery_applied"]:
        lines.append(f"- `{machine}`")
    lines.extend(
        [
            "",
            "## Next Task",
            "",
            artifact["decision"]["single_recommended_next_family_expansion_task"],
            "",
            "No labels, registries, ontology, mechanism fingerprints, thresholds, "
            "production scoring, heldout evaluation, or imports were changed.",
            "",
        ]
    )
    return "\n".join(lines)


def _state(state: str, reason: str, action_class: str) -> dict[str, str]:
    if state not in ADMISSION_STATES:
        raise ValueError(f"unknown admission state: {state}")
    return {
        "state": state,
        "reason": reason,
        "allowed_next_action_class": action_class,
    }


def _load_json(path: Path) -> dict[str, Any]:
    try:
        with Path(path).open(encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError as exc:
        raise ValueError(f"required input artifact is missing: {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"input artifact must be a JSON object: {path}")
    return payload


def _load_optional_json(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    return _load_json(path)


def _required_list(
    artifact: dict[str, Any],
    key: str,
    path: Path,
) -> list[dict[str, Any]]:
    rows = artifact.get(key)
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{path} must contain a non-empty `{key}` list")
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"{path} `{key}` row {index} must be an object")
        if not row.get("entry_id"):
            raise ValueError(f"{path} `{key}` row {index} is missing entry_id")
    return rows


def _index_by_entry_id(
    rows: list[dict[str, Any]],
    label: str,
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        entry_id = str(row.get("entry_id"))
        if entry_id in indexed:
            raise ValueError(f"duplicate entry_id in {label}: {entry_id}")
        indexed[entry_id] = row
    return indexed


def _index_optional_rows(
    artifact: dict[str, Any] | None,
    key: str,
    label: str,
) -> dict[str, dict[str, Any]]:
    if artifact is None:
        return {}
    rows = artifact.get(key, [])
    if rows is None:
        rows = []
    if not isinstance(rows, list):
        raise ValueError(f"{label} `{key}` must be a list when present")
    object_rows = [row for row in rows if isinstance(row, dict) and row.get("entry_id")]
    return _index_by_entry_id(object_rows, label)


def _evidence_by_entry(
    evidence_packets: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    by_entry: dict[str, dict[str, Any]] = {}
    for packet in evidence_packets:
        panel = packet.get("panel", {})
        row_evidence = packet.get("row_evidence", [])
        if not isinstance(row_evidence, list):
            continue
        for row in row_evidence:
            if not isinstance(row, dict) or not row.get("entry_id"):
                continue
            by_entry[str(row["entry_id"])] = {
                "panel": panel,
                "row_evidence": row,
            }
    return by_entry


def _family_onboarding_manifest(
    expansion_targets: dict[str, Any] | None,
    evidence_packets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    manifest: list[dict[str, Any]] = []
    if expansion_targets is not None:
        candidates = expansion_targets.get("candidate_families", [])
        if isinstance(candidates, list):
            for row in candidates:
                if isinstance(row, dict):
                    manifest.append(row)
    seen = {row.get("candidate_family") for row in manifest}
    for packet in evidence_packets:
        panel = packet.get("panel")
        if isinstance(panel, dict) and panel.get("candidate_family") not in seen:
            manifest.append(panel)
            seen.add(panel.get("candidate_family"))
    return manifest


def _preserved_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    if not evidence:
        return {}
    row = evidence.get("row_evidence", {})
    panel = evidence.get("panel", {})
    return {
        "candidate_family_context": panel,
        "benchmark_role": row.get("benchmark_role"),
        "evidence_role": row.get("evidence_role"),
        "predicted_geometry_status": row.get("predicted_geometry_status"),
        "predicted_geometry_accession_repair": row.get(
            "predicted_geometry_accession_repair"
        ),
        "predicted_geometry_top1": row.get("predicted_geometry_top1"),
        "predicted_atlas_geometry_variant_scores": row.get(
            "predicted_atlas_geometry_variant_scores"
        ),
        "predicted_structure_fold_channel": row.get(
            "predicted_structure_fold_channel"
        ),
        "selected_organic_cofactor_scores": row.get(
            "selected_organic_cofactor_scores"
        ),
        "selected_organic_cofactor_max": row.get("selected_organic_cofactor_max"),
        "selected_pdb_fold_proxy": row.get("selected_pdb_fold_proxy"),
        "split_assignment": row.get("split_assignment"),
    }


def _locator_provenance(
    row: dict[str, Any],
    locator_row: dict[str, Any] | None,
) -> dict[str, Any]:
    locator = {
        "locator_decision_class": row.get("locator_decision_class"),
        "locator_resolution_status": row.get("locator_resolution_status"),
    }
    if locator_row:
        locator.update(locator_row)
    return {key: value for key, value in locator.items() if value not in (None, [], {})}


def _allowed_next_action(
    row: dict[str, Any],
    *,
    expert_stub: dict[str, Any],
    locator_row: dict[str, Any] | None,
    source_check_row: dict[str, Any] | None,
) -> str:
    if locator_row and locator_row.get("next_action"):
        return str(locator_row["next_action"])
    if source_check_row and source_check_row.get("next_action"):
        return str(source_check_row["next_action"])
    actions = expert_stub.get("required_actions_before_import_preview")
    if isinstance(actions, list) and actions:
        return str(actions[0])
    actions = row.get("required_actions_before_import_preview")
    if isinstance(actions, list) and actions:
        return str(actions[0])
    return "Preserve review signal; no automated import or label action."


def _select_keys(row: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    return {key: row[key] for key in keys if key in row}


def _source_artifact_records(paths: list[Path | None]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path in paths:
        if path is None:
            continue
        path = Path(path)
        key = path.stem
        records[key] = {
            "path": str(path),
            "exists": path.exists(),
            "sha256": _sha256(path) if path.exists() else None,
        }
    return records


def _source_check_detail_by_entry(
    source_check_artifact_by_entry: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    details: dict[str, dict[str, Any]] = {}
    for entry_id, record in source_check_artifact_by_entry.items():
        path_value = record.get("path")
        if not path_value:
            continue
        path = Path(str(path_value))
        if not path.exists():
            continue
        observed_sha = _sha256(path)
        recorded_sha = record.get("sha256")
        detail = _load_json(path)
        details[entry_id] = {
            "path": str(path),
            "recorded_sha256": recorded_sha,
            "observed_sha256": observed_sha,
            "sha256_matches_record": recorded_sha == observed_sha,
            "artifact": detail,
        }
    return details


def _source_check_detail_summary(
    detail_record: dict[str, Any] | None,
) -> dict[str, Any]:
    if not detail_record:
        return {}
    artifact = detail_record.get("artifact", {})
    local = artifact.get("local_source_evidence", {})
    if not isinstance(local, dict):
        local = {}
    return {
        "path": detail_record.get("path"),
        "recorded_sha256": detail_record.get("recorded_sha256"),
        "observed_sha256": detail_record.get("observed_sha256"),
        "sha256_matches_record": detail_record.get("sha256_matches_record"),
        "row": artifact.get("row"),
        "source_check_decision": artifact.get("source_check_decision"),
        "fold_augmented_readout": artifact.get("fold_augmented_readout"),
        "duplicate_and_leakage_screen": artifact.get("duplicate_and_leakage_screen"),
        "mechanism_locus_assessment": local.get("mechanism_locus_assessment"),
        "mechanism_evidence_summary": local.get("mechanism_evidence_summary"),
        "catalytic_residue_count": local.get("catalytic_residue_count"),
        "catalytic_residue_role_counts": local.get("catalytic_residue_role_counts"),
        "catalytic_residues": local.get("catalytic_residues"),
        "approved_source_free_locator_summary": local.get(
            "approved_source_free_locator_summary"
        ),
        "selected_structure_evidence": local.get("selected_structure_evidence"),
        "panel_packet_scores": local.get("panel_packet_scores"),
        "source_backed_sidecar_status": local.get("source_backed_sidecar_status"),
        "source_backed_sidecar_blockers_to_clear": local.get(
            "source_backed_sidecar_blockers_to_clear"
        ),
        "external_panel_context": local.get("external_panel_context"),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_exact_one_state(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        state = row.get("admission_state")
        if state not in ADMISSION_STATES:
            raise ValueError(f"row {row.get('entry_id')} has invalid state {state!r}")


def _is_oos_signal(row: dict[str, Any]) -> bool:
    evidence = row.get("evidence_preserved", {})
    source_check_provenance = row.get("source_check_provenance", {})
    reconciliation = source_check_provenance.get("reconciliation") or {}
    text_values = [
        evidence.get("benchmark_role"),
        evidence.get("evidence_role"),
        reconciliation.get("source_check_result"),
    ]
    return any("oos" in str(value).lower() for value in text_values if value)
