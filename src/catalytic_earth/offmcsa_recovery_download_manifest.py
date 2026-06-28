"""Download manifest for the off-M-CSA in-scope recovery test (sign-off, no fetch).

The off-M-CSA recovery readout is blocked only by the absence of structures for
trusted non-M-CSA positives. This builds the bounded, reviewable download plan:
the exact trusted bronze-admitted positives (high confidence, label in a family
present in the M-CSA train atlas, non-M-CSA, not already structured locally),
each with its AlphaFold CIF URL, family coverage, and a size estimate. It
performs no download; fetching is a separately authorized step that must respect
the >=10 GiB free-disk floor.

Non-circularity: bronze admission used sequence/cofactor evidence, never
structure, so fold-NN retrieval against the M-CSA atlas is an independent channel
for these rows. Bronze labels here are evaluation targets only, never features.
"""

from __future__ import annotations

import glob
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BRONZE_SHARD_GLOB = "data/registries/external_bronze_labels.shards/*.json"
DEFAULT_ATLAS_MANIFEST_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_input_manifest_current702_20260628.json"
)
DEFAULT_LABEL_MANIFEST_PATH = (
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_COORDINATE_GLOB = "artifacts/*coordinates*"
DEFAULT_OUT_PATH = (
    "artifacts/v3_offmcsa_recovery_download_manifest_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/offmcsa_recovery_download_manifest_current702_20260628.md"
)

# Trusted-positive selection (documented, frozen). bronze rows must be high
# confidence, in-scope (not out_of_scope), in a family the M-CSA atlas can recover.
SELECTION = {
    "confidence": "high",
    "exclude_label_type": "out_of_scope",
    "require_fingerprint_in_atlas_families": True,
    "exclude_mcsa_accessions": True,
    "exclude_already_structured_locally": True,
}
AFDB_URL_TEMPLATE = "https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v4.cif"
# Rough AFDB CIF size for a size estimate (actual confirmed at fetch time).
ESTIMATED_MB_PER_CIF = 0.6
DISK_FLOOR_GIB = 10


def _load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _accession_from_entry(entry_id: str) -> str:
    return entry_id.split(":", 1)[1] if ":" in entry_id else entry_id


def atlas_families(atlas_manifest: dict[str, Any]) -> set[str]:
    return {
        r["true_fingerprint_id"]
        for r in atlas_manifest.get("rows", {}).get("train_in_scope_targets", []) or []
        if r.get("true_fingerprint_id")
    }


def mcsa_accessions(label_manifest: dict[str, Any]) -> set[str]:
    accs: set[str] = set()
    for row in label_manifest.get("rows", []) or []:
        if row.get("sequence_id"):
            accs.add(str(row["sequence_id"]))
        for value in row.get("real_sequence_accessions") or []:
            accs.add(str(value))
    return accs


def locally_structured_accessions(coordinate_glob: str) -> set[str]:
    accs: set[str] = set()
    for directory in glob.glob(coordinate_glob):
        for cif in glob.glob(os.path.join(directory, "*.cif")):
            base = os.path.basename(cif).replace("AF-", "").replace("afdb_", "").replace("pdb_", "")
            match = re.match(r"([A-Za-z0-9]+)", base)
            if match:
                accs.add(match.group(1))
    return accs


def select_trusted_positives(
    *,
    bronze_rows: list[dict[str, Any]],
    families: set[str],
    mcsa: set[str],
    structured: set[str],
) -> list[dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    for row in bronze_rows:
        fingerprint = row.get("fingerprint_id")
        if not fingerprint or fingerprint not in families:
            continue
        if row.get("label_type") == SELECTION["exclude_label_type"]:
            continue
        if row.get("confidence") != SELECTION["confidence"]:
            continue
        accession = _accession_from_entry(str(row.get("entry_id", "")))
        if not accession or accession in mcsa or accession in structured:
            continue
        if accession in selected:
            continue
        selected[accession] = {
            "entry_id": row.get("entry_id"),
            "accession": accession,
            "true_fingerprint_id": fingerprint,
            "confidence": row.get("confidence"),
            "alphafold_cif_url": AFDB_URL_TEMPLATE.format(accession=accession),
        }
    return sorted(selected.values(), key=lambda r: r["accession"])


def build_offmcsa_recovery_download_manifest(
    *,
    selected: list[dict[str, Any]],
    families: set[str],
) -> dict[str, Any]:
    from collections import Counter

    family_coverage = Counter(r["true_fingerprint_id"] for r in selected)
    canonical = json.dumps(
        [r["accession"] for r in selected], sort_keys=True, separators=(",", ":")
    )
    estimated_mb = round(len(selected) * ESTIMATED_MB_PER_CIF, 1)
    return {
        "artifact_id": "v3_offmcsa_recovery_download_manifest_current702_20260628",
        "schema_version": "offmcsa_recovery_download_manifest.v1",
        "created_utc": _utc_now_iso(),
        "status": "download_manifest_ready_awaiting_authorization",
        "result_class": "bounded_download_plan_no_fetch_no_registry_change",
        "guardrails": {
            "downloads_performed": False,
            "fetch_requires_explicit_authorization": True,
            "min_free_disk_gib_required": DISK_FLOOR_GIB,
            "bronze_labels_are_evaluation_targets_only": True,
            "fold_recovery_is_non_circular_admission_used_sequence_cofactor_not_structure": True,
            "registry_or_ontology_changed": False,
            "labels_changed": False,
        },
        "selection_criteria": SELECTION,
        "atlas_families": sorted(families),
        "summary": {
            "selected_structures_to_download": len(selected),
            "families_covered": len(family_coverage),
            "family_coverage": dict(family_coverage.most_common()),
            "estimated_total_mb": estimated_mb,
            "accession_list_sha256": hashlib.sha256(
                canonical.encode("utf-8")
            ).hexdigest(),
        },
        "downloads": selected,
        "fetch_procedure": [
            "Confirm >= 10 GiB free (df -h .).",
            "For each downloads[].alphafold_cif_url, fetch to a staging dir as "
            "afdb_{accession}_v4.cif (skip-if-exists; stop if disk would fall below "
            "the floor).",
            "foldseek easy-search the staged positives vs the M-CSA train in-scope "
            "atlas (artifacts/v3_current57_fold_tm_recompute_current702_20260628_"
            "coordinates/train_in_scope_atlas) with the same flags as the calibration "
            "recompute.",
            "Build the off-M-CSA positive map {rows:[{entry_id,accession,"
            "true_fingerprint_id}]} from downloads, then run "
            "build-fold-nn-mechanism-recovery-readout --positives <map> --foldseek-tsv "
            "<tsv> --surface-label offmcsa_bronze_high_confidence, and compare to the "
            "28/35 (0.80) M-CSA baseline.",
        ],
        "interpretation": {
            "headline": (
                f"Bounded plan: download {len(selected)} AlphaFold CIFs for trusted "
                f"high-confidence non-M-CSA bronze positives across "
                f"{len(family_coverage)} atlas families (~{estimated_mb} MB), to measure "
                f"off-M-CSA in-scope fold-NN recovery against the M-CSA baseline."
            ),
            "decision_needed": (
                "Authorize the bounded AlphaFold download (no other gate); fetching is "
                "not performed by this manifest."
            ),
        },
    }


def _report(manifest: dict[str, Any]) -> str:
    s = manifest["summary"]
    lines = [
        "# Off-M-CSA Recovery Download Manifest (sign-off)",
        "",
        f"Run: {manifest['created_utc']}",
        f"Status: `{manifest['status']}`",
        "",
        "## Plan",
        "",
        f"- Structures to download: **{s['selected_structures_to_download']}** AlphaFold "
        f"CIFs (~{s['estimated_total_mb']} MB est.).",
        f"- Atlas families recoverable: {', '.join(manifest['atlas_families'])}.",
        f"- Family coverage of the sample:",
    ]
    for fam, n in s["family_coverage"].items():
        lines.append(f"  - {fam}: {n}")
    lines += [
        f"- Accession-list sha256: `{s['accession_list_sha256']}`.",
        "",
        "## Selection Criteria",
        "",
        "- High confidence; in-scope (not out_of_scope); fingerprint in an M-CSA atlas "
        "family; non-M-CSA accession; not already structured locally.",
        "",
        "## Fetch Procedure (authorized step, not done here)",
        "",
    ]
    for i, step in enumerate(manifest["fetch_procedure"], 1):
        lines.append(f"{i}. {step}")
    lines += [
        "",
        "## Decision Needed",
        "",
        f"- {manifest['interpretation']['decision_needed']}",
        "",
        "## Guardrails",
        "",
        "- No download performed; fetch requires explicit authorization and >= 10 GiB free.",
        "- Bronze labels are evaluation targets only (admission used sequence/cofactor, "
        "not structure, so fold-NN recovery is non-circular).",
        "- No registry, ontology, or label change.",
    ]
    return "\n".join(lines) + "\n"


def write_offmcsa_recovery_download_manifest(
    *,
    bronze_shard_glob: str = DEFAULT_BRONZE_SHARD_GLOB,
    atlas_manifest_path: Path,
    label_manifest_path: Path,
    coordinate_glob: str = DEFAULT_COORDINATE_GLOB,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    atlas_manifest = _load_json(atlas_manifest_path)
    label_manifest = _load_json(label_manifest_path)
    families = atlas_families(atlas_manifest)
    mcsa = mcsa_accessions(label_manifest)
    structured = locally_structured_accessions(coordinate_glob)

    bronze_rows: list[dict[str, Any]] = []
    for shard in sorted(glob.glob(bronze_shard_glob)):
        data = _load_json(Path(shard))
        rows = data if isinstance(data, list) else next(
            (v for v in data.values() if isinstance(v, list)), []
        )
        bronze_rows.extend(rows)

    selected = select_trusted_positives(
        bronze_rows=bronze_rows, families=families, mcsa=mcsa, structured=structured
    )
    manifest = build_offmcsa_recovery_download_manifest(
        selected=selected, families=families
    )
    manifest["source_artifacts"] = {
        "bronze_shard_glob": bronze_shard_glob,
        "bronze_rows_scanned": len(bronze_rows),
        "atlas_manifest_id": atlas_manifest.get("artifact_id"),
        "label_manifest_id": label_manifest.get("artifact_id"),
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(manifest), encoding="utf-8")
    return manifest
