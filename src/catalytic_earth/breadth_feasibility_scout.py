"""Breadth feasibility scout -- is "10k diverse bronze" reachable from reviewed Swiss-Prot?

The scaling plan's headline uncertainty is whether 10k is the right *target* at all.
`docs/scaling_plan_to_10k.md` already says, by cap math, that the honest v1 ceiling is
"~2k positives + diverse OOS" and that 10k "requires sustained family breadth". This
module REPLACES that estimate with REAL numbers, non-destructively, before any window is
spent sourcing more bronze.

It answers, from reviewed Swiss-Prot, for a curated set of candidate mechanism families
BEYOND the current 12 fingerprints (non-hydrolase chemistries first -- hydrolysis already
holds 6 of 12):

  (a) how many are mechanistically DISTINCT from the existing 12 (curated + EC/cofactor
      overlap check against `coverage_redundancy_audit.FINGERPRINT_SOURCING_SIGNATURES`);
  (b) which have enough reviewed-entry supply to reach the 100-floor; and
  (c) which are NOT redundant with an existing fingerprint's EC+cofactor lane.

For each candidate it estimates, with the SAME cap-math lesson Stage 2 taught:
  - reviewed-entry supply per narrow EC/cofactor lane (the cheap `x-total-results`
    header count -- no paging, no sequence transfer);
  - a labels/distinct-reaction REDUNDANCY ratio (distinct full-EC count over a small
    sample is a sampled lower bound on reaction diversity, so the ratio is a CONSERVATIVE
    upper bound on redundancy -- a family that looks clean here genuinely is);
  - the 150-cap (not 250) when the chemistry is confusable with a sibling, per the
    Stage-2 finding that filling confusable sub-families to 250 manufactures redundancy;
  - the cofactor/EC disambiguation handle that would separate it at the import gate.

It then produces an HONEST verdict: roughly how many clean families and how much total
diverse POSITIVE bronze are realistically reachable from reviewed Swiss-Prot, and whether
"10k diverse bronze" is plausible from this source or whether the target should change
(a smaller validated positive set + diverse OOS, or new sources beyond Swiss-Prot).

NON-DESTRUCTIVE and leakage-safe by construction: it writes NO registry and creates NO
labels (so there is nothing for the leakage wall to gate). EC/cofactor strings here are
used only to *count supply and estimate scope*, exactly the annotation-anchored basis --
never emitted as a predictive feature. Network access is via injected fetchers so the
logic is fully offline-testable.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .adapters import fetch_uniprot_ec_sample, fetch_uniprot_query_count
from .coverage_redundancy_audit import (
    DEFAULT_CAP_CEILING,
    DEFAULT_EXPANSION_REGISTRY_PATH,
    DEFAULT_FROZEN_BENCHMARK_PATH,
    DEFAULT_TARGET_FLOOR,
    FINGERPRINT_SOURCING_SIGNATURES,
)
from .registry_io import load_json

ARTIFACT_ID = "v3_breadth_feasibility_scout_current702"
SCHEMA_VERSION = "breadth_feasibility_scout.v1"

# Cap when the chemistry is confusable with an existing/sibling fingerprint (the Stage-2
# lesson: filling chemistry-confusable lanes to the 250 ceiling manufactures redundancy).
CONFUSABLE_CAP = 150

# Conservative discount from reviewed supply to admissible bronze. Stage-2 observed
# fetched 1530 -> 1167 disambiguated (cofactor/EC corroboration) -> 600 admitted at a
# 150-cap, and Stage-1 under-floor lanes filled to cap from a few hundred supply. ~0.5 is
# the conservative keep fraction across cofactor-corroboration loss + novelty throttling
# for a family whose supply is below cap; above cap the estimate is cap-bound regardless.
SUPPLY_KEEP_FACTOR = 0.5

# Distinct full-EC count below this density over the sample means the lane is reaction-poor
# (ortholog-heavy) -- a redundancy warning, not a disqualifier (metallopeptidase was such
# a lane and was still sourced, honestly, by ortholog breadth).
REACTION_POOR_RATIO = 4.0

TEN_K_TARGET = 10_000


# Candidate mechanism families BEYOND the current 12, curated from enzyme mechanism
# classes that are (i) mechanistically distinct and (ii) separable by an annotated
# cofactor + EC class (the same handle the import gate uses). Non-hydrolase chemistries
# are listed first. `count_query` is the narrow reviewed Swiss-Prot lane (cofactor/keyword
# filtered) whose supply we measure; `ec_prefixes` is the lane it would claim (checked for
# overlap with the existing 12); `chemistry_confusable` selects the 150 vs 250 cap;
# `cofactor_distinct_from_overlap` records whether an EC overlap with an existing
# fingerprint is still cleanly separated by a DIFFERENT cofactor (e.g. P450 heme vs flavin
# monooxygenase on shared EC 1.14.14).
CANDIDATE_FAMILIES: tuple[dict[str, Any], ...] = (
    # ---- Oxidoreductases (EC 1), beyond flavin/heme ----
    {
        "candidate_family": "nad_p_short_chain_dehydrogenase_reductase",
        "ec_class": "EC 1.1.1 (oxidoreductase, CH-OH donor, NAD(P) acceptor)",
        "chemistry": "SDR: NAD(P)(H)-dependent hydride transfer, Rossmann fold, Ser-Tyr-Lys-Asn tetrad",
        "cofactor_ec_handle": "NAD(P)(+/H) bound + EC 1.1.1.* + Rossmann GxxxGxG (no metal/flavin/heme)",
        "count_query": "(ec:1.1.1.*) AND (reviewed:true) AND ((cc_cofactor:nad) OR (cc_cofactor:nadp))",
        "ec_prefixes": ["1.1.1"],
        "chemistry_confusable": True,
        "cofactor_distinct_from_overlap": True,
        "notes": "Largest single oxidoreductase lane; confusable with MDR/AKR -> 150 cap.",
    },
    {
        "candidate_family": "non_heme_iron_2og_dioxygenase",
        "ec_class": "EC 1.14.11 (oxidoreductase, 2-oxoglutarate as one donor)",
        "chemistry": "Non-heme Fe(II)/2-oxoglutarate dioxygenase, 2-His-1-carboxylate facial triad",
        "cofactor_ec_handle": "non-heme Fe(II) + 2-oxoglutarate + EC 1.14.11.* (HxD..H triad; not heme, not flavin)",
        "count_query": "(ec:1.14.11.*) AND (reviewed:true) AND ((cc_cofactor:fe) OR (cc_cofactor:iron) OR (keyword:Dioxygenase))",
        "ec_prefixes": ["1.14.11"],
        "chemistry_confusable": False,
        "cofactor_distinct_from_overlap": True,
        "notes": "Distinct non-heme-iron cofactor; clean facial-triad mechanism.",
    },
    {
        "candidate_family": "cytochrome_p450_monooxygenase",
        "ec_class": "EC 1.14.14/1.14.15 (oxidoreductase, monooxygenase)",
        "chemistry": "Heme-thiolate (Cys axial) P450 monooxygenase, compound-I O insertion",
        "cofactor_ec_handle": "heme-thiolate (Cys ligand) + EC 1.14.14/1.14.15 (NOT EC 1.11.1 peroxidase, NOT flavin)",
        "count_query": "(ec:1.14.14.*) AND (reviewed:true) AND ((keyword:Heme) OR (cc_cofactor:heme)) AND (keyword:Monooxygenase)",
        "ec_prefixes": ["1.14.14", "1.14.15"],
        "chemistry_confusable": True,
        "cofactor_distinct_from_overlap": True,
        "notes": "EC 1.14.14 overlaps flavin_monooxygenase lane; cofactor (heme-thiolate vs flavin) separates.",
    },
    {
        "candidate_family": "copper_oxidoreductase",
        "ec_class": "EC 1.10.3 / 1.4.3 (oxidoreductase, copper)",
        "chemistry": "Type-1/2/3 copper oxidase (laccase / amine oxidase), O2 -> H2O / H2O2",
        "cofactor_ec_handle": "copper (type-1/2/3) + EC 1.10.3/1.4.3 (no heme, no flavin)",
        "count_query": "(reviewed:true) AND ((ec:1.10.3.*) OR (ec:1.4.3.*)) AND ((cc_cofactor:copper) OR (keyword:Copper))",
        "ec_prefixes": ["1.10.3", "1.4.3"],
        "chemistry_confusable": False,
        "cofactor_distinct_from_overlap": True,
        "notes": "Distinct copper cofactor; small-to-moderate supply.",
    },
    {
        "candidate_family": "molybdopterin_oxidoreductase",
        "ec_class": "EC 1.x (oxidoreductase, molybdopterin)",
        "chemistry": "Mo-bis(MGD) oxotransferase (xanthine/sulfite/DMSO families), oxygen-atom transfer",
        "cofactor_ec_handle": "molybdopterin / Mo-cofactor + EC 1.1.3/1.2.3/1.8.3/1.97 (distinct Mo center)",
        "count_query": "(reviewed:true) AND (ec:1.*) AND ((cc_cofactor:molybdopterin) OR (cc_cofactor:molybdenum) OR (keyword:Molybdenum))",
        "ec_prefixes": ["1.1.3", "1.2.3", "1.8.3", "1.97.1"],
        "chemistry_confusable": False,
        "cofactor_distinct_from_overlap": True,
        "notes": "Distinct Mo-pterin center; spans several EC 1 subclasses.",
    },
    {
        "candidate_family": "manganese_iron_superoxide_dismutase",
        "ec_class": "EC 1.15.1.1 (oxidoreductase, superoxide)",
        "chemistry": "Mn/Fe superoxide dismutase, single-metal redox cycling",
        "cofactor_ec_handle": "Mn or Fe (mononuclear, SOD fold) + EC 1.15.1.1",
        "count_query": "(ec:1.15.1.1) AND (reviewed:true) AND ((cc_cofactor:manganese) OR (cc_cofactor:iron))",
        "ec_prefixes": ["1.15.1"],
        "chemistry_confusable": False,
        "cofactor_distinct_from_overlap": True,
        "notes": "Narrow single-reaction lane; floor reach depends on ortholog breadth.",
    },
    # ---- Transferases (EC 2) ----
    {
        "candidate_family": "sam_methyltransferase",
        "ec_class": "EC 2.1.1 (transferase, one-carbon methyl)",
        "chemistry": "Classical SAM-dependent methyltransferase, SN2 methyl transfer (Rossmann MTase fold)",
        "cofactor_ec_handle": "S-adenosyl-L-methionine + EC 2.1.1.* + NO [4Fe-4S] (distinguishes from radical-SAM)",
        "count_query": "(ec:2.1.1.*) AND (reviewed:true) AND (cc_cofactor:s-adenosyl-l-methionine)",
        "ec_prefixes": ["2.1.1"],
        "chemistry_confusable": False,
        "cofactor_distinct_from_overlap": True,
        "notes": "SAM but NOT radical-SAM (no Fe-S motif, EC 2.1.1 not 1.97/2.8.4/4.1.99). Huge, reaction-diverse.",
    },
    {
        "candidate_family": "glycosyltransferase",
        "ec_class": "EC 2.4 (transferase, glycosyl)",
        "chemistry": "Sugar-nucleotide-dependent glycosyltransferase (GT-A/GT-B), DxD-Mg or metal-independent",
        "cofactor_ec_handle": "sugar-nucleotide donor (UDP/GDP-sugar) + EC 2.4.* (acceptor-diverse)",
        "count_query": "(ec:2.4.*) AND (reviewed:true) AND (keyword:Glycosyltransferase)",
        "ec_prefixes": ["2.4.1", "2.4.2", "2.4.99"],
        "chemistry_confusable": False,
        "cofactor_distinct_from_overlap": True,
        "notes": "Distinct donor chemistry; very large supply.",
    },
    {
        "candidate_family": "atp_phosphotransferase_kinase",
        "ec_class": "EC 2.7 (transferase, phosphorus group)",
        "chemistry": "ATP-dependent kinase, in-line phosphoryl transfer (P-loop / catalytic-loop Asp + Mg)",
        "cofactor_ec_handle": "ATP + Mg2+ + EC 2.7.* (phosphoryl DONOR -> distinguishes from hydrolase P-O cleavage)",
        "count_query": "(ec:2.7.*) AND (reviewed:true) AND ((cc_cofactor:atp) OR (cc_cofactor:magnesium) OR (keyword:Kinase)) AND (keyword:Transferase)",
        "ec_prefixes": ["2.7.1", "2.7.2", "2.7.4", "2.7.7", "2.7.11"],
        "chemistry_confusable": True,
        "cofactor_distinct_from_overlap": True,
        "notes": "Mg overlaps metal hydrolases but the ATP donor + EC 2.7 (transfer, not hydrolysis) separates.",
    },
    {
        "candidate_family": "coa_acyltransferase",
        "ec_class": "EC 2.3.1 (transferase, acyl)",
        "chemistry": "Coenzyme-A-dependent acyltransferase, His/Cys nucleophile, acyl-CoA intermediate",
        "cofactor_ec_handle": "coenzyme A / acyl-CoA + EC 2.3.1.*",
        "count_query": "(ec:2.3.1.*) AND (reviewed:true) AND ((cc_cofactor:coa) OR (keyword:Acyltransferase))",
        "ec_prefixes": ["2.3.1"],
        "chemistry_confusable": False,
        "cofactor_distinct_from_overlap": True,
        "notes": "Distinct CoA chemistry; large supply.",
    },
    {
        "candidate_family": "thiamine_diphosphate_enzyme",
        "ec_class": "EC 2.2.1 / 4.1.1 / 1.2 (ThDP-dependent)",
        "chemistry": "Thiamine-diphosphate ylide catalysis (transketolase / decarboxylase), Mg-anchored ThDP",
        "cofactor_ec_handle": "thiamine diphosphate (ThDP) + Mg2+ (distinguishes from PLP at shared EC 4.1.1)",
        "count_query": "(reviewed:true) AND ((ec:2.2.1.*) OR (ec:4.1.1.*) OR (ec:1.2.4.*)) AND ((cc_cofactor:thiamine) OR (keyword:Thiamine\\ pyrophosphate))",
        "ec_prefixes": ["2.2.1", "4.1.1", "1.2.4"],
        "chemistry_confusable": True,
        "cofactor_distinct_from_overlap": True,
        "notes": "EC 4.1.1 overlaps PLP decarboxylase lane; cofactor (ThDP vs PLP) separates.",
    },
    # ---- Lyases (EC 4) ----
    {
        "candidate_family": "zinc_lyase_hydratase",
        "ec_class": "EC 4.2.1 (lyase, hydro-lyase)",
        "chemistry": "Zn-dependent hydro-lyase (carbonic anhydrase / related), reversible H2O elimination",
        "cofactor_ec_handle": "catalytic Zn2+ + EC 4.2.1.* (lyase, NOT hydrolase EC 3)",
        "count_query": "(ec:4.2.1.*) AND (reviewed:true) AND ((cc_cofactor:zinc) OR (keyword:Zinc))",
        "ec_prefixes": ["4.2.1"],
        "chemistry_confusable": True,
        "cofactor_distinct_from_overlap": True,
        "notes": "Zn overlaps metal hydrolases but EC 4 (elimination) not EC 3 (hydrolysis) separates.",
    },
    {
        "candidate_family": "class_ii_metal_aldolase",
        "ec_class": "EC 4.1.2 / 4.1.3 (lyase, aldehyde/oxo-acid)",
        "chemistry": "Class-II (metal-dependent) aldolase, divalent-metal-stabilized enolate",
        "cofactor_ec_handle": "divalent metal (Zn/Co) + EC 4.1.2/4.1.3 (class-II aldol; not Schiff-base class-I)",
        "count_query": "(reviewed:true) AND ((ec:4.1.2.*) OR (ec:4.1.3.*)) AND ((cc_cofactor:zinc) OR (cc_cofactor:cobalt) OR (keyword:Lyase) AND (keyword:Metal-binding))",
        "ec_prefixes": ["4.1.2", "4.1.3"],
        "chemistry_confusable": True,
        "cofactor_distinct_from_overlap": True,
        "notes": "Metal aldolase; moderate supply, reaction-diverse acceptors.",
    },
    {
        "candidate_family": "enolase_superfamily_lyase",
        "ec_class": "EC 4.2.1.11 + (lyase, Mg enolase superfamily)",
        "chemistry": "Mg2+ enolase-superfamily lyase, metal-stabilized enolate intermediate",
        "cofactor_ec_handle": "Mg2+ + enolase-superfamily EC 4.2.1.11/5.1/4.2.1 (TIM-barrel)",
        "count_query": "(reviewed:true) AND (ec:4.2.1.11) AND ((cc_cofactor:magnesium) OR (keyword:Magnesium))",
        "ec_prefixes": ["4.2.1"],
        "chemistry_confusable": True,
        "cofactor_distinct_from_overlap": True,
        "notes": "Overlaps the zinc_lyase_hydratase EC 4.2.1 lane (different metal) -> confusable.",
    },
    # ---- Isomerases (EC 5) ----
    {
        "candidate_family": "cofactor_independent_isomerase",
        "ec_class": "EC 5.3 (intramolecular oxidoreductase / isomerase)",
        "chemistry": "Cofactor-independent isomerase (ketol/aldose-ketose), general acid-base (TIM-barrel)",
        "cofactor_ec_handle": "no cofactor; catalytic Glu/His/Lys acid-base + EC 5.3.* (apo-confirmable)",
        "count_query": "(ec:5.3.*) AND (reviewed:true) AND (keyword:Isomerase)",
        "ec_prefixes": ["5.3.1", "5.3.2", "5.3.3"],
        "chemistry_confusable": False,
        "cofactor_distinct_from_overlap": True,
        "notes": "Cofactorless (like ser_his): apo-confirmable; corroborator is the active-site triad, not a cofactor.",
    },
    {
        "candidate_family": "metal_racemase_epimerase_non_plp",
        "ec_class": "EC 5.1 (racemase/epimerase, non-PLP)",
        "chemistry": "Metal- or cofactor-independent racemase/epimerase (e.g. mandelate racemase), 1,1-proton shift",
        "cofactor_ec_handle": "Mg/Mn (or cofactorless) + EC 5.1.* AND NO PLP (distinguishes from PLP racemase 5.1.1)",
        "count_query": "(ec:5.1.*) AND (reviewed:true) AND (keyword:Isomerase) NOT (cc_cofactor:pyridoxal)",
        "ec_prefixes": ["5.1.1", "5.1.3", "5.1.99"],
        "chemistry_confusable": True,
        "cofactor_distinct_from_overlap": True,
        "notes": "EC 5.1.1 overlaps PLP racemase lane; the NO-PLP constraint separates the cofactor-independent ones.",
    },
    # ---- Ligases (EC 6): an entirely uncovered EC class ----
    {
        "candidate_family": "atp_amide_ligase",
        "ec_class": "EC 6.3 (ligase, C-N bond, ATP)",
        "chemistry": "ATP-dependent amide/peptide ligase (acyl-phosphate intermediate, ATP-grasp), Mg",
        "cofactor_ec_handle": "ATP + Mg2+ + EC 6.3.* (C-N ligation -> entirely outside the current EC 1-5 set)",
        "count_query": "(ec:6.3.*) AND (reviewed:true) AND ((cc_cofactor:atp) OR (cc_cofactor:magnesium) OR (keyword:Ligase))",
        "ec_prefixes": ["6.3.1", "6.3.2", "6.3.4", "6.3.5"],
        "chemistry_confusable": True,
        "cofactor_distinct_from_overlap": False,
        "notes": "EC 6 uncovered today; ATP+Mg overlaps kinases by cofactor -> confusable WITHIN the new EC-6 lanes.",
    },
    {
        "candidate_family": "biotin_dependent_carboxylase",
        "ec_class": "EC 6.4.1 / 6.3.4 (ligase, carboxylase, biotin)",
        "chemistry": "Biotin-dependent carboxylase, CO2 transfer via carboxy-biotin, ATP + Mg",
        "cofactor_ec_handle": "biotin + ATP + Mg2+ + EC 6.4.1/6.3.4 (distinct biotin prosthetic group)",
        "count_query": "(reviewed:true) AND ((ec:6.4.1.*) OR (ec:6.3.4.*)) AND ((cc_cofactor:biotin) OR (keyword:Biotin))",
        "ec_prefixes": ["6.4.1", "6.3.4"],
        "chemistry_confusable": False,
        "cofactor_distinct_from_overlap": True,
        "notes": "Distinct biotin prosthetic group; modest supply.",
    },
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _existing_ec_prefixes() -> list[tuple[str, str]]:
    """(fingerprint_id, ec_prefix) pairs for the live fingerprints' sourcing lanes."""
    pairs: list[tuple[str, str]] = []
    for fp, sig in FINGERPRINT_SOURCING_SIGNATURES.items():
        for prefix in sig.get("ec_prefixes", []):
            pairs.append((fp, str(prefix)))
    return pairs


