# Foldseek / Pocket Representation Track Handoff

Run date: 2026-05-25
Branch: `research/representation-foldseek-pocket`

## Scope

This branch is limited to the Catalytic Earth structural nearest-neighbor baseline track for Foldseek and pocket-restricted variants. No labels, fingerprints, ontology files, production scoring, thresholds, or shared docs were edited.

Shared baseline cited:

- `origin/main`: `8e69bf002097d5cf55521a13764e096908d8e0af`
- Eval contract: `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`, SHA256 `c4190f6f3f695185cd49e0de85d41280666c2986aaf2e359c8c4a60d67b40c50`
- Fingerprint audit: `artifacts/v3_mechanism_fingerprint_v1_coherence_audit_702.json`
- Frozen split: `artifacts/v3_sequence_distance_holdout_eval_1025_current702_split_assignment_repaired_20260525.json`, SHA256 `dbed4d1a60c09e97403f6be26ae52a3de49284ba35b6d6c2fb4efebb55de7425`
- Sequence-NN baseline: `artifacts/v3_sequence_nn_metrics_current702_20260525.json`, SHA256 `22792684a943cd16987a73d048f801c3177a96c5967444d746a5aa768a0e6a26`

## New Artifacts

- `artifacts/representation_tracks/foldseek_pocket/current702_structure_pocket_coverage_20260525.json`
- `artifacts/representation_tracks/foldseek_pocket/current702_foldseek_runtime_status_20260525.json`

Coverage summary:

- Current702 rows: 702
- Full-structure selected-coordinate availability: 676 available, 26 unavailable
- Frozen heldout selected-coordinate availability: 134 available, 6 unavailable
- Known-active-site pocket eligibility: 676 eligible, 26 ineligible
- Pocket-NN is not computed yet; the artifact records the blockers and command plan for a pocket CIF sidecar.

## Foldseek Status

Foldseek is available only through the explicit prior environment path, not `PATH`:

- Binary: `/private/tmp/catalytic-foldseek-env/bin/foldseek`
- Version command: `/private/tmp/catalytic-foldseek-env/bin/foldseek version`
- Version output: `718d42176d2f67d36a60866fedfb881f8d5a7ebf`

The coverage artifact records an exact full-structure command plan using `artifacts/v3_foldseek_coordinates_1000` as both query and target sidecar. During the first run, both an exact all-vs-all command and a smaller heldout-vs-train symlink command were started, but neither emitted a final TSV before wrap. A later retry resumed the heldout-vs-train command from `/private/tmp/catalytic-earth-repr-foldseek-pocket-current702-entrynn`, but it again stayed in the TM-align alignment stage with zero-byte `aln` output and no final TSV. The sandbox denied manual cleanup with `operation not permitted`, so `current702_foldseek_runtime_status_20260525.json` now records the retry and the non-signalable active Foldseek processes. Prediction metrics remain not computed, and no partial intermediate DB output was accepted.

## Leakage Contract

Predictive inputs are restricted to selected-PDB/AFDB coordinates with row-level provenance. EC labels, names, mechanism prose, expert notes, and review text were not used as predictive features. Pocket eligibility uses existing resolved active-site residue counts only as a controlled known-active-site ablation, not as a source-free primary representation benchmark.

## Next Step

After stale `/private/tmp/catalytic-earth-repr-foldseek-pocket-current702*` Foldseek processes have exited or are killed outside this sandbox, rerun heldout-vs-train Foldseek from a fresh scratch directory under a watchdog that can interrupt the job. Then emit:

- `current702_foldseek_full_structure_predictions_20260525.jsonl`
- `current702_foldseek_full_structure_metrics_20260525.json`

Metrics must include primary macro-F1/accuracy, per-fingerprint support and underpowered flags, OOS abstention/false-positive diagnostics by tier, canary predictions, unavailable-structure abstention counts, and exact Foldseek command/version provenance.
