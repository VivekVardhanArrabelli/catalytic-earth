# Packet 1 / Wave 1 Closure Cycle - 2026-05-27

This cycle closed the six-row review ambiguity without changing ontology IDs,
fingerprint definitions, thresholds, production scoring, model outputs, imports,
or artifact migration state.

## Decisions

- `m_csa:217` and `m_csa:477` remain verified fold-conflict OOS anchors.
- `m_csa:428` remains a caveated partial fold-conflict row.
- `m_csa:440` remains a near-orphan OOS abstention diagnostic.
- `m_csa:497` remains excluded from primary flavin metrics after its prior OOS
  relabel.
- `m_csa:750` is now canonically `out_of_scope`, with the prior
  automation-curated label-factory review preserved in evidence. The closure
  reason is radical FAD semiquinone plus catalytic Fe-S dehydration, not ordinary
  v1 flavin hydride-transfer dehydrogenase/reductase chemistry.
- `m_csa:43` remains a valid metal-dependent hydrolase canary, but the
  top-foldseek-success / learned-failure canary set is underpowered after
  removing `m_csa:750`.
- Foldseek coordinate readiness completed with 692 staged current702 Wave 1
  structures, but the direct 5,000-row TM-pair retention run did not return a
  result artifact in this cycle. Fold-neighborhood claims for `m_csa:217`,
  `m_csa:477`, `m_csa:428`, and `m_csa:440` remain capped by the prior 200-row
  retention until the bounded retry or chunked fallback completes.

## TM-Pair Expansion Follow-Up

The chunked fallback completed for the four Packet 1 heldout rows and is
recorded in
`artifacts/v3_wave1_tm_pair_signal_expansion_result_702_20260527.json`.
The fallback retained 2,971 targeted heldout-vs-train pair rows under a
5,000-row reporting cap, so the old 200-row retention ceiling no longer caps
the `m_csa:217`, `m_csa:477`, `m_csa:428`, or `m_csa:440` claims.

Current readout:

- `m_csa:217`: fully supported verified fold-conflict OOS anchor.
- `m_csa:477`: fully supported verified fold-conflict OOS anchor.
- `m_csa:428`: caveated TIM-barrel/incidental-primary-hit case; high-TM
  neighbors are mostly OOS rows with only incidental primary hits.
- `m_csa:440`: fully supported as near-orphan OOS/router-abstention, not a
  fold-conflict row.

The result is review-only evaluation evidence. It does not complete the full
692-query all-materializable all-vs-all TM-score run and does not change labels,
ontology IDs, fingerprints, imports, thresholds, production scoring, model
outputs, representation artifacts, or artifact migration state.

## Acquisition State

FMO acquisition now has two canonical rows (`m_csa:131`, `m_csa:132`) plus two
clean local secondary/future candidates (`m_csa:551`, `m_csa:973`). That gives
four clean acquisition signals and leaves two more clean rows needed before any
primary-promotion reconsideration; hard-negative separation evidence is still
missing.

## Main Artifacts

- `artifacts/v3_packet1_wave1_decision_closure_702_20260527.json`
- `artifacts/v3_m_csa750_label_revision_702_20260527.json`
- `artifacts/v3_m_csa750_wave1_metric_canary_impact_702_20260527.json`
- `artifacts/v3_label_factory_review_import_mechanism_mismatch_close_read_702_20260527.json`
- `artifacts/v3_flavin_monooxygenase_acquisition_closure_702_20260527.json`
- `artifacts/v3_m_csa43_wave1_canary_closure_702_20260527.json`
- `artifacts/v3_foldseek_coordinate_readiness_1000_current702_wave1_20260527.json`
- `artifacts/v3_wave1_tm_pair_signal_expansion_blocker_702_20260527.json`
