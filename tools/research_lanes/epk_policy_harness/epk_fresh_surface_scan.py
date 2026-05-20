#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import shlex
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.catalytic_earth.structure import fetch_pdb_cif, parse_atom_site_loop


LANE_ID = "epk_policy_harness"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
ACCEPTOR_ATOMS = {"SER": "OG", "THR": "OG1", "TYR": "OH"}
METAL_CODES = {
    "MG",
    "MN",
    "CA",
    "ZN",
    "CO",
    "FE",
    "FE2",
    "CU",
    "NI",
    "CD",
    "NA",
    "K",
}
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
RCSB_CHEM_COMP_ATTRIBUTE = "rcsb_chem_comp_container_identifiers.comp_id"
USER_AGENT = "Codex ePK policy harness review-only surface scan"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def atom_code(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_comp_id") or atom.get("label_comp_id") or "").upper()


def atom_name(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_atom_id") or atom.get("label_atom_id") or "").upper()


def atom_chain(atom: dict[str, Any]) -> str:
    return str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")


def atom_entity(atom: dict[str, Any]) -> str | None:
    value = atom.get("label_entity_id")
    if value in {None, "", ".", "?"}:
        return None
    return str(value)


def atom_distance(a: dict[str, Any], b: dict[str, Any]) -> float:
    ax = float(a["Cartn_x"])
    ay = float(a["Cartn_y"])
    az = float(a["Cartn_z"])
    bx = float(b["Cartn_x"])
    by = float(b["Cartn_y"])
    bz = float(b["Cartn_z"])
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2 + (az - bz) ** 2)


def round_distance(value: float | None) -> float | None:
    if value is None:
        return None
    return round(value, 3)


def post_rcsb_search(payload: dict[str, Any]) -> dict[str, Any]:
    request = urllib.request.Request(
        RCSB_SEARCH_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        data = json.load(response)
    if not isinstance(data, dict):
        raise ValueError("RCSB search response must be a JSON object")
    return data


def rcsb_full_text_query(query: str, *, rows: int) -> list[str]:
    payload = {
        "query": {
            "type": "terminal",
            "service": "full_text",
            "parameters": {"value": query},
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": rows},
            "results_content_type": ["experimental"],
            "sort": [
                {
                    "sort_by": "rcsb_accession_info.initial_release_date",
                    "direction": "desc",
                }
            ],
        },
    }
    data = post_rcsb_search(payload)
    result_set = data.get("result_set", [])
    return [str(row["identifier"]).upper() for row in result_set if row.get("identifier")]


def rcsb_chemcomp_query(comp_id: str, *, rows: int) -> list[str]:
    payload = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": RCSB_CHEM_COMP_ATTRIBUTE,
                "operator": "exact_match",
                "value": comp_id.upper(),
            },
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {"start": 0, "rows": rows},
            "results_content_type": ["experimental"],
            "sort": [
                {
                    "sort_by": "rcsb_accession_info.initial_release_date",
                    "direction": "desc",
                }
            ],
        },
    }
    data = post_rcsb_search(payload)
    result_set = data.get("result_set", [])
    return [str(row["identifier"]).upper() for row in result_set if row.get("identifier")]


def rcsb_candidate_ids(args: argparse.Namespace) -> tuple[list[str], str, str]:
    if args.query_mode == "full_text":
        return (
            rcsb_full_text_query(args.query, rows=args.query_rows),
            (
                f"full_text {args.query} sorted by "
                "rcsb_accession_info.initial_release_date desc"
            ),
            "live_rcsb_full_text_and_coordinate_api_bounded_scan",
        )
    if args.query_mode == "chemcomp":
        comp_id = args.chem_comp_id.upper()
        return (
            rcsb_chemcomp_query(comp_id, rows=args.query_rows),
            (
                f"chemcomp {RCSB_CHEM_COMP_ATTRIBUTE} exact_match {comp_id} sorted by "
                "rcsb_accession_info.initial_release_date desc"
            ),
            "live_rcsb_chemcomp_query_and_coordinate_api_bounded_scan",
        )
    raise ValueError(f"unsupported query mode: {args.query_mode}")


