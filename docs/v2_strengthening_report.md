# V2 Strengthening Report

## What Changed

The V2 scaffold was strengthened in several ways:

1. Geometry-aware retrieval now uses residue role phrases and cofactor context,
   not just residue overlap and compactness.
2. Geometry features now include substrate-pocket descriptors from nearby
   protein residues.
3. Serine-hydrolase scoring now requires a coherent Ser nucleophile signal
   before giving full triad evidence.
4. Abstention calibration now reports the tradeoff between zero out-of-scope
   false non-abstentions and retained in-scope positives.
5. Curated labels now cover all 150 entries in the current expanded geometry
   slice, with evaluability tracked separately from label availability.
6. mmCIF structure parsing now resolves catalytic residue positions through
   both `auth_*` and `label_*` numbering namespaces.
7. The repo now has local performance checks, in-scope failure analysis, and a
   slice summary artifact for artifact-only workflows.

## Retrieval Quality

Current artifact:

```text
artifacts/v3_geometry_label_eval.json
```

Current measured result on the 20-entry regression slice:

- evaluated entries: 20
- in-scope seed-fingerprint labels: 7
- out-of-scope labels: 13
- evaluable entries: 20
- top1/top3 in-scope accuracy on evaluable positives: 1.0
- retained top3 in-scope accuracy at selected threshold 0.4681: 1.0
- out-of-scope abstention rate at selected threshold 0.4681: 1.0
- out-of-scope false non-abstentions at selected threshold 0.4681: 0

The abstention sweep selected threshold 0.4681 under the zero-false policy with
automatic score-boundary threshold candidates:

```text
artifacts/v3_abstention_calibration.json
```

At threshold 0.4681, all 7 in-scope positives are retained and all 13
out-of-scope labels abstain on the 20-entry regression slice. On the 125-entry
geometry slice, the zero-false threshold is 0.4704 and abstains on all 87
out-of-scope controls while retaining all 38/38 in-scope positives:

```text
artifacts/v3_geometry_score_margins_125.json
artifacts/v3_hard_negative_controls_125.json
artifacts/v3_label_expansion_candidates_125.json
```

The 150-entry geometry expansion is fully labeled and intentionally harder:
46 in-scope positives, 104 out-of-scope controls, 148 evaluable active-site
structures, and 2 labeled out-of-scope structure-mapping issues. Its calibrated
zero-false threshold is 0.5144, which retains 43/46 in-scope positives
(`0.9348`) and reports 0 hard negatives and 0 near misses. The remaining
failures are in-scope positives with weak or missing cofactor context:
`m_csa:132`, `m_csa:139`, and `m_csa:140`. Two have absent target cofactor
context; one target is absent from the top-k ranking.

## Performance

Current artifact:

```text
artifacts/perf_report.json
```

The suite is local-only and avoids network calls. It measures the current graph,
benchmark, retrieval, label evaluation, abstention sweep, score-margin analysis,
and hard-negative selection on existing artifacts.

Latest 3-iteration mean timings on the 150-entry artifacts:

- load V1 graph: 10.836 ms
- build V2 benchmark: 3.127 ms
- run geometry retrieval: 42.722 ms
- evaluate geometry labels: 0.205 ms
- sweep abstention thresholds: 48.455 ms
- analyze geometry score margins: 0.260 ms
- build hard negative controls: 0.306 ms
- analyze in-scope failures: 0.049 ms
- analyze structure mapping issues: 0.021 ms

## Interpretation

This strengthens V2 as a research scaffold, but it does not make it a validated
enzyme discovery system.

What is now better:

- the model can distinguish metal-dependent hydrolase evidence from heme-like
  residue overlap when metal-ligand roles are present
- serine-hydrolase scoring now penalizes missing Ser nucleophile evidence
- retrieval quality is explicitly measured against curated labels
- abstention has a calibrated threshold artifact with positive-retention
  tradeoffs
- substrate-pocket context now contributes to ranking
- hard negative controls are explicit instead of hidden in aggregate metrics
- near-miss controls now expose out-of-scope rows just below the positive score
  floor
- curated labels cover all 150 entries in the current geometry artifact
- structure-mapping blockers are now summarized as a first-class artifact and
  currently report 0 non-OK mappings on the 100-entry slice, 1 labeled
  out-of-scope issue on the 125-entry slice, and 2 on the 150-entry slice
- the current label queue is explicit and empty
- local performance is measured and reproducible

What remains weak:

- the curated label set is still small and provisional despite covering the
  current 150-entry geometry slice
- the 150-entry slice still has 3 in-scope positives that are misranked or
  abstained because local structure evidence lacks the expected cofactor or
  seed-family context
- ligand/cofactor context is only a simple nearby-ligand heuristic
- substrate-pocket context is currently a heuristic residue-shell summary
- local performance does not measure full-database scalability
