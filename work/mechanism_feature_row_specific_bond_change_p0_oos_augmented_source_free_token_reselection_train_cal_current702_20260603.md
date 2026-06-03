# Source-Free Token Re-Selection on Train/Cal — current702

Run: 2026-06-03  ·  Lever 2  ·  heldout never read

## Question
Before spending the irreplaceable one-shot heldout read, is there *any*
source-free-replicable token in the row-specific bond-change mechanism-feature
family that clears a useful bar on train/cal?

## Setup
- Pool: 43 OOS-augmented train/cal rows (15 in-scope primary, 28 out-of-scope).
- Labels used only as the selection target (never as a predictive feature). Heldout untouched.
- Source-free-replicable family = residue-identity counts (`event_residue_code` /
  `event_residue_code_count`) — i.e. "count residue code X near a source-free locator."
- Excluded as source-derived (not replicable without M-CSA roles / Rhea): all
  `event_residue_role_count`, `residue_role_count`, `event_mapped_*`,
  `event_participant_arity`, `event_type_sequence`, and every `bond_*` / `*_event`
  base feature.
- Note: event-residue counts are an **upper bound** on true source-free locator
  counts (M-CSA names the exact residues; source-free counting is noisier), so a
  null result here is conservative.

## Result — no source-free token clears a useful bar
- **Multivariate LOO-CV AUC of all source-free residue counts = 0.538** (≈ random).
- Best univariate token is **HIS at dir-adjusted AUC 0.601 — but pointing toward
  out-of-scope** (His count is higher in OOS rows, e.g. metalloproteins). It does
  not help retain in-scope rows.
- Every other residue-count token sits near 0.5 or has trivial coverage.

## The His-count fallback was role-dependent, not source-free
- The calibrated fallback `residue_code_count:his=3` (0.643 OOS-abstain recall)
  was computed on His residues carrying the **proton-transfer role** (source-derived).
- Stripped to a raw source-free His count, `HIS>=3` fires on 4 train/cal rows —
  **all out-of-scope** (in-scope precision 0.000). The signal came from the role
  binding, which does not survive source-free.

## Contrast — the real source-free signal is structural
- Predicted-structure fold/TM channel: **AUC 0.814** (in-scope vs all OOS);
  no-fit geometry+fold mean **AUC 0.908** (documented in `docs/project_state.md`).
- That is a different, structural channel — and it is where the source-free
  discriminative value actually lives.

## Conclusion / recommendation
- The Lever 2 row-specific mechanism token has **no source-free signal**; its power
  is entirely in M-CSA role/event bindings.
- **Do not spend the one-shot heldout read on any Lever 2 token.**
- Defer Lever 2. Bank the 53 approved, split-protected source-free locators as an
  asset. Direct source-free effort to the geometry/fold structural channel.

## Guardrails
Heldout never read; no frozen residual threshold applied; labels used only as the
selection target, never as a predictive input; review-only.
