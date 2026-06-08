from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT_ID = "v3_targeted_expansion_factory_batch_current702_20260608"
SCHEMA_VERSION = "v3.targeted_expansion_factory_batch"

DEFAULT_SOURCE_PATHS = {
    "active_learning_1025_preview": (
        "artifacts/v3_active_learning_review_queue_1025_preview_batch.json"
    ),
    "external_panel_router_queue": (
        "artifacts/v3_external_panel_router_queue_20260528.json"
    ),
    "external_hard_negative_next_sourcing": (
        "artifacts/v3_external_hard_negative_next_candidate_sourcing_1025.json"
    ),
    "external_hard_negative_new_sourcing": (
        "artifacts/v3_external_hard_negative_new_candidate_sourcing_1025.json"
    ),
    "label_expansion_candidates_1025": (
        "artifacts/v3_label_expansion_candidates_1025.json"
    ),
    "local_evidence_gap_audit_1025": (
        "artifacts/v3_expert_label_decision_local_evidence_gap_audit_1025.json"
    ),
    "coordinate_readiness_1000": (
        "artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json"
    ),
    "architecture_default_decisions": (
        "artifacts/"
        "v3_family_label_admission_architecture_default_decisions_current702_20260608.json"
    ),
}

ADMISSION_STATES = (
    "countable_candidate",
    "review_only_evidence",
    "reject/OOS_preserve_signal",
    "blocked_locator",
    "blocked_coordinate",
    "blocked_family_decision",
    "acquisition_needed",
)

CANDIDATE_SOURCE_NAMES = {
    "active_learning_1025_preview",
    "external_panel_router_queue",
    "external_hard_negative_next_sourcing",
    "external_hard_negative_new_sourcing",
}

ARCHITECTURE_DEFAULT_ENTRY_IDS = {
    "m_csa:10": "reject_family_panel_import_candidate",
    "m_csa:30": "reject_family_panel_import_candidate",
    "m_csa:31": "reject_family_panel_import_candidate",
    "m_csa:191": "reject_family_panel_import_candidate",
    "m_csa:448": "keep_family_panel_review_only_require_more_evidence",
    "m_csa:973": "keep_family_panel_review_only_require_more_evidence",
}


def _utc_now_iso() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


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


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if not isinstance(payload, dict):
        return []
    for key in (
        "rows",
        "queue_rows",
        "candidate_rows",
        "review_items",
        "expert_import_decisions",
    ):
        rows = payload.get(key)
        if isinstance(rows, list):
            return [row for row in rows if isinstance(row, dict)]
    return []


def _row_id(row: dict[str, Any]) -> str | None:
    for key in ("entry_id", "candidate_id"):
        value = row.get(key)
        if value:
            return str(value)
    accession = row.get("accession")
    if accession:
        return f"uniprot:{accession}"
    return None


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _string_tokens(record: dict[str, Any]) -> str:
    pieces: list[str] = []
    for source in record["source_rows"].values():
        for row in source:
            for key in (
                "source_panels",
                "proposed_routes_or_strata",
                "panel_roles",
                "hard_negative_roles",
                "top1_fingerprint_id",
                "top1_ontology_family",
                "cofactor_families",
                "cofactor_evidence_level",
                "atp_phosphoryl_transfer_family_id",
                "lane_id",
                "panel_id",
                "readiness_blockers",
            ):
                for value in _as_list(row.get(key)):
                    pieces.append(str(value))
    return " ".join(pieces).lower()


def _has_any(text: str, *needles: str) -> bool:
    return any(needle in text for needle in needles)


def _family_axis(record: dict[str, Any]) -> str:
    text = _string_tokens(record)
    if _has_any(text, "radical", "sam", "cobalamin", "fe_s", "fe-s"):
        return "radical_cobalamin_sam_like_probes"
    if _has_any(text, "glycoside", "glycan", "carbohydrate", "nucleoside"):
        return "glycoside_or_nucleoside_hydrolase_controls"
    if _has_any(text, "plp", "aminotransferase", "schiff"):
        return "plp_child_subclasses"
    if _has_any(
        text,
        "flavin",
        "heme",
        "oxidoreductase",
        "oxygenase",
        "peroxidase",
        "monooxygenase",
        "redox",
        "lipoamide",
        "sulfur",
        "thiol",
        "disulfide",
    ):
        return "redox_oxygen_transfer_and_sulfur_lipoamide"
    if _has_any(
        text,
        "metal_dependent_hydrolase",
        "metal_hydrolase",
        "metallo",
        "phosphatase",
        "nuclease",
        "hydrolase",
        "zinc",
    ):
        return "metal_hydrolase_subclasses"
    if _has_any(text, "ser_his", "serine_hydrolase"):
        return "serine_hydrolase_boundary"
    if _has_any(text, "atp", "kinase", "phosphoryl", "transferase_phosphoryl"):
        return "phosphoryl_transfer_boundary"
    if _coordinate_blocked(record) or _locator_blocked(record):
        return "no_reliable_structure_or_locator_gap"
    return "near_orphan_or_unrepresented_mechanism_tail"


def _first_value(record: dict[str, Any], *keys: str) -> Any:
    for source in record["source_rows"].values():
        for row in source:
            for key in keys:
                value = row.get(key)
                if value not in (None, "", []):
                    return value
    return None


def _all_values(record: dict[str, Any], key: str) -> list[Any]:
    values: list[Any] = []
    for source in record["source_rows"].values():
        for row in source:
            values.extend(_as_list(row.get(key)))
    return values


