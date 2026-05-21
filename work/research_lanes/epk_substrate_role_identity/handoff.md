# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T08:08:35-0500

Primary outcome: `blocker_not_cleared_biology_ambiguity`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 49.17 minutes (`2026-05-21T12:19:25Z` to
`2026-05-21T13:08:35Z`).

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Local `HEAD` remains stale relative to
`origin/research/epk-substrate-role-identity`; commit/push must use the same
remote-tip temporary-index workaround as the previous runs.

Final sync: pushed signature-collision commit
`b608bcd0849344967bcd6582a3522bb0e6871abb` to
`origin/research/epk-substrate-role-identity`, then verified
`origin/research/epk-substrate-role-identity` at that commit with
`git fetch --no-write-fetch-head origin`. A temporary-index comparison against
the remote tip was clean for the lane paths. Normal `git status` still reports
this linked worktree as behind with lane-file changes because local `HEAD`
remains `8d38053d85cc28b7592267e9420578ca19a98814`.

## What Was Emitted

This run added a compact source-free signature-collision audit on top of the
existing candidate evidence and conflict-decision artifacts.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_signature_collision_audit_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/candidate_signature_collision_audit.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_evidence_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`

The helper reused:

- 204 gamma/acceptor candidate-pair rows.
- 7 state-only rows.
- 54 PDB-level conflict rows.

It emitted:

- 211 source-free candidate signature rows.
- 65 source-free candidate signature group rows.
- 54 source-free PDB signature rows.
- 34 source-free PDB signature group rows.

Review labels remain only under evaluation context and were used only after
source-free signature grouping to detect collisions. Forbidden predictive
inputs remained excluded: PDB title, UniProt prose, EC/Rhea, paper/source text,
mechanism labels, curated substrate names, post-hoc source repair, and
candidate-specific threshold tuning.

## Evidence Summary

The collision audit grouped candidate rows by categorical source-free evidence:
coordinate state, blocker class, topology, reciprocal context, acceptor context,
orientation support class, local exposure profile, coordinate certainty class,
and the preexisting 6 A transfer-geometry distance class.

Summary counts:

- Candidate signature groups: 65.
- Mixed positive/counterexample candidate signature groups: 4.
- Mixed candidate rows: 40.
- PDBs touched by mixed candidate signatures: 18.
- Mixed PDB signature groups: 2.
- PDBs touched by mixed PDB signatures: 10.
- Mixed `blocker_class=none` signature groups: 0.
- Mixed `topology_ambiguity` signature groups: 3.

Mixed candidate groups by blocker class:

- `topology_ambiguity=3`
- `active_gamma_geometry=1`

The reused review-only conflict routing matrix remained:

- TP=14
- FP=0
- TN=8
- FN=0
- abstained positives=6
- abstained negatives=26

Abstained positives remain the known review-required classes:

- product/ADP state rows: `1L0O`, `3QHR`, `3QHW`
- reciprocal folded-chain rows: `9UUR`, `9UUX`
- same-chain/autophosphorylation-like row: `3TM0`

## Decisive Collisions

The reciprocal folded-chain topology group collides exactly across:

- positives: `9UUR`, `9UUX`
- counterexample: `9UW4`

Those rows share source-free reciprocal folded-chain/Tyr or same-chain topology
signatures with:

- `coordinate_state=active_gamma`
- `blocker_class=topology_ambiguity` for the near candidates
- `coordinate_certainty_class=ordered_like`
- `local_exposure_profile_class=open_or_surface_like`
- `orientation_support_class=gamma_facing_active_site_like` for the reciprocal
  Tyr candidate and `orientation_unsupported` for same-chain candidates
- `distance_transfer_class=within_preexisting_transfer_geometry_6a`

The same-chain topology PDB signature also collides across the positive `3TM0`
and counterexamples `5TT6`, `5XD6`, `6NOO`, `7T55`, `8W2J`, and `9NBW`.

## Interpretation

The blocker is not cleared source-free. Candidate-level structural signatures
are not unique to true substrate-role positives; topology signatures collide
between positives and counterexamples even after including coordinate
certainty, exposure, orientation, reciprocal context, and coordinate state.

No mixed signature group has `blocker_class=none`, so the existing unblocked
candidate rows can remain useful as review-only structural support. However,
the mixed topology groups mean source-free de-abstention would admit `9UW4`-like
counterexamples.

This is review-routing/blocker evidence only. It is not a production
substrate-role identity rule and does not support ePK production readiness.

## Exact Next Experiment

Do not run another scalar source-free rescue on this tranche. Only resume if a
genuinely new evidence modality can separate mixed topology signatures,
especially `9UUR`/`9UUX` versus `9UW4`, without using source text or
candidate-specific thresholds.
