from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from io import StringIO
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


USER_AGENT = "CatalyticEarth/0.0.1 research prototype"
RHEA_REST_URL = "https://www.rhea-db.org/rhea"
MCSA_ENTRIES_URL = "https://www.ebi.ac.uk/thornton-srv/m-csa/api/entries/"
UNIPROT_SEARCH_URL = "https://rest.uniprot.org/uniprotkb/search"
UNIPROT_ENTRY_URL = "https://rest.uniprot.org/uniprotkb"
UNIPROT_FIELDS = "accession,id,protein_name,organism_name,length,ec,xref_pdb,xref_alphafolddb"
UNIPROT_DISCOVERY_FIELDS = (
    "accession,id,protein_name,organism_name,length,sequence,ec,xref_pdb,xref_alphafolddb,reviewed"
)


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


def build_mcsa_page_url(page: int = 1, page_size: int = 100) -> str:
    if page < 1:
        raise ValueError("page must be a positive integer")
    if page_size < 1 or page_size > 100:
        raise ValueError("page_size must be between 1 and 100")
    params = {
        "format": "json",
        "page": str(page),
        "page_size": str(page_size),
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
                "reference_uniprot_ids": _split_accessions(entry.get("reference_uniprot_id")),
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


def fetch_mcsa_page(page: int = 1, page_size: int = 100) -> dict[str, Any]:
    url = build_mcsa_page_url(page=page, page_size=page_size)
    payload = _fetch_json(url)
    records = normalize_mcsa_entries(payload)
    return {
        "metadata": {
            **RetrievalMetadata("m_csa", url, len(records)).to_dict(),
            "total_available": payload.get("count"),
            "next": payload.get("next"),
            "page": page,
            "page_size": page_size,
        },
        "records": records,
    }


def fetch_mcsa_records(max_records: int = 100, page_size: int = 100) -> dict[str, Any]:
    if max_records < 1:
        raise ValueError("max_records must be positive")
    if page_size < 1 or page_size > 100:
        raise ValueError("page_size must be between 1 and 100")

    records: list[dict[str, Any]] = []
    page_metadata: list[dict[str, Any]] = []
    page = 1
    total_available = None
    while len(records) < max_records:
        payload = fetch_mcsa_page(page=page, page_size=page_size)
        page_metadata.append(payload["metadata"])
        total_available = payload["metadata"].get("total_available", total_available)
        records.extend(payload["records"])
        if not payload["metadata"].get("next") or not payload["records"]:
            break
        page += 1

    records = records[:max_records]
    return {
        "metadata": {
            "source": "m_csa",
            "url": MCSA_ENTRIES_URL,
            "record_count": len(records),
            "max_records": max_records,
            "page_size": page_size,
            "pages_fetched": len(page_metadata),
            "total_available": total_available,
            "pages": page_metadata,
        },
        "records": records,
    }


def build_uniprot_accessions_url(accessions: list[str]) -> str:
    cleaned = sorted({accession.strip() for accession in accessions if accession.strip()})
    if not cleaned:
        raise ValueError("at least one UniProt accession is required")
    query = " OR ".join(f"accession:{accession}" for accession in cleaned)
    params = {
        "query": f"({query})",
        "fields": UNIPROT_FIELDS,
        "format": "tsv",
        "size": str(len(cleaned)),
    }
    return f"{UNIPROT_SEARCH_URL}?{urlencode(params)}"


def normalize_uniprot_tsv(text: str) -> list[dict[str, Any]]:
    reader = csv.DictReader(StringIO(text), delimiter="\t")
    records: list[dict[str, Any]] = []
    for row in reader:
        if not row:
            continue
        accession = row.get("Entry", "").strip()
        if not accession:
            continue
        records.append(
            {
                "source": "uniprot",
                "accession": accession,
                "entry_name": row.get("Entry Name", "").strip(),
                "protein_name": row.get("Protein names", "").strip(),
                "organism": row.get("Organism", "").strip(),
                "length": _safe_int(row.get("Length")),
                "sequence": row.get("Sequence", "").strip(),
                "ec_numbers": _split_semicolon_field(row.get("EC number")),
                "pdb_ids": _split_semicolon_field(row.get("PDB")),
                "alphafold_ids": _split_semicolon_field(row.get("AlphaFoldDB")),
                "reviewed": row.get("Reviewed", "").strip(),
                "evidence_level": "protein_cross_reference",
            }
        )
    return records


def build_uniprot_query_url(query: str, fields: str = UNIPROT_DISCOVERY_FIELDS, size: int = 100) -> str:
    if not query.strip():
        raise ValueError("query is required")
    if size < 1 or size > 500:
        raise ValueError("size must be between 1 and 500")
    params = {
        "query": query,
        "fields": fields,
        "format": "tsv",
        "size": str(size),
    }
    return f"{UNIPROT_SEARCH_URL}?{urlencode(params)}"


def fetch_uniprot_query(query: str, size: int = 100) -> dict[str, Any]:
    url = build_uniprot_query_url(query=query, size=size)
    records = normalize_uniprot_tsv(_fetch_text(url))
    return {
        "metadata": {
            **RetrievalMetadata("uniprot", url, len(records)).to_dict(),
            "query": query,
            "size": size,
        },
        "records": records,
    }


def fetch_uniprot_accessions(accessions: list[str]) -> dict[str, Any]:
    cleaned = sorted({item for accession in accessions for item in _split_accessions(accession)})
    if not cleaned:
        return {
            "metadata": RetrievalMetadata("uniprot", UNIPROT_SEARCH_URL, 0).to_dict(),
            "records": [],
        }

    records: list[dict[str, Any]] = []
    batch_metadata: list[dict[str, Any]] = []
    for batch in _chunked(cleaned, 25):
        url = build_uniprot_accessions_url(batch)
        batch_records = normalize_uniprot_tsv(_fetch_text(url))
        records.extend(batch_records)
        batch_metadata.append(
            {
                "url": url,
                "requested_accession_count": len(batch),
                "record_count": len(batch_records),
            }
        )

    by_accession = {record["accession"]: record for record in records}
    records = [by_accession[accession] for accession in sorted(by_accession)]
    return {
        "metadata": {
            **RetrievalMetadata("uniprot", UNIPROT_SEARCH_URL, len(records)).to_dict(),
            "requested_accession_count": len(cleaned),
            "batches": batch_metadata,
        },
        "records": records,
    }


def build_uniprot_entry_url(accession: str) -> str:
    cleaned = accession.strip()
    if not cleaned:
        raise ValueError("accession is required")
    return f"{UNIPROT_ENTRY_URL}/{cleaned}.json"


def fetch_uniprot_entry(accession: str) -> dict[str, Any]:
    url = build_uniprot_entry_url(accession)
    payload = _fetch_json(url)
    record = normalize_uniprot_entry_json(payload)
    return {
        "metadata": RetrievalMetadata("uniprotkb_json", url, 1).to_dict(),
        "record": record,
    }


def normalize_uniprot_entry_json(payload: dict[str, Any]) -> dict[str, Any]:
    features = [
        _normalize_uniprot_feature(feature)
        for feature in payload.get("features", [])
        if isinstance(feature, dict)
    ]
    comments = [
        comment for comment in payload.get("comments", []) if isinstance(comment, dict)
    ]
    catalytic_activity_comments = [
        _normalize_uniprot_catalytic_activity(comment)
        for comment in comments
        if comment.get("commentType") == "CATALYTIC ACTIVITY"
    ]
    cofactor_comments = [
        _normalize_uniprot_cofactor(comment)
        for comment in comments
        if comment.get("commentType") == "COFACTOR"
    ]
    return {
        "source": "uniprot",
        "accession": payload.get("primaryAccession"),
        "entry_name": payload.get("uniProtkbId"),
        "entry_type": payload.get("entryType"),
        "annotation_score": payload.get("annotationScore"),
        "sequence_length": payload.get("sequence", {}).get("length"),
        "active_site_features": [
            feature for feature in features if feature["feature_type"] == "Active site"
        ],
        "binding_site_features": [
            feature for feature in features if feature["feature_type"] == "Binding site"
        ],
        "site_features": [
            feature for feature in features if feature["feature_type"] == "Site"
        ],
        "catalytic_activity_comments": catalytic_activity_comments,
        "cofactor_comments": cofactor_comments,
        "evidence_level": "uniprot_active_site_and_catalytic_activity_context",
    }


def _normalize_uniprot_feature(feature: dict[str, Any]) -> dict[str, Any]:
    ligand = feature.get("ligand") if isinstance(feature.get("ligand"), dict) else {}
    return {
        "feature_type": feature.get("type"),
        "begin": _feature_location_value(feature, "start"),
        "end": _feature_location_value(feature, "end"),
        "description": feature.get("description") or "",
        "ligand_name": ligand.get("name"),
        "ligand_id": ligand.get("id"),
        "ligand_note": ligand.get("note"),
        "evidence": _normalize_uniprot_evidence(feature.get("evidences")),
        "cross_references": _normalize_cross_references(
            feature.get("featureCrossReferences")
        ),
    }


def _normalize_uniprot_catalytic_activity(comment: dict[str, Any]) -> dict[str, Any]:
    reaction = comment.get("reaction") if isinstance(comment.get("reaction"), dict) else {}
    return {
        "reaction": reaction.get("name"),
        "ec_number": reaction.get("ecNumber"),
        "cross_references": _normalize_cross_references(
            reaction.get("reactionCrossReferences")
        ),
        "evidence": _normalize_uniprot_evidence(reaction.get("evidences")),
    }


def _normalize_uniprot_cofactor(comment: dict[str, Any]) -> dict[str, Any]:
    cofactors = []
    for cofactor in comment.get("cofactors", []) or []:
        if not isinstance(cofactor, dict):
            continue
        cross_reference = cofactor.get("cofactorCrossReference")
        cofactors.append(
            {
                "name": cofactor.get("name"),
                "cross_reference": (
                    {
                        "database": cross_reference.get("database"),
                        "id": cross_reference.get("id"),
                    }
                    if isinstance(cross_reference, dict)
                    else None
                ),
                "evidence": _normalize_uniprot_evidence(cofactor.get("evidences")),
            }
        )
    return {"cofactors": cofactors}


def _feature_location_value(feature: dict[str, Any], key: str) -> int | None:
    location = feature.get("location") if isinstance(feature.get("location"), dict) else {}
    endpoint = location.get(key) if isinstance(location.get(key), dict) else {}
    return _safe_int(endpoint.get("value"))


def _normalize_uniprot_evidence(evidences: Any) -> list[dict[str, str | None]]:
    normalized = []
    for evidence in evidences or []:
        if not isinstance(evidence, dict):
            continue
        normalized.append(
            {
                "evidence_code": evidence.get("evidenceCode"),
                "source": evidence.get("source"),
                "id": evidence.get("id"),
            }
        )
    return normalized


def _normalize_cross_references(references: Any) -> list[dict[str, str | None]]:
    normalized = []
    for reference in references or []:
        if not isinstance(reference, dict):
            continue
        normalized.append(
            {
                "database": reference.get("database"),
                "id": reference.get("id"),
            }
        )
    return normalized


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


def _split_semicolon_field(value: Any) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


def _split_accessions(value: Any) -> list[str]:
    if not isinstance(value, str) or not value.strip():
        return []
    return [item for item in re.split(r"[,;\s]+", value.strip()) if item]


def _chunked(items: list[str], size: int) -> list[list[str]]:
    return [items[index : index + size] for index in range(0, len(items), size)]
