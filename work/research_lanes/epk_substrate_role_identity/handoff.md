# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-20T14:29:58-0500

Primary outcome: `blocker_not_cleared_data_scarcity`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Run note: `git fetch origin` failed at start because the sandbox could not
write `FETCH_HEAD` inside the parent repository worktree metadata. Remote tip
was checked with `git ls-remote` and matched local `HEAD` at run start. The run
continued only in the isolated `research/epk-substrate-role-identity` worktree.

## What Was Tested

Two review-only terminal-index experiments are now present in this lane.

First, `epk_folded_nterminal_auth_terminal_stress_v1_review_only` added a
30-row stress artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_folded_nterminal_auth_terminal_stress_20260520.json`

It introduced these source-free coordinate-derived features:

- integer author residue number from coordinate records
- resolved 1-based residue ordinal in the candidate acceptor chain
- `auth_seq_id - resolved_ordinal`
- `auth-terminal-like N-terminal STY` guard:
  `abs(auth_seq_id - resolved_ordinal) <= 5`
- `internal-fragment-like N-terminal STY` flag when resolved N-terminal STY
  numbering is inconsistent with a true chain N terminus

Second, this run executed the handoff's next requested probe,
`epk_folded_nterminal_auth_terminal_guard_generalization_v2_review_only`.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_auth_terminal_guard_generalization_v2_20260520.json`

The new frozen diagnostic set has 24 non-overlap rows from prior review
artifacts: five positive-like rows (`1IR3`, `2PHK`, `4EKK`, `1L0O`, `3TM0`)
and 19 sibling/topology/transporter controls. All 24 PDB coordinate files
fetched successfully in memory. No raw coordinate files were written.

The full requested enrichment for independent true folded N-terminal substrate
positives was not possible: prior lane artifacts repeatedly identify `5HVK` as
the only source-valid heteromeric folded N-terminal protein-substrate positive.
The non-overlap positives available for this run are current protein-substrate,
exact-source/context-ambiguous, product-state, or ligand-analog rows rather
than independent folded auth-terminal positives.

Forbidden predictive inputs remained excluded: PDB title, UniProt prose,
EC/Rhea, paper/source text, mechanism labels, curated substrate names,
post-hoc source repair, candidate-specific threshold tuning, production label
imports, and production threshold calibration.

## Evidence

Over the prior 30-row terminal-index stress set:

- Baseline strict rule: TP=11, FP=1, TN=14, FN=4.
- `strict_auth_terminal_guard_v1`: TP=11, FP=0, TN=15, FN=4.
- The guard removed the decisive `7B56` false positive by classifying its
  resolved N-terminal Ser 822/ordinal 1 as internal-fragment-like
  (`auth_seq_id - resolved_ordinal = 821`).
- Permissive nearest-hydroxyl rule: TP=13, FP=15, TN=0, FN=2.

Over the new 24-row non-overlap generalization set:

- Baseline strict rule: TP=3, FP=0, TN=19, FN=2.
- `strict_auth_terminal_guard_v1`: TP=3, FP=0, TN=19, FN=2.
- Permissive nearest-hydroxyl rule: TP=4, FP=12, TN=7, FN=1.
- Independent folded auth-terminal true-positive coverage: 0/5 positive-like
  rows.

The guard made no difference on the non-overlap set because no independent
true positive supplied a folded, auth-terminal-like N-terminal STY candidate.
The retained positives were all short-peptide-like in coordinate context:
`1IR3` chain length 6, `2PHK` chain length 7, and `4EKK` chain length 10.
`4EKK` also remains source-context ambiguous in prior broad review and is not
clean folded N-terminal guard evidence. False negatives were `1L0O`
(ADP/product-state) and `3TM0` (ligand-analog/topology ambiguity).

## Interpretation

The terminal-index guard is useful review-only counterevidence for one mimic
class: resolved N-terminal Ser/Thr/Tyr candidates that are actually internal
fragments under coordinate residue numbering. It provides a source-free
explanation for why `7B56` should not be generalized as a true folded substrate
positive.

The blocker is still not cleared. The guard has not generalized beyond `5HVK`
because this lane still lacks independent folded N-terminal protein-substrate
positives with auth-terminal-like numbering. It also does not solve
non-terminal folded protein acceptors, product/analog states, topology
ambiguity, or acceptor-role ambiguity.

Comparable ePK substrate-role blockers in this repo have not been cleared by
structure-only nearest-atom, topology, residue-class, or terminal-position
rules. Usable progress remains hybrid: source-reviewed evidence can label and
audit rows, while source text stays excluded from predictive features.

## Current Decision

`strict_auth_terminal_guard_v1` should remain a review-only counteraxis for
`7B56`-style internal-fragment mimics. It is not a general source-free
substrate-role identity rule and does not authorize production readiness,
label imports, fingerprint edits, threshold calibration, or held-out
performance claims.

## Exact Next Experiment

Run a different source-free feature family rather than another terminal-index
generalization probe. Recommended next query:

`epk_reciprocal_cross_chain_entity_asymmetry_or_burial_probe_v1_review_only`

Use the existing positive/control rows and test one frozen feature family:

- reciprocal cross-chain/entity asymmetry between nucleotide-bearing chain and
  acceptor chain, or
- cheap residue burial/local solvent exposure around candidate hydroxyl atoms.

Compare against the existing strict, guarded strict, and permissive rules.
Success requires improving non-terminal folded protein/product-state ambiguity
without reintroducing `7B56`-style or sibling-family false positives. If the
feature only explains one row class, keep it as review-only counterevidence,
not a production rule.
