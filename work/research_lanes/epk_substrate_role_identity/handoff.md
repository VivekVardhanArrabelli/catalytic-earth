# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T17:28:08-0500

Primary outcome: `counterexample_found`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Run note: normal `git fetch origin` / `git pull --ff-only` were attempted at
run start, but the sandbox could not write linked-worktree `FETCH_HEAD`.
Live remote state was checked with `git ls-remote`; local `HEAD` and the live
remote ref both matched `261c6c38038f6a32555ee8358b3925737d7107c0` during
this run.

## What Was Tested

This run executed the requested source-free active-site
orientation/asymmetry probe:

`epk_active_site_orientation_asymmetry_probe_v1_review_only`

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_active_site_orientation_asymmetry_probe_v1_20260520.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/active_site_orientation_asymmetry_probe.py`

The helper:

- reused the prior 54-row local-exposure diagnostic set;
- fetched structures in memory only, with no raw coordinate files written;
- matched compact gamma/hydroxyl candidates already present in the local
  exposure artifact;
- added source-free orientation/asymmetry proxies around selected candidates:
  hydroxyl-anchor-to-gamma angle, hydroxyl gamma-facing versus backside
  half-space protein density, ligand-chain and acceptor-chain density near
  nucleotide gamma, gamma-axis forward/back density, and nearest other
  nucleotide/metal or active-gamma distances;
- compared existing strict, auth-terminal guarded strict, permissive, and
  reciprocal folded-Tyr rescue rules to orientation-gated variants.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, candidate-specific threshold tuning, production label
imports, and production threshold calibration.

## Evidence

Combined 54-row diagnostic set:

- Baseline strict rule: TP=14, FP=1, TN=33, FN=6.
- `strict_auth_terminal_guard_v1`: TP=14, FP=0, TN=34, FN=6.
- Permissive nearest-hydroxyl rule: TP=17, FP=27, TN=7, FN=3.
- Prior `reciprocal_folded_tyr_rescue_v1`: TP=16, FP=1, TN=33, FN=4.
- `orientation_supported_folded_tyr_rescue_v1`: TP=16, FP=1, TN=33, FN=4.
- `orientation_guarded_auth_strict_v1`: TP=14, FP=0, TN=34, FN=6.

The orientation-supported folded-Tyr rescue recovered `9UUR` and `9UUX`, but
also admitted `9UW4`.

Hard folded-Tyr trio under the accepted frozen orientation class:

- `9UUR`: `gamma_facing_active_site_like`; Tyr204, 4.181 A, angle 147.266
  degrees, 15 gamma-facing other-chain heavy atoms within 6 A, 25 ligand-chain
  heavy atoms within 6 A of gamma.
- `9UUX`: `gamma_facing_active_site_like`; Tyr204, 3.968 A, angle 148.035
  degrees, 12 gamma-facing other-chain heavy atoms within 6 A, 27 ligand-chain
  heavy atoms within 6 A of gamma.
- `9UW4`: `gamma_facing_active_site_like`; Tyr204, 4.194 A, angle 146.026
  degrees, 11 gamma-facing other-chain heavy atoms within 6 A, 22 ligand-chain
  heavy atoms within 6 A of gamma.

`7B56` remains a useful blocker probe. Its strict false-positive candidate is
Ser822 and the auth-terminal internal-fragment guard still rejects it. The new
orientation features do not separate it: its strict candidate is also
`gamma_facing_active_site_like` by the frozen descriptor. Thus `7B56` is still
handled by terminal-index/topology counterevidence, not by active-site
orientation.

The helper includes a post-hoc trio separability scan. A few scalar
orientation/density thresholds can reject `9UW4` while retaining `9UUR`/`9UUX`,
such as ligand-chain gamma-site density thresholds between 22 and 25 atoms.
Projected on the 54-row set these can score TP=16, FP=0, TN=34, FN=4, but they
are narrow thresholds learned from the hard trio and are not accepted as
source-free identity rules.

The remaining false negatives under the orientation-supported folded-Tyr rule
are `3QHR`, `3QHW`, `1L0O`, and `3TM0`. The artifact now includes a compact
`remaining_false_negative_probe`: `3QHR`, `3QHW`, and `1L0O` are ADP/product
state rows with no terminal gamma-equivalent candidate and zero candidates
within 8 A; `3TM0` has an ANP gamma and one 4.483 A Ser candidate, but it is
same-chain, folded-chain, `same_chain_gamma_hydroxyl`, and
`orientation_unsupported`.

## Interpretation

Active-site orientation/asymmetry adds useful review-only descriptors, but it
does not identify kinase substrate role on the frozen diagnostic set. The same
feature family that recovers the source-reviewed folded-Tyr positives also
recovers the `9UW4` topology-confounded counterexample.

The decisive issue is not only distance or simple catalytic-site orientation:
the hard trio has nearly identical hydroxyl-to-gamma angles, gamma-facing
protein density, and reciprocal active-site context. Source-free scalar
thresholds can be found after seeing the trio, but those are candidate-specific
tuning and remain excluded by the lane contract.

Comparable ePK substrate-role blockers in this lane still have not cleared
with structure-only nearest-atom, topology, residue-class, terminal-index,
reciprocal-context, local-exposure, or active-site-orientation proxies. Usable
progress remains hybrid: source-reviewed evidence can label and audit rows,
while source text remains excluded from predictive features.

## Current Decision

Do not claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or treat active-site orientation as a
substrate-role identity rule.

Use active-site orientation only as review-only ambiguity evidence:

- broad orientation classes do not separate the hard folded-Tyr counterexample;
- narrow scalar thresholds can be diagnostic but are post-hoc and
  candidate-specific;
- product/analog rows without terminal gamma remain unavailable to
  gamma-to-hydroxyl rules;
- `7B56` remains blocked by the auth-terminal internal-fragment guard, not by
  orientation.

## Exact Next Experiment

Classify the remaining strict-rule false negatives by unavailable ligand state
versus same-chain/autophosphorylation-like topology, then decide whether this
lane should stop feature probing and preserve a source-reviewed adjudication
requirement for ePK substrate-role identity. Treat this as a blocker decision
probe, not a production patch.