def _architecture_default_state(entry_id: str) -> str | None:
    decision = ARCHITECTURE_DEFAULT_ENTRY_IDS.get(entry_id)
    if decision == "reject_family_panel_import_candidate":
        return "reject/OOS_preserve_signal"
    if decision == "keep_family_panel_review_only_require_more_evidence":
        return "review_only_evidence"
    return None


def _locator_blocked(record: dict[str, Any]) -> bool:
    blockers = {str(value) for value in _all_values(record, "readiness_blockers")}
    if "fewer_than_three_resolved_residues" in blockers:
        return True
    local_gap_classes = {
        str(value)
        for value in _all_values(record, "local_evidence_gap_classes")
    }
    if any("active_site_mapping" in value for value in local_gap_classes):
        return True
    statuses = {str(value) for value in _all_values(record, "active_site_evidence_status")}
    if "binding_or_reaction_context_only" in statuses:
        return True
    return False


def _coordinate_blocked(record: dict[str, Any]) -> bool:
    blockers = {str(value) for value in _all_values(record, "readiness_blockers")}
    if "geometry_status_not_ok" in blockers:
        return True
    coordinate_status = str(_first_value(record, "coordinate_status") or "")
    if "missing" in coordinate_status or "blocked" in coordinate_status:
        return True
    sourcing_statuses = {str(value) for value in _all_values(record, "sourcing_status")}
    if "blocked_source_sourcing_criteria" in sourcing_statuses:
        return True
    return False


def _needs_acquisition(record: dict[str, Any]) -> bool:
    statuses = {str(value) for value in _all_values(record, "sourcing_status")}
    if statuses & {
        "blocked_active_site_source_missing",
        "blocked_uncovered_mechanism_lane",
        "excluded_current_external_pool",
        "excluded_prior_new_candidate_pool",
        "sourced_pending_sequence_structure_distance_screens",
    }:
        return True
    active_site_statuses = {
        str(value) for value in _all_values(record, "active_site_evidence_status")
    }
    if active_site_statuses & {"not_sampled_metadata_blocked", "not_sampled_cap_reached"}:
        return True
    return False


def _oos_or_reject_signal(record: dict[str, Any]) -> bool:
    label_values = {
        str(value)
        for value in (
            _all_values(record, "current_label_type")
            + _all_values(record, "target_label_type")
            + _all_values(record, "label_type")
        )
    }
    if "out_of_scope" in label_values:
        return True
    text = _string_tokens(record)
    if _has_any(text, "hard_negative", "oos_control", "out_of_scope_control"):
        return True
    recommended = {str(value) for value in _all_values(record, "recommended_action")}
    if "hold_bronze_boundary_review" in recommended:
        return True
    return False


def _countable_signal(record: dict[str, Any]) -> bool:
    # Countable promotion still requires an explicit label-factory gate. This
    # factory only preserves rows that already carry a positive gate signal.
    for source in record["source_rows"].values():
        for row in source:
            if row.get("countable_label_candidate") is True and (
                row.get("ready_for_label_import") is True
                or row.get("import_ready_candidate") is True
            ):
                return True
    return False


def _admission_state(record: dict[str, Any]) -> tuple[str, str, str]:
    entry_id = str(record["candidate_id"])
    architecture_state = _architecture_default_state(entry_id)
    if architecture_state is not None:
        return (
            architecture_state,
            "architecture_default_non_counting_disposition_reused",
            (
                "preserve the existing architecture-default disposition; do not "
                "ask for another family-admission decision"
            ),
        )
    if _countable_signal(record):
        return (
            "countable_candidate",
            "explicit_countable_and_import_ready_source_signal",
            "run separate human promotion review and label-factory gates before import",
        )
    if _coordinate_blocked(record):
        return (
            "blocked_coordinate",
            "coordinate_or_geometry_status_blocked",
            "materialize or approve a valid coordinate source before scoring",
        )
    if _locator_blocked(record):
        return (
            "blocked_locator",
            "source_free_locator_or_active_site_mapping_blocked",
            "repair source-free residue mapping or active-site locator evidence",
        )
    if _needs_acquisition(record):
        return (
            "acquisition_needed",
            "external_source_or_distance_screen_acquisition_needed",
            "run the named source, sequence, structure, and duplicate screens",
        )
    if _oos_or_reject_signal(record):
        return (
            "reject/OOS_preserve_signal",
            "hard_negative_or_out_of_scope_signal_preserved",
            "preserve as non-counting OOS or hard-negative evidence",
        )
    return (
        "review_only_evidence",
        "evidence_present_without_countable_promotion_authority",
        "preserve as review-only family evidence until explicit promotion gates pass",
    )


def _provenance_tier(record: dict[str, Any]) -> str:
    tiers = [str(value) for value in _all_values(record, "provenance_tiers")]
    if tiers:
        return ";".join(sorted(set(tiers)))
    if "external_hard_negative_next_sourcing" in record["source_rows"] or (
        "external_hard_negative_new_sourcing" in record["source_rows"]
    ):
        return "tier_B_external_sourced_review_only"
    if record["candidate_id"].startswith("m_csa:"):
        return "tier_A_local_mcsa_queue"
    if record["candidate_id"].startswith("uniprot:"):
        return "tier_B_external_uniprot_queue"
    return "mixed_local_review_queue"


