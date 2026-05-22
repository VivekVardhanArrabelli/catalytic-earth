from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def validate_review_only_zero_import_artifacts(paths: list[Path]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if not isinstance(payload, dict):
            raise ValueError(f"{path}: artifact root must be a JSON object")
        metadata = payload.get("metadata", {})
        decision = payload.get("decision", {})
        if not isinstance(metadata, dict):
            metadata = {}
        if not isinstance(decision, dict):
            decision = {}
        import_ready_count = _first_int(
            metadata.get("import_ready_candidate_count"),
            decision.get("import_ready_candidate_count"),
        )
        countable_count = _first_int(
            metadata.get("countable_label_candidate_count"),
            decision.get("countable_label_candidate_count"),
        )
        blockers = _row_blockers(
            metadata=metadata,
            import_ready_count=import_ready_count,
            countable_count=countable_count,
        )
        rows.append(
            {
                "path": str(path),
                "artifact_id": metadata.get("artifact_id"),
                "method": metadata.get("method"),
                "review_only": metadata.get("review_only"),
                "ready_for_label_import": metadata.get("ready_for_label_import"),
                "import_ready_candidate_count": import_ready_count,
                "countable_label_candidate_count": countable_count,
                "new_external_rows_frozen": metadata.get("new_external_rows_frozen"),
                "curated_label_registry_edited": metadata.get(
                    "curated_label_registry_edited"
                ),
                "fingerprint_registry_edited": metadata.get(
                    "fingerprint_registry_edited"
                ),
                "artifact_upload_or_removal_performed": metadata.get(
                    "artifact_upload_or_removal_performed"
                ),
                "artifact_migration_files_edited": metadata.get(
                    "artifact_migration_files_edited"
                ),
                "removal_allowed_set_true": metadata.get("removal_allowed_set_true"),
                "valid": not blockers,
                "blockers": blockers,
            }
        )
    blocker_rows = [row for row in rows if not row["valid"]]
    return {
        "metadata": {
            "method": "review_only_zero_import_artifact_gate",
            "review_only": True,
            "ready_for_label_import": False,
            "import_ready_candidate_count": 0,
            "countable_label_candidate_count": 0,
            "new_external_rows_frozen": 0,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "artifact_migration_files_edited": False,
            "artifact_upload_or_removal_performed": False,
            "removal_allowed_set_true": False,
            "artifact_count": len(rows),
            "valid_artifact_count": len(rows) - len(blocker_rows),
            "blocker_count": len(blocker_rows),
            "valid": not blocker_rows,
        },
        "rows": rows,
    }


def _first_int(*values: Any) -> int | None:
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
    return None


def _row_blockers(
    *,
    metadata: dict[str, Any],
    import_ready_count: int | None,
    countable_count: int | None,
) -> list[str]:
    blockers: list[str] = []
    if metadata.get("review_only") is not True:
        blockers.append("review_only_not_true")
    if metadata.get("ready_for_label_import") is not False:
        blockers.append("ready_for_label_import_not_false")
    if import_ready_count != 0:
        blockers.append("import_ready_candidate_count_not_zero")
    if countable_count != 0:
        blockers.append("countable_label_candidate_count_not_zero")
    if metadata.get("curated_label_registry_edited") is not False:
        blockers.append("curated_label_registry_edited_not_false")
    if metadata.get("fingerprint_registry_edited") is not False:
        blockers.append("fingerprint_registry_edited_not_false")
    if metadata.get("artifact_upload_or_removal_performed") is not False:
        blockers.append("artifact_upload_or_removal_performed_not_false")
    if metadata.get("artifact_migration_files_edited") is True:
        blockers.append("artifact_migration_files_edited_true")
    if metadata.get("removal_allowed_set_true") is True:
        blockers.append("removal_allowed_set_true")
    frozen_rows = metadata.get("new_external_rows_frozen")
    if isinstance(frozen_rows, int) and not isinstance(frozen_rows, bool):
        if frozen_rows != 0:
            blockers.append("new_external_rows_frozen_not_zero")
    return blockers
