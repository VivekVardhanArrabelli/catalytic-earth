"""Option B: a NEW, untouched held-out to validate a repaired fine-57 router.

Gate 1 found the current-57 fine router misroutes non-metal (flavin/heme/PLP)
enzymes into metal v2-subclass fingerprints. Option B is to repair that, then
validate on a fresh held-out. But the M-CSA held-out is SPENT (only ~14 rows
remain, 1 in-scope), so a fresh M-CSA held-out is not available.

This freezes the next best leakage-safe validation vehicle, BEFORE any router
fix: the untouched, high-confidence, atlas-family, non-M-CSA bronze positives
that were NOT used anywhere in development (disjoint from train/cal, from the
M-CSA accessions, and from the off-M-CSA recovery development set). Their
metal/non-metal split directly tests the repair's failure mode: a fixed router
must recover true mechanisms AND stop routing non-metal enzymes into metal
subclasses.

The set is enumerated and content-hashed. The pass bar is pre-committed from
first principles (a recovery floor + a non-metal-misroute ceiling), with no
held-out scoring. Honest caveats: small n, bronze (automation-curated, not gold)
labels, off-M-CSA, structures to be materialised. Executing the test is a
separate, authorised one-shot AFTER the router fix is frozen.
"""

from __future__ import annotations

import glob
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .cofactor_precision_contract import LEGACY_V1_COMPATIBILITY


