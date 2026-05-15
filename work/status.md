# Catalytic Earth Status

Generated from `work/progress_log.jsonl`.

## Time

- Entries: 117
- Measured elapsed time: 4232.4 minutes (70.54 hours)
- Estimated/planned time: 405 minutes (6.75 hours)
- Note: entries before timing instrumentation are estimates, not clock measurements.

## Time By Stage

- external-transfer-spof-hardening: 25.3 measured minutes (0.42 hours)
- ops: 13.4 measured minutes (0.22 hours)
- post-mcsa-spof-hardening: 1586.1 measured minutes (26.44 hours)
- post-v2: 2542.9 measured minutes (42.38 hours)
- v3: 64.8 measured minutes (1.08 hours)
- ops: 45 estimated minutes (0.75 hours)
- post-v2: 180 estimated minutes (3.00 hours)
- v0: 55 estimated minutes (0.92 hours)
- v1: 55 estimated minutes (0.92 hours)
- v2: 70 estimated minutes (1.17 hours)

## Progress Counters

- Artifact references logged: 1337
- Evidence references logged: 1009

## Recent Entries

### 2026-05-15T07:58:35.468841+00:00 - post-mcsa-spof-hardening

- Task: Foldseek cluster-first round7 timeout isolation
- Time mode: measured
- Measured minutes: 53.567
- Started: 2026-05-15T07:04:30Z
- Ended: 2026-05-15T07:58:04Z
- Artifacts: tests/test_generalization.py, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round6_query_subchunk_010_of_112.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round6_query_microchunk_020_of_224.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round7_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round7.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_microchunk_020_of_224.json, README.md, docs/external_source_transfer.md, work/foldseek_readiness_notes.md, work/handoff.md, work/scope.md
- Evidence: startup 387 unit tests passed, validate passed with 679 curated labels, round6 subchunk 010 timed out under 900 seconds with 0 pair rows, round6 microchunk 020 completed with max TM 0.7116 and one m_csa:63/m_csa:188 blocker, round7 cluster-first candidate has 38 high-TM constraints and 0 sequence-cluster splits, round7 microchunk 020 timed out under 900 seconds, git diff check passed, JSON artifacts parsed, final 391 unit tests passed, validate passed, compileall passed
- Notes: Normal locked direct run with no delegation. No M-CSA-only count growth and no external import. Full TM-score holdout claim remains forbidden; next work should isolate round7 microchunk 020 with single-query checks before continuing.

### 2026-05-15T08:46:02.937530+00:00 - post-mcsa-spof-hardening

- Task: Foldseek cluster-first round8 single-query isolation
- Time mode: measured
- Measured minutes: 40.233
- Started: 2026-05-15T08:05:27Z
- Ended: 2026-05-15T08:45:41Z
- Artifacts: src/catalytic_earth/generalization.py, tests/test_generalization.py, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_060_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_061_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_062_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_063_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_064_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_065_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_066_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_067_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_aggregate_060_062_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_aggregate_063_065_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round7_query_single_aggregate_066_067_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round8_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round8.json, README.md, docs/external_source_transfer.md, work/foldseek_readiness_notes.md, work/handoff.md, work/scope.md
- Evidence: startup 391 unit tests passed, validate passed with 679 curated labels, round7 single-query indices 60-62 passed in aggregate at max TM 0.6967, round7 single-query indices 63-65 passed in aggregate at max TM 0.5629, round7 staged index 66 passed at max TM 0.6535, round7 staged index 67 exposed m_csa:68/m_csa:750 at max TM 0.7909, round8 cluster-first candidate has 39 high-TM constraints, 18 constrained clusters, 0 projected violations, and 0 sequence-cluster splits, 0 countable labels and 0 import-ready rows, JSON artifacts parsed, focused artifact/cache tests passed, git diff check passed, final 396 unit tests passed, final validate passed, compileall passed
- Notes: Normal locked direct run with no delegation. No M-CSA-only count growth and no external import. Full TM-score holdout claim remains forbidden.

### 2026-05-15T13:32:19.332566+00:00 - post-mcsa-spof-hardening

- Task: Foldseek cluster-first round9 verification
- Time mode: measured
- Measured minutes: 43.733
- Started: 2026-05-15T12:48:12Z
- Ended: 2026-05-15T13:31:56Z
- Artifacts: tests/test_generalization.py, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_068_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_069_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_070_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_071_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_072_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_073_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_074_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_075_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_076_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_077_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_078_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_079_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round8_query_single_aggregate_068_079_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round9_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round9.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_079_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_080_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_081_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_082_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_083_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_aggregate_079_083_of_672.json, README.md, docs/external_source_transfer.md, work/foldseek_readiness_notes.md, work/handoff.md, work/scope.md
- Evidence: startup 396 unit tests passed, validate passed with 679 curated labels, round8 single-query indices 68-78 passed before index 79 exposed m_csa:80 versus m_csa:408/m_csa:569 at max TM 0.8726, round9 cluster-first candidate has 41 high-TM constraints and 0 sequence-cluster splits, round9 single-query indices 79-83 passed in aggregate at max TM 0.6477 with 0 target-violating pairs, 0 countable labels and 0 import-ready rows, JSON artifacts parsed, focused artifact tests passed
- Notes: Normal locked direct run with no delegation. No M-CSA-only count growth and no external import. Full TM-score holdout claim remains forbidden.

### 2026-05-15T14:31:01.833373+00:00 - post-mcsa-spof-hardening

