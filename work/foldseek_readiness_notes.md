# Foldseek readiness note

Recorded: 2026-05-14T03:05:45Z
Updated: 2026-05-14T09:01:28Z
Delegated slice update: 2026-05-14T10:02:47Z
All-materializable sidecar update: 2026-05-14T10:45:00Z
Expanded60 TM signal update: 2026-05-14T13:48:04Z
Expanded80 TM signal update: 2026-05-14T16:11:42Z
Expanded100 TM signal update: 2026-05-14T17:24:58Z
Target-failure audit update: 2026-05-14T17:58:00Z
Split-repair plan update: 2026-05-14T18:57:00Z
Split-repair projection update: 2026-05-14T19:03:00Z
Sequence-holdout repair-candidate update: 2026-05-14T19:09:00Z
Repaired expanded100 TM signal update: 2026-05-14T20:35:00Z
All-materializable timeout attempt update: 2026-05-14T21:25:00Z
Query-chunk TM signal update: 2026-05-14T22:33:00Z
Query-chunk aggregate and timeout update: 2026-05-14T23:20:00Z
Split-redesign candidate and direct chunk-0 check: 2026-05-15T01:15:00Z
Round-2 split redesign and direct chunk-0 check: 2026-05-15T01:40:00Z
Cluster-first split redesign and subchunk verification: 2026-05-15T04:51:00Z
Cluster-first round-4 verification update: 2026-05-15T05:49:00Z
Cluster-first round-6 verification update: 2026-05-15T06:47:00Z
Cluster-first round-7 timeout/update: 2026-05-15T07:58:00Z
Cluster-first round-19 verification update: 2026-05-15T12:34:47-05:00
Cluster-first round-22 verification update: 2026-05-15T18:33:42Z

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
- Blind query-chunk continuation is no longer the active design. The current
  Foldseek split path is cluster-first: build partition constraints from
  observed `TM >= 0.7` pairs, assign whole connected structural components to
  heldout or in-distribution, then verify bounded query chunks against the
  resulting candidate.
- `artifacts/v3_foldseek_tm_score_cluster_first_split_1000.json` reuses all
  672 staged materializable selected structures as the current structure index.
  It folds the pre-existing blocker evidence into 24 high-TM constraints across
  12 constrained clusters, projects 0 high-TM train/test violations, preserves
  0 sequence-cluster splits, and keeps every row review-only/non-countable.
- The first cluster-first subchunk verification,
  `artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_query_subchunk_006_of_112.json`,
  completes with 14,207 mapped rows and exposes a new `m_csa:38`/`m_csa:118`
  blocker at max train/test TM-score `0.7435`.
- `artifacts/v3_foldseek_tm_score_cluster_first_split_round2_1000.json` folds
  that blocker into the split by moving held-out out-of-scope `m_csa:118` to
  in-distribution. The rerun
  `artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round2_query_subchunk_006_of_112.json`
  passes with 14,207 mapped rows, 2,358 train/test rows, max train/test
  TM-score `0.6509`, and 0 target-violating pairs.
- The paired round-2 subchunk,
  `artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round2_query_subchunk_007_of_112.json`,
  completes with 9,094 mapped rows, 5,449 train/test rows, max train/test
  TM-score `0.8651`, and 16 violating rows across 9 reported structure pairs.
  The aggregate
  `artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round2_query_subchunk_aggregate_006_007_of_112.json`
  keeps that failure explicit.
