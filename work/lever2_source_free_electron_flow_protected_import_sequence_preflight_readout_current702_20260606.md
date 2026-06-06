# Lever 2 Source-Free Electron-Flow Protected Import Sequence Preflight - current702

Run: 2026-06-06T01:38:07Z

Lever 2 measured source-free electron-flow protected-import sequence preflight. It consumes the verified delta-package acceptance contract, rechecks the current approved sidecar and source package hashes, stages the smoke-first then remaining current-split expansion sequence in memory, and reports gate readiness. It does not apply imports, edit approved sidecars, change thresholds, train models, read heldout, or touch labels, registries, ontologies, or Lever 3 surfaces.

## Status

- lever2_source_free_electron_flow_protected_import_sequence_preflight_readout_research_only_protected_import_sequence_preflight_ready
- Result class: research_only_protected_import_sequence_preflight_ready
- Protected import sequence ready: True
- Critical preflight failures: 0
- Protected imports executed: 0
- Approved sidecar rows written: 0

## Hash Preflight

- Current sidecar matches contract: True
- Source package file matches contract: True
- Source package normalized hash matches contract: True
- Source candidate matches contract: True
- Smoke delta rows match contract: True
- Remaining rows match contract: True
- Full delta rows match contract: True

## Staged Gates

| stage | rows | complete | new rows | updated rows | primary positives | retained-OOS IDs | primary retain | union OOS recall |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| smoke | 35 | 35 | 34 | 1 | 0 | m_csa:104 | 1.0 | 0.48 |
| full after smoke | 74 | 74 | 73 | 1 | 0 | m_csa:104, m_csa:119, m_csa:464 | 1.0 | 0.506667 |

## Decision

- Smoke-first preflight ready: True
- Remaining current-split expansion preflight ready: True
- Full gate adds value beyond geometry/fold: True
- Deployable now: False
- Remaining gap: The measured source-free electron-flow package is ready for the smoke-first protected import sequence, but this artifact does not authorize or execute protected imports.
- Smallest next experiment: With explicit protected import authorization, apply only the 35-row smoke tranche, rerun the smoke gate, then apply the remaining 39 rows only if the smoke gate preserves primary retention.

## Interpretation

- The exact smoke-first source-free electron-flow import sequence is hash-fresh and preflight-ready. The measured readout still stays research-only because protected import authorization is absent.
- Protected import authorization, then smoke-only application and gate rerun, remains the smallest next experiment.
