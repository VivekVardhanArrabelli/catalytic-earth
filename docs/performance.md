# Performance Checks

## Purpose

The V2/V3 scaffold should measure local runtime instead of relying on intuition.
`perf-suite` times the current artifact-only workflow without network calls.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli perf-suite \
  --graph artifacts/v1_graph_275.json \
  --geometry artifacts/v3_geometry_features_275.json \
  --retrieval artifacts/v3_geometry_retrieval_275.json \
  --iterations 5 \
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
- analyzing expected cofactor coverage for in-scope labels
- sweeping cofactor abstention policy penalties
- auditing retrieval quality by seed fingerprint family
- summarizing non-OK structure mappings and missing-residue diagnostics

Latest 5-iteration mean timings on the current 275-entry local artifacts, using
calibrated threshold `0.4115` for label evaluation:

- load V1 graph: 35.346 ms
- build V2 benchmark: 3.909 ms
- run geometry retrieval: 107.88 ms
- evaluate geometry labels: 0.373 ms
- sweep abstention thresholds: 139.265 ms
- analyze geometry score margins: 0.444 ms
- build hard negative controls: 0.963 ms
- analyze in-scope failures: 0.559 ms
- analyze cofactor coverage: 0.622 ms
- analyze cofactor abstention policy: 345.878 ms
- analyze seed-family performance: 0.846 ms
- analyze structure mapping issues: 0.031 ms

## Boundary

This is local wall-clock timing for current artifacts. It is not a scalability
benchmark for full M-CSA, full UniProt, AlphaFold DB, or metagenomic-scale
mining.
