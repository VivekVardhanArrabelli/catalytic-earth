from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class RegistryError(ValueError):
    """Raised when a registry record is malformed."""


def _require_mapping(data: Any, context: str) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise RegistryError(f"{context} must be an object")
    return data


def _require_str(data: dict[str, Any], key: str, context: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RegistryError(f"{context}.{key} must be a non-empty string")
    return value


def _require_str_list(data: dict[str, Any], key: str, context: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise RegistryError(f"{context}.{key} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise RegistryError(f"{context}.{key} must contain only non-empty strings")
    return value


@dataclass(frozen=True)
class SourceRecord:
    id: str
    name: str
    category: str
    url: str
    access: str
    license: str
    roles: list[str]
    primary_fields: list[str]
    caveats: list[str]
    priority: int

    @classmethod
    def from_dict(cls, data: Any, index: int) -> "SourceRecord":
        record = _require_mapping(data, f"source[{index}]")
        priority = record.get("priority")
        if not isinstance(priority, int) or priority < 1:
            raise RegistryError(f"source[{index}].priority must be a positive integer")

        return cls(
            id=_require_str(record, "id", f"source[{index}]"),
            name=_require_str(record, "name", f"source[{index}]"),
            category=_require_str(record, "category", f"source[{index}]"),
            url=_require_str(record, "url", f"source[{index}]"),
            access=_require_str(record, "access", f"source[{index}]"),
            license=_require_str(record, "license", f"source[{index}]"),
            roles=_require_str_list(record, "roles", f"source[{index}]"),
            primary_fields=_require_str_list(record, "primary_fields", f"source[{index}]"),
            caveats=_require_str_list(record, "caveats", f"source[{index}]"),
            priority=priority,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "url": self.url,
            "access": self.access,
            "license": self.license,
            "roles": self.roles,
            "primary_fields": self.primary_fields,
            "caveats": self.caveats,
            "priority": self.priority,
        }


@dataclass(frozen=True)
class ActiveSiteRole:
    role: str
    residue: str
    constraints: list[str]

    @classmethod
    def from_dict(cls, data: Any, context: str) -> "ActiveSiteRole":
        record = _require_mapping(data, context)
        return cls(
            role=_require_str(record, "role", context),
            residue=_require_str(record, "residue", context),
            constraints=_require_str_list(record, "constraints", context),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "residue": self.residue,
            "constraints": self.constraints,
        }


@dataclass(frozen=True)
class ReactionCenter:
    bond_changes: list[str]
    chemical_operation: str

    @classmethod
    def from_dict(cls, data: Any, context: str) -> "ReactionCenter":
        record = _require_mapping(data, context)
        return cls(
            bond_changes=_require_str_list(record, "bond_changes", context),
            chemical_operation=_require_str(record, "chemical_operation", context),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "bond_changes": self.bond_changes,
            "chemical_operation": self.chemical_operation,
        }


@dataclass(frozen=True)
class MechanismFingerprint:
    id: str
    name: str
    enzyme_space: list[str]
    active_site_signature: list[ActiveSiteRole]
    cofactors: list[str]
    reaction_center: ReactionCenter
    substrate_constraints: list[str]
    evidence_features: list[str]
    counterevidence_features: list[str]
    uncertainty_axes: list[str]
    seed_examples: list[str]

    @classmethod
    def from_dict(cls, data: Any, index: int) -> "MechanismFingerprint":
        record = _require_mapping(data, f"fingerprint[{index}]")
        active_site = record.get("active_site_signature")
        if not isinstance(active_site, list) or not active_site:
            raise RegistryError(
                f"fingerprint[{index}].active_site_signature must be a non-empty list"
            )

        cofactors = record.get("cofactors", [])
        if not isinstance(cofactors, list) or not all(isinstance(item, str) for item in cofactors):
            raise RegistryError(f"fingerprint[{index}].cofactors must be a list of strings")

        return cls(
            id=_require_str(record, "id", f"fingerprint[{index}]"),
            name=_require_str(record, "name", f"fingerprint[{index}]"),
            enzyme_space=_require_str_list(record, "enzyme_space", f"fingerprint[{index}]"),
            active_site_signature=[
                ActiveSiteRole.from_dict(item, f"fingerprint[{index}].active_site_signature[{i}]")
                for i, item in enumerate(active_site)
            ],
            cofactors=cofactors,
            reaction_center=ReactionCenter.from_dict(
                record.get("reaction_center"), f"fingerprint[{index}].reaction_center"
            ),
            substrate_constraints=_require_str_list(
                record, "substrate_constraints", f"fingerprint[{index}]"
            ),
            evidence_features=_require_str_list(record, "evidence_features", f"fingerprint[{index}]"),
            counterevidence_features=_require_str_list(
                record, "counterevidence_features", f"fingerprint[{index}]"
            ),
            uncertainty_axes=_require_str_list(record, "uncertainty_axes", f"fingerprint[{index}]"),
            seed_examples=_require_str_list(record, "seed_examples", f"fingerprint[{index}]"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "enzyme_space": self.enzyme_space,
            "active_site_signature": [role.to_dict() for role in self.active_site_signature],
            "cofactors": self.cofactors,
            "reaction_center": self.reaction_center.to_dict(),
            "substrate_constraints": self.substrate_constraints,
            "evidence_features": self.evidence_features,
            "counterevidence_features": self.counterevidence_features,
            "uncertainty_axes": self.uncertainty_axes,
            "seed_examples": self.seed_examples,
        }
