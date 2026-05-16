# Foldseek readiness note

Recorded: 2026-05-16T01:55:26-05:00

M-CSA strict pairwise Foldseek/TM-score `<0.7` is closed/deferred, not an
active implementation loop. The final M-CSA adjudication is
`artifacts/v3_mcsa_tm_holdout_feasibility_adjudication_1000.json`.

Preserved evidence:

- `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`
  records 672 materializable selected coordinates, 676 materializable evaluated
  rows, and coordinate exclusions for `m_csa:372` and `m_csa:501`.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json`
  records 952,922 mapped Foldseek pair rows, 274,241 train/test rows, max
  train/test TM-score `0.9749`, and 4,715 target-violating train/test rows.

Removed/deprecated evidence:

- Noncanonical staged, expanded, query-chunk, query-single, target-shard,
  split-repair, split-redesign, and cluster-first round artifacts were removed.
- Do not regenerate round32/index145, round33, or further M-CSA partition
  repair artifacts to force `TM <0.7`.

Current path:

- M-CSA sequence-identity holdout remains valid evidence.
- Future strict TM-diverse holdouts belong on broader external structural data
  such as Swiss-Prot/UniProt/AFDB candidates, with structure clustering before
  split assignment.
- The review-only external structural path starts at
  `artifacts/v3_external_structural_tm_holdout_path_1025.json`.
- `artifacts/v3_external_structural_cluster_index_1025.json` now materializes
  the 10 selected pilot AlphaFold coordinate sidecars, completes Foldseek
  nearest-neighbor clustering, and finds one `TM >=0.7` external pair
  (`O95050`/`P51580`) across nine clusters. This is pre-split review evidence
  only and does not authorize import or countable labels.
