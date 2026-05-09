# Graph Schema

## Purpose

The graph schema defines the persistent v1 representation for Catalytic Earth.
It is intentionally simple JSON so early artifacts are easy to inspect, diff,
test, and regenerate.

## Top-Level Shape

```json
{
  "metadata": {
    "schema_version": "0.1.0",
    "generated_at": "ISO-8601 timestamp",
    "builder": "v1_graph",
    "node_count": 0,
    "edge_count": 0
  },
  "nodes": [],
  "edges": [],
  "summary": {}
}
```

## Node Contract

Every node must have:

- `id`: stable namespaced identifier, for example `uniprot:P56868`.
- `type`: node class.
- `provenance`: list of source evidence records.

Current node types:

- `m_csa_entry`
- `protein`
- `ec_number`
- `rhea_reaction`
- `catalytic_residue`
- `mechanism_text`
- `structure`

## Edge Contract

Every edge must have:

- `source`: node id.
- `target`: node id.
- `predicate`: relationship type.
- `provenance`: list of source evidence records.

Current predicates:

- `has_reference_protein`
- `has_ec`
- `maps_to_reaction`
- `has_catalytic_residue`
- `has_mechanism_text`
- `has_structure`

## Provenance Contract

Every provenance record should have:

- `source`: source registry id, such as `m_csa`, `rhea`, or `uniprot`.
- `source_id`: source-local identifier where available.
- `evidence_level`: what kind of evidence the source provides.

The graph treats provenance as evidence, not truth. Conflicts should be retained
for later benchmark and misannotation work.

## V1 Build Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-v1-graph \
  --max-mcsa 50 \
  --page-size 50 \
  --out artifacts/v1_graph.json

PYTHONPATH=src python -m catalytic_earth.cli graph-summary \
  --graph artifacts/v1_graph.json \
  --out artifacts/v1_graph_summary.json
```
