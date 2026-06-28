# Current-57 Fold/TM Recompute Input Manifest

Run: 2026-06-28T03:50:26Z
Status: `current57_fold_tm_recompute_input_manifest_ready_foldseek_missing`

## Coverage

- Calibration queries: 61/61 staged train/cal-safe CIFs.
- Train in-scope targets: 133/133 staged train/cal-safe CIFs.
- Train reference queries: 235/235 staged train/cal-safe CIFs.

## Foldseek Command

```bash
foldseek easy-search artifacts/v3_current57_fold_tm_recompute_current702_20260628_coordinates/calibration_queries artifacts/v3_current57_fold_tm_recompute_current702_20260628_coordinates/train_in_scope_atlas artifacts/v3_current57_fold_tm_recompute_current702_20260628_results/calibration_vs_current57_train_atlas.tsv artifacts/v3_current57_fold_tm_recompute_current702_20260628_results/tmp_calibration_vs_current57_train_atlas --format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits --exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 --exact-tmscore 1 --threads 4 -v 1
```

## Guardrails

- No heldout rows were scored or read.
- No new Foldseek/TM scores were computed by this manifest.
- No production threshold, model weight, registry, ontology, label, or fingerprint-family change was made.
