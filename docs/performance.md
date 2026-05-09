# Performance Checks

## Purpose

The V2/V3 scaffold should measure local runtime instead of relying on intuition.
`perf-suite` times the current artifact-only workflow without network calls.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli perf-suite \
  --graph artifacts/v1_graph.json \
  --geometry artifacts/v3_geometry_features.json \
  --retrieval artifacts/v3_geometry_retrieval.json \
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
- summarizing non-OK structure mappings and missing-residue diagnostics

Latest 5-iteration mean timings on the current local artifacts, using calibrated
threshold `0.565` for label evaluation:

- load V1 graph: 3.632 ms
- build V2 benchmark: 0.710 ms
- run geometry retrieval: 6.050 ms
- evaluate geometry labels: 0.056 ms
- sweep abstention thresholds: 2.660 ms
- analyze geometry score margins: 0.040 ms
- build hard negative controls: 0.053 ms
- analyze structure mapping issues: 0.007 ms

## Boundary

This is local wall-clock timing for current artifacts. It is not a scalability
benchmark for full M-CSA, full UniProt, AlphaFold DB, or metagenomic-scale
mining.
