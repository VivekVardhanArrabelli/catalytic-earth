"""Backfill explicit PDB residue mappings for silver-ready rows with local mmCIFs."""

from __future__ import annotations

import hashlib
import json
import shlex
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .bronze_silver_promotion_preview import (
    DEFAULT_EXPANSION_REGISTRY_PATH,
    build_bronze_silver_promotion_preview,
)
from .mechanism_representation_loop import DEFAULT_PROMOTION_COHESION
from .registry_io import load_json, write_registry_payload

ARTIFACT_ID = "v3_silver_pdb_residue_mapping_current702"
SCHEMA_VERSION = "silver_pdb_residue_mapping.v1"

FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
EXPANSION_REGISTRY_PATH = DEFAULT_EXPANSION_REGISTRY_PATH
DEFAULT_OUT = Path("artifacts/v3_silver_pdb_residue_mapping_current702.json")
DEFAULT_REPORT = Path("work/silver_pdb_residue_mapping_current702.md")
MAPPING_STATUS = "pdb_residue_mapping_from_mmcif_struct_ref_seq"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return None if text in {"?", "."} else text


def _int(value: Any) -> int | None:
    text = _clean(value)
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _parse_loop(cif_text: str, category: str) -> list[dict[str, str]]:
    lines = cif_text.splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() != "loop_":
            index += 1
            continue
        index += 1
        headers: list[str] = []
        while index < len(lines) and lines[index].strip().startswith("_"):
            headers.append(lines[index].strip())
            index += 1
        if not headers or not all(header.startswith(category) for header in headers):
            continue
        rows: list[dict[str, str]] = []
        while index < len(lines):
            line = lines[index].strip()
            if not line or line == "#":
                break
            if line == "loop_" or line.startswith("_") or line.startswith("data_"):
                break
            values = shlex.split(line)
            if len(values) >= len(headers):
                rows.append({h.removeprefix(category): v for h, v in zip(headers, values)})
            index += 1
        return rows
    return []


def _structure_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return (row.get("evidence") or {}).get("structure_provenance") or {}


def _mechanism_evidence(row: dict[str, Any]) -> dict[str, Any]:
    return (row.get("evidence") or {}).get("mechanism_evidence") or {}


def _holo_confirmation(row: dict[str, Any]) -> dict[str, Any]:
    confirmation = _structure_provenance(row).get("holo_pdb_confirmation") or {}
    return confirmation if isinstance(confirmation, dict) else {}


def _source_accession(row: dict[str, Any]) -> str:
    entry_id = str(row.get("entry_id") or "")
    if entry_id.startswith("uniprot:"):
        return entry_id.split(":", 1)[1]
    source = (row.get("evidence") or {}).get("source_provenance") or {}
    return str(source.get("accession") or "")


def _local_coordinate(row: dict[str, Any]) -> Path | None:
    raw = _structure_provenance(row).get("coordinate_path")
    if not raw:
        return None
    path = Path(str(raw))
    return path if path.exists() else None


def _exact_residues(row: dict[str, Any]) -> list[dict[str, Any]]:
    residues = _mechanism_evidence(row).get("active_site_residues") or []
    return [
        residue
        for residue in residues
        if isinstance(residue, dict) and residue.get("exact") and _int(residue.get("position"))
    ]


def _alignment_maps(
    cif_text: str,
    *,
    pdb_id: str,
    accession: str,
) -> tuple[list[dict[str, Any]], dict[tuple[str, int], dict[str, str]]]:
    refs = []
    for ref in _parse_loop(cif_text, "_struct_ref_seq."):
        if str(ref.get("pdbx_PDB_id_code") or "").upper() != pdb_id.upper():
            continue
        if str(ref.get("pdbx_db_accession") or "") != accession:
            continue
        chain = _clean(ref.get("pdbx_strand_id"))
        db_beg = _int(ref.get("db_align_beg"))
        db_end = _int(ref.get("db_align_end"))
        seq_beg = _int(ref.get("seq_align_beg"))
        if chain is None or db_beg is None or db_end is None or seq_beg is None:
            continue
        refs.append(
            {
                "chain": chain,
                "db_beg": db_beg,
                "db_end": db_end,
                "seq_beg": seq_beg,
            }
        )
    scheme: dict[tuple[str, int], dict[str, str]] = {}
    for row in _parse_loop(cif_text, "_pdbx_poly_seq_scheme."):
        chain = _clean(row.get("pdb_strand_id"))
        seq_id = _int(row.get("seq_id"))
        if chain is not None and seq_id is not None:
            scheme[(chain, seq_id)] = row
    return refs, scheme


