# Project State

Last refreshed: 2026-05-29

This file is the durable state summary for agents who do not have chat context.
Treat it as an orientation layer, not as a replacement for the referenced
artifacts.

Read order for a fresh run:

1. `docs/project_state.md`
2. `docs/decision_log.md`
3. `docs/artifact_index.md`
4. `docs/agent_runbook.md`

## North Star

Catalytic Earth is a mechanism-first enzyme atlas scaffold. The objective is a
computable map from sequence, structure, active-site geometry, catalytic roles,
cofactors, substrate-pocket constraints, reaction bond changes, and evolutionary
context to mechanism-level function hypotheses.

The repo is not an EC-number classifier, a wet-lab protocol, or a production
biological design system. Current benchmark claims must be framed as local,
artifact-backed mechanism diagnostics.

## Current Benchmark State

- Current label surface: 702 curated labels in the current sequence-NN manifest,
  with 562 in-distribution rows and 140 heldout rows.
- Current v1 primary mechanism targets: `ser_his_acid_hydrolase`,
  `metal_dependent_hydrolase`, `plp_dependent_enzyme`,
  `flavin_dehydrogenase_reductase`, and `heme_peroxidase_oxidase`.
- Secondary OOD probe fingerprints: `radical_sam_enzyme`,
  `cobalamin_radical_rearrangement`, and `flavin_monooxygenase`.
- The 2026-05-25 sequence manifest predates the later canonical `m_csa:497` and
  `m_csa:750` OOS revisions. Use the Wave 1 readthrough masks when reading
  Wave 1 artifacts that still carry those rows as primary flavin labels.
- Current Wave 1.2 standardized heldout readout:
  - canonical mask: 45 primary rows, 92 pure OOS rows, 3 secondary-probe rows;
  - Wave 1 readthrough mask after excluding `m_csa:497` and `m_csa:750` from
    primary metrics: 43 primary rows and 97 nonprimary/OOS rows.

When a report predates 2026-05-27 row-level revisions, do not copy its primary
flavin counts directly. Check the decision log and the row-level revision
artifacts first.

## Trusted Results

- Geometry re-export removed the prior join confound. The current Wave 1.2 audit
  joins 140/140 standardized heldout rows, recovers the five rows missed by the
  older preview geometry eval (`m_csa:577`, `m_csa:599`, `m_csa:710`,
  `m_csa:892`, and `m_csa:897`), and reports 45/45 canonical primary accuracy
  with 0/92 pure-OOS false positives under the existing 0.4115 geometry
  abstention threshold.
- Hand-scored active-site geometry remains the current first router. The
  geometry-feature logistic probe is useful but weaker on the audit: 66.7%
  canonical primary accuracy and 4.2% OOS/secondary false-positive rate.
- The clean experimental-coordinate geometry result is not deployment-ready by
  itself. The AlphaFoldDB predicted-geometry audit drops the hand router from
  45/45 to 23/45 primary heldout correct, with 17 primary abstentions, 5 wrong
  non-abstained primary calls, and a 12.3% OOS/secondary false-positive rate.
  This makes robustness to predicted active-site geometry degradation a learned
  model job description, not a raw clean-M-CSA accuracy contest.
- A real AlphaFoldDB-predicted structure Foldseek channel is now scored for all
  126 heldout rows with ok predicted geometry against the predicted
  in-distribution atlas. The standalone nearest-atlas TM signal separates
  in-scope from all OOS at AUC 0.814301; a no-fit mean of predicted geometry
  confidence and fold TM reaches AUC 0.907622 overall and 0.911348 on the six
  cofactor-confounded OOS rows. These are diagnostics, not production thresholds.
- Learned-representation results are diagnostic, not decision-grade. ESM-2
  logistic is the strongest local learned comparator in the Wave 1.2 table but
  does not displace geometry. ESM-C logistic versus ESM-C cosine shows decoder
  choice is a real confound.
- ProtT5 and SaProt have only NN/cosine-style local standardized exports today.
  Matched logistic-head reruns are blocked until raw local sidecars or weights
  exist; do not download large models for this by default.
- FMO remains secondary-only. Local FMO rows and external candidates are useful
  review/acquisition evidence, but no canonical primary promotion, registry
  change, threshold change, production scorer change, or import is authorized.

## Active Blockers

- Fair ProtT5/SaProt logistic-head comparison needs local raw embedding or
  structure-token sidecars and an ESM-2-style train/cal-only head. Existing
  local exports are not equivalent decoders.
- Sequence-to-deployment geometry is blocked by predicted-structure active-site
  degradation: AlphaFoldDB has no proximal ligands and perturbs the hand
  geometry evidence enough to introduce primary wrong calls and OOS false
  positives. ESMFold is not locally available without staging runtime/weights.
- FMO primary promotion is blocked by missing or unsuitable exact coordinate
  materialization for key external subtype rows, subtype/child-stratum
  definition work, PHBH-leaning gate behavior, hard-negative separation, and
  expert review.
- `m_csa:497` and `m_csa:750` must not be used as primary flavin support in old
  Wave 1 cells. They are OOS/boundary negatives under the current registry.
- Review surfaces are not labels. AI-visual review packets, PyMOL queues, FMO
  scouts, and external packets are review-only until a dedicated import preview,
  label-factory gate, and batch acceptance authorize counting.
- Disk must stay above 10 GiB free. Avoid large downloads and broad artifact
  regeneration unless the task explicitly asks for them.

## Next Gates

1. Promote the fold-augmented abstention diagnostic into a leakage-safe
   train/cal/heldout thresholding contract; keep the current heldout operating
   points non-production until then.
2. If representation work resumes, produce row-aligned local sidecars first,
   then train heads on train/cal rows only and evaluate heldout once, including
   a predicted-geometry robustness cell.
3. For FMO, revise the review/silver evidence gate into subtype panels, finish
   coordinate/materialization blockers, and keep candidate rows review-only.
4. For label growth, require explicit expert decision, no-import safety checks
   where applicable, label-factory gate pass, batch acceptance, and registry
   summary refresh before any countable import.

## Maintenance Notes

- Keep this file short enough to scan. Put detailed historical reasoning in the
  decision log or the specific artifact report.
- Refresh this file only when the current gate, trusted result set, blockers, or
  source-of-truth order changes.
- If a run only validates existing outputs, update automation memory rather than
  inflating this file.

## Primary References

- `artifacts/v3_wave1_2_decoder_join_confound_audit_702_20260528.json`
- `work/wave1_2_decoder_join_confound_audit_702_20260528.md`
- `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`
- `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
- `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`
- `artifacts/v3_m_csa497_label_revision_702_20260527.json`
- `artifacts/v3_m_csa750_label_revision_702_20260527.json`
- `artifacts/v3_fmo_fingerprint_definition_audit_702_20260528.json`
- `artifacts/v3_fmo_local_candidate_adjudication_551_973_702_20260528.json`
