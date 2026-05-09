from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .adapters import fetch_uniprot_query
from .fingerprints import load_fingerprints


TOKEN_RE = re.compile(r"[a-z0-9]+")
HYDROLASE_MOTIF_RE = re.compile(r"[GAS][A-Z]S[A-Z]G")


def load_graph(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_mechanism_benchmark(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = {node["id"]: node for node in graph.get("nodes", [])}
    outgoing = _outgoing_edges(graph)
    records: list[dict[str, Any]] = []

    for node in graph.get("nodes", []):
        if node.get("type") != "m_csa_entry":
            continue
        entry_id = node["id"]
        residue_nodes = [
            nodes[edge["target"]]
            for edge in outgoing.get(entry_id, [])
            if edge.get("predicate") == "has_catalytic_residue" and edge["target"] in nodes
        ]
        mechanism_nodes = [
            nodes[edge["target"]]
            for edge in outgoing.get(entry_id, [])
            if edge.get("predicate") == "has_mechanism_text" and edge["target"] in nodes
        ]
        ec_targets = [
            edge["target"]
            for edge in outgoing.get(entry_id, [])
            if edge.get("predicate") == "has_ec"
        ]
        protein_targets = [
            edge["target"]
            for edge in outgoing.get(entry_id, [])
            if edge.get("predicate") == "has_reference_protein"
        ]
        role_terms = sorted(
            {
                role
                for residue in residue_nodes
                for role in residue.get("roles", [])
                if isinstance(role, str)
            }
        )
        residue_codes = sorted(
            {
                position.get("code")
                for residue in residue_nodes
                for position in residue.get("sequence_positions", [])
                if isinstance(position, dict) and position.get("code")
            }
        )
        mechanism_text = " ".join(
            node.get("text", "") for node in mechanism_nodes if isinstance(node.get("text"), str)
        )

        records.append(
            {
                "record_id": entry_id,
                "allowed_features": {
                    "enzyme_name": node.get("name"),
                    "catalytic_role_terms": role_terms,
                    "residue_codes": residue_codes,
                    "mechanism_text": mechanism_text,
                    "mechanism_text_count": len(mechanism_nodes),
                    "catalytic_residue_count": len(residue_nodes),
                    "reference_protein_count": len(protein_targets),
                },
                "blocked_leakage_fields": {
                    "ec_node_ids": ec_targets,
                    "rhea_node_ids": _rhea_targets_for_ec_nodes(outgoing, ec_targets),
                    "source_entry_id": entry_id,
                },
                "target_proxy": {
                    "task": "retrieve_seed_mechanism_fingerprint",
                    "rationale": "V2 uses seed fingerprint retrieval as a benchmark proxy before curated labels exist.",
                },
            }
        )

    return {
        "metadata": {
            "task": "mechanism_fingerprint_retrieval",
            "record_count": len(records),
            "leakage_control": "EC numbers, Rhea identifiers, and source entry ids are blocked from allowed features.",
        },
        "records": sorted(records, key=lambda item: item["record_id"]),
    }


def run_baseline_retrieval(
    benchmark: dict[str, Any],
    fingerprint_path: Path | None = None,
) -> dict[str, Any]:
    fingerprints = load_fingerprints(fingerprint_path) if fingerprint_path else load_fingerprints()
    fingerprint_terms = {
        fingerprint.id: _tokens_from_fingerprint(fingerprint.to_dict()) for fingerprint in fingerprints
    }
    results: list[dict[str, Any]] = []

    for record in benchmark.get("records", []):
        query_terms = _tokens_from_record(record)
        scored = []
        for fingerprint in fingerprints:
            terms = fingerprint_terms[fingerprint.id]
            overlap = sorted(query_terms & terms)
            score = len(overlap) / max(len(query_terms | terms), 1)
            scored.append(
                {
                    "fingerprint_id": fingerprint.id,
                    "fingerprint_name": fingerprint.name,
                    "score": round(score, 4),
                    "overlap_terms": overlap[:25],
                }
            )
        results.append(
            {
                "record_id": record["record_id"],
                "top_fingerprints": sorted(
                    scored, key=lambda item: (-item["score"], item["fingerprint_id"])
                )[:5],
                "leakage_control_checked": bool(record.get("blocked_leakage_fields")),
            }
        )

    return {
        "metadata": {
            "method": "token_overlap_baseline",
            "record_count": len(results),
            "fingerprint_count": len(fingerprints),
            "leakage_control": "baseline consumes only allowed_features from the benchmark record",
        },
        "results": results,
    }


def detect_inconsistencies(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = {node["id"]: node for node in graph.get("nodes", [])}
    outgoing = _outgoing_edges(graph)
    issues: list[dict[str, Any]] = []

    for node in graph.get("nodes", []):
        if node.get("type") != "m_csa_entry":
            continue
        entry_id = node["id"]
        ec_numbers = {
            nodes[edge["target"]].get("ec_number")
            for edge in outgoing.get(entry_id, [])
            if edge.get("predicate") == "has_ec" and edge["target"] in nodes
        }
        proteins = [
            nodes[edge["target"]]
            for edge in outgoing.get(entry_id, [])
            if edge.get("predicate") == "has_reference_protein" and edge["target"] in nodes
        ]
        for protein in proteins:
            protein_ecs = set(protein.get("ec_numbers", []))
            missing_from_uniprot = sorted(ec for ec in ec_numbers if ec and ec not in protein_ecs)
            if missing_from_uniprot:
                issues.append(
                    {
                        "issue_type": "ec_mismatch",
                        "severity": "medium",
                        "entry_id": entry_id,
                        "protein_id": protein["id"],
                        "mcsa_ec_numbers": sorted(ec for ec in ec_numbers if ec),
                        "uniprot_ec_numbers": sorted(protein_ecs),
                        "message": "M-CSA EC annotation is not fully present on the linked UniProt record.",
                    }
                )
            if not _has_outgoing_predicate(outgoing, protein["id"], "has_structure"):
                issues.append(
                    {
                        "issue_type": "missing_structure_cross_reference",
                        "severity": "low",
                        "entry_id": entry_id,
                        "protein_id": protein["id"],
                        "message": "Linked protein has no PDB or AlphaFold cross-reference in the current graph.",
                    }
                )

        for ec in sorted(ec for ec in ec_numbers if ec):
            ec_id = f"ec:{ec}"
            if not _has_outgoing_predicate(outgoing, ec_id, "maps_to_reaction"):
                issues.append(
                    {
                        "issue_type": "missing_rhea_mapping",
                        "severity": "medium",
                        "entry_id": entry_id,
                        "ec_number": ec,
                        "message": "No Rhea reaction mapping was found for this EC number in the current graph.",
                    }
                )

    return {
        "metadata": {
            "issue_count": len(issues),
            "issue_types": dict(Counter(issue["issue_type"] for issue in issues)),
        },
        "issues": sorted(issues, key=lambda item: (item["issue_type"], item.get("entry_id", ""))),
    }


def mine_dark_hydrolase_candidates(limit: int = 100) -> dict[str, Any]:
    query = "(reviewed:false) AND (protein_name:hydrolase) AND NOT (ec:*)"
    payload = fetch_uniprot_query(query=query, size=limit)
    candidates = [_score_dark_hydrolase(record) for record in payload["records"]]
    candidates = sorted(candidates, key=lambda item: (-item["score"], item["accession"]))
    return {
        "metadata": {
            "campaign": "dark_hydrolase_seed",
            "query": query,
            "record_count": len(candidates),
            "safety_scope": "computational prioritization only; not validated function or protocol",
            "source": payload["metadata"],
        },
        "candidates": candidates,
    }


def write_candidate_dossiers(candidates: dict[str, Any], out_dir: Path, top: int = 10) -> list[str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for index, candidate in enumerate(candidates.get("candidates", [])[:top], start=1):
        path = out_dir / f"{index:02d}_{candidate['accession']}.md"
        path.write_text(_candidate_dossier_markdown(candidate), encoding="utf-8")
        written.append(str(path))
    return written


def write_v2_report(
    graph_summary: dict[str, Any],
    benchmark: dict[str, Any],
    baseline: dict[str, Any],
    inconsistencies: dict[str, Any],
    candidates: dict[str, Any],
) -> str:
    top_candidates = candidates.get("candidates", [])[:10]
    lines = [
        "# Catalytic Earth V2 Research Report",
        "",
        "## Status",
        "",
        "This is a computational research artifact. Candidate enzymes are hypotheses",
        "for expert review, not validated functions.",
        "",
        "## Knowledge Graph",
        "",
        f"- Nodes: {graph_summary.get('node_count', 0)}",
        f"- Edges: {graph_summary.get('edge_count', 0)}",
        f"- Node types: {graph_summary.get('node_types', {})}",
        "",
        "## Mechanism Benchmark",
        "",
        f"- Records: {benchmark.get('metadata', {}).get('record_count', 0)}",
        f"- Leakage control: {benchmark.get('metadata', {}).get('leakage_control')}",
        "",
        "## Baseline Retrieval",
        "",
        f"- Method: {baseline.get('metadata', {}).get('method')}",
        f"- Fingerprints: {baseline.get('metadata', {}).get('fingerprint_count')}",
        "",
        "## Inconsistency Prototype",
        "",
        f"- Issues: {inconsistencies.get('metadata', {}).get('issue_count', 0)}",
        f"- Issue types: {inconsistencies.get('metadata', {}).get('issue_types', {})}",
        "",
        "## Dark Hydrolase Campaign",
        "",
        f"- Candidates scored: {candidates.get('metadata', {}).get('record_count', 0)}",
        "- Campaign scope: unreviewed UniProt hydrolase records scored for a",
        "  Ser-His-Asp/Glu hydrolase-like computational signature.",
        "",
        "## Top Candidate Accessions",
        "",
    ]
    for candidate in top_candidates:
        lines.append(
            f"- {candidate['accession']}: score {candidate['score']}, "
            f"motifs {candidate['motif_count']}, length {candidate.get('length')}"
        )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- The benchmark uses seed fingerprint retrieval, not expert-labeled mechanism classes.",
            "- Motif-based mining is a weak baseline and can produce many false positives.",
            "- AlphaFold/PDB cross-references indicate structural availability, not catalytic competence.",
            "- Wet-lab validation is required before any functional claim.",
            "",
            "## Next Work",
            "",
            "- Replace token overlap with geometry-aware active-site retrieval.",
            "- Add curated positive and negative mechanism labels.",
            "- Add substrate-pocket descriptors and environment metadata.",
            "- Expand dark-enzyme campaigns beyond generic hydrolases.",
        ]
    )
    return "\n".join(lines) + "\n"


def _score_dark_hydrolase(record: dict[str, Any]) -> dict[str, Any]:
    sequence = record.get("sequence", "")
    motifs = [
        {"motif": match.group(0), "start": match.start() + 1, "end": match.end()}
        for match in HYDROLASE_MOTIF_RE.finditer(sequence)
    ]
    name = record.get("protein_name", "")
    name_lower = name.lower()
    length = record.get("length") or 0
    score = 0
    evidence: list[str] = []
    uncertainty: list[str] = []

    if "hydrolase" in name_lower:
        score += 2
        evidence.append("protein name contains hydrolase")
    if "uncharacterized" in name_lower or "putative" in name_lower:
        score += 2
        evidence.append("protein name suggests weak characterization")
    if "alpha/beta" in name_lower or "abhydrolase" in name_lower:
        score += 2
        evidence.append("protein name suggests alpha/beta hydrolase context")
    if motifs:
        score += min(2, len(motifs))
        evidence.append("sequence contains GXSXG-like serine hydrolase motif")
    else:
        uncertainty.append("no simple GXSXG-like motif found")
    if 180 <= length <= 450:
        score += 2
        evidence.append("length is compatible with many alpha/beta hydrolase enzymes")
    else:
        score -= 1
        uncertainty.append("length is outside the preferred seed range")
    if record.get("alphafold_ids"):
        score += 1
        evidence.append("AlphaFold DB cross-reference is available")
    if record.get("pdb_ids"):
        score += 1
        evidence.append("PDB cross-reference is available")
    if record.get("ec_numbers"):
        score -= 2
        uncertainty.append("record already has EC annotation; less dark than unannotated candidates")
    else:
        score += 2
        evidence.append("no EC number in fetched UniProt fields")

    return {
        "accession": record.get("accession"),
        "entry_name": record.get("entry_name"),
        "protein_name": name,
        "organism": record.get("organism"),
        "length": length,
        "reviewed": record.get("reviewed"),
        "ec_numbers": record.get("ec_numbers", []),
        "pdb_ids": record.get("pdb_ids", []),
        "alphafold_ids": record.get("alphafold_ids", []),
        "score": score,
        "motif_count": len(motifs),
        "motifs": motifs[:10],
        "mechanistic_hypothesis": "Possible Ser-His-Asp/Glu hydrolase-like candidate if motif and fold context agree.",
        "evidence": evidence,
        "uncertainty": uncertainty,
        "safety_scope": "candidate for computational review only; no validated function is claimed",
    }


def _candidate_dossier_markdown(candidate: dict[str, Any]) -> str:
    lines = [
        f"# Candidate {candidate['accession']}",
        "",
        "## Summary",
        "",
        f"- Protein name: {candidate.get('protein_name')}",
        f"- Organism: {candidate.get('organism')}",
        f"- Length: {candidate.get('length')}",
        f"- Score: {candidate.get('score')}",
        f"- Reviewed status: {candidate.get('reviewed')}",
        "",
        "## Mechanistic Hypothesis",
        "",
        candidate.get("mechanistic_hypothesis", ""),
        "",
        "## Evidence",
        "",
    ]
    lines.extend(f"- {item}" for item in candidate.get("evidence", []))
    lines.extend(["", "## Motifs", ""])
    if candidate.get("motifs"):
        lines.extend(
            f"- {motif['motif']} at {motif['start']}-{motif['end']}"
            for motif in candidate["motifs"]
        )
    else:
        lines.append("- No simple motif match recorded.")
    lines.extend(["", "## Uncertainty", ""])
    if candidate.get("uncertainty"):
        lines.extend(f"- {item}" for item in candidate.get("uncertainty", []))
    else:
        lines.append("- No additional uncertainty flags from the simple scorer.")
    lines.extend(
        [
            "",
            "## Validation Boundary",
            "",
            "This dossier is a computational prioritization note. It is not a",
            "functional claim and does not provide a wet-lab protocol.",
            "",
        ]
    )
    return "\n".join(lines)


def _tokens_from_record(record: dict[str, Any]) -> set[str]:
    features = record.get("allowed_features", {})
    text_parts = [
        str(features.get("enzyme_name", "")),
        str(features.get("mechanism_text", "")),
        " ".join(features.get("catalytic_role_terms", [])),
        " ".join(features.get("residue_codes", [])),
    ]
    return _tokenize(" ".join(text_parts))


def _tokens_from_fingerprint(fingerprint: dict[str, Any]) -> set[str]:
    text_parts = [
        fingerprint.get("name", ""),
        " ".join(fingerprint.get("enzyme_space", [])),
        " ".join(fingerprint.get("cofactors", [])),
        fingerprint.get("reaction_center", {}).get("chemical_operation", ""),
        " ".join(fingerprint.get("reaction_center", {}).get("bond_changes", [])),
        " ".join(fingerprint.get("substrate_constraints", [])),
        " ".join(fingerprint.get("evidence_features", [])),
    ]
    for role in fingerprint.get("active_site_signature", []):
        text_parts.extend([role.get("role", ""), role.get("residue", ""), " ".join(role.get("constraints", []))])
    return _tokenize(" ".join(text_parts))


def _tokenize(text: str) -> set[str]:
    stop = {"the", "and", "or", "a", "an", "of", "to", "with", "in", "for", "by"}
    return {token for token in TOKEN_RE.findall(text.lower()) if token not in stop and len(token) > 1}


def _outgoing_edges(graph: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in graph.get("edges", []):
        outgoing[edge.get("source", "")].append(edge)
    return outgoing


def _rhea_targets_for_ec_nodes(
    outgoing: dict[str, list[dict[str, Any]]], ec_targets: list[str]
) -> list[str]:
    return sorted(
        {
            edge["target"]
            for ec_id in ec_targets
            for edge in outgoing.get(ec_id, [])
            if edge.get("predicate") == "maps_to_reaction"
        }
    )


def _has_outgoing_predicate(
    outgoing: dict[str, list[dict[str, Any]]], node_id: str, predicate: str
) -> bool:
    return any(edge.get("predicate") == predicate for edge in outgoing.get(node_id, []))
