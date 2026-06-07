from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_ID = "v3_family_label_admission_pipeline_current702_20260607"
SCHEMA_VERSION = "v3.family_label_admission_pipeline"

ADMISSION_STATES = (
    "countable_candidate",
    "review_only_evidence",
    "oos_hard_negative",
    "blocked_locator",
    "blocked_coordinate",
    "blocked_family_decision",
    "reject_preserve_signal",
)

DEFAULT_EVIDENCE_PACKET_PATHS = (
    "artifacts/v3_family_panel_evidence_packet_cobalamin_and_radical_rearrangement_panel_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_flavin_monooxygenase_and_flavin_oxygen_transfer_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_glycyl_radical_or_thiamine_radical_lyase_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_lipoamide_or_sulfur_transfer_redox_boundary_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_near_orphan_glycoside_or_nucleoside_hydrolase_controls_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_no_reliable_structure_metal_hydrolase_controls_current702_20260601.json",
    "artifacts/v3_family_panel_evidence_packet_thiol_disulfide_oxidoreductase_isomerase_boundary_current702_20260601.json",
)


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _read_json_required(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"required family admission input missing: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"required family admission input is not a JSON object: {path}")
    return payload


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path),
        "sha256": sha256_path(path),
        "bytes": path.stat().st_size,
    }