- Task: Foldseek cluster-first round9 continuation
- Time mode: measured
- Measured minutes: 40.433
- Started: 2026-05-15T13:50:06Z
- Ended: 2026-05-15T14:30:32Z
- Artifacts: tests/test_generalization.py, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_084_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_085_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_086_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_087_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_088_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_089_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_090_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_091_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_092_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_093_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_094_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_095_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_aggregate_084_095_of_672.json, README.md, docs/external_source_transfer.md, work/foldseek_readiness_notes.md, work/handoff.md, work/scope.md
- Evidence: startup 400 unit tests passed, validate passed with 679 curated labels, round9 single-query indices 84-95 completed with 17189 mapped pair rows, 3257 train/test rows, max TM 0.6579, 0 target-violating pairs, 0 countable labels, 0 import-ready rows
- Notes: Normal locked direct run with no delegation. No M-CSA-only count growth and no external import. Full TM-score holdout claim remains forbidden.

### 2026-05-15T15:32:34.144335+00:00 - post-mcsa-spof-hardening

- Task: Foldseek cluster-first sequence-preserving verification
- Time mode: measured
- Measured minutes: 39.8
- Started: 2026-05-15T14:52:02Z
- Ended: 2026-05-15T15:31:50Z
- Artifacts: src/catalytic_earth/generalization.py, tests/test_generalization.py, artifacts/v3_foldseek_tm_score_signal_1000_split_repair_candidate_all_materializable.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_096_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_097_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_098_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_099_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_100_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_101_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_102_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round9_query_single_aggregate_096_102_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round10_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round10.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round10_query_single_102_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round10_query_single_aggregate_102_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round10_query_single_103_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round10_query_single_aggregate_102_103_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round11_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round11.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round11_query_single_103_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round11_query_single_aggregate_103_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round12_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round12.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round12_query_single_103_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round12_query_single_104_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round12_query_single_105_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round12_query_single_aggregate_103_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round12_query_single_aggregate_103_105_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round13_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round13.json, README.md, docs/external_source_transfer.md, work/foldseek_readiness_notes.md, work/handoff.md, work/scope.md
- Evidence: startup 401 unit tests passed, validate passed with 679 curated labels, all-materializable signal completed but failed target at max TM 0.9749, round9 indices 96-101 passed before index 102 blocker at max TM 0.7653, round12 cleared index 103 at max TM 0.6669, index 104 passed at max TM 0.4496, index 105 blocker folded into round13 at max TM 0.8862, round13 has 48 high-TM constraints and 0 sequence-cluster splits, 0 countable labels, 0 import-ready rows
- Notes: Normal locked direct run with no delegation. No M-CSA-only count growth and no external import. Full TM-score holdout claim remains forbidden.

### 2026-05-15T16:41:11.445104+00:00 - post-mcsa-spof-hardening

- Task: Foldseek cluster-first round16 verification
- Time mode: measured
- Measured minutes: 48.483
- Started: 2026-05-15T15:52:42Z
- Ended: 2026-05-15T16:41:11Z
- Artifacts: artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round13_query_single_105_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round13_query_single_106_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round13_query_single_107_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round13_query_single_aggregate_105_107_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round14_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round14.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round14_query_single_107_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round14_query_single_108_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round14_query_single_aggregate_107_108_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round15_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round15.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round15_query_single_107_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round15_query_single_108_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round15_query_single_109_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round15_query_single_110_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round15_query_single_aggregate_107_109_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round15_query_single_aggregate_107_110_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round16_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round16.json, README.md, docs/external_source_transfer.md, work/foldseek_readiness_notes.md, work/handoff.md, work/scope.md, tests/test_generalization.py
- Evidence: startup 409 unit tests passed, validate passed with 679 curated labels, round13 indices 105-106 passed before index 107 blocker max TM 0.8826, round14 index 107 passed max TM 0.6862 before index 108 blocker max TM 0.7649, round15 indices 107-109 passed max TM 0.6996 before index 110 blocker max TM 0.7521, round16 has 66 high-TM constraints and 0 sequence-cluster splits, final 412 unit tests passed, final validate passed, compileall passed, git diff check passed, 19 new JSON artifacts parsed
- Notes: Normal locked direct run with no delegation. No M-CSA-only count growth and no external import.

### 2026-05-15T17:34:47.871028+00:00 - post-mcsa-spof-hardening

- Task: Foldseek cluster-first round19 verification
- Time mode: measured
- Measured minutes: 40.983
- Started: 2026-05-15T11:53:48-05:00
- Ended: 2026-05-15T12:34:47-05:00
- Artifacts: tests/test_generalization.py, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round16_query_single_110_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round16_query_single_aggregate_110_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round17_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round17.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round17_query_single_110_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round17_query_single_111_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round17_query_single_112_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round17_query_single_aggregate_110_112_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round18_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round18.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round18_query_single_112_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round18_query_single_aggregate_112_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round19_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round19.json, README.md, docs/external_source_transfer.md, work/foldseek_readiness_notes.md, work/handoff.md, work/scope.md
- Evidence: startup 412 unit tests passed and validate passed with 679 curated labels, round16 index 110 failed at max TM 0.7708, round17 cleared index 110 at max TM 0.6823 and index 111 at max TM 0.564, round17 index 112 failed at max TM 0.7063, round18 index 112 failed at max TM 0.9087, round19 has 72 high-TM constraints 38 sequence-identity constraints 0 projected violations and 0 sequence-cluster splits, 0 countable labels and 0 import-ready rows, final 415 unit tests passed and validate passed
- Notes: Normal locked direct run with no delegation. No M-CSA-only count growth and no external import. Full TM-score holdout claim remains forbidden.

### 2026-05-15T18:36:22.139127+00:00 - post-mcsa-spof-hardening