def _proposed_label_tier(state: str) -> str:
    return {
        "countable_candidate": "countable_candidate_requires_separate_promotion_review",
        "review_only_evidence": "review_only_family_evidence",
        "reject/OOS_preserve_signal": "non_counting_oos_or_hard_negative_signal",
        "blocked_locator": "evidence_blocked_locator_repair",
        "blocked_coordinate": "evidence_blocked_coordinate_repair",
        "blocked_family_decision": "family_decision_blocked_non_counting",
        "acquisition_needed": "acquisition_needed_before_admission",
    }[state]


def _coordinate_evidence(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "coordinate_status": _first_value(
            record,
            "coordinate_materialization_status",
            "coordinate_status",
            "structure_statuses",
        ),
        "coordinate_path": _first_value(record, "coordinate_path"),
        "selected_structure": _first_value(
            record,
            "selected_structure_key",
            "selected_structure",
            "pdb_id",
            "selected_structure_id",
        ),
        "pdb_ids": sorted({str(value) for value in _all_values(record, "pdb_ids")}),
        "alphafold_ids": sorted(
            {str(value) for value in _all_values(record, "alphafold_ids")}
        ),
        "coordinate_provenance_available": bool(
            _first_value(record, "coordinate_path", "selected_structure_key", "pdb_id")
            or _all_values(record, "pdb_ids")
            or _all_values(record, "alphafold_ids")
        ),
    }


def _active_site_evidence(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "active_site_evidence_status": _first_value(
            record, "active_site_evidence_status", "local_mechanistic_evidence_status"
        ),
        "active_site_feature_count": _first_value(record, "active_site_feature_count"),
        "binding_site_feature_count": _first_value(record, "binding_site_feature_count"),
        "resolved_residue_count": _first_value(record, "resolved_residue_count"),
        "readiness_blockers": sorted(
            {str(value) for value in _all_values(record, "readiness_blockers")}
        ),
        "local_evidence_gap_classes": sorted(
            {str(value) for value in _all_values(record, "local_evidence_gap_classes")}
        ),
        "repair_bucket": _first_value(record, "repair_bucket"),
    }


def _cofactor_evidence(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "cofactor_evidence_level": _first_value(record, "cofactor_evidence_level"),
        "cofactor_families": sorted(
            {str(value) for value in _all_values(record, "cofactor_families")}
        ),
        "cofactor_or_ligand_states": _all_values(record, "cofactor_or_ligand_states"),
        "cofactor_comment_count": _first_value(record, "cofactor_comment_count"),
        "metal_or_cofactor_confounded": _cofactor_confounded(record),
    }


def _cofactor_confounded(record: dict[str, Any]) -> bool:
    text = _string_tokens(record)
    if _has_any(text, "cofactor", "flavin", "heme", "metal", "plp", "sam", "nad"):
        return True
    return bool(
        _all_values(record, "cofactor_families")
        or _all_values(record, "cofactor_or_ligand_states")
    )


def _fold_signal(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "top1_fingerprint_id": _first_value(record, "top1_fingerprint_id"),
        "top1_ontology_family": _first_value(record, "top1_ontology_family"),
        "top1_score": _first_value(record, "top1_score"),
        "top2_fingerprint_id": _first_value(record, "top2_fingerprint_id"),
        "top2_score": _first_value(record, "top2_score"),
        "tm_score_split_member": _first_value(record, "tm_score_split_member"),
        "nearest_neighbor_signal_source": (
            "local_top1_scores_or_coordinate_readiness"
            if _first_value(record, "top1_score", "tm_score_split_member") is not None
            else None
        ),
    }


def _geometry_status(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "geometry_status": _first_value(record, "geometry_status", "status"),
        "has_pairwise_geometry": _first_value(record, "has_pairwise_geometry"),
        "has_pocket_context": _first_value(record, "has_pocket_context"),
        "pocket_descriptor_available": _first_value(
            record, "pocket_descriptor_available"
        ),
        "reconstruction_status": _first_value(
            record,
            "alternate_structure_scan_outcome",
            "coordinate_materialization_status",
            "sourcing_status",
        ),
    }


def _flags(record: dict[str, Any], family_axis: str) -> dict[str, bool]:
    text = _string_tokens(record)
    return {
        "oos_or_hard_negative_signal": _oos_or_reject_signal(record),
        "novel_or_near_orphan_signal": family_axis
        == "near_orphan_or_unrepresented_mechanism_tail",
        "cofactor_confounded_signal": _cofactor_confounded(record),
        "source_free_feature_gap": _locator_blocked(record),
        "coordinate_gap": _coordinate_blocked(record),
        "external_candidate": str(record["candidate_id"]).startswith("uniprot:"),
        "heldout_sensitive": "heldout" in text,
    }


def _mechanical_unblock_requirements(
    record: dict[str, Any],
    state: str,
    allowed_next_action: str,
) -> dict[str, Any]:
    required_screens = sorted(
        {str(value) for value in _all_values(record, "next_required_screens")}
    )
    source_evidence_blockers = sorted(
        {str(value) for value in _all_values(record, "source_evidence_blockers")}
    )
    readiness_blockers = sorted(
        {str(value) for value in _all_values(record, "readiness_blockers")}
    )
    source_next_actions = sorted(
        {
            str(value)
            for value in (
                _all_values(record, "next_action")
                + _all_values(record, "recommended_next_action")
                + _all_values(record, "recommended_action")
            )
            if str(value)
        }
    )
    return {
        "state": state,
        "allowed_next_action": allowed_next_action,
        "next_required_screens": required_screens,
        "source_evidence_blockers": source_evidence_blockers,
        "readiness_blockers": readiness_blockers,
        "source_next_actions": source_next_actions,
        "machine_actionable_now": state
        in {"acquisition_needed", "blocked_locator", "blocked_coordinate"},
    }


