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
- `artifacts/representation_tracks/foldseek_pocket/current702_foldseek_fast3di_full_structure_predictions_20260525.jsonl`
- `artifacts/representation_tracks/foldseek_pocket/current702_foldseek_fast3di_full_structure_metrics_20260525.json`

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

The coverage artifact records an exact full-structure command plan using `artifacts/v3_foldseek_coordinates_1000` as both query and target sidecar. During earlier runs, exact TM and TM-align-fast attempts did not emit a final TSV and no partial intermediate DB output was accepted.

This run completed the immediate unblock by switching to a clearly labeled fast Foldseek structural NN / 3Di smoke baseline with entry-specific coordinate symlinks:

- Command mode: heldout-vs-train `foldseek easy-search`, `--alignment-type 0`, `--max-seqs 100`, `--threads 1`
- Scratch: `/private/tmp/catalytic-foldseek-fast3di-current702-20260525T181437Z`
- Final TSV: 22,716 rows, SHA256 `c3d0fbab2cb9e6da6502a3f54a15d5a99b42fb2bae53894e622a3498373d7027`
- Runtime: 97.114 seconds
- Heldout/train symlinks: 134 / 542

Fast Foldseek structural NN metrics:

- Primary supervised accuracy: 0.6222 over 45 primary heldout rows
- Primary supervised macro-F1: 0.7649
- Available-only primary accuracy: 0.7000 over 40 primary heldout rows with coordinates
- All-heldout exact-label accuracy: 0.8000
- OOS false-positive rate without threshold: 0.0870
- Unavailable heldout structure abstentions: 6

Primary scoreboard:

| Comparator | Primary accuracy | Primary macro-F1 | OOS FP rate | Status |
| --- | ---: | ---: | ---: | --- |
| Fast Foldseek structural NN / 3Di alignment | 0.6222 | 0.7649 | 0.0870 | Computed in this track |
| Sequence-NN current702 | 0.1556 | 0.2374 | 0.2717 | Computed repaired split comparator |
| ESM-2 150M mechanism-NN current702 | n/a | n/a | n/a | Not available in repository; only review-only external samples found |
| ProtT5 current702 | n/a | n/a | n/a | No current702 metrics artifact found |
| SaProt current702 | n/a | n/a | n/a | No current702 metrics artifact found |
| 3Di token NN current702 | n/a | n/a | n/a | No separate 3Di-token NN artifact found; this Foldseek run uses 3Di alignment scores |

Per-fingerprint primary breakdown:

| Fingerprint | Heldout rows | Available | Accuracy | Precision | Recall | F1 | Unavailable abstentions | Note |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `flavin_dehydrogenase_reductase` | 10 | 9 | 0.6000 | 0.8571 | 0.6000 | 0.7059 | 1 | - |
| `heme_peroxidase_oxidase` | 4 | 4 | 0.7500 | 1.0000 | 0.7500 | 0.8571 | 0 | Underpowered |
| `metal_dependent_hydrolase` | 17 | 14 | 0.4118 | 0.7778 | 0.4118 | 0.5385 | 3 | - |
| `plp_dependent_enzyme` | 6 | 6 | 1.0000 | 0.8571 | 1.0000 | 0.9231 | 0 | - |
| `ser_his_acid_hydrolase` | 8 | 7 | 0.7500 | 0.8571 | 0.7500 | 0.8000 | 1 | - |

OOS and abstention diagnostics:

- OOS heldout rows with available structures: 92; abstentions: 84; abstention rate: 0.9130.
- OOS false positives without a calibrated threshold: 8 / 92, rate 0.0870.
- OOS tier breakdown: far OOS 1 / 1 abstained and 0 false positives; near OOS 3 / 3 abstained and 0 false positives; unknown OOS 80 / 88 abstained and 8 false positives.
- There is no strict Foldseek-bits threshold separating OOS false positives from correctly classified primary rows: max OOS FP bits 245.0, min correct primary bits 25.0.
- Unavailable heldout structure abstentions: 6 total (`m_csa:372`, `m_csa:577`, `m_csa:599`, `m_csa:710`, `m_csa:892`, `m_csa:897`).

The metrics JSON includes per-fingerprint precision/recall/F1, underpowered-cell flags, OOS abstention/false-positive diagnostics by tier, secondary probes, canary predictions, unavailable-structure abstention counts, and direct comparison entries for sequence-NN, the fast 3Di structural smoke, and unavailable representation comparators.

## Leakage Contract

Predictive inputs are restricted to selected-PDB/AFDB coordinates with row-level provenance. EC labels, names, mechanism prose, expert notes, and review text were not used as predictive features. Pocket eligibility uses existing resolved active-site residue counts only as a controlled known-active-site ablation, not as a source-free primary representation benchmark.

## Verification

- JSON validation passed for the metrics/status artifacts.
- JSONL validation passed for 140 heldout prediction rows.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed with 702 curated labels, 8 mechanism fingerprints, and 15 ontology families.
- Local commits created on `research/representation-foldseek-pocket`.
- Fast artifact push was verified before this status-only follow-up: local `HEAD` equaled `origin/research/representation-foldseek-pocket` at `ae5f46fec8c239948365909e4e0a88377697e8ef`.
- Follow-up local Git push attempt on 2026-05-26T02:10:30Z is blocked in this environment: HTTPS reports `could not read Username for 'https://github.com'`, and SSH reports `Permission denied (publickey)`.
- GitHub connector publish fallback was started on 2026-05-26T02:15:07Z after the local credential blocker; final branch/ref verification is recorded in the automation wrap-up.
- Post-fast3Di runtime check on 2026-05-26T02:08:08Z: process inspection is still blocked by sandbox policy (`ps` reports `operation not permitted`), and stale scratch directories remain at `/private/tmp/catalytic-earth-repr-foldseek-pocket-current702`, `/private/tmp/catalytic-earth-repr-foldseek-pocket-current702-entrynn`, and `/private/tmp/catalytic-foldseek-fast3di-current702-20260525T181437Z`. No exact-TM refinement was launched after this check.

## Next Step

Optional next work:

- Run exact-TM refinement only as a separate artifact from a fresh scratch path; keep it distinct from the accepted fast3Di baseline and continue to reject partial DBs.
- Materialize a pocket coordinate sidecar before attempting pocket-restricted Foldseek NN. Pocket eligibility is still coverage-only.
- A full current702 ESM-2 150M mechanism-NN comparator is still absent from the repository; only external review-only 150M sidecars were found. Full current702 ProtT5, SaProt, and separate 3Di-token NN metrics were not found.

## Orchestration Update

- 2026-05-26T05:06Z: the stale shell-credential push blocker is resolved for
  this branch. `research/representation-foldseek-pocket` is pushed to origin at
  `241fa71`, including the refreshed Foldseek Wave 1 status. No further human
  push action is required for this handoff state.
