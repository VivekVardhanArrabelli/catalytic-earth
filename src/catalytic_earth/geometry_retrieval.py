from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any

from .fingerprints import load_fingerprints


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def run_geometry_retrieval(
    geometry: dict[str, Any],
    top_k: int = 5,
) -> dict[str, Any]:
    fingerprints = load_fingerprints()
    results: list[dict[str, Any]] = []
    for entry in geometry.get("entries", []):
        scored = [
            score_entry_against_fingerprint(entry, fingerprint.to_dict())
            for fingerprint in fingerprints
        ]
        results.append(
            {
                "entry_id": entry.get("entry_id"),
                "pdb_id": entry.get("pdb_id"),
                "status": entry.get("status"),
                "resolved_residue_count": entry.get("resolved_residue_count", 0),
                "top_fingerprints": sorted(
                    scored, key=lambda item: (-item["score"], item["fingerprint_id"])
                )[:top_k],
            }
        )

    return {
        "metadata": {
            "method": "geometry_aware_seed_fingerprint_retrieval",
            "entry_count": len(results),
            "fingerprint_count": len(fingerprints),
            "scoring": "residue signature match plus catalytic-cluster compactness",
            "validation_boundary": "retrieval evidence only; not mechanism validation",
        },
        "results": results,
    }


def score_entry_against_fingerprint(
    entry: dict[str, Any],
    fingerprint: dict[str, Any],
) -> dict[str, Any]:
    residues = entry.get("residues", [])
    distances = entry.get("pairwise_distances_angstrom", [])
    signature = fingerprint.get("active_site_signature", [])
    residue_codes = [_canonical_code(residue.get("code")) for residue in residues]
    residue_roles = {
        role.lower()
        for residue in residues
        for role in residue.get("roles", [])
        if isinstance(role, str)
    }

    matched_signature_roles: list[dict[str, Any]] = []
    for requirement in signature:
        allowed = _allowed_residue_codes(requirement.get("residue", ""))
        role = str(requirement.get("role", "")).lower()
        matched_codes = sorted(code for code in residue_codes if code in allowed)
        role_hint_match = any(part in " ".join(residue_roles) for part in role.split("_") if part)
        if matched_codes or role_hint_match:
            matched_signature_roles.append(
                {
                    "required_role": requirement.get("role"),
                    "required_residue": requirement.get("residue"),
                    "matched_codes": matched_codes,
                    "role_hint_match": role_hint_match,
                }
            )

    residue_match_fraction = len(matched_signature_roles) / max(len(signature), 1)
    compactness = compactness_score(distances)
    score = round(0.72 * residue_match_fraction + 0.28 * compactness, 4)
    return {
        "fingerprint_id": fingerprint.get("id"),
        "fingerprint_name": fingerprint.get("name"),
        "score": score,
        "residue_match_fraction": round(residue_match_fraction, 4),
        "compactness_score": round(compactness, 4),
        "matched_signature_roles": matched_signature_roles,
        "distance_summary": distance_summary(distances),
    }


def compactness_score(distances: list[dict[str, Any]]) -> float:
    values = [
        float(item["distance"])
        for item in distances
        if isinstance(item, dict) and item.get("distance") is not None
    ]
    if not values:
        return 0.0
    median = statistics.median(values)
    if median <= 8:
        return 1.0
    if median >= 24:
        return 0.0
    return max(0.0, 1 - ((median - 8) / 16))


def distance_summary(distances: list[dict[str, Any]]) -> dict[str, Any]:
    values = [
        float(item["distance"])
        for item in distances
        if isinstance(item, dict) and item.get("distance") is not None
    ]
    if not values:
        return {"count": 0}
    return {
        "count": len(values),
        "min": round(min(values), 3),
        "median": round(statistics.median(values), 3),
        "max": round(max(values), 3),
    }


def write_geometry_retrieval(
    geometry_path: Path,
    out_path: Path,
    top_k: int = 5,
) -> dict[str, Any]:
    artifact = run_geometry_retrieval(load_json(geometry_path), top_k=top_k)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return artifact


def _allowed_residue_codes(spec: str) -> set[str]:
    allowed = {_canonical_code(part) for part in spec.replace(",", "/").split("/")}
    return {item for item in allowed if item}


def _canonical_code(code: Any) -> str:
    if not isinstance(code, str):
        return ""
    cleaned = code.strip().upper()
    aliases = {
        "SER": "SER",
        "S": "SER",
        "HIS": "HIS",
        "H": "HIS",
        "ASP": "ASP",
        "D": "ASP",
        "GLU": "GLU",
        "E": "GLU",
        "CYS": "CYS",
        "C": "CYS",
        "TYR": "TYR",
        "Y": "TYR",
        "LYS": "LYS",
        "K": "LYS",
        "ARG": "ARG",
        "R": "ARG",
        "THR": "THR",
        "T": "THR",
    }
    return aliases.get(cleaned, cleaned if len(cleaned) == 3 else "")