def _rationale(record: dict[str, Any], family_axis: str, state: str) -> str:
    source_names = ", ".join(sorted(record["source_rows"]))
    top1 = _first_value(record, "top1_fingerprint_id")
    action = _first_value(record, "recommended_action", "next_action")
    role = _first_value(record, "panel_roles", "target_label_type", "current_label_type")
    parts = [
        f"Routed to {family_axis} from {source_names}.",
        f"Admission state is {state}.",
    ]
    if top1:
        parts.append(f"Nearest/current top1 family signal: {top1}.")
    if role:
        parts.append(f"Source review role: {role}.")
    panel_id = _first_value(record, "panel_id")
    if panel_id:
        parts.append(f"Architecture/source panel: {panel_id}.")
    if action:
        parts.append(f"Next local-source action: {action}.")
    return " ".join(parts)


def _merge_records(
    source_payloads: dict[str, Any],
    source_records: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    architecture_rows = {
        str(_row_id(row)): row
        for row in _rows_from_payload(
            source_payloads.get("architecture_default_decisions", {})
        )
        if _row_id(row)
    }
    for source_name, payload in source_payloads.items():
        if source_name == "architecture_default_decisions":
            continue
        if source_name not in CANDIDATE_SOURCE_NAMES:
            continue
        for row in _rows_from_payload(payload):
            candidate_id = _row_id(row)
            if not candidate_id:
                continue
            record = records.setdefault(
                candidate_id,
                {
                    "candidate_id": candidate_id,
                    "source_rows": defaultdict(list),
                    "source_hashes": {},
                },
            )
            record["source_rows"][source_name].append(row)
            record["source_hashes"][source_name] = source_records[source_name][
                "sha256"
            ]
    for source_name, payload in source_payloads.items():
        if source_name in CANDIDATE_SOURCE_NAMES:
            continue
        if source_name == "architecture_default_decisions":
            continue
        for row in _rows_from_payload(payload):
            candidate_id = _row_id(row)
            if not candidate_id or candidate_id not in records:
                continue
            record = records[candidate_id]
            record["source_rows"][source_name].append(row)
            record["source_hashes"][source_name] = source_records[source_name][
                "sha256"
            ]
    architecture_source = source_records.get("architecture_default_decisions")
    if architecture_source is not None:
        for entry_id in ARCHITECTURE_DEFAULT_ENTRY_IDS:
            architecture_row = architecture_rows.get(entry_id, {})
            if entry_id not in records and not architecture_row:
                continue
            record = records.setdefault(
                entry_id,
                {
                    "candidate_id": entry_id,
                    "source_rows": defaultdict(list),
                    "source_hashes": {},
                },
            )
            record["source_rows"][
                "architecture_default_decisions"
            ].append(
                {
                    "entry_id": entry_id,
                    "architecture_default": architecture_row.get(
                        "architecture_default"
                    ),
                    "architecture_confidence": architecture_row.get(
                        "architecture_confidence"
                    ),
                    "architecture_policy_name": architecture_row.get(
                        "architecture_policy_name"
                    ),
                    "decision": architecture_row.get("decision"),
                    "decision_context_sha256": architecture_row.get(
                        "decision_context_sha256"
                    ),
                    "panel_id": architecture_row.get("panel_id"),
                    "review_status": architecture_row.get("review_status"),
                    "row_context_sha256": architecture_row.get("row_context_sha256"),
                }
            )
            record["source_hashes"][
                "architecture_default_decisions"
            ] = architecture_source["sha256"]
    return records


def build_targeted_expansion_factory_batch(
    *,
    source_payloads: dict[str, Any],
    source_records: dict[str, dict[str, Any]],
    created_utc: str | None = None,
    min_target_candidates: int = 500,
    max_candidates: int = 1000,
) -> dict[str, Any]:
    records = _merge_records(source_payloads, source_records)
    candidate_rows = [
        _candidate_output_row(record) for record in records.values()
    ]
    candidate_rows = sorted(
        candidate_rows,
        key=lambda row: (
            row["family_axis"],
            row["admission_state"],
            row["candidate_id"],
        ),
    )
    if len(candidate_rows) > max_candidates:
        candidate_rows = _round_robin_limit(candidate_rows, max_candidates)

    state_counts = Counter(row["admission_state"] for row in candidate_rows)
    axis_counts = Counter(row["family_axis"] for row in candidate_rows)
    tier_counts = Counter(row["proposed_label_tier"] for row in candidate_rows)
    source_counts: Counter[str] = Counter()
    for row in candidate_rows:
        source_counts.update(row["sources"])

    audit = _state_assignment_audit(candidate_rows)
    target_status = (
        "target_volume_reached"
        if len(candidate_rows) >= min_target_candidates
        else "largest_defensible_local_batch_below_target"
    )
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created_utc or _utc_now_iso(),
        "status": target_status,
        "scope": (
            "first targeted expansion factory batch for diverse atlas growth; "
            "non-importing admission states only"
        ),
        "candidate_count": len(candidate_rows),
        "target_policy": {
            "min_target_candidates": min_target_candidates,
            "max_candidates": max_candidates,
            "human_review_required_only_for_countable_promotion": True,
            "default_non_counting_routes_do_not_require_vivek_row_review": True,
            "architecture_default_rows_reused_not_reasked": sorted(
                ARCHITECTURE_DEFAULT_ENTRY_IDS
            ),
        },
        "routing_policy": {
            "candidate_seed_sources": sorted(CANDIDATE_SOURCE_NAMES),
            "non_counting_carryover_seed_sources": [
                "architecture_default_decisions"
            ],
            "enrichment_sources": sorted(
                set(DEFAULT_SOURCE_PATHS)
                - CANDIDATE_SOURCE_NAMES
                - {"architecture_default_decisions"}
            ),
            "state_priority": [
                "architecture_default_reuse",
                "explicit_countable_gate_signal",
                "blocked_coordinate",
                "blocked_locator",
                "acquisition_needed",
                "reject_or_oos_preserve_signal",
                "review_only_evidence",
            ],
            "forbidden_scoring_features": [
                "mechanism_text",
                "EC_or_Rhea_ID",
                "source_ID",
                "target_name",
                "current_label",
            ],
            "provenance_only_fields_may_include_for_rationale": [
                "display_name",
                "source_review_role",
                "recommended_next_action",
                "top1_family_signal",
                "architecture_panel_id",
            ],
            "non_promotion_disposition_fields": [
                "current_label_type",
                "target_label_type",
                "label_type",
                "recommended_action",
            ],
            "routing_is_queue_organization_not_predictive_scoring": True,
        },
        "guardrails": {
            "label_registry_edited": False,
            "ontology_edited": False,
            "imports_or_promotions_performed": False,
            "train_test_splits_changed": False,
            "model_weights_fit_or_refit": False,
            "production_thresholds_changed": False,
            "heldout_mcsa_rows_used_for_training_or_tuning": False,
            "mechanism_text_or_ids_used_as_scoring_features": False,
            "source_ids_or_target_names_used_as_scoring_features": False,
        },
        "counts": {
            "admission_state_counts": {
                state: state_counts.get(state, 0) for state in ADMISSION_STATES
            },
            "family_axis_counts": dict(sorted(axis_counts.items())),
            "proposed_label_tier_counts": dict(sorted(tier_counts.items())),
            "source_counts": dict(sorted(source_counts.items())),
        },
        "evidence_coverage": _evidence_coverage(candidate_rows),
        "action_queues": _action_queues(candidate_rows),
        "state_assignment_audit": audit,
        "validation_checks": _validation_checks(
            candidate_rows=candidate_rows,
            source_records=source_records,
            min_target_candidates=min_target_candidates,
            max_candidates=max_candidates,
        ),
        "family_axes": _family_axis_summary(candidate_rows),
        "candidate_rows": candidate_rows,
        "acquisition_plan": _acquisition_plan(candidate_rows, min_target_candidates),
        "next_batch_recommendation": _next_batch_recommendation(candidate_rows),
        "source_artifacts": source_records,
    }