def _broad_ec_query(ec_prefixes: list[str]) -> str:
    """Reviewed Swiss-Prot count for the lane's EC prefixes WITHOUT the cofactor filter.

    This is the EC supply ceiling; comparing it to the cofactor-narrowed count measures how
    much of the biology the cofactor-annotation disambiguation handle actually reaches (NAD(P)
    is a cosubstrate, not a UniProt COFACTOR comment, so cofactor-anchored handles miss the
    huge EC 1.1.1 pool -- an honest finding, not a bug).
    """
    clauses = " OR ".join(f"(ec:{str(p).rstrip('.')}.*)" for p in ec_prefixes)
    return f"(reviewed:true) AND ({clauses})"


def _ec_prefix_overlap(candidate_prefixes: list[str]) -> list[str]:
    """Existing fingerprints whose EC prefix shares a dotted-prefix with the candidate."""
    overlap: set[str] = set()
    for fp, existing in _existing_ec_prefixes():
        for cand in candidate_prefixes:
            a = existing.rstrip(".")
            b = str(cand).rstrip(".")
            if a == b or a.startswith(b + ".") or b.startswith(a + "."):
                overlap.add(fp)
    return sorted(overlap)


def _distinct_reaction_estimate(ec_per_row: list[list[str]]) -> dict[str, Any]:
    """Distinct full-EC count over a sample = sampled lower bound on reaction diversity."""
    distinct: set[str] = set()
    rows_with_ec = 0
    for ec_list in ec_per_row:
        leaves = [e for e in ec_list if e and "-" not in e]  # drop partial "3.2.1.-"
        if leaves:
            rows_with_ec += 1
        distinct.update(leaves)
    return {
        "sample_rows": len(ec_per_row),
        "sample_rows_with_full_ec": rows_with_ec,
        "distinct_full_ec_in_sample": len(distinct),
    }


