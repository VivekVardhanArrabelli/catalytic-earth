# External Source Transfer

The 1,025 preview shows that M-CSA-only tranche growth is no longer the right
path to 10,000 countable labels. The current M-CSA slice exposes 1,003 source
records, while the benchmark target is 10,000 countable labels. External-source
transfer is therefore a new methodology, not a continuation of M-CSA label
import.

## Current State

- Canonical countable labels remain at 679.
- The 1,025 preview passes 21/21 label-factory gates but adds 0 clean countable
  labels.
- All 329 preview review-state rows remain non-countable.
- External UniProtKB/Swiss-Prot artifacts are review-only and create 0
  countable label candidates.
- The first read-only external sample has 30 candidates across six query lanes,
  0 fetch failures, and a clean non-countable guardrail audit.

## Artifacts

```bash
PYTHONPATH=src python -m catalytic_earth.cli audit-source-scale-limits \
  --graph artifacts/v1_graph_1025.json \
  --prior-graph artifacts/v1_graph_1000.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --review-debt artifacts/v3_review_debt_summary_1025_preview.json \
  --label-expansion-candidates artifacts/v3_label_expansion_candidates_1025.json \
  --target-source-entries 1025 \
  --public-target-countable-labels 10000 \
  --out artifacts/v3_source_scale_limit_audit_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-transfer-manifest \
  --source-scale-audit artifacts/v3_source_scale_limit_audit_1025.json \
  --learned-retrieval-manifest artifacts/v3_learned_retrieval_manifest_1025.json \
  --sequence-similarity-failure-sets artifacts/v3_sequence_similarity_failure_sets_1025.json \
  --ontology-gap-audit artifacts/v3_mechanism_ontology_gap_audit_1025.json \
  --active-learning-queue artifacts/v3_active_learning_review_queue_1025_preview_batch.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --out artifacts/v3_external_source_transfer_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-query-manifest \
  --transfer-manifest artifacts/v3_external_source_transfer_manifest_1025.json \
  --ontology-gap-audit artifacts/v3_mechanism_ontology_gap_audit_1025.json \
  --max-lanes 8 \
  --out artifacts/v3_external_source_query_manifest_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-ood-calibration-plan \
  --query-manifest artifacts/v3_external_source_query_manifest_1025.json \
  --sequence-similarity-failure-sets artifacts/v3_sequence_similarity_failure_sets_1025.json \
  --labels artifacts/v3_countable_labels_batch_1025_preview.json \
  --out artifacts/v3_external_ood_calibration_plan_1025.json

PYTHONPATH=src python -m catalytic_earth.cli build-external-source-candidate-sample \
  --query-manifest artifacts/v3_external_source_query_manifest_1025.json \
  --max-records-per-lane 5 \
  --out artifacts/v3_external_source_candidate_sample_1025.json

PYTHONPATH=src python -m catalytic_earth.cli audit-external-source-candidate-sample \
  --candidate-sample artifacts/v3_external_source_candidate_sample_1025.json \
  --out artifacts/v3_external_source_candidate_sample_audit_1025.json
```

## Guardrails

External-source artifacts are not label registries. They must remain
non-countable until a future run builds explicit external candidate evidence,
OOD calibration, sequence-similarity failure controls, review exports, decision
artifacts, and the full label-factory gate.

Do not import external candidates directly into
`data/registries/curated_mechanism_labels.json`. The first safe external-source
milestone is a review-only candidate manifest that can fail cleanly without
changing the benchmark label count.
