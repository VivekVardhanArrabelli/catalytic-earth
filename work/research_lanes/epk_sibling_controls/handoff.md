# ePK sibling controls handoff

Run started: 2026-05-20T14:16:23Z
Run ended: 2026-05-20T14:32:53Z

Primary outcome: `counterexample_found`

## What changed

Added a lane-only bounded source-free control screen for the under-covered ATP/Mg phosphoryl-transfer sibling families. The helper fetches RCSB mmCIF files in memory, writes no raw coordinate dumps, and emits compact local ligand/coordinate summaries only.

New artifacts:

- `artifacts/research_lanes/epk_sibling_controls/askha_bounded_control_screen_20260520.json`
- `artifacts/research_lanes/epk_sibling_controls/dnk_bounded_control_screen_20260520.json`
- `artifacts/research_lanes/epk_sibling_controls/ghkl_bounded_control_screen_20260520.json`
- `artifacts/research_lanes/epk_sibling_controls/ghmp_bounded_control_screen_20260520.json`

Helper:

- `tools/research_lanes/epk_sibling_controls/askha_control_screen.py`

## Results

| family | rows reviewed | gamma/metal controls | weak nearest-hydroxyl counterexamples |
| --- | ---: | ---: | --- |
| ASKHA | 32 | 4 | `3FGU`, `6PDT`, `5ZQT` |
| dNK | 32 | 1 | `2QQ0` |
| GHKL | 32 | 7 | `1I5A`, `1I5B`, `6BLK`, `3SL2`, `8F71` |
| GHMP | 23 | 2 | `3GON`, `1H74` |

The primary ASKHA control set adds fresh weak-rule counterexamples beyond the prior `3FGU` row: `6PDT` and `5ZQT` have ATP/ANP plus local Mg and protein hydroxyl atoms within 6 angstroms of the gamma atom. These rows break any source-free ePK rule based only on nearest gamma-to-protein-hydroxyl distance.

The existing unified review-only scorer already blocks prior ASKHA rows `3FGU` and `1QHA` through `local_substrate_role_context_present=0`; the new rows were not production-scored. The bounded evidence supports keeping distance-only and nearest-oxygen ePK rules closed, while using substrate-role/nonpolymer-acceptor counteraxes only as review-only diagnostics until calibration gates are cleared.

## Safety notes

No production label registries, fingerprint registries, migration files, or git history were edited. No labels were imported, no thresholds were calibrated, no ePK production score was claimed, and no raw coordinate dumps were written.

Initial `git fetch origin` and `git pull --ff-only origin research/epk-sibling-controls` failed because the linked worktree could not open `.git/worktrees/catalytic-earth-epk-sibling-controls/FETCH_HEAD` (`Operation not permitted`). Local `HEAD` matched the last known upstream ref before edits, but remote freshness could not be verified. `git add` was also blocked on `.git/worktrees/catalytic-earth-epk-sibling-controls/index.lock` (`Operation not permitted`), so commit/push could not be completed from this sandbox.

## Next query

Expand ATP-grasp beyond the two measured rows, or rerun ASKHA/dNK/GHKL/GHMP with a stricter nonpolymer-acceptor counteraxis that separates small-molecule acceptor geometry from ePK protein-substrate geometry.