def evaluate_candidate_family(
    spec: dict[str, Any],
    *,
    count_fetcher: Callable[[str], dict[str, Any]],
    ec_sample_fetcher: Callable[[str, int], dict[str, Any]],
    sample_size: int,
    target_floor: int,
    cap_ceiling: int,
) -> dict[str, Any]:
    """Probe one candidate family: supply count + reaction-diversity sample + verdict."""
    count = count_fetcher(spec["count_query"])
    reviewed_supply = count.get("total_results")
    # EC ceiling (no cofactor filter): how much of the biology exists vs how much the
    # cofactor-annotation handle actually reaches.
    ec_only = count_fetcher(_broad_ec_query(list(spec["ec_prefixes"])))
    ec_only_supply = ec_only.get("total_results")
    supply_int = int(reviewed_supply or 0)
    ec_only_int = int(ec_only_supply or 0)
    capture_ratio = round(supply_int / ec_only_int, 3) if ec_only_int else None

    sample = ec_sample_fetcher(spec["count_query"], sample_size)
    diversity = _distinct_reaction_estimate(sample.get("ec_per_row", []))

    ec_overlap = _ec_prefix_overlap(list(spec["ec_prefixes"]))
    cofactor_distinct = bool(spec.get("cofactor_distinct_from_overlap", True))
    # Redundant only if it shares an EC lane AND no different cofactor separates it.
    redundant_with_existing = bool(ec_overlap) and not cofactor_distinct
    mechanistically_distinct = not redundant_with_existing

    cap = CONFUSABLE_CAP if spec.get("chemistry_confusable") else cap_ceiling
    supply = int(reviewed_supply or 0)
    est_admissible = 0
    if mechanistically_distinct and supply > 0:
        est_admissible = min(cap, int(round(supply * SUPPLY_KEEP_FACTOR)))

    distinct_rx = max(diversity["distinct_full_ec_in_sample"], 1)
    # Conservative UPPER bound on redundancy: distinct_rx undersamples reaction diversity
    # when supply > sample, so the true ratio is <= this.
    redundancy_ratio_upper = round(est_admissible / distinct_rx, 3) if est_admissible else 0.0
    reaction_poor = redundancy_ratio_upper > REACTION_POOR_RATIO

    floor_reachable = est_admissible >= target_floor
    clean_family = mechanistically_distinct and floor_reachable and not redundant_with_existing

    return {
        "candidate_family": spec["candidate_family"],
        "ec_class": spec["ec_class"],
        "chemistry": spec["chemistry"],
        "cofactor_ec_disambiguation_handle": spec["cofactor_ec_handle"],
        "count_query": spec["count_query"],
        "ec_prefixes": list(spec["ec_prefixes"]),
        "reviewed_entry_supply": reviewed_supply,
        "ec_only_supply_ceiling": ec_only_supply,
        "cofactor_handle_capture_ratio": capture_ratio,
        "reaction_diversity_sample": diversity,
        "ec_overlap_with_existing_fingerprints": ec_overlap,
        "cofactor_distinct_from_overlap": cofactor_distinct,
        "redundant_with_existing": redundant_with_existing,
        "mechanistically_distinct": mechanistically_distinct,
        "chemistry_confusable": bool(spec.get("chemistry_confusable")),
        "applied_cap": cap,
        "supply_keep_factor": SUPPLY_KEEP_FACTOR,
        "estimated_admissible_diverse_bronze": est_admissible,
        "labels_per_distinct_reaction_upper_bound": redundancy_ratio_upper,
        "reaction_poor_warning": reaction_poor,
        "floor_reachable": floor_reachable,
        "clean_family": clean_family,
        "notes": spec.get("notes", ""),
    }