- The prior handoff split was
  `artifacts/v3_foldseek_tm_score_cluster_first_split_round3_1000.json`; it
  folds the subchunk-007 blockers into 34 high-TM constraints across 14
  constrained clusters, projects 0 remaining known constraint violations,
  preserves 0 sequence-cluster splits, and records 0 countable/import-ready
  rows. Its readiness artifact is
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round3.json`.
- Round-3 verification from that readiness reruns subchunks 006 and 007.
  Subchunk 006 passes with 14,207 mapped rows, 2,356 train/test rows, max
  train/test TM-score `0.6509`, and 0 target-violating pairs. Subchunk 007
  still fails with 9,094 mapped rows, 4,976 train/test rows, max train/test
  TM-score `0.8043`, and one reported blocking structure pair:
  `m_csa:45`/`m_csa:397`.
- Round 4 folds that blocker into 35 high-TM constraints across 14 constrained
  clusters, moves held-out out-of-scope `m_csa:397` to in-distribution, and
  clears subchunk 007 with 9,094 mapped rows, 4,975 train/test rows, max
  train/test TM-score `0.6598`, and 0 target-violating pairs.
- Direct round-4 subchunk 008 then exposes one blocker, `m_csa:54` against
  held-out out-of-scope `m_csa:428`, at max train/test TM-score `0.7205`.
  Round 5 folds that blocker into 36 high-TM constraints, moves `m_csa:428`
  to in-distribution, preserves 0 sequence-cluster splits, and clears
  subchunk 008 with 8,641 mapped rows, 1,532 train/test rows, max train/test
  TM-score `0.6989`, and 0 target-violating pairs.
- Direct round-5 subchunk 009 then exposes one blocker, `m_csa:58` against
  held-out out-of-scope `m_csa:628`, at max train/test TM-score `0.879`.
  The current handoff split is now
  `artifacts/v3_foldseek_tm_score_cluster_first_split_round6_1000.json`; it
  folds that blocker into 37 high-TM constraints across 16 constrained
  clusters, moves `m_csa:628` to in-distribution, preserves 0
  sequence-cluster splits, and records 0 countable/import-ready rows. Its
  readiness artifact is
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round6.json`.
  The direct round-6 subchunk-009 rerun passes with 15,531 mapped rows, 2,939
  train/test rows, max train/test TM-score `0.6699`, and 0 target-violating
  pairs.
- Direct round-6 subchunk 010 times out under the 900-second bound before
  pair rows are emitted. The same query window is split into 3-query
  microchunks. Round-6 microchunk 020 completes with 7,488 mapped rows, 1,319
  train/test rows, max train/test TM-score `0.7116`, and one reported blocker:
  in-distribution `m_csa:63`/`pdb:1CB7` against held-out `m_csa:188`/
  `pdb:1XEL`.
