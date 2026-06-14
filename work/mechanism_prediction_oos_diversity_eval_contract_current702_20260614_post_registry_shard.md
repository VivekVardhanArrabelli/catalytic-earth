# Mechanism Prediction OOS/Diversity Eval Contract - post registry sharding

Artifact: `artifacts/v3_mechanism_prediction_oos_and_diversity_eval_contract_current702_20260614_post_registry_shard.json`

SHA-256: `b1c5e0acce61c1286236bf1c41177af20eea2ecc860c0a105596d2aed9640276`

This is a leakage-safe design artifact only. It does not run a benchmark, train a model,
change thresholds, or claim performance. It records the OOS tiering, diversity-stratified
accuracy, abstention diagnostics, canary, support-threshold, and pooling contract that any
future mechanism-prediction benchmark must cite before interpretation.

## Scope

- Baseline label count: 702.
- Schema: `mechanism_prediction_oos_and_diversity_eval_contract.v1`.
- Primary benchmark pooling mode: whole sequence.
- Required primary fingerprints: ser_his_acid_hydrolase, metal_dependent_hydrolase,
  plp_dependent_enzyme, flavin_dehydrogenase_reductase, heme_peroxidase_oxidase.
- Secondary OOD probes remain excluded from primary supervised metrics.

## Guardrails

- No label import, registry edit, fingerprint edit, ontology edit, benchmark run, model
  training, or production scoring change occurred.
- Forbidden predictive features remain EC labels, entry names, mechanism prose, expert
  notes, curator rationale text, review decision text, and source identifiers as semantic
  features.
- Any future benchmark must record this contract SHA and report OOS/diversity/abstention
  diagnostics before making an interpretation.

## Limitation

This regenerates the existing v1 702-scope contract under a dated path after the registry
sharding safety repair. It is not yet the new external-bronze-scale split design; the next
eval action is to design a current external-surface OOS tier assignment and split manifest.
