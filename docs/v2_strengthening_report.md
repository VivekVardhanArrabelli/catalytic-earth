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
5. Curated labels now cover all 100 entries in the current expanded geometry
   slice, with evaluability tracked separately from label availability.
6. mmCIF structure parsing now resolves catalytic residue positions through
   both `auth_*` and `label_*` numbering namespaces.
7. The repo now has local performance checks for artifact-only workflows.

## Retrieval Quality

Current artifact:

```text
artifacts/v3_geometry_label_eval.json
```

Current measured result on the 20-entry regression slice:

- evaluated entries: 20
- in-scope seed-fingerprint labels: 5
- out-of-scope labels: 15
- evaluable entries: 20
- top1/top3 in-scope accuracy on evaluable positives: 1.0
- retained top3 in-scope accuracy at selected threshold 0.565: 1.0
- out-of-scope abstention rate at selected threshold 0.565: 1.0
- out-of-scope false non-abstentions at selected threshold 0.565: 0

The abstention sweep selected threshold 0.565 under the zero-false policy with
automatic score-boundary threshold candidates:

```text
artifacts/v3_abstention_calibration.json
```

At threshold 0.565, all 5 in-scope positives are retained and all 15
out-of-scope labels abstain on the 20-entry regression slice. On the 100-entry
geometry slice, the zero-false threshold is 0.5653 and abstains on all 75
out-of-scope controls while retaining all 25/25 in-scope positives:

```text
artifacts/v3_geometry_score_margins_100.json
artifacts/v3_hard_negative_controls_100.json
artifacts/v3_label_expansion_candidates_100.json
```

The 100-entry geometry expansion artifact is fully labeled and has 100
geometry-evaluable active-site structures. No entries remain in the current
label-expansion queue. The 100-entry hard-negative artifact has 0 score-overlap
controls and 0 near misses within 0.01 below the in-scope score floor after
cobalamin, carbon-transfer ligand, aromatic role-inferred metal-pocket,
nucleotide-transfer, absent-PLP, and flavin-dehydrogenase contexts are
separated from generic seed evidence.

## Performance

Current artifact:

```text
artifacts/perf_report.json
```

The suite is local-only and avoids network calls. It measures the current graph,
benchmark, retrieval, label evaluation, abstention sweep, score-margin analysis,
and hard-negative selection on existing artifacts.

Latest 5-iteration mean timings:

- load V1 graph: 3.888 ms
- build V2 benchmark: 0.731 ms
- run geometry retrieval: 7.092 ms
- evaluate geometry labels: 0.050 ms
- sweep abstention thresholds: 2.614 ms
- analyze geometry score margins: 0.042 ms
- build hard negative controls: 0.050 ms
- analyze structure mapping issues: 0.008 ms

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
- near-miss controls now expose out-of-scope rows just below the positive score
  floor
- curated labels cover all 100 entries in the current geometry artifact
- structure-mapping blockers are now summarized as a first-class artifact and
  currently report 0 non-OK mappings on the 100-entry slice
- the current label queue is explicit and empty
- local performance is measured and reproducible

What remains weak:

- the curated label set is still small and provisional despite covering the
  current 100-entry geometry slice
- the 100-entry slice is still small despite a clean 0.0125 score gap, so the
  current perfect retained accuracy needs broader labels and a larger benchmark
- ligand/cofactor context is only a simple nearby-ligand heuristic
- substrate-pocket context is currently a heuristic residue-shell summary
- local performance does not measure full-database scalability