- The current handoff split is now
  `artifacts/v3_foldseek_tm_score_cluster_first_split_round7_1000.json`; it
  folds that blocker into 38 high-TM constraints across 17 constrained
  clusters, moves `m_csa:188` to in-distribution as part of the connected
  high-TM neighborhood, preserves 0 sequence-cluster splits, and records 0
  countable/import-ready rows. Its readiness artifact is
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round7.json`.
  The direct round-7 microchunk-020 rerun times out under the 900-second bound
  before pair rows are emitted. Single-query isolation then verifies the same
  span without a target failure: staged indices 60-62 (`m_csa:61`-`m_csa:63`)
  aggregate to 7,488 mapped rows, 1,311 train/test rows, max train/test
  TM-score `0.6967`, and 0 target-violating pairs, while staged indices 63-65
  (`m_csa:64`-`m_csa:66`) aggregate to 2,190 mapped rows, 378 train/test rows,
  max train/test TM-score `0.5629`, and 0 target-violating pairs. Staged index
  66 (`m_csa:67`) then passes at max train/test TM-score `0.6535`, but staged
  index 67 (`m_csa:68`) exposes one new `m_csa:68`/`m_csa:750` blocker at max
  TM-score `0.7909`. `src/catalytic_earth/generalization.py` now accepts prior
  cluster-first `partition_constraints` as pair-cache evidence, and
  `artifacts/v3_foldseek_tm_score_cluster_first_split_round8_1000.json` folds
  the new pair into 39 high-TM constraints across 18 constrained clusters with
  0 projected violations and 0 sequence-cluster splits. Its readiness artifact
  is `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round8.json`.
  Direct round-8 single-query verification then clears staged indices 68-78
  (`m_csa:69`-`m_csa:79`) in aggregate until staged index 79 (`m_csa:80`)
  exposes two blockers against in-distribution `m_csa:408` and `m_csa:569`,
  with max train/test TM-score `0.8726`. Round 9 folds those blockers into 41
  high-TM constraints across 19 constrained clusters, moves the `m_csa:80`
  high-TM neighborhood to in-distribution, preserves 0 sequence-cluster splits,
  and keeps 0 held-out out-of-scope false non-abstentions. Its readiness
  artifact is
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round9.json`.
  The direct round-9 rerun of staged index 79 plus staged indices 80-83 passes
  in aggregate with 4,434 mapped rows, 763 train/test rows, max train/test
  TM-score `0.6477`, and 0 target-violating pairs. Continuing round-9
  single-query verification clears staged indices 84-95 with 17,189 mapped
  rows, 3,257 train/test rows, max train/test TM-score `0.6579`, and 0
  target-violating pairs. Continuing from index 96 clears staged indices
  96-101 before staged index 102 exposes `m_csa:103`/`pdb:1VAO` versus
  held-out `m_csa:115`/`pdb:1W1O` at max TM-score `0.7653`. The
  cluster-first builder now unions real sequence-identity clusters before
  assignment, and round 10 folds the blocker into 42 high-TM constraints plus
  38 sequence-identity partition constraints while preserving 0
  sequence-cluster splits. Its direct staged-index-102 rerun passes at max
  train/test TM-score `0.6725` with 0 target-violating pairs. Staged index 103
  then exposes `m_csa:104`/`pdb:1C9U` against held-out `m_csa:686`/`pdb:1E1A`
  at max TM-score `0.7633`; round 11 folds that in but the rerun still exposes
  `m_csa:104` against `m_csa:360` and `m_csa:740` at max `0.7317`. Round 12
  folds those two blockers and clears staged index 103 at max `0.6669`, then
  staged index 104 passes at max `0.4496` before staged index 105 exposes a
  larger blocker surface at max `0.8862` with 72 violating rows. Round 13 folds
  that evidence into 48 high-TM constraints, 38 sequence-identity partition
  constraints, 0 projected violations, and 0 sequence-cluster splits. Its
  direct verification clears indices 105-106, then index 107 exposes
  `m_csa:108` at max `0.8826`; round 14 folds that evidence into 60 high-TM
  constraints and reruns index 107 cleanly at max `0.6862`. Index 108 exposes
  `m_csa:109` at max `0.7649`; round 15 folds those blockers and verifies
  indices 107-109 cleanly at max `0.6996`. Index 110 exposes `m_csa:111` at
  max `0.7521`; round 16 folds that evidence into 66 high-TM constraints plus
  38 sequence-identity partition constraints. Its direct index-110 rerun still
  exposes `m_csa:111` versus `m_csa:852` at max `0.7708`; round 17 folds that
  pair, clears index 110 at max `0.6823`, clears index 111 at max `0.564`, and
  then index 112 exposes `m_csa:113` versus held-out `m_csa:131` at max
  `0.7063`. Round 18 folds that pair, but its index-112 rerun exposes a
  larger `m_csa:113` blocker surface against `m_csa:942`, `m_csa:978`, and
  related in-distribution neighbors at max `0.9087`. Round 19 folds that
  evidence into 72 high-TM constraints, clears staged indices 112-113, and
  then exposes `m_csa:115` versus `m_csa:822` at max `0.7338`. Round 20 folds
  that pair, clears staged index 114 at max `0.6732`, and then exposes a
  broader `m_csa:116` surface at max `0.9749`. Round 21 folds that surface
  into 81 high-TM constraints, but its index-115 rerun still exposes
  `m_csa:116` versus held-out `m_csa:67` at max `0.9032`. Round 22 folds the
  remaining pair into 82 high-TM constraints plus 38 sequence-identity
  partition constraints, 0 projected violations, 0 sequence-cluster splits,
  and readiness at
  `artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round22.json`.
  Direct round-22 verification clears staged indices 115-118 in aggregate with
  6,103 mapped rows, 1,319 train/test rows, max train/test TM-score `0.6939`,
  and 0 target-violating pairs. Full TM-score holdout claims remain forbidden
  until the remaining round-22 cluster-first coverage passes or is explicitly
  adjudicated.

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
- `artifacts/v3_foldseek_tm_score_split_repair_plan_1000.json` now turns that
  observed target failure into one concrete review-only repair candidate. The
  plan proposes moving the held-out out-of-scope row `m_csa:34` to
  in-distribution before regenerating the sequence-holdout metrics. It would
  reduce the held-out count from 136 to 135, preserve all 44 held-out in-scope
  rows, and reduce observed blocking pairs in the supplied signal to 0. The
  repair is not applied, the source signal is still partial, the uncapped
  Foldseek-backed split remains uncomputed, and the artifact keeps 0
  countable/import-ready rows.
