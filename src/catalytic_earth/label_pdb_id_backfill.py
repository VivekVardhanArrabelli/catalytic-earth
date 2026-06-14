"""Backfill UniProt PDB cross-reference IDs onto expansion labels.

This is a structure-provenance backfill only. It copies curated UniProt ``xref_pdb``
handles into ``evidence.structure_provenance.pdb_ids`` for external registry rows that
currently lack experimental PDB IDs. PDB IDs remain provenance/admission context for holo
confirmation; they are never predictive features.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .adapters import UNIPROT_SEARCH_URL, USER_AGENT, fetch_uniprot_accessions
from .registry_io import load_json, write_registry_payload

ARTIFACT_ID = "v3_label_pdb_id_backfill_preview_current702"
SCHEMA_VERSION = "label_pdb_id_backfill.v1"
BACKFILLED_STATUS = "uniprot_xref_pdb_ids_backfilled"

FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")
DEFAULT_OUT = Path("artifacts/v3_label_pdb_id_backfill_preview_current702.json")
DEFAULT_REPORT = Path("work/label_pdb_id_backfill_current702.md")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _source_accession(row: dict[str, Any]) -> str:
    entry_id = str(row.get("entry_id") or "")
    if entry_id.startswith("uniprot:"):
        return entry_id.split(":", 1)[1]
    source = (row.get("evidence") or {}).get("source_provenance") or {}
    return str(source.get("accession") or "")


def _pdb_ids_from_structure(row: dict[str, Any]) -> list[str]:
    structure = (row.get("evidence") or {}).get("structure_provenance") or {}
    return sorted({str(value).upper() for value in structure.get("pdb_ids", []) or [] if value})


def _records_by_accession(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records = payload.get("records") if isinstance(payload, dict) else []
    return {
        str(record.get("accession")): record
        for record in records or []
        if isinstance(record, dict) and record.get("accession")
    }


def build_label_pdb_id_backfill(
    *,
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    uniprot_payload: dict[str, Any] | None = None,
    accessions_fetcher: Callable[[list[str]], dict[str, Any]] | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """Add missing UniProt PDB xrefs to external rows, non-destructively.

    ``limit`` caps rows whose accessions are fetched this run; rows beyond that are
    deferred unchanged. Already populated PDB IDs are preserved.
    """
    created = created_utc or _utc_now_iso()
    needed: list[str] = []
    for row in expansion_payload:
        if _pdb_ids_from_structure(row):
            continue
        accession = _source_accession(row)
        if accession:
            needed.append(accession)
        if limit is not None and len(needed) >= limit:
            break

    fetcher = accessions_fetcher or fetch_uniprot_accessions
    payload = uniprot_payload if uniprot_payload is not None else fetcher(needed)
    records = _records_by_accession(payload)
    fetched_accessions = set(needed)

    out_rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    by_fingerprint: Counter[str] = Counter()
    examples: list[dict[str, Any]] = []
    missing_examples: list[dict[str, Any]] = []

    for row in expansion_payload:
        new_row = json.loads(json.dumps(row))
        evidence = new_row.setdefault("evidence", {})
        structure = evidence.setdefault("structure_provenance", {})
        existing = _pdb_ids_from_structure(new_row)
        if existing:
            counts["already_had_pdb_ids"] += 1
            out_rows.append(new_row)
            continue

        accession = _source_accession(new_row)
        if not accession:
            counts["no_accession"] += 1
            out_rows.append(new_row)
            continue
        if accession not in fetched_accessions:
            counts["deferred_over_limit"] += 1
            out_rows.append(new_row)
            continue

        record = records.get(accession) or {}
        pdb_ids = sorted({str(value).upper() for value in record.get("pdb_ids", []) or [] if value})
        if not pdb_ids:
            counts["uniprot_record_without_pdb_xref"] += 1
            if len(missing_examples) < 25:
                missing_examples.append(
                    {
                        "entry_id": new_row.get("entry_id"),
                        "fingerprint_id": new_row.get("fingerprint_id"),
                        "accession": accession,
                    }
                )
            out_rows.append(new_row)
            continue

        structure["pdb_ids"] = pdb_ids
        structure["pdb_id_backfill_provenance"] = {
            "status": BACKFILLED_STATUS,
            "source": "uniprot_xref_pdb",
            "source_accession": accession,
            "pdb_ids": pdb_ids,
            "retrieved_utc": created,
            "retrieval": {
                "endpoint": UNIPROT_SEARCH_URL,
                "fields": "xref_pdb",
                "format": "tsv",
                "user_agent": USER_AGENT,
                "record_reviewed_status": record.get("reviewed"),
            },
            "pdb_ids_are_provenance_not_predictive_features": True,
        }
        counts["backfilled_pdb_ids"] += 1
        fp = str(new_row.get("fingerprint_id") or "__out_of_scope__")
        by_fingerprint[fp] += 1
        if len(examples) < 25:
            examples.append(
                {
                    "entry_id": new_row.get("entry_id"),
                    "fingerprint_id": new_row.get("fingerprint_id"),
                    "accession": accession,
                    "pdb_ids": pdb_ids,
                }
            )
        out_rows.append(new_row)

    rows_with_pdb_after = sum(1 for row in out_rows if _pdb_ids_from_structure(row))
    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_write",
        "what": (
            "backfill missing evidence.structure_provenance.pdb_ids from curated UniProt "
            "xref_pdb cross-references; PDB IDs are structure provenance for holo "
            "confirmation and are never predictive features"
        ),
        "guardrails": {
            "frozen_current702_benchmark_preserved": True,
            "writes_expansion_registry_only": True,
            "row_count_unchanged": len(out_rows) == len(expansion_payload),
            "pdb_ids_are_provenance_not_predictive_features": True,
            "predictive_evidence_unchanged": True,
            "existing_pdb_ids_preserved": True,
            "no_pdb_ids_fabricated_when_uniprot_lacks_xref": True,
        },
        "counts": {
            "expansion_labels": len(expansion_payload),
            "accessions_queried": len(needed),
            "uniprot_records_returned": len(records),
            "backfilled_pdb_rows_this_run": counts["backfilled_pdb_ids"],
            "already_had_pdb_ids": counts["already_had_pdb_ids"],
            "uniprot_record_without_pdb_xref": counts["uniprot_record_without_pdb_xref"],
            "no_accession": counts["no_accession"],
            "deferred_over_limit": counts["deferred_over_limit"],
            "rows_with_pdb_ids_after": rows_with_pdb_after,
        },
        "backfilled_by_fingerprint": dict(sorted(by_fingerprint.items())),
        "backfilled_examples": examples,
        "uniprot_without_pdb_xref_examples": missing_examples,
        "fetch_metadata": payload.get("metadata", {}) if isinstance(payload, dict) else {},
        "next_action": (
            "Review counts, then re-run with --apply to write only the external registry. "
            "Follow with holo structure promotion and bronze-silver promotion preview."
        ),
        "backfilled_registry": out_rows,
    }


def summarize_backfill(audit: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in audit.items() if key != "backfilled_registry"}


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Label PDB-ID Backfill - UniProt xref provenance",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Backfills missing `evidence.structure_provenance.pdb_ids` from UniProt",
        "`xref_pdb` cross-references. PDB IDs remain structure provenance for holo",
        "confirmation and are never predictive features. No frozen current702 row is written.",
        "",
        "## Result",
        "",
        f"- Expansion labels: {c['expansion_labels']} (row count unchanged).",
        f"- Accessions queried: {c['accessions_queried']}; UniProt records returned: "
        f"{c['uniprot_records_returned']}.",
        f"- **Backfilled PDB rows this run: {c['backfilled_pdb_rows_this_run']}**.",
        f"- Already had PDB IDs: {c['already_had_pdb_ids']}.",
        f"- UniProt records without PDB xrefs: {c['uniprot_record_without_pdb_xref']}.",
        f"- Deferred over limit: {c['deferred_over_limit']}.",
        f"- Rows with PDB IDs after: {c['rows_with_pdb_ids_after']}.",
        "",
        "## Guardrails",
        "",
        f"- Frozen current702 preserved: "
        f"{audit['guardrails']['frozen_current702_benchmark_preserved']}.",
        f"- Writes expansion registry only: "
        f"{audit['guardrails']['writes_expansion_registry_only']}.",
        f"- Row count unchanged: {audit['guardrails']['row_count_unchanged']}.",
        "- PDB IDs are provenance, not predictive features; existing PDB IDs are preserved.",
        "",
        "## Next action",
        "",
        f"- {audit['next_action']}",
    ]
    return "\n".join(lines) + "\n"


def write_label_pdb_id_backfill(
    *,
    out_path: Path = DEFAULT_OUT,
    report_path: Path | None = DEFAULT_REPORT,
    expansion_registry_path: Path = EXPANSION_REGISTRY_PATH,
    frozen_benchmark_path: Path = FROZEN_BENCHMARK_PATH,
    apply: bool = False,
    limit: int | None = None,
) -> dict[str, Any]:
    expansion_path = Path(expansion_registry_path)
    frozen_path = Path(frozen_benchmark_path)
    if expansion_path.resolve() == frozen_path.resolve():
        raise ValueError(
            "refusing to backfill: expansion registry path resolves to the frozen "
            "current702 benchmark, which is never written"
        )

    expansion_payload = load_json(expansion_path) if expansion_path.exists() else []
    audit = build_label_pdb_id_backfill(
        expansion_payload=expansion_payload,
        limit=limit,
    )

    summary = summarize_backfill(audit)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")

    summary["expansion_registry_written"] = False
    summary["frozen_benchmark_registry_written"] = False
    if apply:
        backfilled = audit["backfilled_registry"]
        if len(backfilled) != len(expansion_payload):
            raise ValueError(
                "row-count guard tripped: backfilled registry length "
                f"{len(backfilled)} != input {len(expansion_payload)}"
            )
        from .labels import MechanismLabel

        for label in backfilled:
            MechanismLabel.from_dict(label)
        write_result = write_registry_payload(expansion_path, backfilled)
        summary["expansion_registry_written"] = True
        summary["expansion_registry_path"] = str(expansion_path)
        summary["expansion_registry_storage"] = write_result

    return summary