def iter_existing_text_paths(
    root: Path, output_paths: set[Path], *, max_existing_text_bytes: int
) -> list[Path]:
    paths: list[Path] = []
    for base in (
        root / "artifacts" / "research_lanes" / LANE_ID,
        root / "work" / "research_lanes" / LANE_ID,
    ):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path in output_paths:
                continue
            if path.suffix.lower() not in {".json", ".jsonl", ".md", ".txt"}:
                continue
            try:
                if path.stat().st_size > max_existing_text_bytes:
                    continue
            except OSError:
                continue
            paths.append(path)
    return paths


def ids_seen_in_existing_artifacts(
    root: Path,
    candidate_ids: list[str],
    output_paths: set[Path],
    *,
    max_existing_text_bytes: int,
) -> set[str]:
    remaining = set(candidate_ids)
    seen: set[str] = set()
    for path in iter_existing_text_paths(
        root, output_paths, max_existing_text_bytes=max_existing_text_bytes
    ):
        if not remaining:
            break
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pdb_id in list(remaining):
            if re.search(rf"(?<![A-Za-z0-9]){re.escape(pdb_id)}(?![A-Za-z0-9])", text):
                seen.add(pdb_id)
                remaining.remove(pdb_id)
    return seen


def polymer_entity_by_chain(atoms: list[dict[str, Any]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for atom in atoms:
        if atom.get("group_PDB") != "ATOM":
            continue
        entity_id = atom_entity(atom)
        if not entity_id:
            continue
        for key in ("auth_asym_id", "label_asym_id"):
            chain = str(atom.get(key) or "")
            if chain and chain not in mapping:
                mapping[chain] = entity_id
    return mapping


def compact_structure_summary(
    pdb_id: str,
    *,
    ligand_code: str,
    cutoff: float,
    local_metal_cutoff: float,
    max_atoms: int,
) -> dict[str, Any]:
    cif_text = fetch_pdb_cif(pdb_id)
    atoms = parse_atom_site_loop(cif_text)
    if len(atoms) > max_atoms:
        return {
            "pdb_id": pdb_id,
            "fetch_status": "skipped_structure_too_large_for_compact_scan",
            "atom_site_row_count": len(atoms),
            "terminal_gamma_atom_detected": None,
            "terminal_gamma_atom_name": None,
            "gamma_ligand_code": None,
            "best_any_ser_thr_tyr_gamma_distance_angstrom": None,
            "best_any_auth_chain_relation": "not_reviewed_structure_too_large",
            "best_cross_auth_chain_distance_angstrom": None,
            "best_cross_polymer_entity_distance_angstrom": None,
            "nearest_gamma_metal_distance_angstrom": None,
            "nearest_gamma_metal_code": None,
            "local_metal_context_review_only": False,
            "nonconfounded_inter_auth_chain_within_cutoff": False,
            "nonconfounded_cross_polymer_entity_within_cutoff": False,
            "raw_coordinate_dump_written": False,
        }
    polymer_entities = polymer_entity_by_chain(atoms)
    gamma_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM"
        and atom_code(atom) == ligand_code
        and atom_name(atom) == "PG"
    ]
    acceptor_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "ATOM"
        and ACCEPTOR_ATOMS.get(atom_code(atom)) == atom_name(atom)
    ]
    metal_atoms = [
        atom
        for atom in atoms
        if atom.get("group_PDB") == "HETATM" and atom_code(atom) in METAL_CODES
    ]

    best_any: dict[str, Any] | None = None
    best_cross_auth: dict[str, Any] | None = None
    best_cross_entity: dict[str, Any] | None = None
    for acceptor in acceptor_atoms:
        for gamma in gamma_atoms:
            try:
                distance = atom_distance(acceptor, gamma)
            except (KeyError, TypeError, ValueError):
                continue
            gamma_chain = atom_chain(gamma)
            acceptor_chain = atom_chain(acceptor)
            gamma_entity = polymer_entities.get(gamma_chain)
            acceptor_entity = atom_entity(acceptor)
            hit = {
                "distance": distance,
                "acceptor_residue_code": atom_code(acceptor),
                "acceptor_atom_name": atom_name(acceptor),
                "acceptor_auth_chain": acceptor_chain,
                "acceptor_auth_seq_id": str(
                    acceptor.get("auth_seq_id") or acceptor.get("label_seq_id") or ""
                ),
                "acceptor_entity_id": acceptor_entity,
                "gamma_auth_chain": gamma_chain,
                "gamma_polymer_entity_id": gamma_entity,
                "gamma_ligand_code": atom_code(gamma),
                "gamma_atom_name": atom_name(gamma),
            }
            if best_any is None or distance < float(best_any["distance"]):
                best_any = hit
            if acceptor_chain and gamma_chain and acceptor_chain != gamma_chain:
                if best_cross_auth is None or distance < float(best_cross_auth["distance"]):
                    best_cross_auth = hit
            if (
                acceptor_entity
                and gamma_entity
                and acceptor_entity != gamma_entity
                and (best_cross_entity is None or distance < float(best_cross_entity["distance"]))
            ):
                best_cross_entity = hit

    nearest_metal: dict[str, Any] | None = None
    for gamma in gamma_atoms:
        for metal in metal_atoms:
            try:
                distance = atom_distance(gamma, metal)
            except (KeyError, TypeError, ValueError):
                continue
            hit = {
                "distance": distance,
                "metal_code": atom_code(metal),
                "metal_auth_chain": atom_chain(metal),
                "gamma_auth_chain": atom_chain(gamma),
            }
            if nearest_metal is None or distance < float(nearest_metal["distance"]):
                nearest_metal = hit

    any_relation = "none_found"
    if best_any is not None:
        any_relation = (
            "same_auth_chain"
            if best_any.get("acceptor_auth_chain") == best_any.get("gamma_auth_chain")
            else "cross_auth_chain"
        )
    cross_auth_distance = round_distance(
        float(best_cross_auth["distance"]) if best_cross_auth else None
    )
    cross_entity_distance = round_distance(
        float(best_cross_entity["distance"]) if best_cross_entity else None
    )
    nearest_metal_distance = round_distance(
        float(nearest_metal["distance"]) if nearest_metal else None
    )
    return {
        "pdb_id": pdb_id,
        "fetch_status": "fetched",
        "terminal_gamma_atom_detected": bool(gamma_atoms),
        "terminal_gamma_atom_name": "PG" if gamma_atoms else None,
        "gamma_ligand_code": ligand_code if gamma_atoms else None,
        "best_any_ser_thr_tyr_gamma_distance_angstrom": round_distance(
            float(best_any["distance"]) if best_any else None
        ),
        "best_any_auth_chain_relation": any_relation,
        "best_cross_auth_chain_distance_angstrom": cross_auth_distance,
        "best_cross_polymer_entity_distance_angstrom": cross_entity_distance,
        "nearest_gamma_metal_distance_angstrom": nearest_metal_distance,
        "nearest_gamma_metal_code": nearest_metal.get("metal_code") if nearest_metal else None,
        "local_metal_context_review_only": (
            nearest_metal_distance is not None and nearest_metal_distance <= local_metal_cutoff
        ),
        "nonconfounded_inter_auth_chain_within_cutoff": (
            cross_auth_distance is not None and cross_auth_distance <= cutoff
        ),
        "nonconfounded_cross_polymer_entity_within_cutoff": (
            cross_entity_distance is not None and cross_entity_distance <= cutoff
        ),
        "raw_coordinate_dump_written": False,
    }


