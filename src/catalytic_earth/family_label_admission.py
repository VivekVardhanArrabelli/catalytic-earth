from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ADMISSION_STATES: tuple[str, ...] = (
    "countable_candidate",
    "review_only_evidence",
    "oos_hard_negative",
    "blocked_locator",
    "blocked_coordinate",
    "blocked_family_decision",
    "reject_preserve_signal",
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"expected JSON object at {path}")
    return payload


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _payload_sha256(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


def _source_record(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    return {"path": str(path), "exists": True, "sha256": _sha256(path)}


def _row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("panel_id") or row.get("candidate_family_id") or ""), str(
        row.get("entry_id") or ""
    )


def _index_rows(rows: list[dict[str, Any]], *, require_panel: bool = True) -> dict[tuple[str, str], dict[str, Any]]:
    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        panel_id, entry_id = _row_key(row)
        if not entry_id or (require_panel and not panel_id):
            continue
        indexed[(panel_id, entry_id)] = row
    return indexed


def _target_rows(targets: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for family in targets.get("candidate_families", []):
        if not isinstance(family, dict):
            continue
        panel_id = str(family.get("candidate_family") or "")
        for entry_id in family.get("candidate_rows", []):
            rows.append(
                {
                    "panel_id": panel_id,
                    "entry_id": str(entry_id),
                    "candidate_family": panel_id,
                    "priority_bins": list(family.get("priority_bins", [])),
                    "candidate_sources": list(family.get("candidate_sources", [])),
                    "expected_eval_bin_impact": family.get("expected_eval_bin_impact"),
                    "required_human_validation": family.get(
                        "required_human_validation"
                    ),
                }
            )
    return rows


def _load_panel_evidence(
    *, research_readout: dict[str, Any], source_artifacts: dict[str, dict[str, Any]]
) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[tuple[str, str], str]]:
    evidence_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    evidence_source_by_key: dict[tuple[str, str], str] = {}
    for summary in research_readout.get("panel_summaries", []):
        if not isinstance(summary, dict) or not summary.get("artifact"):
            continue
        packet_path = Path(str(summary["artifact"]))
        source_key = f"panel_packet::{packet_path.stem}"
        packet = _read_json(packet_path)
        source_artifacts[source_key] = _source_record(packet_path)
        panel = packet.get("panel", {})
        panel_id = str(
            panel.get("candidate_family")
            or summary.get("panel_id")
            or packet.get("panel_id")
            or ""
        )
        for row in packet.get("row_evidence", []):
            if not isinstance(row, dict):
                continue
            entry_id = str(row.get("entry_id") or "")
            if not panel_id or not entry_id:
                continue
            key = (panel_id, entry_id)
            evidence_by_key[key] = row
            evidence_source_by_key[key] = source_key
    return evidence_by_key, evidence_source_by_key


def _row_sources(
    *,
    base_source_keys: list[str],
    source_artifacts: dict[str, dict[str, Any]],
    extra_keys: list[str],
) -> dict[str, str]:
    keys = [*base_source_keys, *extra_keys]
    return {
        key: str(source_artifacts[key]["sha256"])
        for key in keys
        if key in source_artifacts and source_artifacts[key].get("sha256")
    }


def _merged_blocker_text(*rows: dict[str, Any] | None) -> str:
    parts: list[str] = []
    for row in rows:
        if not row:
            continue
        for field in (
            "primary_blocker_class",
            "locator_decision_class",
            "locator_resolution_status",
            "source_check_completion_status",
            "research_gate_status",
        ):
            value = row.get(field)
            if value is not None:
                parts.append(str(value))
        for field in (
            "gate_blockers",
            "required_actions_before_import_preview",
            "critical_violations",
        ):
            values = row.get(field)
            if isinstance(values, list):
                parts.extend(str(value) for value in values)
    return " ".join(parts).lower()


def _is_coordinate_blocked(
    *,
    gate_row: dict[str, Any] | None,
    blocker_row: dict[str, Any] | None,
    decision_stub: dict[str, Any] | None,
) -> bool:
    locator_class = str(
        (blocker_row or {}).get("locator_decision_class")
        or (gate_row or {}).get("locator_resolution_class")
        or (decision_stub or {}).get("locator_decision_class")
        or ""
    ).lower()
    if "nonlabel_locator" in locator_class or "ligand_specificity" in locator_class:
        return False
    if (
        "matching_coordinate" in locator_class
        or "alternate_coordinate" in locator_class
        or "coordinate_fetch" in locator_class
    ):
        return True
    blocker_text = _merged_blocker_text(gate_row, blocker_row, decision_stub)
    return (
        "primary_channel_score_missing" in blocker_text
        or "materialize_primary_channel_score" in blocker_text
        or "coordinate_required" in blocker_text
    )


def _explicit_decision(
    *, decision_stub: dict[str, Any] | None, accepted_preview_row: dict[str, Any] | None
) -> str | None:
    for row in (accepted_preview_row, decision_stub):
        if not row:
            continue
        decision = row.get("decision") or row.get("expert_decision")
        if decision:
            return str(decision)
    return None


def classify_family_label_admission_state(
    *,
    gate_row: dict[str, Any] | None,
    blocker_row: dict[str, Any] | None,
    decision_stub: dict[str, Any] | None,
    accepted_preview_row: dict[str, Any] | None,
    label_factory_gate_row: dict[str, Any] | None,
) -> tuple[str, str, list[str], str]:
    """Classify one candidate row from gate outputs, not predictive features."""

    blockers: list[str] = []
    explicit = _explicit_decision(
        decision_stub=decision_stub, accepted_preview_row=accepted_preview_row
    )
    blocker_text = _merged_blocker_text(gate_row, blocker_row, decision_stub)
    if explicit == "reject_family_panel_import_candidate":
        return (
            "reject_preserve_signal",
            "explicit_reject_family_panel_import_candidate",
            ["expert_rejected_import_candidate"],
            "Preserve the row in the rejects/OOS signal packet; do not import or count it.",
        )

    if label_factory_gate_row or bool((gate_row or {}).get("countable_label_candidate")):
        return (
            "countable_candidate",
            "label_factory_gate_input_ready_review_only",
            [],
            "Review the import preview, then run the label-factory gate only on emitted rows.",
        )

    primary_blocker_class = str(
        (blocker_row or {}).get("primary_blocker_class")
        or (decision_stub or {}).get("primary_blocker_class")
        or ""
    )
    if (
        primary_blocker_class == "accepted_oos_hard_negative"
        or "oos_hard_negative_signal" in blocker_text
        or "completed_oos_hard_negative" in blocker_text
    ):
        return (
            "oos_hard_negative",
            "accepted_oos_hard_negative_signal",
            [],
            "Stage as OOS/hard-negative signal only; keep it out of imports and labels.",
        )

    has_locator_or_coordinate_block = (
        primary_blocker_class == "source_free_locator_or_primary_channel_missing"
        or "source_free_locator_human_or_policy_decision_required" in blocker_text
        or bool((blocker_row or {}).get("locator_decision_class"))
        or bool((gate_row or {}).get("locator_resolution_class"))
    )
    if has_locator_or_coordinate_block:
        state = (
            "blocked_coordinate"
            if _is_coordinate_blocked(
                gate_row=gate_row,
                blocker_row=blocker_row,
                decision_stub=decision_stub,
            )
            else "blocked_locator"
        )
        blockers.append("source_free_locator_or_primary_channel_missing")
        action = (
            "Provide matching frozen coordinates or approve the coordinate fetch/remap, then rerun the primary-channel gate."
            if state == "blocked_coordinate"
            else "Resolve the source-free locator policy/locator decision, then rerun locator validation."
        )
        return state, primary_blocker_class or "locator_or_coordinate_blocker", blockers, action

    if (
        primary_blocker_class == "completed_source_check_review_only_no_promotion"
        or "completed_review_only_no_label_change" in blocker_text
    ):
        blockers.append("completed_source_check_review_only_no_promotion")
        return (
            "review_only_evidence",
            "completed_source_check_review_only_no_promotion",
            blockers,
            "Keep as review-only evidence unless an explicit family-promotion override is recorded.",
        )

    if (
        primary_blocker_class == "expert_family_admission_decision_required"
        or "review_packet_not_expert_import_decision" in blocker_text
        or "expert_import_decision_required" in blocker_text
    ):
        blockers.append("expert_family_admission_decision_required")
        return (
            "blocked_family_decision",
            primary_blocker_class or "expert_family_admission_decision_required",
            blockers,
            "Record an explicit expert family admission decision with the row context hash.",
        )

    blockers.append("missing_or_unrecognized_admission_inputs")
    return (
        "reject_preserve_signal",
        "missing_or_unrecognized_admission_inputs",
        blockers,
        "Preserve available signal for review; do not import, count, or train on this row.",
    )


def _preserved_evidence(
    *,
    target_row: dict[str, Any],
    research_row: dict[str, Any] | None,
    gate_row: dict[str, Any] | None,
    blocker_row: dict[str, Any] | None,
    decision_stub: dict[str, Any] | None,
    evidence_row: dict[str, Any] | None,
) -> dict[str, Any]:
    evidence = evidence_row or {}
    research = research_row or {}
    gate = gate_row or {}
    blocker = blocker_row or {}
    decision = decision_stub or {}
    channel_scores = research.get("channel_scores") or {}
    return {
        "candidate_sources": target_row.get("candidate_sources", []),
        "priority_bins": target_row.get("priority_bins", []),
        "expected_eval_bin_impact": target_row.get("expected_eval_bin_impact"),
        "required_human_validation": target_row.get("required_human_validation"),
        "catalytic_residues_roles": (
            evidence.get("catalytic_residues_roles")
            or evidence.get("active_site_residue_roles")
            or evidence.get("residue_roles")
        ),
        "cofactors_metals": {
            "selected_organic_cofactor_max": (
                research.get("selected_organic_cofactor_max")
                if research.get("selected_organic_cofactor_max") is not None
                else evidence.get("selected_organic_cofactor_max")
            ),
            "selected_organic_cofactor_scores": evidence.get(
                "selected_organic_cofactor_scores"
            ),
        },
        "active_site_geometry": {
            "predicted_atlas_geometry_variant_scores": evidence.get(
                "predicted_atlas_geometry_variant_scores"
            ),
            "predicted_geometry_top1": evidence.get("predicted_geometry_top1"),
            "channel_scores": channel_scores,
        },
        "predicted_vs_experimental_context": {
            "predicted_geometry_status": research.get("predicted_geometry_status")
            or evidence.get("predicted_geometry_status"),
            "predicted_structure_fold_channel": evidence.get(
                "predicted_structure_fold_channel"
            ),
            "predicted_structure_nearest_atlas_entry_id": research.get(
                "predicted_structure_nearest_atlas_entry_id"
            ),
            "predicted_structure_nearest_atlas_true_fingerprint_id": research.get(
                "predicted_structure_nearest_atlas_true_fingerprint_id"
            ),
            "fold_nearest_atlas_tm_score": channel_scores.get(
                "fold_nearest_atlas_tm_score"
            ),
            "selected_pdb_fold_proxy": evidence.get("selected_pdb_fold_proxy"),
        },
        "reconstruction": {
            "predicted_geometry_accession_repair": evidence.get(
                "predicted_geometry_accession_repair"
            ),
            "reconstruction_applied": evidence.get("reconstruction_applied"),
        },
        "bond_electron_proton_hints": {
            "bond_change": evidence.get("bond_change"),
            "electron_flow": evidence.get("electron_flow"),
            "proton_transfer": evidence.get("proton_transfer"),
        },
        "source_free_locator_provenance": {
            "locator_decision_class": blocker.get("locator_decision_class")
            or decision.get("locator_decision_class"),
            "locator_resolution_status": blocker.get("locator_resolution_status")
            or gate.get("locator_resolution_status"),
        },
        "fold_tm_or_lever3_gate_result": {
            "research_gate_status": research.get("research_gate_status")
            or gate.get("research_gate_status")
            or blocker.get("research_gate_status"),
            "primary_threshold": research.get("primary_threshold"),
            "primary_threshold_margin": research.get("primary_threshold_margin"),
            "primary_channel": research.get("primary_channel"),
        },
        "cofactor_electron_flow_applicability": {
            "selected_organic_cofactor_max": research.get(
                "selected_organic_cofactor_max"
            ),
            "electron_flow_available": evidence.get("electron_flow") is not None,
        },
        "gates": {
            "gate_blockers": sorted(
                set(gate.get("gate_blockers", []) + blocker.get("gate_blockers", []))
            ),
            "ready_for_import_preview": bool(
                gate.get("ready_for_import_preview")
                or blocker.get("ready_for_import_preview")
            ),
            "ready_for_label_factory_gate": bool(
                gate.get("ready_for_label_factory_gate")
                or blocker.get("ready_for_label_factory_gate")
            ),
            "source_check_completion_status": gate.get(
                "source_check_completion_status"
            )
            or blocker.get("source_check_completion_status"),
            "source_check_family_promotion_ready": gate.get(
                "source_check_family_promotion_ready"
            ),
        },
        "human_expert_decision_provenance": {
            "decision_context_sha256": decision.get("decision_context_sha256"),
            "allowed_decisions": decision.get("allowed_decisions"),
            "review_status": decision.get("review_status"),
            "default_decision": decision.get("default_decision"),
        },
    }


def build_family_label_admission_pipeline(
    *,
    family_expansion_targets_path: Path,
    family_panel_research_readout_path: Path,
    countability_gate_preflight_path: Path,
    import_preview_blocker_gate_path: Path,
    expert_import_decision_packet_path: Path,
    accepted_import_preview_path: Path,
    label_factory_gate_readiness_path: Path,
    artifact_id: str = "v3_family_label_admission_pipeline_current702_20260607",
    created_utc: str | None = None,
) -> dict[str, Any]:
    targets = _read_json(family_expansion_targets_path)
    research = _read_json(family_panel_research_readout_path)
    countability = _read_json(countability_gate_preflight_path)
    import_blockers = _read_json(import_preview_blocker_gate_path)
    expert_packet = _read_json(expert_import_decision_packet_path)
    accepted_preview = _read_json(accepted_import_preview_path)
    label_readiness = _read_json(label_factory_gate_readiness_path)

    source_artifacts: dict[str, dict[str, Any]] = {
        "family_onboarding_manifest": _source_record(family_expansion_targets_path),
        "family_panel_research_readout": _source_record(
            family_panel_research_readout_path
        ),
        "countability_gate_preflight": _source_record(countability_gate_preflight_path),
        "import_preview_blocker_gate": _source_record(import_preview_blocker_gate_path),
        "expert_import_decision_packet": _source_record(expert_import_decision_packet_path),
        "accepted_import_preview": _source_record(accepted_import_preview_path),
        "label_factory_gate_readiness": _source_record(label_factory_gate_readiness_path),
    }
    evidence_by_key, evidence_source_by_key = _load_panel_evidence(
        research_readout=research, source_artifacts=source_artifacts
    )

    research_by_key = _index_rows(research.get("row_scores", []))
    gate_by_key = _index_rows(countability.get("row_gate_status", []))
    blocker_by_key = _index_rows(import_blockers.get("row_blockers", []))
    decision_by_key = _index_rows(expert_packet.get("expert_import_decision_stubs", []))
    accepted_by_key = _index_rows(accepted_preview.get("accepted_import_preview_rows", []))
    label_gate_by_key = _index_rows(
        label_readiness.get("label_factory_gate_input_rows", [])
    )

    base_source_keys = [
        "family_onboarding_manifest",
        "family_panel_research_readout",
        "countability_gate_preflight",
        "import_preview_blocker_gate",
        "expert_import_decision_packet",
    ]
    candidate_rows = _target_rows(targets)
    row_table: list[dict[str, Any]] = []
    for target_row in candidate_rows:
        key = (target_row["panel_id"], target_row["entry_id"])
        research_row = research_by_key.get(key)
        gate_row = gate_by_key.get(key)
        blocker_row = blocker_by_key.get(key)
        decision_stub = decision_by_key.get(key)
        accepted_row = accepted_by_key.get(key)
        label_gate_row = label_gate_by_key.get(key)
        state, blocker_class, blockers, allowed_next_action = (
            classify_family_label_admission_state(
                gate_row=gate_row,
                blocker_row=blocker_row,
                decision_stub=decision_stub,
                accepted_preview_row=accepted_row,
                label_factory_gate_row=label_gate_row,
            )
        )
        extra_source_keys: list[str] = []
        if accepted_row:
            extra_source_keys.append("accepted_import_preview")
        if label_gate_row:
            extra_source_keys.append("label_factory_gate_readiness")
        if key in evidence_source_by_key:
            extra_source_keys.append(evidence_source_by_key[key])
        row_payload = {
            "entry_id": target_row["entry_id"],
            "panel_id": target_row["panel_id"],
            "state": state,
            "state_blocker_class": blocker_class,
            "state_blockers": blockers,
            "allowed_next_action": allowed_next_action,
            "row_context_sha256": _payload_sha256(
                {
                    "entry_id": target_row["entry_id"],
                    "panel_id": target_row["panel_id"],
                    "state": state,
                    "state_blocker_class": blocker_class,
                    "decision_context_sha256": (decision_stub or {}).get(
                        "decision_context_sha256"
                    ),
                }
            ),
            "evidence_preserved": _preserved_evidence(
                target_row=target_row,
                research_row=research_row,
                gate_row=gate_row,
                blocker_row=blocker_row,
                decision_stub=decision_stub,
                evidence_row=evidence_by_key.get(key),
            ),
            "source_hashes": _row_sources(
                base_source_keys=base_source_keys,
                source_artifacts=source_artifacts,
                extra_keys=extra_source_keys,
            ),
        }
        row_table.append(row_payload)

    state_counts = Counter(row["state"] for row in row_table)
    panel_counts: dict[str, Counter[str]] = {}
    for row in row_table:
        panel_counts.setdefault(row["panel_id"], Counter())[row["state"]] += 1
    import_rows = [
        row for row in row_table if row["state"] == "countable_candidate"
    ]
    review_rows = [
        row
        for row in row_table
        if row["state"]
        in {
            "review_only_evidence",
            "blocked_locator",
            "blocked_coordinate",
            "blocked_family_decision",
        }
    ]
    rejects_oos_rows = [
        row
        for row in row_table
        if row["state"]
        in {"oos_hard_negative", "reject_preserve_signal", "review_only_evidence"}
    ]
    recommended_next = (
        import_blockers.get("interpretation", {}).get("next_action")
        or import_blockers.get("decision", {}).get("next_gate")
        or "Record the next explicit expert family admission decision and rerun the admission pipeline."
    )

    return {
        "artifact_id": artifact_id,
        "schema_version": "family_label_admission.v0",
        "created_utc": created_utc or _utc_now_iso(),
        "status": (
            "family_label_admission_pipeline_ready_with_countable_candidates_review_only"
            if import_rows
            else "family_label_admission_pipeline_ready_no_countable_candidates"
        ),
        "scope": (
            "Deterministic family-label admission adapter for current family-panel "
            "candidate rows. It classifies row states, preserves mechanism/provenance "
            "signal, and emits review/import/reject packets without editing labels, "
            "registries, ontology, thresholds, splits, or model weights."
        ),
        "guardrails": {
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "label_factory_gate_run": False,
            "model_weights_fit_or_refit": False,
            "production_thresholds_changed": False,
            "heldout_evaluated_or_tuned": False,
            "heldout_splits_changed": False,
            "source_text_or_label_fields_used_as_predictive_features": False,
            "classification_uses_only_gate_and_review_outputs": True,
            "review_only": True,
        },
        "counts": {
            "candidate_family_axes_evaluated": len(
                targets.get("candidate_families", [])
            ),
            "candidate_rows_evaluated": len(row_table),
            "state_counts": dict(sorted(state_counts.items())),
            "countable_candidate_rows": len(import_rows),
            "review_packet_rows": len(review_rows),
            "rejects_oos_signal_rows": len(rejects_oos_rows),
        },
        "family_onboarding_manifest": {
            "status": targets.get("status"),
            "candidate_families": [
                {
                    "panel_id": family.get("candidate_family"),
                    "candidate_rows": family.get("candidate_rows", []),
                    "state_counts": dict(
                        sorted(
                            panel_counts.get(
                                str(family.get("candidate_family") or ""),
                                Counter(),
                            ).items()
                        )
                    ),
                    "priority_bins": family.get("priority_bins", []),
                    "required_human_validation": family.get(
                        "required_human_validation"
                    ),
                }
                for family in targets.get("candidate_families", [])
            ],
        },
        "machinery_applied": {
            "row_state_classifier": {
                "method": "deterministic_gate_output_adapter",
                "allowed_states": list(ADMISSION_STATES),
                "classification_input_fields": [
                    "countable_label_candidate",
                    "ready_for_import_preview",
                    "ready_for_label_factory_gate",
                    "gate_blockers",
                    "primary_blocker_class",
                    "locator_decision_class",
                    "locator_resolution_status",
                    "source_check_completion_status",
                    "source_check_family_promotion_ready",
                    "expert_decision_value",
                    "accepted_import_preview_presence",
                    "label_factory_gate_input_presence",
                ],
            },
            "source_artifact_count": len(source_artifacts),
            "source_artifacts": source_artifacts,
        },
        "row_admission_table": row_table,
        "review_packet": {
            "status": "family_label_admission_review_packet_ready",
            "rows": review_rows,
        },
        "import_preview": {
            "status": (
                "family_label_admission_import_preview_ready_review_only"
                if import_rows
                else "family_label_admission_import_preview_empty"
            ),
            "rows": import_rows,
        },
        "rejects_oos_signal_packet": {
            "status": "family_label_admission_rejects_oos_signal_packet_ready",
            "rows": rejects_oos_rows,
        },
        "recommended_next_concrete_family_expansion_task": recommended_next,
    }


def render_family_label_admission_report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    lines = [
        "# Family Label Admission Pipeline - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Outcome",
        "",
        f"- Status: {audit['status']}",
        f"- Candidate axes evaluated: {counts['candidate_family_axes_evaluated']}",
        f"- Candidate rows evaluated: {counts['candidate_rows_evaluated']}",
        f"- State counts: {counts['state_counts']}",
        f"- Import-preview rows: {counts['countable_candidate_rows']}",
        f"- Review packet rows: {counts['review_packet_rows']}",
        f"- Reject/OOS-signal rows: {counts['rejects_oos_signal_rows']}",
        "",
        "## Row Admission Table",
        "",
        "| Panel | Row | State | Blocker class | Allowed next action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in audit["row_admission_table"]:
        lines.append(
            f"| {row['panel_id']} | {row['entry_id']} | {row['state']} | "
            f"{row['state_blocker_class']} | {row['allowed_next_action']} |"
        )
    lines += [
        "",
        "## Outputs",
        "",
        f"- Review packet: {audit['review_packet']['status']} ({len(audit['review_packet']['rows'])} rows)",
        f"- Import preview: {audit['import_preview']['status']} ({len(audit['import_preview']['rows'])} rows)",
        f"- Reject/OOS-signal packet: {audit['rejects_oos_signal_packet']['status']} ({len(audit['rejects_oos_signal_packet']['rows'])} rows)",
        "",
        "## Next Task",
        "",
        audit["recommended_next_concrete_family_expansion_task"],
    ]
    return "\n".join(lines) + "\n"


def write_family_label_admission_pipeline(
    *,
    family_expansion_targets_path: Path,
    family_panel_research_readout_path: Path,
    countability_gate_preflight_path: Path,
    import_preview_blocker_gate_path: Path,
    expert_import_decision_packet_path: Path,
    accepted_import_preview_path: Path,
    label_factory_gate_readiness_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    artifact_id: str = "v3_family_label_admission_pipeline_current702_20260607",
) -> dict[str, Any]:
    audit = build_family_label_admission_pipeline(
        family_expansion_targets_path=family_expansion_targets_path,
        family_panel_research_readout_path=family_panel_research_readout_path,
        countability_gate_preflight_path=countability_gate_preflight_path,
        import_preview_blocker_gate_path=import_preview_blocker_gate_path,
        expert_import_decision_packet_path=expert_import_decision_packet_path,
        accepted_import_preview_path=accepted_import_preview_path,
        label_factory_gate_readiness_path=label_factory_gate_readiness_path,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_family_label_admission_report(audit), encoding="utf-8"
        )
    return audit
