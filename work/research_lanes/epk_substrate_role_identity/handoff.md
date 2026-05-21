# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T09:09:12-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 48.88 minutes (`2026-05-21T13:20:19Z` to
`2026-05-21T14:09:12Z`).

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Normal local `HEAD` remains stale
relative to `origin/research/epk-substrate-role-identity`; commit/push used
the same remote-tip temporary-index workaround as the prior runs.

## What Was Emitted

This run added one compact source-free feature family: metal cofactor
materialization plus reduced gamma-phosphate transfer geometry.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_gamma_metal_transfer_geometry_probe_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/gamma_metal_transfer_geometry_probe.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`

The helper reused:

- 204 candidate gamma/acceptor rows.
- 7 state-only rows.
- 54 diagnostic PDBs.

It emitted:

- 204 candidate metal/transfer-geometry rows.
- 7 state-only pass-through rows.
- 4 review-only sanity/stress rule evaluations.

No raw coordinate files were written. The artifact is under 1 MiB and stores
only compact reduced distances, shell classes, bridge-angle classes, and
candidate identifiers. Review labels remain under evaluation-only context.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, and candidate-specific threshold tuning.

## Evidence Summary

Metal-adjusted coordinate states for candidate-pair rows:

- `active_gamma=186`
- `metal_absent=18`

Source candidate-pair coordinate state before overlay:

- `active_gamma=204`

State-only rows remained:

- `active_gamma=1`
- `adp_state=3`
- `ambiguous_coordinate_state=1`
- `ligand_absent=2`

Metal shell classes:

- `direct_metal_shell_le_4a=161`
- `loose_metal_shell_4_to_8a=25`
- `no_metal_atoms_model1=8`
- `no_metal_within_8a=10`

Gamma bridge-angle classes:

- `inline_like_ge_150=22`
- `partial_inline_120_to_150=38`
- `oblique_80_to_120=63`
- `not_inline_lt_80=81`

The conservative metal-adjusted PDB no-blocker sanity flag remained zero-FP:

- TP=13
- FP=0
- TN=34
- FN=7

False negatives were `1L0O`, `3QHR`, `3QHW`, `3TM0`, `6Z3R`, `9UUR`,
and `9UUX`.

## Decisive Result

The reciprocal Tyr hard trio did not separate source-free:

- `9UUR|gamma=A:ANP501:PG|acceptor=B:TYR204:OH`
- `9UUX|gamma=A:ANP501:PG|acceptor=B:TYR204:OH`
- `9UW4|gamma=A:ANP501:PG|acceptor=B:TYR204:OH`

All three reciprocal Tyr candidates are `metal_absent` under the broad 8 A
gamma shell and have `oblique_80_to_120` bridge-angle classes. This does not
recover the positives without also preserving the `9UW4` counterexample
pressure.

The same-chain transfer-geometry stress rule is unsafe. It recovers some
topology positives but admits these counterexamples:

- `3FGU`
- `5XD6`
- `6U1D`
- `6U1E`
- `9OAN`
- `9UW4`

That stress result is the decisive blocker: metal-supported same-chain
transfer geometry is shared by positives and counterexamples, so it cannot be
promoted to source-free substrate-role identity.

## Interpretation

The blocker is not cleared source-free. Metal/cofactor materialization is useful
coordinate-state review evidence and makes `metal_absent` first-class for
candidate rows, but it does not assign biological substrate role. Product/ADP
rows remain state-specific review-only evidence, reciprocal folded-chain Tyr
rows remain topology biology ambiguity, and same-chain metal-supported transfer
geometry remains unsafe because it admits `9UW4`-like counterexamples.

This is review-routing/blocker evidence only. It is not a production
substrate-role identity rule and does not support ePK production readiness.

## Exact Next Experiment

Do not run another scalar source-free rescue on this tranche. Only resume if a
non-scalar, genuinely new source-free modality can separate both:

- same-chain metal-supported topology counterexamples (`3FGU`, `5XD6`, `6U1D`,
  `6U1E`, `9OAN`, `9UW4`)
- the reciprocal Tyr hard trio (`9UUR`, `9UUX`, `9UW4`)

without using source text, candidate-specific thresholds, labels as predictive
input, or production fingerprint edits.
