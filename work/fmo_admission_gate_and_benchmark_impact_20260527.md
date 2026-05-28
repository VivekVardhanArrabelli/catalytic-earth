# FMO Admission Gate and Benchmark Impact - 2026-05-27

Status: `blocked_missing_parallel_fmo_artifacts`.

This is a waiting/blocker artifact, not an import run. The v2 fingerprint proposal is present and names two context candidates, but the candidate scout, geometry, source-evidence, and hard-negative artifacts are missing, so no candidate is ready for a human review packet.

## Inputs

Present:

| path | role |
| --- | --- |
| `artifacts/v3_fmo_v2_fingerprint_design_proposal_702_20260527.json` | Future v2 design context; proposal-only candidate context |
| `artifacts/v3_wave1_1_diagnostic_benchmark_result_702_20260527.json` | Wave 1.1 diagnostic benchmark context only |

Missing required inputs:

| path | missing impact |
| --- | --- |
| `artifacts/v3_fmo_mcsa_candidate_scout_702_20260527.json` | No candidate list or candidate-level claims are available. |
| `artifacts/v3_fmo_structure_geometry_audit_702_20260527.json` | Geometry support and geometry failure modes cannot be assessed. |
| `artifacts/v3_fmo_source_evidence_scout_702_20260527.json` | Source evidence and source-transfer risk cannot be assessed. |
| `artifacts/v3_fmo_hard_negative_counteraxis_702_20260527.json` | Candidate-specific hard negative controls cannot be named. |

## Admission Gate Result

No FMO candidates are ready for a human review packet in this run. The present v2 proposal lists `m_csa:551` and `m_csa:973` as clean future context candidates, but both remain blocked because the candidate scout, geometry audit, source-evidence scout, and hard-negative counteraxis artifacts are missing.

| candidate | ready for human review packet | blocked reason | clean support impact if later approved | benchmark impact if later approved | hard negatives required |
| --- | --- | --- | --- | --- | --- |
| `m_csa:551` phenol 2-monooxygenase | no | Proposal-only context; missing candidate scout, geometry, source evidence, and hard-negative counteraxis. | Conditional increase toward four clean FMO rows if expert accepted and evidence gates pass. | Still secondary/acquisition-target or later pilot-only; four clean rows remain below `n>=6`. | Class-level FMO controls plus candidate-specific counteraxis controls. |
| `m_csa:973` DszC protein | no | Proposal-only context; missing candidate scout, geometry, source evidence, and hard-negative counteraxis. | Conditional increase toward four clean FMO rows if expert accepted and evidence gates pass. | Still secondary/acquisition-target or later pilot-only; four clean rows remain below `n>=6`. | Class-level FMO controls plus candidate-specific counteraxis controls. |

## Benchmark Context

The available Wave 1.1 benchmark remains useful context only. It reports a review-only diagnostic result where active-site geometry resolves the near-orphan and wrong-Foldseek-transfer slices, while child-label and mixed-chemistry cells remain underpowered or blocked. That context does not identify FMO candidates, prove clean FMO support, or justify adding candidates to Wave 1.1 or future v2 diagnostics.

The present v2 proposal keeps `flavin_monooxygenase` as `secondary_ood_probe_and_future_acquisition_target`. It reports two canonical FMO rows and two future context candidates, for a possible clean count of four only if the future candidates are expert accepted. That is still below the proposed `n>=6` floor and lacks hard-negative separation, so it does not support a primary supervised metric, production scoring, threshold tuning, label import, or canonical child registry entry.

## Required Next Inputs

Before this gate can produce candidate-level decisions, provide:

1. `artifacts/v3_fmo_mcsa_candidate_scout_702_20260527.json`
2. `artifacts/v3_fmo_structure_geometry_audit_702_20260527.json`
3. `artifacts/v3_fmo_source_evidence_scout_702_20260527.json`
4. `artifacts/v3_fmo_hard_negative_counteraxis_702_20260527.json`

## Guardrails

- No canonical label changes were made.
- No imports were run.
- No ontology edits, thresholds, model training, production scoring, or registry edits were made.
- Any future proposed candidates must remain `requires_human_approval_before_registry_edit`.