def _candidate_output_row(record: dict[str, Any]) -> dict[str, Any]:
    candidate_id = str(record["candidate_id"])
    state, basis, next_action = _admission_state(record)
    family_axis = _family_axis(record)
    sources = sorted(record["source_rows"])
    row = {
        "candidate_id": candidate_id,
        "accession_or_source_id": _first_value(record, "accession") or candidate_id,
        "display_name": _first_value(record, "entry_name", "display_name", "protein_name"),
        "family_axis": family_axis,
        "proposed_label_tier": _proposed_label_tier(state),
        "provenance_tier": _provenance_tier(record),
        "admission_state": state,
        "admission_route_basis": basis,
        "allowed_next_action": next_action,
        "sources": sources,
        "source_hashes": dict(sorted(record["source_hashes"].items())),
        "predicted_coordinate_or_provenance_availability": _coordinate_evidence(
            record
        ),
        "active_site_or_locator_evidence": _active_site_evidence(record),
        "cofactor_or_metal_evidence": _cofactor_evidence(record),
        "fold_tm_or_near_neighbor_signal": _fold_signal(record),
        "geometry_or_reconstruction_status": _geometry_status(record),
        "flags": _flags(record, family_axis),
        "mechanical_unblock_requirements": _mechanical_unblock_requirements(
            record,
            state,
            next_action,
        ),
        "rationale": _rationale(record, family_axis, state),
        "row_context_sha256": None,
    }
    row["row_context_sha256"] = _canonical_sha256(
        {key: value for key, value in row.items() if key != "row_context_sha256"}
    )
    return row


def _round_robin_limit(
    rows: list[dict[str, Any]],
    max_candidates: int,
) -> list[dict[str, Any]]:
    by_axis: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_axis[row["family_axis"]].append(row)
    selected: list[dict[str, Any]] = []
    while len(selected) < max_candidates and by_axis:
        for axis in sorted(list(by_axis)):
            if by_axis[axis]:
                selected.append(by_axis[axis].pop(0))
                if len(selected) >= max_candidates:
                    break
            if not by_axis[axis]:
                del by_axis[axis]
    return sorted(
        selected,
        key=lambda row: (
            row["family_axis"],
            row["admission_state"],
            row["candidate_id"],
        ),
    )


