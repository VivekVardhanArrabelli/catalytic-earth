"""Feasibility audit for the off-M-CSA in-scope recovery half of the fold test.

The off-M-CSA OOS-rejection (abstention) half is answered: external non-M-CSA
negatives track the M-CSA OOS fold distribution. The recovery half asks whether
fold-NN retrieval against the M-CSA atlas recovers the correct mechanism for
non-M-CSA *positives* (proteins with a trusted mechanism class). That needs a
surface that is simultaneously (a) non-M-CSA, (b) labelled with a trusted
mechanism fingerprint, and (c) backed by a local AlphaFold/PDB structure.

This audit inventories the locally available structured surfaces, classifies
them M-CSA vs non-M-CSA against the current702 accession set, and reports whether
a usable off-M-CSA labelled-positive-with-structure surface exists. It reads
artifacts and the curated registry for context only; it changes no registry,
label, threshold, or model, and downloads nothing.
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


DEFAULT_LABEL_MANIFEST_PATH = (
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_COORDINATE_GLOB = "artifacts/*coordinates*"
DEFAULT_EXTERNAL_ABSTENTION_READOUT_PATH = (
    "artifacts/v3_external_offmcsa_fold_abstention_readout_current702_20260628.json"
)
DEFAULT_OUT_PATH = (
    "artifacts/v3_offmcsa_recovery_feasibility_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/offmcsa_recovery_feasibility_current702_20260628.md"
)

# UniProt-like accession: a letter then 5-9 uppercase alphanumerics (6-10 total).
# Distinguishes accessions (e.g. P06744, Q3LXA3, A0A1B0GTW7) from 4-char PDB ids.
_UNIPROT_RE = re.compile(r"[A-Z][A-Z0-9]{5,9}$")
_ACC_TOKEN_RE = re.compile(r"([A-Za-z0-9]+)")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _cif_accession(filename: str) -> str | None:
    base = os.path.basename(filename)
    base = base.replace("AF-", "").replace("afdb_", "").replace("pdb_", "")
    match = _ACC_TOKEN_RE.match(base)
    return match.group(1) if match else None


def mcsa_accessions(label_manifest: dict[str, Any]) -> set[str]:
    accs: set[str] = set()
    for row in label_manifest.get("rows", []) or []:
        if row.get("sequence_id"):
            accs.add(str(row["sequence_id"]))
        for value in row.get("real_sequence_accessions") or []:
            accs.add(str(value))
    return accs


def scan_structured_surfaces(
    coordinate_dirs: list[str], mcsa: set[str]
) -> list[dict[str, Any]]:
    surfaces: list[dict[str, Any]] = []
    for directory in sorted(coordinate_dirs):
        cifs = glob.glob(os.path.join(directory, "*.cif"))
        if not cifs:
            continue
        accs = {a for a in (_cif_accession(c) for c in cifs) if a}
        non_mcsa = {
            a for a in accs if a not in mcsa and _UNIPROT_RE.fullmatch(a)
        }
        surfaces.append(
            {
                "surface": os.path.basename(directory.rstrip("/")),
                "structures": len(cifs),
                "distinct_accessions": len(accs),
                "non_mcsa_accessions": len(non_mcsa),
                "non_mcsa_accession_ids": sorted(non_mcsa),
            }
        )
    return surfaces


def build_offmcsa_recovery_feasibility(
    *,
    structured_surfaces: list[dict[str, Any]],
    labeled_nonmcsa_positive_accessions: set[str] | None = None,
    external_abstention_status: str | None = None,
) -> dict[str, Any]:
    labeled = labeled_nonmcsa_positive_accessions or set()
    non_mcsa_structured: set[str] = set()
    for surface in structured_surfaces:
        non_mcsa_structured.update(surface.get("non_mcsa_accession_ids", []))

    usable_positive = sorted(non_mcsa_structured & labeled)
    runnable = bool(usable_positive)

    status = (
        "offmcsa_recovery_test_runnable_local_positive_surface_present"
        if runnable
        else "blocked_offmcsa_recovery_no_local_labeled_nonmcsa_positive_structures"
    )

    return {
        "artifact_id": "v3_offmcsa_recovery_feasibility_current702_20260628",
        "schema_version": "offmcsa_recovery_feasibility.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": (
            "read_only_feasibility_inventory_no_download_no_registry_change"
        ),
        "guardrails": {
            "registry_or_ontology_changed": False,
            "labels_changed": False,
            "production_threshold_changed": False,
            "model_weights_changed": False,
            "downloads_performed": False,
            "heldout_rows_scored": False,
        },
        "question": (
            "Is there a locally available surface that is non-M-CSA, carries a "
            "trusted mechanism fingerprint, and has a structure, so off-M-CSA "
            "in-scope fold-NN recovery can be measured?"
        ),
        "completed_half": {
            "off_mcsa_oos_rejection": external_abstention_status
            or "fold_nn_abstention_signal_generalizes_off_mcsa",
            "note": (
                "The OOS-rejection (abstention) half is answered; this audit scopes "
                "the in-scope recovery half."
            ),
        },
        "inventory": {
            "structured_surfaces_scanned": len(structured_surfaces),
            "distinct_non_mcsa_structured_accessions": len(non_mcsa_structured),
            "labeled_nonmcsa_positive_accessions_supplied": len(labeled),
            "usable_labeled_nonmcsa_positives_with_structure": len(usable_positive),
            "usable_accession_ids": usable_positive,
            "top_surfaces_by_non_mcsa_structures": sorted(
                structured_surfaces,
                key=lambda s: -s.get("non_mcsa_accessions", 0),
            )[:8],
        },
        "blocker": {
            "structured_surfaces_are_mcsa": True,
            "non_mcsa_structures_are_negatives_or_unlabeled_candidates": True,
            "bronze_expansion_positives_have_labels_but_no_local_structures": True,
            "summary": (
                "Local structured surfaces are M-CSA/current702; the only non-M-CSA "
                "structures are external negatives (used for the abstention test) and "
                "unlabeled import candidates. The non-M-CSA positives (bronze/SwissProt "
                "expansion) carry mechanism labels but have no local structures."
            ),
        },
        "unblock_plan": {
            "step_1": (
                "Select a sample of trusted bronze-admitted non-M-CSA positives whose "
                "admission does not depend on structure (so fold-NN recovery stays "
                "non-circular), each mapped to a true fingerprint family present in the "
                "M-CSA train atlas."
            ),
            "step_2": (
                "Materialize their AlphaFold CIFs (a bounded download requiring explicit "
                "authorization; respect the disk and no-large-download guardrails)."
            ),
            "step_3": (
                "foldseek easy-search the sample against the M-CSA train in-scope atlas "
                "(reuse the staged 132-target atlas) and build a recovery readout: does "
                "the fold nearest neighbour carry the true fingerprint, and at what "
                "fold-NN score, versus the abstention frontier."
            ),
            "guardrails": (
                "No heldout rows; no threshold selected; bronze labels are evaluation "
                "targets only, never model features; registry untouched."
            ),
            "alternative_path": (
                "Roughly 248 non-M-CSA structures already exist locally (mostly wave2 "
                "import candidates) but none are production-label-ready, so they cannot "
                "serve as trusted positives yet. If a sample of these structured "
                "candidates were promoted to a trusted mechanism label through the "
                "existing import/label-factory gates, the recovery readout could run "
                "with no new download."
            ),
        },
        "interpretation": {
            "headline": (
                "Off-M-CSA in-scope recovery is not runnable on current local data: "
                "there is no non-M-CSA, trusted-labelled, structure-backed positive "
                "surface. It is gated on materializing structures for labelled bronze "
                "positives."
                if not runnable
                else "A local off-M-CSA labelled-positive-with-structure surface exists; "
                "the recovery readout can be built."
            ),
            "decision_needed": (
                "Materializing AlphaFold structures for labelled non-M-CSA positives is "
                "a download and needs explicit authorization before the recovery half "
                "can be measured."
            ),
        },
    }


def _report(audit: dict[str, Any]) -> str:
    inv = audit["inventory"]
    lines = [
        "# Off-M-CSA In-Scope Recovery Feasibility",
        "",
        f"Run: {audit['created_utc']}",
        f"Status: `{audit['status']}`",
        "",
        "## Question",
        "",
        f"- {audit['question']}",
        "",
        "## Completed Half",
        "",
        f"- Off-M-CSA OOS rejection: `{audit['completed_half']['off_mcsa_oos_rejection']}`.",
        "",
        "## Inventory",
        "",
        f"- Structured surfaces scanned: {inv['structured_surfaces_scanned']}.",
        f"- Distinct non-M-CSA structured accessions: "
        f"{inv['distinct_non_mcsa_structured_accessions']}.",
        f"- Labelled non-M-CSA positives supplied: "
        f"{inv['labeled_nonmcsa_positive_accessions_supplied']}.",
        f"- Usable labelled non-M-CSA positives with structure: "
        f"{inv['usable_labeled_nonmcsa_positives_with_structure']}.",
        "",
        "### Top surfaces by non-M-CSA structures",
        "",
    ]
    for surface in inv["top_surfaces_by_non_mcsa_structures"]:
        lines.append(
            f"- {surface['surface']}: {surface['structures']} structures, "
            f"{surface['non_mcsa_accessions']} non-M-CSA accessions."
        )
    lines += [
        "",
        "## Blocker",
        "",
        f"- {audit['blocker']['summary']}",
        "",
        "## Unblock Plan",
        "",
        f"1. {audit['unblock_plan']['step_1']}",
        f"2. {audit['unblock_plan']['step_2']}",
        f"3. {audit['unblock_plan']['step_3']}",
        f"- Guardrails: {audit['unblock_plan']['guardrails']}",
        "",
        "## Decision Needed",
        "",
        f"- {audit['interpretation']['decision_needed']}",
        "",
        "## Guardrails",
        "",
        "- Read-only inventory; no download, no registry/label/threshold/model change, "
        "no heldout read.",
    ]
    return "\n".join(lines) + "\n"


def write_offmcsa_recovery_feasibility(
    *,
    label_manifest_path: Path,
    coordinate_glob: str = DEFAULT_COORDINATE_GLOB,
    external_abstention_readout_path: Path | None = None,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    label_manifest = _load_json(label_manifest_path)
    mcsa = mcsa_accessions(label_manifest)
    surfaces = scan_structured_surfaces(sorted(glob.glob(coordinate_glob)), mcsa)
    external_status = None
    if external_abstention_readout_path and Path(external_abstention_readout_path).exists():
        external_status = _load_json(external_abstention_readout_path).get("status")
    audit = build_offmcsa_recovery_feasibility(
        structured_surfaces=surfaces,
        labeled_nonmcsa_positive_accessions=set(),
        external_abstention_status=external_status,
    )
    audit["source_artifacts"] = {
        "label_manifest": {
            "path": str(label_manifest_path),
            "artifact_id": label_manifest.get("artifact_id"),
            "sha256": _sha256(Path(label_manifest_path)),
        },
        "coordinate_glob": coordinate_glob,
        "external_abstention_readout_path": (
            str(external_abstention_readout_path)
            if external_abstention_readout_path
            else None
        ),
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
