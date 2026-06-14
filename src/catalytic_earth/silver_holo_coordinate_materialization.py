"""Materialize verified HOLO PDB coordinate files for silver-ready rows.

The silver geometry audit requires a local coordinate file, but the previous holo
confirmation step intentionally stored only a PDB id plus sha-pinned confirmation. This
module bridges that gap without changing tiers: it reuses already committed coordinate
artifacts when their sha matches the recorded holo confirmation, or fetches a bounded
number of RCSB mmCIF files and records the verified path as structure provenance.
Explicit PDB chain/residue mappings remain a separate blocker.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .bronze_silver_promotion_preview import (
    DEFAULT_EXPANSION_REGISTRY_PATH,
    build_bronze_silver_promotion_preview,
)
from .holo_structure_promotion import RCSB_CIF_URL, robust_rcsb_cif_fetcher
from .mechanism_representation_loop import DEFAULT_PROMOTION_COHESION
from .registry_io import load_json, write_registry_payload

ARTIFACT_ID = "v3_silver_holo_coordinate_materialization_current702"
SCHEMA_VERSION = "silver_holo_coordinate_materialization.v1"

FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
EXPANSION_REGISTRY_PATH = DEFAULT_EXPANSION_REGISTRY_PATH
DEFAULT_OUT = Path("artifacts/v3_silver_holo_coordinate_materialization_current702.json")
DEFAULT_REPORT = Path("work/silver_holo_coordinate_materialization_current702.md")
DEFAULT_COORDINATE_DIR = Path("artifacts/v3_silver_holo_coordinates_current702")

MATERIALIZED_STATUS = "holo_experimental_pdb_coordinate_materialized"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _structure_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return (row.get("evidence") or {}).get("structure_provenance") or {}


def _holo_confirmation(row: dict[str, Any]) -> dict[str, Any]:
    confirmation = _structure_provenance(row).get("holo_pdb_confirmation") or {}
    return confirmation if isinstance(confirmation, dict) else {}


def _coordinate_path(row: dict[str, Any]) -> Path | None:
    raw = _structure_provenance(row).get("coordinate_path")
    if not raw:
        return None
    path = Path(str(raw))
    return path if path.exists() else None


def _artifact_coordinate_candidates(pdb_id: str, *, artifacts_root: Path) -> list[Path]:
    if not pdb_id:
        return []
    return sorted(Path(artifacts_root).glob(f"**/pdb_{pdb_id.upper()}.cif"))


def _verified_existing_coordinate(
    row: dict[str, Any],
    *,
    artifacts_root: Path,
) -> tuple[Path | None, dict[str, Any] | None]:
    """Return a matching local coordinate path, plus mismatch details when present."""
    confirmation = _holo_confirmation(row)
    expected_sha = confirmation.get("coordinate_sha256")
    pdb_id = str(confirmation.get("pdb_id") or "").upper()
    candidates: list[Path] = []
    current = _coordinate_path(row)
    if current is not None:
        candidates.append(current)
    candidates.extend(
        path
        for path in _artifact_coordinate_candidates(pdb_id, artifacts_root=artifacts_root)
        if path not in candidates
    )

    mismatch: dict[str, Any] | None = None
    for path in candidates:
        digest = _sha256_path(path)
        if expected_sha is None or digest == expected_sha:
            return path, None
        if mismatch is None:
            mismatch = {
                "path": str(path),
                "coordinate_sha256": digest,
                "expected_holo_confirmation_sha256": expected_sha,
            }
    return None, mismatch


def _record_materialized_coordinate(
    row: dict[str, Any],
    *,
    path: Path,
    digest: str,
    byte_count: int,
    source: str,
    created_utc: str,
) -> None:
    structure = row.setdefault("evidence", {}).setdefault("structure_provenance", {})
    pdb_id = str((_holo_confirmation(row).get("pdb_id") or "")).upper()
    structure["coordinate_path"] = str(path)
    structure["coordinate_status"] = MATERIALIZED_STATUS
    structure["holo_coordinate_materialization"] = {
        "status": MATERIALIZED_STATUS,
        "source": source,
        "pdb_id": pdb_id,
        "coordinate_path": str(path),
        "coordinate_sha256": digest,
        "coordinate_bytes": byte_count,
        "retrieved_utc": created_utc,
        "model_url": RCSB_CIF_URL.format(pdb_id=pdb_id) if pdb_id else None,
        "coordinate_matches_holo_confirmation_sha256": True,
        "coordinate_regeneratable_from_pdb_id": True,
        "coordinate_is_review_only_not_predictive_feature": True,
    }


def build_silver_holo_coordinate_materialization(
    *,
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    coordinate_dir: Path = DEFAULT_COORDINATE_DIR,
    artifacts_root: Path = Path("artifacts"),
    cif_fetcher: Callable[[str], str | None] | None = None,
    fetch_limit: int = 0,
) -> dict[str, Any]:
    """Build a preview/apply payload for verified holo coordinate materialization."""
    created = created_utc or _utc_now_iso()
    fetcher = cif_fetcher or robust_rcsb_cif_fetcher
    promotion = build_bronze_silver_promotion_preview(
        expansion_payload,
        cohesion_threshold=cohesion_threshold,
    )
    silver_ready_entries = {
        row["entry_id"]
        for row in promotion.get("silver_ready_preview", [])
        if isinstance(row, dict) and row.get("entry_id")
    }

    out_rows: list[dict[str, Any]] = []
    materialization_rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    by_fingerprint: Counter[str] = Counter()
    fetches = 0
    coordinate_dir = Path(coordinate_dir)

    for row in expansion_payload:
        new_row = json.loads(json.dumps(row))
        entry_id = str(new_row.get("entry_id") or "")
        if entry_id not in silver_ready_entries:
            out_rows.append(new_row)
            continue

        confirmation = _holo_confirmation(new_row)
        pdb_id = str(confirmation.get("pdb_id") or "").upper()
        expected_sha = confirmation.get("coordinate_sha256")
        row_record: dict[str, Any] = {
            "entry_id": entry_id,
            "fingerprint_id": new_row.get("fingerprint_id"),
            "pdb_id": pdb_id,
            "expected_holo_confirmation_sha256": expected_sha,
            "source": None,
            "coordinate_path": None,
            "coordinate_sha256": None,
            "decision": "blocked_no_verified_coordinate",
            "registry_updated": False,
            "tier_changed": False,
        }

        if confirmation.get("status") != "holo_experimental_coordinate_confirmed" or not pdb_id:
            counts["missing_holo_confirmation"] += 1
            row_record["decision"] = "blocked_missing_holo_confirmation"
            materialization_rows.append(row_record)
            out_rows.append(new_row)
            continue

        existing, mismatch = _verified_existing_coordinate(
            new_row,
            artifacts_root=Path(artifacts_root),
        )
        if existing is not None:
            digest = _sha256_path(existing)
            if _coordinate_path(new_row) == existing:
                counts["already_materialized_verified"] += 1
                decision = "already_materialized_verified"
                source = "existing_recorded_coordinate_path"
            else:
                counts["reused_existing_artifact_coordinate"] += 1
                decision = "materialized_from_existing_artifact"
                source = "existing_artifact_coordinate"
                _record_materialized_coordinate(
                    new_row,
                    path=existing,
                    digest=digest,
                    byte_count=existing.stat().st_size,
                    source=source,
                    created_utc=created,
                )
                row_record["registry_updated"] = True
                by_fingerprint[str(new_row.get("fingerprint_id") or "__missing__")] += 1
            row_record.update(
                {
                    "decision": decision,
                    "source": source,
                    "coordinate_path": str(existing),
                    "coordinate_sha256": digest,
                }
            )
            materialization_rows.append(row_record)
            out_rows.append(new_row)
            continue

        if fetches >= fetch_limit:
            counts["deferred_over_fetch_limit"] += 1
            row_record["decision"] = "deferred_over_fetch_limit"
            if mismatch is not None:
                row_record["mismatch"] = mismatch
                counts["existing_local_coordinate_sha_mismatch"] += 1
            materialization_rows.append(row_record)
            out_rows.append(new_row)
            continue

        cif_text = fetcher(pdb_id)
        fetches += 1
        if cif_text is None:
            counts["pdb_fetch_unavailable"] += 1
            row_record["decision"] = "blocked_pdb_fetch_unavailable"
            materialization_rows.append(row_record)
            out_rows.append(new_row)
            continue

        payload = cif_text.encode("utf-8")
        digest = _sha256_bytes(payload)
        if expected_sha is not None and digest != expected_sha:
            counts["fetched_coordinate_sha_mismatch"] += 1
            row_record.update(
                {
                    "decision": "blocked_fetched_coordinate_sha_mismatch",
                    "coordinate_sha256": digest,
                }
            )
            if mismatch is not None:
                row_record["mismatch"] = mismatch
                counts["existing_local_coordinate_sha_mismatch"] += 1
            materialization_rows.append(row_record)
            out_rows.append(new_row)
            continue

        coordinate_dir.mkdir(parents=True, exist_ok=True)
        path = coordinate_dir / f"pdb_{pdb_id}.cif"
        path.write_bytes(payload)
        counts["fetched_and_materialized_coordinate"] += 1
        _record_materialized_coordinate(
            new_row,
            path=path,
            digest=digest,
            byte_count=len(payload),
            source="rcsb_mmcif_refetch",
            created_utc=created,
        )
        by_fingerprint[str(new_row.get("fingerprint_id") or "__missing__")] += 1
        row_record.update(
            {
                "decision": "materialized_from_rcsb_refetch",
                "source": "rcsb_mmcif_refetch",
                "coordinate_path": str(path),
                "coordinate_sha256": digest,
                "registry_updated": True,
            }
        )
        materialization_rows.append(row_record)
        out_rows.append(new_row)

    registry_updates = sum(1 for row in materialization_rows if row["registry_updated"])
    verified_after = sum(
        1
        for row in out_rows
        if row.get("entry_id") in silver_ready_entries
        and _coordinate_path(row) is not None
        and (
            _holo_confirmation(row).get("coordinate_sha256") is None
            or _sha256_path(_coordinate_path(row))  # type: ignore[arg-type]
            == _holo_confirmation(row).get("coordinate_sha256")
        )
    )
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_write",
        "what": (
            "materialize verified local holo experimental-PDB coordinate files for "
            "silver-ready rows; this does not run geometry confirmation and does not "
            "change tiers"
        ),
        "policy": {
            "silver_ready_source": "bronze_silver_promotion_preview",
            "cohesion_threshold": cohesion_threshold,
            "requires_recorded_holo_pdb_confirmation": True,
            "requires_coordinate_sha256_match_to_holo_confirmation": True,
            "explicit_pdb_chain_residue_mapping_still_required": True,
            "coordinate_path_is_review_only_not_predictive_feature": True,
        },
        "guardrails": {
            "frozen_current702_benchmark_preserved": True,
            "writes_expansion_registry_only": True,
            "row_count_unchanged": len(out_rows) == len(expansion_payload),
            "tier_changed": False,
            "geometry_confirmation_run_or_faked": False,
            "predictive_evidence_changed": False,
            "annotation_only_silver_promotion": False,
        },
        "counts": {
            "expansion_labels": len(expansion_payload),
            "silver_ready_input_rows": len(silver_ready_entries),
            "already_materialized_verified": counts["already_materialized_verified"],
            "reused_existing_artifact_coordinate": counts[
                "reused_existing_artifact_coordinate"
            ],
            "fetched_and_materialized_coordinate": counts[
                "fetched_and_materialized_coordinate"
            ],
            "registry_coordinate_updates": registry_updates,
            "verified_local_coordinates_after": verified_after,
            "deferred_over_fetch_limit": counts["deferred_over_fetch_limit"],
            "existing_local_coordinate_sha_mismatch": counts[
                "existing_local_coordinate_sha_mismatch"
            ],
            "fetched_coordinate_sha_mismatch": counts["fetched_coordinate_sha_mismatch"],
            "pdb_fetch_unavailable": counts["pdb_fetch_unavailable"],
            "missing_holo_confirmation": counts["missing_holo_confirmation"],
            "rows_fetched_this_run": fetches,
        },
        "materialized_by_fingerprint": dict(sorted(by_fingerprint.items())),
        "next_action": (
            "Apply the verified coordinate-path updates, rerun the silver geometry audit, "
            "then build explicit PDB chain/residue mappings before any geometry-confirmation "
            "or silver tier apply."
        ),
        "rows": materialization_rows,
        "materialized_registry": out_rows,
    }


def summarize_materialization(audit: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in audit.items() if key != "materialized_registry"}


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Silver Holo Coordinate Materialization",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Materializes verified local experimental-PDB coordinates for the silver-ready",
        "queue. This is a provenance-only step: no geometry scoring is run and no tier is",
        "changed.",
        "",
        "## Result",
        "",
        f"- Silver-ready input rows: {c['silver_ready_input_rows']}.",
        f"- Already verified local coordinates: {c['already_materialized_verified']}.",
        f"- Reused existing artifact coordinates: {c['reused_existing_artifact_coordinate']}.",
        f"- Fetched and materialized coordinates: {c['fetched_and_materialized_coordinate']}.",
        f"- Registry coordinate updates staged: {c['registry_coordinate_updates']}.",
        f"- Verified local coordinates after: {c['verified_local_coordinates_after']}.",
        f"- Deferred over fetch limit: {c['deferred_over_fetch_limit']}.",
        f"- Existing local sha mismatches: {c['existing_local_coordinate_sha_mismatch']}.",
        f"- Fetched sha mismatches: {c['fetched_coordinate_sha_mismatch']}.",
        "",
        "## Guardrails",
        "",
        f"- Row count unchanged: {audit['guardrails']['row_count_unchanged']}.",
        f"- Tier changed: {audit['guardrails']['tier_changed']}.",
        f"- Geometry confirmation run or faked: "
        f"{audit['guardrails']['geometry_confirmation_run_or_faked']}.",
        "- Coordinates are review-only provenance and are not predictive features.",
        "",
        "## Next Action",
        "",
        f"- {audit['next_action']}",
        "",
    ]
    return "\n".join(lines)


def write_silver_holo_coordinate_materialization(
    *,
    out_path: Path = DEFAULT_OUT,
    report_path: Path | None = DEFAULT_REPORT,
    expansion_registry_path: Path = EXPANSION_REGISTRY_PATH,
    frozen_benchmark_path: Path = FROZEN_BENCHMARK_PATH,
    coordinate_dir: Path = DEFAULT_COORDINATE_DIR,
    artifacts_root: Path = Path("artifacts"),
    cif_fetcher: Callable[[str], str | None] | None = None,
    apply: bool = False,
    fetch_limit: int = 0,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    frozen_path = Path(frozen_benchmark_path)
    if expansion_path.resolve() == frozen_path.resolve():
        raise ValueError(
            "refusing to materialize coordinates into the frozen current702 benchmark"
        )

    frozen_sha_before = (
        hashlib.sha256(frozen_path.read_bytes()).hexdigest() if frozen_path.exists() else None
    )
    expansion_payload = load_json(expansion_path) if expansion_path.exists() else []
    audit = build_silver_holo_coordinate_materialization(
        expansion_payload=expansion_payload,
        coordinate_dir=coordinate_dir,
        artifacts_root=artifacts_root,
        cif_fetcher=cif_fetcher,
        fetch_limit=fetch_limit,
        cohesion_threshold=cohesion_threshold,
    )

    summary = summarize_materialization(audit)
    summary["frozen_sha256_before"] = frozen_sha_before
    summary["expansion_registry_written"] = False
    summary["frozen_benchmark_registry_written"] = False
    if apply:
        materialized = audit["materialized_registry"]
        if len(materialized) != len(expansion_payload):
            raise ValueError(
                "row-count guard tripped: materialized registry length "
                f"{len(materialized)} != input {len(expansion_payload)}"
            )
        from .labels import MechanismLabel

        for label in materialized:
            MechanismLabel.from_dict(label)
        write_result = write_registry_payload(expansion_path, materialized)
        summary["expansion_registry_written"] = True
        summary["expansion_registry_path"] = str(expansion_path)
        summary["expansion_registry_storage"] = write_result

    summary["frozen_sha256_after"] = (
        hashlib.sha256(frozen_path.read_bytes()).hexdigest() if frozen_path.exists() else None
    )
    summary["frozen_benchmark_byte_unchanged"] = (
        summary["frozen_sha256_before"] == summary["frozen_sha256_after"]
    )

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(summary), encoding="utf-8")
    return summary
