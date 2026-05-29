from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .transfer_scope import _compute_sequence_embedding_payload


def build_sequence_embedding_sidecar(
    *,
    sequence_manifest: dict[str, Any],
    fasta_text: str,
    embedding_backend: str = "deterministic_sequence_kmer_control",
    model_name: str = "facebook/esm2_t6_8M_UR50D",
    local_files_only: bool = True,
    max_rows: int = 0,
    fallback_to_largest_local_esm2: bool = True,
) -> dict[str, Any]:
    """Build a raw embedding sidecar without retaining label fields."""
    fasta_by_alias = _parse_fasta_aliases(fasta_text)
    manifest_rows = [
        row for row in sequence_manifest.get("rows", []) if isinstance(row, dict)
    ]
    if max_rows > 0:
        manifest_rows = manifest_rows[:max_rows]

    sidecar_inputs: list[dict[str, Any]] = []
    missing_sequences: list[dict[str, str]] = []
    records_by_key: dict[str, dict[str, str]] = {}
    for row in manifest_rows:
        entry_id = str(row.get("entry_id") or "")
        if not entry_id:
            continue
        sequence_record = _first_sequence_record(row)
        aliases = _sequence_record_aliases(entry_id, sequence_record)
        sequence = ""
        matched_alias = None
        for alias in aliases:
            if alias in fasta_by_alias:
                sequence = fasta_by_alias[alias]["sequence"]
                matched_alias = alias
                break
        if not sequence:
            missing_sequences.append(
                {"entry_id": entry_id, "reason": "sequence_not_found_in_fasta"}
            )
            continue
        records_by_key[entry_id] = {"sequence": sequence}
        sidecar_inputs.append(
            {
                "entry_id": entry_id,
                "sequence_record_id": sequence_record.get("accession_or_structure_id")
                or sequence_record.get("accession")
                or row.get("sequence_id")
                or matched_alias,
                "sequence_sha256": sequence_record.get("sequence_sha256")
                or hashlib.sha256(sequence.encode("utf-8")).hexdigest(),
                "sequence_length": len(sequence),
                "matched_fasta_alias": str(matched_alias or ""),
                "split_assignment": row.get("split_assignment"),
            }
        )

    entry_ids = [row["entry_id"] for row in sidecar_inputs]
    embedding_payload = _compute_sequence_embedding_payload(
        records_by_accession=records_by_key,
        accessions=entry_ids,
        embedding_backend=embedding_backend,
        model_name=model_name,
        local_files_only=local_files_only,
        fallback_to_largest_local_esm2=fallback_to_largest_local_esm2,
    )
    embeddings = embedding_payload.get("embeddings_by_accession", {})
    records: list[dict[str, Any]] = []
    for row in sidecar_inputs:
        vector = embeddings.get(row["entry_id"])
        if vector is None:
            continue
        records.append(
            {
                "schema_version": "sequence_embedding_sidecar_row.v1",
                "entry_id": row["entry_id"],
                "sequence_record_id": row["sequence_record_id"],
                "sequence_sha256": row["sequence_sha256"],
                "sequence_length": row["sequence_length"],
                "split_assignment": row["split_assignment"],
                "embedding_backend": embedding_payload["metadata"].get(
                    "embedding_backend"
                ),
                "computed_embedding_backend": embedding_payload["metadata"].get(
                    "computed_embedding_backend"
                ),
                "model_name": embedding_payload["metadata"].get("model_name"),
                "embedding_vector_dimension": embedding_payload["metadata"].get(
                    "embedding_vector_dimension"
                ),
                "vector_storage": (
                    "raw_dense_list" if isinstance(vector, list) else "raw_sparse_mapping"
                ),
                "raw_embedding": vector,
            }
        )

    embedding_failures = embedding_payload.get("embedding_failures", [])
    summary = {
        "artifact_id": "v3_sequence_embedding_sidecar_current702_20260529",
        "schema_version": "sequence_embedding_sidecar_summary.v1",
        "created_utc": _utc_now_iso(),
        "status": _summary_status(
            emitted_count=len(records),
            joined_count=len(sidecar_inputs),
            failure_count=int(
                embedding_payload["metadata"].get("embedding_failure_count", 0) or 0
            ),
        ),
        "raw_embedding_vectors_retained": bool(records),
        "raw_embedding_vectors_requested": True,
        "label_fields_retained": False,
        "review_or_import_fields_retained": False,
        "label_registry_edited": False,
        "fingerprint_registry_edited": False,
        "ontology_registry_edited": False,
        "production_scoring_changed": False,
        "global_threshold_changed": False,
        "large_downloads_performed": False,
        "sequence_manifest_method": sequence_manifest.get("metadata", {}).get("method"),
        "requested_row_count": len(manifest_rows),
        "sequence_joined_row_count": len(sidecar_inputs),
        "emitted_row_count": len(records),
        "missing_sequence_rows": missing_sequences,
        "embedding_backend": embedding_payload["metadata"].get("embedding_backend"),
        "computed_embedding_backend": embedding_payload["metadata"].get(
            "computed_embedding_backend"
        ),
        "requested_embedding_backend": embedding_payload["metadata"].get(
            "requested_embedding_backend", embedding_backend
        ),
        "model_name": embedding_payload["metadata"].get("model_name"),
        "local_files_only": embedding_payload["metadata"].get("local_files_only"),
        "embedding_backend_available": embedding_payload["metadata"].get(
            "embedding_backend_available"
        ),
        "embedding_vector_dimension": embedding_payload["metadata"].get(
            "embedding_vector_dimension"
        ),
        "embedding_failure_count": embedding_payload["metadata"].get(
            "embedding_failure_count", 0
        ),
        "embedding_failures_sample": embedding_failures[:20],
        "embedding_failure_error_types": sorted(
            {str(row.get("error_type")) for row in embedding_failures if row.get("error_type")}
        ),
        "warnings": embedding_payload.get("warnings", []),
        "predictive_feature_policy": (
            "sidecar rows retain only raw sequence-derived embeddings plus row "
            "identity/split metadata; labels, EC/Rhea, names, mechanism text, "
            "expert notes, review decisions, and heuristic predictions are not "
            "retained in the sidecar"
        ),
    }
    return {"summary": summary, "records": records}