- `artifacts/v3_foldseek_tm_score_split_repair_projection_1000.json` projects
  the planned move over the existing expanded100 Foldseek rows without mutating
  the sequence holdout. It reclassifies `m_csa:34` as in-distribution in the
  projection only, lowering the computed-subset train/test violations from 48
  to 0 and max train/test TM-score from `0.7515` to `0.6993`. This removes the
  observed computed-subset target blocker only in projection. The actual split
  still needs sequence-holdout regeneration, downstream metric recomputation,
  and an uncapped Foldseek-backed run before any full TM-score holdout claim.
- `artifacts/v3_sequence_distance_holdout_split_repair_candidate_1000.json`
  applies the same move to a candidate copy of the sequence holdout. It moves
  `m_csa:34` from held-out to in-distribution, recomputes held-out count as
  135, preserves all 44 held-out in-scope rows, keeps held-out out-of-scope
  false non-abstentions at 0, and records no remaining held-out overlap with
  the moved `mmseqs30:m_csa:34` cluster. This candidate is not canonical,
  does not rebuild downstream retrieval artifacts, and still forbids a full
  TM-score holdout claim.
- `artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json`
  rebuilds the coordinate-readiness view from the candidate sequence holdout.
  It reuses the all-materializable coordinate sidecar with 672 staged
  coordinates, moves `m_csa:34` to in-distribution, keeps `m_csa:372` and
  `m_csa:501` as explicit coordinate exclusions, records 0 fetch failures, and
  keeps all rows review-only/non-countable.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_expanded100.json`
  reruns the actual Foldseek signal under that candidate split, using
  `/private/tmp/catalytic-foldseek-env/bin/foldseek` version `10.941cd33`,
  `--max-staged-coordinates 100`, and `--prior-staged-coordinate-count 100`.
  The run maps 27,542 pair rows, 646 heldout pair rows, 6,930
  heldout/in-distribution train/test rows, 19,966 in-distribution pair rows,
  and max observed train/test TM-score `0.6993`; the computed subset now
  achieves the `<0.7` target without relying on projection-only metadata. It
  remains capped, review-only, non-countable, and not import-ready because 572
  staged coordinates remain uncomputed and a full split builder has not run.
- `artifacts/v3_foldseek_tm_score_target_failure_audit_1000_split_repair_candidate_expanded100.json`
  confirms 0 target-violating train/test pairs for the repaired expanded100
  computed subset. It keeps `full_tm_score_holdout_claim_permitted=false`
  because the source signal is still capped, two evaluated rows lack supported
  selected coordinates, and the full all-materializable Foldseek/TM-score split
  remains uncomputed.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json`
  now records a completed all-materializable staged-coordinate Foldseek signal.
  It used all 672 staged materializable coordinates, Foldseek `10.941cd33`,
  and `--threads 4`, maps 952,922 pair rows and 274,241 train/test rows, and
  fails the `<0.7` target at max train/test TM-score `0.9749` with 4,715
  target-violating train/test rows. This removes the prior all-materializable
  runtime ambiguity, but the artifact remains review-only, non-countable, not
  import-ready, and non-claiming because `m_csa:372` and `m_csa:501` remain
  coordinate exclusions and the artifact is a signal rather than a canonical
  full split.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000_of_056.json`
  and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_001_of_056.json`
  record the first two direct resumable all-materializable query chunks. They
  used the repaired candidate readiness artifact, 12 deterministic query
  coordinates per chunk, all 672 staged materializable target coordinates,
  Foldseek `10.941cd33`, `--threads 4`, and a 900-second runtime bound per
  chunk. The chunks completed with 28,251 mapped pair rows, 9,142
  heldout/in-distribution train/test rows, max observed train/test TM-score
  `0.8957`, 70 total target-violating row-level pairs, and per-chunk unique
  target-violating structure-pair counts of six and seven. This removes the
  single all-at-once Foldseek runtime SPOF by proving the query-chunk path, but
  it also exposes new exact target-failure evidence beyond the repaired
  expanded100 cap. They remain chunks 1-2/56, review-only, non-countable, not
  import-ready, and keep
  `full_tm_score_holdout_claim_permitted=false`.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_of_056.json`
  attempts the next deterministic 12-query chunk with the same repaired
  candidate readiness artifact, all 672 staged materializable targets,
  Foldseek `10.941cd33`, `--threads 4`, and a 900-second runtime bound. It
  times out before Foldseek emits pair rows, so it records 0 pair rows, no max
  train/test TM-score, and no target pass. The aggregate artifact
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_of_056.json`
  now summarizes chunks 0-2: 3 attempted chunks, 2 completed chunks, 24
  completed query coordinates, 28,251 mapped pair rows, 9,142 train/test rows,
  max train/test TM-score `0.8957`, 70 target-violating row-level pairs, 13
  reported target-violating structure pairs, and 54 non-completed chunks. This
  removes the first chunk-aggregation ambiguity but not the full-holdout
  blocker: the completed chunks fail `<0.7`, chunk 2 exceeds the routine
  runtime bound, `m_csa:372` and `m_csa:501` remain coordinate exclusions, and
  `full_tm_score_holdout_claim_permitted=false`.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_retry_1800_of_056.json`
  retries chunk 2 with the same 12-query/all-target command shape and a
  1,800-second runtime bound. It completes with 12,639 mapped pair rows, 3,216
  train/test rows, max train/test TM-score `0.8427`, and 6 target-violating
  row-level pairs across 2 reported structure pairs. The completed-retry
  aggregate
  `artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_retry_1800_of_056.json`
  records 3/56 completed chunks, 36 completed query coordinates, 40,890 mapped
  pair rows, 12,358 train/test rows, max train/test TM-score `0.8957`, 76
  target-violating row-level pairs, 15 reported target-violating structure
  pairs, and 53 non-completed chunks. The query-chunk split-repair plan
  `artifacts/v3_foldseek_tm_score_query_chunk_split_repair_plan_1000.json`
  classifies those blockers into 9 conservative held-out out-of-scope repair
  candidates and 6 manual split-redesign blockers involving held-out in-scope
  rows (`m_csa:20`, `m_csa:497`, and `m_csa:895`). This removes the chunk-2
  runtime ambiguity but keeps the full-holdout blocker active: the completed
  chunks fail `<0.7`, most query chunks remain uncomputed, `m_csa:372` and
  `m_csa:501` remain coordinate exclusions, and
  `full_tm_score_holdout_claim_permitted=false`.
- `artifacts/v3_sequence_distance_holdout_split_redesign_candidate_1000.json`
  applies the first review-only split-redesign candidate over the completed
  query-chunk blockers. It moves 9 held-out out-of-scope rows to
  in-distribution and moves 6 high-TM train neighbors to heldout to preserve
  held-out in-scope blockers (`m_csa:20`, `m_csa:497`, and `m_csa:895`).
  Projection over the 15 observed blockers drops the observed blocker count to
  0, keeps sequence-identity cluster splits at 0, increases held-out in-scope
  rows from 44 to 50, and preserves 0 held-out out-of-scope false
  non-abstentions. This candidate is not canonical and remains review-only.
- `artifacts/v3_foldseek_coordinate_readiness_1000_split_redesign_candidate.json`
  rebuilds coordinate readiness from that redesigned candidate holdout. It
  reuses all 672 staged materializable coordinates, keeps `m_csa:372` and
  `m_csa:501` as coordinate exclusions, and keeps all rows non-countable.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_query_chunk_000_of_056.json`
  directly reruns chunk 0 against the redesigned partition with Foldseek
  `10.941cd33`, 12 query coordinates, all 672 staged targets, `--threads 4`,
  and a 900-second cap. It completes but fails the target: 16,475 mapped pair
  rows, 6,909 train/test rows, max train/test TM-score `0.926`, and 15
  target-violating row-level pairs across 4 reported structure pairs.
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_query_chunk_aggregate_000_of_056.json`
  records the same single-chunk aggregate.
- `artifacts/v3_foldseek_tm_score_split_redesign_candidate_query_chunk_repair_plan_1000.json`
  classifies the new direct blocker: 4/4 observed blocking pairs are manual
  split-redesign blockers involving held-out in-scope `m_csa:6` against
  `m_csa:277`, `m_csa:378`, `m_csa:320`, and `m_csa:108`. There are 0
  conservative held-out out-of-scope repair candidates in this direct chunk-0
  result. This invalidates the projection-only redesign as a sufficient fix
  while narrowing the next split-redesign target.
- `artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round2_1000.json`
  applies that narrowed repair as a second review-only redesign candidate by
  moving `m_csa:277`, `m_csa:378`, `m_csa:320`, and `m_csa:108` to heldout.
  It projects 0 observed blockers, keeps sequence-identity cluster splits at
  0, increases held-out in-scope rows to 54, and preserves 0 held-out
  out-of-scope false non-abstentions. It is still not canonical.
- `artifacts/v3_foldseek_coordinate_readiness_1000_split_redesign_candidate_round2.json`
  rebuilds readiness from the round-2 split and reuses all 672 staged
  materializable coordinates with the same two coordinate exclusions.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_000_of_056.json`
  directly reruns chunk 0 against the round-2 partition with Foldseek
  `10.941cd33`, 12 query coordinates, all 672 staged targets, `--threads 4`,
  and a 900-second cap. It completes and clears the target for chunk 0:
  16,475 mapped pair rows, 6,939 train/test rows, max train/test TM-score
  `0.695`, and 0 target-violating pairs.
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_aggregate_000_of_056.json`
  records the same 1/56 completed chunk result. This removes the redesigned
  chunk-0 blocker but not the full split blocker: 55 redesigned chunks remain
  uncomputed, coordinate exclusions remain, and the split is still candidate
  review evidence only.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_001_of_056.json`
  directly continues the round-2 candidate into chunk 1 with Foldseek
  `10.941cd33`, 12 query coordinates, all 672 staged targets, `--threads 4`,
  and a 900-second cap. It completes but fails the target with 11,776 mapped
  rows, 4,154 train/test rows, max train/test TM-score `0.8182`, and 12
  target-violating row-level pairs across 4 reported structure pairs. The
  aggregate
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round2_query_chunk_aggregate_000_001_of_056.json`
  records 2/56 completed round-2 chunks, 28,251 mapped rows, 11,093
  train/test rows, max train/test TM-score `0.8182`, and 12 target-violating
  rows.
- `artifacts/v3_foldseek_tm_score_split_redesign_candidate_round2_query_chunk_repair_plan_1000.json`
  classifies the round-2 chunk-1 blocker. There are 0 conservative held-out
  out-of-scope repair candidates and 4 manual split-redesign blockers
  involving held-out in-scope `m_csa:15` and `m_csa:16` against train
  neighbors `m_csa:258` and `m_csa:157`.
- `artifacts/v3_sequence_distance_holdout_split_redesign_candidate_round3_1000.json`
  applies the next review-only redesign by moving `m_csa:157` and `m_csa:258`
  to heldout. It projects 0 observed blockers, preserves 0 sequence-cluster
  splits, increases heldout rows to 138, keeps held-out in-scope rows at 56,
  and preserves 0 held-out out-of-scope false non-abstentions.
- `artifacts/v3_foldseek_coordinate_readiness_1000_split_redesign_candidate_round3.json`
  rebuilds readiness from the round-3 split and reuses all 672 staged
  materializable coordinates with the same `m_csa:372` and `m_csa:501`
  coordinate exclusions.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_000_of_056.json`
  and
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_001_of_056.json`
  directly rerun chunks 0 and 1 against the round-3 partition. Both complete
  with Foldseek `10.941cd33`, 12 query coordinates per chunk, all 672 staged
  targets, `--threads 4`, and a 900-second cap. Chunk 0 records 16,475 mapped
  rows, 6,930 train/test rows, max train/test TM-score `0.695`, and 0
  target-violating pairs. Chunk 1 records 11,776 mapped rows, 4,157
  train/test rows, max train/test TM-score `0.6598`, and 0 target-violating
  pairs. The aggregate
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_001_of_056.json`
  records 2/56 completed round-3 chunks, 24 query coordinates, 28,251 mapped
  rows, 11,087 train/test rows, max train/test TM-score `0.695`, and 0
  target-violating pairs. This removes the first two round-3 query-chunk
  blockers but not the full split blocker: 54 chunks remain uncomputed,
  coordinate exclusions remain, and the split is still candidate review
  evidence only.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_002_of_056.json`
  continues the same direct round-3 query-chunk path. It completes with
  Foldseek `10.941cd33`, 12 query coordinates against all 672 staged targets,
  `--threads 4`, and a 900-second cap; it records 12,639 mapped rows, 2,385
  train/test rows, max train/test TM-score `0.584`, and 0 target-violating
  pairs. The aggregate
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_002_of_056.json`
  now records 3/56 completed round-3 chunks, 36 query coordinates, 40,890
  mapped rows, 13,472 train/test rows, max train/test TM-score `0.695`, and
  0 target-violating pairs. This removes the first three round-3 query-chunk
  blockers but not the full split blocker: 53 chunks remain uncomputed,
  coordinate exclusions remain, and the split is still candidate review
  evidence only.
