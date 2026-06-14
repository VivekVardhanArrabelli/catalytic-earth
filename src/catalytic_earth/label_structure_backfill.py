"""Stage AlphaFoldDB v6 coordinates for expansion labels and record provenance.

Track 1 (context depth), step 1b. With the deploy-input sequence now on every expansion
label (1a), the next missing context is STRUCTURE: the predicted coordinate unlocks
geometry / active-site context and the bronze->silver promotion path for all families.

This module derives the AlphaFoldDB v6 handle from each label's UniProt accession
(``AF-{accession}-F1-model_v6.cif``), fetches the predicted CIF, and records its
provenance + content hash under ``evidence.structure_provenance.afdb_v6_coordinate``
(handle, model URL, model version, sha256, byte size, atom-record count, retrieved_utc,
status). It is deliberately conservative:

- Coordinates are REGENERATABLE from the handle, so the large CIFs are NEVER committed:
  each is staged to a temp dir, hashed, and discarded. Only the hash + handle are stored.
- Only the SEPARATE expansion registry is ever written, and only on explicit ``apply``;
  the frozen ``curated_mechanism_labels.json`` benchmark is never touched and the writer
  refuses to target it.
- Row counts are UNCHANGED: a nested ``afdb_v6_coordinate`` block is added to each row's
  existing ``structure_provenance`` in place. The existing ``coordinate_status`` /
  ``coordinate_path`` fields (incl. the ser_his triad-confirmed status) are preserved --
  the staging provenance is additive.
- No sequence/EC/name/prose is touched; the leakage wall is unchanged. Structure is
  review-only mechanism context, never a predictive feature (a bronze->silver signal).

A small on-disk cache (under the git-ignored ``data/cache/``) records per-accession
provenance so a preview run and a later ``apply`` run (and chunked/resumed runs) share one
network pass.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .adapters import USER_AGENT
from .registry_io import load_json, write_registry_payload
from .ser_his_hole_sourcing import ALPHAFOLD_CIF_URL

ARTIFACT_ID = "v3_label_structure_backfill_preview_current702"
SCHEMA_VERSION = "label_structure_backfill.v1"

AFDB_MODEL_VERSION = "v6"
STAGED_STATUS = "afdb_v6_predicted_coordinate_staged"
UNAVAILABLE_STATUS = "afdb_v6_unavailable"
DEFAULT_STRUCTURE_CACHE_PATH = Path("data/cache/label_structure_afdb_v6_cache.json")

FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")
DEFAULT_OUT = Path("artifacts/v3_label_structure_backfill_preview_current702.json")
DEFAULT_REPORT = Path("work/label_structure_backfill_current702.md")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atom_record_count(cif_text: str) -> int:
    return sum(
        1
        for line in cif_text.splitlines()
        if line.startswith("ATOM ") or line.startswith("HETATM")
    )


def afdb_v6_handle(accession: str) -> tuple[str, str]:
    """Return the (structure_handle, model_url) for an accession's AFDB v6 prediction."""
    return f"AF-{accession}-F1", ALPHAFOLD_CIF_URL.format(accession=accession)


class _TransientFetchError(RuntimeError):
    """A transient (non-404) AFDB fetch failure that exhausted retries."""


def robust_afdb_v6_cif_fetcher(accession: str, *, attempts: int = 4) -> str | None:
    """Fetch the AFDB v6 CIF, distinguishing a genuine 404 from transient errors.

    Returns the CIF text, or ``None`` for a genuine 404 (no AFDB prediction). Transient
    errors (timeouts/5xx/connection resets) are retried with exponential backoff; if they
    persist it raises ``_TransientFetchError`` so the run fails loudly rather than caching
    a transient blip as a permanent "unavailable".
    """
    url = ALPHAFOLD_CIF_URL.format(accession=accession)
    last_exc: Exception | None = None
    for attempt in range(attempts):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=30) as response:  # noqa: S310 - public AFDB
                return response.read().decode("utf-8")
        except HTTPError as exc:
            if exc.code == 404:
                return None
            last_exc = exc  # 5xx etc. -> retry
        except (URLError, OSError) as exc:
            last_exc = exc
        if attempt < attempts - 1:
            time.sleep(2 ** attempt)
    raise _TransientFetchError(f"AFDB v6 fetch failed for {accession}: {last_exc}")


