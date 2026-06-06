# Lever 2 Source-Free Electron-Flow Approval Import Delta Package Readout - current702

Run: 2026-06-05T23:57:35Z

Lever 2 measured protected-delta package for the direct source-free electron-flow candidate sidecar route. It consumes the candidate-sidecar readout and the current approved train/cal feature sidecar, emits the exact smoke and remaining current-split delta rows needed for a future protected import, reconstructs the delta-applied sidecar states, and reruns the fixed gates from those reconstructed rows. It does not edit the approved sidecar, labels, registries, imports, thresholds, model weights, or heldout splits.

## Status

- lever2_source_free_electron_flow_approval_import_delta_package_readout_research_only_candidate_sidecar_delta_package_ready_pending_protected_import
- Result class: research_only_candidate_sidecar_delta_package_ready_pending_protected_import
- Approved sidecar rows before delta: 43
- Approved current-split direct rows before delta: 0
- Smoke delta rows: 35 (34 new, 1 update)
- Remaining current-split delta rows: 39
- Full delta field writes: 592
- Reconstructed sidecar rows after smoke/full delta: 77/116
- Critical violations: 0

## Fixed Gates

| gate | rows complete | primary positives | retained-OOS IDs | primary retain | union OOS recall | matches source |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| smoke | 35/35 | 0 | m_csa:104 | 1.0 | 0.48 | True |
| full 74-row | 74/74 | 0 | m_csa:104, m_csa:119, m_csa:464 | 1.0 | 0.506667 | True |

## Decision

- Protected smoke delta ready: True
- Protected full delta ready: True
- Full gate preserves primary retention: True
- Full gate adds value beyond geometry/fold: True
- Delta rows reconstruct candidate sidecar gates: True
- Approved sidecar modified: False
- Protected surfaces modified: False
- Deployable now: False
- Remaining gap: The exact source-free electron-flow smoke/full delta is ready as a research-only package, but canonical approved sidecar import remains intentionally unexecuted under this run's guardrails.
- Smallest next experiment: When protected import edits are explicitly allowed, apply the 35-row smoke delta first, rerun this smoke gate, then apply the remaining 39 current-split rows and rerun the full 74-row fixed gate.

## Interpretation

- The protected delta package reproduces the candidate smoke and full current-split gates, preserves all current primary rows, and catches m_csa:104, m_csa:119, and m_csa:464 with only direct source-free electron-flow fields.
- No source-free evidence blocker remains for the measured train/cal split; the next step is protected import authorization, not another evidence scan.
