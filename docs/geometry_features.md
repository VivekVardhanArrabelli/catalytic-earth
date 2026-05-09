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
  --abstain-threshold 0.5682 \
  --out artifacts/v3_geometry_label_eval.json

PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention \
  --retrieval artifacts/v3_geometry_retrieval.json \
  --out artifacts/v3_abstention_calibration.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-failures \
  --retrieval artifacts/v3_geometry_retrieval.json \
  --abstain-threshold 0.5682 \
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
  --abstain-threshold 0.5777 \
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
  --abstain-threshold 0.5777 \
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

PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features \
  --graph artifacts/v1_graph.json \
  --max-entries 50 \
  --out artifacts/v3_geometry_features_50.json

PYTHONPATH=src python -m catalytic_earth.cli run-geometry-retrieval \
  --geometry artifacts/v3_geometry_features_50.json \
  --out artifacts/v3_geometry_retrieval_50.json

PYTHONPATH=src python -m catalytic_earth.cli evaluate-geometry-labels \
  --retrieval artifacts/v3_geometry_retrieval_50.json \
  --abstain-threshold 0.5777 \
  --out artifacts/v3_geometry_label_eval_50.json

PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention \
  --retrieval artifacts/v3_geometry_retrieval_50.json \
  --out artifacts/v3_abstention_calibration_50.json

PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates \
  --geometry artifacts/v3_geometry_features_50.json \
  --retrieval artifacts/v3_geometry_retrieval_50.json \
  --out artifacts/v3_label_expansion_candidates_50.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-structure-mapping-issues \
  --geometry artifacts/v3_geometry_features_50.json \
  --out artifacts/v3_structure_mapping_issues_50.json

PYTHONPATH=src python -m catalytic_earth.cli build-v1-graph \
  --max-mcsa 75 \
  --page-size 75 \
  --out artifacts/v1_graph_75.json

PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features \
  --graph artifacts/v1_graph_75.json \
  --max-entries 60 \
  --out artifacts/v3_geometry_features_60.json

PYTHONPATH=src python -m catalytic_earth.cli run-geometry-retrieval \
  --geometry artifacts/v3_geometry_features_60.json \
  --out artifacts/v3_geometry_retrieval_60.json

PYTHONPATH=src python -m catalytic_earth.cli evaluate-geometry-labels \
  --retrieval artifacts/v3_geometry_retrieval_60.json \
  --abstain-threshold 0.5931 \
  --out artifacts/v3_geometry_label_eval_60.json

PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention \
  --retrieval artifacts/v3_geometry_retrieval_60.json \
  --out artifacts/v3_abstention_calibration_60.json

PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls \
  --retrieval artifacts/v3_geometry_retrieval_60.json \
  --out artifacts/v3_hard_negative_controls_60.json

PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates \
  --geometry artifacts/v3_geometry_features_60.json \
  --retrieval artifacts/v3_geometry_retrieval_60.json \
  --out artifacts/v3_label_expansion_candidates_60.json
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
- auth-vs-label residue-number fallback for mmCIF structures that use different
  sequence numbering namespaces
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
- counterevidence penalties for heme-only metal-role overlap, ATP/ADP transfer
  context, redox electron-transfer roles, and PLP-like lysine motifs without PLP
- catalytic-cluster compactness from pairwise distances

This is still a weak baseline, but it is materially better than pure text
overlap because it makes catalytic residue identity and spatial arrangement part
of the retrieval score.

## Abstention And Hard Negatives

`calibrate-abstention` now records both the conservative zero-false threshold
and a positive-retention reference point. Its default `--thresholds auto`
includes observed score-boundary candidates, not only a coarse fixed grid.

Current slices:

- 20-entry regression slice: threshold 0.5682, 20/20 evaluable, 4/4 in-scope
  positives retained, 0 out-of-scope false non-abstentions.
- 40-entry expansion slice: threshold 0.5777, 40/40 evaluable, 12/12 in-scope
  positives retained, 0 out-of-scope false non-abstentions.
- 50-entry graph slice: threshold 0.5777, 50/50 evaluable, 13/13 in-scope
  positives retained, 0 out-of-scope false non-abstentions.
- 60-entry expanded slice: threshold 0.5931, 60/60 evaluable, 5/13 in-scope
  positives retained, 0 out-of-scope false non-abstentions.

The current 60-entry score-margin artifact shows a -0.0153 gap: 2 out-of-scope
metal-like controls score at or above the in-scope positive floor, and 2 more
near misses sit within 0.01 below it. This is the next scorer-separation target.

## Label Expansion Queue

The 60-entry geometry artifact is now fully labeled in the provisional registry:

- geometry entries in expansion artifact: 60
- curated labels: 63
- evaluable active-site structures: 60
- unlabeled entries remaining: 0
- ready label-expansion candidates remaining: 0

The structure-mapping issue artifacts currently list 0 non-OK entries for the
40-, 50-, and 60-entry slices after matching catalytic residue positions against
both mmCIF `auth_*` and `label_*` numbering.

## Curated Seed Labels

`data/registries/curated_mechanism_labels.json` provides 63 provisional labels,
covering all entries in the 60-entry geometry expansion slice. Labels are
intentionally conservative:

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
