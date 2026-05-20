#!/usr/bin/env python3
"""Audit ePK review-only chain namespace pressure paths.

This lane helper fetches a bounded set of pressure PDB IDs in memory, compares
auth-preferred topology with label-only and mixed namespace variants, and emits
compact evidence only. It does not write raw coordinates.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import time
from pathlib import Path
from typing import Any

import atpase_substrate_mode_stress as base


LANE_ID = "epk_false_positive_hunter"
PRESSURE_IDS = ["5TT6", "6NOO", "9NBW", "4KFT", "1A82", "3C9S"]
CURRENT_ATP_LIKE_LIGANDS = {"A3P", "ACP", "AGS", "ANP", "ATP"}
PATHS_UNDER_AUDIT = {
    "current_auth": ("auth", "auth"),
    "actual_materializer_auth_prefer": ("auth_prefer", "auth_prefer"),
    "label_only_hazard": ("label", "label"),
    "label_prefer_hazard": ("label_prefer", "label_prefer"),
    "mixed_label_ligand_auth_acceptor_hazard": ("label", "auth"),
    "id_intersection_guard": ("intersection", "intersection"),
}
CODE_PATH_PATTERNS = [
    {
        "file": "src/catalytic_earth/structure.py",
        "purpose": "shared ligand-context grouping prefers author chain ids",
        "pattern": 'chain = str(atom.get("auth_asym_id") or atom.get("label_asym_id") or "")',
    },
    {
        "file": "src/catalytic_earth/labels.py",
        "purpose": "heteromeric materializer stores acceptor chain as auth_asym_id with label fallback",
        "pattern": 'str(atom.get("auth_asym_id") or atom.get("label_asym_id") or ""),',
    },
    {
        "file": "src/catalytic_earth/labels.py",
        "purpose": "heteromeric materializer stores gamma ligand chain as auth_asym_id with label fallback",
        "pattern": 'nearest_gamma.get("auth_asym_id")',
    },
    {
        "file": "src/catalytic_earth/labels.py",
        "purpose": "MEK/ERK topology counteraxis compares materialized candidate and gamma chain fields",
        "pattern": '== str(hit.get("gamma_associated_polymer_chain_name") or "")',
    },
    {
        "file": "src/catalytic_earth/labels.py",
        "purpose": "substrate-mode counteraxis uses materialized auth sequence ids for N-terminal mode",
        "pattern": 'auth_seq_id = _optional_int(hit.get("candidate_auth_seq_id"))',
    },
]


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def intish(value: Any) -> int | None:
    match = re.match(r"^-?\d+", str(value or ""))
    return int(match.group(0)) if match else None


def chain(atom: dict[str, Any], mode: str) -> str:
    auth = str(atom.get("auth_asym_id") or "")
    label = str(atom.get("label_asym_id") or "")
    if mode == "auth":
        return auth
    if mode == "label":
        return label
    if mode == "auth_prefer":
        return auth or label
    if mode == "label_prefer":
        return label or auth
    raise ValueError(f"unsupported chain mode: {mode}")


def chain_ids(atom: dict[str, Any]) -> set[str]:
    return {
        str(value)
        for value in (atom.get("auth_asym_id"), atom.get("label_asym_id"))
        if value not in {None, "", ".", "?"}
    }


def chains_same(left: dict[str, Any], right: dict[str, Any], mode: str) -> bool:
    if mode == "intersection":
        return bool(chain_ids(left) & chain_ids(right))
    return bool(chain(left, mode) and chain(left, mode) == chain(right, mode))


def chain_pair(left: dict[str, Any], right: dict[str, Any], mode: str) -> tuple[str, str]:
    if mode == "intersection":
        return ("|".join(sorted(chain_ids(left))), "|".join(sorted(chain_ids(right))))
    return chain(left, mode), chain(right, mode)


def terminal_p_atoms(atoms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    preferred = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["type_symbol"] == "P"
        and base.atom_comp(atom) in CURRENT_ATP_LIKE_LIGANDS
        and base.norm_atom_name(atom) in base.TERMINAL_PHOSPHATE_NAMES
    ]
    fallback = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and atom["type_symbol"] == "P"
        and base.atom_comp(atom) in CURRENT_ATP_LIKE_LIGANDS
    ]
    return preferred or fallback


def compact_acceptor(acceptor: dict[str, Any], terminal: dict[str, Any], distance: float) -> dict[str, Any]:
    residue = base.atom_comp(acceptor)
    seq_id = intish(acceptor.get("auth_seq_id"))
    n_terminal = seq_id is not None and seq_id <= base.MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID
    tyrosine = residue == "TYR"
    return {
        "auth_chain": chain(acceptor, "auth"),
        "label_chain": chain(acceptor, "label"),
        "auth_seq_id": acceptor.get("auth_seq_id"),
        "label_seq_id": acceptor.get("label_seq_id"),
        "residue": residue,
        "atom": base.norm_atom_name(acceptor),
        "distance_angstrom": round(distance, 3),
        "n_terminal_acceptor": n_terminal,
        "tyrosine_acceptor": tyrosine,
        "substrate_mode_rule_hit": bool(n_terminal or tyrosine),
        "auth_same_chain_to_ligand": chains_same(acceptor, terminal, "auth"),
        "label_same_chain_to_ligand": chains_same(acceptor, terminal, "label"),
        "id_intersection_same_chain_to_ligand": chains_same(acceptor, terminal, "intersection"),
    }


def summarize_hit_paths(hit: dict[str, Any]) -> dict[str, dict[str, Any]]:
    terminal = hit["_terminal_atom"]
    acceptors = hit["_acceptor_atoms"]
    path_summaries: dict[str, dict[str, Any]] = {}
    for path_name, (ligand_mode, acceptor_mode) in PATHS_UNDER_AUDIT.items():
        all_pairs: list[tuple[str, str]] = []
        mode_pairs: list[tuple[str, str]] = []
        cross_chain_mode_hits = []
        same_chain_mode_hits = []
        same_chain_flags = []
        for acceptor, compact in acceptors:
            if ligand_mode == "intersection" or acceptor_mode == "intersection":
                same_chain = chains_same(acceptor, terminal, "intersection")
                pair = chain_pair(acceptor, terminal, "intersection")
            else:
                acceptor_chain = chain(acceptor, acceptor_mode)
                ligand_chain = chain(terminal, ligand_mode)
                same_chain = bool(acceptor_chain and acceptor_chain == ligand_chain)
                pair = (acceptor_chain, ligand_chain)
            all_pairs.append(pair)
            same_chain_flags.append(same_chain)
            if compact["substrate_mode_rule_hit"]:
                mode_pairs.append(pair)
                if same_chain:
                    same_chain_mode_hits.append(compact)
                else:
                    cross_chain_mode_hits.append(compact)
        same_chain_topology = any(same_chain_flags)
        reciprocal_topology = any(
            left_candidate == right_ligand
            and left_ligand == right_candidate
            and left_candidate != left_ligand
            for left_index, (left_candidate, left_ligand) in enumerate(all_pairs)
            for right_candidate, right_ligand in all_pairs[left_index + 1 :]
        )
        topology_ambiguity = same_chain_topology or reciprocal_topology
        topology_clear_cross_chain_mode_hit_count = (
            len(cross_chain_mode_hits) if not topology_ambiguity else 0
        )
        path_summaries[path_name] = {
            "ligand_chain_mode": ligand_mode,
            "acceptor_chain_mode": acceptor_mode,
            "mode_hit_count": len(mode_pairs),
            "same_chain_mode_hit_count": len(same_chain_mode_hits),
            "cross_chain_mode_hit_count": len(cross_chain_mode_hits),
            "same_chain_topology_detected": same_chain_topology,
            "reciprocal_cross_chain_topology_detected": reciprocal_topology,
            "topology_ambiguity_counteraxis_hit": topology_ambiguity,
            "topology_clear_cross_chain_mode_hit_count": topology_clear_cross_chain_mode_hit_count,
            "primary_cross_chain_mode_hit": cross_chain_mode_hits[0] if cross_chain_mode_hits else None,
        }
    return path_summaries


def summarize_entry_paths(raw_hits: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    path_summaries: dict[str, dict[str, Any]] = {}
    for path_name, (ligand_mode, acceptor_mode) in PATHS_UNDER_AUDIT.items():
        all_pairs: list[tuple[str, str]] = []
        mode_pairs: list[tuple[str, str]] = []
        cross_chain_mode_hits = []
        same_chain_mode_hits = []
        same_chain_flags = []
        for hit in raw_hits:
            terminal = hit["_terminal_atom"]
            for acceptor, compact in hit["_acceptor_atoms"]:
                if ligand_mode == "intersection" or acceptor_mode == "intersection":
                    same_chain = chains_same(acceptor, terminal, "intersection")
                    pair = chain_pair(acceptor, terminal, "intersection")
                else:
                    acceptor_chain = chain(acceptor, acceptor_mode)
                    ligand_chain = chain(terminal, ligand_mode)
                    same_chain = bool(acceptor_chain and acceptor_chain == ligand_chain)
                    pair = (acceptor_chain, ligand_chain)
                all_pairs.append(pair)
                same_chain_flags.append(same_chain)
                if compact["substrate_mode_rule_hit"]:
                    mode_pairs.append(pair)
                    if same_chain:
                        same_chain_mode_hits.append(compact)
                    else:
                        cross_chain_mode_hits.append(compact)
        same_chain_topology = any(same_chain_flags)
        reciprocal_topology = any(
            left_candidate == right_ligand
            and left_ligand == right_candidate
            and left_candidate != left_ligand
            for left_index, (left_candidate, left_ligand) in enumerate(all_pairs)
            for right_candidate, right_ligand in all_pairs[left_index + 1 :]
        )
        topology_ambiguity = same_chain_topology or reciprocal_topology
        topology_clear_cross_chain_mode_hit_count = (
            len(cross_chain_mode_hits) if not topology_ambiguity else 0
        )
        path_summaries[path_name] = {
            "ligand_chain_mode": ligand_mode,
            "acceptor_chain_mode": acceptor_mode,
            "mode_hit_count": len(mode_pairs),
            "same_chain_mode_hit_count": len(same_chain_mode_hits),
            "cross_chain_mode_hit_count": len(cross_chain_mode_hits),
            "same_chain_topology_detected": same_chain_topology,
            "reciprocal_cross_chain_topology_detected": reciprocal_topology,
            "topology_ambiguity_counteraxis_hit": topology_ambiguity,
            "topology_clear_cross_chain_mode_hit_count": topology_clear_cross_chain_mode_hit_count,
            "primary_cross_chain_mode_hit": cross_chain_mode_hits[0] if cross_chain_mode_hits else None,
        }
    return path_summaries


def summarize_entry(pdb_id: str) -> dict[str, Any]:
    cif_text = base.fetch_text(base.RCSB_CIF_URL.format(pdb_id=pdb_id))
    entry = base.fetch_json(base.RCSB_ENTRY_URL.format(pdb_id=pdb_id))
    title = entry.get("struct", {}).get("title", "")
    keywords = base.entry_keywords(entry)
    polymer_summaries = base.fetch_polymer_summaries(pdb_id, entry)
    context_text = " ".join(
        str(part or "")
        for part in [
            title,
            keywords.get("pdbx_keywords"),
            keywords.get("text"),
            " ".join(str(summary.get("description") or "") for summary in polymer_summaries),
        ]
    )
    atoms = base.parse_atom_site(cif_text)
    magnesium_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "HETATM"
        and (base.atom_comp(atom) in base.MAGNESIUM_CODES or atom["type_symbol"] == "MG")
    ]
    acceptor_atoms = [
        atom
        for atom in atoms
        if atom["group"] == "ATOM"
        and (base.atom_comp(atom), base.norm_atom_name(atom)) in base.ACCEPTOR_ATOMS
    ]
    hits = []
    for terminal in terminal_p_atoms(atoms):
        mg_distances = [base.distance(terminal, mg_atom) for mg_atom in magnesium_atoms]
        nearest_mg = min(mg_distances) if mg_distances else None
        if nearest_mg is None or nearest_mg > base.MG_DISTANCE_CUTOFF_ANGSTROM:
            continue
        nearby = []
        for acceptor in acceptor_atoms:
            distance = base.distance(terminal, acceptor)
            if distance <= base.DISTANCE_CUTOFF_ANGSTROM:
                nearby.append((acceptor, compact_acceptor(acceptor, terminal, distance)))
        nearby.sort(key=lambda item: item[1]["distance_angstrom"])
        if not nearby:
            continue
        hit: dict[str, Any] = {
            "ligand": base.atom_comp(terminal),
            "terminal_p_atom": base.norm_atom_name(terminal),
            "auth_ligand_chain": chain(terminal, "auth"),
            "label_ligand_chain": chain(terminal, "label"),
            "ligand_auth_seq_id": terminal.get("auth_seq_id"),
            "ligand_label_seq_id": terminal.get("label_seq_id"),
            "nearest_mg_distance_angstrom": round(nearest_mg, 3),
            "nearby_acceptor_count": len(nearby),
            "substrate_mode_acceptor_count": sum(
                1 for _, acceptor in nearby if acceptor["substrate_mode_rule_hit"]
            ),
            "nearest_acceptors": [acceptor for _, acceptor in nearby[:8]],
            "_terminal_atom": terminal,
            "_acceptor_atoms": nearby,
        }
        hit["path_summaries"] = summarize_hit_paths(hit)
        hits.append(hit)
    hits.sort(
        key=lambda hit: (
            0 if hit["substrate_mode_acceptor_count"] else 1,
            hit["nearest_acceptors"][0]["distance_angstrom"] if hit["nearest_acceptors"] else 99,
            str(hit["auth_ligand_chain"]),
        )
    )
    entry_path_summaries = summarize_entry_paths(hits)
    compact_hits = []
    for hit in hits[:6]:
        compact_hit = dict(hit)
        compact_hit.pop("_terminal_atom")
        compact_hit.pop("_acceptor_atoms")
        compact_hits.append(compact_hit)
    return {
        "pdb_id": pdb_id,
        "title": title,
        "keywords": keywords,
        "polymer_entities": polymer_summaries,
        "probable_epk_from_context": base.looks_probable_epk(context_text),
        "terminal_p_atom_count": len(terminal_p_atoms(atoms)),
        "mg_atom_count": len(magnesium_atoms),
        "acceptor_atom_count": len(acceptor_atoms),
        "reviewed": True,
        "local_hit_count": len(hits),
        "entry_path_summaries": entry_path_summaries,
        "hits": compact_hits,
    }


def source_line_evidence(repo_root: Path) -> list[dict[str, Any]]:
    evidence = []
    for item in CODE_PATH_PATTERNS:
        path = repo_root / item["file"]
        matches = []
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            evidence.append({**item, "read_error": str(exc), "matches": []})
            continue
        for index, line in enumerate(lines, start=1):
            if item["pattern"] in line:
                matches.append({"line": index, "excerpt": line.strip()})
                if len(matches) >= 5:
                    break
        evidence.append({**item, "matches": matches})
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    rows = []
    fetch_errors: dict[str, str] = {}
    for pdb_id in PRESSURE_IDS:
        try:
            rows.append(summarize_entry(pdb_id))
        except Exception as exc:  # pragma: no cover - recorded as evidence.
            fetch_errors[pdb_id] = repr(exc)
        time.sleep(0.2)

    path_totals: dict[str, dict[str, int]] = {
        path: {
            "entries_with_topology_clear_cross_chain_mode_hit": 0,
            "topology_clear_cross_chain_mode_hit_count": 0,
            "entries_with_same_chain_topology": 0,
            "entries_with_reciprocal_topology": 0,
        }
        for path in PATHS_UNDER_AUDIT
    }
    for row in rows:
        for path_name, summary in row.get("entry_path_summaries", {}).items():
            clear_count = int(summary.get("topology_clear_cross_chain_mode_hit_count") or 0)
            path_totals[path_name]["topology_clear_cross_chain_mode_hit_count"] += clear_count
            if clear_count > 0:
                path_totals[path_name]["entries_with_topology_clear_cross_chain_mode_hit"] += 1
            if summary.get("same_chain_topology_detected"):
                path_totals[path_name]["entries_with_same_chain_topology"] += 1
            if summary.get("reciprocal_cross_chain_topology_detected"):
                path_totals[path_name]["entries_with_reciprocal_topology"] += 1

    current_counterexamples = [
        row["pdb_id"]
        for row in rows
        if int(
            row.get("entry_path_summaries", {})
            .get("current_auth", {})
            .get("topology_clear_cross_chain_mode_hit_count")
            or 0
        )
        > 0
        and not row.get("probable_epk_from_context")
    ]
    label_hazard_ids = [
        row["pdb_id"]
        for row in rows
        if int(
            row.get("entry_path_summaries", {})
            .get("label_only_hazard", {})
            .get("topology_clear_cross_chain_mode_hit_count")
            or 0
        )
        > 0
    ]
    payload = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "epk_review_only_namespace_path_audit",
            "started_at": args.started_at,
            "ended_at": now_utc(),
            "review_only": True,
            "rule_under_attack": (
                "epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0 "
                "plus epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0"
            ),
            "search_surface": {
                "pressure_pdb_ids": PRESSURE_IDS,
                "path_variants": {
                    name: {"ligand_chain_mode": modes[0], "acceptor_chain_mode": modes[1]}
                    for name, modes in PATHS_UNDER_AUDIT.items()
                },
                "candidate_threshold_angstrom": base.DISTANCE_CUTOFF_ANGSTROM,
                "mg_distance_cutoff_angstrom": base.MG_DISTANCE_CUTOFF_ANGSTROM,
                "max_n_terminal_acceptor_auth_seq_id": base.MAX_N_TERMINAL_ACCEPTOR_AUTH_SEQ_ID,
                "current_atp_like_ligands": sorted(CURRENT_ATP_LIKE_LIGANDS),
                "raw_coordinate_files_written": False,
            },
            "rows_reviewed": len(rows),
            "fetch_error_count": len(fetch_errors),
            "counterexample_count_current_auth": len(current_counterexamples),
            "counterexample_pdb_ids_current_auth": sorted(current_counterexamples),
            "label_namespace_hazard_pdb_ids": sorted(label_hazard_ids),
            "path_totals": path_totals,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
        },
        "source_line_evidence": source_line_evidence(Path(args.repo_root)),
        "fetch_errors": fetch_errors,
        "rows": rows,
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
