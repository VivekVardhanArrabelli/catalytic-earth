# Targeted Bin Expansion Proposal - current702

Run: 2026-05-30T07:14:27Z

Proposal/materialization queue only. No labels, registries, ontologies, imports, production scoring, global thresholds, model weights, or frozen LOMO split artifacts were changed.

## Baseline

- Snapshot: `snapshot/concordance-gate-current702-20260530`
- Required commit: `f393ad25c3959778c7e66a68974bcfee6c93f031`
- Worktree HEAD: `f393ad25c3959778c7e66a68974bcfee6c93f031`
- Frozen split: `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`

## Current frozen bin counts

| Bin | Rows | Primary | OOS/sec | Primary gap to 30 | OOS/sec gap to 10 | OOS-FP rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `dense_same_mechanism_structural_neighborhood` | 10 | 10 | 0 | 20 | 10 | n/a |
| `fold_conflict_oos_hard_negative` | 11 | 0 | 11 | 30 | 0 | 0.0 |
| `high_structure_similarity_different_fingerprint` | 5 | 0 | 5 | 30 | 5 | 0.2 |
| `low_structure_neighborhood_near_orphan` | 30 | 30 | 0 | 0 | 10 | n/a |
| `no_reliable_structure` | 6 | 5 | 1 | 25 | 9 | 0.0 |

## Target counts

- Stable metric target: 30 primary-support rows and 10 OOS/secondary controls where applicable.
- Minimal next-batch floor: 10 primary-support rows and 5 OOS/secondary controls for the two underpowered bins. This is diagnostic/evaluable only, not a stable metric claim.
- Verified fold-conflict target: 10 verified anchors; current verified anchors are 3, with 2 additional review candidates and 11 OOS fold-conflict hard negatives.
- Boundary/near-OOD controls target: 10; current secondary OOD support is 3.

## Smallest next acquisition batch

Smallest diagnostic batch: 14 rows.

| Need | Candidate IDs |
| --- | --- |
| `no_reliable_primary_positive_leads` | `mh_064`, `mh_065`, `mh_066`, `mh_067`, `mh_068` |
| `no_reliable_oos_or_secondary_controls` | `uniprot:P22830`, `uniprot:P78549`, `uniprot:Q3LXA3`, `mh_072` |
| `near_orphan_oos_or_secondary_controls` | `mh_073`, `m_csa:10`, `m_csa:30`, `m_csa:31`, `m_csa:116` |

This closes the minimal floor gaps for `no_reliable_structure` and `low_structure_neighborhood_near_orphan` without padding the dense same-structure bin. Relative to the frozen baseline, the stable 30/10 target gaps remain 25 primary and 9 OOS/secondary for `no_reliable_structure`, and 10 OOS/secondary for `low_structure_neighborhood_near_orphan`.

## Candidate list

