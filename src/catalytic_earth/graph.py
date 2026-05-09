from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any

from .adapters import fetch_mcsa_records, fetch_mcsa_sample, fetch_rhea_by_ec, fetch_uniprot_accessions


GRAPH_SCHEMA_VERSION = "0.1.0"


def provenance(source: str, evidence_level: str, source_id: str | None = None) -> list[dict[str, Any]]:
    return [
        {
            "source": source,
            "source_id": source_id,
            "evidence_level": evidence_level,
        }
    ]


class GraphAccumulator:
    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: dict[tuple[str, str, str], dict[str, Any]] = {}

    def add_node(self, node_id: str, node_type: str, **attrs: Any) -> None:
        payload = {"id": node_id, "type": node_type, **attrs}
        if node_id not in self.nodes:
            self.nodes[node_id] = payload
            return

        existing = self.nodes[node_id]
        for key, value in payload.items():
            if value is None:
                continue
            if key == "provenance":
                existing[key] = _merge_provenance(existing.get(key, []), value)
            elif key not in existing or existing[key] in (None, [], ""):
                existing[key] = value

    def add_edge(self, source: str, target: str, predicate: str, **attrs: Any) -> None:
        key = (source, predicate, target)
        payload = {"source": source, "target": target, "predicate": predicate, **attrs}
        if key not in self.edges:
            self.edges[key] = payload
            return

        existing = self.edges[key]
        for attr_key, value in payload.items():
            if value is None:
                continue
            if attr_key == "provenance":
                existing[attr_key] = _merge_provenance(existing.get(attr_key, []), value)
            elif attr_key not in existing or existing[attr_key] in (None, [], ""):
                existing[attr_key] = value

    def to_graph(self, metadata: dict[str, Any]) -> dict[str, Any]:
        nodes = sorted(self.nodes.values(), key=lambda item: item["id"])
        edges = sorted(
            self.edges.values(),
            key=lambda item: (item["source"], item["predicate"], item["target"]),
        )
        return {
            "metadata": {
                "schema_version": GRAPH_SCHEMA_VERSION,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "node_count": len(nodes),
                "edge_count": len(edges),
                **metadata,
            },
            "nodes": nodes,
            "edges": edges,
            "summary": summarize_graph({"nodes": nodes, "edges": edges}),
        }


