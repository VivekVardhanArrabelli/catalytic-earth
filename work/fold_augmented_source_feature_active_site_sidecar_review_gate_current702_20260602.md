# Fold-Augmented Source-Feature Active-Site Sidecar Review Gate - current702

Run: 2026-06-02T22:07:13Z

Review-only approval gate for the Lever 3 source-feature active-site sidecar candidates. It composes the draft candidate packet, strict audit, and remaining-blocker decision matrix into explicit per-row approval decisions without approving, copying, scoring, or changing thresholds.

## Status

- fold_augmented_source_feature_active_site_sidecar_review_gate_ready_review_only
- Candidate sidecar rows: 3
- Manual approval review-ready rows: 3
- Manual approval decisions required: 3
- Strict-audit blocked rows: 0
- Approved rows: 0
- Copy authorized now: 0
- Ready for predicted-geometry scoring now: 0
- Deployment blockers cleared now: 0
- Source-feature support rows: 18

## Review Gate Rows

| row | accession | features | strict audit | review ready | decision required | blocked actions |
| --- | --- | ---: | --- | ---: | ---: | --- |
| m_csa:531 | P31572 | 3 | passed | True | True | copy_candidate_sidecar_to_scoring_surface, rerun_combined_geometry_fold_channel, claim_deployment_blocker_cleared |
| uniprot:P78549 | P78549 | 6 | passed | True | True | copy_candidate_sidecar_to_scoring_surface, rerun_combined_geometry_fold_channel, claim_deployment_blocker_cleared |
| uniprot:Q3LXA3 | Q3LXA3 | 9 | passed | True | True | copy_candidate_sidecar_to_scoring_surface, rerun_combined_geometry_fold_channel, claim_deployment_blocker_cleared |

## Non-Sidecar Policy Rows

| row | accession | decision class | authorized | next action |
| --- | --- | --- | ---: | --- |
| m_csa:78 | P23007 | alternate_accession_coordinate_policy_review | False | If an alternate is authorized, fetch its AFDB coordinate and rerun the fold channel without changing thresholds. |
| m_csa:204 | P10746 | non_residue_interaction_sidecar_policy_design | False | Do not force a residue sidecar; either define an explicit interaction-sidecar policy or keep the row fold-only. |

## Interpretation

- The three draft source-feature sidecar candidates are strict-audit clean and ready for manual approval review; none is approved, copied, scoring-ready, or deployment-clearing.
- Approve, reject, or request rewrites for m_csa:531, uniprot:P78549, and uniprot:Q3LXA3 before rerunning the combined predicted-geometry/fold channel.
