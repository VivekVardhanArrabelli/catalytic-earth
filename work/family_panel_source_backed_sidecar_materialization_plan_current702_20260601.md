# Family Panel Source-Backed Sidecar Materialization Plan - current702

Review-only manifest for the 10 family-panel rows still missing primary predicted-geometry and predicted-fold channels after the M-CSA repair. This file stages sidecar and coordinate work only; it does not fetch coordinates, score rows, import labels, change splits, or change thresholds.

## Counts

- planned_rows: 10
- source_backed_representatives_selected: 10
- prior_identifier_resolution_rows: 7
- secondary_probe_representatives: 2
- glycoside_representatives: 1
- manifest_only_fetch_commands: 30
- rows_still_unscored: 10
- labels_or_imports_changed: 0

## Row Plan

| Rank | Entry | Representative | Accession | Structure | Priority | Next action |
|---:|---|---|---|---|---|---|
| 1 | `secondary_probe::cobalamin_radical_rearrangement` | Adenosylcobalamin-dependent ribonucleoside-triphosphate reductase (RTPR) (EC 1.17.4.2) | `uniprot:Q59490` | `1L1L` | P0 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/secondary_probe_cobalamin_radical_rearrangement_Q59490.json, fetch pdb_1L1L.cif, then score only as review-only family-panel evidence. |
| 2 | `secondary_probe::radical_sam_enzyme` | Radical SAM cyclopropyl synthase TigE (EC 4.1.-.-) (Ribosomally synthesized and post-translationally modified peptide-modifying enzyme TigE) (RiPP-modifying enzyme TigE) (TigB maturase) | `uniprot:A0A1M6T2I7` | `8VPO` | P0 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/secondary_probe_radical_sam_enzyme_A0A1M6T2I7.json, fetch pdb_8VPO.cif, then score only as review-only family-panel evidence. |
| 3 | `external_glycoside_panel` | Alpha-galactosidase MYORG | `uniprot:Q6NSJ0` | `7QQF` | P0 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/external_glycoside_panel_Q6NSJ0.json, fetch pdb_7QQF.cif and AF-Q6NSJ0 model, then score against the frozen atlas as review-only evidence. |
| 4 | `mh_073` | GTPase HRas | `uniprot:P01112` | `121P` | P1 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/mh_073.json, fetch pdb_121P.cif and AF-P01112 model if needed, then score only as review-only family-panel evidence. |
| 5 | `mh_064` | Metallo-beta-lactamase NDM-1 | `uniprot:C7C422` | `3PG4` | P1 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/mh_064.json, fetch pdb_3PG4.cif and AF-C7C422 model if needed, then score only as review-only family-panel evidence. |
| 6 | `mh_065` | Metallo-beta-lactamase VIM-like enzyme | `uniprot:Q79MP6` | `1DDK` | P1 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/mh_065.json, fetch pdb_1DDK.cif and AF-Q79MP6 model if needed, then score only as review-only family-panel evidence. |
| 7 | `mh_066` | Metallo-beta-lactamase IMP-1 | `uniprot:P52699` | `1DD6` | P1 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/mh_066.json, fetch pdb_1DD6.cif and AF-P52699 model if needed, then score only as review-only family-panel evidence. |
| 8 | `mh_067` | Carbonic anhydrase 2 | `uniprot:P00918` | `12CA` | P1 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/mh_067.json, fetch pdb_12CA.cif and AF-P00918 model if needed, then score only as review-only family-panel evidence. |
| 9 | `mh_068` | Arylsulfatase A | `uniprot:P15289` | `1AUK` | P1 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/mh_068.json, fetch pdb_1AUK.cif and AF-P15289 model if needed, then score only as review-only family-panel evidence. |
| 10 | `mh_072` | Enolase | `uniprot:P0A6P9` | `1E9I` | P1 | Create artifacts/family_panel_source_backed_sidecars_current702_20260601/mh_072.json, fetch pdb_1E9I.cif and AF-P0A6P9 model if needed, then score only as review-only family-panel evidence. |

## Guardrails

- review-only manifest; no labels, registries, ontologies, imports, splits, thresholds, model weights, or production scoring changed
- representatives were selected from frozen/current702-safe artifacts before any new scoring in this run
- external rows remain non-countable until duplicate/leakage, source-free geometry, Foldseek/TM, expert review, and future split/import gates pass
- AlphaFoldDB commands are materialization candidates only; each fetched coordinate must be hash-recorded before scoring

## Commands To Run Next

