# Foldseek readiness note

Recorded: 2026-05-14T03:05:45Z
Updated: 2026-05-14T09:01:28Z

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

TM-score split remains blocked on materializing the remaining selected
PDB/AlphaFold coordinate files and adding a full Foldseek-backed split builder.
The expanded40 signal proves the backend can produce a larger staged-coordinate
partial signal with capped-search execution and raw-name mapping aligned, but
it does not satisfy the full accepted-registry TM-score holdout or the `<0.7`
train/test target. The readiness and partial TM signal artifacts are
non-countable review evidence only. The exact bounded readiness command is:

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
  --out artifacts/v3_foldseek_tm_score_signal_1000_expanded40.json
```
