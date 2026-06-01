# Predicted-Structure Fold Channel - current702

Run: 2026-06-01T03:20:54Z

Bounded manifest for a deployment-regime predicted-structure Foldseek/TM channel: AlphaFoldDB-predicted heldout rows scored against the current702 in-distribution predicted-structure atlas.

## Status

- computed_all_heldout_foldseek_scores
- Foldseek available: True
- Priority scope missing coordinate files: 173
- All-heldout scope missing coordinate files: 293
- Priority Foldseek TSV parse status: parsed
- All-heldout Foldseek TSV parse status: parsed

## Scope Counts

- Atlas in-distribution rows with ok predicted geometry: 168
- Heldout rows with ok predicted geometry: 126
- Priority cofactor-confounded OOS rows: 6

## Priority Rows

- m_csa:30
- m_csa:31
- m_csa:80
- m_csa:191
- m_csa:267
- m_csa:448

## Blockers

- The scored Foldseek TSVs below were parsed successfully; these blockers track missing persistent coordinate-file provenance for reproduction.
- predicted_coordinate_files_missing_for_priority_scope
- predicted_coordinate_files_missing_for_all_heldout_scope

## All-Heldout Fold Signal

- AUC in-scope > all OOS: 0.814301
- AUC in-scope > confounded OOS: 0.829787
- Mean in-scope: 0.687219; mean OOS: 0.519843; mean confounded: 0.5044
- Best >=90% retention diagnostic: {'threshold': 0.48, 'inscope_retain_recall': 0.9149, 'oos_abstain_recall': 0.4177, 'confounded_abstain_recall': 0.3333}
- Best >=85% retention diagnostic: {'threshold': 0.5055, 'inscope_retain_recall': 0.8511, 'oos_abstain_recall': 0.5063, 'confounded_abstain_recall': 0.5}

## Priority Parsed Hits

| Query | nearest atlas | atlas fingerprint | TM score |
| --- | --- | --- | ---: |
| m_csa:30 | m_csa:11 | metal_dependent_hydrolase | 0.4988 |
| m_csa:31 | m_csa:900 | ser_his_acid_hydrolase | 0.3809 |
| m_csa:80 | m_csa:973 | flavin_dehydrogenase_reductase | 0.5109 |
| m_csa:191 | m_csa:631 | ser_his_acid_hydrolase | 0.3863 |
| m_csa:267 | m_csa:800 | flavin_dehydrogenase_reductase | 0.7389 |
| m_csa:448 | m_csa:528 | metal_dependent_hydrolase | 0.5106 |

## Commands

Materialize the exact predicted CIF bundle:

```bash
python - <<'PY'
import json
import urllib.request
from pathlib import Path
artifact = json.loads(Path('artifacts/v3_predicted_structure_fold_channel_current702_20260601.json').read_text())
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

Run the six-row priority Foldseek/TM pass:

```bash
/private/tmp/catalytic-foldseek-env/bin/foldseek easy-search artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/queries_cofactor_confounded_oos artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/atlas_in_distribution artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/cofactor_confounded_oos_vs_atlas.tsv artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/tmp_confounded --format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits --exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 --exact-tmscore 1 --threads 4 -v 1
```

Run all heldout rows when cheap:

```bash
/private/tmp/catalytic-foldseek-env/bin/foldseek easy-search artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/queries_all_heldout artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates/atlas_in_distribution artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/all_heldout_vs_atlas.tsv artifacts/v3_predicted_structure_fold_channel_current702_20260601_coordinates_foldseek_results/tmp_all_heldout --format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits --exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 --exact-tmscore 1 --threads 4 -v 1
```

## Interpretation

- All-heldout Foldseek/TM scores were parsed from the configured result TSV; the fold channel now has a real nearest-atlas TM signal for every ok predicted-geometry heldout row.
- Use the all-heldout fold-channel signal in the next abstention combiner diagnostic, or decide whether persistent predicted-CIF coordinate provenance should be committed.
