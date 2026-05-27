# Packet 1 Expert Disposition - 2026-05-27

This is a review-only correction to Packet 1. It does not change labels,
fingerprints, ontology, imports, thresholds, model outputs, or production
policy.

## Core Correction

Packet 1 grouped three different evaluation objects under one
`fold-conflict / OOS hard-negative` heading. That framing should not be used
for evaluation design.

The corrected split is:

- True fold-control candidates: `m_csa:131`, `m_csa:217`, `m_csa:428`,
  `m_csa:440`, `m_csa:477`.
- Near-orphan candidates: `m_csa:250`, `m_csa:497`, `m_csa:517`,
  `m_csa:916`, `m_csa:990`.
- Neither-flag OOS abstention diagnostics: `m_csa:10`, `m_csa:30`,
  `m_csa:31`, `m_csa:116`, `m_csa:191`, `m_csa:369`, `m_csa:634`,
  `m_csa:651`.

Only `m_csa:217` is currently TM-pair verified as a fold-control hard-negative
anchor. `m_csa:428`, `m_csa:440`, and `m_csa:477` stay OOS but need TM-pair
verification before being used as verified fold-controlled eval anchors.

## Decisions

- All 12 OOS rows stay OOS.
- `m_csa:131` stays a secondary OOD probe for `flavin_monooxygenase`; it is not
  a v2 replacement question and not insufficient evidence.
- `m_csa:250`, `m_csa:517`, and `m_csa:916` are near-orphan geometry-rescue
  candidates, not fold-conflict anchors.
- `m_csa:990` is usable as a near-orphan / misleading-neighbor case with
  explicit Fe-S plus flavin cofactor caveat metadata.
- `m_csa:497` should be pulled from the test set until expert label review
  resolves whether the broad v1 `flavin_dehydrogenase_reductase` label is
  appropriate for its FMN plus di-metal nitric-oxide reductase chemistry.

## Corrected Eval Cells

| Cell | Rows | Use |
| --- | --- | --- |
| Verified fold-controlled OOS hard negative | `m_csa:217` | Primary fold-conflict metric anchor |
| Candidate fold-controlled OOS hard negatives | `m_csa:428`, `m_csa:440`, `m_csa:477` | Verify TM-pairs before use |
| OOS-as-OOS structural neighbor | `m_csa:10`, `m_csa:116`, `m_csa:191`, `m_csa:369` | Foldseek-as-router correctly transfers OOS status |
| Weak-Foldseek abstention floor | `m_csa:30`, `m_csa:31`, `m_csa:634`, `m_csa:651` | Calibration/noise diagnostic |
| Secondary flavin monooxygenase probe | `m_csa:131` | Boundary probe against flavin dehydrogenase/reductase |
| Near-orphan geometry rescue | `m_csa:250`, `m_csa:517`, `m_csa:916` | Geometry better because Foldseek has no useful neighbor |
| Near-orphan misleading neighbor | `m_csa:990` | Use with Fe-S/flavin caveat |
| Pull pending label review | `m_csa:497` | Do not use as anchor yet |

## Open Questions

1. Review `m_csa:497` label validity before any fold-conflict use.
2. Run TM-pair verification for `m_csa:428`, `m_csa:440`, and `m_csa:477`.
3. Decide whether `m_csa:990` needs a future flavin+Fe-S child stratum or only
   caveat metadata.
4. Acquire more flavin monooxygenase support before any primary-promotion
   discussion for `flavin_monooxygenase`.