def _state_assignment_audit(candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    allowed = set(ADMISSION_STATES)
    seen: set[str] = set()
    violations: list[dict[str, Any]] = []
    for row in candidate_rows:
        row_violations: list[str] = []
        candidate_id = str(row.get("candidate_id") or "")
        state = row.get("admission_state")
        if not candidate_id:
            row_violations.append("missing_candidate_id")
        elif candidate_id in seen:
            row_violations.append("duplicate_candidate_id")
        else:
            seen.add(candidate_id)
        if state not in allowed:
            row_violations.append("unknown_or_missing_admission_state")
        if row_violations:
            violations.append(
                {
                    "candidate_id": candidate_id or None,
                    "admission_state": state,
                    "violations": row_violations,
                }
            )
    return {
        "passed": not violations,
        "rows_checked": len(candidate_rows),
        "rows_with_exactly_one_state": len(candidate_rows) - len(violations),
        "allowed_states": list(ADMISSION_STATES),
        "violations": violations,
    }


def _family_axis_summary(candidate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows_by_axis: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in candidate_rows:
        rows_by_axis[row["family_axis"]].append(row)
    summaries: list[dict[str, Any]] = []
    for axis, rows in sorted(rows_by_axis.items()):
        summaries.append(
            {
                "family_axis": axis,
                "candidate_count": len(rows),
                "admission_state_counts": dict(
                    sorted(Counter(row["admission_state"] for row in rows).items())
                ),
                "representative_candidate_ids": [
                    row["candidate_id"] for row in rows[:10]
                ],
            }
        )
    return summaries


def _acquisition_plan(
    candidate_rows: list[dict[str, Any]],
    min_target_candidates: int,
) -> dict[str, Any]:
    acquisition_rows = [
        row for row in candidate_rows if row["admission_state"] == "acquisition_needed"
    ]
    blocked_rows = [
        row
        for row in candidate_rows
        if row["admission_state"] in {"blocked_locator", "blocked_coordinate"}
    ]
    required_screen_counts: Counter[str] = Counter()
    for row in acquisition_rows:
        required_screen_counts.update(
            row["mechanical_unblock_requirements"].get("next_required_screens")
            or []
        )
    missing_to_floor = max(0, min_target_candidates - len(candidate_rows))
    return {
        "target_floor_gap": missing_to_floor,
        "acquisition_needed_rows": len(acquisition_rows),
        "acquisition_rows_with_explicit_screen_lists": sum(
            1
            for row in acquisition_rows
            if row["mechanical_unblock_requirements"].get("next_required_screens")
        ),
        "acquisition_rows_missing_explicit_screen_lists": sum(
            1
            for row in acquisition_rows
            if not row["mechanical_unblock_requirements"].get("next_required_screens")
        ),
        "required_screen_counts": dict(sorted(required_screen_counts.items())),
        "locator_or_coordinate_blocked_rows": len(blocked_rows),
        "first_unblock_actions": [
            "run current-reference sequence search and current-countable structural screen for external sourced rows",
            "materialize source-free active-site locators for blocked M-CSA rows",
            "promote no row until a separate label-factory gate and human countable-promotion review pass",
        ],
        "priority_candidate_ids": [
            row["candidate_id"] for row in (acquisition_rows + blocked_rows)[:25]
        ],
    }


def _validation_checks(
    *,
    candidate_rows: list[dict[str, Any]],
    source_records: dict[str, dict[str, Any]],
    min_target_candidates: int,
    max_candidates: int,
) -> dict[str, Any]:
    required_row_fields = {
        "candidate_id",
        "accession_or_source_id",
        "family_axis",
        "proposed_label_tier",
        "provenance_tier",
        "admission_state",
        "admission_route_basis",
        "allowed_next_action",
        "source_hashes",
        "predicted_coordinate_or_provenance_availability",
        "active_site_or_locator_evidence",
        "cofactor_or_metal_evidence",
        "fold_tm_or_near_neighbor_signal",
        "geometry_or_reconstruction_status",
        "flags",
        "mechanical_unblock_requirements",
        "rationale",
        "row_context_sha256",
    }
    required_field_violations: list[dict[str, Any]] = []
    source_hash_violations: list[dict[str, Any]] = []
    row_hash_violations: list[dict[str, Any]] = []
    forbidden_field_violations: list[dict[str, Any]] = []
    known_hashes = {
        name: str(record["sha256"]) for name, record in source_records.items()
    }
    for row in candidate_rows:
        missing = sorted(
            field for field in required_row_fields if not _has_value(row.get(field))
        )
        row_hash = str(row.get("row_context_sha256") or "")
        if len(row_hash) != 64:
            missing.append("valid_row_context_sha256")
        else:
            expected_hash = _canonical_sha256(
                {
                    key: value
                    for key, value in row.items()
                    if key != "row_context_sha256"
                }
            )
            if row_hash != expected_hash:
                row_hash_violations.append(
                    {
                        "candidate_id": row.get("candidate_id"),
                        "expected_row_context_sha256": expected_hash,
                        "actual_row_context_sha256": row_hash,
                    }
                )
        if missing:
            required_field_violations.append(
                {
                    "candidate_id": row.get("candidate_id"),
                    "missing_or_invalid_fields": missing,
                }
            )
        for source_name, source_hash in (row.get("source_hashes") or {}).items():
            if source_name not in known_hashes:
                source_hash_violations.append(
                    {
                        "candidate_id": row.get("candidate_id"),
                        "source": source_name,
                        "violation": "source_not_declared_top_level",
                    }
                )
            elif str(source_hash) != known_hashes[source_name]:
                source_hash_violations.append(
                    {
                        "candidate_id": row.get("candidate_id"),
                        "source": source_name,
                        "violation": "source_hash_mismatch",
                    }
                )
        forbidden_field_violations.extend(_forbidden_field_violations(row))
    candidate_count = len(candidate_rows)
    checks = {
        "candidate_volume_within_requested_bounds": (
            min_target_candidates <= candidate_count <= max_candidates
        ),
        "required_row_fields_present": not required_field_violations,
        "row_source_hashes_match_declared_sources": not source_hash_violations,
        "all_rows_have_source_hashes": all(
            bool(row.get("source_hashes")) for row in candidate_rows
        ),
        "all_rows_have_row_context_hashes": all(
            isinstance(row.get("row_context_sha256"), str)
            and len(str(row.get("row_context_sha256"))) == 64
            for row in candidate_rows
        ),
        "row_context_hashes_recompute": not row_hash_violations,
        "forbidden_raw_predictive_fields_absent": not forbidden_field_violations,
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "required_row_fields": sorted(required_row_fields),
        "required_field_violation_count": len(required_field_violations),
        "required_field_violations": required_field_violations[:25],
        "source_hash_violation_count": len(source_hash_violations),
        "source_hash_violations": source_hash_violations[:25],
        "row_hash_violation_count": len(row_hash_violations),
        "row_hash_violations": row_hash_violations[:25],
        "forbidden_field_violation_count": len(forbidden_field_violations),
        "forbidden_field_violations": forbidden_field_violations[:25],
    }


def _forbidden_field_violations(row: dict[str, Any]) -> list[dict[str, Any]]:
    forbidden_fields = {
        "mechanism_text",
        "mechanism_text_snippets",
        "ec_numbers",
        "rhea_ids",
        "source_ids",
        "target_names",
    }
    violations: list[dict[str, Any]] = []

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}/{key}"
                if key in forbidden_fields:
                    violations.append(
                        {
                            "candidate_id": row.get("candidate_id"),
                            "field_path": child_path,
                        }
                    )
                walk(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, f"{path}/{index}")

    walk(row, "")
    return violations


def _has_value(value: Any) -> bool:
    return value not in (None, "", [], {})


def _evidence_coverage(candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    def count_if(predicate: Any) -> int:
        return sum(1 for row in candidate_rows if predicate(row))

    return {
        "candidate_rows": len(candidate_rows),
        "coordinate_or_structure_provenance_available": count_if(
            lambda row: row[
                "predicted_coordinate_or_provenance_availability"
            ].get("coordinate_provenance_available")
        ),
        "active_site_or_locator_evidence_present": count_if(
            lambda row: any(
                _has_value(value)
                for value in row["active_site_or_locator_evidence"].values()
            )
        ),
        "cofactor_or_metal_evidence_present": count_if(
            lambda row: any(
                _has_value(value)
                for key, value in row["cofactor_or_metal_evidence"].items()
                if key != "metal_or_cofactor_confounded"
            )
        ),
        "fold_or_near_neighbor_signal_present": count_if(
            lambda row: any(
                _has_value(value)
                for value in row["fold_tm_or_near_neighbor_signal"].values()
            )
        ),
        "row_context_hash_present": count_if(
            lambda row: bool(row.get("row_context_sha256"))
        ),
        "source_hashes_present": count_if(lambda row: bool(row.get("source_hashes"))),
    }


def _action_queues(candidate_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    queue_map: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for row in candidate_rows:
        key = (
            row["admission_state"],
            row["family_axis"],
            row["allowed_next_action"],
        )
        queue_map[key].append(row["candidate_id"])
    queues: list[dict[str, Any]] = []
    for (state, axis, action), candidate_ids in sorted(
        queue_map.items(),
        key=lambda item: (-len(item[1]), item[0]),
    ):
        queues.append(
            {
                "admission_state": state,
                "family_axis": axis,
                "allowed_next_action": action,
                "candidate_count": len(candidate_ids),
                "representative_candidate_ids": candidate_ids[:20],
            }
        )
    return queues


def _next_batch_recommendation(candidate_rows: list[dict[str, Any]]) -> dict[str, Any]:
    axis_counts = Counter(row["family_axis"] for row in candidate_rows)
    state_counts = Counter(row["admission_state"] for row in candidate_rows)
    return {
        "recommended_next_batch": "external_sourced_rows_sequence_structure_distance_screens",
        "rationale": (
            "The first batch already clears the 500-row target locally. The "
            "largest actionable next lift is converting acquisition_needed "
            "external rows into review_only_evidence with source-free locator, "
            "sequence-distance, and structural duplicate screens."
        ),
        "highest_volume_axes": [
            {"family_axis": axis, "candidate_count": count}
            for axis, count in axis_counts.most_common(5)
        ],
        "state_pressure": dict(state_counts.most_common()),
    }


def write_targeted_expansion_factory_batch(
    *,
    out_path: Path,
    report_path: Path | None = None,
    source_paths: dict[str, Path] | None = None,
    created_utc: str | None = None,
    min_target_candidates: int = 500,
    max_candidates: int = 1000,
) -> dict[str, Any]:
    resolved_paths = {
        name: Path(path)
        for name, path in (source_paths or DEFAULT_SOURCE_PATHS).items()
    }
    source_records = {
        name: _source_record(path) for name, path in sorted(resolved_paths.items())
    }
    source_payloads = {
        name: _read_json(path) for name, path in sorted(resolved_paths.items())
    }
    artifact = build_targeted_expansion_factory_batch(
        source_payloads=source_payloads,
        source_records=source_records,
        created_utc=created_utc,
        min_target_candidates=min_target_candidates,
        max_candidates=max_candidates,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(render_targeted_expansion_report(artifact), encoding="utf-8")
    return artifact


def render_targeted_expansion_report(artifact: dict[str, Any]) -> str:
    counts = artifact["counts"]
    lines = [
        "# Targeted Expansion Factory Batch",
        "",
        f"Run: `{artifact['created_utc']}`",
        "",
        (
            "Non-importing targeted expansion artifact. No labels, registries, "
            "ontologies, splits, model weights, production thresholds, or imports "
            "were changed."
        ),
        "",
        "## Summary",
        "",
        f"- Status: `{artifact['status']}`",
        f"- Candidate rows: `{artifact['candidate_count']}`",
        f"- Exact-one-state audit: `{artifact['state_assignment_audit']['passed']}`",
        "",
        "## Admission Counts",
        "",
    ]
    for state, count in counts["admission_state_counts"].items():
        lines.append(f"- `{state}`: {count}")
    lines.extend(["", "## Family Axes", ""])
    lines.append("| Family axis | Candidates | Admission mix |")
    lines.append("| --- | ---: | --- |")
    for axis in artifact["family_axes"]:
        mix = ", ".join(
            f"{state}={count}"
            for state, count in axis["admission_state_counts"].items()
        )
        lines.append(
            f"| `{axis['family_axis']}` | {axis['candidate_count']} | {mix} |"
        )
    lines.extend(["", "## Source Counts", ""])
    for source, count in counts["source_counts"].items():
        lines.append(f"- `{source}`: {count}")
    coverage = artifact["evidence_coverage"]
    lines.extend(["", "## Evidence Coverage", ""])
    for key, value in coverage.items():
        lines.append(f"- `{key}`: {value}")
    validation = artifact["validation_checks"]
    lines.extend(["", "## Validation Checks", ""])
    lines.append(f"- Passed: `{validation['passed']}`")
    for key, value in validation["checks"].items():
        lines.append(f"- `{key}`: {value}")
    architecture_rows = [
        row
        for row in artifact["candidate_rows"]
        if row["candidate_id"]
        in artifact["target_policy"]["architecture_default_rows_reused_not_reasked"]
    ]
    architecture_state_counts = Counter(
        row["admission_state"] for row in architecture_rows
    )
    lines.extend(
        [
            "",
            "## Architecture Defaults Reused",
            "",
            (
                "- Expected default rows: "
                f"`{len(artifact['target_policy']['architecture_default_rows_reused_not_reasked'])}`"
            ),
            f"- Present default rows: `{len(architecture_rows)}`",
            "- Default row states:",
        ]
    )
    for state, count in sorted(architecture_state_counts.items()):
        lines.append(f"  - `{state}`: {count}")
    lines.append("- Default row IDs:")
    for row in sorted(architecture_rows, key=lambda item: item["candidate_id"]):
        lines.append(
            f"  - `{row['candidate_id']}`: `{row['admission_state']}` "
            f"via `{row['family_axis']}`"
        )
    acquisition = artifact["acquisition_plan"]
    lines.extend(
        [
            "",
            "## Blockers And Acquisition",
            "",
            f"- Target floor gap: `{acquisition['target_floor_gap']}`",
            f"- Acquisition-needed rows: `{acquisition['acquisition_needed_rows']}`",
            (
                "- Acquisition rows with explicit screen lists: "
                f"`{acquisition['acquisition_rows_with_explicit_screen_lists']}`"
            ),
            (
                "- Acquisition rows missing explicit screen lists: "
                f"`{acquisition['acquisition_rows_missing_explicit_screen_lists']}`"
            ),
            (
                "- Locator/coordinate blocked rows: "
                f"`{acquisition['locator_or_coordinate_blocked_rows']}`"
            ),
            "- Required screen counts:",
        ]
    )
    for screen, count in acquisition["required_screen_counts"].items():
        lines.append(f"  - `{screen}`: {count}")
    screen_ready_rows = [
        row
        for row in artifact["candidate_rows"]
        if row["admission_state"] == "acquisition_needed"
        and row["mechanical_unblock_requirements"].get("next_required_screens")
    ]
    lines.append("- Screen-ready acquisition rows:")
    for row in screen_ready_rows[:25]:
        lines.append(f"  - `{row['candidate_id']}` via `{row['family_axis']}`")
    lines.extend(
        [
            "- First unblock actions:",
        ]
    )
    for action in acquisition["first_unblock_actions"]:
        lines.append(f"  - {action}")
    lines.append("- Priority unblock candidate IDs:")
    for candidate_id in acquisition["priority_candidate_ids"]:
        lines.append(f"  - `{candidate_id}`")
    lines.extend(["", "## Largest Action Queues", ""])
    lines.append("| Admission state | Family axis | Rows | Next action |")
    lines.append("| --- | --- | ---: | --- |")
    for queue in artifact["action_queues"][:12]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{queue['admission_state']}`",
                    f"`{queue['family_axis']}`",
                    str(queue["candidate_count"]),
                    queue["allowed_next_action"],
                ]
            )
            + " |"
        )
    next_batch = artifact["next_batch_recommendation"]
    lines.extend(
        [
            "",
            "## Next Batch Recommendation",
            "",
            f"`{next_batch['recommended_next_batch']}`: {next_batch['rationale']}",
            "",
        ]
    )
    return "\n".join(lines)
