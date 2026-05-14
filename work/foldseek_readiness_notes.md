# Foldseek readiness note

Recorded: 2026-05-14T03:05:45Z
Updated: 2026-05-14T09:01:28Z
Delegated slice update: 2026-05-14T10:02:47Z
All-materializable sidecar update: 2026-05-14T10:45:00Z
Expanded60 TM signal update: 2026-05-14T13:48:04Z
Expanded80 TM signal update: 2026-05-14T16:11:42Z
Expanded100 TM signal update: 2026-05-14T17:24:58Z
Target-failure audit update: 2026-05-14T17:58:00Z

Status:

- `foldseek` was absent from the default `PATH`.
- Homebrew 5.1.11 is present, but `brew info foldseek` reported no available
  formula and `brew search foldseek` only returned `folderify`.
- Conda 25.1.1 is present. The default Conda cache path under
  `~/Library/Caches/conda-anaconda-tos` is not writable from this sandbox, so
  the direct Bioconda lookup failed with `CondaToSPermissionError`.
- Redirecting Conda home and package cache to `/private/tmp` allowed Bioconda
  lookup and an isolated install:
  `/private/tmp/catalytic-foldseek-env/bin/foldseek version` reports
  `10.941cd33`.

Current TM-score readiness:

- The 1,025 geometry artifact has 1,002 entries, 998 entries with selected PDB
  identifiers, and 963 `ok` geometry rows, but no `structure_path`,
  `mmcif_path`, `cif_path`, or similar coordinate-file fields.
- The 1,025 graph artifact has 22,440 structure nodes, including 21,399
  `pdb:` nodes and 1,041 `alphafold:` nodes, but no local coordinate paths.
- `artifacts/v3_foldseek_coordinate_readiness_1000.json` now records a
  review-only coordinate-readiness pass over the accepted 1,000 context. It
  identifies 678 evaluated rows, 676 rows with supported selected PDB
  coordinates, two rows with missing selected structures (`m_csa:372` and
  `m_csa:501`), and no fetch failures in the bounded materialization pass.
- The readiness pass stages 25 deterministic selected PDB mmCIF files under
  `artifacts/v3_foldseek_coordinates_1000/`.
- `artifacts/v3_foldseek_coordinate_readiness_1000_expanded100.json` expands
  the same readiness path to 100 deterministic selected PDB mmCIF sidecars in
  the same directory, with 0 fetch failures and 572 supported selected
  structures still unstaged behind the cap.
- `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`
  stages all currently materializable supported selected coordinates for the
  accepted 1,000 context: 672 unique supported selected PDB mmCIF sidecars,
  676 coordinate-materializable evaluated rows, 0 fetch failures, and 0
  supported selected structures left unstaged. It now explicitly records
  `m_csa:372` and `m_csa:501` as Foldseek coordinate exclusions because both
  rows have `geometry_status=no_structure_positions` and
  `selected_structure_id=null` in the current evidence. It removes the
  unstaged selected-coordinate sidecar blocker, but remains review-only and
  non-countable with `tm_score_split_computed=false` and
  `full_tm_score_split_computed=false`. The remaining blockers are the still
  unrun full Foldseek/TM-score split/target check and reporting the exclusions
  before any full-holdout claim.
- `artifacts/v3_foldseek_tm_score_signal_1000_staged25.json` adds a bounded
  Foldseek `easy-search` signal over only those staged sidecars. It records
  25 staged coordinates, 1,840 pair rows, 1,840 mapped rows, 532 staged
  heldout/in-distribution pair rows, and max observed staged train/test TM
  signal `0.6426` against the `<0.7` target. It is review-only evidence with
  0 countable/import-ready rows and keeps both `tm_score_split_computed=false`
  and `full_tm_score_split_computed=false`.
