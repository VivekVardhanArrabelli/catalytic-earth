# Performance Checks

## Purpose

The V2/V3 scaffold should measure local runtime instead of relying on intuition.
`perf-suite` times the current artifact-only workflow without network calls.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli perf-suite \
  --graph artifacts/v1_graph_175.json \
  --geometry artifacts/v3_geometry_features_175.json \
  --retrieval artifacts/v3_geometry_retrieval_175.json \
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

Latest 5-iteration mean timings on the current 175-entry local artifacts, using
calibrated threshold `0.4236` for label evaluation:

- load V1 graph: 17.795 ms
- build V2 benchmark: 1.974 ms
- run geometry retrieval: 50.458 ms
- evaluate geometry labels: 0.217 ms
- sweep abstention thresholds: 64.375 ms
- analyze geometry score margins: 0.299 ms
- build hard negative controls: 0.436 ms
- analyze in-scope failures: 0.455 ms
- analyze cofactor coverage: 0.485 ms
- analyze cofactor abstention policy: 206.252 ms
- analyze seed-family performance: 0.681 ms
- analyze structure mapping issues: 0.021 ms

## Boundary

This is local wall-clock timing for current artifacts. It is not a scalability
benchmark for full M-CSA, full UniProt, AlphaFold DB, or metagenomic-scale
mining.
