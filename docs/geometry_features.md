# Geometry Features

## Purpose

The V2 baseline uses text and motif evidence. That is useful only as a scaffold.
The next scientific-quality step is geometry-aware active-site representation.

`build-geometry-features` converts M-CSA catalytic residue positions into simple
3D descriptors by fetching public PDB mmCIF files and measuring residue
coordinates.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features \
  --graph artifacts/v1_graph.json \
  --max-entries 20 \
  --out artifacts/v3_geometry_features.json

PYTHONPATH=src python -m catalytic_earth.cli run-geometry-retrieval \
  --geometry artifacts/v3_geometry_features.json \
  --top-k 5 \
  --out artifacts/v3_geometry_retrieval.json

PYTHONPATH=src python -m catalytic_earth.cli evaluate-geometry-labels \
  --retrieval artifacts/v3_geometry_retrieval.json \
  --labels data/registries/curated_mechanism_labels.json \
  --out artifacts/v3_geometry_label_eval.json
```

## Current Feature Set

For each M-CSA entry with structure positions:

- chosen PDB id
- catalytic residue nodes
- residue codes, chain ids, and residue ids
- residue centroids
- CA coordinates when present
- pairwise catalytic-residue distances
- missing-position counts

## Geometry-Aware Retrieval

`run-geometry-retrieval` ranks seed mechanism fingerprints with:

- residue signature overlap
- role hint overlap
- catalytic-cluster compactness from pairwise distances

This is still a weak baseline, but it is materially better than pure text
overlap because it makes catalytic residue identity and spatial arrangement part
of the retrieval score.

## Curated Seed Labels

`data/registries/curated_mechanism_labels.json` provides provisional labels for
the 20-entry geometry slice. Labels are intentionally conservative:

- `seed_fingerprint` means the entry maps to one of the current seed mechanism
  fingerprints.
- `out_of_scope` means the entry needs a more specific fingerprint before it
  should be used as a positive label.

These labels are curated enough to test retrieval behavior and abstention, but
they are not a substitute for expert mechanism review.

## Why This Matters

Mechanism-first enzyme discovery cannot rely on EC labels or keyword overlap.
Catalytic function depends on residue identity, spatial arrangement, cofactors,
substrate access, and reaction chemistry. This artifact starts the move from
label retrieval toward active-site geometry retrieval.

## Limitations

- Distances are crude CA-or-centroid descriptors.
- Alternate conformations, insertion codes, ligands, cofactors, and biological
  assemblies are not modeled yet.
- Static PDB structures can miss catalytically relevant conformations.
- Geometry features are evidence, not validation.
- The current retrieval baseline uses simple compactness heuristics, not a
  learned geometry model.