def stage_afdb_v6_coordinate(
    accession: str,
    *,
    cif_fetcher: Callable[[str], str | None] = robust_afdb_v6_cif_fetcher,
    retrieved_utc: str,
    staging_dir: Path | None = None,
) -> dict[str, Any]:
    """Fetch + hash the AFDB v6 CIF for an accession; the CIF is NOT kept.

    The coordinate is staged to a temp file, hashed, and discarded (it is regeneratable
    from the handle). Returns the provenance block recorded on ``structure_provenance``.
    """
    handle, url = afdb_v6_handle(accession)
    base = {
        "structure_handle": handle,
        "model_url": url,
        "model_version": AFDB_MODEL_VERSION,
        "retrieved_utc": retrieved_utc,
        "coordinate_committed": False,
        "regeneratable_from_handle": True,
    }
    cif_text = cif_fetcher(accession)
    if not cif_text:
        return {**base, "status": UNAVAILABLE_STATUS}

    encoded = cif_text.encode("utf-8")
    if staging_dir is not None:
        staging_dir = Path(staging_dir)
        staging_dir.mkdir(parents=True, exist_ok=True)
        coord_path = staging_dir / f"{handle}-model_{AFDB_MODEL_VERSION}.cif"
        coord_path.write_bytes(encoded)
        digest = hashlib.sha256(coord_path.read_bytes()).hexdigest()
        coord_path.unlink()  # regeneratable; never committed
    else:
        digest = hashlib.sha256(encoded).hexdigest()
    return {
        **base,
        "status": STAGED_STATUS,
        "coordinate_sha256": digest,
        "coordinate_bytes": len(encoded),
        "atom_record_count": _atom_record_count(cif_text),
    }


def _load_cache(cache_path: Path | None) -> dict[str, dict[str, Any]]:
    if cache_path is None or not Path(cache_path).exists():
        return {}
    try:
        loaded = json.loads(Path(cache_path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return {str(k): v for k, v in loaded.items() if isinstance(v, dict)} if isinstance(
        loaded, dict
    ) else {}


def build_label_structure_backfill(
    *,
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    cif_fetcher: Callable[[str], str | None] | None = None,
    cache_path: Path | None = None,
    limit: int | None = None,
    stage_to_temp: bool = True,
    cache_flush_every: int = 100,
) -> dict[str, Any]:
    """Stage AFDB v6 coordinates and add ``structure_provenance.afdb_v6_coordinate``.

    Returns a non-destructive audit. ``backfilled_registry`` is the FULL new registry
    (rows in original order, provenance added in place); the writer separates the small
    committable summary from that full payload. ``limit`` caps NEW fetches this run (for
    chunked runs); already-cached accessions never count against it.
    """
    created = created_utc or _utc_now_iso()
    fetcher = cif_fetcher or robust_afdb_v6_cif_fetcher
    cache = _load_cache(cache_path)

    counts: Counter = Counter()
    status_counts: Counter = Counter()
    fetched_this_run = 0
    backfilled: list[dict[str, Any]] = []
    unavailable: list[str] = []

    def _flush_cache() -> None:
        if cache_path is not None:
            Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
            Path(cache_path).write_text(json.dumps(cache, sort_keys=True), encoding="utf-8")

    staging_ctx = tempfile.TemporaryDirectory() if stage_to_temp else None
    staging_dir = Path(staging_ctx.name) if staging_ctx else None
    try:
        for row in expansion_payload:
            new_row = json.loads(json.dumps(row))
            evidence = new_row.setdefault("evidence", {})
            structure = evidence.setdefault("structure_provenance", {})
            accession = str((evidence.get("source_provenance") or {}).get("accession") or "")

            existing = structure.get("afdb_v6_coordinate")
            if isinstance(existing, dict) and existing.get("status") == STAGED_STATUS:
                counts["already_staged"] += 1
                status_counts[STAGED_STATUS] += 1
                backfilled.append(new_row)
                continue

            if not accession:
                counts["no_accession"] += 1
                backfilled.append(new_row)
                continue

            provenance = cache.get(accession)
            if provenance is None:
                if limit is not None and fetched_this_run >= limit:
                    counts["deferred_over_limit"] += 1
                    backfilled.append(new_row)
                    continue
                provenance = stage_afdb_v6_coordinate(
                    accession,
                    cif_fetcher=fetcher,
                    retrieved_utc=created,
                    staging_dir=staging_dir,
                )
                fetched_this_run += 1
                if cache_path is not None:
                    cache[accession] = provenance
                    # Incremental flush so a long resumable run never loses staged work.
                    if fetched_this_run % cache_flush_every == 0:
                        _flush_cache()

            structure["afdb_v6_coordinate"] = provenance
            status = provenance.get("status")
            status_counts[status] += 1
            if status == STAGED_STATUS:
                counts["staged"] += 1
            elif status == UNAVAILABLE_STATUS:
                counts["unavailable"] += 1
                unavailable.append(accession)
            backfilled.append(new_row)
    finally:
        if staging_ctx is not None:
            staging_ctx.cleanup()

    if fetched_this_run:
        _flush_cache()

    rows_with_coord = sum(
        1
        for row in backfilled
        if (row.get("evidence") or {})
        .get("structure_provenance", {})
        .get("afdb_v6_coordinate", {})
        .get("coordinate_sha256")
    )

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_write",
        "what": (
            "stage AlphaFoldDB v6 predicted coordinates for expansion labels and record "
            "evidence.structure_provenance.afdb_v6_coordinate (handle + sha256 + provenance); "
            "the CIFs are regeneratable from the handle and are NOT committed; structure is "
            "review-only mechanism context (a bronze->silver signal), never a predictive feature"
        ),
        "guardrails": {
            "frozen_current702_benchmark_preserved": True,
            "writes_expansion_registry_only": True,
            "row_count_unchanged": len(backfilled) == len(expansion_payload),
            "large_cifs_never_committed": True,
            "coordinate_regeneratable_from_handle": True,
            "existing_structure_provenance_preserved_additive": True,
            "structure_is_review_only_not_predictive_feature": True,
        },
        "counts": {
            "expansion_labels": len(expansion_payload),
            "staged_this_run": counts["staged"],
            "already_staged": counts["already_staged"],
            "unavailable": counts["unavailable"],
            "deferred_over_limit": counts["deferred_over_limit"],
            "no_accession": counts["no_accession"],
            "fetched_this_run": fetched_this_run,
            "rows_with_staged_coordinate_after": rows_with_coord,
            "coverage_fraction_after": (
                round(rows_with_coord / len(backfilled), 4) if backfilled else 0.0
            ),
        },
        "status_counts": dict(sorted(status_counts.items(), key=lambda kv: str(kv[0]))),
        "unavailable_accessions": sorted(unavailable)[:200],
        "unavailable_accession_count": len(unavailable),
        "next_action": (
            "Review counts, then re-run with --apply to write "
            "data/registries/external_bronze_labels.json (frozen current702 never written; "
            "row count unchanged; only evidence.structure_provenance.afdb_v6_coordinate added). "
            "Use --limit for chunked runs; the cache makes re-runs resumable."
        ),
        "backfilled_registry": backfilled,
    }


def summarize_backfill(audit: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in audit.items() if key != "backfilled_registry"}


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Label Structure Backfill — AlphaFoldDB v6 coordinate provenance "
        "(non-destructive preview)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Stages the AlphaFoldDB v6 predicted coordinate for each expansion label by",
        "accession (`AF-{acc}-F1-model_v6.cif`), hashes it, and records",
        "`evidence.structure_provenance.afdb_v6_coordinate` (handle + sha256 + provenance).",
        "The CIFs are regeneratable from the handle and are NOT committed. Structure is",
        "review-only mechanism context (a bronze->silver signal), never a predictive feature.",
        "The frozen current702 benchmark is NOT written.",
        "",
        "## Result",
        "",
        f"- Expansion labels: {c['expansion_labels']} (row count unchanged).",
        f"- **Staged this run: {c['staged_this_run']}** "
        f"(already staged {c['already_staged']}; unavailable {c['unavailable']}; "
        f"deferred over --limit {c['deferred_over_limit']}).",
        f"- Rows with a staged coordinate after: {c['rows_with_staged_coordinate_after']} "
        f"({c['coverage_fraction_after'] * 100:.1f}% coverage).",
        f"- AFDB fetches this run: {c['fetched_this_run']}.",
        "",
        f"Status breakdown: {audit['status_counts']}.",
        "",
        "## Guardrails",
        "",
        f"- Frozen current702 preserved: "
        f"{audit['guardrails']['frozen_current702_benchmark_preserved']}.",
        f"- Writes expansion registry only: "
        f"{audit['guardrails']['writes_expansion_registry_only']}.",
        f"- Row count unchanged: {audit['guardrails']['row_count_unchanged']}.",
        "- Large CIFs never committed; coordinate regeneratable from handle; existing "
        "structure_provenance preserved (additive); structure is review-only, not predictive.",
        "",
        "## Next action",
        "",
        f"- {audit['next_action']}",
    ]
    if audit["unavailable_accession_count"]:
        lines.extend(
            [
                "",
                f"## AFDB v6 unavailable ({audit['unavailable_accession_count']} accessions, "
                "first 200)",
                "",
                ", ".join(audit["unavailable_accessions"]),
            ]
        )
    return "\n".join(lines) + "\n"