def _canonical_sha256(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _list_rows(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    return [row for row in payload.get(key, []) if isinstance(row, dict)]


def _by_entry(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(row["entry_id"]): row
        for row in rows
        if row.get("entry_id") is not None
    }


def _entry_sort_key(entry_id: str) -> tuple[int, str, str]:
    prefix, _, suffix = entry_id.partition(":")
    if suffix.isdigit():
        return (0, prefix, f"{int(suffix):09d}")
    return (1, prefix, suffix or entry_id)


def _is_explicit_countable_signal(row: dict[str, Any]) -> bool:
    label_factory = row.get("label_factory_gate_input") or {}
    preflight = row.get("countability_gate") or {}
    application = row.get("expert_application") or {}
    accepted_preview = row.get("accepted_import_preview") or {}
    return any(
        (
            preflight.get("countable_label_candidate") is True,
            label_factory.get("countable_label_candidate_now") is True,
            label_factory.get("label_factory_gate_result") in {"passed", "pass"},
            application.get("countable_label_candidate_now") is True,
            accepted_preview.get("countable_label_candidate_now") is True,
        )
    )


def _coordinate_blocked(row: dict[str, Any]) -> bool:
    blocker = row.get("import_preview_blocker") or {}
    locator_class = str(blocker.get("locator_decision_class") or "")
    locator_status = str(blocker.get("locator_resolution_status") or "")
    locator_needed = str(blocker.get("locator_decision_needed") or "")
    locator_classes = {
        "accession_equivalence_or_matching_coordinate_required",
    }
    if locator_class in locator_classes:
        return False
    coordinate_classes = {
        "alternate_coordinate_fetch_approval_required",
        "ligand_specificity_validator_or_substrate_coordinate_required",
    }
    if locator_class in coordinate_classes:
        return True
    coordinate_status_terms = (
        "no_coordinate_anchor",
        "pending_fetch_policy",
        "no_local_alternates",
        "substrate_coordinate",
    )
    if any(term in locator_status for term in coordinate_status_terms):
        return True
    if "coordinate" in locator_needed and "locator" not in locator_class:
        return True
    return False


def classify_family_label_admission_row(row: dict[str, Any]) -> dict[str, Any]:
    blocker = row.get("import_preview_blocker") or {}
    preflight = row.get("countability_gate") or {}
    application = row.get("expert_application") or {}
    accepted_preview = row.get("accepted_import_preview") or {}
    label_factory = row.get("label_factory_gate_input") or {}
    primary_blocker = str(
        blocker.get("primary_blocker_class")
        or preflight.get("primary_blocker_class")
        or application.get("primary_blocker_class")
        or ""
    )
    decision = str(application.get("decision") or "")
    critical_violations = application.get("critical_violations") or []
    source_check_status = str(
        preflight.get("source_check_completion_status")
        or blocker.get("source_check_completion_status")
        or ""
    )
    source_check_promotion_ready = (
        preflight.get("source_check_family_promotion_ready")
        if "source_check_family_promotion_ready" in preflight
        else blocker.get("source_check_family_promotion_ready")
    )

    if _is_explicit_countable_signal(row):
        return {
            "state": "countable_candidate",
            "blocker_class": None,
            "allowed_next_action": (
                "review the passing label-factory gate output before any separate "
                "label import or registry change"
            ),
            "classification_basis": "explicit_countable_gate_signal",
        }
    if decision.startswith("reject_"):
        return {
            "state": "reject_preserve_signal",
            "blocker_class": "explicit_expert_reject",
            "allowed_next_action": (
                "preserve the reviewed rejection/OOS signal and do not import"
            ),
            "classification_basis": "explicit_reject_decision",
        }
    if critical_violations:
        return {
            "state": "reject_preserve_signal",
            "blocker_class": "decision_integrity_violation",
            "allowed_next_action": (
                "repair the reviewed decision record and matching context hash"
            ),
            "classification_basis": "decision_application_critical_violations",
        }
    if accepted_preview or label_factory:
        return {
            "state": "review_only_evidence",
            "blocker_class": "label_factory_gate_not_run",
            "allowed_next_action": (
                "run the family-panel label-factory gate on accepted preview rows"
            ),
            "classification_basis": "accepted_preview_or_gate_input_review_only",
        }
    if primary_blocker == "source_free_locator_or_primary_channel_missing":
        if _coordinate_blocked(row):
            return {
                "state": "blocked_coordinate",
                "blocker_class": "coordinate_or_coordinate_policy_missing",
                "allowed_next_action": (
                    blocker.get("locator_decision_needed")
                    or "provide an approved coordinate source before scoring"
                ),
                "classification_basis": "source_free_coordinate_or_policy_blocker",
            }
        return {
            "state": "blocked_locator",
            "blocker_class": "source_free_locator_or_position_mapping_missing",
            "allowed_next_action": (
                blocker.get("locator_decision_needed")
                or "record source-free locator or position-mapping approval"
            ),
            "classification_basis": "source_free_locator_blocker",
        }
    if primary_blocker == "expert_family_admission_decision_required":
        return {
            "state": "blocked_family_decision",
            "blocker_class": "expert_family_admission_decision_required",
            "allowed_next_action": (
                "record an explicit expert accept/reject/review-only decision "
                "with the preserved decision_context_sha256"
            ),
            "classification_basis": "pending_expert_family_admission_decision",
        }
    if (
        primary_blocker == "completed_source_check_review_only_no_promotion"
        or (
            source_check_status == "completed_review_only_no_label_change"
            and source_check_promotion_ready is False
        )
    ):
        return {
            "state": "oos_hard_negative",
            "blocker_class": "completed_source_check_no_family_promotion",
            "allowed_next_action": (
                "preserve as OOS/boundary signal unless a separate family-promotion "
                "override is explicitly reviewed"
            ),
            "classification_basis": "completed_review_only_source_check_no_promotion",
        }
    if row.get("research_readout") or row.get("evidence_packet"):
        return {
            "state": "review_only_evidence",
            "blocker_class": "review_only_no_import_gate",
            "allowed_next_action": "preserve evidence and route through admission gates",
            "classification_basis": "evidence_present_without_import_authority",
        }
    return {
        "state": "reject_preserve_signal",
        "blocker_class": "fail_closed_unrecognized_admission_context",
        "allowed_next_action": "add a recognized admission gate source before reuse",
        "classification_basis": "unrecognized_context_fail_closed",
    }


def _compact_evidence(row: dict[str, Any]) -> dict[str, Any]:
    evidence = row.get("evidence_packet") or {}
    research = row.get("research_readout") or {}
    preflight = row.get("countability_gate") or {}
    blocker = row.get("import_preview_blocker") or {}
    stub = row.get("expert_decision_stub") or {}
    application = row.get("expert_application") or {}
    locator = row.get("locator_decision") or {}
    retrieval = row.get("source_free_retrieval") or {}
    return {
        "mechanism_and_review_signal": {
            "evidence_role": evidence.get("evidence_role"),
            "benchmark_role": (
                evidence.get("benchmark_role") or research.get("benchmark_role")
            ),
            "split_assignment": (
                evidence.get("split_assignment") or research.get("split_assignment")
            ),
            "catalytic_residues_roles": (
                evidence.get("catalytic_residues_roles")
                or evidence.get("catalytic_residue_roles")
                or evidence.get("residue_roles")
            ),
            "bond_electron_proton_hints": (
                evidence.get("bond_electron_proton_hints")
                or evidence.get("bond_change_hints")
                or evidence.get("electron_flow_hints")
                or evidence.get("proton_transfer_hints")
            ),
        },
        "cofactor_metal_signal": {
            "selected_organic_cofactor_max": (
                evidence.get("selected_organic_cofactor_max")
                or research.get("selected_organic_cofactor_max")
            ),
            "selected_organic_cofactor_scores": evidence.get(
                "selected_organic_cofactor_scores"
            ),
            "predicted_geometry_top1_cofactor_context_score": (
                (evidence.get("predicted_geometry_top1") or {}).get(
                    "cofactor_context_score"
                )
            ),
            "source_free_top1_cofactor_evidence_level": (
                (retrieval.get("predicted_geometry_retrieval") or {}).get(
                    "top1_cofactor_evidence_level"
                )
            ),
        },
        "active_site_geometry": {
            "predicted_geometry_status": (
                evidence.get("predicted_geometry_status")
                or research.get("predicted_geometry_status")
                or retrieval.get("predicted_geometry_status")
            ),
            "predicted_geometry_top1": evidence.get("predicted_geometry_top1"),
            "predicted_atlas_geometry_variant_scores": evidence.get(
                "predicted_atlas_geometry_variant_scores"
            ),
            "resolved_residue_count": retrieval.get("resolved_residue_count"),
            "source_free_locator_sidecar": retrieval.get(
                "source_free_locator_sidecar"
            ),
        },
        "predicted_vs_experimental_context": {
            "predicted_structure_fold_channel": (
                evidence.get("predicted_structure_fold_channel")
                or retrieval.get("predicted_structure_fold_channel")
            ),
            "selected_pdb_fold_proxy": evidence.get("selected_pdb_fold_proxy"),
            "predicted_geometry_accession_repair": evidence.get(
                "predicted_geometry_accession_repair"
            ),
            "reconstruction_status": (
                evidence.get("reconstruction_status")
                or locator.get("previous_action_class")
            ),
        },
        "fold_tm_or_lever3_gate_result": {
            "research_gate_status": (
                research.get("research_gate_status")
                or preflight.get("research_gate_status")
                or blocker.get("research_gate_status")
            ),
            "primary_channel": research.get("primary_channel"),
            "primary_threshold": research.get("primary_threshold"),
            "primary_threshold_margin": research.get("primary_threshold_margin"),
            "channel_scores": research.get("channel_scores"),
            "predicted_structure_nearest_atlas_entry_id": research.get(
                "predicted_structure_nearest_atlas_entry_id"
            ),
            "predicted_structure_nearest_atlas_true_fingerprint_id": research.get(
                "predicted_structure_nearest_atlas_true_fingerprint_id"
            ),
        },
        "source_free_locator_provenance": {
            "locator_resolution_status": blocker.get("locator_resolution_status"),
            "locator_decision_class": blocker.get("locator_decision_class"),
            "locator_decision_needed": blocker.get("locator_decision_needed"),
            "locator_matrix_row": locator or None,
        },
        "gates_and_decisions": {
            "gate_blockers": (
                blocker.get("gate_blockers") or preflight.get("gate_blockers") or []
            ),
            "ready_for_import_preview": (
                blocker.get("ready_for_import_preview")
                or preflight.get("ready_for_import_preview")
            ),
            "ready_for_label_factory_gate": (
                blocker.get("ready_for_label_factory_gate")
                or preflight.get("ready_for_label_factory_gate")
            ),
            "source_check_completion_status": (
                blocker.get("source_check_completion_status")
                or preflight.get("source_check_completion_status")
            ),
            "source_check_family_promotion_ready": (
                blocker.get("source_check_family_promotion_ready")
                if "source_check_family_promotion_ready" in blocker
                else preflight.get("source_check_family_promotion_ready")
            ),
            "expert_decision": application.get("decision") or stub.get("default_decision"),
            "review_status": application.get("review_status") or stub.get("review_status"),
            "allowed_decisions": stub.get("allowed_decisions") or [],
            "decision_context_sha256": (
                application.get("decision_context_sha256")
                or stub.get("decision_context_sha256")
            ),
        },
    }


def _row_source_hashes(
    *,
    entry_id: str,
    row: dict[str, Any],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, str]:
    sources: dict[str, str] = {}
    if source_records.get("family_set_expansion_targets"):
        sources["family_set_expansion_targets"] = source_records[
            "family_set_expansion_targets"
        ]["sha256"]
    evidence_source_key = row.get("evidence_packet_source_key")
    if evidence_source_key and evidence_source_key in source_records:
        sources[str(evidence_source_key)] = str(
            source_records[str(evidence_source_key)]["sha256"]
        )
    if row.get("countability_gate") and source_records.get("countability_gate_preflight"):
        sources["countability_gate_preflight"] = source_records[
            "countability_gate_preflight"
        ]["sha256"]
    if row.get("import_preview_blocker") and source_records.get(
        "import_preview_blocker_gate"
    ):
        sources["import_preview_blocker_gate"] = source_records[
            "import_preview_blocker_gate"
        ]["sha256"]
    if row.get("expert_decision_stub") and source_records.get(
        "expert_import_decision_packet"
    ):
        sources["expert_import_decision_packet"] = source_records[
            "expert_import_decision_packet"
        ]["sha256"]
    if row.get("acceptance_scenario") and source_records.get(
        "acceptance_scenario_plan"
    ):
        sources["acceptance_scenario_plan"] = source_records[
            "acceptance_scenario_plan"
        ]["sha256"]
    if row.get("expert_application") and source_records.get(
        "expert_import_decision_application"
    ):
        sources["expert_import_decision_application"] = source_records[
            "expert_import_decision_application"
        ]["sha256"]
    if row.get("accepted_import_preview") and source_records.get(
        "accepted_import_preview"
    ):
        sources["accepted_import_preview"] = source_records[
            "accepted_import_preview"
        ]["sha256"]
    if row.get("label_factory_gate_input") and source_records.get(
        "label_factory_gate_readiness"
    ):
        sources["label_factory_gate_readiness"] = source_records[
            "label_factory_gate_readiness"
        ]["sha256"]
    if row.get("research_readout") and source_records.get("research_readout"):
        sources["research_readout"] = source_records["research_readout"]["sha256"]
    if row.get("locator_decision") and source_records.get(
        "locator_human_decision_matrix"
    ):
        sources["locator_human_decision_matrix"] = source_records[
            "locator_human_decision_matrix"
        ]["sha256"]
    if row.get("source_free_retrieval") and source_records.get(
        "source_free_predicted_geometry_retrieval"
    ):
        sources["source_free_predicted_geometry_retrieval"] = source_records[
            "source_free_predicted_geometry_retrieval"
        ]["sha256"]
    if not sources:
        raise ValueError(f"row has no source hashes after admission merge: {entry_id}")
    return dict(sorted(sources.items()))


def build_family_label_admission_pipeline(
    *,
    family_set_expansion_targets_path: Path,
    countability_gate_preflight_path: Path,
    import_preview_blocker_gate_path: Path,
    expert_import_decision_packet_path: Path,
    acceptance_scenario_plan_path: Path,
    expert_import_decision_application_path: Path,
    accepted_import_preview_path: Path,
    label_factory_gate_readiness_path: Path,
    research_readout_path: Path,
    locator_human_decision_matrix_path: Path,
    source_free_predicted_geometry_retrieval_path: Path,
    evidence_packet_paths: list[Path] | None = None,
    artifact_id: str = ARTIFACT_ID,
) -> dict[str, Any]:
    evidence_packet_paths = evidence_packet_paths or [
        Path(path) for path in DEFAULT_EVIDENCE_PACKET_PATHS
    ]
    input_paths = {
        "family_set_expansion_targets": family_set_expansion_targets_path,
        "countability_gate_preflight": countability_gate_preflight_path,
        "import_preview_blocker_gate": import_preview_blocker_gate_path,
        "expert_import_decision_packet": expert_import_decision_packet_path,
        "acceptance_scenario_plan": acceptance_scenario_plan_path,
        "expert_import_decision_application": expert_import_decision_application_path,
        "accepted_import_preview": accepted_import_preview_path,
        "label_factory_gate_readiness": label_factory_gate_readiness_path,
        "research_readout": research_readout_path,
        "locator_human_decision_matrix": locator_human_decision_matrix_path,
        "source_free_predicted_geometry_retrieval": (
            source_free_predicted_geometry_retrieval_path
        ),
    }
    payloads = {
        key: _read_json_required(path) for key, path in input_paths.items()
    }
    evidence_payloads: list[tuple[str, Path, dict[str, Any]]] = []
    for index, path in enumerate(evidence_packet_paths):
        evidence_payloads.append(
            (f"family_panel_evidence_packet_{index}", path, _read_json_required(path))
        )

    source_records = {
        key: _source_record(path) for key, path in input_paths.items()
    }
    for key, path, _payload in evidence_payloads:
        source_records[key] = _source_record(path)

    family_axis_by_panel: dict[str, dict[str, Any]] = {}
    for family in _list_rows(payloads["family_set_expansion_targets"], "candidate_families"):
        panel_id = str(family.get("candidate_family") or "")
        if panel_id:
            family_axis_by_panel[panel_id] = family

    evidence_by_entry: dict[str, dict[str, Any]] = {}
    evidence_source_by_entry: dict[str, str] = {}
    for source_key, _path, payload in evidence_payloads:
        panel = payload.get("panel", {}) if isinstance(payload.get("panel"), dict) else {}
        panel_id = str(panel.get("candidate_family") or "")
        for row in _list_rows(payload, "row_evidence"):
            entry_id = str(row.get("entry_id") or "")
            if not entry_id:
                continue
            merged = dict(row)
            if panel_id and "panel_id" not in merged:
                merged["panel_id"] = panel_id
            evidence_by_entry[entry_id] = merged
            evidence_source_by_entry[entry_id] = source_key

    research_by_entry = _by_entry(
        _list_rows(payloads["research_readout"], "row_scores")
    )
    preflight_by_entry = _by_entry(
        _list_rows(payloads["countability_gate_preflight"], "row_gate_status")
    )
    blocker_by_entry = _by_entry(
        _list_rows(payloads["import_preview_blocker_gate"], "row_blockers")
    )
    stub_by_entry = _by_entry(
        _list_rows(payloads["expert_import_decision_packet"], "expert_import_decision_stubs")
    )
    application_by_entry = _by_entry(
        _list_rows(payloads["expert_import_decision_application"], "row_decisions")
    )
    accepted_preview_by_entry = _by_entry(
        _list_rows(payloads["accepted_import_preview"], "accepted_import_preview_rows")
    )
    label_factory_by_entry = _by_entry(
        _list_rows(payloads["label_factory_gate_readiness"], "label_factory_gate_input_rows")
    )
    locator_by_entry = _by_entry(
        _list_rows(payloads["locator_human_decision_matrix"], "row_decisions")
    )
    retrieval_by_entry = _by_entry(
        _list_rows(payloads["source_free_predicted_geometry_retrieval"], "row_scores")
    )
    scenario_by_entry = _by_entry(
        _list_rows(payloads["acceptance_scenario_plan"], "acceptance_scenario_rows")
    )

    entry_ids = sorted(
        set(preflight_by_entry)
        | set(blocker_by_entry)
        | set(stub_by_entry)
        | set(application_by_entry)
        | set(accepted_preview_by_entry)
        | set(label_factory_by_entry)
        | set(research_by_entry)
        | set(evidence_by_entry),
        key=_entry_sort_key,
    )
    if not entry_ids:
        raise ValueError("family admission pipeline has no candidate rows to classify")

    row_admission_table: list[dict[str, Any]] = []
    for entry_id in entry_ids:
        panel_id = str(
            (blocker_by_entry.get(entry_id) or {}).get("panel_id")
            or (preflight_by_entry.get(entry_id) or {}).get("panel_id")
            or (stub_by_entry.get(entry_id) or {}).get("panel_id")
            or (research_by_entry.get(entry_id) or {}).get("panel_id")
            or (evidence_by_entry.get(entry_id) or {}).get("panel_id")
            or ""
        )
        merged = {
            "entry_id": entry_id,
            "panel_id": panel_id,
            "family_axis": family_axis_by_panel.get(panel_id),
            "evidence_packet": evidence_by_entry.get(entry_id),
            "evidence_packet_source_key": evidence_source_by_entry.get(entry_id),
            "research_readout": research_by_entry.get(entry_id),
            "countability_gate": preflight_by_entry.get(entry_id),
            "import_preview_blocker": blocker_by_entry.get(entry_id),
            "expert_decision_stub": stub_by_entry.get(entry_id),
            "acceptance_scenario": scenario_by_entry.get(entry_id),
            "expert_application": application_by_entry.get(entry_id),
            "accepted_import_preview": accepted_preview_by_entry.get(entry_id),
            "label_factory_gate_input": label_factory_by_entry.get(entry_id),
            "locator_decision": locator_by_entry.get(entry_id),
            "source_free_retrieval": retrieval_by_entry.get(entry_id),
        }
        classification = classify_family_label_admission_row(merged)
        row_context_payload = {
            "entry_id": entry_id,
            "panel_id": panel_id,
            "classification": classification,
            "merged_context": merged,
        }
        source_hashes = _row_source_hashes(
            entry_id=entry_id,
            row=merged,
            source_records=source_records,
        )
        row_admission_table.append(
            {
                "entry_id": entry_id,
                "candidate_family_axis": panel_id,
                "admission_state": classification["state"],
                "blocker_class": classification["blocker_class"],
                "classification_basis": classification["classification_basis"],
                "allowed_next_action": classification["allowed_next_action"],
                "would_enter_import_preview_if_accepted": bool(
                    (scenario_by_entry.get(entry_id) or {}).get(
                        "would_enter_import_preview_if_accepted"
                    )
                ),
                "evidence_preserved": _compact_evidence(merged),
                "source_hashes": source_hashes,
                "row_context_sha256": _canonical_sha256(row_context_payload),
            }
        )

    state_counts = Counter(row["admission_state"] for row in row_admission_table)
    panel_state_counts: defaultdict[str, Counter[str]] = defaultdict(Counter)
    for row in row_admission_table:
        panel_state_counts[row["candidate_family_axis"]][row["admission_state"]] += 1
    family_onboarding_manifest = [
        {
            "candidate_family_axis": panel_id,
            "candidate_rows_declared": family.get("candidate_rows") or [],
            "candidate_sources": family.get("candidate_sources") or [],
            "priority_bins": family.get("priority_bins") or [],
            "required_human_validation": family.get("required_human_validation"),
            "evaluated_rows": sorted(
                [
                    row["entry_id"]
                    for row in row_admission_table
                    if row["candidate_family_axis"] == panel_id
                ],
                key=_entry_sort_key,
            ),
            "admission_state_counts": dict(sorted(panel_state_counts[panel_id].items())),
        }
        for panel_id, family in sorted(family_axis_by_panel.items())
    ]

    blocked_family_rows = [
        row
        for row in row_admission_table
        if row["admission_state"] == "blocked_family_decision"
    ]
    blocked_locator_rows = [
        row
        for row in row_admission_table
        if row["admission_state"] == "blocked_locator"
    ]
    blocked_coordinate_rows = [
        row
        for row in row_admission_table
        if row["admission_state"] == "blocked_coordinate"
    ]
    import_preview_rows = [
        row
        for row in row_admission_table
        if row["admission_state"] in {"countable_candidate", "review_only_evidence"}
        and (
            (accepted_preview_by_entry.get(row["entry_id"]) is not None)
            or (label_factory_by_entry.get(row["entry_id"]) is not None)
            or row["admission_state"] == "countable_candidate"
        )
    ]
    oos_signal_rows = [
        row
        for row in row_admission_table
        if row["admission_state"] in {"oos_hard_negative", "reject_preserve_signal"}
    ]

    if blocked_family_rows:
        previewable = [
            row for row in blocked_family_rows if row["would_enter_import_preview_if_accepted"]
        ]
        targets = previewable or blocked_family_rows
        next_task = (
            "Adjudicate the blocked family-decision rows with preserved "
            "decision_context_sha256 values, starting with "
            + ", ".join(row["entry_id"] for row in targets[:6])
            + "; then rerun the expert-decision application and accepted "
            "import-preview builders."
        )
        human_decision_needed = (
            "explicit accept/reject/review-only expert decisions for "
            f"{len(blocked_family_rows)} family-panel rows"
        )
    elif blocked_locator_rows:
        first = blocked_locator_rows[0]
        next_task = (
            "Resolve the highest-priority blocked locator row "
            f"{first['entry_id']}: {first['allowed_next_action']}"
        )
        human_decision_needed = "source-free locator or position-mapping approval"
    elif blocked_coordinate_rows:
        first = blocked_coordinate_rows[0]
        next_task = (
            "Resolve the highest-priority blocked coordinate row "
            f"{first['entry_id']}: {first['allowed_next_action']}"
        )
        human_decision_needed = "coordinate-source or coordinate-policy approval"
    elif import_preview_rows:
        next_task = (
            "Run the family-panel label-factory gate on the accepted "
            "review-only import-preview rows."
        )
        human_decision_needed = None
    else:
        next_task = "Review preserved OOS/reject signals and select the next family axis."
        human_decision_needed = None

    blockers = []
    if blocked_family_rows:
        blockers.append("family_decisions_pending")
    if blocked_locator_rows:
        blockers.append("source_free_locators_pending")
    if blocked_coordinate_rows:
        blockers.append("coordinates_or_coordinate_policy_pending")
    if state_counts.get("countable_candidate", 0) == 0:
        blockers.append("no_countable_candidates_from_current_inputs")

    return {
        "artifact_id": artifact_id,
        "schema_version": SCHEMA_VERSION,
        "created_utc": _utc_now_iso(),
        "status": "family_label_admission_pipeline_ready_review_only",
        "scope": (
            "Small deterministic family-label admission pipeline for current702 "
            "family-panel rows. It normalizes existing family-panel gates into "
            "one row-level state, preserves mechanism/provenance signal, and "
            "does not import, promote, score heldout, refit, or change thresholds."
        ),
        "admission_states": list(ADMISSION_STATES),
        "guardrails": {
            "review_only": True,
            "labels_registries_ontologies_changed": False,
            "imports_or_promotions_performed": False,
            "label_factory_gate_run": False,
            "family_panel_rows_countable_now": False,
            "production_thresholds_changed": False,
            "threshold_values_changed": False,
            "model_weights_fit_or_refit": False,
            "heldout_rows_used_for_training": False,
            "mechanism_text_or_ids_used_as_predictive_features": False,
        },
        "counts": {
            "candidate_rows_evaluated": len(row_admission_table),
            "family_axes_evaluated": len(
                {row["candidate_family_axis"] for row in row_admission_table}
            ),
            "admission_state_counts": {
                state: int(state_counts.get(state, 0)) for state in ADMISSION_STATES
            },
            "import_preview_rows": len(import_preview_rows),
            "review_packet_rows": (
                len(blocked_family_rows)
                + len(blocked_locator_rows)
                + len(blocked_coordinate_rows)
            ),
            "oos_signal_rows": len(oos_signal_rows),
            "blockers": len(blockers),
        },
        "machinery_applied": [
            "family_set_expansion_targets",
            "family_panel_evidence_packets",
            "fold_augmented_family_panel_research_readout",
            "family_panel_countability_gate_preflight",
            "family_panel_import_preview_blocker_gate",
            "family_panel_expert_import_decision_packet",
            "family_panel_acceptance_scenario_plan",
            "family_panel_expert_import_decision_application",
            "family_panel_accepted_import_preview",
            "family_panel_label_factory_gate_readiness",
            "family_panel_source_free_locator_human_decision_matrix",
            "family_panel_source_free_predicted_geometry_retrieval",
        ],
        "blockers": blockers,
        "family_onboarding_manifest": family_onboarding_manifest,
        "row_admission_table": row_admission_table,
        "review_packet": {
            "blocked_family_decision_rows": blocked_family_rows,
            "blocked_locator_rows": blocked_locator_rows,
            "blocked_coordinate_rows": blocked_coordinate_rows,
        },
        "import_preview": {
            "rows": import_preview_rows,
            "countable_candidates": [
                row
                for row in row_admission_table
                if row["admission_state"] == "countable_candidate"
            ],
        },
        "rejects_oos_signal_packet": {
            "rows": oos_signal_rows,
            "oos_hard_negative_rows": [
                row
                for row in oos_signal_rows
                if row["admission_state"] == "oos_hard_negative"
            ],
            "reject_preserve_signal_rows": [
                row
                for row in oos_signal_rows
                if row["admission_state"] == "reject_preserve_signal"
            ],
        },
        "recommended_next_concrete_family_expansion_task": next_task,
        "human_decision_needed": human_decision_needed,
        "source_artifacts": source_records,
        "interpretation": {
            "headline": (
                f"{len(row_admission_table)} family-panel rows classified into "
                "exactly one admission state each."
            ),
            "result": (
                "The current inputs emit no countable candidates and no import "
                "preview rows; they preserve OOS signal plus pending family, "
                "locator, and coordinate blockers."
            ),
            "next_action": next_task,
        },
    }


def render_family_label_admission_pipeline_report(audit: dict[str, Any]) -> str:
    counts = audit["counts"]
    lines = [
        "# Family Label Admission Pipeline - current702",
        "",
        f"Run: {audit['created_utc']}",
        "",
        audit["scope"],
        "",
        "## Status",
        "",
        f"- {audit['status']}",
        f"- Candidate rows evaluated: {counts['candidate_rows_evaluated']}",
        f"- Family axes evaluated: {counts['family_axes_evaluated']}",
        f"- Admission states: {counts['admission_state_counts']}",
        f"- Import-preview rows: {counts['import_preview_rows']}",
        f"- Review-packet rows: {counts['review_packet_rows']}",
        f"- OOS/reject signal rows: {counts['oos_signal_rows']}",
        f"- Blockers: {audit['blockers']}",
        "",
        "## Machinery Applied",
        "",
    ]
    lines.extend(f"- {item}" for item in audit["machinery_applied"])
    lines += [
        "",
        "## Family Axes",
        "",
        "| family axis | evaluated rows | states |",
        "| --- | ---: | --- |",
    ]
    for row in audit["family_onboarding_manifest"]:
        lines.append(
            f"| {row['candidate_family_axis']} | {len(row['evaluated_rows'])} | "
            f"{row['admission_state_counts']} |"
        )
    lines += [
        "",
        "## Row Admission Table",
        "",
        "| row | family axis | state | blocker | next action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in audit["row_admission_table"]:
        lines.append(
            f"| {row['entry_id']} | {row['candidate_family_axis']} | "
            f"{row['admission_state']} | {row['blocker_class'] or 'none'} | "
            f"{row['allowed_next_action']} |"
        )
    lines += [
        "",
        "## Outputs",
        "",
        "- Review packet: "
        f"{counts['review_packet_rows']} unresolved family/locator/coordinate rows.",
        "- Import preview: "
        f"{counts['import_preview_rows']} rows from current inputs.",
        "- Rejects/OOS signal packet: "
        f"{counts['oos_signal_rows']} preserved signal rows.",
        "",
        "## Next Task",
        "",
        f"- {audit['recommended_next_concrete_family_expansion_task']}",
    ]
    if audit.get("human_decision_needed"):
        lines.append(f"- Human decision needed: {audit['human_decision_needed']}")
    return "\n".join(lines) + "\n"


def write_family_label_admission_pipeline(
    *,
    family_set_expansion_targets_path: Path,
    countability_gate_preflight_path: Path,
    import_preview_blocker_gate_path: Path,
    expert_import_decision_packet_path: Path,
    acceptance_scenario_plan_path: Path,
    expert_import_decision_application_path: Path,
    accepted_import_preview_path: Path,
    label_factory_gate_readiness_path: Path,
    research_readout_path: Path,
    locator_human_decision_matrix_path: Path,
    source_free_predicted_geometry_retrieval_path: Path,
    out_path: Path,
    report_path: Path | None = None,
    evidence_packet_paths: list[Path] | None = None,
    artifact_id: str = ARTIFACT_ID,
) -> dict[str, Any]:
    audit = build_family_label_admission_pipeline(
        family_set_expansion_targets_path=family_set_expansion_targets_path,
        countability_gate_preflight_path=countability_gate_preflight_path,
        import_preview_blocker_gate_path=import_preview_blocker_gate_path,
        expert_import_decision_packet_path=expert_import_decision_packet_path,
        acceptance_scenario_plan_path=acceptance_scenario_plan_path,
        expert_import_decision_application_path=expert_import_decision_application_path,
        accepted_import_preview_path=accepted_import_preview_path,
        label_factory_gate_readiness_path=label_factory_gate_readiness_path,
        research_readout_path=research_readout_path,
        locator_human_decision_matrix_path=locator_human_decision_matrix_path,
        source_free_predicted_geometry_retrieval_path=(
            source_free_predicted_geometry_retrieval_path
        ),
        evidence_packet_paths=evidence_packet_paths,
        artifact_id=artifact_id,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            render_family_label_admission_pipeline_report(audit),
            encoding="utf-8",
        )
    return audit
