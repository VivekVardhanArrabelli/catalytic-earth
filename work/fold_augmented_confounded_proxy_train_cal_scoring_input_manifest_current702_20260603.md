# Fold-Augmented Confounded Proxy Train/Cal Scoring Input Manifest - current702

Run: 2026-06-03T14:44:38Z

Read-only input manifest for scoring the selected Lever 3 confounded-proxy train/cal OOS tranche with predicted structures against the threshold-contract train atlas. It maps tranche rows to sequence-manifest accessions, expected AFDB-v6 CIF paths, train-atlas targets, and rerun commands without downloading coordinates or parsing scores.

## Status

- confounded_proxy_train_cal_scoring_input_manifest_staged_missing_coordinates
- Scoring tranche rows: 50
- Unique query accessions: 50
- Query coordinate files missing: 50
- Train-atlas target coordinate files missing: 0
- Foldseek result TSV exists: 0
- Foldseek runtime available: True
- Blockers: ['tranche_query_coordinate_files_missing', 'tranche_foldseek_tsv_not_run']

## Decision

- Score tranche now: False
- Apply/change threshold now: False
- Proxy calibration rerun ready now: False
- Coordinate manifest ready for fetch: True
- Foldseek ready to run after coordinates: True
- Next gate: Materialize the 50 missing tranche query AFDB-v6 CIFs, stage the tranche query and threshold-contract train-target Foldseek directories, run the recorded Foldseek command, then parse scores back into train/cal OOS rows before rerunning the fixed-threshold proxy audit.

## Missing Query Coordinates

| accession | rows | expected path |
| --- | --- | --- |
| O81192 | m_csa:259 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_O81192_v6.cif |
| P04177 | m_csa:134 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P04177_v6.cif |
| P05164 | m_csa:601 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P05164_v6.cif |
| P06169 | m_csa:215 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P06169_v6.cif |
| P07071 | m_csa:416 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P07071_v6.cif |
| P07342 | m_csa:289 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P07342_v6.cif |
| P07598 | m_csa:127 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P07598_v6.cif |
| P07658 | m_csa:562 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P07658_v6.cif |
| P08200 | m_csa:7 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P08200_v6.cif |
| P08536 | m_csa:287 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P08536_v6.cif |
| P0A110 | m_csa:130 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P0A110_v6.cif |
| P0A796 | m_csa:365 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P0A796_v6.cif |
| P0A8M3 | m_csa:540 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P0A8M3_v6.cif |
| P0AEP7 | m_csa:298 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P0AEP7_v6.cif |
| P11409 | m_csa:427 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P11409_v6.cif |
| P11974 | m_csa:326 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P11974_v6.cif |
| P11986 | m_csa:331 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P11986_v6.cif |
| P12070 | m_csa:308 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P12070_v6.cif |
| P13009 | m_csa:268 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P13009_v6.cif |
| P13255 | m_csa:23 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P13255_v6.cif |
| P14925 | m_csa:135 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P14925_v6.cif |
| P16455 | m_csa:251 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P16455_v6.cif |
| P17846 | m_csa:398 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P17846_v6.cif |
| P20004 | m_csa:552 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P20004_v6.cif |
| P22259 | m_csa:51 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P22259_v6.cif |
| P22983 | m_csa:207 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P22983_v6.cif |
| P23368 | m_csa:21 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P23368_v6.cif |
| P23532 | m_csa:514 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P23532_v6.cif |
| P27001 | m_csa:539 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P27001_v6.cif |
| P32170 | m_csa:488 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P32170_v6.cif |
| P38539 | m_csa:99 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P38539_v6.cif |
| P43912 | m_csa:332 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P43912_v6.cif |
| P48637 | m_csa:498 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P48637_v6.cif |
| P51016 | m_csa:652 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P51016_v6.cif |
| P53686 | m_csa:240 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P53686_v6.cif |
| P61112 | m_csa:179 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P61112_v6.cif |
| P69922 | m_csa:95 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P69922_v6.cif |
| P77541 | m_csa:182 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P77541_v6.cif |
| P80457 | m_csa:139 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P80457_v6.cif |
| P9WKK7 | m_csa:272 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_P9WKK7_v6.cif |
| Q05514 | m_csa:468 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q05514_v6.cif |
| Q43088 | m_csa:604 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q43088_v6.cif |
| Q53176 | m_csa:276 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q53176_v6.cif |
| Q60364 | m_csa:648 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q60364_v6.cif |
| Q76K71 | m_csa:361 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q76K71_v6.cif |
| Q8EMJ9 | m_csa:502 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q8EMJ9_v6.cif |
| Q9F4L3 | m_csa:221 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q9F4L3_v6.cif |
| Q9K499 | m_csa:263 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q9K499_v6.cif |
| Q9LCV9 | m_csa:367 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q9LCV9_v6.cif |
| Q9SE42 | m_csa:270 | artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/confounded_proxy_train_cal_tranche_queries/afdb_Q9SE42_v6.cif |

## Commands

Materialize the missing tranche query coordinates:

```bash
python - <<'PY'
import json
import urllib.request
from pathlib import Path
artifact = json.loads(Path('artifacts/v3_fold_augmented_confounded_proxy_train_cal_scoring_input_manifest_current702_20260603.json').read_text())
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
artifact = json.loads(Path('artifacts/v3_fold_augmented_confounded_proxy_train_cal_scoring_input_manifest_current702_20260603.json').read_text())
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
/private/tmp/catalytic-foldseek-env/bin/foldseek easy-search /private/tmp/catalytic_confounded_proxy_tranche_foldseek/queries /private/tmp/catalytic_confounded_proxy_tranche_foldseek/train_atlas_targets artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/confounded_proxy_train_cal_tranche_vs_train_atlas.tsv artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/tmp_confounded_proxy_tranche_vs_train_atlas --format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits --exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 --exact-tmscore 1 --threads 4 -v 1
```

## Interpretation

- 50 selected train/cal OOS rows are mapped to 50 unique query accessions.
- 50 tranche query coordinate files are missing; 0 threshold-contract train-atlas target files are missing.
- Use the recorded materialization and Foldseek commands to score exactly this train/cal tranche; do not count rows as abstained evidence until parsed scores exist.
