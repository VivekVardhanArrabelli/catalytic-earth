# Fold-Level Novelty Signal - current702

Run: 2026-06-01T02:15:00Z

Fold-level novelty diagnostic against the current702 heldout rows, using the frozen selected-PDB Foldseek/fast-3Di structural-neighborhood metadata already in the repo. This is a bounded fold proxy, not a new predicted-geometry Foldseek run.

## Counts

- Heldout fold rows scored: 140
- In-scope: 48
- OOS: 92
- Cofactor-confounded OOS from novelty eval: 8
- Cofactor-confounded OOS overlapping predicted-geometry gate: 6

## Primary Signal

`nearest_primary_foldseek_prob` is the top Foldseek probability only when the nearest training neighbor carries a primary fingerprint; otherwise it is 0. Higher means the row sits near the occupied primary atlas.

- AUC in-scope > all OOS: 0.823256
- AUC in-scope > predicted-geometry confounded OOS: 0.793403
- Mean in-scope: 0.612771; mean OOS: 0.045804; mean confounded: 0.011833
- Best >=90% retention point: {'threshold': 0.0, 'inscope_retain_recall': 1.0, 'oos_abstain_recall': 0.0, 'confounded_abstain_recall': 0.0}
- Best >=85% retention point: {'threshold': 0.0, 'inscope_retain_recall': 1.0, 'oos_abstain_recall': 0.0, 'confounded_abstain_recall': 0.0}

## Orthogonality

- Pearson fold vs predicted-geometry top1: 0.24572
- Pearson fold vs cofactor max: 0.344169
- Pearson predicted-geometry top1 vs cofactor max: -0.204472

The selected-PDB fold proxy is only weakly correlated with both current deployment channels on overlapping heldout rows, so it is partly orthogonal. It catches the confounded rows by fold novelty, but its standalone high-retention operating point remains weak.

## Confounded Rows

| Row | nearest primary prob | top3 primary prob | high-conf primary hits | nearest train label |
| --- | ---: | ---: | ---: | --- |
| m_csa:30 | 0.057 | 0.057 | 0 | heme_peroxidase_oxidase |
| m_csa:31 | 0.014 | 0.014 | 0 | metal_dependent_hydrolase |
| m_csa:80 | 0.0 | 0.0 | 0 | out_of_scope |
| m_csa:191 | 0.0 | 0.0 | 0 | out_of_scope |
| m_csa:267 | 0.0 | 0.0 | 25 | out_of_scope |
| m_csa:448 | 0.0 | 0.009 | 0 | out_of_scope |
| m_csa:549 | 0.0 | 0.126 | 0 | out_of_scope |
| m_csa:563 | 0.0 | 0.0 | 0 | out_of_scope |

## Interpretation

- yes_as_a_rank_signal; all predicted-geometry confounded rows have near-zero nearest-primary Foldseek support in the existing selected-PDB proxy
- not_deployable_standalone; at >=85% or >=90% in-scope retention the nearest-primary Foldseek proxy cannot abstain many OOS rows, because many in-scope rows also lack strong primary structural-neighbor support
- A real deployment fold channel still needs predicted-structure Foldseek/TM scoring against the in-distribution atlas; this artifact uses selected-PDB structure metadata already frozen in repo.
