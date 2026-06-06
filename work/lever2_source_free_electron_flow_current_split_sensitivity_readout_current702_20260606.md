# Lever 2 Source-Free Electron-Flow Current-Split Sensitivity Readout - current702

Run: 2026-06-06T04:39:33Z

Lever 2 measured train/cal sensitivity readout for the direct source-free electron-flow operating point. It consumes the measured current-split operating-point artifact and computes leave-one-component and leave-one-retained-OOS-row ablations without applying protected imports, editing approved sidecars, changing thresholds, training models, scoring heldout, or touching labels, registries, ontologies, or Lever 3 surfaces.

## Status

- lever2_source_free_electron_flow_current_split_sensitivity_readout_research_only_direct_source_free_electron_flow_sensitivity_signal
- Result class: research_only_direct_source_free_electron_flow_sensitivity_signal
- Critical violations: 0
- Protected imports executed: 0
- Approved sidecar rows written: 0

## Sensitivity Summary

- Full positive rows: ['m_csa:104', 'm_csa:119', 'm_csa:464']
- Smoke positive rows: ['m_csa:104']
- Leave-one-component variants: 3, min delta 0.026667
- Leave-one-positive-row variants: 3, min delta 0.026667
- Smoke single-row minimal signal: True
- Component union matches full positives: True
- Component delta additive within tolerance: True

## Leave-One-Component Variants

| variant | removed | OOS recall | delta | primary positives | retained-OOS IDs |
| --- | --- | ---: | ---: | ---: | --- |
| full_current_split_without_pqq | pqq | 0.493334 | 0.026667 | 0 | m_csa:119, m_csa:464 |
| full_current_split_without_nad_family | nad_family | 0.493334 | 0.026667 | 0 | m_csa:104, m_csa:119 |
| full_current_split_without_iron_sulfur_or_iron | iron_sulfur_or_iron | 0.493334 | 0.026667 | 0 | m_csa:104, m_csa:464 |

## Leave-One-Positive-Row Variants

| variant | removed | OOS recall | delta | primary positives | retained-OOS IDs |
| --- | --- | ---: | ---: | ---: | --- |
| full_current_split_without_m_csa_104 | m_csa:104 | 0.493334 | 0.026667 | 0 | m_csa:119, m_csa:464 |
| full_current_split_without_m_csa_119 | m_csa:119 | 0.493334 | 0.026667 | 0 | m_csa:104, m_csa:464 |
| full_current_split_without_m_csa_464 | m_csa:464 | 0.493334 | 0.026667 | 0 | m_csa:104, m_csa:119 |

## Decision

- Sensitivity readout measured: True
- Survives leave-one-component: True
- Survives leave-one-positive-row: True
- Primary retention preserved under sensitivity: True
- Done-bar evidence reinforced: True
- Deployable now: False
- Remaining gap: No source-free electron-flow evidence gap remains for the current train/cal split; the remaining gap is explicit protected import authorization and approved-sidecar rerun.

## Interpretation

- Direct source-free electron-flow remains primary-safe and positive under any one-component or one-positive-row ablation of the full current split: minimum retained delta 0.026667 versus the current geometry/fold surface.
- Treat the remaining gap as protected import authorization, not missing source-free electron-flow evidence.
