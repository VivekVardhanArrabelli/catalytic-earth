# Geometry Features

## Purpose

The V2 baseline uses text and motif evidence. That is useful only as a scaffold.
The next scientific-quality step is geometry-aware active-site representation.

`build-geometry-features` converts M-CSA catalytic residue positions into simple
3D descriptors by fetching public PDB mmCIF files and measuring residue
coordinates.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-v1-graph \
  --max-mcsa 150 \
  --page-size 100 \
  --out artifacts/v1_graph_150.json

PYTHONPATH=src python -m catalytic_earth.cli graph-summary \
  --graph artifacts/v1_graph_150.json \
  --out artifacts/v1_graph_summary_150.json

PYTHONPATH=src python -m catalytic_earth.cli build-v2-benchmark \
  --graph artifacts/v1_graph_150.json \
  --out artifacts/v2_benchmark_150.json

PYTHONPATH=src python -m catalytic_earth.cli build-geometry-features \
  --graph artifacts/v1_graph_150.json \
  --max-entries 150 \
  --out artifacts/v3_geometry_features_150.json

PYTHONPATH=src python -m catalytic_earth.cli run-geometry-retrieval \
  --geometry artifacts/v3_geometry_features_150.json \
  --out artifacts/v3_geometry_retrieval_150.json

PYTHONPATH=src python -m catalytic_earth.cli calibrate-abstention \
  --retrieval artifacts/v3_geometry_retrieval_150.json \
  --out artifacts/v3_abstention_calibration_150.json

PYTHONPATH=src python -m catalytic_earth.cli evaluate-geometry-labels \
  --retrieval artifacts/v3_geometry_retrieval_150.json \
  --abstain-threshold 0.5144 \
  --out artifacts/v3_geometry_label_eval_150.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-failures \
  --retrieval artifacts/v3_geometry_retrieval_150.json \
  --abstain-threshold 0.5144 \
  --out artifacts/v3_geometry_failure_analysis_150.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-in-scope-failures \
  --retrieval artifacts/v3_geometry_retrieval_150.json \
  --abstain-threshold 0.5144 \
  --out artifacts/v3_in_scope_failure_analysis_150.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-geometry-score-margins \
  --retrieval artifacts/v3_geometry_retrieval_150.json \
  --out artifacts/v3_geometry_score_margins_150.json

PYTHONPATH=src python -m catalytic_earth.cli build-hard-negative-controls \
  --retrieval artifacts/v3_geometry_retrieval_150.json \
  --out artifacts/v3_hard_negative_controls_150.json

PYTHONPATH=src python -m catalytic_earth.cli build-label-expansion-candidates \
  --geometry artifacts/v3_geometry_features_150.json \
  --retrieval artifacts/v3_geometry_retrieval_150.json \
  --out artifacts/v3_label_expansion_candidates_150.json

PYTHONPATH=src python -m catalytic_earth.cli analyze-structure-mapping-issues \
  --geometry artifacts/v3_geometry_features_150.json \
  --out artifacts/v3_structure_mapping_issues_150.json

PYTHONPATH=src python -m catalytic_earth.cli summarize-geometry-slices \
  --artifact-dir artifacts \
  --out artifacts/v3_geometry_slice_summary.json
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
  cobalamin, metal ions, SAM, Fe-S clusters)
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
- cobalamin radical rearrangement scoring with explicit B12/cofactor evidence
- flavin dehydrogenase/reductase scoring separated from flavin monooxygenases
- counterevidence penalties for heme-only metal-role overlap, ATP/ADP transfer
  context, carbon-transfer ligand context, hydrogenase and metal-redox ligand
  context, redox electron-transfer roles, histidine-only metal-role sites,
  molybdenum-center heme-like contexts, PLP-like lysine motifs without PLP,
  absent B12 context, nonflavin Fe-S/metal contexts, and flavin contexts
  missing reductant or monooxygenase substrate support
- catalytic-cluster compactness from pairwise distances

This is still a weak baseline, but it is materially better than pure text
overlap because it makes catalytic residue identity and spatial arrangement part
of the retrieval score.

## Abstention And Hard Negatives

`calibrate-abstention` now records both the conservative zero-false threshold
and a positive-retention reference point. Its default `--thresholds auto`
includes observed score-boundary candidates, not only a coarse fixed grid.

Current slices:

- 20-entry regression slice: threshold 0.4681, 20/20 evaluable, 7/7 in-scope
  positives retained, 0 out-of-scope false non-abstentions, 0 hard negatives.
- 100-entry expanded slice: threshold 0.4704, 100/100 evaluable, 25/25
  in-scope positives retained, 0 out-of-scope false non-abstentions, 0 hard
  negatives.
- 125-entry expanded slice: threshold 0.4704, 124/125 evaluable, 38/38
  in-scope positives retained, 0 out-of-scope false non-abstentions, 0 hard
  negatives, 0 near misses, and score gap 0.0562.
- 150-entry expanded slice: threshold 0.5144, 148/150 evaluable, 43/46
  in-scope positives retained, 0 out-of-scope false non-abstentions, 0 hard
  negatives, 0 near misses, and 3 in-scope failures. Two failures have absent
  target cofactor context and one target is absent from the top-k ranking.

`artifacts/v3_geometry_slice_summary.json` summarizes the 20-, 30-, 40-, 50-,
60-, 75-, 100-, 125-, and 150-entry slices. It currently reports zero hard
negatives and zero out-of-scope false non-abstentions across all slices. Only
the 150-entry slice has in-scope failures.

## Label Expansion Queue

The 150-entry geometry artifact is now fully labeled in the provisional registry:

- geometry entries in expansion artifact: 150
- curated labels: 150
- evaluable active-site structures: 148
- unlabeled entries remaining: 0
- ready label-expansion candidates remaining: 0

The structure-mapping issue artifacts currently list 0 non-OK entries for the
20-, 30-, 40-, 50-, 60-, 75-, and 100-entry slices after matching catalytic
residue positions against both mmCIF `auth_*` and `label_*` numbering. The
125-entry slice has 1 labeled out-of-scope mapping issue; the 150-entry slice
has 2 labeled out-of-scope mapping issues.

## Curated Seed Labels

`data/registries/curated_mechanism_labels.json` provides 150 provisional labels,
covering all entries in the 150-entry geometry expansion slice. Labels are
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