- `artifacts/v3_foldseek_tm_score_signal_1000_expanded40.json` now records a
  completed bounded expanded Foldseek `easy-search` signal over a capped
  40-coordinate selected-coordinate directory. It records 5,699 pair rows, all
  5,699 safely mapped rows, 183 heldout pair rows, 1,633
  heldout/in-distribution train/test rows, max observed train/test TM score
  `0.7515`, 0 unmapped raw Foldseek names, and 0 countable/import-ready rows.
  This removes the staged25-only proof blocker and the expanded40 raw-name
  mapping blocker, but it remains partial, review-only, non-countable, and not
  import-ready. The computed subset does not achieve the `<0.7` target, and both
  `tm_score_split_computed=false` and `full_tm_score_split_computed=false`
  remain true.
- `artifacts/v3_foldseek_tm_score_signal_1000_expanded60.json` now records the
  highest-value completed bounded signal from this delegated run. It used
  `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`,
  `/private/tmp/catalytic-foldseek-env/bin/foldseek` version `10.941cd33`,
  `--max-staged-coordinates 60`, and `--prior-staged-coordinate-count 40`.
  Runtime was 777.55 seconds. The artifact records 60 staged coordinates out of
  672 available staged coordinates, 12,329 pair rows, all 12,329 safely mapped,
  457 heldout pair rows, 3,716 heldout/in-distribution train/test rows, 8,156
  in-distribution pair rows, max observed train/test TM score `0.7515`, 0
  unmapped raw Foldseek names, and explicit zero countable/import-ready rows.
  It removes the expanded40 partial-signal ceiling, but remains partial,
  review-only, non-countable, and not import-ready. The computed subset does
  not achieve the `<0.7` target, the cap leaves 612 staged coordinates
  uncomputed, and both `tm_score_split_computed=false` and
  `full_tm_score_split_computed=false` remain true.
- `artifacts/v3_foldseek_tm_score_signal_1000_expanded80.json` now records the
  completed bounded expanded80 signal from a direct run. It used
  `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`,
  `/private/tmp/catalytic-foldseek-env/bin/foldseek` version `10.941cd33`,
  `--max-staged-coordinates 80`, and `--prior-staged-coordinate-count 60`.
  Runtime was 1,232 seconds. The artifact records 80 staged coordinates out of
  672 available staged coordinates, 18,591 pair rows, all 18,591 safely mapped,
  827 heldout pair rows, 5,666 heldout/in-distribution train/test rows, 12,098
  in-distribution pair rows, max observed train/test TM score `0.7515`, 0
  unmapped raw Foldseek names, and explicit zero countable/import-ready rows.
  It removes the expanded60 partial-signal ceiling, but remains partial,
  review-only, non-countable, and not import-ready. The computed subset does
  not achieve the `<0.7` target, the cap leaves 592 staged coordinates
  uncomputed, and both `tm_score_split_computed=false` and
  `full_tm_score_split_computed=false` remain true.
- `artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json` now records the
  latest completed bounded signal from this direct run. It used
  `artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json`,
  `/private/tmp/catalytic-foldseek-env/bin/foldseek` version `10.941cd33`,
  `--max-staged-coordinates 100`, and `--prior-staged-coordinate-count 80`.
  The artifact records 100 staged coordinates out of 672 available staged
  coordinates, 27,542 pair rows, all 27,542 safely mapped, 838 heldout pair
  rows, 7,317 heldout/in-distribution train/test rows,
  19,387 in-distribution pair rows, max observed train/test TM score `0.7515`,
  0 unmapped raw Foldseek names, and explicit zero countable/import-ready rows.
  It removes the expanded80 partial-signal ceiling, but remains partial,
  review-only, non-countable, and not import-ready. The computed subset does
  not achieve the `<0.7` target, the cap leaves 572 staged coordinates
  uncomputed, and both `tm_score_split_computed=false` and
  `full_tm_score_split_computed=false` remain true.
- `artifacts/v3_foldseek_tm_score_target_failure_audit_1000.json` now records
  the exact current-split target failure exposed by the expanded100 signal. It
  finds 48 train/test chain-level rows at or above the `<0.7` target, all from
  one unique structure pair: `m_csa:33`/`m_csa:34` mapped to
  `pdb:1JC5`/`pdb:1MPY`, with max pair TM-score `0.7515`. This audit does not
  run Foldseek and does not claim a full split; it removes ambiguity about the
  current sequence-holdout split by showing that the target already fails in
  the computed subset. The full holdout claim remains forbidden until split
  repair or explicit exclusion review is done.
