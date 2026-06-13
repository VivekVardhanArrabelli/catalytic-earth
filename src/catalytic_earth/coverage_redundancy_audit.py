"""Coverage + redundancy audit and balance-capped acquisition policy.

The expansion has solved *admission* (can we accept a candidate); the binding
constraint at 4x volume is now **diverse, non-redundant supply + honest quality**.
We have so far deduped only on EXACT accession / sequence-SHA -- we have NOT
measured near-duplicate redundancy or class balance of the 1,710 expansion
labels. This module is that measurement, plus the policy it implies.

It is strictly NON-DESTRUCTIVE and metadata-only: it reads both registries
(frozen current702 benchmark + the separate expansion registry) and emits a
reporting artifact (JSON) plus a work report (Markdown). It writes NO registry
and depends on NO network / mmseqs / embedding backend -- redundancy is measured
from the annotation metadata already carried on every label
(``source_provenance`` organism / sequence length / lane, and
``mechanism_evidence`` EC numbers / Rhea reactions).

Two deliverables:

1. **Coverage + redundancy audit** of all combined labels: distribution by
   fingerprint x lane x organism x EC-class x sequence-length; class-imbalance
   flags; and a metadata-only near-duplicate / saturation read (per-fingerprint
   effective reaction diversity, reaction saturation, and ortholog-cluster
   proxies keyed on ``(fingerprint, full-EC, organism, sequence-length bin)``).

2. **A prioritized, balance-capped acquisition target list** built from (1):
   which fingerprints/lanes are HOLES (e.g. ser_his, radical-SAM, cobalamin),
   which to CAP (e.g. metal-dependent hydrolase), and -- per fingerprint -- the
   EC-class / lane / cofactor signatures to source or predict next. This is the
   policy the rest of the climb (more sourcing OR a self-feeding model loop)
   should be driven by.

Guardrails honoured: the frozen 702 benchmark is read-only and never written;
EC/lane/organism are metadata used for *coverage accounting only*, never emitted
as predictive features (this module produces no labels at all).
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_FROZEN_BENCHMARK_PATH = Path("data/registries/curated_mechanism_labels.json")
DEFAULT_EXPANSION_REGISTRY_PATH = Path("data/registries/external_bronze_labels.json")

# The eight seed mechanism fingerprints, with the textbook EC-class / lane /
# cofactor signatures the annotation-anchored engine sources them from (mirrors
# the 2026-06-09 cofactor/EC disambiguation rules). These drive the per-hole
# sourcing hints; they are accounting metadata, never predictive features.
FINGERPRINT_SOURCING_SIGNATURES: dict[str, dict[str, Any]] = {
    "metal_dependent_hydrolase": {
        "ec_prefixes": ["3.4.24", "3.5.2", "3.1.3", "3.1.4"],
        "cofactor": "catalytic divalent metal (Zn2+/Mn2+/Mg2+/Ni2+)",
        "lanes": ["metal hydrolase"],
    },
    # Stage-2 v2 sub-families of metal_dependent_hydrolase (the over-cap umbrella).
    # Separated by reaction-center bond change; each carries a catalytic divalent
    # metal. Accounting metadata only, never predictive features.
    "metallopeptidase": {
        "ec_prefixes": ["3.4.24", "3.4.17", "3.4.11"],
        "cofactor": "catalytic Zn2+ (HExxH / co-catalytic dizinc); peptide C-N hydrolysis",
        "lanes": ["metallopeptidase"],
    },
    "metallophosphoesterase_nuclease": {
        "ec_prefixes": ["3.1.4", "3.1.11", "3.1.21", "3.1.26", "3.1.27", "3.1.31"],
        "cofactor": "two-metal Mg2+/Mn2+ (sometimes Zn2+); phosphodiester P-O hydrolysis",
        "lanes": ["metallophosphoesterase/nuclease"],
    },
    "metallophosphomonoesterase": {
        "ec_prefixes": ["3.1.3"],
        "cofactor": "dinuclear Zn/Mg/Mn/Fe; phosphomonoester P-O hydrolysis (not Cys-PTP)",
        "lanes": ["metallophosphomonoesterase"],
    },
    "metallo_amidohydrolase_deaminase": {
        "ec_prefixes": ["3.5.2", "3.5.4", "3.5.1"],
        "cofactor": "catalytic Zn2+ (mono/di-nuclear); non-peptide amide/amidine C-N hydrolysis",
        "lanes": ["metallo amidohydrolase/deaminase"],
    },
    "ser_his_acid_hydrolase": {
        "ec_prefixes": ["3.4.21", "3.1.1", "3.5.1"],
        "cofactor": "no cofactor; Ser/Cys-His-Asp/Glu catalytic triad",
        "lanes": ["serine/cysteine hydrolase", "esterase/lipase triad"],
    },
    "plp_dependent_enzyme": {
        "ec_prefixes": ["2.6.1", "4.1.1", "4.3.1", "5.1.1", "4.4.1"],
        "cofactor": "pyridoxal-5'-phosphate (PLP) Schiff base",
        "lanes": [
            "PLP lyase/eliminase",
            "PLP decarboxylase",
            "PLP aminotransferase",
            "PLP racemase/epimerase",
            "PLP sulfur lyase boundary",
        ],
    },
    "heme_peroxidase_oxidase": {
        "ec_prefixes": ["1.11.1"],
        "cofactor": "heme b / heme c (peroxidase)",
        "lanes": ["heme peroxidase/oxidase-like"],
    },
    "flavin_monooxygenase": {
        "ec_prefixes": ["1.14.13", "1.14.14"],
        "cofactor": "flavin (FAD/FMN), no heme; inserts one O",
        "lanes": ["flavin monooxygenase"],
    },
    "flavin_dehydrogenase_reductase": {
        "ec_prefixes": ["1.3", "1.6", "1.8.1"],
        "cofactor": "flavin (FAD/FMN), no heme; hydride/electron transfer",
        "lanes": ["flavin redox boundary", "flavin dehydrogenase/reductase"],
    },
    "radical_sam_enzyme": {
        "ec_prefixes": ["1.97.1", "2.8.4", "4.1.99", "2.5.1"],
        "cofactor": "[4Fe-4S] + S-adenosylmethionine (CX3CX2C motif)",
        "lanes": ["radical SAM", "plp_radical_cobalamin"],
    },
    "cobalamin_radical_rearrangement": {
        "ec_prefixes": ["5.4.99", "5.4.3", "4.2.1.28", "4.2.1.30", "4.3.1.7"],
        "cofactor": "adenosylcobalamin / vitamin B12 (radical rearrangement)",
        "lanes": ["cobalamin radical", "plp_radical_cobalamin"],
    },
    # Broadened-handle families (2026-06-12). Their defining corroborator is a dissociable
    # COSUBSTRATE / donor (read as a Rhea participant or functional keyword), NOT a cofactor
    # comment -- `cofactor` below records that deploy-missing context. Accounting metadata only.
    "nad_p_dehydrogenase": {
        "ec_prefixes": ["1.1.1"],
        "cofactor": "NAD(P) cosubstrate (dissociable nicotinamide dinucleotide; Rossmann GxGxxG)",
        "lanes": ["nad_p_dehydrogenase"],
    },
    "glycosyltransferase": {
        "ec_prefixes": ["2.4"],
        "cofactor": "nucleotide-sugar donor (UDP/GDP/dTDP/CMP-sugar; GT-A DxD metal or GT-B cleft)",
        "lanes": ["glycosyltransferase"],
    },
    "sam_methyltransferase": {
        "ec_prefixes": ["2.1.1"],
        "cofactor": "SAM methyl donor / SAH product (dissociable methyl-transfer cosubstrate); no Fe-S radical-SAM context",
        "lanes": ["sam_methyltransferase"],
    },
    "cytochrome_p450_monooxygenase": {
        "ec_prefixes": ["1.14"],
        "cofactor": "heme-thiolate plus O2/reductant cosubstrate; non-peroxidase P450 monooxygenation",
        "lanes": ["cytochrome_p450_monooxygenase"],
    },
    "non_heme_iron_2og_dioxygenase": {
        "ec_prefixes": ["1.14.11"],
        "cofactor": "Fe(II), 2-oxoglutarate, and O2 cosubstrates; non-heme 2OG oxygenation",
        "lanes": ["non_heme_iron_2og_dioxygenase"],
    },
    "coa_acyltransferase": {
        "ec_prefixes": ["2.3.1"],
        "cofactor": "CoA/acyl-CoA donor (dissociable thioester cosubstrate); acyl group transfer",
        "lanes": ["coa_acyltransferase"],
    },
    "cofactor_independent_isomerase": {
        "ec_prefixes": ["5.3"],
        "cofactor": "no cofactor; Rhea isomerization equation plus active-site/base context",
        "lanes": ["cofactor_independent_isomerase"],
    },
    "molybdopterin_oxidoreductase": {
        "ec_prefixes": ["1"],
        "cofactor": "molybdopterin / molybdenum cofactor redox center; Mo/W oxo-transfer or electron-transfer chemistry",
        "lanes": ["molybdopterin_oxidoreductase"],
    },
    "copper_oxidoreductase": {
        "ec_prefixes": ["1.10.3", "1.4.3"],
        "cofactor": "copper redox center; multicopper oxidase or copper amine oxidase oxygen/electron-transfer chemistry",
        "lanes": ["copper_oxidoreductase"],
    },
    "metal_racemase_epimerase_non_plp": {
        "ec_prefixes": ["5.1"],
        "cofactor": "non-PLP racemase/epimerase proton-transfer chemistry; metal or cofactorless active-site context",
        "lanes": ["metal_racemase_epimerase_non_plp"],
    },
    "atp_amide_ligase": {
        "ec_prefixes": ["6.3"],
        "cofactor": "ATP/Mg cosubstrate context; acyl-phosphate-like intermediate and C-N amide ligation",
        "lanes": ["atp_amide_ligase"],
    },
    "class_ii_metal_aldolase": {
        "ec_prefixes": ["4.1.2", "4.1.3"],
        "cofactor": "Zn/Co/divalent metal; enolate-stabilized aldol C-C lyase chemistry",
        "lanes": ["class_ii_metal_aldolase"],
    },
    "thiamine_diphosphate_enzyme": {
        "ec_prefixes": ["2.2.1", "4.1.1", "1.2.4"],
        "cofactor": "ThDP/Mg ylide cofactor context; decarboxylation, carbonyl transfer, or 2-oxoacid dehydrogenase E1 chemistry",
        "lanes": ["thiamine_diphosphate_enzyme"],
    },
    "zinc_lyase_hydratase": {
        "ec_prefixes": ["4.2.1"],
        "cofactor": "catalytic Zn2+; reversible water elimination/addition, carbonic anhydrase, or hydro-lyase chemistry",
        "lanes": ["zinc_lyase_hydratase"],
    },
}

ALL_FINGERPRINTS = tuple(FINGERPRINT_SOURCING_SIGNATURES.keys())

# Default balance policy. ``target_floor`` is the minimum seed-label count every
# in-scope fingerprint should reach before broad volume scaling continues;
# ``cap_ceiling`` is the count above which a fingerprint is over-supplied and
# should be paused / deduped rather than sourced. Both are conservative,
# overridable defaults -- the point is a defensible, explicit policy, not a tuned
# constant.
DEFAULT_TARGET_FLOOR = 100
DEFAULT_CAP_CEILING = 250
# A fingerprint whose expansion count is 0 (or whose combined count is far below
# the floor) is a HOLE -- the sharpest acquisition priority.
DEFAULT_HOLE_THRESHOLD = 25


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> list[dict[str, Any]]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def _source_provenance(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("source_provenance", {}) or {}


def _mechanism_evidence(row: dict[str, Any]) -> dict[str, Any]:
    return row.get("evidence", {}).get("mechanism_evidence", {}) or {}


def _lane(row: dict[str, Any]) -> str | None:
    return _source_provenance(row).get("target_family_lane")


def _organism(row: dict[str, Any]) -> str | None:
    return _source_provenance(row).get("organism")


def _sequence_length(row: dict[str, Any]) -> int | None:
    value = _source_provenance(row).get("sequence_length")
    return value if isinstance(value, int) else None


def _ec_numbers(row: dict[str, Any]) -> list[str]:
    return [e for e in (_mechanism_evidence(row).get("ec_numbers") or []) if e]


def _ec_top_class(row: dict[str, Any]) -> str | None:
    """The top-level EC class (1..7) -- coverage accounting only, never predictive."""
    for ec in _ec_numbers(row):
        head = ec.split(".")[0]
        if head.isdigit():
            return head
    return None


def _full_ec_signature(row: dict[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(set(_ec_numbers(row))))


def _reaction_ids(row: dict[str, Any]) -> tuple[str, ...]:
    """Concrete Rhea reaction ids (``RHEA:NNNN``); excludes generic ``RHEA-COMP``
    component placeholders, which are polymer/acceptor stand-ins, not reactions."""
    out = set()
    for req in _mechanism_evidence(row).get("reaction_equations") or []:
        rid = req.get("rhea_id")
        if isinstance(rid, str) and rid.startswith("RHEA:"):
            out.add(rid)
    return tuple(sorted(out))


def _sequence_length_bin(length: int | None) -> str:
    if not length:
        return "unknown"
    lo = (length // 100) * 100
    return f"{lo:04d}-{lo + 99:04d}"


def _gini(counts: list[int]) -> float:
    """Gini coefficient of a count distribution (0 = perfectly even)."""
    values = sorted(v for v in counts if v >= 0)
    n = len(values)
    total = sum(values)
    if n == 0 or total == 0:
        return 0.0
    cumulative = 0
    for i, value in enumerate(values, start=1):
        cumulative += i * value
    return round((2 * cumulative) / (n * total) - (n + 1) / n, 4)


def _normalized_entropy(counts: list[int]) -> float:
    values = [v for v in counts if v > 0]
    total = sum(values)
    if total == 0 or len(values) <= 1:
        return 0.0
    entropy = -sum((v / total) * math.log(v / total) for v in values)
    return round(entropy / math.log(len(values)), 4)


def _counter_to_sorted(counter: Counter, top: int | None = None) -> dict[str, int]:
    items = sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0])))
    if top is not None:
        items = items[:top]
    return {str(k): v for k, v in items}


def build_coverage_redundancy_audit(
    frozen: list[dict[str, Any]],
    expansion: list[dict[str, Any]],
    *,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    hole_threshold: int = DEFAULT_HOLE_THRESHOLD,
    cluster_min_size: int = 3,
) -> dict[str, Any]:
    combined = [
        {**row, "_registry": "frozen_current702"} for row in frozen
    ] + [{**row, "_registry": "expansion_bronze"} for row in expansion]

    # ---- top-line totals -------------------------------------------------
    label_type_by_registry: dict[str, Counter] = {
        "frozen_current702": Counter(r.get("label_type") for r in frozen),
        "expansion_bronze": Counter(r.get("label_type") for r in expansion),
    }
    totals = {
        "frozen_current702": len(frozen),
        "expansion_bronze": len(expansion),
        "combined": len(combined),
        "label_type_by_registry": {
            reg: _counter_to_sorted(c) for reg, c in label_type_by_registry.items()
        },
    }

    # ---- fingerprint distribution (seed positives) -----------------------
    fp_frozen = Counter(
        r.get("fingerprint_id")
        for r in frozen
        if r.get("label_type") == "seed_fingerprint"
    )
    fp_expansion = Counter(
        r.get("fingerprint_id")
        for r in expansion
        if r.get("label_type") == "seed_fingerprint"
    )
    fingerprint_distribution = {}
    for fp in ALL_FINGERPRINTS:
        fingerprint_distribution[fp] = {
            "frozen": fp_frozen.get(fp, 0),
            "expansion": fp_expansion.get(fp, 0),
            "combined": fp_frozen.get(fp, 0) + fp_expansion.get(fp, 0),
        }

    # ---- dimension distributions (expansion carries the metadata) --------
    lane_counts = Counter(_lane(r) or "unspecified" for r in expansion)
    organism_counts = Counter(_organism(r) or "unspecified" for r in expansion)
    ec_class_counts = Counter(_ec_top_class(r) or "unspecified" for r in combined)
    seqlen_counts = Counter(
        _sequence_length_bin(_sequence_length(r)) for r in expansion
    )

    # cross-tabs (seed rows only, expansion -- the governed supply)
    seed_expansion = [
        r for r in expansion if r.get("label_type") == "seed_fingerprint"
    ]
    fp_by_lane: dict[str, Counter] = defaultdict(Counter)
    fp_by_ec_class: dict[str, Counter] = defaultdict(Counter)
    fp_by_organism: dict[str, Counter] = defaultdict(Counter)
    for r in seed_expansion:
        fp = r.get("fingerprint_id")
        fp_by_lane[fp][_lane(r) or "unspecified"] += 1
        fp_by_ec_class[fp][_ec_top_class(r) or "unspecified"] += 1
        fp_by_organism[fp][_organism(r) or "unspecified"] += 1

    distributions = {
        "by_lane_expansion": _counter_to_sorted(lane_counts),
        "by_organism_expansion_top25": _counter_to_sorted(organism_counts, top=25),
        "distinct_organisms_expansion": len(
            {o for o in (_organism(r) for r in expansion) if o}
        ),
        "by_ec_class_combined": _counter_to_sorted(ec_class_counts),
        "by_sequence_length_bin_expansion": _counter_to_sorted(seqlen_counts),
        "fingerprint_by_lane_expansion_seed": {
            fp: _counter_to_sorted(c) for fp, c in sorted(fp_by_lane.items())
        },
        "fingerprint_by_ec_class_expansion_seed": {
            fp: _counter_to_sorted(c) for fp, c in sorted(fp_by_ec_class.items())
        },
        "fingerprint_by_organism_expansion_seed_top10": {
            fp: _counter_to_sorted(c, top=10) for fp, c in sorted(fp_by_organism.items())
        },
    }

    # ---- metadata completeness (what is even measurable) -----------------
    metadata_completeness = {
        "expansion_rows": len(expansion),
        "with_organism": sum(1 for r in expansion if _organism(r)),
        "with_sequence_length": sum(1 for r in expansion if _sequence_length(r)),
        "with_ec_numbers": sum(1 for r in expansion if _ec_numbers(r)),
        "with_concrete_rhea": sum(1 for r in expansion if _reaction_ids(r)),
        "frozen_rows": len(frozen),
        "frozen_with_organism": sum(1 for r in frozen if _organism(r)),
        "frozen_with_ec_numbers": sum(1 for r in frozen if _ec_numbers(r)),
        "note": (
            "the frozen current702 benchmark carries only fingerprint_id / "
            "label_type (M-CSA rows), so lane/organism/EC/sequence-length coverage "
            "is measured on the expansion registry; frozen rows still count toward "
            "the combined fingerprint distribution"
        ),
    }

    # ---- class imbalance -------------------------------------------------
    seed_combined = [fingerprint_distribution[fp]["combined"] for fp in ALL_FINGERPRINTS]
    seed_total = sum(seed_combined)
    oos_total = (
        label_type_by_registry["frozen_current702"].get("out_of_scope", 0)
        + label_type_by_registry["expansion_bronze"].get("out_of_scope", 0)
    )
    nonzero = [v for v in seed_combined if v > 0]
    class_imbalance = {
        "seed_total_combined": seed_total,
        "out_of_scope_total_combined": oos_total,
        "positive_to_oos_ratio": round(seed_total / oos_total, 4) if oos_total else None,
        "max_fingerprint": max(seed_combined) if seed_combined else 0,
        "min_nonzero_fingerprint": min(nonzero) if nonzero else 0,
        "max_min_ratio": (
            round(max(seed_combined) / min(nonzero), 2) if nonzero else None
        ),
        "fingerprint_gini": _gini(seed_combined),
        "fingerprint_normalized_entropy": _normalized_entropy(seed_combined),
        "fingerprints_below_floor": sorted(
            fp
            for fp in ALL_FINGERPRINTS
            if fingerprint_distribution[fp]["combined"] < target_floor
        ),
        "fingerprints_above_cap": sorted(
            fp
            for fp in ALL_FINGERPRINTS
            if fingerprint_distribution[fp]["combined"] > cap_ceiling
        ),
        "expansion_holes": sorted(
            fp for fp in ALL_FINGERPRINTS if fingerprint_distribution[fp]["expansion"] == 0
        ),
    }

    # ---- redundancy / saturation (metadata-only proxies) -----------------
    per_fp_diversity = {}
    for fp in ALL_FINGERPRINTS:
        rows = [r for r in seed_expansion if r.get("fingerprint_id") == fp]
        distinct_ec = {e for r in rows for e in _ec_numbers(r)}
        distinct_org = {_organism(r) for r in rows if _organism(r)}
        distinct_rx = {x for r in rows for x in _reaction_ids(r)}
        n = len(rows)
        per_fp_diversity[fp] = {
            "expansion_seed_labels": n,
            "distinct_full_ec": len(distinct_ec),
            "distinct_organisms": len(distinct_org),
            "distinct_reactions": len(distinct_rx),
            # >1 means multiple labels share a reaction -- a redundancy proxy
            "labels_per_distinct_reaction": (
                round(n / len(distinct_rx), 2) if distinct_rx else None
            ),
            "labels_per_distinct_ec": (
                round(n / len(distinct_ec), 2) if distinct_ec else None
            ),
        }

    # reaction saturation across the whole expansion (which reactions repeat)
    reaction_counter: Counter = Counter()
    for r in expansion:
        for rid in _reaction_ids(r):
            reaction_counter[rid] += 1
    reaction_saturation = {
        "distinct_concrete_reactions": len(reaction_counter),
        "rows_with_concrete_reaction": sum(
            1 for r in expansion if _reaction_ids(r)
        ),
        "most_repeated_reactions_top15": _counter_to_sorted(reaction_counter, top=15),
    }

    # near-duplicate ortholog clusters: same fingerprint/OOS + identical full-EC
    # signature + same organism + same sequence-length bin. Same enzyme, same
    # organism, near-identical length => almost certainly near-duplicate
    # sequences the exact-accession/SHA screen does not catch.
    cluster_map: dict[tuple, list[str]] = defaultdict(list)
    for r in expansion:
        fp = r.get("fingerprint_id") or "out_of_scope"
        ec_sig = _full_ec_signature(r)
        org = _organism(r)
        seq_bin = _sequence_length_bin(_sequence_length(r))
        # only cluster rows where the redundancy signal is actually measurable
        if not ec_sig or not org or seq_bin == "unknown":
            continue
        cluster_map[(fp, ec_sig, org, seq_bin)].append(r["entry_id"])
    clusters = [
        {
            "fingerprint_or_scope": key[0],
            "full_ec": list(key[1]),
            "organism": key[2],
            "sequence_length_bin": key[3],
            "size": len(members),
            "entry_ids_sample": sorted(members)[:6],
        }
        for key, members in cluster_map.items()
        if len(members) >= cluster_min_size
    ]
    clusters.sort(key=lambda c: (-c["size"], c["fingerprint_or_scope"]))
    redundant_rows = sum(c["size"] for c in clusters)
    redundancy = {
        "per_fingerprint_diversity": per_fp_diversity,
        "reaction_saturation": reaction_saturation,
        "near_duplicate_clusters": {
            "cluster_key": "(fingerprint_or_scope, full_ec, organism, sequence_length_bin)",
            "cluster_min_size": cluster_min_size,
            "measurable_rows": sum(len(v) for v in cluster_map.values()),
            "cluster_count": len(clusters),
            "rows_in_clusters": redundant_rows,
            "redundancy_fraction_of_measurable": (
                round(redundant_rows / sum(len(v) for v in cluster_map.values()), 4)
                if cluster_map
                else 0.0
            ),
            "clusters_top25": clusters[:25],
        },
    }

    # ---- prioritized, balance-capped acquisition target list -------------
    acquisition_targets = _build_acquisition_targets(
        fingerprint_distribution=fingerprint_distribution,
        per_fp_diversity=per_fp_diversity,
        target_floor=target_floor,
        cap_ceiling=cap_ceiling,
        hole_threshold=hole_threshold,
    )

    return {
        "audit": "coverage_redundancy_audit",
        "created_utc": _utc_now_iso(),
        "status": "ok",
        "non_destructive": True,
        "policy": {
            "target_floor_per_fingerprint": target_floor,
            "cap_ceiling_per_fingerprint": cap_ceiling,
            "hole_threshold": hole_threshold,
            "cluster_min_size": cluster_min_size,
        },
        "totals": totals,
        "fingerprint_distribution": fingerprint_distribution,
        "distributions": distributions,
        "metadata_completeness": metadata_completeness,
        "class_imbalance": class_imbalance,
        "redundancy": redundancy,
        "acquisition_targets": acquisition_targets,
        "guardrails": {
            "frozen_benchmark_written": False,
            "expansion_registry_written": False,
            "labels_emitted": 0,
            "ec_lane_organism_used_for_coverage_accounting_only_never_predictive": True,
            "metadata_only_no_network_no_mmseqs_no_embeddings": True,
        },
    }


def _build_acquisition_targets(
    *,
    fingerprint_distribution: dict[str, dict[str, int]],
    per_fp_diversity: dict[str, dict[str, Any]],
    target_floor: int,
    cap_ceiling: int,
    hole_threshold: int,
) -> dict[str, Any]:
    rows = []
    for fp in ALL_FINGERPRINTS:
        dist = fingerprint_distribution[fp]
        combined = dist["combined"]
        diversity = per_fp_diversity.get(fp, {})
        distinct_rx = diversity.get("distinct_reactions") or 0
        redundancy_ratio = diversity.get("labels_per_distinct_reaction")

        if combined <= hole_threshold or dist["expansion"] == 0:
            status = "HOLE"
        elif combined < target_floor:
            status = "UNDER"
        elif combined > cap_ceiling:
            status = "OVER_CAP"
        else:
            status = "BALANCED"

        deficit = max(0, target_floor - combined)
        surplus = max(0, combined - cap_ceiling)

        if status in ("HOLE", "UNDER"):
            action = (
                f"SOURCE ~{deficit} more seed labels to reach the {target_floor} floor"
            )
        elif status == "OVER_CAP":
            action = (
                f"CAP / PAUSE -- {surplus} over the {cap_ceiling} ceiling; dedup toward "
                f"distinct reactions before adding any"
            )
        else:
            action = "HOLD -- at balance; only add if a new reaction/organism is gained"

        signature = FINGERPRINT_SOURCING_SIGNATURES[fp]
        rows.append(
            {
                "fingerprint": fp,
                "status": status,
                "priority_rank": 0,  # filled after sort
                "combined": combined,
                "frozen": dist["frozen"],
                "expansion": dist["expansion"],
                "deficit_to_floor": deficit,
                "surplus_over_cap": surplus,
                "distinct_reactions": distinct_rx,
                "labels_per_distinct_reaction": redundancy_ratio,
                "recommended_action": action,
                "sourcing_hints": {
                    "ec_prefixes": signature["ec_prefixes"],
                    "cofactor_signature": signature["cofactor"],
                    "lanes": signature["lanes"],
                },
            }
        )

    # priority: HOLE > UNDER > OVER_CAP > BALANCED; within tier, largest gap first
    status_rank = {"HOLE": 0, "UNDER": 1, "OVER_CAP": 2, "BALANCED": 3}
    rows.sort(
        key=lambda r: (
            status_rank[r["status"]],
            -r["deficit_to_floor"],
            -r["surplus_over_cap"],
            r["fingerprint"],
        )
    )
    for i, r in enumerate(rows, start=1):
        r["priority_rank"] = i

    holes = [r["fingerprint"] for r in rows if r["status"] == "HOLE"]
    under = [r["fingerprint"] for r in rows if r["status"] == "UNDER"]
    caps = [r["fingerprint"] for r in rows if r["status"] == "OVER_CAP"]
    total_deficit = sum(r["deficit_to_floor"] for r in rows)

    return {
        "policy_summary": (
            "Close HOLES first (esp. fingerprints absent from the expansion), then "
            "raise UNDER-floor fingerprints, while CAPPING over-supplied ones and "
            "deduplicating them toward distinct reactions. Pause broad out_of_scope "
            "draining (kinase/phosphatase/glycoside lanes are already saturated) until "
            "the positive holes are closed -- the binding constraint is diverse "
            "positive supply, not raw count."
        ),
        "next_batch_floor_deficit_total": total_deficit,
        "holes": holes,
        "under_floor": under,
        "over_cap": caps,
        "targets": rows,
    }


def _report(audit: dict[str, Any]) -> str:
    t = audit["totals"]
    ci = audit["class_imbalance"]
    at = audit["acquisition_targets"]
    nd = audit["redundancy"]["near_duplicate_clusters"]
    lines = [
        "# Coverage + Redundancy Audit And Balance-Capped Acquisition Policy",
        "",
        f"Run: {audit['created_utc']}",
        "",
        "Non-destructive, metadata-only audit of all combined labels "
        f"({t['combined']} = {t['frozen_current702']} frozen current702 + "
        f"{t['expansion_bronze']} expansion bronze). No registry is written and no "
        "label is emitted. Redundancy is measured from annotation metadata only "
        "(no mmseqs / no embeddings / no network).",
        "",
        "## Class balance (seed fingerprints, combined)",
        "",
        f"- Seed positives: {ci['seed_total_combined']}; out_of_scope: "
        f"{ci['out_of_scope_total_combined']}; positive:OOS = "
        f"{ci['positive_to_oos_ratio']}.",
        f"- Fingerprint Gini {ci['fingerprint_gini']} / normalized entropy "
        f"{ci['fingerprint_normalized_entropy']}; max/min(nonzero) ratio "
        f"{ci['max_min_ratio']} ({ci['max_fingerprint']} vs "
        f"{ci['min_nonzero_fingerprint']}).",
        f"- Below floor: {ci['fingerprints_below_floor']}.",
        f"- Above cap: {ci['fingerprints_above_cap']}.",
        f"- Absent from expansion (holes): {ci['expansion_holes']}.",
        "",
        "| Fingerprint | frozen | expansion | combined | distinct rxn | labels/rxn |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for fp in ALL_FINGERPRINTS:
        d = audit["fingerprint_distribution"][fp]
        div = audit["redundancy"]["per_fingerprint_diversity"][fp]
        lines.append(
            f"| {fp} | {d['frozen']} | {d['expansion']} | {d['combined']} | "
            f"{div['distinct_reactions']} | {div['labels_per_distinct_reaction']} |"
        )
    lines.extend(
        [
            "",
            "## Near-duplicate / saturation read (metadata proxy)",
            "",
            f"- Cluster key: {nd['cluster_key']}.",
            f"- Measurable rows: {nd['measurable_rows']}; clusters (size >= "
            f"{nd['cluster_min_size']}): {nd['cluster_count']}; rows in clusters: "
            f"{nd['rows_in_clusters']} ({nd['redundancy_fraction_of_measurable']} of "
            "measurable).",
            "- Top redundancy clusters (same enzyme/organism/length, near-dup orthologs):",
            "",
            "| size | scope | full EC | organism | len bin |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for c in nd["clusters_top25"][:12]:
        lines.append(
            f"| {c['size']} | {c['fingerprint_or_scope']} | "
            f"{','.join(c['full_ec'])} | {c['organism']} | {c['sequence_length_bin']} |"
        )
    lines.extend(
        [
            "",
            "## Prioritized, balance-capped acquisition targets",
            "",
            at["policy_summary"],
            "",
            f"- Holes: {at['holes']}.",
            f"- Under floor: {at['under_floor']}.",
            f"- Over cap: {at['over_cap']}.",
            f"- Total deficit to floor (next-batch positive target): "
            f"{at['next_batch_floor_deficit_total']}.",
            "",
            "| # | fingerprint | status | combined | deficit | surplus | action |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for r in at["targets"]:
        lines.append(
            f"| {r['priority_rank']} | {r['fingerprint']} | {r['status']} | "
            f"{r['combined']} | {r['deficit_to_floor']} | {r['surplus_over_cap']} | "
            f"{r['recommended_action']} |"
        )
    lines.extend(
        [
            "",
            "### Sourcing hints per fingerprint (coverage accounting only, never predictive)",
            "",
            "| fingerprint | EC prefixes | cofactor signature | lanes |",
            "| --- | --- | --- | --- |",
        ]
    )
    for r in at["targets"]:
        h = r["sourcing_hints"]
        lines.append(
            f"| {r['fingerprint']} | {', '.join(h['ec_prefixes'])} | "
            f"{h['cofactor_signature']} | {', '.join(h['lanes'])} |"
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            f"- Frozen benchmark written: {audit['guardrails']['frozen_benchmark_written']}.",
            f"- Expansion registry written: "
            f"{audit['guardrails']['expansion_registry_written']}.",
            f"- Labels emitted: {audit['guardrails']['labels_emitted']}.",
            "- EC/lane/organism used for coverage accounting only, never predictive.",
            "- Metadata-only: no network, no mmseqs, no embedding backend.",
            "",
        ]
    )
    return "\n".join(lines)


def write_coverage_redundancy_audit(
    *,
    out_path: Path,
    report_path: Path | None = None,
    frozen_benchmark_path: Path = DEFAULT_FROZEN_BENCHMARK_PATH,
    expansion_registry_path: Path = DEFAULT_EXPANSION_REGISTRY_PATH,
    target_floor: int = DEFAULT_TARGET_FLOOR,
    cap_ceiling: int = DEFAULT_CAP_CEILING,
    hole_threshold: int = DEFAULT_HOLE_THRESHOLD,
    cluster_min_size: int = 3,
) -> dict[str, Any]:
    frozen = _load_json(frozen_benchmark_path)
    expansion_path = Path(expansion_registry_path)
    expansion = _load_json(expansion_path) if expansion_path.exists() else []
    audit = build_coverage_redundancy_audit(
        frozen,
        expansion,
        target_floor=target_floor,
        cap_ceiling=cap_ceiling,
        hole_threshold=hole_threshold,
        cluster_min_size=cluster_min_size,
    )
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report_path is not None:
        report_path = Path(report_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(_report(audit), encoding="utf-8")
    return audit
