# V2 Strengthening Report

## What Changed

The V2 scaffold was strengthened in several ways:

1. Geometry-aware retrieval now uses residue role phrases and cofactor context,
   not just residue overlap and compactness.
2. Geometry features now include substrate-pocket descriptors from nearby
   protein residues.
3. Serine-hydrolase scoring now requires a coherent Ser nucleophile signal
   before giving full triad evidence.
4. Abstention calibration now reports the tradeoff between zero out-of-scope
   false non-abstentions and retained in-scope positives.
5. Curated labels now cover 36 entries in the 40-entry geometry expansion
   artifact, with evaluability tracked separately from label availability.
6. The repo now has local performance checks for artifact-only workflows.

## Retrieval Quality

Current artifact:

```text
artifacts/v3_geometry_label_eval.json
```

Current measured result on the 20-entry regression slice:

- evaluated entries: 20
- in-scope seed-fingerprint labels: 4
- out-of-scope labels: 16
- evaluable entries: 13
- top1/top3 in-scope accuracy on evaluable positives: 1.0
- retained top3 in-scope accuracy at selected threshold 0.5796: 1.0
- out-of-scope abstention rate at selected threshold 0.5796: 1.0
- out-of-scope false non-abstentions at selected threshold 0.5796: 0

The abstention sweep selected threshold 0.5796 under the zero-false policy with
automatic score-boundary threshold candidates:

```text
artifacts/v3_abstention_calibration.json
```

At threshold 0.5796, all 3 evaluable in-scope positives are retained and all 10
evaluable out-of-scope labels abstain on the 20-entry regression slice. On the
40-entry expansion slice, the zero-false threshold is 0.587 and retains 4/7
evaluable positives; 2 metal-like out-of-scope controls remain above the
evaluable positive score floor:

```text
artifacts/v3_geometry_score_margins.json
artifacts/v3_hard_negative_controls.json
artifacts/v3_label_expansion_candidates.json
```

The 40-entry geometry expansion artifact has 36 provisional labels. Four
entries remain unlabeled, and none are ready for review under current evidence
heuristics. Ten labeled entries are not geometry-evaluable yet because their
selected PDB structure did not resolve enough catalytic residues.

## Performance

Current artifact:

```text
artifacts/perf_report.json
```

The suite is local-only and avoids network calls. It measures the current graph,
benchmark, retrieval, label evaluation, abstention sweep, score-margin analysis,
and hard-negative selection on existing artifacts.

Latest 5-iteration mean timings:

- load V1 graph: 3.826 ms
- build V2 benchmark: 0.705 ms
- run geometry retrieval: 3.401 ms
- evaluate geometry labels: 0.042 ms
- sweep abstention thresholds: 1.581 ms
- analyze geometry score margins: 0.025 ms
- build hard negative controls: 0.029 ms
- analyze structure mapping issues: 0.030 ms

## Interpretation

This strengthens V2 as a research scaffold, but it does not make it a validated
enzyme discovery system.

What is now better:

- the model can distinguish metal-dependent hydrolase evidence from heme-like
  residue overlap when metal-ligand roles are present
- serine-hydrolase scoring now penalizes missing Ser nucleophile evidence
- retrieval quality is explicitly measured against curated labels
- abstention has a calibrated threshold artifact with positive-retention
  tradeoffs
- substrate-pocket context now contributes to ranking
- hard negative controls are explicit instead of hidden in aggregate metrics
- curated labels cover 36 entries in the first 40 geometry entries
- structure-mapping blockers are now summarized as a first-class artifact
- the remaining label queue is explicit and currently blocked on evidence
  quality
- local performance is measured and reproducible

What remains weak:

- the curated label set is still small and provisional
- the 40-entry expansion slice still has two hard metal-like out-of-scope
  controls above the evaluable positive score floor; both are role-inferred
  metal overlaps without confirmed hydrolysis labels
- several labeled positives are not geometry-evaluable with the current
  selected PDB structures; the 40-entry issue artifact lists 14 non-evaluable
  mappings, including 2 in-scope positives
- ligand/cofactor context is only a simple nearby-ligand heuristic
- substrate-pocket context is currently a heuristic residue-shell summary
- local performance does not measure full-database scalability
