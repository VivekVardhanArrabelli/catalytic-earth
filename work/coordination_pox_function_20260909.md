# POX functional evidence comparison — 2026-09-09

Parent owns Git, publication and the cooperative lock. All reviewers are
read-only. Start: 2026-09-09T23:06:50Z. Base:
`e9ce146bb519e3489d8d43b7d4eb5162391ddf86`.

Question: can the retained study's POX Table 2b and methods support a second
enzyme context that distinguishes MAP analogue binding, pyruvate processing
and steady-state function using the existing functional-comparison concepts?

Expected gain: preserve assay/parameter identity across chemically distinct
contexts and expose invalid cross-endpoint transfers relevant to design data.
Stop if enzyme/source/assay identity is unresolved, case-specific code would be
needed, or there is no useful relation beyond the source table.

Source scope: `human-tkt-e160q-6ha3-geometry-function`. Retained bytes at
`/private/tmp/ce-6ha3-UOvXho/` only. New scientific requests/bytes: 0/0.
Inherited 7 captures / 3,004,884 bytes is a metered lower bound; complete
accounting/headroom remains unknown. Do not reacquire or rename the batch.

Review roles (computational; correlated errors remain possible):

- Source: independently transcribe POX Table 2b and bind exact enzyme/methods.
- Representation: test reuse of existing assay/parameter/uncertainty concepts.
- Adversarial: challenge meaningful added value, inference and claim boundaries.
- Parent: inspect retained originals, curate only supported facts, integrate,
  verify, inspect diff and publish after accepted review and required CI.

## Findings and review

- Source reviewer independently matched all six POX rows and ten kinetic
  columns, Table 2b footnotes h-k and Methods printed pages 8-9. The exact
  reported enzyme is L. plantarum POX; no accession or coordinate map is inferred.
- E59Q has source-reported MAP nonbinding and unavailable MAP parameters,
  but source-reported fitted pyruvate/DCPIP kcat 0.49 ± 0.01 s^-1 and anaerobic pyruvate/FAD
  apparent processing 1.07 ± 0.08 s^-1. These do not establish oxygen turnover,
  a common activity label, a single elementary-step rate or geometric causation.
- Retained both MAP source-name spellings, the invalid printed path-length
  unit `10 mM`, and unstated single-turnover pH. E60A's printed single-turnover
  efficiency 12.5 is not replaced by 113/9.0 = 12.56 from displayed inputs.
- All case facts fit additive data. Reported quotients retain formula,
  denominator, units and non-independent identity. No runtime or validator
  change is needed, and no curation-time saving is claimed.
- Parent verified all repository/source-body pins, eight central-value ratios,
  17 source-reported quotients at their displayed rounding, and both exact
  cross-context pointers. One shared traversal of both comparison files
  returns three TKT reporter-unavailable variants and one POX
  analogue-nonbinding variant, with separate steady-state assay identities.
  These are reused observations, not independent new evidence.
- Final comparison after source clarification and fitted-parameter wording:
  `570ffb83d9272d41ed72ff389c2f56fbc1415c7d6d9fbdd6c622476957c2a4b5`.
  Source, representation and adversarial reviewers each accepted this exact
  hash with no remaining objection. All three read-only workers have completed.
  `data/atlas/study_context/pox2019/functional_review.json` records the accepted
  scope and adjudications. Repository contracts and all 14 truth-governance
  tests pass; the existing exact claim-count assertion now includes CE-025.
  Required remote publication checks are pending at this checkpoint.

The shared consumer read is complete. The next scientific gap is functional
outcomes of actual designed variants outside this one natural-enzyme study,
subject to exact primary-source/construct/assay identity and cumulative metering.
Do not repeat the completed TKT/POX traversal or blocked M0081 trace search.

Source objections override agent agreement. Review is computational, not
independent human review or validation of the paper's hydrogen-bond hypothesis.
