from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from io import StringIO
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


USER_AGENT = "CatalyticEarth/0.0.1 research prototype"
RHEA_REST_URL = "https://www.rhea-db.org/rhea"
MCSA_ENTRIES_URL = "https://www.ebi.ac.uk/thornton-srv/m-csa/api/entries/"


@dataclass(frozen=True)
class RetrievalMetadata:
    source: str
    url: str
    record_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "url": self.url,
            "record_count": self.record_count,
        }


def _fetch_text(url: str, timeout: int = 30) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def _fetch_json(url: str, timeout: int = 30) -> Any:
    return json.loads(_fetch_text(url, timeout=timeout))


def build_rhea_sample_url(limit: int) -> str:
    query = urlencode(
        {
            "query": "",
            "columns": "rhea-id,equation,uniprot",
            "format": "tsv",
            "limit": str(limit),
        }
    )
    return f"{RHEA_REST_URL}?{query}"


def build_rhea_ec_url(ec_number: str, limit: int = 100) -> str:
    query = urlencode(
        {
            "query": f"ec:{ec_number}",
            "columns": "rhea-id,equation,ec",
            "format": "tsv",
            "limit": str(limit),
        }
    )
    return f"{RHEA_REST_URL}?{query}"


def normalize_rhea_tsv(text: str) -> list[dict[str, Any]]:
    reader = csv.DictReader(StringIO(text), delimiter="\t")
    records: list[dict[str, Any]] = []
    for row in reader:
        if not row:
            continue
        records.append(
            {
                "source": "rhea",
                "rhea_id": row.get("Reaction identifier", "").strip(),
                "equation": row.get("Equation", "").strip(),
                "ec_number": _strip_ec_prefix(row.get("EC number")),
                "mapped_enzyme_count": _safe_int(row.get("Enzymes")),
                "evidence_level": "reaction_record",
            }
        )
    return records


def fetch_rhea_sample(limit: int = 25) -> dict[str, Any]:
    if limit < 1 or limit > 500:
        raise ValueError("limit must be between 1 and 500")
    url = build_rhea_sample_url(limit)
    records = normalize_rhea_tsv(_fetch_text(url))
    return {
        "metadata": RetrievalMetadata("rhea", url, len(records)).to_dict(),
        "records": records,
    }


def fetch_rhea_by_ec(ec_number: str, limit: int = 100) -> dict[str, Any]:
    if not ec_number or not ec_number.strip():
        raise ValueError("ec_number is required")
    if limit < 1 or limit > 500:
        raise ValueError("limit must be between 1 and 500")
    url = build_rhea_ec_url(ec_number.strip(), limit=limit)
    records = normalize_rhea_tsv(_fetch_text(url))
    return {
        "metadata": RetrievalMetadata("rhea", url, len(records)).to_dict(),
        "records": records,
    }


def build_mcsa_entries_url(ids: list[int]) -> str:
    if not ids:
        raise ValueError("at least one M-CSA id is required")
    params = {
        "format": "json",
        "entries.mcsa_ids": ",".join(str(item) for item in ids),
    }
    return f"{MCSA_ENTRIES_URL}?{urlencode(params)}"


def normalize_mcsa_entries(payload: dict[str, Any]) -> list[dict[str, Any]]:
    results = payload.get("results", [])
    if not isinstance(results, list):
        raise ValueError("M-CSA payload does not contain a results list")

    records: list[dict[str, Any]] = []
    for entry in results:
        if not isinstance(entry, dict):
            continue
        reaction = entry.get("reaction") if isinstance(entry.get("reaction"), dict) else {}
        mechanisms = reaction.get("mechanisms") if isinstance(reaction.get("mechanisms"), list) else []
        compounds = reaction.get("compounds") if isinstance(reaction.get("compounds"), list) else []
        residues = entry.get("residues") if isinstance(entry.get("residues"), list) else []

        records.append(
            {
                "source": "m_csa",
                "mcsa_id": entry.get("mcsa_id"),
                "enzyme_name": entry.get("enzyme_name"),
                "reference_uniprot_id": entry.get("reference_uniprot_id"),
                "ec_numbers": entry.get("all_ecs", []),
                "reaction_ec": reaction.get("ec"),
                "compound_count": len(compounds),
                "mechanism_count": len(mechanisms),
                "residue_count": len(residues),
                "catalytic_residues": [_normalize_mcsa_residue(item) for item in residues[:20]],
                "mechanism_summaries": [
                    {
                        "mechanism_id": mechanism.get("mechanism_id"),
                        "is_detailed": mechanism.get("is_detailed"),
                        "text": mechanism.get("mechanism_text"),
                    }
                    for mechanism in mechanisms[:5]
                    if isinstance(mechanism, dict)
                ],
                "evidence_level": "curated_active_site_and_mechanism",
            }
        )
    return records


def fetch_mcsa_sample(ids: list[int]) -> dict[str, Any]:
    url = build_mcsa_entries_url(ids)
    payload = _fetch_json(url)
    records = normalize_mcsa_entries(payload)
    return {
        "metadata": RetrievalMetadata("m_csa", url, len(records)).to_dict(),
        "records": records,
    }


def _normalize_mcsa_residue(residue: Any) -> dict[str, Any]:
    if not isinstance(residue, dict):
        return {}
    roles = residue.get("roles") if isinstance(residue.get("roles"), list) else []
    residue_sequences = (
        residue.get("residue_sequences")
        if isinstance(residue.get("residue_sequences"), list)
        else []
    )
    residue_chains = residue.get("residue_chains") if isinstance(residue.get("residue_chains"), list) else []

    return {
        "roles_summary": residue.get("roles_summary"),
        "main_annotation": residue.get("main_annotation"),
        "function_location_abv": residue.get("function_location_abv"),
        "roles": [
            {
                "function_type": role.get("function_type"),
                "function": role.get("function"),
                "group_function": role.get("group_function"),
                "emo": role.get("emo"),
            }
            for role in roles
            if isinstance(role, dict)
        ],
        "sequence_positions": [
            {
                "uniprot_id": item.get("uniprot_id"),
                "code": item.get("code"),
                "resid": item.get("resid"),
                "is_reference": item.get("is_reference"),
            }
            for item in residue_sequences
            if isinstance(item, dict)
        ],
        "structure_positions": [
            {
                "pdb_id": item.get("pdb_id"),
                "chain_name": item.get("chain_name"),
                "code": item.get("code"),
                "resid": item.get("resid"),
                "is_reference": item.get("is_reference"),
            }
            for item in residue_chains
            if isinstance(item, dict)
        ],
    }


def _safe_int(value: Any) -> int | None:
    try:
        if value is None or value == "":
            return None
        return int(value)
    except (TypeError, ValueError):
        return None


def _strip_ec_prefix(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return value.replace("EC:", "", 1).strip()
