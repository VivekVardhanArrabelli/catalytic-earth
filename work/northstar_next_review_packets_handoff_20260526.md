# North-Star Next Review Packets Handoff - 2026-05-26

This handoff converts the Wave 1 Foldseek+geometry diagnostic router into
concrete expert-review packets. It is review-only/proposal-only: no labels,
registries, ontology, fingerprints, imports, thresholds, model scaling, or
production policy changed.

## Deliverables

- `artifacts/v3_fold_conflict_oos_hard_negative_review_packet_702_20260526.json`
- `artifacts/v3_near_orphan_geometry_support_review_packet_702_20260526.json`
- `artifacts/v3_v2_sublabel_expert_review_packet_702_20260526.json`

## Packet Counts

Packet 1, fold-conflict / OOS hard-negative review:

- Rows: 18
- `keep_oos_hard_negative`: 12 rows
  - `m_csa:217`, `m_csa:428`, `m_csa:440`, `m_csa:477`, `m_csa:30`,
    `m_csa:31`, `m_csa:634`, `m_csa:651`, `m_csa:10`, `m_csa:116`,
    `m_csa:191`, `m_csa:369`
- `structure_neighbor_transfer_invalid`: 5 rows
  - `m_csa:250`, `m_csa:497`, `m_csa:517`, `m_csa:916`, `m_csa:990`
- `boundary_review_needed`: 1 row
  - `m_csa:131`

Packet 2, near-orphan geometry support review:

- Rows: 26
- `future_curated_validation_candidate`: 18 rows
  - `m_csa:163`, `m_csa:686`, `m_csa:97`, `m_csa:211`, `m_csa:750`,
    `m_csa:115`, `m_csa:159`, `m_csa:171`, `m_csa:20`, `m_csa:213`,
    `m_csa:242`, `m_csa:3`, `m_csa:321`, `m_csa:424`, `m_csa:43`,
    `m_csa:44`, `m_csa:609`, `m_csa:714`
- `review_only_signal`: 8 rows
  - `m_csa:403`, `m_csa:994`, `m_csa:497`, `m_csa:723`,
    `m_csa:250`, `m_csa:517`, `m_csa:916`, `m_csa:990`
- `acquisition_target`: 0 rows in this packet. Missing-structure rows remain
  in the router queue but are outside this near-orphan support packet.

Packet 3, v2 sublabel expert review:

- Proposal-only child labels: 25
- Candidate-summary labels: 23
- Expected candidate gaps: 2
- Readiness counts:
  - `candidate_ready_for_future_eval_design_after_expert_approval`: 9
  - `candidate_underpowered_but_named_for_review`: 3
  - `needs_expert_review_before_future_evaluation`: 12
  - `needs_expert_review_and_or_additional_curated_support_before_future_evaluation`: 1

## Exact Human / Expert Questions

1. For OOS hard negatives `m_csa:217`, `m_csa:428`, `m_csa:440`,
   `m_csa:477`, `m_csa:30`, `m_csa:31`, `m_csa:634`, `m_csa:651`,
   `m_csa:10`, `m_csa:116`, `m_csa:191`, and `m_csa:369`: do these stay
   out-of-scope hard negatives even when Foldseek or raw geometry retains a
   current-family neighbor/prediction as audit-only evidence?
2. For `m_csa:131`: is the flavin monooxygenase conflict a secondary-only
   boundary probe, a future proposal-only v2 boundary stratum, or insufficient
   evidence?
3. For primary fold-conflict geometry-rescue rows `m_csa:250`, `m_csa:497`,
   `m_csa:517`, `m_csa:916`, and `m_csa:990`: can the wrong Foldseek nearest
   train transfer be marked invalid for evaluation design after expert review?
4. For near-orphan geometry-supported candidates `m_csa:163`, `m_csa:686`,
   `m_csa:97`, `m_csa:211`, `m_csa:750`, `m_csa:115`, `m_csa:159`,
   `m_csa:171`, `m_csa:20`, `m_csa:213`, `m_csa:242`, `m_csa:3`,
   `m_csa:321`, `m_csa:424`, `m_csa:43`, `m_csa:44`, `m_csa:609`, and
   `m_csa:714`: are geometry plus selected-structure provenance sufficient
   for future curated validation after expert approval?
5. For near-orphan review-only signals `m_csa:403`, `m_csa:994`,
   `m_csa:497`, `m_csa:723`, `m_csa:250`, `m_csa:517`, `m_csa:916`, and
   `m_csa:990`: should the blocker be resolved through packet 1 fold-conflict
   review, packet 3 v2 review, or additional evidence acquisition?
6. For `metal_hydrolase.unresolved_metal_water_hydrolase` rows
   `m_csa:180`, `m_csa:403`, `m_csa:577`, `m_csa:897`, and `m_csa:994`:
   should this remain an unresolved bucket, split into named metal-water child
   mechanisms, or be excluded from future child-stratum evaluation?
7. For `ser_his_acid.unresolved_acyl_enzyme_hydrolase` rows `m_csa:599`,
   `m_csa:688`, `m_csa:723`, and `m_csa:866`: should this remain unresolved,
   split into acyl-enzyme child families, or require more source-free evidence?
8. For flavin boundary rows `m_csa:109`, `m_csa:131`, and `m_csa:551`: is a
   monooxygenase-like boundary label needed for evaluation, or should these
   remain review-only secondary/boundary context?
9. For underpowered child-family rows `m_csa:517`, `m_csa:213`, `m_csa:866`,
   plus audit-only examples `m_csa:15`, `m_csa:16`, `m_csa:258`,
   `m_csa:535`, `m_csa:158`, `m_csa:195`, `m_csa:358`, `m_csa:430`,
   `m_csa:482`, `m_csa:860`, `m_csa:937`, `m_csa:205`, `m_csa:545`,
   `m_csa:183`, and `m_csa:248`: which are real future evaluation strata and
   which need more curated support?

## Review Order

Review packet 1 first for the biggest North-Star gain. It directly decides
whether high Foldseek structural similarity transfers mechanism, must abstain
on OOS boundaries, or is invalidated by active-site geometry. Those decisions
unlock or block both near-orphan validation and v2 child-stratum use.

Packet 2 should be reviewed second to turn geometry-supported near-orphans into
future curated validation candidates, but only after fold-conflict blockers are
understood. Packet 3 should run in parallel with expert availability because
the child labels remain proposal-only and cannot be used for production or
countable evaluation without approval.

## Automatic Action Boundary

No packet can be acted on automatically later without expert input. The only
safe automatic follow-up is packaging already-reviewed outcomes into a future
explicit import/evaluation-design gate after a human decision exists. These
packets themselves do not authorize label edits, registry changes, import
decisions, threshold tuning, model scaling, or production claims.

## Orchestration Update

- 2026-05-26T07:02Z: the review-packet branch state was validated and pushed
  to `origin/main` at `2c49174`. The earlier local push blocker recorded by the
  automation is resolved. Because the packet conclusion says no row can be
  acted on automatically without expert input, the main work loop should pause
  rather than manufacture additional review-only machinery.
