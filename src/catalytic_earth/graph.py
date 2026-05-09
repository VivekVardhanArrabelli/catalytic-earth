from __future__ import annotations

from collections import defaultdict
from typing import Any

from .adapters import fetch_mcsa_sample, fetch_rhea_by_ec


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