- Task: Foldseek cluster-first round22 verification
- Time mode: measured
- Measured minutes: 41.433
- Started: 2026-05-15T17:54:36Z
- Ended: 2026-05-15T18:36:02Z
- Artifacts: tests/test_generalization.py, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round19_query_single_112_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round19_query_single_113_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round19_query_single_114_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round19_query_single_aggregate_112_114_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round20_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round20.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round20_query_single_114_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round20_query_single_115_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round20_query_single_aggregate_114_115_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round21_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round21.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round21_query_single_115_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round21_query_single_aggregate_115_of_672.json, artifacts/v3_foldseek_tm_score_cluster_first_split_round22_1000.json, artifacts/v3_foldseek_coordinate_readiness_1000_cluster_first_split_round22.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round22_query_single_115_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round22_query_single_116_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round22_query_single_117_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round22_query_single_118_of_672.json, artifacts/v3_foldseek_tm_score_signal_1000_cluster_first_split_round22_query_single_aggregate_115_118_of_672.json, README.md, docs/external_source_transfer.md, work/foldseek_readiness_notes.md, work/handoff.md, work/scope.md
- Evidence: startup 415 unit tests passed, startup validate passed with 679 curated labels, round19 indices 112-113 passed before index 114 blocker max TM 0.7338, round20 index 114 passed before index 115 blocker max TM 0.9749, round21 index 115 rerun exposed m_csa:116/m_csa:67 at max TM 0.9032, round22 has 82 high-TM constraints and 0 sequence-cluster splits, round22 indices 115-118 passed in aggregate at max TM 0.6939, JSON artifacts parsed, final 418 unit tests passed, final validate passed
- Notes: Normal locked direct run with no delegation. No M-CSA-only count growth and no external import. Full TM-score holdout claim remains forbidden.

## Expectation Updates