- `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_003_of_056.json`
  attempts the next direct round-3 chunk with the same Foldseek `10.941cd33`,
  12-query/all-target command shape, `--threads 4`, and 900-second cap. It
  times out before pair rows are emitted, so it records 0 mapped rows, no max
  train/test TM-score, and no target pass. The aggregate
  `artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_003_of_056.json`
  preserves the timeout status while keeping the completed chunks 0-2 metrics:
  3/56 completed chunks, 36 completed query coordinates, 40,890 mapped rows,
  13,472 train/test rows, max train/test TM-score `0.695`, and 0
  target-violating pairs among completed chunks. Chunk 3 now needs a longer
  retry or smaller query slice before chunked Foldseek coverage can advance.
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

The repaired split coordinate-readiness command used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-coordinate-readiness \
  --slice-id 1000 \
  --retrieval artifacts/v3_geometry_retrieval_1000.json \
  --labels data/registries/curated_mechanism_labels.json \
  --geometry artifacts/v3_geometry_features_1000.json \
  --sequence-holdout artifacts/v3_sequence_distance_holdout_split_repair_candidate_1000.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --coordinate-dir artifacts/v3_foldseek_coordinates_1000 \
  --max-coordinate-files 676 \
  --out artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json
```

The repaired expanded100 partial signal used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --max-staged-coordinates 100 \
  --prior-staged-coordinate-count 100 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_expanded100.json
```

