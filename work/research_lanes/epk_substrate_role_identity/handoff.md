# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T21:33:02-0500

Primary outcome: `counterexample_found`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. The linked-worktree metadata remains
stale/unwritable, so the final push uses the lane's temporary-index workaround
rather than updating local `HEAD`.

## What Was Tested

This run introduced a new source-free evidence modality:

`epk_sequence_context_probe_v1_review_only`

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_sequence_context_probe_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/sequence_context_probe.py`

The helper reused the frozen 54-row state/topology diagnostic set and fetched
PDB coordinate text in memory only. It wrote compact reduced evidence around
the selected candidate hydroxyl residue: resolved polymer sequence windows
from -5..+5 and -3..+3, plus-one/plus-two Pro indicators, upstream/downstream
basic counts, acidic/hydrophobic/polar counts, and generic residue-chemistry
support classes. It did not write raw coordinate dumps.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, candidate-specific threshold tuning, production label
imports, and production threshold calibration.

## Evidence

Frozen 54-row decision matrix:

- Prior conservative source-free claim gate reused: TP=14, FP=0, TN=34, FN=6.
- Sequence-context reciprocal folded-Tyr rescue: TP=16, FP=1, TN=33, FN=4.
- Sequence-context ambiguous reciprocal-or-same-chain rescue: TP=17, FP=15,
  TN=19, FN=3.
- Proline-directed ambiguous rescue: TP=15, FP=1, TN=33, FN=5.
- Charged-context ambiguous rescue: TP=17, FP=14, TN=20, FN=3.

Decisive reciprocal folded-Tyr counterexample:

- `9UUR`: positive, selected Tyr204, window `GFLTEYVATRW`, support class
  `tyr_adjacent_pro_or_charged_context`.
- `9UUX`: positive, selected Tyr204, window `TGFLEYVATRW`, support class
  `tyr_adjacent_pro_or_charged_context`.
- `9UW4`: counterexample, selected Tyr204, window `GFLTEYVATRW`, support
  class `tyr_adjacent_pro_or_charged_context`.

Exact-window collision:

- `GFLTEYVATRW` contains both positive `9UUR` and counterexample `9UW4`.

Thus the sequence-context rule that recovers `9UUR` and `9UUX` also admits
`9UW4`. A stricter proline-only rule avoids the reciprocal Tyr false positive
but loses both reciprocal Tyr positives and still admits same-chain
counterexample `1OJ4`.

Same-chain stress remains unresolved. Broad ambiguous sequence-context rescue
recovers `3TM0` but admits 15 counterexamples:

`2JJ2`, `7ZE5`, `9UW4`, `5C1O`, `6U1D`, `5TT6`, `7ZDU`, `9L3M`, `7T55`,
`7T57`, `9L3U`, `8W2H`, `8W2J`, `9OAN`, `1OJ4`.

Product/ADP rows remain unavailable to terminal-gamma transfer geometry:
`3QHR`, `3QHW`, and `1L0O` stay false negatives under sequence-context rescue
rules.

`7B56` remains rejected by prior auth-terminal/internal-fragment
counterevidence. Its selected Ser822 sequence window has no generic
sequence-context signal, so sequence context is not the feature that repairs
or generalizes the `7B56` blocker.

## Interpretation

Sequence context is useful compact review evidence, but it is not a
source-free substrate-role identity rule. The hard blocker remains biological
role ambiguity in structure-derived evidence:

1. Exact or generic acceptor sequence context can be shared by a true substrate
   positive and a counterexample (`9UUR`/`9UW4`).
2. Product/ADP structures lack terminal gamma transfer geometry.
3. Same-chain/autophosphorylation-like topology recovers `3TM0` only by
   admitting many counterexamples in the same source-free class.

Within this lane, comparable blockers have now failed to clear with
nearest-atom, terminal-index, reciprocal-context, local-exposure,
active-site-orientation, state/topology, abstention-gate, coordinate-
certainty/ordering, and sequence-context features.

## Current Decision

Do not claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or turn sequence context into a production
identity rule.

Use sequence context only as review-only evidence. A true production
substrate-role identity decision still requires hybrid source-reviewed
adjudication, with source evidence excluded from predictive features.

## Exact Next Experiment

Do not add another scalar source-free probe unless a genuinely new evidence
modality is available. Preserve product/ADP, reciprocal folded-chain, and
same-chain/autophosphorylation-like cases as source-reviewed adjudication
requirements rather than production source-free claims.
