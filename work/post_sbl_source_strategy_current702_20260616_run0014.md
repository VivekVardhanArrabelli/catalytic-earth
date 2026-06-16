# Post-SBL Source Strategy - 2026-06-16 run0014

This is a non-destructive strategy note. It writes no labels and does not authorize a second
same-run registry mutation.

## Post-Apply State

- Frozen current702 sha: `5eec9bef56baed7f68a82daa3b3dbc854fcf88f91c915ff5b48a42050c272505`.
- Current positive universe: `label_factory_v1_46fp` with 46 fingerprints and 43 ontology families.
- External registry: 7926 rows = 6702 seed + 1224 OOS, with 30 silver-tier rows.
- Combined label surface: 8628 rows; combined seed surface: 6932.
- Honest counters: positive_bronze 6885, oos_bronze 1696, silver_confirmed 47, projected 0.

## SBL Outcome

The `serine_beta_lactamase` tier-2 active-site/reaction lane was applied through the explicit
reuse-preview path. It fetched 240 rows, produced 115 mechanism-corroborated bronze labels, admitted
106 novelty-safe rows, held 0 off-target fingerprint matches, and found 0 row-guardrail problems.
The family now has 106 combined labels and reaches the 100 floor.

Do not source more SBL without a new reaction-diversity split. The post-apply coverage audit marks
`serine_beta_lactamase` reaction-saturated because the admitted batch is concentrated in one
reaction surface.

## Follow-Up Scouts

- Coverage: `artifacts/v3_coverage_redundancy_audit_current702_20260616_run0014_post_sbl_apply.json`
  reports 8628 combined labels, Gini 0.1948, `metal_independent_phosphodiesterase` as the only
  hole, floor deficit 100, and `metal_dependent_hydrolase` over cap.
- Novelty replay:
  `artifacts/v3_novelty_admission_gate_audit_current702_20260616_run0014_post_sbl_apply.json`
  reports 7465 admit / 414 throttle / 47 reject across 7926 expansion rows, with 461 rows that
  would not readmit.
- Factory:
  `artifacts/v3_high_yield_family_lane_factory_current702_20260616_run0014_post_sbl_apply.json`
  reports 0 ready existing lanes with >=150 projected clean admits; top current-handle clean supply
  is 77.
- Evidence-handle expansion:
  `artifacts/v3_evidence_handle_expansion_current702_20260616_run0014_post_sbl_apply.json`
  still finds 741 capped reachable positive-bronze uplift across handle-blocked families, but this
  is source-wall headroom in balanced/capped families, not apply authority.
- Breadth feasibility:
  `artifacts/v3_breadth_feasibility_scout_current702_20260616_run0014_post_sbl_apply.json`
  reports reviewed Swiss-Prot alone is not enough for 10k diverse positive bronze: clean-only
  projection is 9573, leaving a 427-positive gap before further diversity discounts.

## Next Exact Action

The next safe scaling action is still the `metal_independent_phosphodiesterase` hole, but only with
a sharper mechanism-bearing source wall that can plausibly close the 100 floor. Do not retry broad
PDE EC/name handles, the 7-row PLD preview, or terpene window170. If PDE remains blocked, move to a
source-tier expansion strategy beyond reviewed Swiss-Prot through a count scout, preregistration if
the fingerprint universe changes, non-destructive preview, row guardrail audit,
novelty/governor/dedup/cap replay, and leakage/source-contract tests before any apply.
