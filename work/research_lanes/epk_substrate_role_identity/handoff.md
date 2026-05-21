# ePK Substrate-Role Identity Handoff

Last updated: 2026-05-21T12:12:30-0500

Primary outcome: `candidate_evidence_rows_emitted`

`production_claim_allowed=false`

`labels_or_fingerprints_changed=false`

Measured run time: 48.73 minutes (`2026-05-21T16:23:21Z` to
`2026-05-21T17:12:05Z`).

Run note: normal `git fetch origin` and `git pull --ff-only origin
research/epk-substrate-role-identity` were attempted at run start but the
sandbox could not write the linked-worktree `FETCH_HEAD`. `git fetch
--no-write-fetch-head origin` succeeded. Normal local `HEAD` remains stale
relative to `origin/research/epk-substrate-role-identity`; commit/push should
continue using the remote-tip temporary-index workaround.

Final sync notes: pending until wrap verification. Use the remote-tip
temporary-index flow for this run's artifact/helper/handoff/ledger commit, then
refresh this section if a handoff-only sync commit is needed. Normal `git
status` may still report stale/dirty because local `HEAD` is behind the remote
tip.

## What Was Emitted

This run added one compact source-free coordinate modality:
phosphoproduct materialization audit. The helper fetches diagnostic structures
in memory, writes only reduced rows, and does not write raw coordinate dumps.

Artifact:

`artifacts/research_lanes/epk_substrate_role_identity/epk_phosphoproduct_materialization_audit_v1_20260521.json`

Helper:

`tools/research_lanes/epk_substrate_role_identity/phosphoproduct_materialization_audit.py`

Inputs:

- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_coordinate_state_taxonomy_v1_20260521.json`
- `artifacts/research_lanes/epk_substrate_role_identity/epk_candidate_conflict_decision_v1_20260521.json`

The helper reused 211 coordinate-state taxonomy rows and 54 PDB-level conflict
rows. It scanned all 54 diagnostic PDBs in memory and emitted 135 compact
phosphoproduct materialization rows:

- `terminal_gamma_context=126`
- `adp_phosphoacceptor_pair=4`
- `adp_only_state=2`
- `non_adp_nucleotide_phosphoacceptor_pair=1`
- `state_only=2`

No source text, titles, UniProt prose, EC/Rhea, mechanism labels, curated
substrate names, post-hoc source repair, candidate-specific threshold tuning,
production labels, registries, fingerprints, migration manifests, or raw
coordinate dumps were used or changed.

## Evidence Summary

Coordinate states observed in this phosphoproduct audit:

- `active_gamma=126`
- `product_state=4`
- `adp_state=2`
- `split_state=1`
- `ligand_absent=2`

Phosphoproduct materialization classes:

- `active_gamma_terminal_gamma_present_product_scan_suppressed=126`
- `adp_plus_phosphorylated_sty_same_chain_global_product_chemistry=4`
- `adp_without_phosphorylated_sty_product_not_materialized=2`
- `non_adp_nucleotide_without_terminal_gamma_plus_phosphorylated_sty_split_like=1`
- `ligand_absent_product_not_materialized=2`

Hard state rows:

- `3QHR` and `3QHW` now have source-free `product_state` chemistry rows:
  ADP plus covalently phosphorylated TPO on the same chain. These are global
  product-chemistry rows, not active-site transfer-geometry or biological
  substrate-role proof; nearest ADP-to-TPO distances remain distant
  (`13.206` to `13.28` A).
- `1L0O` remains source-free `adp_state` only: two ADP rows and no materialized
  phosphorylated STY acceptor.
- `4HPU` materializes a source-free `split_state` pressure row:
  non-ADP nucleotide without terminal gamma plus phosphorylated SEP at direct
  contact (`3.15` A). It is a counterpressure row against promoting split/product
  chemistry to a positive substrate-role call.
- `3TM0` remains active-gamma/same-chain review-analog context. The audit did
  not materialize a source-free `substrate_acceptor_analog_state`.

Source-leakage guard:

- `no_review_state_claim_to_promote=128`
- `review_product_context_has_source_free_phosphoproduct_state=4`
- `review_product_context_not_source_free_product_state=2`
- `review_analog_context_not_source_free_analog_state=1`

Guarded review-context promotions remain prohibited for:

- `1L0O|gamma=none|acceptor=none|nucleotide=A:ADP601`
- `1L0O|gamma=none|acceptor=none|nucleotide=B:ADP701`
- `3TM0|gamma=A:ANP300:PG|acceptor=none|nucleotide=A:ANP300`

The conservative conflict projection remains review-only and abstaining:

- TP=14
- FP=0
- TN=8
- FN=0
- Abstained positives=6
- Abstained negatives=26

## Decisive Result

The blocker is not cleared source-free.

Phosphoproduct chemistry directly materializes product-state coordinate rows for
`3QHR` and `3QHW`, reducing one coordinate-state uncertainty from the prior
taxonomy audit. It still does not assign biological substrate role source-free.
The audit does not cover ADP-only `1L0O`, substrate-analog `3TM0`, reciprocal
folded-chain `9UUR`/`9UUX`, or same-chain topology blockers.

This is review-only blocker evidence. It is not a production rule and does not
support ePK production readiness.

## Interpretation

The useful refinement is narrow: source-free coordinates can distinguish
terminal-gamma-active rows, global ADP plus phospho-STY product chemistry,
ADP-only rows, and split-like non-ADP nucleotide/phospho-STY rows. That helps
route product/split blockers but does not identify the biological substrate
acceptor role.

Promoting product/split rows would be unsafe because `4HPU` is a split-state
counterpressure row and because global product chemistry lacks source-free
evidence that the phosphorylated residue is the biological substrate of the
kinase chain in the entry.

## Exact Next Experiment

Do not add scalar rescues. Only resume this lane for a genuinely new source-free
modality that can adjudicate biological substrate role for ADP-only, analog,
reciprocal folded-chain, or same-chain cases without review-context leakage.
Otherwise preserve source-reviewed adjudication for product/ADP, split-state,
substrate-analog, reciprocal folded-chain, and same-chain substrate biology.
