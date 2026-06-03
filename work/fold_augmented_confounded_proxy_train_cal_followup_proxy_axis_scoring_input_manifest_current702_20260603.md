# Fold-Augmented Confounded Proxy Train/Cal Scoring Input Manifest - current702

Run: 2026-06-03T18:09:21Z

Read-only input manifest for scoring the selected Lever 3 confounded-proxy train/cal OOS tranche with predicted structures against the threshold-contract train atlas. It maps tranche rows to sequence-manifest accessions, expected AFDB-v6 CIF paths, train-atlas targets, and rerun commands without downloading coordinates or parsing scores.

## Status

- confounded_proxy_train_cal_scoring_input_manifest_scored_ready_to_parse
- Scoring tranche rows: 4
- Unique query accessions: 4
- Query coordinate files missing: 0
- Train-atlas target coordinate files missing: 0
- Foldseek result TSV exists: 1
- Foldseek current-query hits: 4
- Foldseek runtime available: True
- Blockers: []

## Decision

- Score tranche now: False
- Apply/change threshold now: False
- Proxy calibration rerun ready now: False
- Coordinate manifest ready for fetch: True
- Foldseek ready to run after coordinates: True
- Next gate: Materialize the 0 missing tranche query AFDB-v6 CIFs if available; if the Foldseek TSV already has 4 current-query hits, parse those partial scores back into train/cal OOS rows before rerunning the fixed-threshold proxy audit.

## Missing Query Coordinates

| accession | rows | expected path |
| --- | --- | --- |

## Commands

Materialize the missing tranche query coordinates:

```bash
python - <<'PY'
import json
import urllib.request
from pathlib import Path
artifact = json.loads(Path('artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scoring_input_manifest_current702_20260603.json').read_text())
queries = artifact['foldseek_input_manifest']['coordinate_request_groups']['confounded_proxy_train_cal_tranche_queries']
for item in queries:
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

Stage the tranche Foldseek directories:

```bash
python - <<'PY'
import json
import shutil
from pathlib import Path
artifact = json.loads(Path('artifacts/v3_fold_augmented_confounded_proxy_train_cal_followup_proxy_axis_scoring_input_manifest_current702_20260603.json').read_text())
groups = artifact['foldseek_input_manifest']['coordinate_request_groups']
root = Path('/private/tmp/catalytic_confounded_proxy_tranche_foldseek')
if root.exists():
    shutil.rmtree(root)
query_dir = root / 'queries'
target_dir = root / 'train_atlas_targets'
query_dir.mkdir(parents=True)
target_dir.mkdir(parents=True)
for src_group, dst_dir in (
    ('confounded_proxy_train_cal_tranche_queries', query_dir),
    ('threshold_contract_train_atlas_targets', target_dir),
):
    for item in groups.get(src_group, []):
        src = Path(item.get('expected_local_path') or '')
        if not src.exists():
            continue
        dst = dst_dir / src.name
        if not dst.exists():
            dst.symlink_to(src.resolve())
print({'queries': len(list(query_dir.iterdir())), 'targets': len(list(target_dir.iterdir()))})
PY
```

Run the tranche against the threshold-contract train atlas:

```bash
/private/tmp/catalytic-foldseek-env/bin/foldseek easy-search /private/tmp/catalytic_confounded_proxy_tranche_foldseek/queries /private/tmp/catalytic_confounded_proxy_tranche_foldseek/train_atlas_targets artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/confounded_proxy_train_cal_followup_proxy_axis_vs_train_atlas.tsv artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/tmp_confounded_proxy_tranche_vs_train_atlas --format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits --exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 --exact-tmscore 1 --threads 4 -v 1
```

## Interpretation

- 4 selected train/cal OOS rows are mapped to 4 unique query accessions.
- 0 tranche query coordinate files are missing; 0 threshold-contract train-atlas target files are missing.
- Use the recorded materialization and Foldseek commands to score exactly this train/cal tranche; do not count rows as abstained evidence until parsed scores exist.