def assemble_knowledge_graph(
    mcsa_records: list[dict[str, Any]],
    rhea_by_ec: dict[str, dict[str, Any]],
    uniprot_records: list[dict[str, Any]],
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    graph = GraphAccumulator()
    uniprot_by_accession = {
        record["accession"]: record
        for record in uniprot_records
        if isinstance(record.get("accession"), str)
    }

    for protein in uniprot_by_accession.values():
        protein_id = f"uniprot:{protein['accession']}"
        graph.add_node(
            protein_id,
            "protein",
            accession=protein["accession"],
            entry_name=protein.get("entry_name"),
            protein_name=protein.get("protein_name"),
            organism=protein.get("organism"),
            length=protein.get("length"),
            ec_numbers=protein.get("ec_numbers", []),
            provenance=provenance("uniprot", "protein_cross_reference", protein["accession"]),
        )
        for pdb_id in protein.get("pdb_ids", []):
            structure_id = f"pdb:{pdb_id}"
            graph.add_node(
                structure_id,
                "structure",
                structure_source="pdb",
                structure_id=pdb_id,
                provenance=provenance("uniprot", "structure_cross_reference", protein["accession"]),
            )
            graph.add_edge(
                protein_id,
                structure_id,
                "has_structure",
                provenance=provenance("uniprot", "structure_cross_reference", protein["accession"]),
            )
        for alphafold_id in protein.get("alphafold_ids", []):
            structure_id = f"alphafold:{alphafold_id}"
            graph.add_node(
                structure_id,
                "structure",
                structure_source="alphafold_db",
                structure_id=alphafold_id,
                provenance=provenance("uniprot", "structure_cross_reference", protein["accession"]),
            )
            graph.add_edge(
                protein_id,
                structure_id,
                "has_structure",
                provenance=provenance("uniprot", "structure_cross_reference", protein["accession"]),
            )

    for entry in mcsa_records:
        mcsa_id = entry.get("mcsa_id")
        if mcsa_id is None:
            continue
        enzyme_id = f"m_csa:{mcsa_id}"
        graph.add_node(
            enzyme_id,
            "m_csa_entry",
            name=entry.get("enzyme_name"),
            reference_uniprot_id=entry.get("reference_uniprot_id"),
            mechanism_count=entry.get("mechanism_count"),
            residue_count=entry.get("residue_count"),
            compound_count=entry.get("compound_count"),
            provenance=provenance("m_csa", "curated_active_site_and_mechanism", str(mcsa_id)),
        )

        reference_uniprot_ids = entry.get("reference_uniprot_ids") or [entry.get("reference_uniprot_id")]
        for reference_uniprot_id in [
            accession
            for accession in reference_uniprot_ids
            if isinstance(accession, str) and accession
        ]:
            protein_id = f"uniprot:{reference_uniprot_id}"
            if reference_uniprot_id not in uniprot_by_accession:
                graph.add_node(
                    protein_id,
                    "protein",
                    accession=reference_uniprot_id,
                    provenance=provenance("m_csa", "reference_uniprot_link", str(mcsa_id)),
                )
            graph.add_edge(
                enzyme_id,
                protein_id,
                "has_reference_protein",
                provenance=provenance("m_csa", "reference_uniprot_link", str(mcsa_id)),
            )

        for ec_number in sorted(_ec_numbers_for_entry(entry)):
            ec_id = f"ec:{ec_number}"
            graph.add_node(
                ec_id,
                "ec_number",
                ec_number=ec_number,
                provenance=provenance("m_csa", "ec_annotation", str(mcsa_id)),
            )
            graph.add_edge(
                enzyme_id,
                ec_id,
                "has_ec",
                provenance=provenance("m_csa", "ec_annotation", str(mcsa_id)),
            )

            for reaction in rhea_by_ec.get(ec_number, {}).get("records", []):
                rhea_id = reaction.get("rhea_id")
                if not rhea_id:
                    continue
                reaction_id = f"rhea:{rhea_id}"
                graph.add_node(
                    reaction_id,
                    "rhea_reaction",
                    rhea_id=rhea_id,
                    equation=reaction.get("equation"),
                    ec_number=reaction.get("ec_number"),
                    provenance=provenance("rhea", "reaction_record", rhea_id),
                )
                graph.add_edge(
                    ec_id,
                    reaction_id,
                    "maps_to_reaction",
                    provenance=provenance("rhea", "ec_reaction_mapping", ec_number),
                )

        for index, residue in enumerate(entry.get("catalytic_residues", []), start=1):
            residue_id = f"{enzyme_id}:residue:{index}"
            role_names = sorted(
                {
                    role.get("function")
                    for role in residue.get("roles", [])
                    if isinstance(role, dict) and role.get("function")
                }
            )
            graph.add_node(
                residue_id,
                "catalytic_residue",
                roles=role_names,
                sequence_positions=residue.get("sequence_positions", []),
                structure_positions=residue.get("structure_positions", []),
                roles_summary=residue.get("roles_summary"),
                provenance=provenance("m_csa", "curated_catalytic_residue", str(mcsa_id)),
            )
            graph.add_edge(
                enzyme_id,
                residue_id,
                "has_catalytic_residue",
                provenance=provenance("m_csa", "curated_catalytic_residue", str(mcsa_id)),
            )

        for mechanism in entry.get("mechanism_summaries", []):
            mechanism_id = mechanism.get("mechanism_id")
            if mechanism_id is None:
                continue
            node_id = f"m_csa:{mcsa_id}:mechanism:{mechanism_id}"
            graph.add_node(
                node_id,
                "mechanism_text",
                is_detailed=mechanism.get("is_detailed"),
                text=mechanism.get("text"),
                provenance=provenance("m_csa", "curated_mechanism_text", str(mcsa_id)),
            )
            graph.add_edge(
                enzyme_id,
                node_id,
                "has_mechanism_text",
                provenance=provenance("m_csa", "curated_mechanism_text", str(mcsa_id)),
            )

    return graph.to_graph(metadata or {})


def build_v1_graph(max_mcsa: int = 50, page_size: int = 50) -> dict[str, Any]:
    mcsa_payload = fetch_mcsa_records(max_records=max_mcsa, page_size=page_size)
    mcsa_records = mcsa_payload["records"]
    ec_numbers = sorted({ec for entry in mcsa_records for ec in _ec_numbers_for_entry(entry)})
    accessions = sorted(
        {
            accession
            for entry in mcsa_records
            for accession in (entry.get("reference_uniprot_ids") or [entry.get("reference_uniprot_id")])
            if isinstance(accession, str) and accession
        }
    )
    rhea_by_ec = {ec: fetch_rhea_by_ec(ec) for ec in ec_numbers}
    uniprot_payload = fetch_uniprot_accessions(accessions)
    return assemble_knowledge_graph(
        mcsa_records=mcsa_records,
        rhea_by_ec=rhea_by_ec,
        uniprot_records=uniprot_payload["records"],
        metadata={
            "builder": "v1_graph",
            "mcsa": mcsa_payload["metadata"],
            "rhea_query_count": len(rhea_by_ec),
            "uniprot": uniprot_payload["metadata"],
        },
    )


def summarize_graph(graph: dict[str, Any]) -> dict[str, Any]:
    node_types = Counter(node.get("type", "unknown") for node in graph.get("nodes", []))
    edge_predicates = Counter(edge.get("predicate", "unknown") for edge in graph.get("edges", []))
    provenance_sources = Counter()
    for item in [*graph.get("nodes", []), *graph.get("edges", [])]:
        for prov in item.get("provenance", []):
            source = prov.get("source")
            if source:
                provenance_sources[source] += 1
    return {
        "node_count": len(graph.get("nodes", [])),
        "edge_count": len(graph.get("edges", [])),
        "node_types": dict(sorted(node_types.items())),
        "edge_predicates": dict(sorted(edge_predicates.items())),
        "provenance_sources": dict(sorted(provenance_sources.items())),
    }


def build_seed_graph(mcsa_ids: list[int]) -> dict[str, Any]:
    mcsa_sample = fetch_mcsa_sample(mcsa_ids)
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    rhea_by_ec: dict[str, dict[str, Any]] = {}

    def add_node(node_id: str, node_type: str, **attrs: Any) -> None:
        if node_id not in nodes:
            nodes[node_id] = {"id": node_id, "type": node_type, **attrs}
        else:
            nodes[node_id].update({key: value for key, value in attrs.items() if value is not None})

    def add_edge(source: str, target: str, predicate: str, **attrs: Any) -> None:
        edges.append({"source": source, "target": target, "predicate": predicate, **attrs})

    for entry in mcsa_sample["records"]:
        enzyme_id = f"m_csa:{entry['mcsa_id']}"
        add_node(
            enzyme_id,
            "m_csa_entry",
            name=entry.get("enzyme_name"),
            reference_uniprot_id=entry.get("reference_uniprot_id"),
            mechanism_count=entry.get("mechanism_count"),
            residue_count=entry.get("residue_count"),
        )

        ec_numbers = sorted(
            {
                ec
                for ec in [entry.get("reaction_ec"), *entry.get("ec_numbers", [])]
                if isinstance(ec, str) and ec
            }
        )
        for ec_number in ec_numbers:
            ec_id = f"ec:{ec_number}"
            add_node(ec_id, "ec_number", ec_number=ec_number)
            add_edge(enzyme_id, ec_id, "has_ec", evidence_source="m_csa")

            if ec_number not in rhea_by_ec:
                rhea_by_ec[ec_number] = fetch_rhea_by_ec(ec_number)
            for reaction in rhea_by_ec[ec_number]["records"]:
                rhea_id = reaction.get("rhea_id")
                if not rhea_id:
                    continue
                reaction_id = f"rhea:{rhea_id}"
                add_node(
                    reaction_id,
                    "rhea_reaction",
                    rhea_id=rhea_id,
                    equation=reaction.get("equation"),
                    ec_number=reaction.get("ec_number"),
                )
                add_edge(ec_id, reaction_id, "maps_to_reaction", evidence_source="rhea")

        for index, residue in enumerate(entry.get("catalytic_residues", []), start=1):
            residue_id = f"{enzyme_id}:residue:{index}"
            role_names = sorted(
                {
                    role.get("function")
                    for role in residue.get("roles", [])
                    if isinstance(role, dict) and role.get("function")
                }
            )
            positions = residue.get("sequence_positions", [])
            add_node(
                residue_id,
                "catalytic_residue",
                roles=role_names,
                sequence_positions=positions,
                roles_summary=residue.get("roles_summary"),
            )
            add_edge(enzyme_id, residue_id, "has_catalytic_residue", evidence_source="m_csa")

    degree = defaultdict(int)
    for edge in edges:
        degree[edge["source"]] += 1
        degree[edge["target"]] += 1

    return {
        "metadata": {
            "builder": "seed_graph",
            "mcsa_ids": mcsa_ids,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "rhea_queries": {
                ec: sample["metadata"] for ec, sample in sorted(rhea_by_ec.items())
            },
            "mcsa_query": mcsa_sample["metadata"],
        },
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": sorted(edges, key=lambda item: (item["source"], item["predicate"], item["target"])),
        "degree": dict(sorted(degree.items())),
    }


def _ec_numbers_for_entry(entry: dict[str, Any]) -> set[str]:
    return {
        ec
        for ec in [entry.get("reaction_ec"), *entry.get("ec_numbers", [])]
        if isinstance(ec, str) and ec
    }


def _merge_provenance(left: list[dict[str, Any]], right: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, Any, Any]] = set()
    merged: list[dict[str, Any]] = []
    for item in [*left, *right]:
        if not isinstance(item, dict):
            continue
        key = (item.get("source"), item.get("source_id"), item.get("evidence_level"))
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)
    return merged
