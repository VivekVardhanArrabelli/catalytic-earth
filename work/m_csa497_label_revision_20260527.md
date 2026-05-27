# m_csa:497 Label Revision - 2026-05-27

## Decision

Relabel `m_csa:497` from `seed_fingerprint::flavin_dehydrogenase_reductase`
to `out_of_scope`.

## Rationale

The expert mechanism-locus review concluded that `m_csa:497` is a
flavodiiron nitric oxide reductase. The catalytic chemistry is NO reduction at
a non-heme Fe(II)Fe(II) carboxylate-bridged center. FMNH2 donates electrons to
the di-iron nitrosyl complex, but it is not the catalytic flavin
hydride-transfer locus represented by the v1
`flavin_dehydrogenase_reductase` fingerprint.

## Effects

- Total canonical labels remain `702`.
- Seed-fingerprint labels decrease by `1`.
- Out-of-scope labels increase by `1`.
- `flavin_dehydrogenase_reductase` support decreases by `1`.
- No ontology ids, thresholds, imports, external labels, model outputs, or
  production registries changed.
- Wave 1 primary metrics should exclude `m_csa:497`; OOS/boundary diagnostics
  may keep it as a flavin-cofactor leakage negative.

## Artifacts

- `artifacts/v3_m_csa497_label_revision_702_20260527.json`
- `artifacts/v3_m_csa497_wave1_metric_impact_702_20260527.json`
- Source review: `artifacts/v3_packet1_tm_and_497_expert_disposition_702_20260527.json`

## Wave 1 Metric Effect

Existing standardized Wave 1 heldout predictions were re-scored without
retraining. `m_csa:497` was previously wrong for every track as a primary
flavin row. After the relabel, primary accuracy increases slightly for every
track. It becomes an OOS false positive only for tracks that predicted
`metal_dependent_hydrolase` rather than abstaining.
