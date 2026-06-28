"""Locked one-shot pre-registration for the held-out mechanism-recovery test.

Every operating point produced this session (30/35 @ 8 FP June 9 dial, the fold
frontier, 28/35 fold-NN recovery) is a calibration *development* figure: the same
calibration rows were inspected from several angles, so those numbers are
optimistic by construction and not unbiased generalization estimates. The only
unbiased estimate is a single, choices-frozen read of the never-touched held-out
split.

This module freezes that test BEFORE it is run: the exact rule, the exact
held-out row set (enumerated and content-hashed so it cannot be swapped or
cherry-picked), the pre-committed pass/fail bar (derived only from the
calibration point, never from held-out data), and the exact execution procedure.
It scores nothing on held-out; it only emits the contract. Executing the test is
a separate, explicitly authorized one-shot that must match this artifact's
``frozen_heldout_set.sha256`` and commit hash.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SPLIT_MANIFEST_PATH = (
    "artifacts/v3_mechanism_feature_embedding_train_cal_split_manifest_current702_20260601.json"
)
DEFAULT_LABEL_MANIFEST_PATH = (
    "artifacts/v3_sequence_nn_label_manifest_current702_20260525.json"
)
DEFAULT_HELDOUT_COORDINATE_DIRS: tuple[str, ...] = (
    "artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/"
    "queries_all_heldout",
    "artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/"
    "queries_cofactor_confounded_oos",
)
DEFAULT_OUT_PATH = (
    "artifacts/v3_heldout_oneshot_preregistration_current702_20260628.json"
)
DEFAULT_REPORT_PATH = (
    "work/heldout_oneshot_preregistration_current702_20260628.md"
)

# ---------------------------------------------------------------------------
# Frozen rule. Pinned BEFORE any held-out scoring. Do not edit after commit.
# ---------------------------------------------------------------------------
PRIMARY_RULE: dict[str, Any] = {
    "name": "june9_router_cofactor_dial_0p44_fold_gate_off",
    "router": (
        "cofactor_fusion_operating_point builder with the fingerprint registry pinned "
        "to git commit d567ee0d (the June 9 state: 8 fingerprint families), default "
        "graph artifacts/v1_graph_1025.json, label manifest "
        "v3_sequence_nn_label_manifest_current702_20260525, channel "
        "v3_cofactor_presence_calibration_current702_20260604, alphafold_version 6"
    ),
    "cofactor_threshold": 0.44,
    "fold_gate": "off",
    "inscope_correct_definition": (
        "fused.top1_fingerprint_id == frozen true_fingerprint_id AND fused.top1_score "
        ">= 0.44 (identical to the builder's fused_correct_at_threshold that produced "
        "the calibration 30/35)"
    ),
    "oos_false_positive_definition": "fused.top1_score >= 0.44 on an OOS row",
}

# Pre-committed pass/fail bar, derived ONLY from the calibration operating point
# plus a generalization tolerance. No held-out data informs these numbers.
SUCCESS_BAR: dict[str, Any] = {
    "calibration_reference": {
        "inscope_recovery": "30/35 (0.857)",
        "oos_false_positive_rate": "8/26 (0.308)",
    },
    "primary_pass_criteria": (
        "heldout in-scope recovery rate >= 0.70 AND heldout OOS false-positive rate "
        "<= 0.40"
    ),
    "derivation": (
        "Calibration recovery 0.857 has SE ~0.059 on n=35, so ~2 SE below is ~0.74; "
        "rounded conservatively to a 0.70 floor. Calibration OOS-FP 0.308 has SE ~0.090 "
        "on n=26, so ~2 SE above is ~0.49; rounded conservatively to a 0.40 ceiling. "
        "Both bars were fixed before any held-out row was scored."
    ),
    "interpretation": (
        "PASS means the calibration June 9 dial operating point generalizes to the "
        "never-seen held-out M-CSA split. FAIL means it does not, and no post-hoc "
        "threshold change may rescue this pre-registration."
    ),
}

SECONDARY_EXPLORATORY: dict[str, Any] = {
    "name": "cofactor_dial_0p44_plus_fold_nn_gate_0p65",
    "description": (
        "Exploratory only, no pass/fail: also apply a fold-NN TM gate >= 0.65 (the "
        "M-CSA baseline's high-precision point) on top of the primary rule, to check "
        "whether the off-M-CSA-validated abstention signal also tightens held-out "
        "precision. Reported alongside the primary result but never used to redefine "
        "the primary decision."
    ),
}

ONE_SHOT_GUARDRAIL = (
    "Run exactly once. Report the resulting counts verbatim. Do not adjust the rule, "
    "thresholds, correctness definition, or row set after observing any held-out "
    "result. Any re-run or post-hoc change invalidates this pre-registration."
)


def _load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _accessions(row: dict[str, Any]) -> list[str]:
    values = []
    if row.get("sequence_id"):
        values.append(str(row["sequence_id"]))
    values.extend(str(v) for v in (row.get("real_sequence_accessions") or []))
    return list(dict.fromkeys(values))


def _true_fingerprint(row: dict[str, Any]) -> str | None:
    return row.get("true_fingerprint_id") or row.get("fingerprint_id")


def build_frozen_heldout_set(
    *,
    split_manifest: dict[str, Any],
    label_manifest: dict[str, Any],
    heldout_structure_accessions: set[str],
) -> dict[str, Any]:
    train_cal = {
        str(r.get("entry_id"))
        for r in split_manifest.get("split_records", [])
        if r.get("entry_id")
    }
    rows = {
        str(r.get("entry_id")): r
        for r in label_manifest.get("rows", [])
        if r.get("entry_id")
    }
    members: list[dict[str, Any]] = []
    for entry_id in sorted(set(rows) - train_cal):
        row = rows[entry_id]
        accessions = _accessions(row)
        has_structure = any(a in heldout_structure_accessions for a in accessions)
        if not has_structure:
            continue
        true_fp = _true_fingerprint(row)
        members.append(
            {
                "entry_id": entry_id,
                "row_class": "inscope" if true_fp else "oos",
                "true_fingerprint_id": true_fp,
                "accessions": accessions,
            }
        )
    members.sort(key=lambda m: m["entry_id"])
    canonical = json.dumps(members, sort_keys=True, separators=(",", ":"))
    inscope = [m for m in members if m["row_class"] == "inscope"]
    oos = [m for m in members if m["row_class"] == "oos"]
    return {
        "definition": (
            "current702 label rows not in the train/cal split manifest that also have a "
            "staged held-out structure (scoreable). Enumerated and content-hashed so the "
            "evaluated set cannot be swapped or trimmed after the fact."
        ),
        "members": members,
        "counts": {
            "total": len(members),
            "inscope": len(inscope),
            "oos": len(oos),
        },
        "sha256": _sha256_text(canonical),
    }


def build_heldout_oneshot_preregistration(
    *,
    frozen_heldout_set: dict[str, Any],
    heldout_coordinate_dirs: tuple[str, ...],
    split_manifest_summary: dict[str, Any],
    label_manifest_summary: dict[str, Any],
) -> dict[str, Any]:
    counts = frozen_heldout_set["counts"]
    procedure = [
        "In an isolated git worktree at HEAD, pin the registry: "
        "git checkout d567ee0d -- data/registries/mechanism_fingerprints.json "
        "data/registries/mechanism_ontology.json (the main repo registry is never "
        "mutated).",
        "Construct a held-out split manifest containing exactly the "
        f"{counts['total']} frozen_heldout_set entry_ids (verify sha256 first).",
        "Run the cofactor_fusion_operating_point router over the held-out coordinate "
        "dirs at cofactor_threshold 0.44, producing fused per-row calls and scores for "
        "the frozen held-out rows only.",
        "Count in-scope recovery (fused exact match at threshold) and OOS false "
        "positives (fused retained at threshold); compute the two rates.",
        "Compare to SUCCESS_BAR.primary_pass_criteria; emit PASS or FAIL verbatim and "
        "stop. Report the secondary fold-gated point for information only.",
    ]
    return {
        "artifact_id": "v3_heldout_oneshot_preregistration_current702_20260628",
        "schema_version": "heldout_oneshot_preregistration.v1",
        "created_utc": _utc_now_iso(),
        "status": "preregistered_not_yet_run",
        "result_class": (
            "locked_one_shot_heldout_preregistration_no_heldout_scoring_no_registry_change"
        ),
        "guardrails": {
            "heldout_rows_scored": False,
            "heldout_labels_used_as_features": False,
            "heldout_labels_used_only_to_size_and_freeze_the_set": True,
            "success_bar_derived_from_heldout": False,
            "success_bar_derived_from_calibration_only": True,
            "registry_or_ontology_changed": False,
            "production_threshold_changed": False,
            "model_weights_changed": False,
        },
        "why": (
            "All session operating points are calibration development figures (the "
            "calibration rows were inspected repeatedly), so they are optimistic and "
            "unvalidated. This locks the single unbiased test before it is run so the "
            "result cannot be cherry-picked."
        ),
        "primary_hypothesis": (
            "The June 9 router at the 0.44 cofactor dial (calibration 30/35 recovery, "
            "8/26 OOS FP) generalizes to the never-seen held-out M-CSA split at the "
            "pre-committed bar."
        ),
        "frozen_rule": PRIMARY_RULE,
        "success_bar": SUCCESS_BAR,
        "secondary_exploratory": SECONDARY_EXPLORATORY,
        "frozen_heldout_set": frozen_heldout_set,
        "heldout_coordinate_dirs": list(heldout_coordinate_dirs),
        "execution_procedure": procedure,
        "one_shot_guardrail": ONE_SHOT_GUARDRAIL,
        "provenance": {
            "split_manifest": split_manifest_summary,
            "label_manifest": label_manifest_summary,
            "note": (
                "The committing git commit is the pre-registration lock; the executing "
                "run must cite this artifact_id, match frozen_heldout_set.sha256, and "
                "apply frozen_rule unchanged."
            ),
        },
    }


def _report(prereg: dict[str, Any]) -> str:
    fs = prereg["frozen_heldout_set"]
    bar = prereg["success_bar"]
    rule = prereg["frozen_rule"]
    lines = [
        "# Held-Out One-Shot Pre-Registration",
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
        "## Frozen Rule",
        "",
        f"- Router: {rule['router']}",
        f"- Cofactor threshold: {rule['cofactor_threshold']}; fold gate: {rule['fold_gate']}.",
        f"- In-scope correct: {rule['inscope_correct_definition']}.",
        f"- OOS false positive: {rule['oos_false_positive_definition']}.",
        "",
        "## Pre-Committed Success Bar",
        "",
        f"- Calibration reference: recovery {bar['calibration_reference']['inscope_recovery']}, "
        f"OOS FP {bar['calibration_reference']['oos_false_positive_rate']}.",
        f"- PASS criteria: {bar['primary_pass_criteria']}.",
        f"- Derivation: {bar['derivation']}",
        "",
        "## Frozen Held-Out Set",
        "",
        f"- {fs['definition']}",
        f"- Counts: {fs['counts']['total']} total "
        f"({fs['counts']['inscope']} in-scope, {fs['counts']['oos']} OOS).",
        f"- Content hash (sha256): `{fs['sha256']}`.",
        "",
        "## Execution Procedure (authorized one-shot)",
        "",
    ]
    for i, step in enumerate(prereg["execution_procedure"], 1):
        lines.append(f"{i}. {step}")
    lines += [
        "",
        "## One-Shot Guardrail",
        "",
        f"- {prereg['one_shot_guardrail']}",
        "",
        "## Guardrails",
        "",
        "- No held-out row was scored; held-out labels were used only to size and freeze "
        "the set, never as features.",
        "- The success bar was derived from calibration only, before any held-out scoring.",
        "- No registry, ontology, label, threshold, or model change.",
    ]
    return "\n".join(lines) + "\n"


def write_heldout_oneshot_preregistration(
    *,
    split_manifest_path: Path,
    label_manifest_path: Path,
    heldout_coordinate_dirs: tuple[str, ...] = DEFAULT_HELDOUT_COORDINATE_DIRS,
    out_path: Path,
    report_path: Path | None = None,
) -> dict[str, Any]:
    import glob
    import os
    import re

    split_manifest = _load_json(split_manifest_path)
    label_manifest = _load_json(label_manifest_path)

    heldout_structure_accessions: set[str] = set()
    for directory in heldout_coordinate_dirs:
        for cif in glob.glob(os.path.join(directory, "*.cif")):
            match = re.search(r"afdb_([A-Za-z0-9]+)_v6", os.path.basename(cif))
            if match:
                heldout_structure_accessions.add(match.group(1))

    frozen = build_frozen_heldout_set(
        split_manifest=split_manifest,
        label_manifest=label_manifest,
        heldout_structure_accessions=heldout_structure_accessions,
    )
    prereg = build_heldout_oneshot_preregistration(
        frozen_heldout_set=frozen,
        heldout_coordinate_dirs=heldout_coordinate_dirs,
        split_manifest_summary={
            "path": str(split_manifest_path),
            "sha256": _sha256_path(Path(split_manifest_path)),
        },
        label_manifest_summary={
            "path": str(label_manifest_path),
            "artifact_id": label_manifest.get("artifact_id"),
            "sha256": _sha256_path(Path(label_manifest_path)),
        },
    )
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