The repaired expanded100 target audit used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-foldseek-tm-score-target-failure \
  --signal artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_expanded100.json \
  --threshold 0.7 \
  --max-blocking-pairs 20 \
  --out artifacts/v3_foldseek_tm_score_target_failure_audit_1000_split_repair_candidate_expanded100.json
```

The direct all-materializable timeout attempt used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-all-materializable-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --threads 4 \
  --max-runtime-seconds 1500 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json
```

The first resumable query-chunk signals used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-query-chunk-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --chunk-index 0 \
  --chunk-size 12 \
  --threads 4 \
  --max-runtime-seconds 900 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000_of_056.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-query-chunk-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --chunk-index 1 \
  --chunk-size 12 \
  --threads 4 \
  --max-runtime-seconds 900 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_001_of_056.json
```

The timeout chunk and aggregate used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-query-chunk-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --chunk-index 2 \
  --chunk-size 12 \
  --threads 4 \
  --max-runtime-seconds 900 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_of_056.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli aggregate-foldseek-tm-score-query-chunks \
  --slice-id 1000 \
  --chunks artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000_of_056.json \
    artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_001_of_056.json \
    artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_of_056.json \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_of_056.json
```

The completed chunk-2 retry, retry aggregate, and query-chunk split-repair
adjudication used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-query-chunk-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_split_repair_candidate.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --chunk-index 2 \
  --chunk-size 12 \
  --threads 4 \
  --max-runtime-seconds 1800 \
  --max-reported-pairs 30 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_retry_1800_of_056.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli aggregate-foldseek-tm-score-query-chunks \
  --slice-id 1000 \
  --chunks artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_000_of_056.json \
    artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_001_of_056.json \
    artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_002_retry_1800_of_056.json \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_retry_1800_of_056.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-foldseek-tm-score-split-repair \
  --target-failure artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_query_chunk_aggregate_000_002_retry_1800_of_056.json \
  --sequence-holdout artifacts/v3_sequence_distance_holdout_split_repair_candidate_1000.json \
  --out artifacts/v3_foldseek_tm_score_query_chunk_split_repair_plan_1000.json
