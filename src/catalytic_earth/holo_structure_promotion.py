"""Stage HOLO experimental-PDB coordinate confirmation for bronze->silver promotion.

The bronze->silver promotion gate (`bronze_silver_promotion_preview`) abstains whenever
the annotated cofactor is ABSENT from a label's coordinates (the documented Problem-2
degradation). The registry's staged coordinates are AlphaFoldDB predictions, which are
inherently apo (AlphaFold models carry no cofactor), so `silver_ready` has been stuck at
**0**: every chemistry-corroborated row is `blocked_pending_structure` /
`blocked_apo_needs_cofactor_fusion`.

This module supplies the missing HOLO signal from EXPERIMENTAL structures. For each bronze
seed label whose chemistry already independently corroborates its fingerprint (the
promotion gate's own decision) and that carries experimental ``pdb_ids`` plus an annotated
cofactor, it fetches the PDB mmCIF and checks whether the annotated cofactor is present as
a HETATM (the SAME holo test the gate uses). When it is, it records a sha-pinned
``structure_provenance.holo_pdb_confirmation`` block. The gate's
``structure_confirmability`` honours that recorded confirmation as ``holo`` -- so the row
becomes ``silver_ready_pending_geometry_run`` (still pending the SEPARATE authorized
geometry-confirmation run; this only proves the gate is meetable).

It mirrors the AFDB backfill's discipline:

- The mmCIF is REGENERATABLE from the PDB id, so the (large) coordinate file is NEVER
  committed -- staged to temp, hashed, discarded. Only the holo determination + sha are
  stored.
- Only the SEPARATE expansion registry is ever written, and only on explicit ``apply``;
  the frozen ``curated_mechanism_labels.json`` is never touched (the writer refuses to
  target it and prints its sha before/after).
- Row counts are UNCHANGED: a nested ``holo_pdb_confirmation`` block is added in place.
- Leakage wall unchanged: structure is review-only mechanism context, never a predictive
  feature. The corroboration that selects candidates is the chemistry gate (cofactor/ligand
  identity + Rhea reaction), never EC/name/prose/fingerprint.
- A git-ignored cache under ``data/cache/`` records per-PDB HETATM content so a preview and
  a later apply (and chunked/resumed runs) share one network pass.
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
from .bronze_silver_promotion_preview import (
    _NON_COFACTOR_HET,
    expected_cofactor_comp_ids,
)
from .external_annotation_anchored_import import _dump_registry
from .mechanism_representation_loop import (
    DEFAULT_PROMOTION_COHESION,
    assess_row_against_centroids,
    fingerprint_centroids,
)
from .structure import parse_atom_site_loop

ARTIFACT_ID = "v3_holo_structure_promotion_preview_current702"
SCHEMA_VERSION = "holo_structure_promotion.v1"

FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")
DEFAULT_OUT = Path("artifacts/v3_holo_structure_promotion_preview_current702.json")
DEFAULT_REPORT = Path("work/holo_structure_promotion_current702.md")
DEFAULT_CACHE_PATH = Path("data/cache/holo_pdb_hetatm_cache.json")

RCSB_CIF_URL = "https://files.rcsb.org/download/{pdb_id}.cif"
CONFIRMED_STATUS = "holo_experimental_coordinate_confirmed"
NO_HOLO_STATUS = "no_holo_pdb_found"

# The promotion-gate decisions that mean "chemistry corroborates, only structure is
# missing" -- exactly the rows a holo confirmation can unblock.
STRUCTURE_BLOCKED_DECISIONS = frozenset(
    {"blocked_pending_structure", "blocked_apo_needs_cofactor_fusion"}
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _atom_record_count(cif_text: str) -> int:
    return sum(
        1
        for line in cif_text.splitlines()
        if line.startswith("ATOM ") or line.startswith("HETATM")
    )


class _TransientFetchError(RuntimeError):
    """A transient (non-404) RCSB fetch failure that exhausted retries."""


def robust_rcsb_cif_fetcher(pdb_id: str, *, attempts: int = 4) -> str | None:
    """Fetch the experimental PDB mmCIF, distinguishing a genuine 404 from transients.

    Returns the CIF text, or ``None`` for a genuine 404 (no such entry / obsoleted).
    Transient errors (timeouts/5xx) are retried with exponential backoff; persistent
    transients raise so the run fails loudly rather than caching a blip as "no entry".
    """
    url = RCSB_CIF_URL.format(pdb_id=pdb_id.upper())
    last_exc: Exception | None = None
    for attempt in range(attempts):
        request = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=30) as response:  # noqa: S310 - public RCSB
                return response.read().decode("utf-8", "replace")
        except HTTPError as exc:
            if exc.code == 404:
                return None
            last_exc = exc
        except (URLError, OSError) as exc:
            last_exc = exc
        if attempt < attempts - 1:
            time.sleep(2 ** attempt)
    raise _TransientFetchError(f"RCSB mmCIF fetch failed for {pdb_id}: {last_exc}")


def hetatm_comp_ids_from_cif(cif_text: str) -> set[str]:
    """The non-solvent HETATM comp ids in a mmCIF (the candidate cofactor ligands)."""
    atoms = parse_atom_site_loop(cif_text)
    return {
        a.get("label_comp_id")
        for a in atoms
        if a.get("group_PDB") == "HETATM" and a.get("label_comp_id") not in _NON_COFACTOR_HET
    }


def _pdb_hetatm_record(
    pdb_id: str,
    *,
    cif_fetcher: Callable[[str], str | None],
    retrieved_utc: str,
    staging_dir: Path | None,
) -> dict[str, Any] | None:
    """Fetch + hash one PDB mmCIF; record its HETATM content. CIF is NOT kept.

    Returns ``None`` for a genuine 404 (entry unavailable).
    """
    cif_text = cif_fetcher(pdb_id)
    if cif_text is None:
        return None
    encoded = cif_text.encode("utf-8")
    if staging_dir is not None:
        staging_dir = Path(staging_dir)
        staging_dir.mkdir(parents=True, exist_ok=True)
        coord_path = staging_dir / f"pdb_{pdb_id.upper()}.cif"
        coord_path.write_bytes(encoded)
        digest = hashlib.sha256(coord_path.read_bytes()).hexdigest()
        coord_path.unlink()  # regeneratable from the PDB id; never committed
    else:
        digest = hashlib.sha256(encoded).hexdigest()
    return {
        "hetatm_comp_ids": sorted(hetatm_comp_ids_from_cif(cif_text)),
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
    return (
        {str(k): v for k, v in loaded.items() if isinstance(v, dict)}
        if isinstance(loaded, dict)
        else {}
    )


def _structure_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("structure_provenance", {}) or {}


def build_holo_structure_promotion(
    *,
    expansion_payload: list[dict[str, Any]],
    created_utc: str | None = None,
    cif_fetcher: Callable[[str], str | None] | None = None,
    cache_path: Path | None = None,
    limit: int | None = None,
    per_fingerprint_cap: int | None = None,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
    stage_to_temp: bool = True,
    cache_flush_every: int = 50,
) -> dict[str, Any]:
    """Confirm HOLO experimental coordinates for chemistry-corroborated bronze labels.

    Returns a non-destructive audit. ``promoted_registry`` is the FULL new registry (rows in
    original order, ``holo_pdb_confirmation`` added in place on confirmed rows). ``limit``
    caps NEW candidate rows fetched this run (already-confirmed/cached rows do not count).
    """
    created = created_utc or _utc_now_iso()
    fetcher = cif_fetcher or robust_rcsb_cif_fetcher
    cache = _load_cache(cache_path)

    seed = [r for r in expansion_payload if r.get("label_type") == "seed_fingerprint"]
    centroids = fingerprint_centroids(seed)

    counts: Counter = Counter()
    status_counts: Counter = Counter()
    confirmed_by_fp: Counter = Counter()
    fp_attempted: Counter = Counter()
    fetched_rows = 0
    confirmed_examples: list[dict[str, Any]] = []
    out_rows: list[dict[str, Any]] = []

    def _flush_cache() -> None:
        if cache_path is not None:
            Path(cache_path).parent.mkdir(parents=True, exist_ok=True)
            Path(cache_path).write_text(json.dumps(cache, sort_keys=True), encoding="utf-8")

    def _is_corroborated_structure_blocked(row: dict[str, Any]) -> bool:
        chem = assess_row_against_centroids(row, centroids)
        if chem["chemistry_agrees_with_label"] is not True:
            return False
        return (chem["own_cohesion"] or 0.0) >= cohesion_threshold

    staging_ctx = tempfile.TemporaryDirectory() if stage_to_temp else None
    staging_dir = Path(staging_ctx.name) if staging_ctx else None
    try:
        for row in expansion_payload:
            new_row = json.loads(json.dumps(row))
            if new_row.get("label_type") != "seed_fingerprint":
                out_rows.append(new_row)
                continue

            structure = new_row.setdefault("evidence", {}).setdefault(
                "structure_provenance", {}
            )
            existing = structure.get("holo_pdb_confirmation")
            if isinstance(existing, dict) and existing.get("status") == CONFIRMED_STATUS:
                counts["already_confirmed"] += 1
                status_counts[CONFIRMED_STATUS] += 1
                out_rows.append(new_row)
                continue

            fp = new_row.get("fingerprint_id")
            pdb_ids = [str(p) for p in (_structure_provenance(new_row).get("pdb_ids") or [])]
            expected = expected_cofactor_comp_ids(new_row)
            if not pdb_ids or not expected:
                counts["no_pdb_or_cofactor"] += 1
                out_rows.append(new_row)
                continue
            if not _is_corroborated_structure_blocked(new_row):
                counts["not_chemistry_corroborated"] += 1
                out_rows.append(new_row)
                continue
            if per_fingerprint_cap is not None and fp_attempted[fp] >= per_fingerprint_cap:
                counts["deferred_over_fingerprint_cap"] += 1
                out_rows.append(new_row)
                continue

            # does this row need a NEW network fetch (any of its PDBs uncached)?
            needs_fetch = any(pid.upper() not in cache for pid in pdb_ids)
            if needs_fetch and limit is not None and fetched_rows >= limit:
                counts["deferred_over_limit"] += 1
                out_rows.append(new_row)
                continue

            fp_attempted[fp] += 1
            confirmation: dict[str, Any] | None = None
            checked: list[str] = []
            did_fetch = False
            for pid in pdb_ids:
                key = pid.upper()
                rec = cache.get(key)
                if rec is None:
                    rec = _pdb_hetatm_record(
                        pid,
                        cif_fetcher=fetcher,
                        retrieved_utc=created,
                        staging_dir=staging_dir,
                    )
                    did_fetch = True
                    if rec is None:  # genuine 404
                        cache[key] = {"hetatm_comp_ids": [], "unavailable": True}
                        rec = cache[key]
                    else:
                        cache[key] = rec
                    if cache_path is not None and len(cache) % cache_flush_every == 0:
                        _flush_cache()
                checked.append(key)
                present = sorted(set(rec.get("hetatm_comp_ids") or []) & expected)
                if present:
                    confirmation = {
                        "status": CONFIRMED_STATUS,
                        "pdb_id": key,
                        "model_url": RCSB_CIF_URL.format(pdb_id=key),
                        "cofactor_comp_ids_present": present,
                        "coordinate_sha256": rec.get("coordinate_sha256"),
                        "atom_record_count": rec.get("atom_record_count"),
                        "pdb_ids_checked": checked,
                        "retrieved_utc": created,
                        "coordinate_committed": False,
                        "regeneratable_from_pdb_id": True,
                    }
                    break
            if did_fetch:
                fetched_rows += 1

            if confirmation is None:
                confirmation = {
                    "status": NO_HOLO_STATUS,
                    "pdb_ids_checked": checked,
                    "expected_cofactor_comp_ids": sorted(expected),
                    "retrieved_utc": created,
                }
                counts["no_holo_pdb_found"] += 1
                status_counts[NO_HOLO_STATUS] += 1
            else:
                counts["holo_confirmed"] += 1
                status_counts[CONFIRMED_STATUS] += 1
                confirmed_by_fp[fp] += 1
                if len(confirmed_examples) < 25:
                    confirmed_examples.append(
                        {
                            "entry_id": new_row.get("entry_id"),
                            "fingerprint_id": fp,
                            "pdb_id": confirmation["pdb_id"],
                            "cofactor_comp_ids_present": confirmation[
                                "cofactor_comp_ids_present"
                            ],
                        }
                    )
            structure["holo_pdb_confirmation"] = confirmation
            out_rows.append(new_row)
    finally:
        if staging_ctx is not None:
            staging_ctx.cleanup()

    if cache_path is not None:
        _flush_cache()

    rows_confirmed_after = sum(
        1
        for row in out_rows
        if _structure_provenance(row).get("holo_pdb_confirmation", {}).get("status")
        == CONFIRMED_STATUS
    )

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_preview_pending_explicit_registry_write",
        "what": (
            "confirm HOLO experimental-PDB coordinates for chemistry-corroborated bronze "
            "labels and record evidence.structure_provenance.holo_pdb_confirmation "
            "(pdb_id + cofactor comp ids present + sha256); the mmCIFs are regeneratable "
            "from the PDB id and are NOT committed; structure is review-only mechanism "
            "context (a bronze->silver signal), never a predictive feature"
        ),
        "policy": {
            "candidate_definition": (
                "bronze seed label whose chemistry independently corroborates its "
                "fingerprint (nearest centroid == assigned AND own cohesion >= "
                f"{cohesion_threshold}) and that carries experimental pdb_ids + an "
                "annotated cofactor"
            ),
            "holo_test": (
                "the annotated cofactor's PDB HETATM comp id is present in the experimental "
                "coordinates -- the SAME test bronze_silver_promotion_preview uses"
            ),
            "cohesion_threshold": cohesion_threshold,
        },
        "guardrails": {
            "frozen_current702_benchmark_preserved": True,
            "writes_expansion_registry_only": True,
            "row_count_unchanged": len(out_rows) == len(expansion_payload),
            "large_cifs_never_committed": True,
            "coordinate_regeneratable_from_pdb_id": True,
            "existing_structure_provenance_preserved_additive": True,
            "structure_is_review_only_not_predictive_feature": True,
            "candidate_selection_is_leakage_safe_chemistry_only": True,
        },
        "counts": {
            "expansion_labels": len(expansion_payload),
            "seed_labels": len(seed),
            "holo_confirmed_this_run": counts["holo_confirmed"],
            "already_confirmed": counts["already_confirmed"],
            "no_holo_pdb_found": counts["no_holo_pdb_found"],
            "not_chemistry_corroborated": counts["not_chemistry_corroborated"],
            "no_pdb_or_cofactor": counts["no_pdb_or_cofactor"],
            "deferred_over_limit": counts["deferred_over_limit"],
            "deferred_over_fingerprint_cap": counts["deferred_over_fingerprint_cap"],
            "rows_fetched_this_run": fetched_rows,
            "rows_holo_confirmed_after": rows_confirmed_after,
        },
        "status_counts": dict(sorted(status_counts.items(), key=lambda kv: str(kv[0]))),
        "holo_confirmed_by_fingerprint": dict(sorted(confirmed_by_fp.items())),
        "holo_confirmed_examples": confirmed_examples,
        "next_action": (
            "Review counts, then re-run with --apply to write "
            "data/registries/external_bronze_labels.json (frozen current702 never written, "
            "sha printed before/after; row count unchanged; only "
            "evidence.structure_provenance.holo_pdb_confirmation added). The confirmed rows "
            "become silver_ready_pending_geometry_run in the promotion preview -- still "
            "pending the SEPARATE authorized geometry-confirmation run. Use --limit / "
            "--per-fingerprint-cap for chunked runs; the cache makes re-runs resumable."
        ),
        "promoted_registry": out_rows,
    }


def summarize_promotion(audit: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in audit.items() if key != "promoted_registry"}


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Holo Structure Promotion — experimental-PDB cofactor confirmation "
        "(non-destructive preview)",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Supplies the missing HOLO signal the bronze->silver gate needs. AlphaFold "
        "predictions are apo (no cofactor), so silver_ready was stuck at 0; this confirms "
        "the annotated cofactor IS present in an EXPERIMENTAL PDB for chemistry-corroborated "
        "labels, recording a sha-pinned holo_pdb_confirmation. The mmCIFs are regeneratable "
        "from the PDB id and are NOT committed. Structure is review-only mechanism context.",
        "",
        f"- Seed labels: {c['seed_labels']}.",
        f"- **Holo confirmed this run: {c['holo_confirmed_this_run']}** "
        f"(already confirmed {c['already_confirmed']}; total after "
        f"{c['rows_holo_confirmed_after']}).",
        f"- No holo PDB found: {c['no_holo_pdb_found']}; not corroborated: "
        f"{c['not_chemistry_corroborated']}; no pdb/cofactor: {c['no_pdb_or_cofactor']}.",
        f"- Deferred (limit/cap): {c['deferred_over_limit']}/"
        f"{c['deferred_over_fingerprint_cap']}; rows fetched this run: "
        f"{c['rows_fetched_this_run']}.",
        "",
        "## Holo confirmed by fingerprint",
        "",
        "| fingerprint | confirmed |",
        "| --- | --- |",
    ]
    for fp, n in audit["holo_confirmed_by_fingerprint"].items():
        lines.append(f"| {fp} | {n} |")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            f"- Frozen current702 preserved: "
            f"{audit['guardrails']['frozen_current702_benchmark_preserved']}.",
            f"- Writes expansion registry only: "
            f"{audit['guardrails']['writes_expansion_registry_only']}.",
            f"- Row count unchanged: {audit['guardrails']['row_count_unchanged']}.",
            "- Large mmCIFs never committed; coordinate regeneratable from PDB id; existing "
            "structure_provenance preserved (additive); structure review-only, not predictive.",
            "",
            "## Next action",
            "",
            f"- {audit['next_action']}",
            "",
        ]
    )
    return "\n".join(lines)


def write_holo_structure_promotion(
    *,
    out_path: Path = DEFAULT_OUT,
    report_path: Path | None = DEFAULT_REPORT,
    expansion_registry_path: Path = EXPANSION_REGISTRY_PATH,
    frozen_benchmark_path: Path = FROZEN_BENCHMARK_PATH,
    apply: bool = False,
    cache_path: Path | None = DEFAULT_CACHE_PATH,
    limit: int | None = None,
    per_fingerprint_cap: int | None = None,
    cohesion_threshold: float = DEFAULT_PROMOTION_COHESION,
) -> dict[str, Any]:
    """Build the holo confirmation, write summary + report, and (only on apply) registry."""
    expansion_path = Path(expansion_registry_path)
    frozen_path = Path(frozen_benchmark_path)
    if expansion_path.resolve() == frozen_path.resolve():
        raise ValueError(
            "refusing to promote: expansion registry path resolves to the frozen "
            "current702 benchmark, which is never written"
        )

    frozen_sha_before = (
        hashlib.sha256(frozen_path.read_bytes()).hexdigest() if frozen_path.exists() else None
    )

    expansion_payload = (
        json.loads(expansion_path.read_text(encoding="utf-8")) if expansion_path.exists() else []
    )
    audit = build_holo_structure_promotion(
        expansion_payload=expansion_payload,
        cache_path=cache_path,
        limit=limit,
        per_fingerprint_cap=per_fingerprint_cap,
        cohesion_threshold=cohesion_threshold,
    )

    summary = summarize_promotion(audit)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")

    summary["frozen_sha256_before"] = frozen_sha_before
    summary["expansion_registry_written"] = False
    summary["frozen_benchmark_registry_written"] = False
    if apply:
        promoted = audit["promoted_registry"]
        if len(promoted) != len(expansion_payload):
            raise ValueError(
                "row-count guard tripped: promoted registry length "
                f"{len(promoted)} != input {len(expansion_payload)}"
            )
        from .labels import MechanismLabel  # local import avoids a module cycle

        for label in promoted:
            MechanismLabel.from_dict(label)
        expansion_path.write_text(_dump_registry(promoted), encoding="utf-8")
        summary["expansion_registry_written"] = True
        summary["expansion_registry_path"] = str(expansion_path)

    summary["frozen_sha256_after"] = (
        hashlib.sha256(frozen_path.read_bytes()).hexdigest() if frozen_path.exists() else None
    )
    summary["frozen_benchmark_byte_unchanged"] = (
        summary["frozen_sha256_before"] == summary["frozen_sha256_after"]
    )
    return summary
