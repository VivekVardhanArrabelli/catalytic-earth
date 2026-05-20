#!/usr/bin/env python3
"""Audit legacy ANP/PB terminal-phosphate naming in prior ePK lane scouts.

This helper keeps coordinate use transient. It records compact structure,
ligand-group, and distance summaries only.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LANE_ID = "epk_positive_evidence"
TARGET_FAMILY_ID = "epk"
TARGET_FINGERPRINT_ID = "epk_atp_gamma_phosphoryl_transfer"
RCSB_ANP_SEARCH = {
    "query": {
        "type": "terminal",
        "service": "text",
        "parameters": {
            "attribute": "rcsb_nonpolymer_entity_container_identifiers.nonpolymer_comp_id",
            "operator": "exact_match",
            "value": "ANP",
        },
    },
    "return_type": "entry",
    "request_options": {
        "paginate": {"start": 0, "rows": 2000},
        "results_content_type": ["experimental"],
    },
}


def load_epk_helper() -> Any:
    helper_path = Path(__file__).with_name("epk_evidence_search.py")
    spec = importlib.util.spec_from_file_location("epk_evidence_search", helper_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load helper from {helper_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["epk_evidence_search"] = module
    spec.loader.exec_module(module)
    return module


epk = load_epk_helper()


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def collect_prior_scout_ids(artifact_dir: Path, output_name: str) -> tuple[dict[str, set[str]], list[str]]:
    pdb_to_seed_files: dict[str, set[str]] = defaultdict(set)
    seed_files: list[str] = []
    for path in sorted(artifact_dir.glob("*scout*.json")):
        if path.name == output_name:
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        seed_files.append(str(path))

        def walk(value: Any) -> None:
            if isinstance(value, dict):
                pdb_id = value.get("pdb_id")
                if is_pdb_id(pdb_id):
                    pdb_to_seed_files[pdb_id.upper()].add(str(path))
                pdb_ids = value.get("pdb_ids")
                if isinstance(pdb_ids, list):
                    for candidate in pdb_ids:
                        if is_pdb_id(candidate):
                            pdb_to_seed_files[candidate.upper()].add(str(path))
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(data)
    return pdb_to_seed_files, seed_files


def is_pdb_id(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 4 and value[0].isdigit()


def search_anp_entries() -> set[str]:
    result = epk.fetch_json(epk.RCSB_SEARCH_URL, payload=RCSB_ANP_SEARCH, timeout=30)
    return {row["identifier"].upper() for row in result.get("result_set", [])}


def candidate_entity_context(row: dict[str, Any], hit: dict[str, Any]) -> None:
    entities = row.get("polymer_entities", {})
    candidate_entity = entities.get(str(hit.get("candidate_entity_id")), {})
    gamma_entity = entities.get(str(hit.get("pb_associated_polymer_entity_id")), {})
    hit["candidate_entity_description"] = candidate_entity.get("description")
    hit["candidate_entity_uniprot_ids"] = candidate_entity.get("uniprot_ids", [])
    hit["pb_associated_entity_description"] = gamma_entity.get("description")
    hit["pb_associated_entity_uniprot_ids"] = gamma_entity.get("uniprot_ids", [])


def scan_cif_for_legacy_anp_pb(cif_text: str) -> dict[str, Any]:
    atoms = [atom for row in epk.extract_loop(cif_text, "atom_site") if (atom := epk.atom_from_row(row))]
    polymer_atoms = [atom for atom in atoms if atom["group"] == "ATOM"]
    ligand_atoms = [atom for atom in atoms if atom["group"] == "HETATM"]
    metals = [atom for atom in ligand_atoms if atom["comp"] in epk.METAL_CODES]
    acceptor_atoms = [
        atom
        for atom in polymer_atoms
        if atom["comp"] in epk.ACCEPTOR_ATOMS and atom["atom"] in epk.ACCEPTOR_ATOMS[atom["comp"]]
    ]
    ligand_atoms_by_key: dict[tuple[str | None, str, str | None], list[dict[str, Any]]] = {}
    for atom in ligand_atoms:
        ligand_atoms_by_key.setdefault(epk.ligand_key(atom), []).append(atom)

    anp_groups = []
    legacy_groups = []
    candidate_hits = []
    for key, group_atoms in sorted(ligand_atoms_by_key.items(), key=lambda item: str(item[0])):
        comp = key[1]
        if comp != "ANP":
            continue
        atom_names = sorted({atom["atom"] for atom in group_atoms})
        has_pg = "PG" in atom_names
        has_pb = "PB" in atom_names
        group_record = {
            "label_asym_id": key[0],
            "auth_seq_id": key[2],
            "atom_names": atom_names,
            "has_pg": has_pg,
            "has_pb": has_pb,
            "is_legacy_anp_pb_no_pg": has_pb and not has_pg,
        }
        anp_groups.append(group_record)
        if not (has_pb and not has_pg):
            continue

        associated = epk.nearest_polymer_entity(group_atoms, polymer_atoms)
        associated_entity = associated.get("entity_id") if associated else None
        associated_chain = associated.get("chain") if associated else None
        heteromeric_acceptors = [
            atom
            for atom in acceptor_atoms
            if not (associated_entity is not None and atom.get("entity_id") == associated_entity)
            and not (associated_chain is not None and atom.get("chain") == associated_chain)
        ]
        pb_atoms = [atom for atom in group_atoms if atom["atom"] == "PB"]
        nearest_heteromeric_acceptor = None
        for pb_atom in pb_atoms:
            if heteromeric_acceptors:
                nearest_distance, nearest_acceptor = min(
                    ((epk.dist(pb_atom, acceptor), acceptor) for acceptor in heteromeric_acceptors),
                    key=lambda item: item[0],
                )
                nearest_record = {
                    "candidate_residue_code": nearest_acceptor["comp"],
                    "candidate_atom_name": nearest_acceptor["atom"],
                    "candidate_chain_name": nearest_acceptor.get("chain"),
                    "candidate_entity_id": nearest_acceptor.get("entity_id"),
                    "candidate_auth_seq_id": nearest_acceptor.get("auth_seq_id"),
                    "candidate_label_seq_id": nearest_acceptor.get("label_seq_id"),
                    "nearest_pb_distance_angstrom": round(nearest_distance, 3),
                }
                if (
                    nearest_heteromeric_acceptor is None
                    or nearest_record["nearest_pb_distance_angstrom"]
                    < nearest_heteromeric_acceptor["nearest_pb_distance_angstrom"]
                ):
                    nearest_heteromeric_acceptor = nearest_record

            local_metals = epk.local_metals(pb_atom, metals)
            for acceptor in heteromeric_acceptors:
                distance = epk.dist(pb_atom, acceptor)
                if distance <= 6.0:
                    candidate_hits.append(
                        {
                            "candidate_residue_code": acceptor["comp"],
                            "candidate_atom_name": acceptor["atom"],
                            "candidate_chain_name": acceptor.get("chain"),
                            "candidate_entity_id": acceptor.get("entity_id"),
                            "candidate_auth_seq_id": acceptor.get("auth_seq_id"),
                            "candidate_label_seq_id": acceptor.get("label_seq_id"),
                            "pb_ligand_code": "ANP",
                            "pb_atom_name": "PB",
                            "pb_chain_name": pb_atom.get("chain"),
                            "pb_auth_seq_id": pb_atom.get("auth_seq_id"),
                            "pb_label_asym_id": pb_atom.get("label_asym_id"),
                            "pb_associated_polymer_chain_name": associated_chain,
                            "pb_associated_polymer_entity_id": associated_entity,
                            "nearest_pb_distance_angstrom": round(distance, 3),
                            "local_metals": local_metals,
                            "review_only_legacy_terminal_atom": True,
                        }
                    )

        legacy_groups.append(
            {
                **group_record,
                "associated_polymer_chain_name": associated_chain,
                "associated_polymer_entity_id": associated_entity,
                "associated_polymer_distance_angstrom": associated.get("distance_angstrom")
                if associated
                else None,
                "associated_polymer_basis": associated.get("association_basis") if associated else None,
                "nearest_heteromeric_acceptor_to_pb": nearest_heteromeric_acceptor,
            }
        )

    candidate_hits.sort(key=lambda item: item["nearest_pb_distance_angstrom"])
    return {
        "atom_count_model_1": len(atoms),
        "anp_ligand_group_count": len(anp_groups),
        "active_anp_pg_group_count": sum(1 for group in anp_groups if group["has_pg"]),
        "legacy_anp_pb_no_pg_group_count": len(legacy_groups),
        "anp_ligand_groups": anp_groups,
        "legacy_anp_pb_no_pg_groups": legacy_groups,
        "legacy_pb_candidate_hits_within_6_angstrom": candidate_hits,
    }


def build_artifact(artifact_dir: Path, out: Path, sleep_seconds: float) -> dict[str, Any]:
    generated_at = now_iso()
    pdb_to_seed_files, seed_files = collect_prior_scout_ids(artifact_dir, out.name)
    anp_entries = search_anp_entries()
    candidate_pdb_ids = sorted(set(pdb_to_seed_files) & anp_entries)

    rows = []
    fetch_failures = []
    for pdb_id in candidate_pdb_ids:
        try:
            metadata = epk.compact_entry_metadata(pdb_id)
            cif_text = epk.fetch_text(epk.RCSB_CIF_URL.format(pdb_id=pdb_id), timeout=60)
            scan = scan_cif_for_legacy_anp_pb(cif_text)
            row = {
                **metadata,
                "seed_scout_files": sorted(pdb_to_seed_files[pdb_id]),
                "review_only": True,
                "countable_label_candidate": False,
                "production_claim_allowed": False,
                "labels_or_fingerprints_changed": False,
                "epk_score_computed": False,
                "ready_for_production_scoring": False,
                "ready_for_label_import": False,
                "target_family_id": TARGET_FAMILY_ID,
                "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
                **scan,
            }
            for hit in row["legacy_pb_candidate_hits_within_6_angstrom"]:
                candidate_entity_context(row, hit)
            if row["legacy_pb_candidate_hits_within_6_angstrom"]:
                row["candidate_status"] = "legacy_anp_pb_within_6_source_mapping_required_review_only"
            elif row["legacy_anp_pb_no_pg_group_count"]:
                row["candidate_status"] = "legacy_anp_pb_no_pg_without_within_6_hit_review_only"
            else:
                row["candidate_status"] = "anp_uses_pg_or_no_legacy_pb_review_only"
            rows.append(row)
        except Exception as exc:  # noqa: BLE001 - compact research failure record.
            fetch_failures.append({"pdb_id": pdb_id, "error": repr(exc)})
            rows.append(
                {
                    "pdb_id": pdb_id,
                    "seed_scout_files": sorted(pdb_to_seed_files[pdb_id]),
                    "candidate_status": "fetch_or_parse_failed_review_only",
                    "fetch_error": repr(exc),
                    "review_only": True,
                    "countable_label_candidate": False,
                    "production_claim_allowed": False,
                    "labels_or_fingerprints_changed": False,
                    "epk_score_computed": False,
                    "ready_for_production_scoring": False,
                    "ready_for_label_import": False,
                    "target_family_id": TARGET_FAMILY_ID,
                    "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
                }
            )
        if sleep_seconds:
            time.sleep(sleep_seconds)

    status_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["candidate_status"]] = status_counts.get(row["candidate_status"], 0) + 1
    legacy_rows = [row for row in rows if row.get("legacy_anp_pb_no_pg_group_count", 0) > 0]
    within_6_rows = [row for row in rows if row.get("legacy_pb_candidate_hits_within_6_angstrom")]
    artifact = {
        "metadata": {
            "lane_id": LANE_ID,
            "method": "legacy_anp_pb_terminal_atom_audit_prior_scout_artifacts",
            "generated_at": generated_at,
            "review_only": True,
            "production_claim_allowed": False,
            "labels_or_fingerprints_changed": False,
            "target_family_id": TARGET_FAMILY_ID,
            "target_fingerprint_id_if_future_gated": TARGET_FINGERPRINT_ID,
            "prior_scout_artifact_count": len(seed_files),
            "prior_scout_unique_pdb_ids": len(pdb_to_seed_files),
            "rcsb_anp_entry_count": len(anp_entries),
            "prior_scout_anp_intersection_count": len(candidate_pdb_ids),
            "fetch_failure_count": len(fetch_failures),
            "candidate_status_counts": status_counts,
            "legacy_anp_pb_no_pg_structure_count": len(legacy_rows),
            "legacy_anp_pb_within_6_structure_count": len(within_6_rows),
            "legacy_anp_pb_within_6_pdb_ids": [row["pdb_id"] for row in within_6_rows],
            "ready_for_production_scoring": False,
            "ready_for_label_import": False,
            "review_only_rule": (
                "This lane-local audit checks whether prior scout structures contain ANP "
                "ligands that lack PG but retain PB close to a heteromeric Ser/Thr/Tyr "
                "acceptor. PB proximity is a review-only rescue signal, not a production "
                "gamma-transfer measurement or label."
            ),
            "source_urls": [
                epk.RCSB_SEARCH_URL,
                "https://data.rcsb.org/rest/v1/core/entry/{pdb_id}",
                "https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb_id}/{entity_id}",
                epk.RCSB_CIF_URL,
            ],
        },
        "seed_files": seed_files,
        "fetch_failures": fetch_failures,
        "rows": rows,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    return artifact


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--sleep-seconds", type=float, default=0.02)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    artifact = build_artifact(args.artifact_dir, args.out, args.sleep_seconds)
    print(
        json.dumps(
            {
                "out": str(args.out),
                "prior_scout_unique_pdb_ids": artifact["metadata"]["prior_scout_unique_pdb_ids"],
                "prior_scout_anp_intersection_count": artifact["metadata"][
                    "prior_scout_anp_intersection_count"
                ],
                "legacy_anp_pb_no_pg_structure_count": artifact["metadata"][
                    "legacy_anp_pb_no_pg_structure_count"
                ],
                "legacy_anp_pb_within_6_structure_count": artifact["metadata"][
                    "legacy_anp_pb_within_6_structure_count"
                ],
                "legacy_anp_pb_within_6_pdb_ids": artifact["metadata"][
                    "legacy_anp_pb_within_6_pdb_ids"
                ],
                "candidate_status_counts": artifact["metadata"]["candidate_status_counts"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
