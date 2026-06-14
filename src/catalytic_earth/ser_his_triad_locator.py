"""Source-free Ser/Cys-His-Asp catalytic-triad locator for the ser_his hole.

`ser_his_acid_hydrolase` is the one seed fingerprint the annotation-anchored
engine structurally cannot reach: it is **cofactorless**, so the engine's
positive policy -- "annotation-derived lane corroborated by the matching cofactor
class" -- can never fire (there is no metal/PLP/flavin/heme to corroborate). The
2026-06-10 coverage/redundancy governor confirmed it as the sharpest HOLE (42
frozen, 0 expansion). The 2026-06-03 decision log already named the fix as an open
design item: a source-free catalytic-triad geometric locator for serine
hydrolases.

This module supplies the missing corroborator. For a cofactorless serine
hydrolase the structural signature of catalysis is the Ser/Cys/Thr-His-Asp/Glu
charge-relay triad, which is readable from coordinates alone. The geometry
primitive already exists (`serine_active_site.extract_source_free_ser_his_acid_triad`),
but resolving a *geometric* triad is not specific on its own -- many folds carry
an incidental Ser/His/acid proximity (~1/3 of arbitrary structures trip the raw
distance cutoffs). The precision comes from corroboration: the geometric triad
must coincide with the **annotated catalytic ACT_SITE residues** of a
**serine-hydrolase EC family**, with **no catalytic cofactor** annotated. That
combination -- annotation-anchored scope (EC for scope only, in excluded_context,
never predictive) + coordinate triad confirmation matching the annotated catalytic
center -- is the cofactorless analogue of the engine's cofactor corroboration.

Deliverables (all NON-DESTRUCTIVE; no network, no registry write, no label
emitted into any registry):

1. ``confirm_catalytic_triad`` -- the corroborated-triad primitive.
2. ``assess_ser_his_candidate`` -- the full annotation-anchored ser_his rule on a
   registry-shaped row (assign / hold / skip + reason).
3. ``build_ser_his_triad_locator_scan`` -- a control panel (measures the raw
   incidental-trigger rate that motivates corroboration, plus positive controls),
   a recovery scan over coordinate-bearing registry rows, and a ready-to-run
   **acquisition contract** that an authorized network-enabled sourcing run uses
   to fill the hole to the governor's floor.

Why a contract and not filled labels here: in this environment the hand-curated
pools are drained and UniProt is network-blocked (HTTP 403), and the registries
carry no local serine-hydrolase-family rows -- so there is genuinely no candidate
supply to source or recover. This mirrors the project's established pattern (the
ESMFold2 staged contract, the banked Lever-2 locators): build the mechanism and a
ready-to-run contract when the environment blocks execution, so the climb resumes
the moment sourcing is authorized.
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from typing import Any

from .registry_io import load_json
from .serine_active_site import extract_source_free_ser_his_acid_triad
from .structure import parse_atom_site_loop

DEFAULT_FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
DEFAULT_EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")

# Serine-hydrolase EC families whose catalysis runs through a Ser/Cys/Thr-His-acid
# triad. EC is used for SCOPE ASSIGNMENT only (it stays in excluded_context and is
# never a predictive feature). The nuclease/phosphodiesterase 3.1.11/3.1.13/3.1.16
# families share the 3.1.1 prefix textually but are NOT triad hydrolases -- they
# are excluded explicitly.
SERINE_HYDROLASE_EC_PREFIXES = ("3.4.21", "3.4.16", "3.1.1")
NON_TRIAD_EC_PREFIXES = ("3.1.11", "3.1.13", "3.1.16")

# The governor's 100-label floor; ser_his is at 42 combined -> deficit 58.
DEFAULT_TARGET_FLOOR = 100


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> list[dict[str, Any]]:
    payload = load_json(Path(path))
    if not isinstance(payload, list):
        raise ValueError(f"{path} must contain a JSON list")
    return payload


def is_serine_hydrolase_ec(ec_numbers: list[str]) -> bool:
    """True iff a serine-hydrolase-family EC is present and no nuclease EC shadows it.

    EC is consumed for scope assignment only -- never as a predictive feature.
    """
    for ec in ec_numbers or []:
        if ec.startswith(NON_TRIAD_EC_PREFIXES):
            continue
        if ec.startswith(SERINE_HYDROLASE_EC_PREFIXES):
            return True
    return False


def confirm_catalytic_triad(
    atoms: list[dict[str, Any]],
    annotated_act_site_positions: set[int],
    *,
    min_annotated_overlap: int = 2,
) -> dict[str, Any]:
    """Confirm a catalytic Ser/Cys/Thr-His-Asp/Glu triad from coordinates.

    Runs the source-free geometric triad extractor, then *corroborates* that the
    resolved triad coincides with the annotated catalytic ACT_SITE residues. The
    geometric step alone is not specific (incidental triads are common); the
    corroboration against the annotation is what makes a positive call precise.
    No EC / name / prose is consumed.
    """
    extraction = extract_source_free_ser_his_acid_triad(atoms)
    resolved = extraction.get("status") == "ser_his_acid_triad_resolved"
    triad = extraction.get("selected_triad") or {}
    triad_resids = {
        int(item["resid"])
        for item in triad.get("residue_ids", [])
        if str(item.get("resid", "")).lstrip("-").isdigit()
    }
    overlap = sorted(triad_resids & set(annotated_act_site_positions or set()))
    corroborated = resolved and len(overlap) >= min_annotated_overlap
    return {
        "geometric_triad_resolved": resolved,
        "annotation_corroborated": corroborated,
        "triad_residue_ids": sorted(triad_resids),
        "annotated_act_site_overlap": overlap,
        "annotated_act_site_overlap_count": len(overlap),
        "min_annotated_overlap_required": min_annotated_overlap,
        "triad_geometry": triad if resolved else None,
        "status": (
            "ser_his_triad_annotation_corroborated"
            if corroborated
            else "ser_his_triad_resolved_uncorroborated"
            if resolved
            else "no_ser_his_triad"
        ),
    }


def _mechanism_evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("mechanism_evidence", {}) or {}


def _structure_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("structure_provenance", {}) or {}


def _act_site_positions(row: dict[str, Any]) -> set[int]:
    positions = set()
    for residue in _mechanism_evidence(row).get("active_site_residues") or []:
        if residue.get("feature_code") == "ACT_SITE" and isinstance(
            residue.get("position"), int
        ):
            positions.add(residue["position"])
    return positions


def assess_ser_his_candidate(
    row: dict[str, Any],
    *,
    coordinate_root: Path | None = None,
) -> dict[str, Any]:
    """Annotation-anchored ser_his rule for a registry-shaped row.

    Conservative, HOLD-by-default: a row is assigned ``ser_his_acid_hydrolase``
    only when (a) it carries a serine-hydrolase-family EC, (b) it has NO catalytic
    cofactor annotated, (c) staged coordinates are available, and (d) the
    coordinate triad is annotation-corroborated against the catalytic ACT_SITE.
    Anything ambiguous is HELD; non-serine-EC rows are SKIPPED. EC is used for
    scope assignment only and is recorded as excluded predictive context.
    """
    mech = _mechanism_evidence(row)
    ec_numbers = [e for e in (mech.get("ec_numbers") or []) if e]
    if not is_serine_hydrolase_ec(ec_numbers):
        return {"decision": "skip", "reason": "not_a_serine_hydrolase_ec_family"}
    if mech.get("cofactors"):
        # a catalytic cofactor means this is not a cofactorless triad hydrolase
        return {"decision": "hold", "reason": "catalytic_cofactor_annotated"}

    coord_path = _structure_provenance(row).get("coordinate_path")
    if coord_path and coordinate_root is not None:
        coord_path = str(Path(coordinate_root) / coord_path)
    if not coord_path or not Path(coord_path).exists():
        return {
            "decision": "hold",
            "reason": "no_staged_coordinates_for_triad_confirmation",
            "ec_numbers": ec_numbers,
        }

    try:
        atoms = parse_atom_site_loop(Path(coord_path).read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive
        return {"decision": "hold", "reason": f"coordinate_parse_error:{type(exc).__name__}"}

    confirmation = confirm_catalytic_triad(atoms, _act_site_positions(row))
    if confirmation["annotation_corroborated"]:
        return {
            "decision": "assign_ser_his",
            "reason": "serine_hydrolase_ec_no_cofactor_triad_annotation_corroborated",
            "fingerprint_id": "ser_his_acid_hydrolase",
            "ec_numbers": ec_numbers,
            "triad_confirmation": confirmation,
        }
    return {
        "decision": "hold",
        "reason": confirmation["status"],
        "ec_numbers": ec_numbers,
        "triad_confirmation": confirmation,
    }


def _ser_his_combined_count(frozen: list[dict], expansion: list[dict]) -> dict[str, int]:
    f = sum(1 for r in frozen if r.get("fingerprint_id") == "ser_his_acid_hydrolase")
    e = sum(1 for r in expansion if r.get("fingerprint_id") == "ser_his_acid_hydrolase")
    return {"frozen": f, "expansion": e, "combined": f + e}


def build_control_panel(
    cif_paths: list[Path],
    *,
    sample_limit: int = 120,
) -> dict[str, Any]:
    """Measure the raw geometric incidental-trigger rate over local structures.

    This quantifies *why* annotation corroboration is required: the fraction of
    arbitrary local structures whose raw distance cutoffs resolve a triad is the
    false-positive surface that the ACT_SITE corroboration suppresses.
    """
    ordered = sorted(str(p) for p in cif_paths)[:sample_limit]
    resolved = 0
    checked = 0
    positive_controls = []
    for path in ordered:
        try:
            atoms = parse_atom_site_loop(Path(path).read_text(encoding="utf-8"))
        except Exception:
            continue
        checked += 1
        extraction = extract_source_free_ser_his_acid_triad(atoms)
        if extraction.get("status") == "ser_his_acid_triad_resolved":
            resolved += 1
            if len(positive_controls) < 5:
                positive_controls.append(
                    {
                        "structure": Path(path).name,
                        "triad": extraction.get("selected_triad"),
                    }
                )
    return {
        "structures_checked": checked,
        "geometric_triad_resolved": resolved,
        "raw_incidental_resolution_rate": (
            round(resolved / checked, 4) if checked else None
        ),
        "interpretation": (
            "raw geometric triad resolution is NOT specific; this rate is the "
            "incidental-trigger surface that the annotated-ACT_SITE corroboration "
            "suppresses to make a ser_his assignment precise"
        ),
        "positive_control_triads": positive_controls,
    }


def build_ser_his_triad_locator_scan(
    frozen: list[dict[str, Any]],
    expansion: list[dict[str, Any]],
    *,
    coordinate_root: Path | None = None,
    cif_paths: list[Path] | None = None,
    control_sample_limit: int = 120,
    target_floor: int = DEFAULT_TARGET_FLOOR,
) -> dict[str, Any]:
    counts = _ser_his_combined_count(frozen, expansion)
    deficit = max(0, target_floor - counts["combined"])

    # ---- recovery scan over coordinate-bearing registry rows -------------
    decisions: Counter = Counter()
    assigned: list[dict[str, Any]] = []
    held_samples: list[dict[str, Any]] = []
    serine_ec_rows = 0
    for row in expansion:
        ec_numbers = [e for e in (_mechanism_evidence(row).get("ec_numbers") or []) if e]
        if not is_serine_hydrolase_ec(ec_numbers):
            continue
        serine_ec_rows += 1
        assessment = assess_ser_his_candidate(row, coordinate_root=coordinate_root)
        decisions[assessment["decision"]] += 1
        if assessment["decision"] == "assign_ser_his":
            assigned.append({"entry_id": row.get("entry_id"), **assessment})
        elif len(held_samples) < 10:
            held_samples.append({"entry_id": row.get("entry_id"), **assessment})

    recovery_scan = {
        "expansion_serine_hydrolase_ec_rows": serine_ec_rows,
        "decision_counts": dict(sorted(decisions.items())),
        "confirmed_ser_his_recoveries": len(assigned),
        "apply_ready_labels": assigned,
        "held_samples": held_samples,
        "note": (
            "recovers genuine cofactorless triad hydrolases mis-binned as OOS only "
            "when triad geometry is corroborated against the annotated catalytic "
            "ACT_SITE; non-destructive -- nothing is written to any registry"
        ),
    }

    # ---- control panel ---------------------------------------------------
    control_panel = (
        build_control_panel(cif_paths, sample_limit=control_sample_limit)
        if cif_paths
        else {"skipped": "no_cif_paths_provided"}
    )

    # ---- ready-to-run acquisition contract -------------------------------
    acquisition_contract = {
        "fingerprint": "ser_his_acid_hydrolase",
        "current_combined": counts["combined"],
        "frozen": counts["frozen"],
        "expansion": counts["expansion"],
        "target_floor": target_floor,
        "deficit_to_floor": deficit,
        "blocked_in_this_environment": {
            "hand_curated_pools": "drained",
            "uniprot_network": "blocked_http_403",
            "local_serine_hydrolase_candidate_rows": serine_ec_rows,
            "consequence": (
                "no candidate supply exists locally; the hole cannot be filled here "
                "-- this contract is ready to run when sourcing is authorized"
            ),
        },
        "sourcing_rule": {
            "scope_assignment_ec_families": list(SERINE_HYDROLASE_EC_PREFIXES),
            "excluded_ec_families": list(NON_TRIAD_EC_PREFIXES),
            "ec_usage": "scope_assignment_only_never_predictive_feature",
            "cofactor_requirement": "no_catalytic_cofactor_annotated",
            "structural_corroboration": (
                "coordinate Ser/Cys/Thr-His-Asp/Glu triad must coincide with the "
                "annotated catalytic ACT_SITE residues (>=2 overlap)"
            ),
            "dedup": "against BOTH registries (accession + sequence-SHA)",
            "tiering": "tier=bronze, review_status=automation_curated, uniprot namespace",
            "evidence_basis": "reviewed_swissprot_ec_rhea_annotation + source_free_triad_geometry",
        },
        "execution_command_when_authorized": (
            "fetch reviewed Swiss-Prot serine-hydrolase entries (EC 3.4.21/3.4.16/"
            "3.1.1, ACT_SITE catalytic triad annotated, no cofactor), stage AF/PDB "
            "coordinates, then run assess_ser_his_candidate over them and apply the "
            "confirmed labels via apply-external-annotation-anchored-import"
        ),
    }

    return {
        "audit": "ser_his_triad_locator_scan",
        "created_utc": _utc_now_iso(),
        "status": "ok",
        "non_destructive": True,
        "ser_his_counts": counts,
        "control_panel": control_panel,
        "recovery_scan": recovery_scan,
        "acquisition_contract": acquisition_contract,
        "guardrails": {
            "frozen_benchmark_written": False,
            "expansion_registry_written": False,
            "labels_emitted_to_registry": 0,
            "ec_used_for_scope_assignment_only_never_predictive": True,
            "triad_confirmation_uses_only_coordinates_no_text": True,
            "metadata_and_local_coordinates_only_no_network": True,
        },
    }


def _report(audit: dict[str, Any]) -> str:
    counts = audit["ser_his_counts"]
    cp = audit["control_panel"]
    rs = audit["recovery_scan"]
    ac = audit["acquisition_contract"]
    lines = [
        "# Ser/Cys-His-Asp Catalytic-Triad Locator For The ser_his Hole",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "`ser_his_acid_hydrolase` is the one seed fingerprint the cofactor-anchored "
        "engine cannot reach -- it is cofactorless. This supplies the missing "
        "corroborator: a coordinate Ser/Cys/Thr-His-Asp/Glu triad that must coincide "
        "with the annotated catalytic ACT_SITE of a serine-hydrolase EC family. "
        "Non-destructive: no registry is written, no label emitted.",
        "",
        "## ser_his standing",
        "",
        f"- Combined {counts['combined']} ({counts['frozen']} frozen + "
        f"{counts['expansion']} expansion); floor {ac['target_floor']}; deficit "
        f"{ac['deficit_to_floor']}.",
        "",
        "## Control panel -- why corroboration is required",
        "",
    ]
    if "skipped" in cp:
        lines.append(f"- Control panel skipped: {cp['skipped']}.")
    else:
        lines.append(
            f"- Raw geometric triad resolves on {cp['geometric_triad_resolved']}/"
            f"{cp['structures_checked']} local structures "
            f"(rate {cp['raw_incidental_resolution_rate']}) -- the incidental-trigger "
            "surface that ACT_SITE corroboration suppresses."
        )
    lines.extend(
        [
            "",
            "## Recovery scan (coordinate-bearing registry rows)",
            "",
            f"- Serine-hydrolase-EC rows in expansion: "
            f"{rs['expansion_serine_hydrolase_ec_rows']}.",
            f"- Decisions: {rs['decision_counts']}.",
            f"- Confirmed ser_his recoveries (apply-ready): "
            f"{rs['confirmed_ser_his_recoveries']}.",
            "",
            "## Acquisition contract (ready to run when sourcing is authorized)",
            "",
            f"- Blocked here: pools {ac['blocked_in_this_environment']['hand_curated_pools']}; "
            f"UniProt {ac['blocked_in_this_environment']['uniprot_network']}; local "
            f"serine-hydrolase candidate rows "
            f"{ac['blocked_in_this_environment']['local_serine_hydrolase_candidate_rows']}.",
            f"- Scope EC families: {ac['sourcing_rule']['scope_assignment_ec_families']} "
            f"(excluding {ac['sourcing_rule']['excluded_ec_families']}); EC "
            f"{ac['sourcing_rule']['ec_usage']}.",
            f"- Cofactor: {ac['sourcing_rule']['cofactor_requirement']}; structural "
            f"corroboration: {ac['sourcing_rule']['structural_corroboration']}.",
            f"- Dedup: {ac['sourcing_rule']['dedup']}; tiering: "
            f"{ac['sourcing_rule']['tiering']}.",
            "",
            "## Guardrails",
            "",
            f"- Frozen benchmark written: {audit['guardrails']['frozen_benchmark_written']}.",
            f"- Registry labels emitted: {audit['guardrails']['labels_emitted_to_registry']}.",
            "- EC used for scope assignment only, never predictive; triad confirmation "
            "uses coordinates only; no network.",
            "",
        ]
    )
    return "\n".join(lines)


def write_ser_his_triad_locator_scan(
    *,
    out_path: Path,
    report_path: Path | None = None,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    coordinate_glob: str = "artifacts/**/*.cif",
    control_sample_limit: int = 120,
    target_floor: int = DEFAULT_TARGET_FLOOR,
) -> dict[str, Any]:
    frozen = _load_json(frozen_benchmark_path)
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    cif_paths = sorted(Path(".").glob(coordinate_glob))
    audit = build_ser_his_triad_locator_scan(
        frozen,
        expansion,
        cif_paths=cif_paths,
        control_sample_limit=control_sample_limit,
        target_floor=target_floor,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
