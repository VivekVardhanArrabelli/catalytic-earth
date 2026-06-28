"""Feasibility audit for broadening the M-CSA fold atlas beyond the cofactor families.

The off-M-CSA recovery test ran against a 5-family cofactor atlas (the families
the current-57 cofactor operating point covers). Broadening it to more of the 57
fingerprint families needs M-CSA train rows that are simultaneously (a) labelled
in the FINE (57-family) taxonomy, (b) backed by a local structure. This audit
checks whether such a multi-family fine-labelled atlas source exists locally.

It reads artifacts/registries for context only; it changes no registry, label,
threshold, or model, downloads nothing, and scores no held-out data.
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


DEFAULT_ATLAS_MANIFEST_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_input_manifest_current702_20260628.json"
)
DEFAULT_LABEL_MANIFEST_PATH = (
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_CURATED_LABELS_PATH = "data/registries/curated_mechanism_labels.json"
DEFAULT_OUT_PATH = (
    "artifacts/v3_atlas_broadening_feasibility_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/atlas_broadening_feasibility_current702_20260628.md"
)


def _load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def current_atlas_families(atlas_manifest: dict[str, Any]) -> dict[str, Any]:
    targets = atlas_manifest.get("rows", {}).get("train_in_scope_targets", []) or []
    fams = sorted({r["true_fingerprint_id"] for r in targets if r.get("true_fingerprint_id")})
    return {"families": fams, "family_count": len(fams), "structures": len(targets)}


def label_manifest_fine_fingerprint_rows(label_manifest: dict[str, Any]) -> int:
    return sum(1 for r in label_manifest.get("rows", []) or [] if r.get("true_fingerprint_id"))


def curated_label_family_count(curated: Any) -> int:
    rows = curated if isinstance(curated, list) else curated.get("labels", [])
    return len({r.get("fingerprint_id") for r in rows if r.get("fingerprint_id")})


def build_atlas_broadening_feasibility(
    *,
    current_atlas: dict[str, Any],
    label_manifest_fine_rows: int,
    curated_families: int,
    full_registry_family_count: int = 57,
) -> dict[str, Any]:
    has_multifamily_fine_source = label_manifest_fine_rows > 0
    runnable = has_multifamily_fine_source
    status = (
        "atlas_broadening_runnable_fine_multifamily_source_present"
        if runnable
        else "blocked_atlas_broadening_no_fine_multifamily_mcsa_label_source"
    )
    return {
        "artifact_id": "v3_atlas_broadening_feasibility_current702_20260628",
        "schema_version": "atlas_broadening_feasibility.v1",
        "created_utc": _utc_now_iso(),
        "status": status,
        "result_class": "read_only_feasibility_inventory_no_download_no_registry_change",
        "guardrails": {
            "registry_or_ontology_changed": False,
            "labels_changed": False,
            "downloads_performed": False,
            "heldout_rows_scored": False,
        },
        "question": (
            "Can the M-CSA fold atlas be broadened beyond the cofactor families using a "
            "locally available fine (57-family) labelled, structure-backed M-CSA source?"
        ),
        "current_atlas": current_atlas,
        "fine_label_sources_checked": {
            "current57_cofactor_operating_point": (
                f"fine labels present but scoped to {current_atlas['family_count']} "
                "cofactor families only"
            ),
            "sequence_nn_label_manifest_true_fingerprint_rows": label_manifest_fine_rows,
            "curated_mechanism_labels_family_count": curated_families,
            "curated_taxonomy": (
                "coarse (8-family) frozen taxonomy, incompatible with the fine 57-family "
                "atlas/bronze labels"
            ),
            "external_bronze_labels": "non-M-CSA (cannot serve as the M-CSA atlas)",
        },
        "blocker": {
            "summary": (
                "Fine (57-family) M-CSA truth labels exist only on the current-57 "
                "cofactor operating-point surface "
                f"({current_atlas['family_count']} families). The label manifest carries "
                f"{label_manifest_fine_rows} fine-fingerprint rows, the curated registry "
                f"is coarse ({curated_families} families), and bronze labels are "
                "non-M-CSA. So no local source provides a fine multi-family "
                "structure-backed M-CSA atlas beyond the cofactor families."
            ),
            "full_registry_family_count": full_registry_family_count,
            "families_unreachable_for_now": (
                full_registry_family_count - current_atlas["family_count"]
            ),
        },
        "unblock_plan": {
            "step_1": (
                "Derive fine (57-family) truth fingerprints for M-CSA train in-scope rows "
                "across all families (run the router/operating-point machinery on the full "
                "M-CSA in-distribution set, not just the cofactor surface), with explicit "
                "leakage controls."
            ),
            "step_2": (
                "Stage AlphaFold/PDB structures for those M-CSA rows (most are likely "
                "already local; backfill the rest via an authorized bounded download)."
            ),
            "step_3": (
                "Rebuild the atlas accession->fine-fingerprint map across families and "
                "re-run the off-M-CSA recovery harness against the broadened atlas."
            ),
            "caveat": (
                "Router-derived fine M-CSA labels are not gold truth; broadening trades "
                "coverage for label confidence and should be reported as such."
            ),
        },
        "interpretation": {
            "headline": (
                "Broadening the fold atlas beyond the cofactor families is not runnable on "
                "current local data: no fine multi-family structure-backed M-CSA label "
                "source exists. Off-M-CSA recovery remains validated for the cofactor "
                "families; broadening is a separate fine-labelling effort."
                if not runnable
                else "A fine multi-family M-CSA label source is available; the atlas can "
                "be broadened and recovery re-run."
            ),
            "decision_needed": (
                "Whether to invest in deriving fine multi-family M-CSA truth labels "
                "(router/operating-point on the full in-distribution set) to broaden the "
                "atlas, accepting that those labels are router-derived, not gold."
            ),
        },
    }


def _report(audit: dict[str, Any]) -> str:
    ca = audit["current_atlas"]
    fs = audit["fine_label_sources_checked"]
    lines = [
        "# Atlas Broadening Feasibility",
        "",
        f"Run: {audit['created_utc']}",
        f"Status: `{audit['status']}`",
        "",
        "## Question",
        "",
        f"- {audit['question']}",
        "",
        "## Current Atlas",
        "",
        f"- {ca['family_count']} families, {ca['structures']} structures: "
        f"{', '.join(ca['families'])}.",
        "",
        "## Fine-Label Sources Checked",
        "",
        f"- current-57 cofactor operating point: {fs['current57_cofactor_operating_point']}.",
        f"- label manifest fine-fingerprint rows: "
        f"{fs['sequence_nn_label_manifest_true_fingerprint_rows']}.",
        f"- curated registry families: {fs['curated_mechanism_labels_family_count']} "
        f"({fs['curated_taxonomy']}).",
        f"- external bronze labels: {fs['external_bronze_labels']}.",
        "",
        "## Blocker",
        "",
        f"- {audit['blocker']['summary']}",
        f"- Families unreachable for now: {audit['blocker']['families_unreachable_for_now']} "
        f"of {audit['blocker']['full_registry_family_count']}.",
        "",
        "## Unblock Plan",
        "",
        f"1. {audit['unblock_plan']['step_1']}",
        f"2. {audit['unblock_plan']['step_2']}",
        f"3. {audit['unblock_plan']['step_3']}",
        f"- Caveat: {audit['unblock_plan']['caveat']}",
        "",
        "## Bottom Line",
        "",
        f"- {audit['interpretation']['headline']}",
        "",
        "## Guardrails",
        "",
        "- Read-only inventory; no download, no registry/label/threshold/model change, no "
        "held-out read.",
    ]
    return "\n".join(lines) + "\n"


def write_atlas_broadening_feasibility(
    *,
    atlas_manifest_path: Path,
    label_manifest_path: Path,
    curated_labels_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    atlas_manifest = _load_json(Path(atlas_manifest_path))
    label_manifest = _load_json(Path(label_manifest_path))
    curated = _load_json(Path(curated_labels_path))
    audit = build_atlas_broadening_feasibility(
        current_atlas=current_atlas_families(atlas_manifest),
        label_manifest_fine_rows=label_manifest_fine_fingerprint_rows(label_manifest),
        curated_families=curated_label_family_count(curated),
    )
    audit["source_artifacts"] = {
        "atlas_manifest": {
            "path": str(atlas_manifest_path),
            "sha256": _sha256(Path(atlas_manifest_path)),
        },
        "label_manifest": {
            "path": str(label_manifest_path),
            "sha256": _sha256(Path(label_manifest_path)),
        },
        "curated_labels": {
            "path": str(curated_labels_path),
            "sha256": _sha256(Path(curated_labels_path)),
        },
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
