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
            "scoring": "residue and role overlap plus ligand/cofactor context, substrate-pocket descriptors, and compactness",
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
        _normalize_phrase(role)
        for residue in residues
        for role in residue.get("roles", [])
        if isinstance(role, str)
    }

    matched_signature_roles: list[dict[str, Any]] = []
    for requirement in signature:
        allowed = _allowed_residue_codes(requirement.get("residue", ""))
        role = _normalize_phrase(str(requirement.get("role", "")))
        matched_codes = sorted(code for code in residue_codes if code in allowed)
        role_hint_match = _role_hint_match(role, residue_roles)
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
    role_match_fraction = _role_match_fraction(signature, residue_roles)
    cofactor_context = cofactor_context_score(
        fingerprint,
        residue_codes,
        residue_roles,
        entry.get("ligand_context"),
    )
    compactness = compactness_score(distances)
    substrate_pocket = substrate_pocket_score(fingerprint, entry.get("pocket_context"))
    score = round(
        0.35 * residue_match_fraction
        + 0.24 * role_match_fraction
        + 0.18 * cofactor_context
        + 0.08 * compactness
        + 0.15 * substrate_pocket,
        4,
    )
    return {
        "fingerprint_id": fingerprint.get("id"),
        "fingerprint_name": fingerprint.get("name"),
        "score": score,
        "residue_match_fraction": round(residue_match_fraction, 4),
        "role_match_fraction": round(role_match_fraction, 4),
        "cofactor_context_score": round(cofactor_context, 4),
        "compactness_score": round(compactness, 4),
        "substrate_pocket_score": round(substrate_pocket, 4),
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


def cofactor_context_score(
    fingerprint: dict[str, Any],
    residue_codes: list[str],
    residue_roles: set[str],
    ligand_context: dict[str, Any] | None = None,
) -> float:
    cofactors = {_normalize_phrase(cofactor) for cofactor in fingerprint.get("cofactors", [])}
    fingerprint_id = fingerprint.get("id")
    observed_families = _observed_cofactor_families(ligand_context, residue_roles)
    role_text = " ".join(residue_roles)
    residue_code_set = set(residue_codes)
    cys_count = sum(1 for code in residue_codes if code == "CYS")

    if not cofactors:
        if fingerprint_id == "ser_his_acid_hydrolase":
            expected = {"SER", "HIS"}
            acid = bool({"ASP", "GLU"} & residue_code_set)
            return 1.0 if expected.issubset(set(residue_codes)) and acid else 0.25
        return 0.5

    requirement_scores: list[float] = []
    for cofactor in sorted(cofactors):
        if _is_metal_cofactor(cofactor):
            if "metal_ion" in observed_families:
                requirement_scores.append(1.0)
            elif "metal ligand" in role_text:
                requirement_scores.append(0.4)
            elif {"HIS", "ASP", "GLU", "CYS"} & residue_code_set:
                requirement_scores.append(0.2)
            else:
                requirement_scores.append(0.0)
            continue

        if "heme" in cofactor:
            if "heme" in observed_families:
                requirement_scores.append(1.0)
            elif "heme" in role_text:
                requirement_scores.append(0.25)
            else:
                requirement_scores.append(0.0)
            continue

        if "pyridoxal phosphate" in cofactor:
            if "plp" in observed_families:
                requirement_scores.append(1.0)
            elif "LYS" in residue_code_set:
                requirement_scores.append(0.3)
            else:
                requirement_scores.append(0.0)
            continue

        if cofactor in {"fad", "fmn"}:
            if "flavin" in observed_families:
                requirement_scores.append(1.0)
            elif any(term in role_text for term in ["flavin", "redox"]):
                requirement_scores.append(0.25)
            else:
                requirement_scores.append(0.0)
            continue

        if cofactor in {"nadph", "nadp", "nad", "nadh"}:
            if "nad" in observed_families:
                requirement_scores.append(1.0)
            elif any(term in role_text for term in ["nadph", "redox"]):
                requirement_scores.append(0.2)
            else:
                requirement_scores.append(0.0)
            continue

        if "sam" in cofactor or "adenosylmethionine" in cofactor:
            if "sam" in observed_families:
                requirement_scores.append(1.0)
            elif cys_count >= 3:
                requirement_scores.append(0.2)
            else:
                requirement_scores.append(0.0)
            continue

        if "4fe-4s" in cofactor:
            if "fe_s_cluster" in observed_families:
                requirement_scores.append(1.0)
            elif cys_count >= 3:
                requirement_scores.append(0.2)
            else:
                requirement_scores.append(0.0)
            continue

        requirement_scores.append(0.0)

    return sum(requirement_scores) / len(requirement_scores) if requirement_scores else 0.0


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


def substrate_pocket_score(
    fingerprint: dict[str, Any],
    pocket_context: dict[str, Any] | None = None,
) -> float:
    if not isinstance(pocket_context, dict):
        return 0.5
    if int(pocket_context.get("nearby_residue_count", 0)) < 1:
        return 0.5
    descriptors = pocket_context.get("descriptors", {})
    if not isinstance(descriptors, dict):
        return 0.5

    hydrophobic = float(descriptors.get("hydrophobic_fraction", 0.0))
    polar = float(descriptors.get("polar_fraction", 0.0))
    positive = float(descriptors.get("positive_fraction", 0.0))
    negative = float(descriptors.get("negative_fraction", 0.0))
    aromatic = float(descriptors.get("aromatic_fraction", 0.0))
    sulfur = float(descriptors.get("sulfur_fraction", 0.0))
    charge_balance = float(descriptors.get("charge_balance", 0.0))

    fingerprint_id = str(fingerprint.get("id", ""))
    if fingerprint_id == "ser_his_acid_hydrolase":
        hydrophobic_match = 1.0 - min(1.0, abs(hydrophobic - 0.45) / 0.45)
        charge_match = 1.0 - min(1.0, abs(charge_balance) / 0.4)
        return _clamp(0.6 * hydrophobic_match + 0.4 * charge_match)

    if fingerprint_id == "metal_dependent_hydrolase":
        return _clamp(0.55 * polar + 0.35 * negative + 0.10 * positive)

    if fingerprint_id == "plp_dependent_enzyme":
        return _clamp(0.50 * polar + 0.30 * positive + 0.20 * hydrophobic)

    if fingerprint_id == "radical_sam_enzyme":
        return _clamp(0.65 * sulfur + 0.20 * hydrophobic + 0.15 * aromatic)

    if fingerprint_id == "flavin_monooxygenase":
        hydrophobic_match = 1.0 - min(1.0, abs(hydrophobic - 0.4) / 0.4)
        return _clamp(0.45 * hydrophobic_match + 0.35 * aromatic + 0.20 * polar)

    if fingerprint_id == "heme_peroxidase_oxidase":
        return _clamp(0.45 * aromatic + 0.35 * hydrophobic + 0.20 * polar)

    return 0.5


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


def _normalize_phrase(value: str) -> str:
    return value.lower().replace("_", " ").replace("-", " ").strip()


def _role_hint_match(required_role: str, residue_roles: set[str]) -> bool:
    if required_role in residue_roles:
        return True
    if required_role == "acid base":
        return any("proton acceptor" in role or "proton donor" in role for role in residue_roles)
    if required_role == "acid or orienter":
        return any("proton" in role or "hydrogen bond" in role for role in residue_roles)
    return False


def _role_match_fraction(signature: list[dict[str, Any]], residue_roles: set[str]) -> float:
    if not signature:
        return 0.0
    matched = 0
    for requirement in signature:
        if _role_hint_match(_normalize_phrase(str(requirement.get("role", ""))), residue_roles):
            matched += 1
    return matched / len(signature)


def _is_metal_cofactor(cofactor: str) -> bool:
    metals = {"zn2+", "mg2+", "mn2+", "fe2+/fe3+", "fe2+", "fe3+", "metal"}
    return cofactor in metals or any(metal in cofactor for metal in metals)


def _observed_cofactor_families(
    ligand_context: dict[str, Any] | None,
    residue_roles: set[str],
) -> set[str]:
    families: set[str] = set()
    if isinstance(ligand_context, dict):
        for value in ligand_context.get("cofactor_families", []):
            normalized = _normalize_phrase(str(value))
            if normalized:
                families.add(normalized)
    role_text = " ".join(residue_roles)
    if "heme" in role_text:
        families.add("heme")
    if "flavin" in role_text:
        families.add("flavin")
    if "nadph" in role_text or "nadp" in role_text or "nad" in role_text:
        families.add("nad")
    if "metal ligand" in role_text:
        families.add("metal_ion")
    return families


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))
