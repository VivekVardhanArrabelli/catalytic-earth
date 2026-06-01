# Fold-Augmented Abstention Threshold Contract - current702

Run: 2026-06-01T04:11:52Z

Leakage-safe thresholding contract for the fold-augmented abstention diagnostic. Thresholds are selected on deterministic in-distribution calibration rows only; heldout rows are final evaluation diagnostics.

## Status

- computed_train_cal_threshold_contract
- Blockers: []
- Train rows: 134
- Calibration rows scored: 34 / 34
- Heldout final-eval rows: 126

## Primary Channel

- Channel: combined_mean_geometry_fold
- Calibration-selected 90% threshold: {'threshold': 0.44155, 'min_retain_target': 0.9, 'calibration_in_scope_retain_recall': 0.9118, 'calibration_in_scope_retained': 31, 'calibration_in_scope_total': 34}
- Heldout final eval at that threshold: {'threshold': 0.44155, 'heldout_in_scope_retained': 45, 'heldout_in_scope_total': 47, 'heldout_in_scope_retain_recall': 0.9574, 'heldout_oos_abstained': 44, 'heldout_oos_total': 79, 'heldout_oos_abstain_recall': 0.557, 'heldout_confounded_oos_abstained': 5, 'heldout_confounded_oos_total': 6, 'heldout_confounded_oos_abstain_recall': 0.8333}

## Thresholds

| Channel | cal >=90 threshold | heldout in-scope retain | heldout OOS abstain | heldout confounded abstain |
| --- | ---: | ---: | ---: | ---: |
| cofactor_max_score | 0.022422 | 0.8723 | 0.2532 | 0.0 |
| combined_mean_geometry_cofactor_fold | 0.357468 | 0.9574 | 0.6329 | 0.0 |
| combined_mean_geometry_fold | 0.44155 | 0.9574 | 0.557 | 0.8333 |
| combined_min_geometry_fold | 0.338 | 0.9362 | 0.1266 | 0.1667 |
| fold_nearest_atlas_tm_score | 0.4325 | 0.9574 | 0.2785 | 0.3333 |
| geometry_top1_score | 0.338 | 0.9362 | 0.1266 | 0.1667 |

## Contract

- highest_score_threshold_retaining_at_least_target_fraction_of_in_scope_calibration_rows
- The current predicted-geometry atlas contains in-distribution fingerprint rows, not train/cal OOS negatives. Thresholds therefore control in-scope retention only; OOS abstain recall remains a final heldout diagnostic.
- research_contract_not_production_threshold; no production scorer or global threshold was changed

## Commands

Materialize the atlas coordinate bundle:

```bash
python - <<'PY'
import json
import urllib.request
from pathlib import Path
artifact = json.loads(Path('artifacts/v3_predicted_structure_fold_channel_current702_20260601.json').read_text())
atlas = artifact['foldseek_input_manifest']['coordinate_request_groups']['atlas_in_distribution']
for item in atlas:
    path = item.get('expected_local_path')
    url = item.get('url')
    if not path or not url:
        continue
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        continue
    urllib.request.urlretrieve(url, target)
PY
```

Stage the calibration-query and train-target Foldseek directories:

```bash
python - <<'PY'
import json
import shutil
from pathlib import Path
contract = json.loads(Path('artifacts/v3_fold_augmented_abstention_threshold_contract_current702_20260601.json').read_text())
fold = json.loads(Path('artifacts/v3_predicted_structure_fold_channel_current702_20260601.json').read_text())
root = Path('/private/tmp/catalytic_threshold_train_cal_foldseek')
if root.exists():
    shutil.rmtree(root)
query_dir = root / 'calibration_queries'
target_dir = root / 'train_targets'
query_dir.mkdir(parents=True)
target_dir.mkdir(parents=True)
cal = set(contract['train_cal_partition']['calibration_entry_ids'])
train = set(contract['train_cal_partition']['train_entry_ids'])
atlas = fold['foldseek_input_manifest']['coordinate_request_groups']['atlas_in_distribution']
for item in atlas:
    src = Path(item['expected_local_path'])
    if not src.exists():
        continue
    ids = set(item.get('entry_ids') or [])
    if ids & cal:
        dst = query_dir / src.name
        if not dst.exists():
            dst.symlink_to(src.resolve())
    if ids & train:
        dst = target_dir / src.name
        if not dst.exists():
            dst.symlink_to(src.resolve())
print({'queries': len(list(query_dir.iterdir())), 'targets': len(list(target_dir.iterdir()))})
PY
```

Run the in-distribution Foldseek pass:

```bash
/private/tmp/catalytic-foldseek-env/bin/foldseek easy-search /private/tmp/catalytic_threshold_train_cal_foldseek/calibration_queries /private/tmp/catalytic_threshold_train_cal_foldseek/train_targets artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/in_distribution_atlas_self_vs_atlas.tsv artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/tmp_in_distribution_atlas_self_vs_atlas --format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits --exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 --exact-tmscore 1 --threads 4 -v 1
```

Rerun the parser:

```bash
PYTHONPATH=src python -m catalytic_earth.cli eval-fold-augmented-abstention-threshold-contract --train-cal-foldseek-tsv artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/in_distribution_atlas_self_vs_atlas.tsv
```

## Interpretation

- Train/cal thresholds were selected without heldout threshold tuning.
