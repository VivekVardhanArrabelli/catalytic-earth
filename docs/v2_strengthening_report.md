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
5. Curated labels now cover all 225 entries in the current source slice, with
   geometry evaluability tracked separately from label availability.
6. mmCIF structure parsing now resolves catalytic residue positions through
   both `auth_*` and `label_*` numbering namespaces.
7. The repo now has local performance checks, in-scope failure analysis,
   expected-cofactor coverage analysis, cofactor policy sweeps, seed-family
   performance audits, and a slice summary artifact for artifact-only workflows.

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
- retained top3 in-scope accuracy at selected threshold 0.4104: 1.0
- out-of-scope abstention rate at selected threshold 0.4104: 1.0
- out-of-scope false non-abstentions at selected threshold 0.4104: 0

The abstention sweep selected threshold 0.4104 under the zero-false policy with
automatic score-boundary threshold candidates:

```text
artifacts/v3_abstention_calibration.json
```

At threshold 0.4104, all 7 in-scope positives are retained and all 13
out-of-scope labels abstain on the 20-entry regression slice. On the 125-entry
geometry slice, the zero-false threshold is 0.4115 and abstains on all 87
out-of-scope controls while retaining all 38/38 in-scope positives:

```text
artifacts/v3_geometry_score_margins_125.json
artifacts/v3_hard_negative_controls_125.json
artifacts/v3_label_expansion_candidates_125.json
```

The 225-label geometry stress slice is fully labeled and intentionally harder:
71 in-scope positives, 153 evaluated out-of-scope controls, 221 evaluable
active-site structures, and 3 labeled out-of-scope structure-mapping issues. Its
calibrated zero-false threshold is 0.4145, which retains 70/71 in-scope
positives (`0.9859`) and reports 0 hard negatives plus 0 near misses. The
remaining in-scope failure is `m_csa:132`, an evidence-limited abstention where
the selected `1LUC` structure lacks the expected flavin/NAD cofactor evidence;
the current actionable in-scope failure count is 0.

## Performance

Current artifact:

```text
artifacts/perf_report.json
```

The suite is local-only and avoids network calls. It measures the current graph,
benchmark, retrieval, label evaluation, abstention sweep, score-margin analysis,
hard-negative selection, in-scope failure analysis, cofactor coverage, cofactor
policy sweeps, seed-family audits, and structure-mapping diagnostics on existing
artifacts.

Latest 5-iteration mean timings on the 225-entry artifacts:

- load V1 graph: 31.686 ms
- build V2 benchmark: 3.045 ms
- run geometry retrieval: 70.038 ms
- evaluate geometry labels: 0.274 ms
- sweep abstention thresholds: 98.516 ms
- analyze geometry score margins: 0.393 ms
- build hard negative controls: 0.821 ms
- analyze in-scope failures: 0.52 ms
- analyze cofactor coverage: 0.55 ms
- analyze cofactor abstention policy: 275.475 ms
- analyze seed-family performance: 0.783 ms
- analyze structure mapping issues: 0.027 ms

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
  floor; the current 225-entry slice has no near misses
- curated labels cover all 225 entries in the current source slice
- structure-mapping blockers are now summarized as a first-class artifact and
  currently report 0 non-OK mappings on the 100-entry slice, 1 labeled
  out-of-scope issue on the 125-entry slice, 2 on the 150- and 175-entry
  slices, and 3 on the 200- and 225-entry slices
- the current label queue is explicit and empty
- cofactor coverage now separates local support, structure-only support, and
  expected cofactors absent from the selected structure
- cofactor policy sweeps recommend audit-only handling for evidence-limited
  retained positives rather than a post-hoc score penalty
- local performance is measured and reproducible

What remains weak:

- the curated label set is still small and provisional despite covering the
  current 225-entry source slice
- the 225-entry slice still has 1 in-scope positive that is abstained because
  the selected structure lacks the expected cofactor context
- ligand/cofactor context is only a simple nearby-ligand heuristic
- substrate-pocket context is currently a heuristic residue-shell summary
- local performance does not measure full-database scalability