| Candidate | Proposed bin | Role | Batch | Structure | Leakage risk | Blocker |
| --- | --- | --- | --- | --- | --- | --- |
| `mh_064` | `no_reliable_structure` | `positive` | `smallest_next_batch` | not_in_current702_active_site_cache | medium_external; public PDB/AlphaFold available but no current702 import gates run | external lead; no import/countable use until duplicate, Foldseek, geometry, expert, and factory gates pass |
| `mh_065` | `no_reliable_structure` | `positive` | `smallest_next_batch` | not_in_current702_active_site_cache | medium_external; public PDB/AlphaFold available but no current702 import gates run | external lead; no import/countable use until duplicate, Foldseek, geometry, expert, and factory gates pass |
| `mh_066` | `no_reliable_structure` | `positive` | `smallest_next_batch` | not_in_current702_active_site_cache | medium_external; public PDB/AlphaFold available but no current702 import gates run | external lead; no import/countable use until duplicate, Foldseek, geometry, expert, and factory gates pass |
| `mh_067` | `no_reliable_structure` | `positive` | `smallest_next_batch` | not_in_current702_active_site_cache | medium_external; public PDB/AlphaFold available but no current702 import gates run | external lead; no import/countable use until duplicate, Foldseek, geometry, expert, and factory gates pass |
| `mh_068` | `no_reliable_structure` | `positive` | `smallest_next_batch` | not_in_current702_active_site_cache | medium_external; public PDB/AlphaFold available but no current702 import gates run | external lead; no import/countable use until duplicate, Foldseek, geometry, expert, and factory gates pass |
| `mh_069` | `no_reliable_structure` | `review-only` | `reserve` | not_in_current702_active_site_cache | medium_external; public PDB/AlphaFold available but no current702 import gates run | external lead; no import/countable use until duplicate, Foldseek, geometry, expert, and factory gates pass |
| `uniprot:P22830` | `no_reliable_structure` | `hard-negative` | `smallest_next_batch` | unknown | medium; bounded duplicate screens clear but terminal/factory gates remain | full_label_factory_gate_not_run; terminal_review_decision_not_accepted; uniref_wide_duplicate_screening_required |
| `uniprot:P78549` | `no_reliable_structure` | `hard-negative` | `smallest_next_batch` | unknown | medium; bounded duplicate screens clear but terminal/factory gates remain | full_label_factory_gate_not_run; terminal_review_decision_not_accepted; uniref_wide_duplicate_screening_required |
| `uniprot:Q3LXA3` | `no_reliable_structure` | `hard-negative` | `smallest_next_batch` | unknown | medium; bounded duplicate screens clear but terminal/factory gates remain | full_label_factory_gate_not_run; terminal_review_decision_not_accepted; uniref_wide_duplicate_screening_required |
| `mh_072` | `no_reliable_structure` | `hard-negative` | `smallest_next_batch` | not_in_current702_active_site_cache | medium_external; public PDB/AlphaFold available but no current702 import gates run | external lead; no import/countable use until duplicate, Foldseek, geometry, expert, and factory gates pass |
| `mh_073` | `low_structure_neighborhood_near_orphan` | `hard-negative` | `smallest_next_batch` | not_in_current702_active_site_cache | medium_external; public PDB/AlphaFold available but no current702 import gates run | external lead; no import/countable use until duplicate, Foldseek, geometry, expert, and factory gates pass |
| `m_csa:10` | `low_structure_neighborhood_near_orphan` | `canary` | `smallest_next_batch` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:30` | `low_structure_neighborhood_near_orphan` | `canary` | `smallest_next_batch` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:31` | `low_structure_neighborhood_near_orphan` | `canary` | `smallest_next_batch` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:116` | `low_structure_neighborhood_near_orphan` | `canary` | `smallest_next_batch` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:217` | `verified_fold_conflict` | `canary` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:428` | `verified_fold_conflict` | `canary` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:477` | `verified_fold_conflict` | `canary` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:131` | `verified_fold_conflict` | `review-only` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:853` | `verified_fold_conflict` | `review-only` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:118` | `oos_hard_negatives` | `hard-negative` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:144` | `oos_hard_negatives` | `hard-negative` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:188` | `oos_hard_negatives` | `hard-negative` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:220` | `oos_hard_negatives` | `hard-negative` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:255` | `oos_hard_negatives` | `hard-negative` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:128` | `boundary_near_ood_controls` | `hard-negative` | `reserve` | already_materialized | high_if_imported; M-CSA row must stay eval-only unless already frozen current702 | review-only; future expert decision and frozen split required |
| `m_csa:129` | `boundary_near_ood_controls` | `hard-negative` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:130` | `boundary_near_ood_controls` | `hard-negative` | `reserve` | already_materialized | high_if_imported; M-CSA row must stay eval-only unless already frozen current702 | review-only; future expert decision and frozen split required |
| `m_csa:133` | `boundary_near_ood_controls` | `hard-negative` | `reserve` | already_materialized | high_if_imported; M-CSA row must stay eval-only unless already frozen current702 | review-only; future expert decision and frozen split required |
| `m_csa:134` | `boundary_near_ood_controls` | `hard-negative` | `reserve` | already_materialized | high_if_imported; M-CSA row must stay eval-only unless already frozen current702 | review-only; future expert decision and frozen split required |
| `m_csa:135` | `boundary_near_ood_controls` | `hard-negative` | `reserve` | already_materialized | high_if_imported; M-CSA row must stay eval-only unless already frozen current702 | review-only; future expert decision and frozen split required |
| `m_csa:141` | `boundary_near_ood_controls` | `hard-negative` | `reserve` | already_materialized | high_if_imported; M-CSA row must stay eval-only unless already frozen current702 | review-only; future expert decision and frozen split required |
| `m_csa:497` | `boundary_near_ood_controls` | `canary` | `reserve` | already_materialized | high_if_reused_for_training; frozen heldout/eval-only context | already frozen heldout/eval-only; do not train, import, or alter split assignment |
| `m_csa:699` | `boundary_near_ood_controls` | `hard-negative` | `reserve` | already_materialized | high_if_imported; M-CSA row must stay eval-only unless already frozen current702 | review-only; future expert decision and frozen split required |
| `m_csa:795` | `boundary_near_ood_controls` | `hard-negative` | `reserve` | already_materialized | high_if_imported; M-CSA row must stay eval-only unless already frozen current702 | review-only; future expert decision and frozen split required |

## Gates

- M-CSA rows stay eval-only unless already frozen in current702; none of these rows are marked import-ready.
- External rows keep source/provenance tags and require structure materialization, duplicate/leakage screens, expert decisions, label-factory gates, and a future frozen split before countable use.
- Cofactor evidence must come from experimental ligand/local structure context or source-reviewed cofactor records, never from mechanism fingerprint labels alone.
- OOS-FP is a hard gate: any future nonzero OOS false-positive rate blocks promotion.

## Output

- JSON: `artifacts/v3_targeted_bin_expansion_proposal_current702_20260530.json`
- Report: `work/targeted_bin_expansion_proposal_current702_20260530.md`
