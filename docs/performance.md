# Performance Checks

## Purpose

The V2/V3 scaffold should measure local runtime instead of relying on intuition.
`perf-suite` times the current artifact-only workflow without network calls.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli perf-suite \
  --graph artifacts/v1_graph_950.json \
  --geometry artifacts/v3_geometry_features_950.json \
  --retrieval artifacts/v3_geometry_retrieval_950.json \
  --iterations 5 \
  --out artifacts/perf_report_950.json
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
- mining adversarial negative controls
- applying label-factory promotion/demotion audit
- building the active-learning review queue
- analyzing in-scope failures
- analyzing expected cofactor coverage for in-scope labels
- sweeping cofactor abstention policy penalties
- auditing retrieval quality by seed fingerprint family
- summarizing non-OK structure mappings and missing-residue diagnostics

Latest 5-iteration mean timings on the current 950-entry local artifacts, using
calibrated threshold `0.4115` for label evaluation:

- load V1 graph: 108.511 ms
- build V2 benchmark: 14.298 ms
- run geometry retrieval: 360.688 ms
- evaluate geometry labels: 1.496 ms
- sweep abstention thresholds: 1414.655 ms
- analyze geometry score margins: 1.924 ms
- build hard negative controls: 3.216 ms
- build adversarial negative controls: 5.728 ms
- build label-factory audit: 26.859 ms
- build active-learning review queue: 8.737 ms
- analyze in-scope failures: 1.178 ms
- analyze cofactor coverage: 1.493 ms
- analyze cofactor abstention policy: 1911.291 ms
- analyze seed-family performance: 2.010 ms
- analyze structure mapping issues: 0.113 ms

## Boundary

This is local wall-clock timing for current artifacts. It is not a scalability
benchmark for full M-CSA, full UniProt, AlphaFold DB, or metagenomic-scale
mining.
