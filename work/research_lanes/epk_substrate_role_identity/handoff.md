# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T19:28:00-0500

Primary outcome: `blocker_not_cleared_biology_ambiguity`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Run note: normal `git fetch origin` failed because the sandbox could not write
the linked-worktree `FETCH_HEAD`. A subsequent `git merge --ff-only
origin/research/epk-substrate-role-identity` also failed because the sandbox
could not write linked-worktree `ORIG_HEAD`. The live remote ref was checked
with `git ls-remote`: `origin/research/epk-substrate-role-identity` was at
`ac0ffbadf6b07655c7a4bae73f8ce7c5e47d1240` before this run. The lane files
from that commit were present in the working tree, so this run continued with
the compact lane-local evidence only. Final commit
`7bdcacd6131ef98e7660fb7918fcc3f8fd07a42c` was created and pushed with a
temporary Git index because the checked-out linked-worktree metadata remained
unwritable. The live remote and local `origin/research/epk-substrate-role-identity`
ref point at that commit; local `HEAD` remains stale until the worktree Git
metadata can be updated outside this sandbox.

## What Was Tested

This run executed the requested source-free adjudication decision probe:

`epk_source_free_adjudication_requirement_decision_v1_review_only`

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_source_free_adjudication_requirement_decision_v1_20260520.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/source_free_adjudication_requirement_decision.py`

The helper reused the 54-row false-negative state/topology decision artifact.
It did not fetch structures and wrote no raw coordinates. Source labels were
used only for evaluation after source-free features had already been frozen.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, candidate-specific threshold tuning, production label
imports, and production threshold calibration.

## Evidence

Frozen 54-row decision matrix:

- `source_free_claim_gate_or_review_required_v1`: TP=14, FP=0, TN=34, FN=6.
- Positive rows: 14 source-free claimable strict/auth-terminal contexts and 6
  review-required rows.
- Counterexample rows: 1 internal-fragment no-claim row, 4 insufficient-context
  no-claim rows, and 29 review-required ambiguous or unavailable rows.
- Prior lane records checked: 6. No prior run had
  `blocker_cleared_source_free`.

Review-required positive rows:

- `9UUR`, `9UUX`: reciprocal folded-chain Tyr context. Admitting this class
  also admits `9UW4`.
- `3QHR`, `3QHW`, `1L0O`: ADP/product state with no terminal gamma-equivalent
  transfer geometry and zero near-candidate hydroxyls.
- `3TM0`: same-chain/autophosphorylation-like context; 4.483 A Ser candidate
  on the same folded chain.

Concrete blocker probes:

- `7B56`: counterexample, active-gamma-capable ANP, Ser822 at 3.921 A. The
  source-free auth-terminal/internal-fragment counterevidence rejects it because
  the acceptor is resolved as ordinal 1 while author numbering is 822.
- `9UUR`: positive, Tyr204 at 4.181 A, reciprocal active-gamma different entity,
  gamma-facing active-site-like.
- `9UUX`: positive, Tyr204 at 3.968 A, reciprocal active-gamma different entity,
  gamma-facing active-site-like.
- `9UW4`: counterexample, Tyr204 at 4.194 A, reciprocal active-gamma different
  entity, gamma-facing active-site-like.

## Interpretation

The source-free feature set can make a conservative no-false-positive claim for
14 rows, but only by abstaining on the rows that actually define the blocker.
`7B56` is locally separable by an internal-fragment/auth-terminal feature, but
that feature does not identify reciprocal folded-chain positives or same-chain
substrate-role positives.

The decisive unresolved pattern is biological role ambiguity in structure-only
evidence:

1. Product/ADP structures lack terminal gamma transfer geometry.
2. Reciprocal folded-Tyr topology is shared by positives (`9UUR`, `9UUX`) and
   a counterexample (`9UW4`).
3. Same-chain/autophosphorylation-like topology recovers `3TM0` only by
   admitting many counterexamples in the same source-free class.

Within this lane, comparable ePK substrate-role blockers have not cleared with
structure-only nearest-atom, terminal-index, reciprocal-context, local-exposure,
active-site-orientation, or state/topology proxies. The current result converts
that pattern into an explicit source-reviewed adjudication requirement rather
than another scalar feature search.

## Current Decision

Do not claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or turn the review-required classes into a
production identity rule.

Use the structure-derived features as compact review evidence only. A true
production substrate-role identity decision still requires hybrid
source-reviewed adjudication, with source evidence excluded from predictive
features.

## Exact Next Experiment

Stop source-free scalar probing unless a new source-free evidence modality is
introduced. Promote this lane result into a review requirement for product/ADP,
reciprocal folded-chain, and same-chain/autophosphorylation-like ePK
substrate-role identity cases.
