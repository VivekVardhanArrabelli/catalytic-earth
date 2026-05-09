from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .models import MechanismFingerprint, RegistryError
from .sources import PROJECT_ROOT


FINGERPRINT_REGISTRY = PROJECT_ROOT / "data" / "registries" / "mechanism_fingerprints.json"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_fingerprints(path: Path = FINGERPRINT_REGISTRY) -> list[MechanismFingerprint]:
    data = read_json(path)
    if not isinstance(data, list):
        raise RegistryError("mechanism fingerprint registry must be a list")

    records = [MechanismFingerprint.from_dict(item, index) for index, item in enumerate(data)]
    ids = [record.id for record in records]
    duplicates = sorted(item for item, count in Counter(ids).items() if count > 1)
    if duplicates:
        raise RegistryError(f"duplicate fingerprint ids: {', '.join(duplicates)}")
    return records


def completeness_score(fingerprint: MechanismFingerprint) -> float:
    expected_groups = [
        fingerprint.enzyme_space,
        fingerprint.active_site_signature,
        fingerprint.reaction_center.bond_changes,
        [fingerprint.reaction_center.chemical_operation],
        fingerprint.substrate_constraints,
        fingerprint.evidence_features,
        fingerprint.counterevidence_features,
        fingerprint.uncertainty_axes,
        fingerprint.seed_examples,
    ]
    present = sum(1 for group in expected_groups if group)
    return round(present / len(expected_groups), 3)


def build_mechanism_demo(records: list[MechanismFingerprint]) -> dict[str, Any]:
    cofactor_index: dict[str, list[str]] = defaultdict(list)
    operation_index: dict[str, list[str]] = defaultdict(list)
    residue_role_index: dict[str, list[str]] = defaultdict(list)

    for record in records:
        cofactors = record.cofactors or ["no_explicit_cofactor"]
        for cofactor in cofactors:
            cofactor_index[cofactor].append(record.id)
        operation_index[record.reaction_center.chemical_operation].append(record.id)
        for active_site_role in record.active_site_signature:
            residue_role_index[active_site_role.role].append(record.id)

    return {
        "fingerprint_count": len(records),
        "mean_completeness": round(
            sum(completeness_score(record) for record in records) / max(len(records), 1), 3
        ),
        "cofactor_index": {
            key: sorted(value) for key, value in sorted(cofactor_index.items())
        },
        "chemical_operation_index": {
            key: sorted(value) for key, value in sorted(operation_index.items())
        },
        "active_site_role_index": {
            key: sorted(value) for key, value in sorted(residue_role_index.items())
        },
        "fingerprints": [
            {
                "id": record.id,
                "name": record.name,
                "chemical_operation": record.reaction_center.chemical_operation,
                "bond_changes": record.reaction_center.bond_changes,
                "active_site_roles": [
                    {
                        "role": role.role,
                        "residue": role.residue,
                    }
                    for role in record.active_site_signature
                ],
                "cofactors": record.cofactors,
                "completeness": completeness_score(record),
            }
            for record in sorted(records, key=lambda item: item.id)
        ],
    }
