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
  --abstain-threshold 0.5796 \
  --out artifacts/v3_geometry_label_eval.json

PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention \
  --retrieval artifacts/v3_geometry_retrieval.json \
  --out artifacts/v3_abstention_calibration.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-failures \
  --retrieval artifacts/v3_geometry_retrieval.json \
  --abstain-threshold 0.5796 \
  --out artifacts/v3_geometry_failure_analysis.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-score-margins \
  --retrieval artifacts/v3_geometry_retrieval.json \
  --out artifacts/v3_geometry_score_margins.json

PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls \
  --retrieval artifacts/v3_geometry_retrieval.json \
  --out artifacts/v3_hard_negative_controls.json

PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features \
  --graph artifacts/v1_graph.json \
  --max-entries 30 \
  --out artifacts/v3_geometry_features_30.json

PYTHONPATH=src python -m catalytic_earth.cli run-geometry-retrieval \
  --geometry artifacts/v3_geometry_features_30.json \
  --out artifacts/v3_geometry_retrieval_30.json

PYTHONPATH=src python -m catalytic_earth.cli evaluate-geometry-labels \
  --retrieval artifacts/v3_geometry_retrieval_30.json \
  --abstain-threshold 0.587 \
  --out artifacts/v3_geometry_label_eval_30.json

PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention \
  --retrieval artifacts/v3_geometry_retrieval_30.json \
  --out artifacts/v3_abstention_calibration_30.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-score-margins \
  --retrieval artifacts/v3_geometry_retrieval_30.json \
  --out artifacts/v3_geometry_score_margins_30.json

PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls \
  --retrieval artifacts/v3_geometry_retrieval_30.json \
  --out artifacts/v3_hard_negative_controls_30.json

PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features \
  --graph artifacts/v1_graph.json \
  --max-entries 40 \
  --out artifacts/v3_geometry_features_40.json

PYTHONPATH=src python -m catalytic_earth.cli run-geometry-retrieval \
  --geometry artifacts/v3_geometry_features_40.json \
  --out artifacts/v3_geometry_retrieval_40.json

PYTHONPATH=src python -m catalytic_earth.cli evaluate-geometry-labels \
  --retrieval artifacts/v3_geometry_retrieval_40.json \
  --abstain-threshold 0.587 \
  --out artifacts/v3_geometry_label_eval_40.json

PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention \
  --retrieval artifacts/v3_geometry_retrieval_40.json \
  --out artifacts/v3_abstention_calibration_40.json

PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls \
  --retrieval artifacts/v3_geometry_retrieval_40.json \
  --out artifacts/v3_hard_negative_controls_40.json

PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates \
  --geometry artifacts/v3_geometry_features_40.json \
  --retrieval artifacts/v3_geometry_retrieval_40.json \
  --out artifacts/v3_label_expansion_candidates.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-structure-mapping-issues \
  --geometry artifacts/v3_geometry_features_40.json \
  --out artifacts/v3_structure_mapping_issues_40.json
```

## Current Feature Set

For each M-CSA entry with structure positions:

- chosen PDB id
- catalytic residue nodes
- residue codes, chain ids, and residue ids
- residue centroids
- CA coordinates when present
- pairwise catalytic-residue distances
- missing-position counts and observed residue-code mismatch diagnostics
- proximal non-polymer ligands from mmCIF `HETATM` records
- inferred cofactor families from nearby ligands (for example heme, flavin, PLP,
  metal ions, SAM, Fe-S clusters)
- cofactor evidence level for retrieval hits (`ligand_supported`,
  `role_inferred`, `absent`, or `not_required`)
- substrate-pocket residue context from nearby protein `ATOM` records
- pocket descriptors (hydrophobic/polar/charge/aromatic/sulfur fractions and
  mean residue distance to active site)

## Geometry-Aware Retrieval

`run-geometry-retrieval` ranks seed mechanism fingerprints with:

- residue signature overlap
- role hint overlap
- ligand-supported cofactor context
- substrate-pocket descriptor compatibility
- serine-hydrolase mechanistic coherence for the Ser nucleophile requirement
- catalytic-cluster compactness from pairwise distances

This is still a weak baseline, but it is materially better than pure text
overlap because it makes catalytic residue identity and spatial arrangement part
of the retrieval score.

## Abstention And Hard Negatives

`calibrate-abstention` now records both the conservative zero-false threshold
and a positive-retention reference point. Its default `--thresholds auto`
includes observed score-boundary candidates, not only a coarse fixed grid. On
the 20-entry regression slice:

- selected zero-false threshold: 0.5796
- out-of-scope false non-abstentions at 0.5796: 0
- in-scope retention at 0.5796: 0.75 overall, 1.0 for evaluable positives
- hard negative controls at the evaluable positive score floor: 0

On the 40-entry label slice, 2 evaluable out-of-scope controls still overlap
the evaluable positive score range, so scorer separation remains the next
quality target. Both current hard negatives are metal-role overlaps without
confirmed hydrolysis labels.

## Label Expansion Queue

The 40-entry geometry artifact is mostly labeled in the provisional registry:

- geometry entries in expansion artifact: 40
- curated labels: 36
- evaluable active-site structures: 26
- unlabeled entries remaining: 4

The remaining unlabeled entries are not ready by current evidence heuristics;
the next label pass should either improve structure mapping first or build a
larger geometry artifact. The candidate artifact lists per-entry readiness
blockers such as unresolved catalytic residues, absent pairwise geometry, or low
retrieval score.

The structure-mapping issue artifact currently lists 14 non-OK 40-slice
entries: 10 are already labeled and 2 are in-scope seed positives. All current
mapping failures are insufficient-resolved-residue cases, so the next productive
data task is alternate structure selection or residue-alias handling rather than
labeling those entries blindly. The most common expected residue codes in the
missing mappings are Asp and His (12 each), followed by Glu (8), which points to
chain/numbering mismatches around catalytic residues rather than a single
cofactor-specific alias. The in-scope positive mapping blockers are `m_csa:15`
on PDB `1ZNB` and `m_csa:28` on PDB `1DJX`.

## Curated Seed Labels

`data/registries/curated_mechanism_labels.json` provides 36 provisional labels
for the 40-entry geometry expansion slice. Labels are intentionally
conservative:

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
- Alternate conformations, insertion codes, and biological assemblies are not
  modeled yet.
- Static PDB structures can miss catalytically relevant conformations.
- Geometry features are evidence, not validation.
- The current retrieval baseline uses simple compactness heuristics, not a
  learned geometry model.