DEFAULT_BRONZE_SHARD_GLOB = "data/registries/external_bronze_labels.shards/*.json"
DEFAULT_ATLAS_MANIFEST_PATH = (
    "artifacts/v3_current57_fold_tm_recompute_input_manifest_current702_20260628.json"
)
DEFAULT_LABEL_MANIFEST_PATH = (
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_RECOVERY_POSITIVE_MAP_PATH = (
    "artifacts/v3_offmcsa_recovery_bronze_positive_map_current702_20260628.json"
)
DEFAULT_RECOVERY_DOWNLOAD_MANIFEST_PATH = (
    "artifacts/v3_offmcsa_recovery_download_manifest_current702_20260628.json"
)
DEFAULT_OUT_PATH = (
    "artifacts/v3_option_b_heldout_preregistration_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/option_b_heldout_preregistration_current702_20260628.md"
)

METAL_UMBRELLA = "metal_dependent_hydrolase"
METAL_SUBCLASSES = set(LEGACY_V1_COMPATIBILITY.get(METAL_UMBRELLA, ()))

# Pre-committed pass bar (set from first principles, before any fix or scoring).
PASS_BAR = {
    "min_recovery_rate": 0.70,
    "max_nonmetal_into_metal_misroute_rate": 0.20,
    "derivation": (
        "Recovery floor mirrors the held-out one-shot bar (0.70). The non-metal "
        "misroute ceiling (0.20) targets the Gate-1 failure mode directly: on M-CSA "
        "calibration 7/8 misroutes were non-metal enzymes routed into metal subclasses; "
        "a repaired router should keep that well under 1-in-5 on never-seen non-metal "
        "positives. Both fixed before any held-out scoring."
    ),
}


def _load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _accession_from_entry(entry_id: str) -> str:
    return entry_id.split(":", 1)[1] if ":" in entry_id else entry_id


def _atlas_families(atlas_manifest: dict[str, Any]) -> set[str]:
    return {
        r["true_fingerprint_id"]
        for r in atlas_manifest.get("rows", {}).get("train_in_scope_targets", []) or []
        if r.get("true_fingerprint_id")
    }


def _mcsa_accessions(label_manifest: dict[str, Any]) -> set[str]:
    accs: set[str] = set()
    for row in label_manifest.get("rows", []) or []:
        if row.get("sequence_id"):
            accs.add(str(row["sequence_id"]))
        for value in row.get("real_sequence_accessions") or []:
            accs.add(str(value))
    return accs


def select_untouched_heldout_positives(
    *,
    bronze_rows: list[dict[str, Any]],
    families: set[str],
    mcsa: set[str],
    used_accessions: set[str],
) -> list[dict[str, Any]]:
    seen: dict[str, dict[str, Any]] = {}
    for row in bronze_rows:
        fp = row.get("fingerprint_id")
        if not fp or fp not in families:
            continue
        if row.get("label_type") == "out_of_scope":
            continue
        if row.get("confidence") != "high":
            continue
        accession = _accession_from_entry(str(row.get("entry_id", "")))
        if not accession or accession in mcsa or accession in used_accessions:
            continue
        if accession in seen:
            continue
        is_metal = fp == METAL_UMBRELLA or fp in METAL_SUBCLASSES
        seen[accession] = {
            "entry_id": row.get("entry_id"),
            "accession": accession,
            "true_fingerprint_id": fp,
            "metal_family": is_metal,
        }
    return sorted(seen.values(), key=lambda r: r["accession"])


def build_option_b_heldout_preregistration(
    *, members: list[dict[str, Any]]
) -> dict[str, Any]:
    canonical = json.dumps(
        [m["accession"] for m in members], sort_keys=True, separators=(",", ":")
    )
    metal = [m for m in members if m["metal_family"]]
    nonmetal = [m for m in members if not m["metal_family"]]
    return {
        "artifact_id": "v3_option_b_heldout_preregistration_current702_20260628",
        "schema_version": "option_b_heldout_preregistration.v1",
        "created_utc": _utc_now_iso(),
        "status": "preregistered_not_yet_run_pending_router_fix",
        "result_class": (
            "frozen_untouched_offmcsa_bronze_heldout_no_scoring_no_registry_change"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "set_is_untouched_by_development": True,
            "disjoint_from_train_cal_and_mcsa": True,
            "disjoint_from_offmcsa_recovery_development_set": True,
            "labels_are_bronze_not_gold": True,
            "structures_to_be_materialised": True,
            "pass_bar_from_first_principles_before_scoring": True,
            "registry_or_ontology_changed": False,
        },
        "why": (
            "The M-CSA held-out is spent (~14 rows left, 1 in-scope), so a repaired "
            "fine-57 router cannot be validated on a fresh M-CSA held-out. This freezes "
            "the next best untouched validation vehicle before any router fix."
        ),
        "primary_hypothesis": (
            "A repaired fine-57 router that constrains the metal v2-subclasses will, on "
            "this never-seen set, (a) recover true mechanism families at >= the bar AND "
            "(b) stop routing non-metal (flavin/heme/PLP) positives into metal subclasses "
            "(the Gate-1 failure mode)."
        ),
        "frozen_heldout_set": {
            "definition": (
                "Untouched high-confidence, atlas-family, non-M-CSA bronze positives, "
                "disjoint from train/cal, M-CSA accessions, and the off-M-CSA recovery "
                "development set. Enumerated and content-hashed."
            ),
            "members": members,
            "counts": {
                "total": len(members),
                "metal_family": len(metal),
                "non_metal_family": len(nonmetal),
            },
            "sha256": _sha256_text(canonical),
        },
        "pass_bar": PASS_BAR,
        "execution_procedure": [
            "Repair the fine-57 router on TRAIN/CAL only (constrain the metal "
            "v2-subclasses so they require metal-cofactor support; re-verify calibration "
            "recovery moves toward 30/35).",
            "Freeze the repaired-router rule (its own pre-registration / sha) BEFORE "
            "touching this held-out.",
            "Materialise AlphaFold structures for the frozen held-out accessions "
            "(bounded download; verify the sha256 first).",
            "Score the held-out once through the repaired router; compute recovery rate "
            "and non-metal-into-metal misroute rate.",
            "Compare to PASS_BAR; emit PASS/FAIL verbatim and stop. Run once.",
        ],
        "caveats": [
            f"Small n ({len(members)} positives; {len(nonmetal)} non-metal, "
            f"{len(metal)} metal) -- a focused failure-mode probe, not a high-precision "
            "estimate.",
            "Bronze labels are automation-curated (concordance, not gold truth).",
            "Off-M-CSA and structure-materialisation-gated; a deployment-grade validation "
            "would need gold-curated rows.",
        ],
        "one_shot_guardrail": (
            "Run exactly once, after the repaired-router rule is frozen. No post-hoc "
            "change to the rule, bar, or set; any re-run invalidates this pre-registration."
        ),
    }


def _report(prereg: dict[str, Any]) -> str:
    fs = prereg["frozen_heldout_set"]
    bar = prereg["pass_bar"]
    lines = [
        "# Option B: New Held-Out Pre-Registration (repaired fine-57 router)",
        "",
        f"Run: {prereg['created_utc']}",
        f"Status: `{prereg['status']}`",
        "",
        "## Why",
        "",
        f"- {prereg['why']}",
        "",
        "## Primary Hypothesis",
        "",
        f"- {prereg['primary_hypothesis']}",
        "",
        "## Frozen Held-Out Set",
        "",
        f"- {fs['definition']}",
        f"- Counts: {fs['counts']['total']} total "
        f"({fs['counts']['non_metal_family']} non-metal, "
        f"{fs['counts']['metal_family']} metal).",
        f"- Content hash (sha256): `{fs['sha256']}`.",
        "",
        "## Pre-Committed Pass Bar",
        "",
        f"- Min recovery rate: {bar['min_recovery_rate']}.",
        f"- Max non-metal-into-metal misroute rate: "
        f"{bar['max_nonmetal_into_metal_misroute_rate']}.",
        f"- Derivation: {bar['derivation']}",
        "",
        "## Execution Procedure (after the router fix, one shot)",
        "",
    ]
    for i, step in enumerate(prereg["execution_procedure"], 1):
        lines.append(f"{i}. {step}")
    lines += ["", "## Caveats", ""]
    lines += [f"- {c}" for c in prereg["caveats"]]
    lines += [
        "",
        "## One-Shot Guardrail",
        "",
        f"- {prereg['one_shot_guardrail']}",
        "",
        "## Guardrails",
        "",
        "- No held-out row scored; set is untouched by development; pass bar fixed from "
        "first principles before scoring; no registry/ontology/label change.",
    ]
    return "\n".join(lines) + "\n"


def write_option_b_heldout_preregistration(
    *,
    bronze_shard_glob: str = DEFAULT_BRONZE_SHARD_GLOB,
    atlas_manifest_path: Path,
    label_manifest_path: Path,
    recovery_positive_map_path: Path,
    recovery_download_manifest_path: Path,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    atlas = _load_json(Path(atlas_manifest_path))
    labels = _load_json(Path(label_manifest_path))
    families = _atlas_families(atlas)
    mcsa = _mcsa_accessions(labels)

    used: set[str] = set()
    for row in _load_json(Path(recovery_positive_map_path)).get("rows", []) or []:
        if row.get("accession"):
            used.add(str(row["accession"]))
    for row in _load_json(Path(recovery_download_manifest_path)).get("downloads", []) or []:
        if row.get("accession"):
            used.add(str(row["accession"]))

    bronze_rows: list[dict[str, Any]] = []
    for shard in sorted(glob.glob(bronze_shard_glob)):
        data = _load_json(Path(shard))
        rows = data if isinstance(data, list) else next(
            (v for v in data.values() if isinstance(v, list)), []
        )
        bronze_rows.extend(rows)

    members = select_untouched_heldout_positives(
        bronze_rows=bronze_rows, families=families, mcsa=mcsa, used_accessions=used
    )
    prereg = build_option_b_heldout_preregistration(members=members)
    prereg["source_artifacts"] = {
        "bronze_shard_glob": bronze_shard_glob,
        "atlas_manifest_id": atlas.get("artifact_id"),
        "label_manifest_id": labels.get("artifact_id"),
        "used_accessions_excluded": len(used),
    }
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(prereg, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(prereg), encoding="utf-8")
    return prereg
