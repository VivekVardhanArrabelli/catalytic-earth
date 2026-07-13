"""Fail-closed accounting for intentionally preserved historical lineage drift."""

from __future__ import annotations

from typing import Any


def assert_lineage_edge_accounted_for(
    quarantine: dict[str, Any],
    *,
    artifact_path: str,
    edge_id: str,
    source_path: str,
    recorded_sha256: str | None,
    observed_sha256: str | None,
) -> str:
    """Return ``current`` or ``quarantined``; reject an unaccounted mismatch."""

    recorded = str(recorded_sha256 or "").removeprefix("sha256:") or None
    if observed_sha256 is not None and observed_sha256 == recorded:
        return "current"
    expected = {
        "artifact_path": artifact_path,
        "edge_id": edge_id,
        "source_path": source_path,
        "recorded_source_sha256": recorded,
        "observed_source_sha256": observed_sha256,
    }
    for row in quarantine.get("rows", []):
        if all(row.get(key) == value for key, value in expected.items()):
            if row.get("release_eligible") is not False:
                raise AssertionError(f"quarantined lineage edge became release eligible: {expected}")
            if row.get("disposition") != "historical_only_regenerate_do_not_rehash":
                raise AssertionError(f"invalid lineage quarantine disposition: {expected}")
            return "quarantined"
    raise AssertionError(f"unaccounted lineage mismatch: {expected}")
