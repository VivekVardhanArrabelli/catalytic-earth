"""Evidence-handle expansion scout — recover within-Swiss-Prot supply the cofactor handle misses.

The breadth scout (decision_log 2026-06-11 "BREADTH FEASIBILITY SCOUT") found that part of the
apparent reviewed-Swiss-Prot shortage is an EVIDENCE-HANDLE problem, not a supply problem: the
import gate corroborates family scope mostly via the UniProt COFACTOR comment (`cc_cofactor`), but
many families annotate their defining evidence elsewhere. The decision-grade case: NAD(P)-dependent
dehydrogenases (EC 1.1.1) have ~7800 reviewed entries, but `cc_cofactor:nad/nadp` reaches only ~7
because NAD(P) is a *cosubstrate / reaction participant*, recorded as a UniProt KEYWORD
(KW-0520/KW-0521) and as binding-site / active-site features — not as a cofactor comment.

This module MEASURES, per family, how much reviewed supply each alternative within-Swiss-Prot
corroborator handle recovers, so "weak handle" becomes "here is the handle that works and the
supply it unlocks." It is the empirical basis for broadening the admission engine's corroborators
BEFORE leaving reviewed Swiss-Prot (the same lesson as cofactorless ser_his, which needed a
catalytic-triad route instead of a cofactor).

Corroborator axes probed (all are *reviewed annotation*, used for SCOPE/admission only — they go in
`excluded_context`, never a predictive feature, exactly like the existing cofactor+EC handle):
  - `cofactor_comment`   — `cc_cofactor:<x>` (the current handle; the cofactor/cosubstrate ligand)
  - `functional_keyword` — `keyword:<KW>` (controlled-vocabulary functional/family signature)
  - `binding_site`       — `ft_binding:*` (annotated ligand/substrate binding residues)
  - `active_site`        — `ft_act_site:*` (annotated catalytic residues)
EC scope (`ec:<family>`) is the ceiling but is NOT itself a corroborator (EC decides scope only and
stays excluded). A handle is only counted as a corroborator if it adds an independent annotated
evidence axis beyond EC. Rhea-participant and sequence-motif/domain-profile corroborators need
entry-level evidence (not header-countable), so they are recorded as recommended handles, not
measured here — disclosed, not faked.

NON-DESTRUCTIVE and leakage-safe: writes NO registry, creates NO labels; cheap `x-total-results`
header counts via injected fetchers (offline-testable).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_uniprot_query_count
from .breadth_feasibility_scout import CONFUSABLE_CAP, SUPPLY_KEEP_FACTOR
from .coverage_redundancy_audit import DEFAULT_CAP_CEILING, DEFAULT_TARGET_FLOOR

ARTIFACT_ID = "v3_evidence_handle_expansion_current702"
SCHEMA_VERSION = "evidence_handle_expansion.v1"

# A handle counts as "corroborated" recovery only if it is an evidence axis INDEPENDENT of the EC
# scope. EC-family alone (the ceiling) is scope, not corroboration.
CORROBORATOR_HANDLE_IDS = ("cofactor_comment", "functional_keyword", "binding_site", "active_site")

# Families where the current cofactor handle is weak or where the defining evidence is annotated as
# a keyword / cosubstrate / active-site rather than a cofactor comment. `current_handle` is the
# cc_cofactor-style clause the cofactor-anchored gate would use today (None = no cofactor handle
# exists for this chemistry); `candidate_handles` are the alternative within-Swiss-Prot corroborators
# to measure. `confusable` selects the 150 vs 250 cap (Stage-2 cap lesson).
HANDLE_FAMILIES: tuple[dict[str, Any], ...] = (
    {
        "family": "nad_p_dehydrogenase_ec_1_1_1",
        "ec_class": "EC 1.1.1 (CH-OH donor, NAD(P) acceptor)",
        "chemistry": "NAD(P)(H)-dependent hydride-transfer dehydrogenase/reductase (SDR/MDR/AKR)",
        "ec_filter": "(ec:1.1.1.*)",
        "current_handle": "((cc_cofactor:nad) OR (cc_cofactor:nadp))",
        "candidate_handles": (
            ("functional_keyword", "((keyword:NAD) OR (keyword:NADP))"),
            ("binding_site", "(ft_binding:*)"),
            ("active_site", "(ft_act_site:*)"),
        ),
        "confusable": True,
        "recommended_entry_level_corroborators": [
            "Rhea NAD(P)(+)/NAD(P)H participant in the catalytic-activity reaction",
            "Rossmann GxGxxG dinucleotide-binding sequence motif",
        ],
        "notes": "The decision-grade handle gap: NAD(P) is a cosubstrate (keyword), not a cofactor comment.",
    },
    {
        "family": "nad_p_oxidoreductase_broad_ec_1",
        "ec_class": "EC 1.* (oxidoreductase, NAD(P)-dependent broadly)",
        "chemistry": "NAD(P)-dependent oxidoreductases beyond EC 1.1.1 (1.2/1.3/1.4/1.5/...)",
        "ec_filter": "(ec:1.*)",
        "current_handle": "((cc_cofactor:nad) OR (cc_cofactor:nadp))",
        "candidate_handles": (
            ("functional_keyword", "((keyword:NAD) OR (keyword:NADP))"),
            ("binding_site", "(ft_binding:*)"),
            ("active_site", "(ft_act_site:*)"),
        ),
        "confusable": True,
        "recommended_entry_level_corroborators": [
            "Rhea NAD(P) participant + EC-subclass-specific reaction",
            "subclass-specific active-site residue roles",
        ],
        "notes": "Broad NAD(P) redox pool; must be split by EC-subclass before sourcing (cap per lane).",
    },
    {
        "family": "sam_methyltransferase_ec_2_1_1",
        "ec_class": "EC 2.1.1 (one-carbon methyl transferase)",
        "chemistry": "Classical SAM-dependent methyltransferase (SN2 methyl transfer)",
        "ec_filter": "(ec:2.1.1.*)",
        "current_handle": "(cc_cofactor:s-adenosyl-l-methionine)",
        "candidate_handles": (
            ("functional_keyword", "(keyword:Methyltransferase)"),
            ("binding_site", "(ft_binding:*)"),
            ("active_site", "(ft_act_site:*)"),
        ),
        "confusable": False,
        "recommended_entry_level_corroborators": [
            "Rhea S-adenosyl-L-methionine + S-adenosyl-L-homocysteine participant pair",
            "no [4Fe-4S] (separates from radical-SAM)",
        ],
        "notes": "SAM is a cosubstrate; most MTases use the Methyltransferase keyword, not a cofactor comment.",
    },
    {
        "family": "non_heme_iron_2og_dioxygenase_ec_1_14_11",
        "ec_class": "EC 1.14.11 (2-oxoglutarate dioxygenase)",
        "chemistry": "Non-heme Fe(II)/2-oxoglutarate dioxygenase (2-His-1-carboxylate facial triad)",
        "ec_filter": "(ec:1.14.11.*)",
        "current_handle": "((cc_cofactor:fe) OR (cc_cofactor:iron))",
        "candidate_handles": (
            ("functional_keyword", "((keyword:Dioxygenase) OR (keyword:Iron))"),
            ("binding_site", "(ft_binding:*)"),
            ("active_site", "(ft_act_site:*)"),
        ),
        "confusable": False,
        "recommended_entry_level_corroborators": [
            "Rhea 2-oxoglutarate + succinate + CO2 participant",
            "HxD..H facial-triad residue roles",
        ],
        "notes": "Control: cofactor handle already decent; keyword/active-site confirm independence.",
    },
    {
        "family": "biotin_dependent_carboxylase_ec_6_4_1",
        "ec_class": "EC 6.4.1 / 6.3.4 (biotin carboxylase)",
        "chemistry": "Biotin-dependent carboxylase (carboxy-biotin transfer, ATP+Mg)",
        "ec_filter": "((ec:6.4.1.*) OR (ec:6.3.4.*))",
        "current_handle": "(cc_cofactor:biotin)",
        "candidate_handles": (
            ("functional_keyword", "(keyword:Biotin)"),
            ("binding_site", "(ft_binding:*)"),
            ("active_site", "(ft_act_site:*)"),
        ),
        "confusable": False,
        "recommended_entry_level_corroborators": [
            "biotinyl-lysine (K-biotin) modified-residue feature",
            "Rhea hydrogencarbonate + ATP participant",
        ],
        "notes": "Biotin is a prosthetic group recorded as a keyword + modified residue, not always a cofactor comment.",
    },
    {
        "family": "glycosyltransferase_ec_2_4",
        "ec_class": "EC 2.4 (glycosyltransferase)",
        "chemistry": "Sugar-nucleotide-dependent glycosyltransferase (GT-A/GT-B)",
        "ec_filter": "(ec:2.4.*)",
        "current_handle": None,
        "candidate_handles": (
            ("functional_keyword", "(keyword:Glycosyltransferase)"),
            ("binding_site", "(ft_binding:*)"),
            ("active_site", "(ft_act_site:*)"),
        ),
        "confusable": False,
        "recommended_entry_level_corroborators": [
            "Rhea UDP/GDP-sugar donor participant",
            "DxD motif (GT-A) / GT-B two-domain signature",
        ],
        "notes": "No single cofactor handle (donor varies); the functional keyword is the corroborator.",
    },
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _count(fetcher: Callable[[str], dict[str, Any]], clause: str) -> int | None:
    return fetcher(f"(reviewed:true) AND {clause}").get("total_results")


def evaluate_handle_family(
    spec: dict[str, Any],
    *,
    count_fetcher: Callable[[str], dict[str, Any]],
    target_floor: int,
    cap_ceiling: int,
) -> dict[str, Any]:
    """Measure reviewed supply per corroborator handle and the uplift over the current handle."""
    ec_filter = spec["ec_filter"]
    ec_ceiling = _count(count_fetcher, ec_filter)

    current_clause = spec.get("current_handle")
    current_supply = (
        _count(count_fetcher, f"{ec_filter} AND {current_clause}") if current_clause else None
    )

    handle_supplies: list[dict[str, Any]] = []
    for handle_id, clause in spec["candidate_handles"]:
        supply = _count(count_fetcher, f"{ec_filter} AND {clause}")
        ceiling = int(ec_ceiling or 0)
        handle_supplies.append(
            {
                "handle_id": handle_id,
                "is_corroborator": handle_id in CORROBORATOR_HANDLE_IDS,
                "clause": clause,
                "reviewed_supply": supply,
                "recovery_ratio_vs_ec_ceiling": (
                    round(int(supply or 0) / ceiling, 3) if ceiling else None
                ),
            }
        )

    corroborators = [h for h in handle_supplies if h["is_corroborator"]]
    best = max(
        corroborators, key=lambda h: int(h["reviewed_supply"] or 0), default=None
    )
    recovered = int(best["reviewed_supply"] or 0) if best else 0
    current_int = int(current_supply or 0)
    uplift = recovered - current_int

    cap = CONFUSABLE_CAP if spec.get("confusable") else cap_ceiling
    reachable = min(cap, int(round(recovered * SUPPLY_KEEP_FACTOR))) if recovered else 0
    reachable_current = min(cap, int(round(current_int * SUPPLY_KEEP_FACTOR))) if current_int else 0

    return {
        "family": spec["family"],
        "ec_class": spec["ec_class"],
        "chemistry": spec["chemistry"],
        "ec_filter": ec_filter,
        "ec_ceiling_supply": ec_ceiling,
        "current_handle": current_clause,
        "current_handle_supply": current_supply,
        "candidate_handle_supplies": handle_supplies,
        "best_corroborated_handle": best["handle_id"] if best else None,
        "best_corroborated_clause": best["clause"] if best else None,
        "recovered_supply": recovered,
        "recovery_ratio_vs_ec_ceiling": (
            round(recovered / int(ec_ceiling), 3) if ec_ceiling else None
        ),
        "uplift_vs_current_handle": uplift,
        "applied_cap": cap,
        "reachable_bronze_best_handle": reachable,
        "reachable_bronze_current_handle": reachable_current,
        "reachable_bronze_uplift": reachable - reachable_current,
        "floor_reachable_best_handle": reachable >= target_floor,
        "floor_reachable_current_handle": reachable_current >= target_floor,
        "recommended_entry_level_corroborators": spec.get(
            "recommended_entry_level_corroborators", []
        ),
        "notes": spec.get("notes", ""),
    }


def build_evidence_handle_expansion(
    *,
    handle_families: tuple[dict[str, Any], ...] = HANDLE_FAMILIES,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    created_utc: str | None = None,
    count_fetcher: Callable[[str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Non-destructive recon: how much within-Swiss-Prot supply do broader handles recover?"""
    created = created_utc or _utc_now_iso()
    count_fetcher = count_fetcher or fetch_uniprot_query_count

    probes = [
        evaluate_handle_family(
            spec,
            count_fetcher=count_fetcher,
            target_floor=target_floor,
            cap_ceiling=cap_ceiling,
        )
        for spec in handle_families
    ]

    handle_blocked = [
        p
        for p in probes
        if not p["floor_reachable_current_handle"] and p["floor_reachable_best_handle"]
    ]
    total_reachable_uplift = sum(p["reachable_bronze_uplift"] for p in probes)
    total_supply_uplift = sum(max(p["uplift_vs_current_handle"], 0) for p in probes)

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_recon_no_registry_or_labels_written",
        "purpose": (
            "Measure how much reviewed-Swiss-Prot supply the import gate's evidence handle "
            "recovers when broadened beyond cc_cofactor to keyword / binding-site / active-site "
            "corroborators -- the within-Swiss-Prot fix to do BEFORE expanding source classes."
        ),
        "leakage_note": (
            "All handles are reviewed annotation used for SCOPE/admission only (they belong in "
            "excluded_context, never predictive features) -- the same basis as the existing "
            "cofactor+EC handle. EC is scope only and is NOT counted as a corroborator."
        ),
        "guardrails": {
            "registry_written": False,
            "labels_created": False,
            "frozen_current702_benchmark_preserved": True,
            "ec_keyword_used_for_scope_estimate_only_never_predictive": True,
            "network_via_injected_fetchers_offline_testable": True,
        },
        "counts": {
            "families_probed": len(probes),
            "handle_blocked_families_unlocked_by_better_handle": len(handle_blocked),
            "handle_blocked_family_ids": [p["family"] for p in handle_blocked],
            "total_reviewed_supply_uplift_over_current_handles": total_supply_uplift,
            "total_reachable_positive_bronze_uplift": total_reachable_uplift,
        },
        "honest_reading": (
            f"Across {len(probes)} families, broadening the corroborator handle beyond cc_cofactor "
            f"recovers ~{total_supply_uplift} reviewed entries the cofactor handle misses (RAW and "
            "illustrative -- the broad EC 1.* lane overlaps the EC 1.1.1 lane, so supply pools "
            "OVERLAP and this is headroom, not additive distinct supply), and "
            f"~{total_reachable_uplift} additional reachable POSITIVE bronze once the cap + "
            f"novelty discount are applied (the bounded, non-inflated figure) -- "
            f"{len(handle_blocked)} families cross the 100-floor only with the better handle. This "
            "is real reviewed supply, not source expansion: it is counted as positive_bronze and "
            "never merged with OOS / silver. The winning handles (keyword / binding-site / "
            "active-site) are the corroborators to wire into the import gate per family BEFORE "
            "admitting sources beyond reviewed Swiss-Prot; the big pools (broad oxidoreductase) "
            "must be split by EC-subclass into capped lanes, not sourced as one bucket."
        ),
        "family_probes": probes,
    }


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    lines = [
        "# Evidence-Handle Expansion — recover within-Swiss-Prot supply the cofactor handle misses",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Non-destructive recon (no registry, no labels). Measures how much reviewed supply each",
        "alternative within-Swiss-Prot corroborator handle recovers per family. EC is scope only",
        "(never a corroborator); keyword / binding-site / active-site are reviewed annotation used",
        "for SCOPE/admission only (excluded_context, never predictive).",
        "",
        "## Headline",
        "",
        f"- Families probed: {c['families_probed']}.",
        f"- Handle-blocked families unlocked by a better handle: "
        f"**{c['handle_blocked_families_unlocked_by_better_handle']}** "
        f"({', '.join(c['handle_blocked_family_ids']) or 'none'}).",
        f"- Reviewed supply recovered over current cofactor handles: "
        f"**{c['total_reviewed_supply_uplift_over_current_handles']}**.",
        f"- Additional reachable POSITIVE bronze (capped, discounted): "
        f"**{c['total_reachable_positive_bronze_uplift']}** "
        "(counted as positive_bronze only — never merged with OOS / silver).",
        f"- {audit['honest_reading']}",
        "",
        "## Per-family handle recovery",
        "",
        "| Family | EC ceiling | current handle | best corroborator | recovered | uplift | "
        "reachable bronze (uplift) |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for p in audit["family_probes"]:
        lines.append(
            f"| {p['family']} | {p['ec_ceiling_supply']} | "
            f"{p['current_handle_supply']} | {p['best_corroborated_handle']} | "
            f"{p['recovered_supply']} | {p['uplift_vs_current_handle']} | "
            f"{p['reachable_bronze_best_handle']} ({p['reachable_bronze_uplift']:+d}) |"
        )
    lines.extend(
        [
            "",
            "## Candidate handles measured per family",
            "",
            "| Family | handle | supply | recovery vs EC ceiling |",
            "| --- | --- | --- | --- |",
        ]
    )
    for p in audit["family_probes"]:
        for h in p["candidate_handle_supplies"]:
            lines.append(
                f"| {p['family']} | {h['handle_id']} | {h['reviewed_supply']} | "
                f"{h['recovery_ratio_vs_ec_ceiling']} |"
            )
    lines.extend(
        [
            "",
            "## Recommended entry-level corroborators (not header-countable — wire at sourcing)",
            "",
        ]
    )
    for p in audit["family_probes"]:
        recs = p.get("recommended_entry_level_corroborators") or []
        if recs:
            lines.append(f"- **{p['family']}**: {', '.join(recs)}.")
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            f"- {audit['leakage_note']}",
            "- No registry written; no labels created; frozen current702 preserved.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_evidence_handle_expansion(
    *,
    out_path: Path,
    report_path: Path | None = None,
    handle_families: tuple[dict[str, Any], ...] = HANDLE_FAMILIES,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    count_fetcher: Callable[[str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the recon and write the artifact + report (non-destructive)."""
    audit = build_evidence_handle_expansion(
        handle_families=handle_families,
        target_floor=target_floor,
        cap_ceiling=cap_ceiling,
        count_fetcher=count_fetcher,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