def write_label_structure_backfill(
    *,
    out_path: Path = DEFAULT_OUT,
    report_path: Path | None = DEFAULT_REPORT,
    expansion_registry_path: Path = EXPANSION_REGISTRY_PATH,
    frozen_benchmark_path: Path = FROZEN_BENCHMARK_PATH,
    apply: bool = False,
    cache_path: Path | None = DEFAULT_STRUCTURE_CACHE_PATH,
    limit: int | None = None,
) -> dict[str, Any]:
    """Build the structure backfill, write summary + report, and (only on apply) registry."""
    expansion_path = Path(expansion_registry_path)
    frozen_path = Path(frozen_benchmark_path)
    if expansion_path.resolve() == frozen_path.resolve():
        raise ValueError(
            "refusing to backfill: expansion registry path resolves to the frozen "
            "current702 benchmark, which is never written"
        )

    expansion_payload = load_json(expansion_path) if expansion_path.exists() else []
    audit = build_label_structure_backfill(
        expansion_payload=expansion_payload,
        cache_path=cache_path,
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
        from .labels import MechanismLabel  # local import avoids a module cycle

        for label in backfilled:
            MechanismLabel.from_dict(label)
        write_result = write_registry_payload(expansion_path, backfilled)
        summary["expansion_registry_written"] = True
        summary["expansion_registry_path"] = str(expansion_path)
        summary["expansion_registry_storage"] = write_result

    return summary
