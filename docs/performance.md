# Performance Checks

## Purpose

The V2/V3 scaffold should measure local runtime instead of relying on intuition.
`perf-suite` times the current artifact-only workflow without network calls.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli perf-suite \
  --graph artifacts/v1_graph_1025.json \
  --geometry artifacts/v3_geometry_features_1025.json \
  --retrieval artifacts/v3_geometry_retrieval_1025.json \
  --iterations 3 \
  --out artifacts/perf_report_1025.json
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

Latest 3-iteration mean timings on the current 1,025-preview local artifacts, using
calibrated threshold `0.4115` for label evaluation:

- load V1 graph: 110.104 ms
- build V2 benchmark: 17.555 ms
- run geometry retrieval: 397.688 ms
- evaluate geometry labels: 1.538 ms
- sweep abstention thresholds: 1387.703 ms
- analyze geometry score margins: 1.789 ms
- build hard negative controls: 3.171 ms
- build adversarial negative controls: 5.659 ms
- build label-factory audit: 39.318 ms
- build active-learning review queue: 9.634 ms
- analyze in-scope failures: 1.150 ms
- analyze cofactor coverage: 1.486 ms
- analyze cofactor abstention policy: 1967.761 ms
- analyze seed-family performance: 2.060 ms
- analyze structure mapping issues: 0.141 ms

## Boundary

This is local wall-clock timing for current artifacts. It is not a scalability
benchmark for full M-CSA, full UniProt, AlphaFold DB, or metagenomic-scale
mining.
