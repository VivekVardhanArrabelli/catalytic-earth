# Fold-Augmented Source-Sidecar Clearance Preflight - current702

Run: 2026-06-02T17:10:46Z

Review-only source-sidecar clearance preflight for the five Lever 3 production blockers that remain after coordinate reprobe. It records primary-source active-site feature evidence and policy blockers but does not create sidecars, score heldout rows, or change thresholds.

## Status

- fold_augmented_source_sidecar_clearance_preflight_candidates_ready_review_only
- Remaining blocker rows: 5
- Source-feature sidecar candidates: 3
- Coordinate-policy blocked rows: 1
- Non-residue interaction-policy blocked rows: 1
- Source sidecars created: 0
- Deployment blockers cleared now: 0

## Row Preflight

| row | accession | coordinate | source features | status | next action |
| --- | --- | ---: | ---: | --- | --- |
| m_csa:78 | P23007 | False | 6 | blocked_predicted_coordinate_policy_required | Resolve the predicted-coordinate policy before any deployment-valid fold-channel use. |
| m_csa:204 | P10746 | True | 0 | blocked_non_residue_interaction_policy_required | Define a non-residue active-site interaction sidecar policy before trying to score this row in the combined channel. |
| m_csa:531 | P31572 | True | 3 | source_feature_sidecar_candidate_ready_for_manual_review | Draft a source-feature active-site sidecar for manual review; only after approval should it feed the combined predicted geometry/fold channel. |
| uniprot:P78549 | P78549 | True | 6 | source_feature_sidecar_candidate_ready_for_manual_review | Draft a source-feature active-site sidecar for manual review; only after approval should it feed the combined predicted geometry/fold channel. |
| uniprot:Q3LXA3 | Q3LXA3 | True | 9 | source_feature_sidecar_candidate_ready_for_manual_review | Draft a source-feature active-site sidecar for manual review; only after approval should it feed the combined predicted geometry/fold channel. |

## Candidate Feature Evidence

| row | source | feature positions |
| --- | --- | --- |
| m_csa:78 | P23007 | Active site:274, Active site:320, Active site:375, Binding site:329, Binding site:401, Binding site:421 |
| m_csa:204 | P10746 | none |
| m_csa:531 | P31572 | Active site:169, Binding site:97, Binding site:104 |
| uniprot:P78549 | P78549 | Active site:212, Site:231, Binding site:282, Binding site:289, Binding site:292, Binding site:298 |
| uniprot:Q3LXA3 | Q3LXA3 | Active site:221, Binding site:56-59, Binding site:109, Binding site:114, Binding site:401-404, Binding site:446-447, Binding site:486, Binding site:494-495, Binding site:556-558 |

## Interpretation

- Three coordinate-available blocker rows now have concrete primary-source feature evidence for manual sidecar drafting; no deployment blocker is cleared until reviewed sidecars are created and the combined channel is rebuilt.
- Draft/review source-feature sidecars for m_csa:531, uniprot:P78549, and uniprot:Q3LXA3; separately resolve the P23007 predicted-coordinate policy and the P10746 non-residue interaction-sidecar policy.
