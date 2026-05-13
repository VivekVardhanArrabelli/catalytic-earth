# Performance Checks

## Purpose

The V2/V3 scaffold should measure local runtime instead of relying on intuition.
`perf-suite` times the current artifact-only workflow without network calls.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli perf-suite \
  --graph artifacts/v1_graph_1000.json \
  --geometry artifacts/v3_geometry_features_1000.json \
  --retrieval artifacts/v3_geometry_retrieval_1000.json \
  --iterations 3 \
  --out artifacts/perf_report_1000.json
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

Latest 3-iteration mean timings on the current 1,000-entry local artifacts, using
calibrated threshold `0.4115` for label evaluation:

- load V1 graph: 96.720 ms
- build V2 benchmark: 14.682 ms
- run geometry retrieval: 385.569 ms
- evaluate geometry labels: 1.673 ms
- sweep abstention thresholds: 1386.516 ms
- analyze geometry score margins: 1.729 ms
- build hard negative controls: 3.121 ms
- build adversarial negative controls: 36.282 ms
- build label-factory audit: 8.891 ms
- build active-learning review queue: 9.682 ms
- analyze in-scope failures: 1.226 ms
- analyze cofactor coverage: 1.475 ms
- analyze cofactor abstention policy: 1965.815 ms
- analyze seed-family performance: 2.027 ms
- analyze structure mapping issues: 0.141 ms

## Boundary

This is local wall-clock timing for current artifacts. It is not a scalability
benchmark for full M-CSA, full UniProt, AlphaFold DB, or metagenomic-scale
mining.
