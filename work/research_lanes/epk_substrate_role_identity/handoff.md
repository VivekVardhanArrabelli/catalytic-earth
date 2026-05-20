# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T16:27:38-0500

Primary outcome: `counterexample_found`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Run note: normal `git fetch origin` and `git pull --ff-only` were attempted
at run start, but the sandbox could not write linked-worktree `FETCH_HEAD`.
Live remote state was checked with `git ls-remote`; local `HEAD` and the live
remote ref both matched `2b6d9f8ceaa747fc59bd5f8a2b606cae160323f8` before
this run.

## What Was Tested

This run executed the requested alternate source-free feature-family probe:

`epk_local_burial_solvent_exposure_probe_v1_review_only`

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_local_burial_solvent_exposure_probe_v1_20260520.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/local_burial_solvent_exposure_probe.py`

The helper:

- reused the prior reciprocal-context 54-row diagnostic set;
- fetched structures in memory only, with no raw coordinate files written;
- matched compact gamma/hydroxyl candidates already present in the reciprocal
  artifact;
- added source-free local exposure proxies around candidate hydroxyl atoms:
  protein heavy-atom counts at 4/5/6/8/10 A, same-chain vs other-chain
  density, local residue counts, water oxygen proximity, nonwater heteroatom
  proximity, nucleotide/metal proximity, and 26-direction open-shell vacancy
  fractions at 3 A and 5 A;
- compared existing strict, auth-terminal guarded strict, permissive, and
  reciprocal folded-Tyr rescue rules to local exposure-gated variants.

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
- `local_open_shell_folded_tyr_rescue_v1`: TP=16, FP=1, TN=33, FN=4.
- `local_burial_guarded_auth_strict_v1`: TP=14, FP=0, TN=34, FN=6.
- `water_or_open_permissive_nearest_hydroxyl_v1`: TP=17, FP=27, TN=7, FN=3.

The local exposure class did not separate the decisive folded-Tyr trio:

- `9UUR`: open_or_surface_like; Tyr204, 4.181 A, 25 protein heavy atoms within
  6 A after same-residue exclusion, open-shell fraction 3 A = 0.692.
- `9UUX`: open_or_surface_like; Tyr204, 3.968 A, 25 protein heavy atoms within
  6 A after same-residue exclusion, open-shell fraction 3 A = 0.615.
- `9UW4`: open_or_surface_like; Tyr204, 4.194 A, 25 protein heavy atoms within
  6 A after same-residue exclusion, open-shell fraction 3 A = 0.731.

The helper includes a post-hoc trio separability scan. Several scalar exposure
features can separate `9UW4` from only `9UUR`/`9UUX`, such as a 5 A
same-residue-excluded protein density threshold between 9 and 12 atoms, or a
3 A open-shell threshold between 0.692 and 0.731. Projected on the 54-row set
these would score TP=16, FP=0, TN=34, FN=4, but they are candidate-specific
thresholds learned from the hard trio and are not accepted as source-free
identity rules.

`7B56` remains a useful blocker probe. Its strict false-positive candidate is
Ser822, resolved ordinal 1, and auth-terminal internal-fragment-like; the
auth-terminal guard still rejects it. Local exposure alone would not solve
`7B56`: the selected hydroxyl is open_or_surface_like with water nearby.

The remaining false negatives under the best non-posthoc local-exposure rule
are `3QHR`, `3QHW`, `1L0O`, and `3TM0`: three product/analog-state rows
without a terminal gamma-equivalent candidate, plus one same-chain or
autophosphorylation-like topology row.

## Interpretation

Local burial and solvent exposure are useful review-only context, but broad
source-free exposure classes do not identify kinase substrate role on the
frozen diagnostic set. The feature family confirms that simple local density,
water contact, and shell openness are not enough to distinguish the
source-reviewed folded-Tyr positives from the topology-confounded `9UW4`
counterexample.

The only local-exposure splits that reject `9UW4` are narrow, post-hoc scalar
thresholds against the same hard trio. Those are exactly the kind of
candidate-specific tuning excluded by the lane contract.

Comparable ePK substrate-role blockers in this lane still have not cleared
with structure-only nearest-atom, topology, residue-class, terminal-index,
reciprocal-context, or local-exposure proxies. Usable progress remains hybrid:
source-reviewed evidence can label and audit rows, while source text remains
excluded from predictive features.

## Current Decision

Do not claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or treat local exposure as a substrate-role
identity rule.

Use local exposure only as review-only ambiguity evidence:

- broad open/buried classes do not separate the hard folded-Tyr counterexample;
- narrow scalar thresholds can be diagnostic but are post-hoc and
  candidate-specific;
- product/analog rows without terminal gamma remain unavailable to
  gamma-to-hydroxyl rules;
- `7B56` remains handled by the auth-terminal internal-fragment guard, not by
  exposure.

## Exact Next Experiment

Run a source-free acceptor-chain active-site orientation/asymmetry probe:
compare candidate hydroxyl vector geometry to nucleotide gamma and nearby
catalytic-chain density, especially `9UUR`/`9UUX`/`9UW4` and the product-state
false negatives. The goal is to test whether orientation or reciprocal
active-site geometry adds a non-posthoc separation axis; if it only separates
the known trio by tuned scalar thresholds, keep it review-only.
