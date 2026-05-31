# Selected Organic Cofactor Score Sidecars current702

Run: `2026-05-31T01:37:13Z`

## Decision

Resolved. The previous ESM2-150M fallback is no longer the active selected organic cofactor sidecar.

The original intended ESM2 t6/t12 row-level sidecars were regenerated with fallback disabled, the original 2026-05-29 sequence cofactor channel was rebuilt, and the selected organic sidecar now carries strict original selected t6/t12 scores:

- flavin: `trained:esm2_t12_35m`
- heme: `trained:esm2_t6_8m`
- PLP: `trained:esm2_t6_8m`

No labels, registries, ontologies, imports, production scoring, global thresholds, heldout splits, or model weights were changed.

## Outputs

- `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529.jsonl`
- `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529_summary.json`
- `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529.jsonl`
- `artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529_summary.json`
- `artifacts/v3_sequence_cofactor_channel_current702_20260529.json`
- `artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json`
- `artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`
- `work/mechanism_relationship_eval_cofactor_augmented_current702_20260530.md`

## Counts

- Current rows: 702
- Organic classes: flavin, heme, PLP
- Row-class records: 2106
- Non-null selected scores:
  - flavin: 702/702
  - heme: 702/702
  - PLP: 702/702
- Source counts:
  - `trained:esm2_t12_35m`: 702
  - `trained:esm2_t6_8m`: 1404
- Missingness flags:
  - `score_predicted_for_row_without_clean_experimental_cofactor_label`: 60 row-class records (20 entries x 3 classes)

## Blocker Resolution

The original problem was artifact retention: the 2026-05-29 summaries said t6/t12 emitted 702 rows, but the t6 JSONL was committed as 0 bytes, the t12 JSONL was never committed, and the full sequence cofactor channel JSON was never committed.

This run resolved that by regenerating the original selected models directly:

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-embedding-sidecar \
  --sequence-manifest artifacts/v3_sequence_manifest_current702_repaired_20260525.json \
  --fasta artifacts/v3_sequence_distance_holdout_eval_current702_repaired_20260525.fasta \
  --embedding-backend esm2_t6_8m_ur50d \
  --model-name facebook/esm2_t6_8M_UR50D \
  --no-fallback-to-largest-local-esm2 \
  --out artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529.jsonl \
  --summary artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529_summary.json
```

```bash
PYTHONPATH=src python -m catalytic_earth.cli build-sequence-embedding-sidecar \
  --sequence-manifest artifacts/v3_sequence_manifest_current702_repaired_20260525.json \
  --fasta artifacts/v3_sequence_distance_holdout_eval_current702_repaired_20260525.fasta \
  --embedding-backend esm2_t12_35m_ur50d \
  --model-name facebook/esm2_t12_35M_UR50D \
  --no-fallback-to-largest-local-esm2 \
  --out artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529.jsonl \
  --summary artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529_summary.json
```

Then `write_sequence_cofactor_channel` rebuilt `artifacts/v3_sequence_cofactor_channel_current702_20260529.json` from the strict t6/t12 sidecars and M-Ionic metal artifact.

The selected organic sidecar fits one-vs-rest logistic heads on clean in-distribution rows only, then emits selected scores for all 702 current rows. Heldout labels are not used for fitting or threshold selection.

## D11 Rerun

The cofactor-augmented D11 relationship eval was rerun after replacing the fallback sidecar.

Key metrics from `artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json`:

- Baseline predicted-geometry cosine family top3: `0.8`
- Strict t6/t12 cofactor-augmented cosine family top3: `0.866667`
- Strict t6/t12 cofactor-augmented cosine exact top1: `0.822222`
- Strict t6/t12 non-tuning-adjacent cosine family top3: `0.923077`

The report now states: `Organic cofactor scores use the strict original selected t6/t12 ESM heads with row-level sidecars retained.`

## Validation

- `python -m json.tool artifacts/v3_sequence_embedding_sidecar_current702_esm2_t6_8m_20260529_summary.json >/dev/null` passed.
- `python -m json.tool artifacts/v3_sequence_embedding_sidecar_current702_esm2_t12_35m_20260529_summary.json >/dev/null` passed.
- `python -m json.tool artifacts/v3_sequence_cofactor_channel_current702_20260529.json >/dev/null` passed.
- `python -m json.tool artifacts/v3_selected_organic_cofactor_score_sidecars_current702_20260530.json >/dev/null` passed.
- `python -m json.tool artifacts/v3_mechanism_relationship_eval_cofactor_augmented_current702_20260530.json >/dev/null` passed.
- `PYTHONPATH=src python -m catalytic_earth.cli validate` passed.
- `git diff --check` passed.
- `python -m compileall -q src/catalytic_earth` passed.
- `PYTHONPATH=src python -m unittest tests.test_sequence_cofactor_channel tests.test_cofactor_channel_probe` passed.
- `PYTHONPATH=src python -m unittest discover -s tests` passed: 959 tests.

## Handoff

- Wall-clock start: `2026-05-30T20:20:00-0500`
- Wall-clock end: `2026-05-30T20:47:00-0500`
- Elapsed time: about 27 minutes
- Git branch: `main`
- Git HEAD before commit: `482cf2c`
- Dirty files after repair: strict t6/t12 sidecars, rebuilt sequence cofactor channel, strict selected organic sidecar, cofactor-augmented D11 report, and `src/catalytic_earth/mechanism_relationship_eval.py` caveat logic update.
- Blockers: none for D11 row-level cofactor sidecars.
- Exact next action: commit and push the strict original t6/t12 repair. After that, treat the strict D11 artifact as the current D11 result; the fallback artifact is superseded.
- Next run should: stop this blocker thread unless new D11 analysis is requested.