- 2026-05-09T13:40:20.355854+00:00: v0 completed in one active session, so the previous one-year v0-v2 timeline is too conservative and must be recalibrated from logged progress
- 2026-05-09T13:40:25.768544+00:00: Use observed artifact-per-hour rate to revise v1 and v2 estimates after each material chunk.
- 2026-05-09T13:54:30.954964+00:00: V1 completed much faster than the earlier days-to-weeks estimate because paginated M-CSA and UniProt TSV APIs were straightforward.
- 2026-05-09T13:54:31.022704+00:00: The completed V2 is a scaffold-level research artifact, not the final high-impact enzyme atlas; time estimates must distinguish scaffold completion from scientific validation.
- 2026-05-09T14:01:49.012481+00:00: Geometry extraction was implementable quickly for PDB-linked M-CSA entries; the harder next step is label quality and retrieval evaluation.
- 2026-05-09T14:03:45.516905+00:00: Next quality bottleneck is curated mechanism labels and evaluation, not baseline implementation.
- 2026-05-09T14:10:40.717863+00:00: The next bottleneck is improving ranking and abstention, not adding labels machinery.
- 2026-05-09T14:13:21.398170+00:00: Progress will now be measured per hourly block rather than per ad hoc milestone.
- 2026-05-09T14:18:10.779278+00:00: Continuity is now treated as a required output of each 55-minute work block.
- 2026-05-09T14:25:33.013901+00:00: The time overestimate came from confusing scaffold implementation with scientifically robust validation; current progress is fast but still small-label and artifact-scale.
- 2026-05-09T15:20:27.676203+00:00: Ligand/cofactor context integration from mmCIF was quick; next quality bottleneck shifts to substrate-pocket descriptors and larger curated labels.
- 2026-05-09T15:22:39.241656+00:00: README now states that scaffold work moved faster than first estimated; impact depends on scaling labels, harder benchmarks, expert review, and validation.
- 2026-05-09T15:30:17.008476+00:00: Substrate-pocket descriptors integrated quickly; next bottleneck is targeted failure analysis and label expansion rather than more feature plumbing.
- 2026-05-09T15:42:05.002091+00:00: Future runs should consume the full 55-minute wall-clock block by rolling into the next highest-value bounded task when assigned work finishes early.
- 2026-05-09T16:02:34.920556+00:00: Current out-of-scope errors are threshold-margin cases; next gain likely comes from abstention policy refinement and harder negatives.
- 2026-05-09T16:03:37.698226+00:00: Automation model selection is now treated as an operating invariant, not an implicit app default.
- 2026-05-09T16:14:49.435851+00:00: Automation runs now distinguish productive work time from wrap-up time; normal runs should spend at least 50 measured minutes advancing the project.
- 2026-05-09T17:07:37.625326+00:00: Next priority is hard-negative scorer separation and structure mapping repair, not more scaffold work
- 2026-05-09T18:08:06.495922+00:00: remaining bottleneck is separating two ligand-supported metal-like controls without losing retained positives
- 2026-05-09T19:35:11+00:00: The 100-entry slice is clean, but full 125-entry labeling exposes hard redox and metal-like controls; robustness now depends on hard-negative separation and seed-family splits.
- 2026-05-09T19:52:34.146667+00:00: The main 125-entry bottleneck is no longer hidden heme-absent overlap; remaining controls concentrate in metal-like and Ser-His-like groups.
- 2026-05-09T20:12:10.878697+00:00: End-of-run quality now includes documentation freshness, not only code artifacts and git cleanliness.
- 2026-05-09T21:11:49.565784+00:00: Hard-negative separation is clean through the 150-entry slice; next quality bottleneck is evidence-limited in-scope positives with missing local cofactor context.
- 2026-05-09T22:17:13.285127+00:00: The main 150-entry bottleneck is retained positives without selected-structure cofactor evidence, not hard-negative separation
- 2026-05-09T23:20:32.069816+00:00: The 175-entry bottleneck is now near-miss metal-hydrolase controls and fragile evidence-limited retained positives, not hard-negative separation.
- 2026-05-10T00:22:01.303388+00:00: The 225-entry bottleneck is now the selected-structure cofactor gap for m_csa:132 or the next label expansion, not hard-negative separation.
- 2026-05-10T01:18:40.670377+00:00: Next bottleneck is expanding beyond 275 labels or resolving m_csa:132 selected-structure cofactor absence.
- 2026-05-10T02:23:20.695520+00:00: The benchmark can expand in 25-entry curation tranches while preserving guardrails; the next bottleneck is 400-entry label quality and evidence-limited cofactor gaps.
- 2026-05-10T03:26:17.876722+00:00: The benchmark can continue expanding in curated 25-entry tranches, but the next bottleneck is 475-entry label quality and evidence-limited cofactor gaps.
- 2026-05-10T04:23:35.521223+00:00: The benchmark can keep expanding in 25-entry curation tranches; next bottleneck is 500-entry label quality and evidence-limited cofactor gaps.
- 2026-05-10T05:25:09.634817+00:00: Next bottleneck is importing decisions from the 500 queue through the label factory rather than expanding labels directly.
- 2026-05-10T06:26:21.995107+00:00: The active bottleneck is cobalamin local cofactor evidence for m_csa:494 and preserving countable/review-state separation.
- 2026-05-10T07:28:17.575433+00:00: The active bottleneck moved from the 500 cobalamin deferral to preserving review-state labels while opening a 575-entry tranche.
- 2026-05-10T08:36:59.402518+00:00: The active bottleneck is reviewing the accepted 625 preview before promoting it to canonical labels.
- 2026-05-10T13:59:54.901465+00:00: The active bottleneck is reviewing the accepted 675 preview before promoting it to canonical labels.
- 2026-05-10T14:37:36.208242+00:00: The active bottleneck is auditing the 24 new 675-preview review-debt rows before promotion.
- 2026-05-10T15:39:13.368774+00:00: The active bottleneck is deciding whether to promote m_csa:666 alone or resolve the 61 pending 675-preview review-state rows first.
- 2026-05-10T16:41:45.028412+00:00: Stop further tranche growth at 624 countable labels until 81 review-state rows are triaged or stronger evidence is added.
- 2026-05-10T17:43:34.382296+00:00: Count growth remains stopped at 624 countable labels until accepted-700 review debt has local evidence or explicit expert resolution.
- 2026-05-10T18:46:18.139775+00:00: Next bottleneck is auditing m_csa:577 m_csa:592 and m_csa:641 remap-local leads against counterevidence before any further gated scaling.
- 2026-05-10T19:48:49.955298+00:00: Next bottleneck is deciding whether kinase/phosphoryl-transfer mismatch rows need an ontology-family rule or expert reaction/substrate export before more count growth.
- 2026-05-10T20:50:01.204415+00:00: Next bottleneck shifts from detecting reaction/substrate mismatch lanes to reducing review-only debt without expert-authority count growth.
- 2026-05-10T22:51:19.534178+00:00: Next bottleneck is reducing expert-label decision review-only debt with evidence repair, not opening 725+ count growth.
- 2026-05-10T23:56:45.965586+00:00: Next run should reduce expert-label repair debt or harden local-evidence checks before opening any 725+ tranche.
- 2026-05-11T03:12:54.274263+00:00: Next bottleneck is resolving one local-evidence repair lane from the 21-row plan before count growth.
- 2026-05-12T15:04:26.275853+00:00: After prioritized scientific expansion is implemented and guardrail-clean, agents should resume factory-gated label expansion while preserving label quality and import-safety controls.
- 2026-05-12T16:42:24.970333+00:00: Keep ATP families as boundary evidence; stop scaling if next gate exposes quality drift.
- 2026-05-12T17:48:03.708741+00:00: Next run should repair or explicitly defer the accepted-725 review-debt surface before blind 750 scaling.
- 2026-05-12T18:52:33.655337+00:00: Next run should repair or explicitly defer the 18 new 750-preview review-debt rows before promoting seven clean candidates.
- 2026-05-12T20:14:45.382801+00:00: 750 review debt can be explicitly deferred without weakening countable-label gates; resume bounded scaling toward 1,000 labels.
- 2026-05-12T21:46:07.698000+00:00: Countable registry is 642 labels; the label factory remains below the 1000-label milestone and should continue bounded batches with quality repair on any gate failure.
- 2026-05-12T22:58:26.440004+00:00: Countable registry is 652 labels; next bounded work is an 875 preview while post-850 gate stays clean.
- 2026-05-13T00:50:52.831198+00:00: Countable registry is 673 labels; next bounded work is a 975 preview while post-950 gate stays clean.
- 2026-05-13T02:01:21.378176+00:00: Low-score local heme boundary rows now defer instead of becoming countable out-of-scope negatives.
- 2026-05-13T03:55:19.973294+00:00: The 1,025 preview is guardrail-clean but non-promotable; 10k progress now depends on external-source transfer rather than another M-CSA-only tranche.
- 2026-05-13T04:55:52.608228+00:00: Next bounded work should use the active-site evidence queue for external candidates while keeping all external rows non-countable.
- 2026-05-13T05:57:24.579339+00:00: External transfer remains review-only; repair active-site feature gaps and heuristic metal-hydrolase collapse before any label import.
- 2026-05-13T06:58:30.872167+00:00: External transfer remains non-countable; next bounded work should source active-site evidence for 10 gaps, disambiguate 3 broad-EC rows, and prototype representation controls for 12 mapped controls.
- 2026-05-13T12:55:17.737175+00:00: The next useful milestone is pilot import readiness for named external candidates, not a higher external-transfer gate count.
- 2026-05-13T13:02:54.457092+00:00: The next run should implement holdout/generalization evaluation first; external pilot work resumes after that signal or in parallel only when directly unblocking import readiness.
- 2026-05-13T17:47:33.256358+00:00: External pilot now has per-candidate review dossiers; next work should fill decisions and missing evidence, not add generic gates.
- 2026-05-13T18:44:44.009443+00:00: External pilot import remains blocked; next work should fill real active-site and sequence evidence decisions rather than expanding gate count.
- 2026-05-13T19:39:20.606270+00:00: External pilot import remains blocked; high-fan-in gate maintenance is reduced, but active-site source decisions and complete near-duplicate search remain the next blockers.
- 2026-05-13T20:51:07.000000+00:00: Geometry retrieval predictive evidence is now explicitly text-free; PLP positive signal uses local ligand-anchor context
- 2026-05-13T22:04:23.805937+00:00: M-CSA-only growth remains stopped; next external-pilot work should fill real sequence-search and active-site decisions rather than add generic gates.
- 2026-05-13T22:34:16.818554+00:00: External transfer remains non-countable; complete UniRef/all-vs-all sequence search and active-site evidence decisions still block import.
- 2026-05-13T23:52:26.926762+00:00: external pilot can proceed to review decisions only after active-site sources and complete sequence search; no external import is ready
- 2026-05-14T00:43:19.772463+00:00: Artifact graph consistency still matters at count-decision boundaries; next work should fill external pilot evidence decisions rather than add generic gates.
- 2026-05-14T03:08:19.594666+00:00: External pilot remains review-only; next highest-value work is coordinate staging for TM-score only if it directly unblocks pilot import readiness, plus active-site source decisions and complete near-duplicate search.
- 2026-05-14T04:23:49.348241+00:00: Next useful external-pilot work is active-site source decisions and representation repair for selected rows; M-CSA-only count growth remains stopped.
- 2026-05-14T05:08:05.672183+00:00: Full TM-score split remains blocked until remaining selected coordinates are staged and a Foldseek-backed split builder is added; partial staged25 TM signal is review-only evidence.
- 2026-05-14T05:12:09.497043+00:00: Foldseek artifacts now have regression coverage; full TM-score split remains blocked until the remaining selected coordinates and split builder are implemented.
- 2026-05-14T09:28:41.519786+00:00: Expanded40 Foldseek raw-name mapping is no longer a blocker, but the partial staged-coordinate TM signal still fails the <0.7 target and full TM-score split remains blocked on full coordinate coverage plus a split builder.
- 2026-05-14T10:16:36.145071+00:00: Requested 650M representation remains blocked by local cache/disk/CPU limits; largest feasible cached ESM-2 150M now gives a real review-only control signal while Foldseek remains partial and fails the <0.7 target.
- 2026-05-14T11:07:34.295381+00:00: Next work should run a full Foldseek/TM-score split only after resolving missing selected structures and should advance pilot rows through broader duplicate screening, representation review, and review decisions without countable import.
- 2026-05-14T12:34:37.036864+00:00: Next agent should retry the all-materializable Foldseek TM-score signal as delegated backend work or emit a bounded larger-than-40 completed signal without false full-holdout claims.
- 2026-05-14T12:50:26.982940+00:00: Sequence-distance holdout is real backend evidence; next generalization blocker remains full Foldseek/TM-score split and external import blockers.
- 2026-05-14T14:10:21.275491+00:00: Expanded60 removes the expanded40 partial-signal ceiling, but full TM-score split remains blocked by two missing selected structures, the capped-out staged coordinates, and the failed <0.7 computed-subset target.
- 2026-05-14T15:07:52.876846+00:00: External pilot now has measurable success criteria and remains needs_more_work; Foldseek selected-structure blocker is narrowed to explicit coordinate exclusions plus the unrun full TM-score split.
- 2026-05-14T16:15:30.855586+00:00: Expanded80 removes the expanded60 partial-signal ceiling, but full TM-score split remains blocked by two coordinate exclusions, the capped-out staged coordinates, and the failed <0.7 computed-subset target.
- 2026-05-14T17:29:09.455993+00:00: Expanded100 removes the expanded80 partial-signal ceiling, but full TM-score split remains blocked by two coordinate exclusions, the capped-out staged coordinates, and the failed <0.7 computed-subset target.
- 2026-05-14T19:04:21.441130+00:00: Next Foldseek work should apply/regenerate the repaired split and rerun downstream metrics before any full TM-score claim
- 2026-05-14T19:08:48.002960+00:00: Next Foldseek work should rebuild downstream evaluation from the candidate split and run an uncapped all-materializable Foldseek signal when feasible
- 2026-05-14T20:34:07.608397+00:00: Repaired expanded100 removes the projection-only computed-subset blocker, but full TM-score split remains blocked by the cap, two coordinate exclusions, and the uncomputed all-materializable signal
- 2026-05-14T21:29:26.788448+00:00: Uncapped all-materializable Foldseek exact TM-score search exceeds the normal automation window; next work needs a longer run budget or chunk/resume support, not another routine capped increment
- 2026-05-14T22:36:14.676450+00:00: Resumable Foldseek query chunks remove the all-at-once-only runtime SPOF but show the repaired candidate split still fails the <0.7 TM-score target beyond the expanded100 cap
- 2026-05-14T23:22:21.551765+00:00: Foldseek query chunk aggregation is now durable; next work should adjudicate target-violating chunk blockers or change the chunk-2 runtime/slice strategy before routine chunk continuation
- 2026-05-15T00:19:07.369532+00:00: Full TM-score holdout remains blocked by target-violating completed chunks, held-out in-scope split blockers, incomplete query coverage, and two coordinate exclusions
- 2026-05-15T01:39:52.871051+00:00: Round-2 split redesign clears Foldseek chunk 0 only; next work should continue chunk 1 under the round-2 candidate and stop on any new target violation
- 2026-05-15T02:47:11.394945+00:00: Round-3 split redesign clears Foldseek chunks 0-1 only; next work should continue chunk 2 and stop on any new target violation
- 2026-05-15T03:40:39.370706+00:00: Round-3 Foldseek chunks 0-2 clear the completed-chunk target, but chunk 3 is now the runtime blocker; retry or split chunk 3 before continuing coverage
- 2026-05-15T04:56:18.692987+00:00: Cluster-first Foldseek split design replaces blind 56-chunk continuation; next work should verify bounded subchunks from the round-3 cluster-first readiness and fold in any new high-TM blockers before continuing.
- 2026-05-15T05:48:11.759711+00:00: Cluster-first round4 clears the latest failing verification unit; continue bounded round4 subchunks and fold in any new high-TM blockers before claiming full TM-score holdout.
- 2026-05-15T06:49:36.549572+00:00: Cluster-first round6 clears subchunk 009; next work should continue bounded round6 verification from subchunk 010 and fold in any new high-TM blocker before broad coverage claims
- 2026-05-15T08:46:02.937530+00:00: Round-8 cluster-first split folds in the new m_csa:68/m_csa:750 blocker; next work should continue single-query verification from staged index 68 under round-8 readiness.
- 2026-05-15T13:32:19.332566+00:00: Round-9 cluster-first split folds in the m_csa:80 high-TM blocker; next work should continue single-query verification from staged index 84 under round-9 readiness.
- 2026-05-15T14:31:01.833373+00:00: Round-9 cluster-first verification now clears staged indices 79-95; next work should continue from staged index 96 and stop on any TM>=0.7 blocker
- 2026-05-15T16:41:11.445104+00:00: Full TM-score holdout remains blocked by incomplete round-16 verification coverage and two coordinate exclusions.
- 2026-05-15T17:34:47.871028+00:00: Round-19 cluster-first split is the active Foldseek handoff; next work should verify staged index 112 under round-19 readiness.