def _map_position(
    position: int,
    *,
    pdb_id: str,
    refs: list[dict[str, Any]],
    scheme: dict[tuple[str, int], dict[str, str]],
) -> dict[str, Any] | None:
    for ref in refs:
        if not (ref["db_beg"] <= position <= ref["db_end"]):
            continue
        label_seq_id = ref["seq_beg"] + (position - ref["db_beg"])
        scheme_row = scheme.get((ref["chain"], label_seq_id))
        if scheme_row is None:
            continue
        auth_seq_num = _clean(scheme_row.get("auth_seq_num")) or str(label_seq_id)
        insertion = _clean(scheme_row.get("pdb_ins_code"))
        return {
            "pdb_id": pdb_id.upper(),
            "chain_name": ref["chain"],
            "label_seq_id": label_seq_id,
            "resid": auth_seq_num if insertion is None else f"{auth_seq_num}{insertion}",
            "code": _clean(scheme_row.get("auth_mon_id"))
            or _clean(scheme_row.get("mon_id")),
            "uniprot_position": position,
            "mapping_source": MAPPING_STATUS,
        }
    return None


def build_silver_pdb_residue_mapping(
    *,
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    limit: int | None = None,
) -> dict[str, Any]:
    created = created_utc or _utc_now_iso()
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
    mapping_rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    by_fingerprint: Counter[str] = Counter()
    attempted = 0

    for row in expansion_payload:
        new_row = json.loads(json.dumps(row))
        entry_id = str(new_row.get("entry_id") or "")
        if entry_id not in silver_ready_entries:
            out_rows.append(new_row)
            continue

        record: dict[str, Any] = {
            "entry_id": entry_id,
            "fingerprint_id": new_row.get("fingerprint_id"),
            "decision": "blocked_no_mapping",
            "mapped_residue_count": 0,
            "exact_residue_count": len(_exact_residues(new_row)),
            "registry_updated": False,
            "tier_changed": False,
        }
        coordinate = _local_coordinate(new_row)
        confirmation = _holo_confirmation(new_row)
        pdb_id = str(confirmation.get("pdb_id") or "").upper()
        expected_sha = confirmation.get("coordinate_sha256")
        accession = _source_accession(new_row)

        if coordinate is None:
            counts["missing_local_coordinate"] += 1
            record["decision"] = "blocked_missing_local_coordinate"
            mapping_rows.append(record)
            out_rows.append(new_row)
            continue
        if expected_sha and _sha256_path(coordinate) != expected_sha:
            counts["coordinate_sha_mismatch"] += 1
            record["decision"] = "blocked_coordinate_sha_mismatch"
            mapping_rows.append(record)
            out_rows.append(new_row)
            continue
        exact_residues = _exact_residues(new_row)
        if not exact_residues:
            counts["no_exact_residues"] += 1
            record["decision"] = "blocked_no_exact_residues"
            mapping_rows.append(record)
            out_rows.append(new_row)
            continue
        if limit is not None and attempted >= limit:
            counts["deferred_over_limit"] += 1
            record["decision"] = "deferred_over_limit"
            mapping_rows.append(record)
            out_rows.append(new_row)
            continue
        attempted += 1

        cif_text = coordinate.read_text(encoding="utf-8", errors="replace")
        refs, scheme = _alignment_maps(cif_text, pdb_id=pdb_id, accession=accession)
        if not refs or not scheme:
            counts["missing_mmcif_alignment_tables"] += 1
            record["decision"] = "blocked_missing_mmcif_alignment_tables"
            mapping_rows.append(record)
            out_rows.append(new_row)
            continue

        mapped = 0
        for residue in _exact_residues(new_row):
            position = _int(residue.get("position"))
            if position is None:
                continue
            mapping = _map_position(position, pdb_id=pdb_id, refs=refs, scheme=scheme)
            if mapping is None:
                continue
            existing = residue.setdefault("structure_positions", [])
            if not any(
                item.get("pdb_id") == mapping["pdb_id"]
                and item.get("chain_name") == mapping["chain_name"]
                and item.get("uniprot_position") == mapping["uniprot_position"]
                for item in existing
                if isinstance(item, dict)
            ):
                existing.append(mapping)
                mapped += 1

        if mapped == 0:
            counts["no_residue_positions_mapped"] += 1
            record["decision"] = "blocked_no_residue_positions_mapped"
        else:
            structure = new_row.setdefault("evidence", {}).setdefault(
                "structure_provenance", {}
            )
            structure["pdb_residue_mapping_provenance"] = {
                "status": MAPPING_STATUS,
                "pdb_id": pdb_id,
                "source_accession": accession,
                "coordinate_path": str(coordinate),
                "coordinate_sha256": _sha256_path(coordinate),
                "mapped_exact_active_site_residue_count": mapped,
                "retrieved_utc": created,
                "uniprot_to_pdb_mapping_is_explicit_not_inferred_identity": True,
                "mapping_is_review_only_not_predictive_feature": True,
            }
            counts["rows_mapped"] += 1
            counts["residues_mapped"] += mapped
            by_fingerprint[str(new_row.get("fingerprint_id") or "__missing__")] += 1
            record["decision"] = "mapped_explicit_pdb_residue_positions"
            record["registry_updated"] = True
            record["mapped_residue_count"] = mapped
        mapping_rows.append(record)
        out_rows.append(new_row)

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_write",
        "what": (
            "map exact UniProt active-site residue positions to explicit PDB "
            "chain/residue positions using mmCIF _struct_ref_seq plus "
            "_pdbx_poly_seq_scheme; no geometry scoring and no tier changes"
        ),
        "policy": {
            "silver_ready_source": "bronze_silver_promotion_preview",
            "cohesion_threshold": cohesion_threshold,
            "requires_local_holo_coordinate_sha_match": True,
            "mapping_source": "_struct_ref_seq + _pdbx_poly_seq_scheme",
            "uniprot_sequence_positions_are_not_pdb_residue_mappings_without_alignment": True,
            "mapping_is_review_only_not_predictive_feature": True,
        },
        "guardrails": {
            "frozen_current702_benchmark_preserved": True,
            "writes_expansion_registry_only": True,
            "row_count_unchanged": len(out_rows) == len(expansion_payload),
            "tier_changed": False,
            "geometry_confirmation_run_or_faked": False,
            "predictive_evidence_changed": False,
        },
        "counts": {
            "expansion_labels": len(expansion_payload),
            "silver_ready_input_rows": len(silver_ready_entries),
            "rows_attempted_with_local_coordinates": attempted,
            "rows_mapped": counts["rows_mapped"],
            "residues_mapped": counts["residues_mapped"],
            "missing_local_coordinate": counts["missing_local_coordinate"],
            "coordinate_sha_mismatch": counts["coordinate_sha_mismatch"],
            "no_exact_residues": counts["no_exact_residues"],
            "missing_mmcif_alignment_tables": counts["missing_mmcif_alignment_tables"],
            "no_residue_positions_mapped": counts["no_residue_positions_mapped"],
            "deferred_over_limit": counts["deferred_over_limit"],
        },
        "mapped_by_fingerprint": dict(sorted(by_fingerprint.items())),
        "next_action": (
            "Apply verified mapping updates, rerun the silver geometry audit, then run "
            "the separate geometry confirmation gate only for rows that become runnable."
        ),
        "rows": mapping_rows,
        "mapped_registry": out_rows,
    }


