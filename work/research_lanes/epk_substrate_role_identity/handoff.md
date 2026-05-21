# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T20:30:43-0500

Primary outcome: `counterexample_found`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded, and the lane files in the working tree
were byte-matched against `origin/research/epk-substrate-role-identity` before
new work. The linked-worktree metadata remains stale/unwritable, so final push
uses the lane's temporary-index workaround rather than updating local `HEAD`.

## What Was Tested

This run introduced a new source-free evidence modality:

`epk_coordinate_certainty_probe_v1_review_only`

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_coordinate_certainty_probe_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/coordinate_certainty_probe.py`

The helper reused the frozen 54-row state/topology diagnostic set and fetched
PDB coordinate text in memory only. It wrote compact reduced evidence for the
already-selected hydroxyl/gamma atom pair: occupancy, alternate-location count,
B-factor, and relative B-factor ratios versus same-chain, local 8 A, and global
protein contexts. It did not write raw coordinate dumps.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, candidate-specific threshold tuning, production label
imports, and production threshold calibration.

## Evidence

Frozen 54-row decision matrix:

- Prior conservative source-free claim gate reused: TP=14, FP=0, TN=34, FN=6.
- Coordinate-ordered claim gate: TP=9, FP=0, TN=34, FN=11.
- Coordinate-ordered reciprocal folded-Tyr rescue: TP=16, FP=1, TN=33, FN=4.
- Coordinate-ordered reciprocal-or-same-chain rescue: TP=17, FP=18, TN=16,
  FN=3.

Hard reciprocal folded-Tyr trio:

- `9UUR`: positive, ordered-like, full occupancy, no altloc; acceptor
  B/same-chain median ratio 1.045, local 8 A ratio 1.139, gamma/protein ratio
  1.300.
- `9UUX`: positive, ordered-like, full occupancy, no altloc; acceptor
  B/same-chain median ratio 0.981, local 8 A ratio 1.179, gamma/protein ratio
  1.307.
- `9UW4`: counterexample, ordered-like, full occupancy, no altloc; acceptor
  B/same-chain median ratio 0.982, local 8 A ratio 1.150, gamma/protein ratio
  1.264.

Decisive result: the same generic coordinate-ordered class that recovers
`9UUR` and `9UUX` also admits `9UW4`. Coordinate certainty therefore does not
separate the biological substrate role in the hard reciprocal folded-chain
case.

Same-chain stress result: admitting ordered same-chain/autophosphorylation-like
rows recovers `3TM0`, but also admits 18 counterexamples:

`2JJ2`, `7ZE5`, `9UW4`, `6U1D`, `6U1E`, `5TT6`, `6NOO`, `9NBW`, `7ZDT`,
`7ZDU`, `9L3M`, `7T55`, `7T57`, `5XD6`, `8W2H`, `8W2J`, `1TFW`, `2DRA`.

Product/ADP rows remain unavailable to terminal-gamma transfer geometry:
`3QHR`, `3QHW`, and `1L0O` stay false negatives under coordinate-ordered
rescue rules.

`7B56` remains locally rejected by the auth-terminal/internal-fragment
counterevidence. It is also coordinate-ordered, so coordinate certainty is not
the feature that separates it.

## Interpretation

Coordinate certainty is useful compact review evidence, but it is not a
source-free substrate-role identity rule. The hard blocker is still biological
role ambiguity in structure-only evidence:

1. Product/ADP structures lack terminal gamma transfer geometry.
2. Reciprocal folded-Tyr topology is shared by true positives (`9UUR`, `9UUX`)
   and the counterexample `9UW4`.
3. Same-chain/autophosphorylation-like topology recovers `3TM0` only by
   admitting many counterexamples in the same source-free class.

Within this lane, comparable blockers have now failed to clear with
nearest-atom, terminal-index, reciprocal-context, local-exposure,
active-site-orientation, state/topology, abstention-gate, and coordinate-
certainty/ordering features.

## Current Decision

Do not claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or turn coordinate certainty into a
production identity rule.

Use coordinate certainty only as review-only evidence. A true production
substrate-role identity decision still requires hybrid source-reviewed
adjudication, with source evidence excluded from predictive features.

## Exact Next Experiment

Stop source-free scalar/coordinate probing unless a genuinely new evidence
modality is introduced. Preserve product/ADP, reciprocal folded-chain, and
same-chain/autophosphorylation-like cases as source-reviewed adjudication
requirements rather than production source-free claims.