def _summary_status(
    *,
    emitted_count: int,
    joined_count: int,
    failure_count: int,
) -> str:
    if emitted_count and emitted_count == joined_count and failure_count == 0:
        return "complete"
    if emitted_count:
        return "partial"
    return "blocked_no_embeddings_emitted"


def write_sequence_embedding_sidecar(
    *,
    sequence_manifest_path: Path,
    fasta_path: Path,
    out_path: Path,
    summary_path: Path,
    embedding_backend: str = "deterministic_sequence_kmer_control",
    model_name: str = "facebook/esm2_t6_8M_UR50D",
    local_files_only: bool = True,
    max_rows: int = 0,
    fallback_to_largest_local_esm2: bool = True,
) -> dict[str, Any]:
    with sequence_manifest_path.open("r", encoding="utf-8") as handle:
        sequence_manifest = json.load(handle)
    fasta_text = fasta_path.read_text(encoding="utf-8")
    sidecar = build_sequence_embedding_sidecar(
        sequence_manifest=sequence_manifest,
        fasta_text=fasta_text,
        embedding_backend=embedding_backend,
        model_name=model_name,
        local_files_only=local_files_only,
        max_rows=max_rows,
        fallback_to_largest_local_esm2=fallback_to_largest_local_esm2,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        for record in sidecar["records"]:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(sidecar["summary"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return sidecar["summary"]


def _parse_fasta_aliases(fasta_text: str) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    header = ""
    chunks: list[str] = []
    for raw_line in fasta_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            _store_fasta_record(records, header, chunks)
            header = line[1:].strip()
            chunks = []
        else:
            chunks.append(line)
    _store_fasta_record(records, header, chunks)
    return records


def _store_fasta_record(
    records: dict[str, dict[str, str]],
    header: str,
    chunks: list[str],
) -> None:
    if not header:
        return
    sequence = "".join(chunks).strip().upper()
    first_token = header.split()[0]
    for alias in _header_aliases(first_token):
        records[alias] = {"header": header, "sequence": sequence}


def _header_aliases(first_token: str) -> list[str]:
    aliases = [first_token]
    parts = [part for part in first_token.split("|") if part]
    aliases.extend(parts)
    for part in parts:
        if part.startswith("fallback_for_uniprot:"):
            aliases.append(part.split(":", 1)[1])
        if part.startswith("uniprot:"):
            aliases.append(part.split(":", 1)[1])
    if len(parts) >= 2 and parts[0] in {"sp", "tr"}:
        aliases.append(parts[1])
    seen: set[str] = set()
    ordered: list[str] = []
    for alias in aliases:
        if alias not in seen:
            ordered.append(alias)
            seen.add(alias)
    return ordered


def _first_sequence_record(row: dict[str, Any]) -> dict[str, Any]:
    records = row.get("sequence_records", [])
    if isinstance(records, list) and records and isinstance(records[0], dict):
        return records[0]
    return {}


def _sequence_record_aliases(
    entry_id: str,
    sequence_record: dict[str, Any],
) -> list[str]:
    aliases = [entry_id]
    for key in ("accession_or_structure_id", "accession", "sequence_id"):
        value = sequence_record.get(key)
        if value:
            aliases.append(str(value))
    seen: set[str] = set()
    ordered: list[str] = []
    for alias in aliases:
        if alias and alias not in seen:
            ordered.append(alias)
            seen.add(alias)
    return ordered


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
