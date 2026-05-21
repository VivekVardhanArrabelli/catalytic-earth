# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T22:32:29-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 48.8 minutes (`2026-05-21T02:43:33Z` to
`2026-05-21T03:32:21Z`).

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. The local linked-worktree `HEAD`
remains stale relative to `origin/research/epk-substrate-role-identity`, so
the final commit path should use the lane's temporary-index workaround rather
than relying on a normal local fast-forward.

## What Was Emitted

This run introduced candidate-level source-free evidence rows rather than
another scalar rescue rule.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/candidate_evidence_rows.py`

The helper reused the frozen 54-row orientation diagnostic set and emitted:

- 204 gamma/acceptor candidate-pair rows.
- 7 state-only rows where no materialized gamma/acceptor pair exists.
- 0 duplicate candidate IDs.

Candidate IDs are of the form:

`PDB|gamma=<chain>:<ligand><auth_seq>:<atom>|acceptor=<chain>:<residue><auth_seq>:<atom>`

The artifact separates source-free coordinate evidence from review/source
context:

- `source_free_evidence` holds ligand state, coordinate state, distance,
  topology, auth-terminal/internal-fragment evidence, reciprocal context,
  local exposure, active-site orientation, coordinate certainty, and blocker
  class.
- `review_context_for_evaluation_only` holds evaluation labels/groups. These
  labels were not used to construct predictive features.

Coordinates were fetched in memory only for compact occupancy, altloc, and
B-factor certainty metrics. No raw coordinate dumps were written.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, candidate-specific threshold tuning, production label
imports, and production threshold calibration.

## Evidence Summary

Coordinate states observed:

- Candidate-pair rows: `active_gamma=204`.
- State-only rows: `active_gamma=1`, `adp_state=3`,
  `ambiguous_coordinate_state=1`, `ligand_absent=2`.

Combined blocker counts:

- `topology_ambiguity=109`
- `active_gamma_geometry=72`
- `none=19`
- `substrate_role_identity=4`
- `product_state_evidence=3`
- `ligand_materialization=3`
- `internal_fragment_mimicry=1`

Coordinate certainty for candidate-pair rows:

- `ordered_like=156`
- `high_b_or_context_disordered=41`
- `coordinate_ambiguous_or_partial=7`

Hard-case rows preserve the current blocker interpretation:

- `7B56`: active-gamma candidate remains `internal_fragment_mimicry`
  for `7B56|gamma=B:ANP401:PG|acceptor=A:SER822:OG`.
- `9UUR`, `9UUX`, `9UW4`: reciprocal folded-chain Tyr candidates remain
  `topology_ambiguity`, and all are ordered-like by generic coordinate
  certainty.
- `3QHR`, `3QHW`, `1L0O`: `adp_state` state-only rows with
  `product_state_evidence`, not active-gamma false negatives.
- `3TM0`: same-chain active-gamma candidate remains `topology_ambiguity`.
- `1QHA`: active-gamma state-only row with no near hydroxyl candidate,
  classified as `active_gamma_geometry`.

## Interpretation

The candidate evidence table is review-support infrastructure, not a
production substrate-role identity rule. It makes the source-free evidence
explicit at candidate granularity while preserving the known blocker:
structure-derived distance, orientation, exposure, coordinate certainty,
auth-terminal/internal-fragment, and reciprocal context still do not resolve
biological substrate role for product/ADP, reciprocal folded-chain, or
same-chain/autophosphorylation-like rows.

Do not claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or promote the candidate no-blocker sanity
flag into a production identity rule.

## Exact Next Experiment

Use `epk_candidate_evidence_v1_20260521.json` for review triage and blocker
reporting. Do not add more scalar source-free probes unless a genuinely new
evidence modality is available. Preserve product/ADP, reciprocal folded-chain,
and same-chain/autophosphorylation-like cases as source-reviewed adjudication
requirements.