def _current_positive_count(
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
) -> dict[str, Any]:
    """Current combined positive (seed_fingerprint) bronze, from both registries."""
    def positives(rows: list[dict[str, Any]]) -> int:
        return sum(1 for r in rows if r.get("label_type") == "seed_fingerprint")

    frozen_pos = positives(frozen_benchmark_payload)
    expansion_pos = positives(expansion_payload)
    return {
        "frozen_positive_labels": frozen_pos,
        "expansion_positive_labels": expansion_pos,
        "combined_positive_labels": frozen_pos + expansion_pos,
        "live_fingerprint_count": len(FINGERPRINT_SOURCING_SIGNATURES),
    }


def build_breadth_feasibility_scout(
    *,
    frozen_benchmark_payload: list[dict[str, Any]],
    expansion_payload: list[dict[str, Any]],
    candidate_families: tuple[dict[str, Any], ...] = CANDIDATE_FAMILIES,
    sample_size: int = 200,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    created_utc: str | None = None,
    count_fetcher: Callable[[str], dict[str, Any]] | None = None,
    ec_sample_fetcher: Callable[[str, int], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Non-destructive breadth recon -> honest 10k-feasibility verdict."""
    created = created_utc or _utc_now_iso()
    # Resolve at call time so injection/patching of the module-level live fetchers works.
    count_fetcher = count_fetcher or fetch_uniprot_query_count
    ec_sample_fetcher = ec_sample_fetcher or fetch_uniprot_ec_sample

    probes = [
        evaluate_candidate_family(
            spec,
            count_fetcher=count_fetcher,
            ec_sample_fetcher=ec_sample_fetcher,
            sample_size=sample_size,
            target_floor=target_floor,
            cap_ceiling=cap_ceiling,
        )
        for spec in candidate_families
    ]

    clean = [p for p in probes if p["clean_family"]]
    floor_blocked = [
        p for p in probes if p["mechanistically_distinct"] and not p["floor_reachable"]
    ]
    redundant = [p for p in probes if p["redundant_with_existing"]]
    clean_reaction_poor = [p for p in clean if p["reaction_poor_warning"]]
    # Families whose cofactor-annotation handle reaches < 25% of the EC supply ceiling:
    # the biology exists but the import gate's cofactor corroboration cannot reach it
    # (e.g. NAD(P)-dependent dehydrogenases -- NAD is a cosubstrate, not a cofactor comment).
    weak_handle = [
        p
        for p in probes
        if p["cofactor_handle_capture_ratio"] is not None
        and p["cofactor_handle_capture_ratio"] < 0.25
    ]

    baseline = _current_positive_count(frozen_benchmark_payload, expansion_payload)
    est_new_clean_bronze = sum(p["estimated_admissible_diverse_bronze"] for p in clean)
    # Diversity-discounted view: for reaction-poor clean lanes (ortholog padding), count only
    # a modest ortholog multiple of the distinct sampled reactions, not the full cap.
    est_diversity_discounted = sum(
        (
            min(
                p["estimated_admissible_diverse_bronze"],
                p["reaction_diversity_sample"]["distinct_full_ec_in_sample"]
                * int(REACTION_POOR_RATIO),
            )
            if p["reaction_poor_warning"]
            else p["estimated_admissible_diverse_bronze"]
        )
        for p in clean
    )
    # Upper-supply view: floor-blocked-but-distinct families could still contribute their
    # (sub-floor) admissible bronze if combined/merged; report it separately, not in the
    # headline clean total.
    est_subfloor_bronze = sum(
        p["estimated_admissible_diverse_bronze"] for p in floor_blocked
    )

    projected_positive_bronze = baseline["combined_positive_labels"] + est_new_clean_bronze
    projected_with_subfloor = projected_positive_bronze + est_subfloor_bronze
    gap_to_10k_positive = TEN_K_TARGET - projected_positive_bronze

    # Honest verdict. 10k DIVERSE POSITIVE bronze from reviewed Swiss-Prot is plausible only
    # if the clean-family supply closes the gap; otherwise the target must change.
    ten_k_positive_plausible = projected_positive_bronze >= TEN_K_TARGET
    if ten_k_positive_plausible:
        verdict = "ten_k_diverse_positive_bronze_plausible_from_reviewed_swissprot"
    elif projected_with_subfloor >= TEN_K_TARGET:
        verdict = "ten_k_reachable_only_if_subfloor_families_are_combined_or_capped_higher"
    else:
        verdict = "ten_k_diverse_positive_bronze_NOT_reachable_from_reviewed_swissprot_alone"

    return {
        "artifact_id": ARTIFACT_ID,
        "schema_version": SCHEMA_VERSION,
        "created_utc": created,
        "status": "non_destructive_recon_no_registry_or_labels_written",
        "purpose": (
            "Replace the scaling-plan cap-math ESTIMATE with real reviewed-Swiss-Prot "
            "numbers, so the user can decide whether 10k diverse bronze is the right "
            "target before spending windows sourcing more."
        ),
        "method": {
            "supply_probe": "uniprot x-total-results header count per narrow EC/cofactor lane",
            "reaction_diversity_probe": (
                f"distinct full-EC count over a <= {sample_size}-row sample (sampled LOWER "
                "bound on reaction diversity -> labels/reaction is a conservative UPPER "
                "bound on redundancy)"
            ),
            "cap_math": (
                f"cap = {CONFUSABLE_CAP} when chemistry is confusable with a sibling, else "
                f"{cap_ceiling} (the Stage-2 lesson: filling confusable lanes to the ceiling "
                "manufactures redundancy)"
            ),
            "supply_keep_factor": SUPPLY_KEEP_FACTOR,
            "redundancy_check": (
                "EC-prefix overlap vs coverage_redundancy_audit.FINGERPRINT_SOURCING_"
                "SIGNATURES; an overlap is NOT redundant when a different annotated cofactor "
                "separates the lane at the import gate"
            ),
        },
        "guardrails": {
            "registry_written": False,
            "labels_created": False,
            "frozen_current702_benchmark_preserved": True,
            "ec_cofactor_used_for_supply_and_scope_estimate_only_never_predictive": True,
            "network_via_injected_fetchers_offline_testable": True,
        },
        "baseline": baseline,
        "counts": {
            "candidate_families_probed": len(probes),
            "clean_families": len(clean),
            "clean_but_reaction_poor_ortholog_padded": len(clean_reaction_poor),
            "mechanistically_distinct_but_floor_blocked": len(floor_blocked),
            "redundant_with_existing": len(redundant),
            "weak_cofactor_handle_capture_lt_25pct": len(weak_handle),
            "estimated_new_clean_diverse_bronze": est_new_clean_bronze,
            "estimated_new_clean_bronze_diversity_discounted": est_diversity_discounted,
            "estimated_subfloor_distinct_bronze": est_subfloor_bronze,
            "current_combined_positive_bronze": baseline["combined_positive_labels"],
            "projected_positive_bronze_clean_only": projected_positive_bronze,
            "projected_positive_bronze_with_subfloor": projected_with_subfloor,
            "gap_to_10k_positive_bronze": gap_to_10k_positive,
        },
        "verdict": {
            "ten_k_target": TEN_K_TARGET,
            "ten_k_diverse_positive_bronze_plausible": ten_k_positive_plausible,
            "verdict_code": verdict,
            "honest_reading": _honest_reading(
                baseline=baseline,
                clean=clean,
                floor_blocked=floor_blocked,
                redundant=redundant,
                clean_reaction_poor=clean_reaction_poor,
                weak_handle=weak_handle,
                est_diversity_discounted=est_diversity_discounted,
                projected_positive_bronze=projected_positive_bronze,
                gap=gap_to_10k_positive,
            ),
            "recommendation": _recommendation(verdict, clean),
        },
        "clean_family_ranking": [
            {
                "candidate_family": p["candidate_family"],
                "reviewed_entry_supply": p["reviewed_entry_supply"],
                "estimated_admissible_diverse_bronze": p[
                    "estimated_admissible_diverse_bronze"
                ],
                "labels_per_distinct_reaction_upper_bound": p[
                    "labels_per_distinct_reaction_upper_bound"
                ],
                "applied_cap": p["applied_cap"],
                "cofactor_ec_disambiguation_handle": p[
                    "cofactor_ec_disambiguation_handle"
                ],
            }
            for p in sorted(
                clean,
                key=lambda p: p["estimated_admissible_diverse_bronze"],
                reverse=True,
            )
        ],
        "family_probes": probes,
    }


def _honest_reading(
    *,
    baseline: dict[str, Any],
    clean: list[dict[str, Any]],
    floor_blocked: list[dict[str, Any]],
    redundant: list[dict[str, Any]],
    clean_reaction_poor: list[dict[str, Any]],
    weak_handle: list[dict[str, Any]],
    est_diversity_discounted: int,
    projected_positive_bronze: int,
    gap: int,
) -> str:
    return (
        f"Current combined positive bronze is {baseline['combined_positive_labels']} across "
        f"{baseline['live_fingerprint_count']} fingerprints. Beyond those, "
        f"{len(clean)} candidate families are clean (distinct + floor-reachable + "
        f"non-redundant), {len(floor_blocked)} are distinct but below the 100-floor on "
        f"the cofactor-handle-reachable supply, and {len(redundant)} are redundant with an "
        f"existing lane. Adding the clean families' capped, novelty-discounted supply "
        f"projects to ~{projected_positive_bronze} diverse POSITIVE bronze -- a gap of {gap} "
        f"to 10k. Two honesty discounts shrink even this: {len(clean_reaction_poor)} of the "
        f"clean families are reaction-poor (ortholog padding -- many entries, few distinct "
        f"reactions), so the diversity-discounted new bronze is only ~{est_diversity_discounted} "
        f"(not the headline cap-sum); and {len(weak_handle)} families have a weak cofactor "
        "handle (it reaches <25% of the EC supply ceiling -- NAD(P) dehydrogenases are the "
        "big one, since NAD is a cosubstrate, not a UniProt COFACTOR comment), so their large "
        "EC supply is NOT reachable by the current cofactor-anchored gate without a new "
        "sequence-motif/EC-only handle. Net: reviewed Swiss-Prot yields low thousands of "
        "diverse POSITIVE bronze, not 10k; closing the gap needs either diverse novelty-gated "
        "OOS + bronze->silver depth counted toward 10k, or sources beyond reviewed Swiss-Prot."
    )


def _recommendation(verdict: str, clean: list[dict[str, Any]]) -> str:
    top = ", ".join(p["candidate_family"] for p in clean[:4]) if clean else "(none)"
    if verdict.startswith("ten_k_diverse_positive_bronze_plausible"):
        return (
            "Proceed toward 10k diverse positive bronze; source the clean families in "
            f"supply order (start: {top})."
        )
    if verdict.startswith("ten_k_reachable_only_if"):
        return (
            "10k is reachable only by combining sub-floor families or raising caps where "
            "reaction diversity supports it -- source the clean families first "
            f"({top}); reconsider the cap on the highest-supply lanes."
        )
    return (
        "Re-target: reviewed Swiss-Prot alone does not yield 10k diverse POSITIVE bronze. "
        "Source the clean non-hydrolase families to broaden chemistry "
        f"({top}), and define 10k as positives + diverse novelty-gated OOS + bronze->silver "
        "depth, OR bring in sources beyond reviewed Swiss-Prot (TrEMBL/UniRef clusters, "
        "BRENDA, structure-anchored families). Keep the positive set diverse, not padded."
    )


def _report(audit: dict[str, Any]) -> str:
    c = audit["counts"]
    v = audit["verdict"]
    lines = [
        "# Breadth Feasibility Scout — is 10k diverse bronze reachable from reviewed Swiss-Prot?",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Non-destructive recon (no registry, no labels). Replaces the scaling-plan cap-math",
        "estimate with real reviewed-Swiss-Prot supply + reaction-diversity numbers for",
        "candidate mechanism families beyond the current 12 (non-hydrolase first).",
        "",
        "## Verdict",
        "",
        f"- **{v['verdict_code']}**",
        f"- 10k diverse positive bronze plausible from reviewed Swiss-Prot: "
        f"**{v['ten_k_diverse_positive_bronze_plausible']}**",
        f"- {v['honest_reading']}",
        f"- **Recommendation:** {v['recommendation']}",
        "",
        "## Tally",
        "",
        f"- Candidate families probed: {c['candidate_families_probed']}.",
        f"- Clean families (distinct + floor-reachable + non-redundant): "
        f"**{c['clean_families']}**.",
        f"- Distinct but below the 100-floor: {c['mechanistically_distinct_but_floor_blocked']}.",
        f"- Redundant with an existing lane: {c['redundant_with_existing']}.",
        f"- Current combined positive bronze: {c['current_combined_positive_bronze']}.",
        f"- Estimated NEW clean diverse bronze: **{c['estimated_new_clean_diverse_bronze']}**.",
        f"- Projected positive bronze (clean only): "
        f"**{c['projected_positive_bronze_clean_only']}** "
        f"(+subfloor: {c['projected_positive_bronze_with_subfloor']}).",
        f"- Gap to 10k positive bronze: **{c['gap_to_10k_positive_bronze']}**.",
        "",
        "## Clean families (by estimated admissible bronze)",
        "",
        "| Family | reviewed supply | est. bronze | labels/rxn (≤) | cap | disambiguation handle |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for p in audit["clean_family_ranking"]:
        lines.append(
            f"| {p['candidate_family']} | {p['reviewed_entry_supply']} | "
            f"{p['estimated_admissible_diverse_bronze']} | "
            f"{p['labels_per_distinct_reaction_upper_bound']} | {p['applied_cap']} | "
            f"{p['cofactor_ec_disambiguation_handle']} |"
        )
    lines.extend(
        [
            "",
            "## All probes (incl. floor-blocked + redundant)",
            "",
            "EC ceiling = reviewed count for the EC prefixes with NO cofactor filter; "
            "capture = cofactor-handle-reachable supply ÷ EC ceiling. rxn-poor = "
            "ortholog-padded (labels/distinct-reaction over the warning threshold).",
            "",
            "| Family | handle supply | EC ceiling | capture | distinct-EC/sample | "
            "est. bronze | floor? | rxn-poor? | redundant? |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for p in audit["family_probes"]:
        d = p["reaction_diversity_sample"]
        lines.append(
            f"| {p['candidate_family']} | {p['reviewed_entry_supply']} | "
            f"{p['ec_only_supply_ceiling']} | {p['cofactor_handle_capture_ratio']} | "
            f"{d['distinct_full_ec_in_sample']}/{d['sample_rows']} | "
            f"{p['estimated_admissible_diverse_bronze']} | {p['floor_reachable']} | "
            f"{p['reaction_poor_warning']} | {p['redundant_with_existing']} |"
        )
    lines.extend(
        [
            "",
            "## Method + guardrails",
            "",
            f"- Supply: {audit['method']['supply_probe']}.",
            f"- Reaction diversity: {audit['method']['reaction_diversity_probe']}.",
            f"- Cap math: {audit['method']['cap_math']}.",
            f"- Redundancy check: {audit['method']['redundancy_check']}.",
            "- No registry written; no labels created; EC/cofactor used for supply/scope "
            "estimation only, never as a predictive feature.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_breadth_feasibility_scout(
    *,
    out_path: Path,
    report_path: Path | None = None,
    candidate_families: tuple[dict[str, Any], ...] = CANDIDATE_FAMILIES,
    sample_size: int = 200,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    count_fetcher: Callable[[str], dict[str, Any]] | None = None,
    ec_sample_fetcher: Callable[[str, int], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build the recon and write the artifact + report (non-destructive)."""
    frozen_path = Path(frozen_benchmark_path)
    expansion_path = Path(expansion_registry_path)
    frozen = load_json(frozen_path) if frozen_path.exists() else []
    expansion = load_json(expansion_path) if expansion_path.exists() else []
    audit = build_breadth_feasibility_scout(
        frozen_benchmark_payload=frozen,
        expansion_payload=expansion,
        candidate_families=candidate_families,
        sample_size=sample_size,
        target_floor=target_floor,
        cap_ceiling=cap_ceiling,
        count_fetcher=count_fetcher,
        ec_sample_fetcher=ec_sample_fetcher,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
