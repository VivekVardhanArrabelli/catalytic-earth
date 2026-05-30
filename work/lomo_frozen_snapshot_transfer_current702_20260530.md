# LOMO Frozen Snapshot Transfer Diagnostic

Run: 2026-05-30T07:14:45Z

## Frozen Snapshot

- Expected tag: `snapshot/concordance-gate-current702-20260530`
- Expected commit: `f393ad25c3959778c7e66a68974bcfee6c93f031`
- Observed commit: `f393ad25c3959778c7e66a68974bcfee6c93f031`
- Tag verified at HEAD: `True`
- Free disk before write: `26` GiB; after write: `26` GiB.

## Guardrails

- No label, registry, ontology, import, production-scoring, threshold, or model-weight files were edited.
- No targeted expansion output was read into train/cal/test. The current702 label manifest was the row universe.
- Predictive inputs excluded EC/prose/mechanism text/name/source IDs. Geometry descriptors also excluded per-fingerprint retrieval/template scores for the LOMO run.
- M-CSA rows stayed in frozen benchmark/reference scope: only ephemeral diagnostic fits were run, with no import, promotion, production training, or persisted weights.

## Feasibility Matrix

| Track | Status | Current702 rows | Note |
| --- | --- | ---: | --- |
| `sequence_kmer_oos_aware_logistic` | `computed_dry_run` | 702 | deterministic sequence-only control; no labels retained in sidecar |
| `sequence_esm2_t6_8m_oos_aware_logistic` | `blocked_empty_jsonl_despite_summary` | 0 | summary claims 702 rows but local JSONL is 0 bytes; no huge model download attempted |
| `sequence_esm2_t12_35m_oos_aware_logistic` | `blocked_missing_jsonl_despite_summary` | 0 | summary exists but embedding row file is absent; no huge model download attempted |
| `geometry_local_descriptor_oos_aware_logistic` | `computed_dry_run` | 698 | filtered geometry_features_1025 to current702 entry IDs only; per-fingerprint retrieval/template score features removed |
| `active_site_encoder_cache_547` | `blocked_no_full_current702_or_heldout_cache` |  | cache is label-blind but train/cal feasibility only; not a complete frozen current702 LOMO eval matrix |

## LOMO Results

### Sequence k-mer OOS-aware logistic

Aggregate held-out-class coverage: 1/226 (0.004425).
Aggregate abstention: 225/226 (0.995575).
OOS hard gate pass across LOMO runs: `False`.

| Held-out class | Support | Coverage | Abstention | Top1 family | Top3 family | OOS FP | Gate | Failure modes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `flavin_dehydrogenase_reductase` | 50 | 0 (0.0) | 50 (1.0) | n/a | n/a | 0 | `True` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained |
| `heme_peroxidase_oxidase` | 20 | 0 (0.0) | 20 (1.0) | n/a | n/a | 0 | `True` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained |
| `metal_dependent_hydrolase` | 83 | 1 (0.012048) | 82 (0.987952) | 0.144578 | 0.783133 | 0 | `True` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained |
| `plp_dependent_enzyme` | 31 | 0 (0.0) | 31 (1.0) | n/a | n/a | 1 | `False` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained, oos_false_positive_hard_gate_failed |
| `ser_his_acid_hydrolase` | 42 | 0 (0.0) | 42 (1.0) | 0.52381 | 1.0 | 0 | `True` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained |

### Geometry local-descriptor OOS-aware logistic

Aggregate held-out-class coverage: 0/226 (0.0).
Aggregate abstention: 226/226 (1.0).
OOS hard gate pass across LOMO runs: `True`.

| Held-out class | Support | Coverage | Abstention | Top1 family | Top3 family | OOS FP | Gate | Failure modes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `flavin_dehydrogenase_reductase` | 50 | 0 (0.0) | 50 (1.0) | n/a | n/a | 0 | `True` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained |
| `heme_peroxidase_oxidase` | 20 | 0 (0.0) | 20 (1.0) | n/a | n/a | 0 | `True` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained |
| `metal_dependent_hydrolase` | 83 | 0 (0.0) | 83 (1.0) | 0.180723 | 0.349398 | 0 | `True` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained |
| `plp_dependent_enzyme` | 31 | 0 (0.0) | 31 (1.0) | n/a | n/a | 0 | `True` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained |
| `ser_his_acid_hydrolase` | 42 | 0 (0.0) | 42 (1.0) | 0.190476 | 0.5 | 0 | `True` | no_open_set_class_synthesis_exact_recovery_unavailable, heldout_class_mostly_abstained |

## Interpretation

- Transfer signal: `underpowered_no_exact_open_set_recovery`.
- OOS gate: `failed_for_at_least_one_computed_track`.
- Overall: Current frozen learned/feature path does not demonstrate reliable leave-one-mechanism-out transfer. Exact recovery is unavailable without a candidate class synthesis mechanism, surrogate family recovery is limited, and OOS false-positive behavior fails as a hard gate for computed dry-run tracks.

The exact held-out fingerprint cannot appear in top-k for this protocol because the class is deliberately absent from the candidate label space. The only computable top-k signal here is sibling-family/cofactor surrogate recovery, and that is sparse even before applying the OOS hard gate.
