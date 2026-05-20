#!/usr/bin/env python3
"""Retry residual product-state sibling queries with structured/title seeds.

This is a lane-local review-only helper. It uses RCSB search only to identify a
small bounded set of PDB IDs, then reuses the sibling-control mmCIF scanner in
memory. It writes compact evidence summaries and no raw coordinate files.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
SCREEN_PATH = Path(__file__).with_name("askha_control_screen.py")


def load_screen_module():
    spec = importlib.util.spec_from_file_location("epk_sibling_screen", SCREEN_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load scanner module from {SCREEN_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def text_node(attribute: str, operator: str, value: str) -> dict:
    return {
        "type": "terminal",
        "service": "text",
        "parameters": {
            "attribute": attribute,
            "operator": operator,
            "value": value,
        },
    }


def full_text_node(term: str) -> dict:
    return {
        "type": "terminal",
        "service": "full_text",
        "parameters": {"value": term},
    }


def group_node(nodes: list[dict]) -> dict:
    return {"type": "group", "logical_operator": "and", "nodes": nodes}


def post_search(query_node: dict, rows: int) -> dict:
    payload = {
        "query": query_node,
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": rows},
            "return_all_hits": False,
            "sort": [{"sort_by": "score", "direction": "desc"}],
        },
    }
    request = urllib.request.Request(
        RCSB_SEARCH_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
        if response.status == 204 or not body:
            return {
                "status": "no_hits_204",
                "total_count": 0,
                "hits": [],
                "http_status": response.status,
            }
        data = json.loads(body.decode("utf-8"))
        hits = [row["identifier"].upper() for row in data.get("result_set", [])]
        return {
            "status": "ok",
            "total_count": data.get("total_count", len(hits)),
            "hits": hits,
            "http_status": response.status,
        }


def run_search_record(case_id: str, search: dict, rows: int) -> dict:
    if search["search_type"] == "full_text":
        query_node = full_text_node(search["term"])
    elif search["search_type"] == "structured":
        query_node = group_node(search["nodes"])
    else:
        raise ValueError(f"unknown search type: {search['search_type']}")

    try:
        result = post_search(query_node, rows)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        result = {
            "status": f"query_failed:{type(exc).__name__}",
            "total_count": 0,
            "hits": [],
            "http_status": None,
        }

    return {
        "case_id": case_id,
        "search_label": search["search_label"],
        "search_type": search["search_type"],
        "term": search.get("term"),
        "nodes": search.get("nodes"),
        "status": result["status"],
        "http_status": result["http_status"],
        "total_count": result["total_count"],
        "hits": result["hits"],
    }


def compact_row(row: dict) -> dict:
    return {
        "pdb_id": row.get("pdb_id"),
        "fetch_status": row.get("fetch_status"),
        "structure_title": row.get("structure_title"),
        "family_id": row.get("family_id"),
        "review_status": row.get("review_status"),
        "product_state_branch_status": row.get("product_state_branch_status"),
        "product_state_control_candidate_review_only": row.get(
            "product_state_control_candidate_review_only"
        ),
        "weak_nearest_any_oxygen_rule_hit_6a": row.get(
            "weak_nearest_any_oxygen_rule_hit_6a"
        ),
        "observed_ligand_codes": row.get("observed_ligand_codes", []),
        "gamma_capable_nucleotide_codes": row.get("gamma_capable_nucleotide_codes", []),
        "product_or_partial_nucleotide_codes": row.get(
            "product_or_partial_nucleotide_codes", []
        ),
        "phosphate_or_phosphoryl_mimic_codes": row.get(
            "phosphate_or_phosphoryl_mimic_codes", []
        ),
        "phosphorylated_nonpolymer_ligand_codes": row.get(
            "phosphorylated_nonpolymer_ligand_codes", []
        ),
        "metal_ligand_codes": row.get("metal_ligand_codes", []),
        "nearest_gamma_to_metal_distance_angstrom": row.get(
            "nearest_gamma_to_metal_distance_angstrom"
        ),
        "nearest_gamma_to_protein_hydroxyl_distance_angstrom": row.get(
            "nearest_gamma_to_protein_hydroxyl_distance_angstrom"
        ),
        "nearest_gamma_to_nonpolymer_oxygen_distance_angstrom": row.get(
            "nearest_gamma_to_nonpolymer_oxygen_distance_angstrom"
        ),
        "nearest_product_phosphoryl_to_metal_distance_angstrom": row.get(
            "nearest_product_phosphoryl_to_metal_distance_angstrom"
        ),
        "nearest_product_phosphoryl_to_product_beta_distance_angstrom": row.get(
            "nearest_product_phosphoryl_to_product_beta_distance_angstrom"
        ),
        "query_origins": row.get("query_origins", []),
        "review_only": row.get("review_only", True),
        "production_scoring_admissible": row.get("production_scoring_admissible", False),
        "epk_score_computed": row.get("epk_score_computed", False),
        "labels_or_fingerprints_changed": row.get(
            "labels_or_fingerprints_changed", False
        ),
    }


ADP = text_node(
    "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
    "exact_match",
    "ADP",
)
MG = text_node(
    "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
    "exact_match",
    "MG",
)

RESIDUAL_CASES = [
    {
        "case_id": "askha_structured_product_ligand_retry",
        "family_id": "askha",
        "failed_term": "none; under-covered ASKHA structured product-ligand retry",
        "hypothesis": (
            "Structured ASKHA title/ligand seeds may reveal ADP plus a metal-local "
            "glucose-6-phosphate or acetyl-phosphate product that broad product-state "
            "queries did not retain as a strict control."
        ),
        "searches": [
            {
                "search_label": "structured_glucokinase_adp",
                "search_type": "structured",
                "nodes": [text_node("struct.title", "contains_phrase", "glucokinase"), ADP],
            },
            {
                "search_label": "structured_hexokinase_adp_mg",
                "search_type": "structured",
                "nodes": [
                    text_node("struct.title", "contains_phrase", "hexokinase"),
                    ADP,
                    MG,
                ],
            },
            {
                "search_label": "structured_hexokinase_adp_g6p",
                "search_type": "structured",
                "nodes": [
                    text_node("struct.title", "contains_phrase", "hexokinase"),
                    ADP,
                    text_node(
                        "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
                        "exact_match",
                        "G6P",
                    ),
                ],
            },
            {
                "search_label": "structured_hexokinase_adp",
                "search_type": "structured",
                "nodes": [text_node("struct.title", "contains_phrase", "hexokinase"), ADP],
            },
            {
                "search_label": "structured_acetate_kinase_adp",
                "search_type": "structured",
                "nodes": [
                    text_node("struct.title", "contains_phrase", "acetate kinase"),
                    ADP,
                ],
            },
            {
                "search_label": "title_curated_acetate_kinase",
                "search_type": "structured",
                "nodes": [text_node("struct.title", "contains_phrase", "acetate kinase")],
            },
            {
                "search_label": "structured_glucose_6_phosphate_title_adp",
                "search_type": "structured",
                "nodes": [
                    text_node("struct.title", "contains_phrase", "glucose 6-phosphate"),
                    ADP,
                ],
            },
        ],
    },
    {
        "case_id": "ghkl_chea_phosphohistidine_retry",
        "family_id": "ghkl",
        "failed_term": "CheA ADP phospho histidine magnesium",
        "hypothesis": (
            "A CheA phosphohistidine product-state synonym may reveal ADP/Mg plus a "
            "metal-local phosphoryl product that the broad GHKL product screen missed."
        ),
        "searches": [
            {
                "search_label": "residual_full_text_synonym",
                "search_type": "full_text",
                "term": "CheA ADP phospho histidine magnesium",
            },
            {
                "search_label": "structured_chea_adp_mg",
                "search_type": "structured",
                "nodes": [text_node("struct.title", "contains_phrase", "CheA"), ADP, MG],
            },
            {
                "search_label": "title_curated_chea",
                "search_type": "structured",
                "nodes": [text_node("struct.title", "contains_phrase", "CheA")],
            },
        ],
    },
    {
        "case_id": "ghmp_homoserine_phosphohomoserine_retry",
        "family_id": "ghmp",
        "failed_term": "homoserine kinase ADP phospho homoserine magnesium",
        "hypothesis": (
            "A homoserine kinase phosphohomoserine product synonym may expose ADP/Mg "
            "with a metal-local phosphorylated small-molecule product."
        ),
        "searches": [
            {
                "search_label": "residual_full_text_synonym",
                "search_type": "full_text",
                "term": "homoserine kinase ADP phospho homoserine magnesium",
            },
            {
                "search_label": "structured_homoserine_kinase_adp_mg",
                "search_type": "structured",
                "nodes": [
                    text_node("struct.title", "contains_phrase", "homoserine kinase"),
                    ADP,
                    MG,
                ],
            },
            {
                "search_label": "title_curated_homoserine_kinase",
                "search_type": "structured",
                "nodes": [text_node("struct.title", "contains_phrase", "homoserine kinase")],
            },
        ],
    },
    {
        "case_id": "ghmp_cdp_me_phosphate_retry",
        "family_id": "ghmp",
        "failed_term": "CDP ME kinase ADP phosphate magnesium",
        "hypothesis": (
            "A CDP-ME kinase phosphate product synonym may expose a GHMP ADP/product "
            "state missed by punctuation-sensitive full-text terms."
        ),
        "searches": [
            {
                "search_label": "residual_full_text_synonym",
                "search_type": "full_text",
                "term": "CDP ME kinase ADP phosphate magnesium",
            },
            {
                "search_label": "title_curated_cdp_me_kinase",
                "search_type": "structured",
                "nodes": [
                    text_node(
                        "struct.title",
                        "contains_phrase",
                        "methyl-D-erythritol kinase",
                    )
                ],
            },
        ],
    },
    {
        "case_id": "pfkb_ketohexokinase_product_retry",
        "family_id": "pfkb",
        "failed_term": "ketohexokinase ADP fructose phosphate magnesium",
        "hypothesis": (
            "A ketohexokinase fructose-phosphate product synonym may add PfkB "
            "ADP/product controls or close that residual branch as a no-metal product gap."
        ),
        "searches": [
            {
                "search_label": "residual_full_text_synonym",
                "search_type": "full_text",
                "term": "ketohexokinase ADP fructose phosphate magnesium",
            },
            {
                "search_label": "title_curated_ketohexokinase",
                "search_type": "structured",
                "nodes": [text_node("struct.title", "contains_phrase", "ketohexokinase")],
            },
        ],
    },
]


def summarize_case(case: dict, rows: list[dict], candidate_ids: list[str]) -> dict:
    product_rows = [
        row
        for row in rows
        if row.get("review_status") == f"{case['family_id']}_product_state_only_review_only"
    ]
    product_with_metal = [row for row in product_rows if row.get("metal_ligand_codes")]
    product_with_phosphoryl = [
        row for row in product_rows if row.get("phosphate_or_phosphoryl_mimic_codes")
    ]
    controls = [row for row in rows if row.get("product_state_control_candidate_review_only")]
    weak_hits = [row for row in rows if row.get("weak_nearest_any_oxygen_rule_hit_6a")]
    fetch_failures = [row for row in rows if row.get("fetch_status") != "ok"]
    return {
        "case_id": case["case_id"],
        "family_id": case["family_id"],
        "failed_term": case["failed_term"],
        "hypothesis": case["hypothesis"],
        "candidate_structure_count": len(candidate_ids),
        "rows_reviewed": len(rows),
        "candidate_pdb_ids": candidate_ids,
        "fetch_failure_count": len(fetch_failures),
        "fetch_failures": [
            {"pdb_id": row.get("pdb_id"), "fetch_status": row.get("fetch_status")}
            for row in fetch_failures
        ],
        "review_status_counts": dict(
            sorted(Counter(row.get("review_status", "unknown") for row in rows).items())
        ),
        "product_state_branch_status_counts": dict(
            sorted(
                Counter(
                    row.get("product_state_branch_status")
                    for row in rows
                    if row.get("product_state_branch_status")
                ).items()
            )
        ),
        "product_state_only_row_count": len(product_rows),
        "product_state_with_metal_count": len(product_with_metal),
        "product_state_with_metal_pdb_ids": [row["pdb_id"] for row in product_with_metal],
        "product_state_with_phosphoryl_mimic_count": len(product_with_phosphoryl),
        "product_state_with_phosphoryl_mimic_pdb_ids": [
            row["pdb_id"] for row in product_with_phosphoryl
        ],
        "product_state_branch_control_count": len(controls),
        "product_state_branch_control_pdb_ids": [row["pdb_id"] for row in controls],
        "weak_rule_counterexample_count": len(weak_hits),
        "weak_rule_counterexample_pdb_ids": [row["pdb_id"] for row in weak_hits],
        "compact_product_or_control_rows": [
            compact_row(row)
            for row in rows
            if row in product_rows
            or row in controls
            or row.get("product_state_branch_status")
            or row.get("weak_nearest_any_oxygen_rule_hit_6a")
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--rows-per-search", type=int, default=80)
    parser.add_argument("--sleep-seconds", type=float, default=0.1)
    args = parser.parse_args()

    screen = load_screen_module()
    started_at = utc_now()
    all_search_records = []
    case_summaries = []
    case_rows = {}
    all_control_ids = set()
    all_weak_ids = set()
    total_rows_reviewed = 0
    total_fetch_failures = 0
    unresolved_query_failures = []

    for case in RESIDUAL_CASES:
        origins: dict[str, list[str]] = defaultdict(list)
        case_search_records = []
        for search in case["searches"]:
            record = run_search_record(case["case_id"], search, args.rows_per_search)
            case_search_records.append(record)
            all_search_records.append(record)
            if record["status"].startswith("query_failed"):
                unresolved_query_failures.append(record)
            for pdb_id in record["hits"]:
                origins[pdb_id].append(record["search_label"])
            time.sleep(args.sleep_seconds)

        candidate_ids = []
        for record in case_search_records:
            for pdb_id in record["hits"]:
                if pdb_id not in candidate_ids:
                    candidate_ids.append(pdb_id)

        config = screen.FAMILY_CONFIGS[case["family_id"]]
        rows = [
            screen.scan_structure(pdb_id, sorted(set(origins[pdb_id])), config)
            for pdb_id in candidate_ids
        ]
        total_rows_reviewed += len(rows)
        total_fetch_failures += sum(1 for row in rows if row.get("fetch_status") != "ok")
        for row in rows:
            if row.get("product_state_control_candidate_review_only"):
                all_control_ids.add(row["pdb_id"])
            if row.get("weak_nearest_any_oxygen_rule_hit_6a"):
                all_weak_ids.add(row["pdb_id"])
        case_summaries.append(summarize_case(case, rows, candidate_ids))
        case_rows[case["case_id"]] = [compact_row(row) for row in rows]

    no_hit_synonym_terms = [
        record["term"]
        for record in all_search_records
        if record["search_label"] == "residual_full_text_synonym"
        and record["status"] == "no_hits_204"
    ]
    controls_added = len(all_control_ids)
    primary_outcome = "search_surface_exhausted" if controls_added == 0 else "evidence_for"
    artifact = {
        "metadata": {
            "method": "epk_sibling_controls_residual_product_state_structured_retry",
            "created_at": utc_now(),
            "screen_started_at": started_at,
            "review_only": True,
            "production_claim_allowed": False,
            "production_scoring_admissible": False,
            "curated_label_registry_edited": False,
            "fingerprint_registry_edited": False,
            "labels_or_fingerprints_changed": False,
            "raw_coordinate_files_written": False,
            "target_family_id": "epk",
            "target_fingerprint_id": "epk_atp_gamma_phosphoryl_transfer",
            "target_sibling_families": sorted({case["family_id"] for case in RESIDUAL_CASES}),
            "rows_per_search": args.rows_per_search,
            "rows_reviewed": total_rows_reviewed,
            "case_count": len(RESIDUAL_CASES),
            "controls_added": controls_added,
            "product_state_branch_control_pdb_ids": sorted(all_control_ids),
            "weak_rule_counterexample_count": len(all_weak_ids),
            "weak_rule_counterexample_pdb_ids": sorted(all_weak_ids),
            "fetch_failure_count": total_fetch_failures,
            "unresolved_query_failure_count": len(unresolved_query_failures),
            "no_hit_synonym_terms": no_hit_synonym_terms,
            "primary_outcome": primary_outcome,
            "search_surface_exhausted": primary_outcome == "search_surface_exhausted",
            "search_surface": (
                "Residual product-state full-text synonyms plus structured/title-bounded "
                "RCSB PDB-id seeds for ASKHA product-ligand terms, CheA, homoserine "
                "kinase, CDP-ME kinase, and ketohexokinase; rows scanned in memory "
                "with compact mmCIF-derived product-state and weak-rule measurements."
            ),
            "next_query": (
                "Move to ATP-grasp/dNK/PfkA/PfkB strict product controls against a "
                "new substrate-identity counteraxis once implemented, or continue with "
                "ASKHA/GHKL/GHMP only if new curated product-ligand seeds appear."
            ),
        },
        "case_summaries": case_summaries,
        "search_records": all_search_records,
        "rows_by_case_compact": case_rows,
        "warnings": [
            "Review-only residual sibling-control evidence; not production scoring, threshold calibration, label import, or registry work.",
            "HTTP 204 empty RCSB result sets are recorded as no-hit outcomes, not JSON parsing failures.",
            "No raw coordinate files are persisted; compact rows retain only ligand codes, distances, statuses, and PDB IDs.",
        ],
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(artifact["metadata"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