def topology_status(row: dict[str, Any]) -> str:
    best_cross = row.get("best_cross_auth_chain_distance_angstrom")
    best_any = row.get("best_any_ser_thr_tyr_gamma_distance_angstrom")
    if row.get("nonconfounded_inter_auth_chain_within_cutoff"):
        return f"cross_auth_chain_candidate_distance_{best_cross}A"
    if best_cross is not None:
        return f"same_auth_chain_best_acceptor_cross_chain_distance_{best_cross}A"
    if best_any is not None:
        return "same_auth_chain_best_acceptor_no_cross_auth_chain_acceptor_found"
    return "no_ser_thr_tyr_acceptor_found"


def ligand_slug(ligand_code: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", ligand_code.lower()).strip("_") or "ligand"


def build_tranche_row(row: dict[str, Any], *, ligand_code: str) -> dict[str, Any]:
    nearest_acceptor = row.get("best_any_ser_thr_tyr_gamma_distance_angstrom")
    if row.get("nonconfounded_inter_auth_chain_within_cutoff"):
        nearest_acceptor = row.get("best_cross_auth_chain_distance_angstrom")
    local_metal = bool(row.get("local_metal_context_review_only"))
    slug = ligand_slug(ligand_code)
    return {
        "row_id": f"pdb:{row['pdb_id']}",
        "pdb_id": row["pdb_id"],
        "row_role": (
            f"fresh_{slug}_nonconfounded_folded_role_identity_lead_review_only"
            if row.get("nonconfounded_inter_auth_chain_within_cutoff")
            else f"fresh_{slug}_same_chain_or_no_cross_chain_tripwire"
        ),
        "freshness_status": "not_present_in_existing_artifacts_before_this_run",
        "clean_held_out_performance_evidence": False,
        "development_or_regression_context": False,
        "ligand_code_from_structure": ligand_code,
        "terminal_gamma_equivalent_geometry": bool(row.get("terminal_gamma_atom_detected")),
        "terminal_gamma_atom_name": row.get("terminal_gamma_atom_name"),
        "nearest_gamma_acceptor_distance_angstrom": nearest_acceptor,
        "local_metal_context": local_metal,
        "catalytic_site_locality": local_metal,
        "source_free_acceptor_role_features": False,
        "source_free_acceptor_role_policy_id": None,
        "same_structure_co_materialization": False,
        "product_state_context": False,
        "substrate_acceptor_analog_context": False,
        "split_state_context": False,
        "candidate_specific_source_repair": False,
        "source_review_used_for_predictive_feature": False,
        "source_validation_used_for_predictive_feature": False,
        "source_text_used_for_predictive_feature": False,
        "structure_title_used_for_predictive_feature": False,
        "source_id_as_predictive_feature": False,
        "candidate_specific_source_repair_used_for_predictive_feature": False,
        "topology_ambiguity_status": topology_status(row),
        "source_validation_phase": "after_source_free_local_feature_review",
        "source_validation_status": "not_used_for_prediction_review_only_unresolved",
        "post_score_review_status": (
            f"fresh_{slug}_surface_review_only_no_source_free_role_policy"
        ),
        "expected_frozen_policy_decision": "review_only_abstain_missing_source_free_acceptor_role",
    }


def sort_representative_rows(row: dict[str, Any]) -> tuple[int, float, str]:
    cross = row.get("best_cross_auth_chain_distance_angstrom")
    any_distance = row.get("best_any_ser_thr_tyr_gamma_distance_angstrom")
    distance = cross if cross is not None else any_distance
    if distance is None:
        distance = 9999.0
    return (
        0 if row.get("nonconfounded_inter_auth_chain_within_cutoff") else 1,
        float(distance),
        str(row.get("pdb_id")),
    )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def build_artifacts(args: argparse.Namespace) -> tuple[Path, Path]:
    root = Path(args.root).resolve()
    timestamp_slug = args.timestamp.replace("-", "").replace(":", "").replace("Z", "Z")
    if args.surface_prefix:
        prefix_base = args.surface_prefix
    elif args.query_mode == "chemcomp":
        prefix_base = (
            "epk_fresh_rcsb_chemcomp_"
            f"{ligand_slug(args.ligand_code)}_terminal_gamma_search_surface"
        )
    else:
        prefix_base = f"epk_fresh_{ligand_slug(args.ligand_code)}_folded_role_identity_search_surface"
    prefix = f"{prefix_base}_{timestamp_slug}"
    artifact_dir = root / "artifacts" / "research_lanes" / LANE_ID
    search_surface_path = artifact_dir / f"{prefix}.json"
    tranche_path = artifact_dir / f"{prefix}_tranche.json"
    output_paths = {search_surface_path, tranche_path}

    query_ids, query_description, source_description = rcsb_candidate_ids(args)
    seen_ids = (
        set()
        if args.skip_existing_scan
        else ids_seen_in_existing_artifacts(
            root,
            query_ids,
            output_paths,
            max_existing_text_bytes=args.max_existing_text_bytes,
        )
    )
    selected_ids = [pdb_id for pdb_id in query_ids if pdb_id not in seen_ids][: args.fresh_limit]
    if not selected_ids:
        raise ValueError("RCSB query returned no fresh candidate ids for this surface")

    scan_rows: list[dict[str, Any]] = []
    fetch_failures: list[dict[str, str]] = []
    for pdb_id in selected_ids:
        print(f"scanning {pdb_id}", file=sys.stderr, flush=True)
        try:
            scan_rows.append(
                compact_structure_summary(
                    pdb_id,
                    ligand_code=args.ligand_code,
                    cutoff=args.cutoff,
                    local_metal_cutoff=args.local_metal_cutoff,
                    max_atoms=args.max_atoms,
                )
            )
        except Exception as exc:  # pragma: no cover - live network/data failure.
            fetch_failures.append(
                {"pdb_id": pdb_id, "fetch_status": "failed", "error": str(exc)[:200]}
            )

    nonconfounded_count = sum(
        1 for row in scan_rows if row.get("nonconfounded_inter_auth_chain_within_cutoff")
    )
    terminal_gamma_rows = [
        row for row in scan_rows if row.get("terminal_gamma_atom_detected") is True
    ]
    terminal_gamma_count = len(terminal_gamma_rows)
    representative_pool = terminal_gamma_rows if args.terminal_gamma_tranche_only else scan_rows
    if args.terminal_gamma_tranche_only and not representative_pool:
        raise ValueError(
            "terminal-gamma tranche requested but no fetched candidate had "
            f"{args.ligand_code} PG detected"
        )
    search_surface_exhausted = nonconfounded_count == 0 and bool(representative_pool)
    search_surface = {
        "metadata": {
            "artifact_id": prefix,
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "source": source_description,
            "query": query_description,
            "query_mode": args.query_mode,
            "query_rows_requested": args.query_rows,
            "candidate_ids_frozen_before_local_feature_review": True,
            "source_free_local_features_computed_before_source_validation": True,
            "source_validation_applied_after_local_features": True,
            "source_validation_review_only": True,
            "topology_review_contract": {
                "topology_status_required": True,
                "cross_chain_geometry_review_only_without_preaccepted_role_policy": True,
                "role_policy_status": "none_accepted_in_policy_v0",
            },
            "ligand_code": args.ligand_code,
            "chem_comp_id": args.chem_comp_id.upper(),
            "candidate_distance_cutoff_angstrom": args.cutoff,
            "local_metal_context_review_cutoff_angstrom": args.local_metal_cutoff,
            "terminal_gamma_required_for_tranche": bool(args.terminal_gamma_tranche_only),
            "terminal_gamma_atom_name_required": "PG",
            "terminal_gamma_candidate_count_reviewed": terminal_gamma_count,
            "terminal_gamma_eligible_ids_reviewed": [
                row["pdb_id"] for row in terminal_gamma_rows
            ],
            "terminal_gamma_missing_or_skipped_ids": [
                row["pdb_id"]
                for row in scan_rows
                if row.get("terminal_gamma_atom_detected") is not True
            ],
            "candidate_id_selection": (
                "query_page_ids_existing_artifact_scan_skipped"
                if args.skip_existing_scan
                else "query_page_ids_not_seen_in_lane_artifacts_before_this_run"
            ),
            "existing_artifact_scan_scope": "lane_artifacts_and_lane_work_only",
            "candidate_ids_reviewed": selected_ids,
            "candidate_ids_not_seen_in_lane_artifacts_before_this_run": (
                [] if args.skip_existing_scan else selected_ids
            ),
            "candidate_ids_not_seen_in_existing_artifacts_before_this_run": (
                [] if args.skip_existing_scan else selected_ids
            ),
            "existing_artifact_scan_skipped": bool(args.skip_existing_scan),
            "fresh_candidate_count_reviewed": len(scan_rows),
            "fetch_failure_count": len(fetch_failures),
            "row_count": len(scan_rows),
            "nonconfounded_inter_auth_chain_candidate_count_within_cutoff": nonconfounded_count,
            "nonconfounded_cross_polymer_entity_candidate_count_within_cutoff": sum(
                1
                for row in scan_rows
                if row.get("nonconfounded_cross_polymer_entity_within_cutoff")
            ),
            "search_surface_exhausted": search_surface_exhausted,
            "search_surface_scope": (
                f"first {len(selected_ids)} selected ids from a bounded "
                f"{args.ligand_code} "
                f"{args.query_mode} surface; this does not exhaust all possible RCSB "
                "ePK structures"
            ),
            "raw_coordinate_dump_written": False,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "rows": scan_rows,
        "fetch_failures": fetch_failures,
    }
    write_json(search_surface_path, search_surface)

    representative_rows = sorted(representative_pool, key=sort_representative_rows)[
        : args.tranche_rows
    ]
    tranche = {
        "metadata": {
            "tranche_id": f"{prefix}_tranche",
            "created_at": args.timestamp,
            "lane_id": LANE_ID,
            "review_only": True,
            "clean_held_out_performance_evidence": False,
            "row_count": len(representative_rows),
            "search_surface_exhausted": search_surface_exhausted,
            "search_surface_candidate_count_reviewed": len(scan_rows),
            "nonconfounded_candidate_count_within_cutoff": nonconfounded_count,
            "source_query_mode": args.query_mode,
            "chem_comp_id": args.chem_comp_id.upper(),
            "terminal_gamma_required_for_tranche": bool(args.terminal_gamma_tranche_only),
            "terminal_gamma_atom_name_required": "PG",
            "terminal_gamma_candidate_count_reviewed": terminal_gamma_count,
            "description": (
                f"Compact review-only stress tranche for the fresh {args.ligand_code} "
                "nonconfounded "
                "folded substrate-role identity surface. Candidate ids were frozen "
                "before local feature review; source validation remains downstream "
                "and review-only. When terminal_gamma_required_for_tranche is true, "
                f"only rows with observed {args.ligand_code} PG are admitted to the tranche."
            ),
            "source_artifacts": [
                "artifacts/research_lanes/epk_policy_harness/epk_policy_v0_20260520.json",
                str(search_surface_path.relative_to(root)),
            ],
            "source_validation_phase_contract": {
                "candidate_ids_frozen_before_local_feature_review": True,
                "source_free_local_features_computed_before_source_validation": True,
                "source_validation_applied_after_local_features": True,
                "source_validation_review_only": True,
                "review_only_source_validation_fields": [
                    "source_validation_status",
                    "source_validation_phase",
                    "post_score_review_status",
                    "structure_title",
                    "entity_descriptions",
                ],
            },
            "topology_review_contract": {
                "topology_status_required": True,
                "cross_chain_geometry_review_only_without_preaccepted_role_policy": True,
                "role_policy_status": "none_accepted_in_policy_v0",
            },
        },
        "rows": [
            build_tranche_row(row, ligand_code=args.ligand_code)
            for row in representative_rows
        ],
    }
    write_json(tranche_path, tranche)
    return search_surface_path, tranche_path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build compact review-only ePK fresh ligand search-surface artifacts."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--query-mode", choices=("full_text", "chemcomp"), default="full_text")
    parser.add_argument("--query", default="protein kinase ATP magnesium substrate")
    parser.add_argument("--chem-comp-id", default="ATP")
    parser.add_argument("--query-rows", type=int, default=80)
    parser.add_argument("--fresh-limit", type=int, default=35)
    parser.add_argument("--tranche-rows", type=int, default=6)
    parser.add_argument("--ligand-code", default="ATP")
    parser.add_argument("--cutoff", type=float, default=6.0)
    parser.add_argument("--local-metal-cutoff", type=float, default=4.5)
    parser.add_argument("--max-atoms", type=int, default=120000)
    parser.add_argument("--max-existing-text-bytes", type=int, default=2_000_000)
    parser.add_argument("--skip-existing-scan", action="store_true")
    parser.add_argument("--terminal-gamma-tranche-only", action="store_true")
    parser.add_argument("--surface-prefix")
    parser.add_argument("--timestamp", default=utc_now())
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.query_rows <= 0:
        raise ValueError("--query-rows must be positive")
    if args.fresh_limit <= 0:
        raise ValueError("--fresh-limit must be positive")
    if args.tranche_rows <= 0:
        raise ValueError("--tranche-rows must be positive")
    if not args.chem_comp_id.strip():
        raise ValueError("--chem-comp-id must be non-empty")
    if args.max_atoms <= 0:
        raise ValueError("--max-atoms must be positive")
    if args.max_existing_text_bytes <= 0:
        raise ValueError("--max-existing-text-bytes must be positive")
    search_surface_path, tranche_path = build_artifacts(args)
    print(search_surface_path)
    print(tranche_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