```

The round-3 redesigned chunk-2 signal and 0-2 aggregate used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-query-chunk-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_split_redesign_candidate_round3.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --chunk-index 2 \
  --chunk-size 12 \
  --threads 4 \
  --max-runtime-seconds 900 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_002_of_056.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli aggregate-foldseek-tm-score-query-chunks \
  --slice-id 1000 \
  --chunks artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_000_of_056.json \
    artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_001_of_056.json \
    artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_002_of_056.json \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_002_of_056.json
```

The round-3 redesigned chunk-3 timeout artifact and 0-3 aggregate used:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-foldseek-tm-score-query-chunk-signal \
  --slice-id 1000 \
  --readiness artifacts/v3_foldseek_coordinate_readiness_1000_split_redesign_candidate_round3.json \
  --foldseek-binary /private/tmp/catalytic-foldseek-env/bin/foldseek \
  --chunk-index 3 \
  --chunk-size 12 \
  --threads 4 \
  --max-runtime-seconds 900 \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_003_of_056.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli aggregate-foldseek-tm-score-query-chunks \
  --slice-id 1000 \
  --chunks artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_000_of_056.json \
    artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_001_of_056.json \
    artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_002_of_056.json \
    artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_003_of_056.json \
  --out artifacts/v3_foldseek_tm_score_signal_1000_split_redesign_candidate_round3_query_chunk_aggregate_000_003_of_056.json
```