```bash
mkdir -p artifacts/family_panel_source_backed_coordinates_current702_20260601 artifacts/family_panel_source_backed_sidecars_current702_20260601
curl -L --fail https://files.rcsb.org/download/1L1L.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_1L1L.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-Q59490-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-Q59490-F1-model_v4.cif
curl -L --fail https://files.rcsb.org/download/8VPO.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_8VPO.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-A0A1M6T2I7-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-A0A1M6T2I7-F1-model_v4.cif
curl -L --fail https://files.rcsb.org/download/7QQF.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_7QQF.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-Q6NSJ0-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-Q6NSJ0-F1-model_v4.cif
curl -L --fail https://files.rcsb.org/download/121P.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_121P.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-P01112-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-P01112-F1-model_v4.cif
curl -L --fail https://files.rcsb.org/download/3PG4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_3PG4.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-C7C422-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-C7C422-F1-model_v4.cif
curl -L --fail https://files.rcsb.org/download/1DDK.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_1DDK.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-Q79MP6-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-Q79MP6-F1-model_v4.cif
curl -L --fail https://files.rcsb.org/download/1DD6.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_1DD6.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-P52699-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-P52699-F1-model_v4.cif
curl -L --fail https://files.rcsb.org/download/12CA.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_12CA.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-P00918-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-P00918-F1-model_v4.cif
curl -L --fail https://files.rcsb.org/download/1AUK.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_1AUK.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-P15289-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-P15289-F1-model_v4.cif
curl -L --fail https://files.rcsb.org/download/1E9I.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/pdb_1E9I.cif
curl -L --fail https://alphafold.ebi.ac.uk/files/AF-P0A6P9-F1-model_v4.cif -o artifacts/family_panel_source_backed_coordinates_current702_20260601/AF-P0A6P9-F1-model_v4.cif
/private/tmp/catalytic-foldseek-env/bin/foldseek easy-search artifacts/family_panel_source_backed_coordinates_current702_20260601 /private/tmp/catalytic-earth-predicted-structure-fold-channel-current702/atlas_in_distribution artifacts/v3_family_panel_source_backed_sidecar_materialization_current702_20260601_foldseek.tsv /private/tmp/catalytic-earth-family-panel-sidecar-materialization-current702 --format-output query,target,qtmscore,ttmscore,alntmscore,prob,bits --exhaustive-search 1 --alignment-type 1 --tmalign-fast 0 --exact-tmscore 1 --threads 4 -v 1
PYTHONPATH=src python -m catalytic_earth.cli build-fold-augmented-family-panel-research-readout
PYTHONPATH=src python -m catalytic_earth.cli build-fold-augmented-family-panel-missing-primary-channel-queue
```

## Validation Plan

- Validate this JSON with python -m json.tool.
- Before fetching, confirm disk remains above 10 GiB.
- After fetching, record sha256 for every coordinate and sidecar.
- Run Foldseek/TM only against the frozen in-distribution atlas directory used by v3_predicted_structure_fold_channel_current702_20260601.
- Rerun only review-only family-panel packets/readout/queues; do not mutate production artifacts.

## Source Artifacts

| Artifact | SHA256 | Role |
|---|---|---|
| `artifacts/v3_fold_augmented_family_panel_missing_primary_channel_queue_current702_20260601.json` | `61470de4460ae204e76bc235211f802719139d0fe7cf6a5ace15ddf11ef3359c` | current 10-row missing primary-channel queue |
| `artifacts/v3_fold_augmented_family_panel_missing_primary_channel_diagnosis_current702_20260601.json` | `a28fc9f5d4f06b8a5b64cf47db3f2cf81606f440fb13ca99f98b79ca6ffc8d59` | diagnosis confirming sidecar/coordinate materialization is the remaining blocker |
| `artifacts/v3_external_identifier_resolution_scout_20260528.json` | `0ccf352e3d5d8d1d6bfe786673a626fc0caf811806fe40de48c0291b7f9f30d2` | prior external identifier resolution for metal-hydrolase rows |
| `artifacts/v3_external_materialization_fetch_pack_20260528.json` | `92e026eaec814131185ab8b536ea9dbac7bbe179a1fa0111f0090e4ff7d30632` | prior fetch manifest for first materialization tranche |
| `artifacts/v3_targeted_bin_expansion_proposal_current702_20260530.json` | `0706b0258d61e06601568f0f3efe1133bfbc724ec73cccaf06d5ebd3790d374d` | current702-safe targeted expansion proposal |
| `artifacts/v3_external_glycoside_carbohydrate_panel_20260528.json` | `5fd73c1a47a68047433476e5b04ffd94062117d8710139b8616e8ac38872e20a` | source-backed glycoside representative surface |
| `artifacts/v3_prospective_external_cobalamin_radical_minicampaign_blocker_review_20260521.json` | `52dad94795c92f4d8a0922fd90588e7c908d3ae21f0ab96ac6ba79c34b168406` | cobalamin radical source blocker and eligible representative |
| `artifacts/v3_prospective_external_radical_sam_minicampaign_freeze_20260521.json` | `e5b2686dba305b74e765ae0fe1300fb9cd1ea715903ac7001ee780c9cbe0448c` | frozen radical-SAM source candidates before scoring |
| `artifacts/v3_prospective_external_radical_sam_minicampaign_decision_packet_20260521.json` | `03569b6b26f1e3652caffd95b0ed634fd29f838ff4f7d5108a3b9de47280d1d3` | radical-SAM terminal review status and sequence-neighbor context |

## Exact Next Action

Materialize the two P0 secondary probes and external_glycoside_panel sidecars/coordinates first, record coordinate hashes, then run Foldseek/TM against the frozen atlas and refresh the review-only family-panel readout.
