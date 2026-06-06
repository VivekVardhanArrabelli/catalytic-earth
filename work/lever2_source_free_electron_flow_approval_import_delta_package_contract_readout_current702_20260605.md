# Lever 2 Source-Free Electron-Flow Delta Package Contract Readout - current702

Run: 2026-06-06T00:42:23Z

Lever 2 measured acceptance contract for the direct source-free electron-flow delta package. It verifies the current approved train/cal sidecar and source candidate artifact still match the measured delta package, hashes the exact smoke and remaining current-split delta rows, checks the eight-field source-free electron-flow whitelist, and reports the fixed smoke/full gate evidence. It does not edit sidecars, imports, labels, registries, ontologies, thresholds, model weights, or heldout splits.

## Status

- lever2_source_free_electron_flow_approval_import_delta_package_contract_readout_research_only_import_contract_verified_pending_protected_import
- Result class: research_only_import_contract_verified_pending_protected_import
- Acceptance contract verified: True
- Current approved sidecar matches package: True
- Current candidate readout matches package: True
- Critical contract violations: 0

## Hash Contract

- Base sidecar SHA-256: 5f5823da51c42b70012b606821133ca5f252ac1525a7ce04d7e478f02d743bb0
- Candidate readout SHA-256: e075997a85fbc46442438bd64b4ca9f656669177b53acb6a8fb5d35c633ab90c
- Delta package normalized SHA-256: a254bef4f2f41c58a9f4e5f7a53df1efb4d726af2278dedd4fc7fa5618ac7c62
- Component positive matrix SHA-256: 79e911cc7400a64fc75911056fe1ebd86c83abd5b3d1eca1e9a7729bccd1cdf2
- Smoke delta rows SHA-256: 5c11dec9df466c8956a9e96cc6d8f6ff33bff80e94c0f151c469009e25dd312e
- Remaining current-split rows SHA-256: 9d1781cbe5fa6451cd2f1c796833b75f0f65b211cff978def233bf1e6f9c6ff8
- Full delta rows SHA-256: ff39d9cce93b57333aca77a3a63a7fd6c56fbe89fd102198c297948725da5d74

## Fixed Gates

| gate | delta rows | complete | primary positives | retained-OOS IDs | primary retain | union OOS recall |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| smoke | 35 | 35 | 0 | m_csa:104 | 1.0 | 0.48 |
| full 74-row | 74 | 74 | 0 | m_csa:104, m_csa:119, m_csa:464 | 1.0 | 0.506667 |

## Component Attribution

- PQQ retained-OOS positives: m_csa:104
- NAD-family retained-OOS positives: m_csa:464
- Fe-S/iron retained-OOS positives: m_csa:119
- Component attribution matches PQQ/NAD/Fe-S direct signal: True

## Decision

- Source delta package ready: True
- Delta rows use only direct source-free electron-flow fields: True
- Row counts match source package: True
- Full gate adds value beyond geometry/fold: True
- Protected surfaces modified: False
- Deployable now: False
- Remaining gap: Source-free electron-flow evidence and exact delta package are measured; protected approved-sidecar import authorization is still intentionally absent.
- Smallest next experiment: Under explicit protected import authorization, verify the base sidecar SHA-256 and delta-row hashes in this contract, apply the 35-row smoke tranche, rerun the smoke gate, then apply the remaining 39 rows and rerun the 74-row gate.

## Interpretation

- The current approved sidecar and source candidate readout match the measured delta package; the exact source-free electron-flow delta is hash-pinned, whitelist-clean, and ready for a future protected import.
- No further source-free electron-flow evidence is missing for the current train/cal split; the next action is protected import authorization and smoke-first application.
