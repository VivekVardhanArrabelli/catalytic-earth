# Performance Checks

## Purpose

The V2/V3 scaffold should measure local runtime instead of relying on intuition.
`perf-suite` times the current artifact-only workflow without network calls.

## Command

```bash
PYTHONPATH=src python -m catalytic_earth.cli perf-suite \
  --graph artifacts/v1_graph_775.json \
  --geometry artifacts/v3_geometry_features_775.json \
  --retrieval artifacts/v3_geometry_retrieval_775.json \
  --iterations 50 \
  --out artifacts/perf_report_775.json
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

Latest 50-iteration mean timings on the current 775-entry local artifacts, using
calibrated threshold `0.4115` for label evaluation:

- load V1 graph: 82.559 ms
- build V2 benchmark: 17.290 ms
- run geometry retrieval: 295.450 ms
- evaluate geometry labels: 1.299 ms
- sweep abstention thresholds: 1283.487 ms
- analyze geometry score margins: 1.772 ms
- build hard negative controls: 4.621 ms
- build adversarial negative controls: 7.230 ms
- build label-factory audit: 11.470 ms
- build active-learning review queue: 5.916 ms
- analyze in-scope failures: 0.961 ms
- analyze cofactor coverage: 1.303 ms
- analyze cofactor abstention policy: 1625.668 ms
- analyze seed-family performance: 1.737 ms
- analyze structure mapping issues: 0.070 ms

## Boundary

This is local wall-clock timing for current artifacts. It is not a scalability
benchmark for full M-CSA, full UniProt, AlphaFold DB, or metagenomic-scale
mining.
