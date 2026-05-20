# ePK sibling controls handoff

Run started: 2026-05-20T15:18:16Z
Run ended: 2026-05-20T16:06:34Z

Primary outcome: `counterexample_found`

## What changed

Added ATP-grasp to the lane-only bounded sibling-control screen and fixed the helper title parser so RCSB mmCIF titles on the next quoted line are recognized. The helper still fetches structures in memory, writes no raw coordinate files, and emits compact review-only evidence.

New artifact:

- `artifacts/research_lanes/epk_sibling_controls/atp_grasp_bounded_control_screen_20260520.json`

Updated helper:

- `tools/research_lanes/epk_sibling_controls/askha_control_screen.py`

## Results

| family | rows reviewed | gamma/metal controls | weak-rule counterexamples | product-state metal rows |
| --- | ---: | ---: | ---: | ---: |
| ATP-grasp | 72 | 25 | 21 | 24 |

The weak-rule counterexamples are:

`3R5F`, `5C1O`, `4L1K`, `6U1D`, `6U1E`, `6U1F`, `6U1G`, `4CVL`, `4CVM`, `9DQW`, `1M0W`, `1KJ8`, `1EZ1`, `1EYZ`, `1KJ9`, `1KJI`, `2D32`, `7WAD`, `4QF5`, `7WAF`, `4QDI`.

Breakdown:

- 19 ATP-grasp controls hit the weak nearest gamma-to-protein-hydroxyl rule at <=6A.
- 8 ATP-grasp controls hit the weak nearest gamma-to-nonpolymer-oxygen rule at <=6A.
- 7 ATP-grasp product-state rows carry ADP/UDP plus metal and phosphate/phosphoryl-mimic ligands: `1EHI`, `1IOV`, `1IOW`, `2DLN`, `6U1H`, `6VR8`, `5DOU`.

The existing unified review-only scorer already blocks the prior ATP-grasp rows `3R5F` and `5C1O`; the 19 newly surfaced weak-rule counterexamples were not production-scored. This run therefore falsifies weak distance-only / nearest-oxygen ePK rules for the broader ATP-grasp surface, but does not claim a production scorer or threshold.

## Safety notes

No production label registries, fingerprint registries, migration files, or git history were edited. No labels were imported, no thresholds were calibrated, no ePK production score was claimed, and no raw coordinate dumps were written.

`git fetch origin` and `git pull --ff-only origin research/epk-sibling-controls` still fail because the linked worktree cannot open `.git/worktrees/catalytic-earth-epk-sibling-controls/FETCH_HEAD` (`Operation not permitted`). `git ls-remote` showed the remote branch hash matched local `HEAD` before this run's uncommitted lane edits, but remote-tracking refs could not be refreshed. A direct write probe into the linked-worktree git metadata also failed. `git add` then failed creating `.git/worktrees/catalytic-earth-epk-sibling-controls/index.lock` (`Operation not permitted`), so commit/push could not be completed from this sandbox.

## Next query

Rerun ATP-grasp with an explicit phosphorylated-acceptor/product-state branch for ADP plus phosphate or phosphorylated nonpolymer controls, starting from `1EHI`, `1IOV`, `1IOW`, `2DLN`, `6U1H`, `6VR8`, and `5DOU`.
