# Lever 2 Protected Train/Cal Approved-Sidecar Electron-Flow Import Readout - current702

Run: 2026-06-06T05:26:36Z

Lever 2 protected train/cal-only approved-sidecar electron-flow import test. It applies the 35-row smoke tranche first to an approved-sidecar-shaped artifact copy, reruns the fixed namespaced direct source-free electron-flow operating point, and expands to the remaining 39 current-split rows only if smoke has zero primary positives and preserves primary retention. It does not use heldout, train or tune thresholds, alter labels, registries, ontologies, production thresholds, heldout splits, or Lever 3 surfaces.

## Status

- lever2_source_free_electron_flow_protected_train_cal_approved_sidecar_import_readout_deployment_candidate_protected_train_cal_approved_sidecar_electron_flow_import_signal
- Result class: deployment_candidate_protected_train_cal_approved_sidecar_electron_flow_import_signal
- Classification: deployment-candidate
- Critical guardrail violations: 0
- Source approved sidecar path modified: False

## Protected Smoke Import

- Smoke import rows: 35 (34 new, 1 update)
- Approved-sidecar rows after smoke import: 77
- Namespaced direct source-free fields: 8
- Generic electron-transfer overwrite violations: 0

## Approved-Sidecar Smoke Operating Point

| rows complete | primary positives | primary retain | retained-OOS IDs | OOS recall | delta vs geometry/fold | matches research overlay |
| ---: | ---: | ---: | --- | ---: | ---: | --- |
| 35/35 | 0 | 1.0 | m_csa:104 | 0.48 | 0.013333 | True |

## Full 74-Row Approved-Sidecar Operating Point

- Remaining rows applied after smoke: 39
- Approved-sidecar rows after full import: 116

| rows complete | primary positives | primary retain | retained-OOS IDs | OOS recall | delta vs geometry/fold | matches research overlay |
| ---: | ---: | ---: | --- | ---: | ---: | --- |
| 74/74 | 0 | 1.0 | m_csa:104, m_csa:119, m_csa:464 | 0.506667 | 0.04 | True |

## Decision

- Import class: deployment-candidate
- Smoke applied first: True
- Smoke has zero primary positives: True
- Smoke preserves primary retention: True
- Remaining tranche applied after smoke: True
- Full gate preserves primary retention: True
- Full gate adds value beyond geometry/fold: True
- Approved-sidecar rerun differs from research overlay: False
- Smallest failing tranche: None
- Production thresholds changed: False
- Heldout rows evaluated: False
- Lever 3 surfaces modified: False

## Interpretation

- Protected train/cal approved-sidecar electron-flow import is deployment-candidate: smoke passes first with zero primary positives and primary retain recall 1.0, then the full 74-row import reproduces the research-only overlay with OOS recall 0.506667 and delta 0.04.
- The approved-sidecar rerun matches the research-only overlay for every compared smoke/full gate field.
