# Fold-Augmented Train/Cal OOS Negative Surface Scores - current702

Run: 2026-06-01T06:37:42Z

Bounded predicted-geometry plus Foldseek feature surface for the hash-selected current702 in-distribution OOS calibration negatives needed by the fold-augmented threshold contract.

## Status

- computed_partial_train_cal_oos_negative_surface_scores
- Candidate IDs requested: 76
- Predicted geometry ok rows: 71
- Foldseek rows with nearest train hits: 74
- Full channel score rows: 70
- Foldseek TSV parse status: parsed

## Blockers

- some_calibration_oos_candidates_missing_predicted_geometry
- some_calibration_oos_candidates_missing_fold_scores
- candidate_query_coordinate_files_missing

## Score Preview

| Entry | geometry top1 | geometry score | nearest train atlas | fold TM | combined mean geometry/fold |
| --- | --- | ---: | --- | ---: | ---: |
| m_csa:4 | metal_dependent_hydrolase | 0.3646 | m_csa:42 | 0.3812 | 0.3729 |
| m_csa:17 | ser_his_acid_hydrolase | 0.3962 | m_csa:839 | 0.5215 | 0.45885 |
| m_csa:22 | metal_dependent_hydrolase | 0.3517 | m_csa:623 | 0.4964 | 0.42405 |
| m_csa:25 | metal_dependent_hydrolase | 0.3778 | m_csa:716 | 0.8704 | 0.6241 |
| m_csa:35 | metal_dependent_hydrolase | 0.5997 | m_csa:795 | 0.3937 | 0.4967 |
| m_csa:36 | metal_dependent_hydrolase | 0.3604 | m_csa:727 | 0.6753 | 0.51785 |
| m_csa:39 | metal_dependent_hydrolase | 0.5876 | m_csa:337 | 0.5767 | 0.58215 |
| m_csa:40 | flavin_monooxygenase | 0.2536 | m_csa:337 | 0.5809 | 0.41725 |
| m_csa:52 | metal_dependent_hydrolase | 0.5977 | m_csa:300 | 0.6331 | 0.6154 |
| m_csa:54 | heme_peroxidase_oxidase | 0.4074 | m_csa:697 | 0.7059 | 0.55665 |
| m_csa:57 | heme_peroxidase_oxidase | 0.357 | m_csa:472 | 0.4255 | 0.39125 |
| m_csa:61 | flavin_dehydrogenase_reductase | 0.303 | m_csa:699 | 0.6568 | 0.4799 |
| m_csa:65 | metal_dependent_hydrolase | 0.6047 | m_csa:631 | 0.4901 | 0.5474 |
| m_csa:78 | metal_dependent_hydrolase | 0.075 | None | None | None |
| m_csa:82 | plp_dependent_enzyme | 0.4001 | m_csa:518 | 0.548 | 0.47405 |
| m_csa:85 | metal_dependent_hydrolase | 0.3618 | m_csa:205 | 0.6373 | 0.49955 |
| m_csa:93 | metal_dependent_hydrolase | 0.3204 | m_csa:94 | 0.3853 | 0.35285 |
| m_csa:104 | metal_dependent_hydrolase | 0.5822 | m_csa:740 | 0.7174 | 0.6498 |
| m_csa:106 | metal_dependent_hydrolase | 0.3628 | m_csa:275 | 0.6479 | 0.50535 |
| m_csa:119 | metal_dependent_hydrolase | 0.3572 | m_csa:727 | 0.5354 | 0.4463 |
| m_csa:126 | metal_dependent_hydrolase | 0.6044 | m_csa:395 | 0.421 | 0.5127 |
| m_csa:136 | metal_dependent_hydrolase | 0.4161 | m_csa:795 | 0.614 | 0.51505 |
| m_csa:140 | heme_peroxidase_oxidase | 0.3933 | m_csa:697 | 0.4655 | 0.4294 |
| m_csa:145 | metal_dependent_hydrolase | 0.4308 | m_csa:706 | 0.3769 | 0.40385 |
| m_csa:149 | metal_dependent_hydrolase | 0.3713 | m_csa:358 | 0.3818 | 0.37655 |

## Commands

Materialize the candidate query and train-atlas target coordinate bundle:

```bash
python - <<'PY'
import json
import urllib.request
from pathlib import Path
artifact = json.loads(Path('artifacts/v3_fold_augmented_train_cal_oos_negative_surface_scores_current702_20260601.json').read_text())
groups = artifact['foldseek_input_manifest']['coordinate_request_groups']
for group in groups.values():
    for item in group:
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

Run Foldseek for calibration OOS negatives versus the train atlas:

```bash
/private/tmp/catalytic-foldseek-env/bin/foldseek easy-search /private/tmp/catalytic_train_cal_oos_negative_surface_foldseek/calibration_oos_queries /private/tmp/catalytic_train_cal_oos_negative_surface_foldseek/train_targets artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/train_cal_oos_negatives_vs_train_atlas.tsv artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/tmp_train_cal_oos_negatives_vs_train_atlas --format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits --exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 --exact-tmscore 1 --threads 4 -v 1
```

Rerun the parser:

```bash
PYTHONPATH=src python -m catalytic_earth.cli score-fold-augmented-train-cal-oos-negative-surface --train-cal-oos-foldseek-tsv artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/train_cal_oos_negatives_vs_train_atlas.tsv
```

## Interpretation

- The train/cal OOS negative surface now has predicted-geometry, cofactor, and nearest-train Foldseek/TM channel scores for the 70 score-complete candidate rows.
- Extend the fold-augmented threshold contract to consume these calibration OOS negatives for OOS-aware threshold selection, while keeping heldout final-only.
