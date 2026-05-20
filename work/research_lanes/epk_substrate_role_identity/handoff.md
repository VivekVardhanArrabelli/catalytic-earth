# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T18:28:19-0500

Primary outcome: `blocker_not_cleared_biology_ambiguity`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Run note: normal `git fetch origin` was attempted at run start, but the
sandbox could not write the linked-worktree `FETCH_HEAD`. The live remote ref
was checked with `git ls-remote`: `origin/research/epk-substrate-role-identity`
was at `c77e6a81431002acc9039a95924585ab009d78b7`. Local `HEAD` remained one
commit behind because the linked worktree ref could not be advanced, but the
working tree already contained the pushed lane content from that commit.

## What Was Tested

This run executed the requested false-negative decision probe:

`epk_false_negative_state_topology_decision_probe_v1_review_only`

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_false_negative_state_topology_decision_probe_v1_20260520.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/false_negative_state_topology_decision_probe.py`

The helper reused the 54-row active-site orientation artifact and added compact
source-free state/topology classes only. It did not fetch or write raw
coordinates.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, candidate-specific threshold tuning, production label
imports, and production threshold calibration.

## Evidence

Frozen 54-row diagnostic set:

- `strict_auth_terminal_guard_v1_reused`: TP=14, FP=0, TN=34, FN=6.
- `reciprocal_folded_tyr_admitted_v1_reused`: TP=16, FP=1, TN=33, FN=4.
- `orientation_supported_folded_tyr_v1_reused`: TP=16, FP=1, TN=33, FN=4.
- `auth_or_same_chain_candidate_5a_probe`: TP=17, FP=15, TN=19, FN=3.
- `auth_or_same_chain_candidate_6a_probe`: TP=17, FP=26, TN=8, FN=3.

Availability summary by evaluation label:

- Positives: 14 claimable by auth-guard strict context, 2 ambiguous reciprocal
  folded-Tyr, 1 ambiguous same-chain/autophosphorylation-like, and 3
  product/ADP rows with no terminal gamma-equivalent geometry.
- Counterexamples: 25 same-chain/autophosphorylation-like ambiguous rows, 1
  reciprocal folded-Tyr counterexample (`9UW4`), 1 internal-fragment mimic
  (`7B56`), and several no-claim or gamma-unavailable rows.

Strict/auth false-negative classes:

- `9UUR`, `9UUX`: reciprocal folded-chain topology ambiguity. They can be
  recovered by folded-Tyr reciprocal/context orientation rules, but that same
  class admits `9UW4`.
- `3QHR`, `3QHW`, `1L0O`: product/ADP state with no resolved terminal
  gamma-equivalent atom and zero candidate hydroxyls within 8 A.
- `3TM0`: active-gamma-capable ANP state, but the only near candidate is
  same-chain, folded-chain, same-sequence-entity, and
  autophosphorylation-like.

Remaining false negatives under the orientation-supported folded-Tyr rule:

- `3QHR`, `3QHW`, `1L0O`: missing terminal gamma-equivalent/product-state
  geometry.
- `3TM0`: same-chain/autophosphorylation-like topology.

Same-chain stress result:

- A 5 A same-chain rescue recovers `3TM0` at row level but admits 15
  counterexamples, including `9UW4`.
- A 6 A same-chain rescue admits 26 counterexamples and collapses toward
  permissive nearest-hydroxyl behavior.

## Interpretation

The blocker is no longer just a missing scalar feature. The remaining cases
split into three source-free ambiguity classes:

1. Product/ADP rows where the structure lacks terminal gamma transfer geometry.
2. Reciprocal folded-chain Tyr context where true positives and `9UW4` share
   the same accepted source-free class.
3. Same-chain/autophosphorylation-like topology where admitting near hydroxyls
   floods the set with false positives.

Within this lane, comparable ePK substrate-role blockers have not cleared with
structure-only nearest-atom, terminal-index, reciprocal-context, local-exposure,
active-site-orientation, or state/topology proxies. Source-free features are
useful for compact review triage, but they do not establish production
substrate-role identity.

## Current Decision

Do not claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or turn these review-only classes into a
production rule.

Stop broad scalar feature probing unless a new source-free evidence modality is
introduced. Preserve a source-reviewed adjudication requirement for ePK
substrate-role identity, especially for product/ADP, reciprocal folded-chain,
and same-chain/autophosphorylation-like cases.

## Exact Next Experiment

Convert the lane result into a source-reviewed adjudication requirement:
product/ADP rows, reciprocal folded-chain contexts, and
same-chain/autophosphorylation-like contexts should remain review-only blockers
unless a new source-free modality is introduced. Do not tune production
thresholds from this lane.
