from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .fingerprints import load_fingerprints
from .models import RegistryError
from .sources import PROJECT_ROOT


ONTOLOGY_REGISTRY = PROJECT_ROOT / "data" / "registries" / "mechanism_ontology.json"


def load_mechanism_ontology(path: Path = ONTOLOGY_REGISTRY) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        ontology = json.load(handle)
    if not isinstance(ontology, dict):
        raise RegistryError("mechanism ontology must be an object")
    families = ontology.get("families")
    if not isinstance(families, list) or not families:
        raise RegistryError("mechanism ontology must define non-empty families")
    root = ontology.get("root")
    if not isinstance(root, dict) or not isinstance(root.get("id"), str):
        raise RegistryError("mechanism ontology must define root.id")
    root_id = root["id"]

    known_fingerprints = {fingerprint.id for fingerprint in load_fingerprints()}
    seen_family_ids: set[str] = set()
    mapped_fingerprints: set[str] = set()
    for index, family in enumerate(families):
        if not isinstance(family, dict):
            raise RegistryError(f"ontology family[{index}] must be an object")
        family_id = family.get("id")
        if not isinstance(family_id, str) or not family_id:
            raise RegistryError(f"ontology family[{index}].id must be a non-empty string")
        if family_id in seen_family_ids:
            raise RegistryError(f"duplicate ontology family id: {family_id}")
        seen_family_ids.add(family_id)
        parent_id = family.get("parent_id")
        if not isinstance(parent_id, str) or not parent_id:
            raise RegistryError(f"ontology family {family_id} parent_id must be a string")
        fingerprint_ids = family.get("fingerprint_ids", [])
        if not isinstance(fingerprint_ids, list):
            raise RegistryError(f"ontology family {family_id} fingerprint_ids must be a list")
        for fingerprint_id in fingerprint_ids:
            if fingerprint_id not in known_fingerprints:
                raise RegistryError(
                    f"ontology family {family_id} references unknown fingerprint {fingerprint_id}"
                )
            mapped_fingerprints.add(fingerprint_id)

    missing = sorted(known_fingerprints - mapped_fingerprints)
    if missing:
        raise RegistryError(f"mechanism ontology missing fingerprints: {', '.join(missing)}")
    known_family_or_root_ids = seen_family_ids | {root_id}
    unknown_parents = sorted(
        str(family.get("parent_id"))
        for family in families
        if isinstance(family, dict) and family.get("parent_id") not in known_family_or_root_ids
    )
    if unknown_parents:
        raise RegistryError(f"mechanism ontology references unknown parents: {', '.join(unknown_parents)}")
    return ontology


def mechanism_family_index(ontology: dict[str, Any] | None = None) -> dict[str, str]:
    if ontology is None:
        ontology = load_mechanism_ontology()
    index: dict[str, str] = {}
    for family in ontology.get("families", []):
        if not isinstance(family, dict):
            continue
        family_id = str(family.get("id"))
        for fingerprint_id in family.get("fingerprint_ids", []):
            if isinstance(fingerprint_id, str):
                index[fingerprint_id] = family_id
    return index


def fingerprint_family(fingerprint_id: str | None, ontology: dict[str, Any] | None = None) -> str | None:
    if not fingerprint_id:
        return None
    return mechanism_family_index(ontology).get(fingerprint_id)
