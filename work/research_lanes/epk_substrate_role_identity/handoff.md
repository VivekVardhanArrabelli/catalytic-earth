# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T15:25:58-0500

Primary outcome: `counterexample_found`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Run note: normal `git fetch origin` and `git pull --ff-only` were attempted
at run start, but the sandbox could not write linked-worktree `FETCH_HEAD`.
Live remote state was checked with `git ls-remote`; local `HEAD`, stale
`origin/research/epk-substrate-role-identity`, and the live remote ref all
matched `3e81ffc011601e96ba697a80210252ab6227010f` before this run.

## What Was Tested

This run executed the requested alternate source-free feature-family probe:

`epk_reciprocal_entity_context_probe_v1_review_only`

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_reciprocal_entity_context_probe_v1_20260520.json`

The helper:

- reused the prior 30-row terminal-index stress set and 24-row non-overlap
  set, for 54 compact diagnostic rows;
- fetched structures in memory only, with no raw coordinate files written;
- added source-free reciprocal chain/entity features: resolved residue-name
  sequence hashes by chain, ligand/acceptor same-sequence entity flag,
  acceptor-chain active-gamma occupancy, acceptor-chain nucleotide/metal
  occupancy, and reciprocal context class;
- compared the existing strict, auth-terminal guarded strict, and permissive
  nearest-hydroxyl rules to two reciprocal-context rules.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, candidate-specific threshold tuning, production label
imports, and production threshold calibration.

## Evidence

Combined 54-row diagnostic set:

- Baseline strict rule: TP=14, FP=1, TN=33, FN=6.
- `strict_auth_terminal_guard_v1`: TP=14, FP=0, TN=34, FN=6.
- Permissive nearest-hydroxyl rule: TP=17, FP=27, TN=7, FN=3.
- `reciprocal_asymmetric_guarded_strict_v1`: TP=14, FP=0, TN=34, FN=6.
- `reciprocal_folded_tyr_rescue_v1`: TP=16, FP=1, TN=33, FN=4.

The asymmetric reciprocal guard made no improvement over the auth-terminal
strict baseline. It retained the same true positives and still missed
`9UUR`, `9UUX`, `3QHR`, `3QHW`, `1L0O`, and `3TM0`.

The folded-Tyr reciprocal rescue recovered `9UUR` and `9UUX`, but it also
introduced `9UW4` as a false positive. The decisive source-free match:

- `9UUR`: folded Tyr 204, cross-chain, distance 4.181 A, different resolved
  chain-sequence hash, acceptor chain has active-gamma context.
- `9UUX`: folded Tyr 204, cross-chain, distance 3.968 A, different resolved
  chain-sequence hash, acceptor chain has active-gamma context.
- `9UW4`: folded Tyr 204, cross-chain, distance 4.194 A, different resolved
  chain-sequence hash, acceptor chain has active-gamma context.

Thus the source-free feature needed to recover the MEK/ERK-like folded Tyr
positives also admits the source-reviewed non-substrate-role counterexample.

The context-class summary also shows why reciprocal context is mostly a
review axis, not an identity rule: positive rows and counterexample rows both
contain same-chain gamma/hydroxyl contexts and reciprocal active-gamma
different-entity contexts.

A scratch, no-artifact sanity check of local atom-density around the decisive
Tyr204 trio did not suggest an easy separation: `9UUR`, `9UUX`, and `9UW4`
all had 32 protein ATOM neighbors within 6 A of the Tyr hydroxyl, and very
similar 8-10 A density. A full exposure probe should still be run, but simple
local density alone may be another weak axis.

## Interpretation

Reciprocal chain/entity context further characterizes the blocker, but does
not clear it. It distinguishes clean peptide-like asymmetric substrate rows
from many enzyme-context controls, yet the hard folded protein cases remain
biologically ambiguous from structure alone.

`7B56` remains handled only by the auth-terminal internal-fragment guard. That
guard is still useful review-only counterevidence, not a production identity
rule.

The current decisive counterexample is `9UW4`: a source-free reciprocal
folded-Tyr rule that recovers `9UUR`/`9UUX` cannot keep `9UW4` negative.

Comparable ePK substrate-role blockers in this repo still have not cleared
with structure-only nearest-atom, topology, residue-class, terminal-index, or
reciprocal-context rules. Usable progress remains hybrid: source-reviewed
evidence can label and audit rows, while source text remains excluded from
predictive features.

## Current Decision

Do not claim ePK production readiness. Do not import labels, edit production
fingerprints, calibrate thresholds, or treat reciprocal entity context as a
substrate-role identity rule.

Use reciprocal context only as review-only ambiguity evidence:

- asymmetric cross-chain peptide-like contexts support the existing strict
  review rule;
- reciprocal active-gamma folded Tyr contexts need source-reviewed
  adjudication;
- product/analog rows without terminal gamma remain unavailable to these
  gamma-to-hydroxyl rules.

## Exact Next Experiment

Run a different source-free feature family:

`epk_local_burial_solvent_exposure_probe_v1_review_only`

Use the same combined 54-row diagnostic set and compute cheap local burial or
solvent-exposure proxies around candidate hydroxyl atoms, such as local ATOM
count within fixed radii, same-chain neighbor density, heteroatom proximity,
or accessible-shell vacancy counts. The key test is whether anything richer
than simple neighbor counts separates `9UW4` from `9UUR`/`9UUX` without losing
peptide positives or reintroducing `7B56`. If it only explains one row class,
keep it as review-only counterevidence.
