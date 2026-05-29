# Geometry Nonlinear Head Audit

Run: 2026-05-29T13:08:34Z

No labels, registries, ontologies, imports, production scoring, or global thresholds were edited. The abstention threshold was selected on calibration rows only.

## Headline

- Logistic rerun primary: 5/45 correct, 40 abstained, 0 wrong nonabstained.
- Primary-only MLP-32 primary: 0/45 correct, 45 abstained, 0 wrong nonabstained.
- OOS-aware MLP-32 primary: 32/45 correct, 13 abstained, 0 wrong nonabstained.
- OOS-aware MLP OOS/sec false-positive rate: 0.0.
- Hand edge closed versus Wave 1.2 geometry-logistic: 0.133332.
- Hand edge closed versus local logistic control: 0.675.
- Interpretation: remaining MLP gap is abstention-dominated under the frozen calibration policy.

## Per-bin MLP

| Bin | Primary support | Primary abstain | Primary acc | OOS/sec support | OOS/sec FP |
| --- | ---: | ---: | ---: | ---: | ---: |
| broad_bucket_ambiguous | 0 | 0 | None | 89 | 0.0 |
| dense_same_mechanism_structural_neighborhood | 10 | 3 | 0.7 | 0 | None |
| high_structure_similarity_different_fingerprint | 0 | 0 | None | 5 | 0.0 |
| low_structure_neighborhood_near_orphan | 30 | 7 | 0.766667 | 0 | None |
| no_reliable_structure | 5 | 3 | 0.4 | 1 | 0.0 |
