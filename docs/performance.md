# Performance Checks

## Purpose

The V2/V3 scaffold should measure local runtime instead of relying on intuition.
`perf-suite` times the current artifact-only workflow without network calls.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli perf-suite \
  --graph artifacts/v1_graph_150.json \
  --geometry artifacts/v3_geometry_features_150.json \
  --retrieval artifacts/v3_geometry_retrieval_150.json \
  --iterations 3 \
  --out artifacts/perf_report.json
```

## Benchmarks

The suite currently measures:

- loading the V1 graph artifact
- building the V2 benchmark from the graph
- running geometry-aware retrieval
- evaluating retrieval against curated labels at the artifact's calibrated
  abstention threshold
- sweeping abstention thresholds
- analyzing positive/out-of-scope score margins
- selecting hard negative controls
- analyzing in-scope failures
- summarizing non-OK structure mappings and missing-residue diagnostics

Latest 3-iteration mean timings on the current 150-entry local artifacts, using
calibrated threshold `0.5144` for label evaluation:

- load V1 graph: 10.836 ms
- build V2 benchmark: 3.127 ms
- run geometry retrieval: 42.722 ms
- evaluate geometry labels: 0.205 ms
- sweep abstention thresholds: 48.455 ms
- analyze geometry score margins: 0.260 ms
- build hard negative controls: 0.306 ms
- analyze in-scope failures: 0.049 ms
- analyze structure mapping issues: 0.021 ms

## Boundary

This is local wall-clock timing for current artifacts. It is not a scalability
benchmark for full M-CSA, full UniProt, AlphaFold DB, or metagenomic-scale
mining.
