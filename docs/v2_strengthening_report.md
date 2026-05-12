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
5. Curated labels now cover 642 countable entries: the full 475-entry source
   slice plus 167 factory-accepted labels from the 500-, 525-, 550-, 575-,
   600-, 625-, 650-, 675-, 700-, 725-, 750-, and 775-entry queues, with geometry
   evaluability tracked separately from label availability.
6. mmCIF structure parsing now resolves catalytic residue positions through
   both `auth_*` and `label_*` numbering namespaces.
7. The repo now has local performance checks, in-scope failure analysis,
   expected-cofactor coverage analysis, cofactor policy sweeps, seed-family
   performance audits, and a slice summary artifact for artifact-only workflows.
8. Label-factory automation now gates scaling with explicit label tiers,
   deterministic promotion/demotion, adversarial negatives, active-learning
   review queues, family-propagation guardrails, and expert-review
   export/import.

## Retrieval Quality

Current artifact:

```text
artifacts/v3_geometry_label_eval_775.json
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

The 775-entry countable geometry stress slice is intentionally harder: 175
in-scope positives, 466 evaluated out-of-scope controls, 625 evaluable
active-site structures, and 27 structure-mapping issues. Its calibrated
zero-false threshold is 0.4115, which retains 171/175 in-scope positives
(`0.9828`) and reports 0 hard negatives plus 0 near misses. The
remaining in-scope failures are `m_csa:132`, `m_csa:353`, `m_csa:372`, and
`m_csa:430`; all are evidence-limited abstentions tied to selected-structure
cofactor gaps, so the current actionable in-scope failure count is 0.

The 500-, 525-, 550-, 575-, 600-, 625-, 650-, 675-, 700-, 725-, 750-, and
775-entry candidate queues have been processed through the label factory. The
accepted countable subsets added 167 labels beyond the 475-entry slice and
leave 138 accepted-775 review-state rows outside the benchmark until local
evidence gaps are repaired.

The label-factory slice adds `artifacts/v3_label_factory_audit_500.json`,
`artifacts/v3_label_factory_applied_labels_500.json`,
`artifacts/v3_adversarial_negative_controls_500.json`,
`artifacts/v3_active_learning_review_queue_500.json`,
`artifacts/v3_expert_review_export_500.json`,
`artifacts/v3_family_propagation_guardrails_500.json`, and
`artifacts/v3_label_factory_gate_check_500.json`; the accepted 775 artifacts
carry the same workflow forward at `*_775.json`. The current gate passes for
the 642-label countable registry, and
`artifacts/v3_label_batch_acceptance_check_775.json` records the latest
accepted 775-slice batch. Review-debt remediation artifacts now separate
structure-wide alternate-PDB cofactor hits from local active-site support before
any further count growth.

## Performance

Current artifact:

```text
artifacts/perf_report_775.json
```

The suite is local-only and avoids network calls. It measures the current graph,
benchmark, retrieval, label evaluation, abstention sweep, score-margin analysis,
hard-negative selection, in-scope failure analysis, cofactor coverage, cofactor
policy sweeps, seed-family audits, and structure-mapping diagnostics on existing
artifacts.

Latest 50-iteration mean timings on the 775-entry artifacts:

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
  floor; the current 775-entry countable slice has no near misses
- curated labels cover 642 countable entries
- structure-mapping blockers are now summarized as a first-class artifact and
  currently report 0 non-OK mappings on the 100-entry slice, 1 labeled
  out-of-scope issue on the 125-entry slice, 2 on the 150- and 175-entry
  slices, 3 on the 200-, 225-, 250-, 275-, and 300-entry slices, 4 on the
  325-entry slice, 5 on the 350-entry slice, 7 on the 375-, 400-, 425-, 450-,
  and 475-entry slices, 8 on the 500- and 525-entry slices, 10 on the
  550-entry slice, 11 on the 575- and 600-entry slices, 15 on the 625-entry
  slice, 17 on the 650- and 675-entry slices, 19 on the 700-entry slice, 21 on
  the 725-entry slice, 23 on the 750-entry slice, and 27 on the 775-entry slice
- the current 775-entry label queue is explicit; the accepted 775 batch is
  resolved only for 5 clean labels, and the post-batch active-learning queue
  retains all 133 expert-label decision rows while 138 review-state rows remain
  non-countable; the queue continues to prioritize reaction/substrate mismatch
  review rows with kinase or ATP phosphoryl-transfer text, while
  family-propagation guardrails retain 24 related propagation blockers
- cofactor coverage now separates local support, structure-only support, and
  expected cofactors absent from the selected structure
- cofactor policy sweeps recommend audit-only handling for evidence-limited
  retained positives rather than a post-hoc score penalty
- local performance is measured and reproducible

What remains weak:

- the curated label set is still provisional despite covering 642 countable
  entries; bronze/silver factory tiers are not expert validation
- the 775-entry countable slice still has 4 in-scope positives that are
  abstained because the selected structures lack expected local or
  structure-wide cofactor context
- ligand/cofactor context is only a simple nearby-ligand heuristic
- substrate-pocket context is currently a heuristic residue-shell summary
- local performance does not measure full-database scalability
