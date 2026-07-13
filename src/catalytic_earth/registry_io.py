"""Registry JSON helpers, including transparent sharded registry support."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .truth_guard import assert_expansion_write_allowed

SHARDED_REGISTRY_SCHEMA = "catalytic_earth.sharded_registry.v1"
DEFAULT_SHARD_THRESHOLD_BYTES = 45_000_000
DEFAULT_TARGET_SHARD_BYTES = 18_000_000


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _json_row(row: dict[str, Any]) -> str:
    return json.dumps(row, separators=(",", ":"), sort_keys=True)


def dump_registry(registry: list[dict[str, Any]]) -> str:
    """Serialize a registry in the canonical one-label-per-line compact format."""
    body = ",\n".join("  " + _json_row(label) for label in registry)
    return "[\n" + body + "\n]\n"


def is_sharded_registry_manifest(payload: Any) -> bool:
    return (
        isinstance(payload, dict)
        and payload.get("schema_version") == SHARDED_REGISTRY_SCHEMA
        and isinstance(payload.get("shards"), list)
    )


def _shard_dir_for(path: Path) -> Path:
    return path.with_name(f"{path.stem}.shards")


def _resolve_shard_path(manifest_path: Path, raw_path: str) -> Path:
    shard_path = (manifest_path.parent / raw_path).resolve()
    root = manifest_path.parent.resolve()
    if root != shard_path and root not in shard_path.parents:
        raise ValueError(f"registry shard escapes manifest directory: {raw_path}")
    return shard_path


def _load_sharded_registry(manifest_path: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for shard in manifest.get("shards", []):
        if not isinstance(shard, dict):
            raise ValueError(f"{manifest_path} contains a malformed shard entry")
        raw_path = shard.get("path")
        if not isinstance(raw_path, str) or not raw_path:
            raise ValueError(f"{manifest_path} contains a shard without a path")
        shard_path = _resolve_shard_path(manifest_path, raw_path)
        text = shard_path.read_text(encoding="utf-8")
        expected_sha = shard.get("sha256")
        actual_sha = _sha256_text(text)
        if expected_sha and actual_sha != expected_sha:
            raise ValueError(
                f"{shard_path} sha256 mismatch: expected {expected_sha}, got {actual_sha}"
            )
        payload = json.loads(text)
        if not isinstance(payload, list):
            raise ValueError(f"{shard_path} must contain a JSON list")
        expected_rows = shard.get("row_count")
        if expected_rows is not None and len(payload) != expected_rows:
            raise ValueError(
                f"{shard_path} row count mismatch: expected {expected_rows}, got {len(payload)}"
            )
        rows.extend(payload)
    expected_total = manifest.get("row_count")
    if expected_total is not None and len(rows) != expected_total:
        raise ValueError(
            f"{manifest_path} sharded registry row count mismatch: "
            f"expected {expected_total}, got {len(rows)}"
        )
    return rows


def load_json(path: Path) -> Any:
    """Load ordinary JSON, unwrapping a sharded registry manifest when encountered."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if is_sharded_registry_manifest(payload):
        return _load_sharded_registry(path, payload)
    return payload


def load_registry(path: Path) -> list[dict[str, Any]]:
    payload = load_json(path)
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a registry list or sharded registry manifest")
    return payload


def _split_registry(
    registry: list[dict[str, Any]],
    *,
    target_shard_bytes: int,
) -> list[list[dict[str, Any]]]:
    shards: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_bytes = len("[\n]\n".encode("utf-8"))
    for row in registry:
        row_bytes = len(("  " + _json_row(row)).encode("utf-8"))
        separator_bytes = len(",\n".encode("utf-8")) if current else 0
        if current and current_bytes + separator_bytes + row_bytes > target_shard_bytes:
            shards.append(current)
            current = []
            current_bytes = len("[\n]\n".encode("utf-8"))
            separator_bytes = 0
        current.append(row)
        current_bytes += separator_bytes + row_bytes
    if current or not shards:
        shards.append(current)
    return shards


def write_registry_payload(
    path: Path,
    registry: list[dict[str, Any]],
    *,
    shard_threshold_bytes: int = DEFAULT_SHARD_THRESHOLD_BYTES,
    target_shard_bytes: int = DEFAULT_TARGET_SHARD_BYTES,
) -> dict[str, Any]:
    """Write a registry as a list or, when large, as a manifest plus shard files."""
    path = Path(path)
    assert_expansion_write_allowed(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = dump_registry(registry)
    serialized_bytes = len(serialized.encode("utf-8"))
    shard_dir = _shard_dir_for(path)

    if serialized_bytes <= shard_threshold_bytes:
        path.write_text(serialized, encoding="utf-8")
        if shard_dir.exists():
            for stale in shard_dir.glob("part-*.json"):
                stale.unlink()
            try:
                shard_dir.rmdir()
            except OSError:
                pass
        return {
            "format": "single_json_list",
            "path": str(path),
            "row_count": len(registry),
            "bytes": serialized_bytes,
            "sha256": _sha256_text(serialized),
            "shard_count": 0,
        }

    shard_dir.mkdir(parents=True, exist_ok=True)
    shard_payloads = _split_registry(registry, target_shard_bytes=target_shard_bytes)
    shard_entries: list[dict[str, Any]] = []
    active_names: set[str] = set()
    for index, shard_rows in enumerate(shard_payloads):
        shard_name = f"part-{index:05d}.json"
        active_names.add(shard_name)
        shard_path = shard_dir / shard_name
        shard_text = dump_registry(shard_rows)
        shard_path.write_text(shard_text, encoding="utf-8")
        shard_entries.append(
            {
                "path": str(shard_path.relative_to(path.parent)),
                "row_count": len(shard_rows),
                "bytes": len(shard_text.encode("utf-8")),
                "sha256": _sha256_text(shard_text),
            }
        )
    for stale in shard_dir.glob("part-*.json"):
        if stale.name not in active_names:
            stale.unlink()

    manifest = {
        "schema_version": SHARDED_REGISTRY_SCHEMA,
        "generated_utc": _utc_now_iso(),
        "row_count": len(registry),
        "canonical_order": "preserved input order across shards",
        "full_registry_canonical_sha256": _sha256_text(serialized),
        "full_registry_canonical_bytes": serialized_bytes,
        "shard_count": len(shard_entries),
        "shards": shard_entries,
    }
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "format": "sharded_registry_manifest",
        "path": str(path),
        "row_count": len(registry),
        "bytes": len(path.read_text(encoding="utf-8").encode("utf-8")),
        "full_registry_canonical_bytes": serialized_bytes,
        "full_registry_canonical_sha256": manifest["full_registry_canonical_sha256"],
        "shard_count": len(shard_entries),
        "max_shard_bytes": max(entry["bytes"] for entry in shard_entries) if shard_entries else 0,
    }
