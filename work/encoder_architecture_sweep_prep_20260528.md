# Encoder Architecture Sweep Prep (current702)

Generated: 2026-05-28

This is a prep/report artifact only. No training was started, no tensor cache was materialized, and no labels, registries, ontologies, thresholds, imports, production scoring, or existing model outputs were changed.

## Inputs Read

- Active-site encoder feature-spec automation prompt: paused after `artifacts/v3_active_site_encoder_feature_spec_702_20260528.json` and `work/active_site_encoder_feature_spec_20260528.md` were pushed.
- Feature spec/readiness: `artifacts/v3_active_site_encoder_feature_spec_702_20260528.json`
- Wave 1 split/eval contract: `artifacts/v3_sequence_nn_label_manifest_current702_20260525.json`, `artifacts/v3_sequence_distance_holdout_eval_1025_current702_split_assignment_repaired_20260525.json`, and `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_702.json`
- Wave 1 comparators and diagnostic cells: `artifacts/v3_wave1_representation_shootout_result_card_20260526.json`, `artifacts/v3_wave1_representation_shootout_result_card_702_20260527_addendum.json`, and `artifacts/v3_wave1_1_diagnostic_benchmark_result_702_20260527.json`
- Proposal-only v2 auxiliary source: `artifacts/v3_mechanism_fingerprint_v2_sublabel_audit_702_20260525.json`

## Readiness And Guardrails

- Current rows: 702.
- Frozen Wave 1 split: 562 in-distribution, 140 heldout.
- Minimal encoder-ready rows: 679/702.
- Encoder-ready split coverage: 544/562 in-distribution and 135/140 heldout.
- Heldout denominator: keep all 140 rows in coverage-aware reports; unavailable rows must carry `unavailable_reason`.
- Current prep environment has `torch`, but not `torch_geometric`, `gvp`, `e3nn`, `se3_transformer`, or `escnn`.
- Disk stayed below the requested 10 GiB floor before artifact writing despite safe cache cleanup, so this run did not build caches, install dependencies, or train.

Forbidden predictive fields for every architecture: EC numbers, entry/protein/reaction names, mechanism prose, expert notes, review rationales, source identifiers as categorical features, source paths, post-hoc repair flags, target labels, child-label IDs, and any heldout-derived vocab/scaler/threshold choice.

## Architecture Contracts

| Architecture | Inputs | Runtime/GPU | Pass Gate |
| --- | --- | --- | --- |
| `active_site_mlp_pooled_v0` | Pooled active-site residue/role counts, distance histograms, pocket/cofactor/metal summaries, masks | CPU, 5 seeds under 15 min | Beat Sequence-NN sanity baseline; promote if macro F1 >= ESM-2 0.696 or accuracy >= 0.578 with OOS FP <= 0.168 |
| `active_site_vanilla_graph_gnn_v0` | Active-site residue graph with CA/proxy distances and optional local atom side channel | 1 small GPU, 30-60 min | Beat MLP by >=0.02 macro F1 or match it with safer OOS; support >=15/17 near-orphan rows |
| `active_site_gvp_gnn_v0` | Scalar node features plus CA/centroid coordinates, direction vectors, radial distances | 1 GPU, 45-90 min; dependency-gated | Match/beat vanilla GNN with no OOS regression; strong if closes wrong-Foldseek-transfer rows |
| `active_site_small_se3_equivariant_v0` | Small SE(3)/equivariant local active-site structure model | 1 GPU, 1-3 hr; skip if deps absent | Only keep if it beats GVP/vanilla graph or uniquely fixes wrong-transfer rows without OOS cost |
| `sequence_window_only_baseline_v0` | Sequence-only whole sequence plus known active-site +/-64 window ablation | CPU, 10-30 min | Beat Sequence-NN 3-mer without structure features; window mode remains controlled ablation |

All models use the same heads: parent-v1 label group, binary in-scope/OOS calibration, and masked proposal-only v2 auxiliary if the target-granularity gate freezes that use. No canonical child-label metrics or imports are allowed.

## Exact Launch After Freeze

Do not run these until the active-site feature spec and target-granularity gate are frozen and disk is strictly above 10 GiB, preferably above 20 GiB.