def summarize_mapping(audit: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in audit.items() if key != "mapped_registry"}


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Silver PDB Residue Mapping",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Maps exact UniProt active-site residues to explicit PDB chain/residue positions",
        "through mmCIF alignment tables. This does not run geometry scoring or change",
        "tiers.",
        "",
        "## Result",
        "",
        f"- Silver-ready input rows: {c['silver_ready_input_rows']}.",
        f"- Rows attempted with local coordinates: {c['rows_attempted_with_local_coordinates']}.",
        f"- Rows mapped: {c['rows_mapped']}.",
        f"- Exact residues mapped: {c['residues_mapped']}.",
        f"- Missing local coordinate: {c['missing_local_coordinate']}.",
        f"- Coordinate sha mismatch: {c['coordinate_sha_mismatch']}.",
        f"- Missing mmCIF alignment tables: {c['missing_mmcif_alignment_tables']}.",
        f"- No residue positions mapped: {c['no_residue_positions_mapped']}.",
        "",
        "## Guardrails",
        "",
        f"- Row count unchanged: {audit['guardrails']['row_count_unchanged']}.",
        f"- Tier changed: {audit['guardrails']['tier_changed']}.",
        f"- Geometry confirmation run or faked: "
        f"{audit['guardrails']['geometry_confirmation_run_or_faked']}.",
        "- Mappings are review-only provenance and are not predictive features.",
        "",
        "## Next Action",
        "",
        f"- {audit['next_action']}",
        "",
    ]
    return "\n".join(lines)


def write_silver_pdb_residue_mapping(
    *,
    out_path: Path = DEFAULT_OUT,
    report_path: Path | None = DEFAULT_REPORT,
    expansion_registry_path: Path = EXPANSION_REGISTRY_PATH,
    frozen_benchmark_path: Path = FROZEN_BENCHMARK_PATH,
    apply: bool = False,
    limit: int | None = None,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    frozen_path = Path(frozen_benchmark_path)
    if expansion_path.resolve() == frozen_path.resolve():
        raise ValueError("refusing to map residues into the frozen current702 benchmark")

    frozen_sha_before = (
        hashlib.sha256(frozen_path.read_bytes()).hexdigest() if frozen_path.exists() else None
    )
    expansion_payload = load_json(expansion_path) if expansion_path.exists() else []
    audit = build_silver_pdb_residue_mapping(
        expansion_payload=expansion_payload,
        limit=limit,
        cohesion_threshold=cohesion_threshold,
    )

    summary = summarize_mapping(audit)
    summary["frozen_sha256_before"] = frozen_sha_before
    summary["expansion_registry_written"] = False
    summary["frozen_benchmark_registry_written"] = False
    if apply:
        mapped = audit["mapped_registry"]
        if len(mapped) != len(expansion_payload):
            raise ValueError(
                "row-count guard tripped: mapped registry length "
                f"{len(mapped)} != input {len(expansion_payload)}"
            )
        from .labels import MechanismLabel

        for label in mapped:
            MechanismLabel.from_dict(label)
        write_result = write_registry_payload(expansion_path, mapped)
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
