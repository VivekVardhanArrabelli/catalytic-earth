"""Validation for the bounded, redistributable Atlas-3 source snapshot set."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .atlas_selection import validate_atlas3_selection
from .canonical_hash import canonical_file_sha256


SCHEMA_VERSION = "catalytic-earth.atlas3-source-manifest.v1"
BUNDLED_SOURCES = {"M-CSA", "PDB", "Rhea", "UniProtKB"}
REFERENCE_ONLY_SOURCES = {"DOI", "PMCID"}
EXPECTED_LICENSES = {
    "DOI": "article-specific terms; reference-only handle",
    "M-CSA": "CC BY 4.0",
    "PDB": "CC0 1.0 archive file",
    "PMCID": "article-specific terms; reference-only handle",
    "Rhea": "CC BY 4.0",
    "UniProtKB": "CC BY 4.0",
}
MANIFEST_FIELDS = {
    "applicability",
    "attribution",
    "change_notice",
    "evidence_role",
    "license",
    "media_type",
    "record_id",
    "retrieval_status",
    "retrieval_urls",
    "retrieved_at",
    "snapshot_bytes",
    "snapshot_path",
    "snapshot_sha256",
    "source_id",
    "uri",
}


def _exact_keys(value: dict[str, Any], expected: set[str], context: str) -> None:
    actual = set(value)
    if actual != expected:
        raise ValueError(
            f"{context} keys differ; missing={sorted(expected - actual)}, "
            f"extra={sorted(actual - expected)}"
        )


def _canonical_manifest_set_digest(records: list[dict[str, Any]]) -> str:
    identity = [
        {
            "record_id": record["record_id"],
            "retrieval_status": record["retrieval_status"],
            "snapshot_sha256": record["snapshot_sha256"],
            "source_id": record["source_id"],
        }
        for record in sorted(records, key=lambda item: (item["source_id"], item["record_id"]))
    ]
    raw = json.dumps(identity, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _selection_handles(selection: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    handles: dict[tuple[str, str], dict[str, Any]] = {}
    for case in selection["cases"]:
        for handle in case["source_handles"]:
            key = handle["source_id"], handle["record_id"]
            if key in handles:
                raise ValueError(f"selection repeats a source handle: {key}")
            handles[key] = handle
    return handles


def validate_atlas3_source_manifest(
    value: Any,
    *,
    repo_root: Path,
    selection: dict[str, Any],
) -> dict[str, int | str]:
    """Validate source identities, rights fields, local hashes, and selection binding."""
    if not isinstance(value, dict):
        raise ValueError("Atlas-3 source manifest must be an object")
    _exact_keys(
        value,
        {
            "records",
            "retrieved_at",
            "rights_matrix_path",
            "schema_version",
            "selection_sha256",
            "snapshot_set_sha256",
        },
        "source_manifest",
    )
    if value["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"unsupported Atlas-3 source manifest: {value['schema_version']!r}")
    selection_summary = validate_atlas3_selection(selection)
    if value["selection_sha256"] != selection_summary["selection_sha256"]:
        raise ValueError("source manifest is not bound to the frozen Atlas-3 selection")
    if value["rights_matrix_path"] != "docs/SOURCE_DATA_RIGHTS.md":
        raise ValueError("source manifest must bind the checked source-rights matrix")
    if not isinstance(value["retrieved_at"], str) or not value["retrieved_at"].endswith("Z"):
        raise ValueError("source manifest retrieved_at must be UTC")
    records = value["records"]
    if not isinstance(records, list) or len(records) != 18:
        raise ValueError("Atlas-3 source manifest must contain all 18 frozen handles")
    handles = _selection_handles(selection)
    seen: set[tuple[str, str]] = set()
    bundled = 0
    reference_only = 0
    total_bytes = 0
    for index, record in enumerate(records):
        context = f"source_manifest.records[{index}]"
        if not isinstance(record, dict):
            raise ValueError(f"{context} must be an object")
        _exact_keys(record, MANIFEST_FIELDS, context)
        key = record["source_id"], record["record_id"]
        if key in seen:
            raise ValueError(f"source manifest repeats {key}")
        seen.add(key)
        if key not in handles:
            raise ValueError(f"source manifest contains an unselected handle: {key}")
        handle = handles[key]
        for field in ("applicability", "evidence_role", "uri"):
            if record[field] != handle[field]:
                raise ValueError(f"{context}.{field} differs from the frozen selection")
        if record["retrieved_at"] != value["retrieved_at"]:
            raise ValueError(f"{context}.retrieved_at differs from the manifest timestamp")
        if record["license"] != EXPECTED_LICENSES[record["source_id"]]:
            raise ValueError(f"{context}.license differs from the checked rights policy")
        for field in ("attribution", "change_notice", "media_type"):
            if not isinstance(record[field], str) or not record[field].strip():
                raise ValueError(f"{context}.{field} must be a non-empty string")
        urls = record["retrieval_urls"]
        if (
            not isinstance(urls, list)
            or not urls
            or any(not isinstance(url, str) or not url.startswith("https://") for url in urls)
        ):
            raise ValueError(f"{context}.retrieval_urls must contain HTTPS URLs")
        if record["source_id"] in BUNDLED_SOURCES:
            if record["retrieval_status"] != "bundled_snapshot":
                raise ValueError(f"{context} must be a bundled snapshot")
            relative = record["snapshot_path"]
            if not isinstance(relative, str) or not relative.startswith(
                "data/atlas/atlas3/sources/"
            ):
                raise ValueError(f"{context}.snapshot_path escapes the Atlas-3 namespace")
            path = (repo_root / relative).resolve()
            source_root = (repo_root / "data/atlas/atlas3/sources").resolve()
            if source_root not in path.parents or not path.is_file():
                raise ValueError(f"{context}.snapshot_path is missing or outside source root")
            size = path.stat().st_size
            if record["snapshot_bytes"] != size or size <= 0:
                raise ValueError(f"{context}.snapshot_bytes differs from the local file")
            digest = canonical_file_sha256(path)
            if record["snapshot_sha256"] != digest:
                raise ValueError(f"{context}.snapshot_sha256 differs from the local file")
            bundled += 1
            total_bytes += size
        elif record["source_id"] in REFERENCE_ONLY_SOURCES:
            if record["retrieval_status"] != "reference_only_verified_handle":
                raise ValueError(f"{context} must remain a reference-only literature handle")
            if (
                record["snapshot_path"] is not None
                or record["snapshot_sha256"] is not None
                or record["snapshot_bytes"] != 0
            ):
                raise ValueError(f"{context} cannot bundle reference-only article content")
            reference_only += 1
        else:
            raise ValueError(f"{context}.source_id is unsupported")
    if seen != set(handles):
        raise ValueError("source manifest does not exactly cover the frozen source handles")
    if bundled != 13 or reference_only != 5:
        raise ValueError("Atlas-3 source snapshot/reference-only counts differ")
    digest = _canonical_manifest_set_digest(records)
    if value["snapshot_set_sha256"] != digest:
        raise ValueError("Atlas-3 source snapshot-set digest differs")
    return {
        "schema_version": SCHEMA_VERSION,
        "handles": len(records),
        "bundled_snapshots": bundled,
        "reference_only_handles": reference_only,
        "snapshot_bytes": total_bytes,
        "snapshot_set_sha256": digest,
    }


def load_atlas3_source_manifest(
    path: Path, *, repo_root: Path, selection: dict[str, Any]
) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    validate_atlas3_source_manifest(value, repo_root=repo_root, selection=selection)
    return value