```bash
export FREEZE_TAG=20260528_target_gate_frozen

df -k .
PYTHONPATH=src python -m catalytic_earth.cli validate
PYTHONPATH=src python -m catalytic_earth.cli validate-active-site-encoder-contract \
  --contract artifacts/v3_encoder_architecture_sweep_prep_702_20260528.json

PYTHONPATH=src python -m catalytic_earth.cli build-active-site-encoder-cache \
  --labels data/registries/curated_mechanism_labels.json \
  --geometry artifacts/v3_geometry_features_1025.json \
  --split artifacts/v3_sequence_nn_label_manifest_current702_20260525.json \
  --foldseek-readiness artifacts/v3_foldseek_coordinate_readiness_1000_current702_wave1_20260527.json \
  --coordinate-dir artifacts/v3_foldseek_coordinates_1000 \
  --out artifacts/v3_active_site_encoder_cache_current702_${FREEZE_TAG}.jsonl
```

Launch CPU baselines in parallel:

```bash
PYTHONPATH=src python -m catalytic_earth.cli run-active-site-encoder-experiment \
  --contract artifacts/v3_encoder_architecture_sweep_prep_702_20260528.json \
  --architecture active_site_mlp_pooled_v0 \
  --cache artifacts/v3_active_site_encoder_cache_current702_${FREEZE_TAG}.jsonl \
  --out-dir work/encoder_architecture_sweep_${FREEZE_TAG}/active_site_mlp_pooled_v0 \
  --seeds 11,23,37,53,71

PYTHONPATH=src python -m catalytic_earth.cli run-active-site-encoder-experiment \
  --contract artifacts/v3_encoder_architecture_sweep_prep_702_20260528.json \
  --architecture sequence_window_only_baseline_v0 \
  --cache artifacts/v3_active_site_encoder_cache_current702_${FREEZE_TAG}.jsonl \
  --out-dir work/encoder_architecture_sweep_${FREEZE_TAG}/sequence_window_only_baseline_v0 \
  --seeds 11,23,37,53,71
```

Launch graph models on separate GPUs if available:

```bash
PYTHONPATH=src python -m catalytic_earth.cli run-active-site-encoder-experiment \
  --contract artifacts/v3_encoder_architecture_sweep_prep_702_20260528.json \
  --architecture active_site_vanilla_graph_gnn_v0 \
  --cache artifacts/v3_active_site_encoder_cache_current702_${FREEZE_TAG}.jsonl \
  --out-dir work/encoder_architecture_sweep_${FREEZE_TAG}/active_site_vanilla_graph_gnn_v0 \
  --seeds 11,23,37,53,71

PYTHONPATH=src python -m catalytic_earth.cli run-active-site-encoder-experiment \
  --contract artifacts/v3_encoder_architecture_sweep_prep_702_20260528.json \
  --architecture active_site_gvp_gnn_v0 \
  --cache artifacts/v3_active_site_encoder_cache_current702_${FREEZE_TAG}.jsonl \
  --out-dir work/encoder_architecture_sweep_${FREEZE_TAG}/active_site_gvp_gnn_v0 \
  --seeds 11,23,37,53,71
```

Run the SE(3)/equivariant model only if dependencies already exist:

```bash
PYTHONPATH=src python -m catalytic_earth.cli run-active-site-encoder-experiment \
  --contract artifacts/v3_encoder_architecture_sweep_prep_702_20260528.json \
  --architecture active_site_small_se3_equivariant_v0 \
  --cache artifacts/v3_active_site_encoder_cache_current702_${FREEZE_TAG}.jsonl \
  --out-dir work/encoder_architecture_sweep_${FREEZE_TAG}/active_site_small_se3_equivariant_v0 \
  --seeds 11,23,37,53,71 \
  --skip-if-dependencies-missing
```

Aggregate after all launched runs complete:

```bash
PYTHONPATH=src python -m catalytic_earth.cli aggregate-active-site-encoder-sweep \
  --contract artifacts/v3_encoder_architecture_sweep_prep_702_20260528.json \
  --run-dir work/encoder_architecture_sweep_${FREEZE_TAG} \
  --out artifacts/v3_encoder_architecture_sweep_result_card_702_${FREEZE_TAG}.json
```

## Output Contract

Each run should write a summary JSON and row-level JSONL under new `v3_encoder_architecture_sweep_*` paths only. Required row fields are `entry_id`, `split_assignment`, `architecture_id`, `seed`, `available`, `unavailable_reason`, true/predicted parent labels, abstention flag, score/probability, masked v2 auxiliary fields, `predictive_inputs`, and `forbidden_inputs_used`.

Pass/fail is conjunctive: a model must improve the relevant comparator and keep OOS false non-abstention no worse than ESM-2 for promotion, or no worse than Foldseek for a strong pass. Geometry-specific value must be read from the near-orphan and wrong-Foldseek-transfer diagnostic cells, because the current geometry aggregate result-card metric is not standardized.
