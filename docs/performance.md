# Performance Checks

## Purpose

The V2/V3 scaffold should measure local runtime instead of relying on intuition.
`perf-suite` times the current artifact-only workflow without network calls.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli perf-suite \
  --graph artifacts/v1_graph_475.json \
  --geometry artifacts/v3_geometry_features_475.json \
  --retrieval artifacts/v3_geometry_retrieval_475.json \
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

Latest 5-iteration mean timings on the current 475-entry local artifacts, using
calibrated threshold `0.4115` for label evaluation:

- load V1 graph: 49.736 ms
- build V2 benchmark: 6.766 ms
- run geometry retrieval: 176.244 ms
- evaluate geometry labels: 0.902 ms
- sweep abstention thresholds: 672.691 ms
- analyze geometry score margins: 1.221 ms
- build hard negative controls: 2.213 ms
- analyze in-scope failures: 0.764 ms
- analyze cofactor coverage: 0.925 ms
- analyze cofactor abstention policy: 795.197 ms
- analyze seed-family performance: 1.332 ms
- analyze structure mapping issues: 0.055 ms

## Boundary

This is local wall-clock timing for current artifacts. It is not a scalability
benchmark for full M-CSA, full UniProt, AlphaFold DB, or metagenomic-scale
mining.