- The TM-score signal builder now records explicit partial/full coverage
  semantics for future artifacts: `tm_score_signal_coverage_status`,
  `full_tm_score_holdout_claim_permitted=false`,
  `full_tm_score_holdout_claim_blockers`,
  `remaining_to_full_signal_structure_count`,
  `remaining_uncomputed_staged_coordinate_count`, and optional
  `prior_staged_coordinate_count`/`staged_coordinate_count_exceeds_prior`
  metadata. These fields are intended to prevent a bounded partial signal from
  being mistaken for a full Foldseek-backed TM-score holdout.
TM-score split remains blocked on an uncapped full Foldseek-backed split/signal
over the materialized coordinate set, with the `m_csa:372` and `m_csa:501`
coordinate exclusions reported. The expanded100 signal proves the backend
can produce a larger all-materializable-readiness-derived staged-coordinate
partial signal with capped-search execution and raw-name mapping aligned, but
it does not satisfy the full accepted-registry TM-score holdout or the `<0.7`
train/test target. The readiness and partial TM signal artifacts are
non-countable review evidence only. The new metadata hardening narrows the
SPOF/review blocker by making partial-vs-full TM-score claim safety explicit
and by recording exact zero countable/import-ready row aliases; it does not
remove the full split blocker. The exact bounded readiness command is:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-coordinate-readiness \
  --slice-id 1000 \
  --retrieval artifacts/v3_geometry_retrieval_1000.json \
  --geometry artifacts/v3_geometry_features_1000.json \
  --sequence-holdout artifacts/v3_sequence_distance_holdout_eval_1000.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --coordinate-dir artifacts/v3_foldseek_coordinates_1000 \
  --max-coordinate-files 25 \
  --out artifacts/v3_foldseek_coordinate_readiness_1000.json
```

The expanded coordinate-readiness command is:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-coordinate-readiness \
  --slice-id 1000 \
  --retrieval artifacts/v3_geometry_retrieval_1000.json \
  --geometry artifacts/v3_geometry_features_1000.json \
  --sequence-holdout artifacts/v3_sequence_distance_holdout_eval_1000.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --coordinate-dir artifacts/v3_foldseek_coordinates_1000 \
  --max-coordinate-files 100 \
  --out artifacts/v3_foldseek_coordinate_readiness_1000_expanded100.json
```

The all-materializable coordinate-readiness command is:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-coordinate-readiness \
  --slice-id 1000 \
  --retrieval artifacts/v3_geometry_retrieval_1000.json \
  --geometry artifacts/v3_geometry_features_1000.json \
  --sequence-holdout artifacts/v3_sequence_distance_holdout_eval_1000.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --coordinate-dir artifacts/v3_foldseek_coordinates_1000 \
  --max-coordinate-files 676 \
  --out artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json
```

The exact partial staged-coordinate TM signal command is:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --out artifacts/v3_foldseek_tm_score_signal_1000_staged25.json
```

The completed expanded40 partial signal used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_expanded100.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --max-staged-coordinates 40 \
  --prior-staged-coordinate-count 25 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_expanded40.json
```

The completed expanded60 partial signal used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --max-staged-coordinates 60 \
  --prior-staged-coordinate-count 40 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_expanded60.json
```

The completed expanded80 partial signal used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --max-staged-coordinates 80 \
  --prior-staged-coordinate-count 60 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_expanded80.json
```

The target-failure audit used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-foldseek-tm-score-target-failure \
  --signal artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json \
  --threshold 0.7 \
  --max-blocking-pairs 20 \
  --out artifacts/v3_foldseek_tm_score_target_failure_audit_1000.json
```

The completed expanded100 partial signal used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_all_materializable.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --max-staged-coordinates 100 \
  --prior-staged-coordinate-count 80 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_expanded100.json
```
