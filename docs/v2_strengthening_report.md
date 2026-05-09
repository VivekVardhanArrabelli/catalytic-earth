# V2 Strengthening Report

## What Changed

The V2 scaffold was strengthened in two ways:

1. Geometry-aware retrieval now uses residue role phrases and cofactor context,
   not just residue overlap and compactness.
2. The repo now has local performance checks for artifact-only workflows.

## Retrieval Quality

Current artifact:

```text
artifacts/v3_geometry_label_eval.json
```

Current measured result on the 20-entry curated geometry slice:

- evaluated entries: 20
- in-scope seed-fingerprint labels: 4
- out-of-scope labels: 16
- top1 in-scope accuracy: 1.0
- top3 in-scope accuracy: 1.0
- out-of-scope abstention rate at threshold 0.7: 0.75

The abstention sweep selected threshold 0.8 under the current rule:

```text
artifacts/v3_abstention_calibration.json
```

## Performance

Current artifact:

```text
artifacts/perf_report.json
```

The suite is local-only and avoids network calls. It measures the current graph,
benchmark, retrieval, label evaluation, and abstention sweep on existing
artifacts.

Latest 5-iteration mean timings:

- load V1 graph: 3.630 ms
- build V2 benchmark: 0.558 ms
- run geometry retrieval: 2.205 ms
- evaluate geometry labels: 0.024 ms
- sweep abstention thresholds: 0.363 ms

## Interpretation

This strengthens V2 as a research scaffold, but it does not make it a validated
enzyme discovery system.

What is now better:

- the model can distinguish metal-dependent hydrolase evidence from heme-like
  residue overlap when metal-ligand roles are present
- retrieval quality is explicitly measured against curated labels
- abstention has a calibrated threshold artifact
- local performance is measured and reproducible

What remains weak:

- the curated label set is small and provisional
- out-of-scope abstention is still imperfect
- ligand/cofactor context is only a simple nearby-ligand heuristic
- no substrate-pocket descriptors exist yet
- local performance does not measure full-database scalability
