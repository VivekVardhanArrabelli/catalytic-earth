"""Backfill the deploy-input SEQUENCE onto expansion bronze labels (non-destructive).

The North Star maps a raw protein SEQUENCE -> mechanism, but the expansion atlas
(`data/registries/external_bronze_labels.json`) stored only the UniProt handle and
length -- never the sequence itself. The frozen current702 benchmark sequences live in
a separate manifest, but the expansion labels carried NO sequence, so the one input a
deployed model actually predicts FROM was absent for every expansion row.

This module fetches the reviewed UniProt sequence for each expansion label by accession
and records it under ``evidence.sequence_provenance`` (sequence, sha256, length, source
accession, retrieval provenance, retrieved_utc). It is deliberately conservative:

- The raw sequence is the legitimate DEPLOY INPUT (what we predict FROM); it is NOT
  EC / protein name / UniProt prose, so it is allowed as stored data. It NEVER goes in
  ``predictive_evidence`` or ``excluded_context`` -- the leakage wall is unchanged. The
  block survives ``MechanismLabel.from_dict().to_dict()`` for both seed and out_of_scope
  labels and is accepted by the OOS leakage validator (``predictive_evidence`` stays []).
- Only the SEPARATE expansion registry is ever written, and only on explicit ``apply``.
  The frozen ``curated_mechanism_labels.json`` benchmark is never touched, and the apply
  path refuses to write any path that resolves to the frozen benchmark.
- Row counts are UNCHANGED: a sequence block is added to existing rows in place; no row
  is added, removed, or reordered. The registry is re-serialized with the same compact
  ``_dump_registry`` serializer the import pipeline uses, so the diff is exactly the new
  ``sequence_provenance`` key per row.
- The fetched length is cross-checked against the stored
  ``source_provenance.sequence_length``; on mismatch a conflict note is recorded and the
  stored length is preserved (never overwritten).

Fetching reuses the ``adapters`` UniProt primitives, but with a field set that INCLUDES
the sequence (``adapters.fetch_uniprot_accessions``'s default field set omits it). A
small on-disk fetch cache (under the git-ignored ``data/cache/``) lets a preview run and
a later ``apply`` run share one network pass.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlencode

from .adapters import (
    UNIPROT_SEARCH_URL,
    USER_AGENT,
    _chunked,
    _fetch_text,
    _split_accessions,
    normalize_uniprot_tsv,
)
from .registry_io import load_json, write_registry_payload

ARTIFACT_ID = "v3_label_sequence_backfill_preview_current702"
SCHEMA_VERSION = "label_sequence_backfill.v1"

# Field set that, unlike the adapters default, INCLUDES the sequence. length+reviewed are
# fetched for the length cross-check and to record the reviewed source status.
SEQUENCE_FIELDS = "accession,sequence,length,reviewed"
SEQUENCE_SOURCE = "reviewed_uniprot"
DEFAULT_BATCH_SIZE = 25
DEFAULT_FETCH_CACHE_PATH = Path("data/cache/label_sequence_fetch_cache.json")

# Default IO paths (mirror the other expansion runners).
FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")
DEFAULT_OUT = Path("artifacts/v3_label_sequence_backfill_preview_current702.json")
DEFAULT_REPORT = Path("work/label_sequence_backfill_current702.md")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sequence_sha256(sequence: str) -> str:
    return hashlib.sha256(sequence.encode("utf-8")).hexdigest()


def build_uniprot_sequence_url(accessions: list[str]) -> str:
    """A UniProt search URL whose field set INCLUDES the sequence (TSV)."""
    cleaned = sorted({accession.strip() for accession in accessions if accession.strip()})
    if not cleaned:
        raise ValueError("at least one UniProt accession is required")
    query = " OR ".join(f"accession:{accession}" for accession in cleaned)
    params = {
        "query": f"({query})",
        "fields": SEQUENCE_FIELDS,
        "format": "tsv",
        "size": str(len(cleaned)),
    }
    return f"{UNIPROT_SEARCH_URL}?{urlencode(params)}"


def _live_batch_fetcher(batch: list[str], *, timeout: int = 40) -> list[dict[str, Any]]:
    """Fetch one batch of accessions from live UniProt; return normalized records."""
    url = build_uniprot_sequence_url(batch)
    return normalize_uniprot_tsv(_fetch_text(url, timeout=timeout))


def fetch_uniprot_sequences(
    accessions: list[str],
    *,
    batch_size: int = DEFAULT_BATCH_SIZE,
    batch_fetcher: Callable[[list[str]], list[dict[str, Any]]] = _live_batch_fetcher,
    cache_path: Path | None = None,
) -> dict[str, dict[str, Any]]:
    """Map accession -> UniProt record (with ``sequence``), batched ~25 per request.

    Reuses ``adapters._split_accessions`` / ``_chunked``; each batch is a single TSV
    request whose field set includes the sequence. An optional on-disk cache (keyed by
    accession) lets a preview and a later apply share one network pass and survives
    transient failures.
    """
    wanted = sorted({item for accession in accessions for item in _split_accessions(accession)})
    by_accession: dict[str, dict[str, Any]] = {}

    cache: dict[str, dict[str, Any]] = {}
    if cache_path is not None and Path(cache_path).exists():
        try:
            loaded = json.loads(Path(cache_path).read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                cache = {str(k): v for k, v in loaded.items() if isinstance(v, dict)}
        except (json.JSONDecodeError, OSError):
            cache = {}

    for accession in wanted:
        if accession in cache and cache[accession].get("sequence"):
            by_accession[accession] = cache[accession]

    missing = [accession for accession in wanted if accession not in by_accession]
    for batch in _chunked(missing, batch_size):
        for record in batch_fetcher(batch):
            accession = str(record.get("accession") or "").strip()
            if accession and record.get("sequence"):
                by_accession[accession] = record
                cache[accession] = record

    if cache_path is not None and missing:
        Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
        Path(cache_path).write_text(
            json.dumps(cache, sort_keys=True), encoding="utf-8"
        )

    return by_accession


def sequence_provenance_block(
    *,
    sequence: str,
    accession: str,
    retrieved_utc: str,
    source: str = SEQUENCE_SOURCE,
    retrieval: dict[str, Any] | None = None,
    stored_length: int | None = None,
) -> dict[str, Any]:
    """Build the ``evidence.sequence_provenance`` block (the deploy input as data).

    On a length mismatch vs the stored ``source_provenance.sequence_length`` a conflict
    note is recorded and the stored length is preserved (never overwritten here).
    """
    fetched_length = len(sequence)
    block: dict[str, Any] = {
        "sequence": sequence,
        "sequence_sha256": _sequence_sha256(sequence),
        "sequence_length": fetched_length,
        "source_accession": accession,
        "source": source,
        "retrieved_utc": retrieved_utc,
        "retrieval": retrieval
        or {
            "endpoint": UNIPROT_SEARCH_URL,
            "fields": SEQUENCE_FIELDS,
            "format": "tsv",
            "user_agent": USER_AGENT,
        },
    }
    if stored_length is not None and int(stored_length) != fetched_length:
        block["source_provenance_sequence_length"] = int(stored_length)
        block["length_conflict_note"] = (
            f"fetched sequence length {fetched_length} != stored "
            f"source_provenance.sequence_length {int(stored_length)}; sequence stored "
            "as-fetched, stored length preserved (not overwritten)"
        )
    return block


def _retrieval_provenance(record: dict[str, Any], *, batch_size: int) -> dict[str, Any]:
    return {
        "endpoint": UNIPROT_SEARCH_URL,
        "fields": SEQUENCE_FIELDS,
        "format": "tsv",
        "batch_size": batch_size,
        "user_agent": USER_AGENT,
        "reviewed_status": record.get("reviewed"),
    }


def build_label_sequence_backfill(
    *,
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    sequences: dict[str, dict[str, Any]] | None = None,
    sequence_fetcher: Callable[..., dict[str, dict[str, Any]]] | None = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
    cache_path: Path | None = None,
) -> dict[str, Any]:
    """Backfill ``evidence.sequence_provenance`` onto every expansion label.

    Returns a non-destructive audit. ``backfilled_registry`` is the FULL new registry
    (rows in original order, sequence block added in place); the writer separates the
    small committable summary from that full payload.
    """
    created = created_utc or _utc_now_iso()

    # Accessions that still need a sequence (skip rows already backfilled -> idempotent).
    needed: list[str] = []
    for row in expansion_payload:
        evidence = row.get("evidence") or {}
        existing = (evidence.get("sequence_provenance") or {}).get("sequence")
        if existing:
            continue
        accession = (evidence.get("source_provenance") or {}).get("accession")
        if accession:
            needed.append(str(accession))

    if sequences is None:
        # Resolve the fetcher at call time so a monkeypatched module-level
        # ``fetch_uniprot_sequences`` (and the live default) are both honored.
        fetcher = sequence_fetcher or fetch_uniprot_sequences
        sequences = (
            fetcher(needed, batch_size=batch_size, cache_path=cache_path) if needed else {}
        )

    backfilled: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    fetch_failures: list[str] = []
    counts = Counter()
    coverage_by_fingerprint: Counter = Counter()

    for row in expansion_payload:
        new_row = json.loads(json.dumps(row))  # deep copy without aliasing
        evidence = new_row.setdefault("evidence", {})
        provenance = evidence.get("source_provenance") or {}
        accession = str(provenance.get("accession") or "")
        existing = (evidence.get("sequence_provenance") or {}).get("sequence")

        if existing:
            counts["already_backfilled"] += 1
            backfilled.append(new_row)
            continue

        record = sequences.get(accession) if accession else None
        sequence = (record or {}).get("sequence")
        if not sequence:
            counts["fetch_missing"] += 1
            if accession:
                fetch_failures.append(accession)
            backfilled.append(new_row)  # unchanged; never fabricate a sequence
            continue

        stored_length = provenance.get("sequence_length")
        block = sequence_provenance_block(
            sequence=sequence,
            accession=accession,
            retrieved_utc=created,
            retrieval=_retrieval_provenance(record, batch_size=batch_size),
            stored_length=stored_length,
        )
        evidence["sequence_provenance"] = block
        backfilled.append(new_row)
        counts["backfilled"] += 1
        if "length_conflict_note" in block:
            counts["length_conflict"] += 1
            conflicts.append(
                {
                    "entry_id": new_row.get("entry_id"),
                    "accession": accession,
                    "fetched_length": block["sequence_length"],
                    "stored_length": stored_length,
                }
            )
        fingerprint = new_row.get("fingerprint_id") or "__out_of_scope__"
        coverage_by_fingerprint[fingerprint] += 1

    rows_with_sequence = sum(
        1
        for row in backfilled
        if (row.get("evidence") or {}).get("sequence_provenance", {}).get("sequence")
    )

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_write",
        "what": (
            "backfill the deploy-input sequence (evidence.sequence_provenance) onto every "
            "expansion bronze label; the sequence is the legitimate model INPUT, not a "
            "predictive feature -- the leakage wall (EC/name/prose) is unchanged"
        ),
        "guardrails": {
            "frozen_current702_benchmark_preserved": True,
            "writes_expansion_registry_only": True,
            "row_count_unchanged": len(backfilled) == len(expansion_payload),
            "sequence_is_deploy_input_not_predictive_feature": True,
            "predictive_evidence_unchanged_empty_for_annotation_anchored": True,
            "stored_source_provenance_never_overwritten": True,
            "sequence_never_fabricated_when_fetch_missing": True,
        },
        "counts": {
            "expansion_labels": len(expansion_payload),
            "needed_fetch": len(needed),
            "distinct_accessions_fetched": len(sequences),
            "backfilled_this_run": counts["backfilled"],
            "already_backfilled": counts["already_backfilled"],
            "fetch_missing": counts["fetch_missing"],
            "length_conflicts": counts["length_conflict"],
            "rows_with_sequence_after": rows_with_sequence,
            "coverage_fraction_after": (
                round(rows_with_sequence / len(backfilled), 4) if backfilled else 0.0
            ),
        },
        "coverage_by_fingerprint_this_run": dict(sorted(coverage_by_fingerprint.items())),
        "length_conflicts": conflicts,
        "fetch_failures": sorted(fetch_failures),
        "fetch_failure_count": len(fetch_failures),
        "next_action": (
            "Review counts/conflicts, then on explicit authorization re-run with --apply "
            "to write data/registries/external_bronze_labels.json (frozen current702 never "
            "written; row count unchanged; only evidence.sequence_provenance added)."
        ),
        "backfilled_registry": backfilled,
    }


def summarize_backfill(audit: dict[str, Any]) -> dict[str, Any]:
    """The small, committable summary -- the full registry payload is dropped."""
    return {key: value for key, value in audit.items() if key != "backfilled_registry"}


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Label Sequence Backfill — deploy-input sequence for expansion bronze "
        "(non-destructive preview)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Backfills `evidence.sequence_provenance` (the raw protein SEQUENCE the model",
        "predicts FROM) onto every expansion bronze label by fetching the reviewed UniProt",
        "sequence by accession. The sequence is stored DATA, never a predictive feature:",
        "the leakage wall (EC / protein name / UniProt prose) is unchanged and",
        "`predictive_evidence` stays []. The frozen current702 benchmark is NOT written.",
        "",
        "## Result",
        "",
        f"- Expansion labels: {c['expansion_labels']} (row count unchanged).",
        f"- Needed fetch: {c['needed_fetch']}; distinct accessions fetched: "
        f"{c['distinct_accessions_fetched']}.",
        f"- **Backfilled this run: {c['backfilled_this_run']}** "
        f"(already backfilled {c['already_backfilled']}; fetch-missing {c['fetch_missing']}).",
        f"- Rows with sequence after: {c['rows_with_sequence_after']} "
        f"({c['coverage_fraction_after'] * 100:.1f}% coverage).",
        f"- Length conflicts (stored vs fetched): {c['length_conflicts']}.",
        "",
        "## Guardrails",
        "",
        f"- Frozen current702 preserved: "
        f"{audit['guardrails']['frozen_current702_benchmark_preserved']}.",
        f"- Writes expansion registry only: "
        f"{audit['guardrails']['writes_expansion_registry_only']}.",
        f"- Row count unchanged: {audit['guardrails']['row_count_unchanged']}.",
        "- Sequence is the deploy INPUT, not a predictive feature; "
        "stored source_provenance never overwritten; sequence never fabricated.",
        "",
        "## Next action",
        "",
        f"- {audit['next_action']}",
    ]
    if audit["fetch_failure_count"]:
        lines.extend(
            [
                "",
                "## Fetch failures (accessions with no reviewed sequence returned)",
                "",
                ", ".join(audit["fetch_failures"]),
            ]
        )
    return "\n".join(lines) + "\n"


def write_label_sequence_backfill(
    *,
    out_path: Path = DEFAULT_OUT,
    report_path: Path | None = DEFAULT_REPORT,
    expansion_registry_path: Path = EXPANSION_REGISTRY_PATH,
    frozen_benchmark_path: Path = FROZEN_BENCHMARK_PATH,
    apply: bool = False,
    batch_size: int = DEFAULT_BATCH_SIZE,
    cache_path: Path | None = DEFAULT_FETCH_CACHE_PATH,
) -> dict[str, Any]:
    """Build the backfill, write the summary + report, and (only on apply) the registry.

    Non-destructive by default: the expansion registry is written ONLY when ``apply`` is
    True. The frozen benchmark is never written, and the writer refuses to target it.
    """
    expansion_path = Path(expansion_registry_path)
    frozen_path = Path(frozen_benchmark_path)
    if expansion_path.resolve() == frozen_path.resolve():
        raise ValueError(
            "refusing to backfill: expansion registry path resolves to the frozen "
            "current702 benchmark, which is never written"
        )

    expansion_payload = load_json(expansion_path) if expansion_path.exists() else []
    audit = build_label_sequence_backfill(
        expansion_payload=expansion_payload,
        batch_size=batch_size,
        cache_path=cache_path,
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
        # Validate every row through the canonical (leakage-aware) schema before writing.
        from .labels import MechanismLabel  # local import avoids a module cycle

        for label in backfilled:
            MechanismLabel.from_dict(label)
        write_result = write_registry_payload(expansion_path, backfilled)
        summary["expansion_registry_written"] = True
        summary["expansion_registry_path"] = str(expansion_path)
        summary["expansion_registry_storage"] = write_result

    return summary