## Scope Adjustments

- 2026-05-09T13:40:25.768544+00:00: Project management is now repository state, not chat state; future scope changes must be recorded in the ledger.
- 2026-05-09T13:54:30.954964+00:00: V1 criteria are satisfied by a bounded 50-entry graph slice; broader scale is now an expansion problem, not a schema blocker.
- 2026-05-09T13:54:31.022704+00:00: V2 scaffold criteria are satisfied; next work should increase scientific quality rather than add more dashboard-like surface area.
- 2026-05-09T14:01:49.012481+00:00: Post-V2 quality work now targets geometry-aware retrieval rather than more text-only scaffolding.
- 2026-05-09T14:03:45.516905+00:00: Geometry now affects retrieval scores through residue signature matching and catalytic-cluster compactness.
- 2026-05-09T14:10:40.717863+00:00: Curated labels are now explicit for the 20-entry geometry slice; retrieval quality is measurable and currently weak at top1.
- 2026-05-09T14:13:21.398170+00:00: Each automation run is now an hourly carry-forward block: 55 minutes work, 5 minutes break/overhead, commit and push every run.
- 2026-05-09T14:18:10.779278+00:00: Every automation run must now leave explicit next-agent start instructions before committing and pushing.
- 2026-05-09T14:25:33.013901+00:00: V2 is stronger: retrieval has cofactor-aware scoring, calibrated abstention, and local performance measurement; full scalability and ligand parsing remain future work.
- 2026-05-09T15:20:27.676203+00:00: Post-V2 quality scope now includes ligand-supported cofactor evidence in retrieval; substrate-pocket descriptors become the next bounded upgrade.
- 2026-05-09T15:22:39.241656+00:00: Next automation should continue from substrate-pocket descriptors and harder negative controls, not from v0-v2 scaffold planning.
- 2026-05-09T15:30:17.008476+00:00: Post-V2 retrieval now includes pocket-aware scoring; next bounded iteration should tune abstention and false-positive control using failure categories.
- 2026-05-09T15:42:05.002091+00:00: Automation handoff now requires origin/main sync verification before the next agent starts.
- 2026-05-09T16:02:34.920556+00:00: Failure analysis is now explicit and reproducible; next bounded step is threshold-policy tuning with guardrails.
- 2026-05-09T16:03:37.698226+00:00: Catalytic Earth automation documentation now forbids downgrading below gpt-5.5 with xhigh reasoning.
- 2026-05-09T16:14:49.435851+00:00: If assigned work finishes or blocks early, agents must switch to the highest-value bounded unblocked task until the 50-minute work boundary.
- 2026-05-09T17:07:37.625326+00:00: 40-entry slice now has 36 labels, 26 evaluable structures, and explicit hard-negative plus structure-mapping blockers
- 2026-05-09T18:08:06.495922+00:00: expanded geometry slice to 60 fully labeled entries with 63 labels
- 2026-05-09T19:35:11+00:00: Expanded the audited geometry slice to 125 fully labeled entries; next scope is reducing 125-entry hard negatives without regressing the clean 20-100 slices.
- 2026-05-09T19:52:34.146667+00:00: 125-entry hard-negative controls are now grouped and anchored to correctly ranked positives; next scorer work should target the largest grouped control clusters.
- 2026-05-09T20:12:10.878697+00:00: Every automation wrap-up must update stale README/docs/work files or explicitly record that documentation was checked and unchanged.
- 2026-05-09T21:11:49.565784+00:00: Post-V2 geometry scope now tracks 150 labeled entries with cross-slice summary artifacts and in-scope failure analysis.
- 2026-05-09T22:17:13.285127+00:00: 150-entry geometry scope now separates local active-site positives from enzyme-level labels and tracks cofactor coverage explicitly
- 2026-05-09T23:20:32.069816+00:00: Post-V2 geometry scope now tracks 175 fully labeled entries with cofactor policy and seed-family audits.
- 2026-05-10T00:22:01.303388+00:00: Post-V2 geometry scope now tracks a fully labeled 225-entry source slice with 12 cross-slice summaries and clean hard-negative guardrails.
- 2026-05-10T01:18:40.670377+00:00: Post-V2 geometry scope now tracks a fully labeled 275-entry source slice.
- 2026-05-10T02:23:20.695520+00:00: Post-V2 geometry scope now tracks a fully labeled 375-entry source slice and a generated 400-entry candidate queue.
- 2026-05-10T03:26:17.876722+00:00: Post-V2 geometry scope now tracks a fully labeled 450-entry source slice and a generated 475-entry candidate queue.
- 2026-05-10T04:23:35.521223+00:00: Post-V2 geometry scope now tracks a fully labeled 475-entry source slice and a generated 500-entry candidate queue.
- 2026-05-10T05:25:09.634817+00:00: Label scaling is now factory-gated; new labels must pass promotion, demotion, adversarial-negative, active-learning, expert-review, family-propagation, validation, and test checks before counting.
- 2026-05-10T06:26:21.995107+00:00: 500-slice label scaling now has countable batch import and acceptance checks; next scope is resolving m_csa:494, not opening a 525-label tranche.
- 2026-05-10T07:28:17.575433+00:00: Label-factory scaling can continue from the 550 review-state registry; next tranche should use 546 as the countable baseline.
- 2026-05-10T08:36:59.402518+00:00: Post-V2 geometry scope now tracks accepted 600-entry countable labels and a generated 625-entry preview batch.
- 2026-05-10T13:59:54.901465+00:00: Post-V2 geometry scope now tracks accepted 650-entry countable labels and a generated 675 preview batch.
- 2026-05-10T14:37:36.208242+00:00: Post-V2 label-factory scope now separates preview mechanical acceptance from promotion readiness with carried/new review-debt metadata.
- 2026-05-10T15:39:13.368774+00:00: Post-V2 label-factory scope now blocks accepted review-gap labels, attaches scaling-quality audits to preview summaries, and records the missing sequence-cluster artifact before promotion.
- 2026-05-10T16:41:45.028412+00:00: 700-entry slice is guardrail-clean for clean labels; next bounded work is review-debt repair, not blind expansion.
- 2026-05-10T17:43:34.382296+00:00: Review-debt repair now separates alternate-structure cofactor leads from local active-site evidence before any further gated scaling.
- 2026-05-10T18:46:18.139775+00:00: Alternate-PDB residue remapping now produces review-only local evidence leads but does not reopen count growth.
- 2026-05-10T19:48:49.955298+00:00: 700 scaling remains stopped at 624 countable labels until reaction/substrate mismatch lanes are resolved by ontology rule or expert review.
- 2026-05-10T20:50:01.204415+00:00: 700 scaling remains stopped at 624 countable labels; reaction/substrate mismatch lanes now require complete expert-review export before more count growth.
- 2026-05-10T22:51:19.534178+00:00: 700 scaling remains at 624 countable labels; active expert-label decision lanes now require complete non-countable review export and repair-candidate coverage before any further gated growth.
- 2026-05-10T23:56:45.965586+00:00: 700 scaling remains at 624 countable labels; this run added repair guardrails and discovery-facing controls instead of count growth because review debt remains the limiting gate.
- 2026-05-11T03:12:54.274263+00:00: 700 factory gate now requires local-evidence gap audit and review-only export before count growth.
- 2026-05-12T15:04:26.275853+00:00: Expert-reviewed ATP/phosphoryl-transfer mismatch lanes now drive aggressive fingerprint-family ontology expansion for ePK ASKHA ATP-grasp GHKL dNK NDK PfkA PfkB and GHMP before returning to 10k gated label scaling.
- 2026-05-12T16:42:24.970333+00:00: Nine-family ATP/phosphoryl-transfer expansion is complete; next bounded work can resume factory-gated scaling toward 725.
- 2026-05-12T17:48:03.708741+00:00: Accepted 725 as the latest gated countable slice: 630 countable labels and 100 review-state rows kept non-countable.
- 2026-05-12T18:52:33.655337+00:00: Accepted-725 review debt is explicitly deferred; 750 preview is open but not canonical.
- 2026-05-12T20:14:45.382801+00:00: Accepted 750 as latest gated countable slice; next bounded work is a 775 preview only while the 750 post-batch gate stays clean.
- 2026-05-12T21:46:07.698000+00:00: Accepted 775 as latest gated countable slice; next bounded work is an 800 preview only while the 775 post-batch gate stays clean.
- 2026-05-12T22:58:26.440004+00:00: Accepted 850 as latest gated countable slice; geometry row reuse added for tranche scaling.
- 2026-05-13T00:50:52.831198+00:00: Accepted 950 as latest gated countable slice; review-debt deferral remains mandatory before 1,000-label milestone.
- 2026-05-13T02:01:21.378176+00:00: Accepted 1000 as latest gated countable slice; next bounded tranche is 1025 only while post-1000 gates stay clean.
- 2026-05-13T03:55:19.973294+00:00: M-CSA-only scaling is source-limited at 1,003 observed records; next work should build external-source transfer with all imported candidates non-countable until full factory gates pass.
- 2026-05-13T04:55:52.608228+00:00: M-CSA-only scaling remains stopped at 1,003 observed source records; external-source transfer is review-only evidence collection until active-site evidence OOD sequence holdouts heuristic controls decisions and factory gates pass.
- 2026-05-13T05:57:24.579339+00:00: M-CSA-only count growth remains stopped at 1,003 observed records; post-M-CSA scaling now depends on active-site-supported external controls plus representation or ontology repairs.
- 2026-05-13T06:58:30.872167+00:00: M-CSA-only count growth remains stopped at 1,003 observed records; post-M-CSA scaling still depends on review-only external-source repair and representation controls before label import.
- 2026-05-13T08:00:59.297672+00:00: Post-M-CSA scaling remains review-only; next import readiness depends on active-site sourcing, near-duplicate sequence search, and real representation controls before any external label decision.
- 2026-05-13T09:00:39.138608+00:00: External transfer remains non-countable; next import readiness depends on active-site sourcing, complete near-duplicate sequence search, and real representation controls before any external decision.
- 2026-05-13T10:03:45+00:00: External transfer remains non-countable; next import readiness depends on sourcing explicit active-site evidence, completing near-duplicate sequence search, and replacing feature-proxy representation controls before any external decision.
- 2026-05-13T11:04:16.318492+00:00: External transfer remains non-countable; next import readiness depends on sourcing explicit active-site evidence, completing near-duplicate sequence search, and running real representation controls before any external decision.
- 2026-05-13T12:05:19.086868+00:00: External transfer remains non-countable; next import readiness depends on primary literature/PDB active-site source review, complete near-duplicate sequence search, and replacing deterministic k-mer controls with real learned or structure-language representation controls before any external decision.
- 2026-05-13T12:55:17.737175+00:00: Post-M-CSA work now prioritizes a 5-10 candidate external-source pilot over additional abstract transfer gates or M-CSA-only tranche growth.
- 2026-05-13T13:02:54.457092+00:00: Agent work is now instruction-only redirected toward sequence/fold-distance holdout evaluation before external import or further abstract gates.
- 2026-05-13T14:08:28.620965+00:00: External transfer remains non-countable; next pilot readiness work should use the holdout metrics and learned-vs-heuristic disagreements to rank candidates before active-site source review, complete sequence search, selected-PDB override repairs, and full factory gates.
- 2026-05-13T16:04:03.062604+00:00: External pilot now has leakage-provenance ranking and no-decision review packets; next work should fill active-site and sequence evidence for selected candidates, not increase M-CSA-only count.
- 2026-05-13T16:37:11.331979+00:00: External pilot packets now have consolidated review-only source targets; next work should fill evidence decisions, not increase M-CSA count.
- 2026-05-13T17:47:33.256358+00:00: External transfer gate now fails fast on mixed-slice artifact paths across supplied gate artifacts.
- 2026-05-13T18:44:44.009443+00:00: External pilot review-decision path now fails if selected rows are ineligible, pilot decisions are completed prematurely, required review prerequisites are missing, or pilot dossier evidence blockers are stale.
- 2026-05-13T19:39:20.606270+00:00: External transfer gate input typing and CLI loading are now contract-based; next pilot work should fill real active-site and sequence evidence, not add generic gate count.
- 2026-05-13T20:51:07.000000+00:00: No M-CSA-only growth or external import; SPOF text-leakage hardening only
- 2026-05-13T22:04:23.805937+00:00: External transfer remains non-countable; current-reference sequence screen blocker is cleared, but complete UniRef/all-vs-all near-duplicate search and active-site evidence still block import.
- 2026-05-13T22:34:16.818554+00:00: Artifact-lineage SPOF hardening now includes the external sequence-holdout audit in row-level candidate lineage checks.
- 2026-05-13T23:52:26.926762+00:00: selected-pilot representation coverage is now a direct review-only gate input rather than stale mapped-control evidence
- 2026-05-14T00:43:19.772463+00:00: Label batch acceptance and scaling-quality audits now fail fast on mixed slice lineage before count/import decisions.
- 2026-05-14T01:50:53.503582+00:00: High-fan-in external pilot builders now fail fast on mixed-slice lineage before artifact write; selected-PDB ready overrides must match graph slice provenance.
- 2026-05-14T03:08:19.594666+00:00: Real sequence-distance holdout replaces proxy-only generalization signal; Foldseek/TM-score split now depends on coordinate materialization rather than tool availability alone.
- 2026-05-14T04:23:49.348241+00:00: External pilot sequence-search work now uses real MMseqs2 current-reference backend evidence before review decisions; import remains blocked by active-site, representation, broader duplicate-screening, review, and factory gates.
- 2026-05-14T11:07:34.295381+00:00: Unstaged selected-coordinate sidecar blocker is removed, but full TM-score split remains blocked by two missing selected structures and the unrun Foldseek split builder; selected-pilot active-site source status is classified but import remains blocked.
- 2026-05-14T12:34:37.036864+00:00: No project scope change; full TM-score split remains blocked by two missing selected structures and the unrun all-materializable Foldseek signal.
- 2026-05-14T14:10:21.275491+00:00: Foldseek TM-score evidence is stronger but still review-only and non-countable; do not treat expanded60 as a full holdout split.
- 2026-05-14T15:07:52.876846+00:00: Do not count external pilot evidence as success until terminal decisions and import criteria pass; report m_csa:372 and m_csa:501 as coordinate exclusions before any full TM-score holdout claim.
- 2026-05-14T16:15:30.855586+00:00: Foldseek TM-score evidence is stronger but still review-only and non-countable; do not treat expanded80 as a full holdout split.
- 2026-05-14T17:29:09.455993+00:00: Foldseek TM-score evidence is stronger but still review-only and non-countable; do not treat expanded100 as a full holdout split.
- 2026-05-14T19:04:21.441130+00:00: Foldseek target failure now has a concrete unapplied repair candidate and computed-subset projection; full holdout still requires regenerated sequence metrics and uncapped Foldseek split
- 2026-05-14T19:08:48.002960+00:00: Foldseek split repair now has an unapplied candidate sequence holdout copy; canonical holdout and downstream artifacts still need regeneration before any claim
- 2026-05-14T20:34:07.608397+00:00: Foldseek split repair now has an actual repaired expanded100 signal under the candidate holdout; canonical holdout remains unchanged and no full holdout claim is permitted.
- 2026-05-14T22:36:14.676450+00:00: Full TM-score holdout remains blocked by incomplete chunk aggregation new target-violating pairs and two coordinate exclusions
- 2026-05-14T23:22:21.551765+00:00: Full TM-score holdout remains blocked by target-violating completed chunks a timed-out chunk-2 range incomplete query coverage and two coordinate exclusions
- 2026-05-15T04:56:18.692987+00:00: Foldseek/TM-score work now uses observed high-TM structural clusters as partition constraints before verification chunks.
- 2026-05-15T15:32:34.144335+00:00: Cluster-first Foldseek verification now preserves real sequence-identity components before structural assignment; next work should rerun staged index 105 under round-13 readiness.
- 2026-05-15T16:41:11.445104+00:00: Round-16 cluster-first split is the active Foldseek handoff; next work should verify staged index 110 under round-16 readiness.
- 2026-05-15T18:36:22.139127+00:00: Round-22 cluster-first split is the active Foldseek handoff; next work should continue from staged index 119 under round-22 readiness.
