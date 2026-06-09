# External Scaleout Shard - Redox Cofactor Confounded current702

Read-only targeted external scaleout over reviewed Swiss-Prot rows. The shard targets redox/cofactor-confounded failure modes rather than random candidate volume and performs no production import.

## Family-Selection Rationale

Earlier experiments showed cofactor/fold confounding and OOS false positives as central failure modes; this shard therefore targets redox oxygen/sulfur, heme, flavin, Fe-S, sulfur oxidoreductase, oxygenase, dehydrogenase, and cofactor-confounded boundary rows.

## Summary

- Candidate rows: `2681`
- Unique non-duplicate candidate rows: `2512`
- Target met (>=2,000): `True`
- Stretch met (>=4,000): `False`
- Import-ready preview rows: `743`
- OOS preserve-signal rows: `119`
- Cofactor-confounded signal rows: `1068`
- Duplicate/current/prior conflicts: `169`
- Fetch/source failure rows: `1292`
- Validation passed: `True`

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 169 |
| `coordinate_ready_pending_locator` | 103 |
| `coordinate_repair_candidate` | 18 |
| `hard_blocked_with_next_action` | 1294 |
| `import_ready_preview` | 743 |
| `locator_ready_candidate` | 214 |
| `locator_repair_candidate` | 21 |
| `reject/OOS_preserve_signal` | 119 |

## Boundary Classes Covered

| boundary class | terminal counts |
| --- | --- |
| `dehydrogenase_reductase_boundary` | `{'blocked_duplicate_or_current_registry_conflict': 26, 'hard_blocked_with_next_action': 101, 'reject/OOS_preserve_signal': 54}` |
| `fe_s_flavin_combined_system` | `{'blocked_duplicate_or_current_registry_conflict': 20, 'coordinate_ready_pending_locator': 6, 'coordinate_repair_candidate': 3, 'hard_blocked_with_next_action': 165, 'import_ready_preview': 112, 'locator_ready_candidate': 41, 'locator_repair_candidate': 4}` |
| `flavin_monooxygenase_dehydrogenase_boundary` | `{'blocked_duplicate_or_current_registry_conflict': 26, 'coordinate_ready_pending_locator': 12, 'hard_blocked_with_next_action': 254, 'import_ready_preview': 104, 'locator_ready_candidate': 39, 'locator_repair_candidate': 11, 'reject/OOS_preserve_signal': 65}` |
| `heme_peroxidase_oxidase_like` | `{'blocked_duplicate_or_current_registry_conflict': 11, 'coordinate_ready_pending_locator': 25, 'coordinate_repair_candidate': 10, 'hard_blocked_with_next_action': 272, 'import_ready_preview': 186, 'locator_ready_candidate': 60, 'locator_repair_candidate': 1}` |
| `oxygenase` | `{'blocked_duplicate_or_current_registry_conflict': 38, 'coordinate_ready_pending_locator': 9, 'coordinate_repair_candidate': 1, 'hard_blocked_with_next_action': 208, 'import_ready_preview': 170, 'locator_ready_candidate': 23, 'locator_repair_candidate': 3}` |
| `redox_oxygen_sulfur` | `{'blocked_duplicate_or_current_registry_conflict': 48, 'coordinate_ready_pending_locator': 51, 'coordinate_repair_candidate': 4, 'hard_blocked_with_next_action': 294, 'import_ready_preview': 171, 'locator_ready_candidate': 51, 'locator_repair_candidate': 2}` |

## Materialization Blockers

| bucket | count |
| --- | ---: |
| `duplicate_or_current_conflict` | 169 |
| `hard_materialization_or_source_blocker` | 1294 |
| `reaction_or_family_review_pending` | 214 |
| `reject_oos_or_confounded_signal` | 119 |
| `repairable_coordinate_blocker` | 18 |
| `repairable_locator_blocker` | 124 |
| `source_preflight_import_ready_preview` | 743 |

## Source Query Coverage

| lane | boundary role | fetched | unique queued | status |
| --- | --- | ---: | ---: | --- |
| `oxygenase_ec114_monooxygenase` | `source_candidate` | 240 | 240 | query_fetched |
| `oxygenase_ec113_dioxygenase` | `source_candidate` | 240 | 212 | query_fetched |
| `sulfur_oxidoreductase_ec18` | `source_candidate` | 240 | 237 | query_fetched |
| `heme_peroxidase_ec1111` | `source_candidate` | 240 | 233 | query_fetched |
| `heme_cytochrome_oxidase_like` | `boundary_review` | 240 | 172 | query_fetched |
| `flavin_broad_redox` | `boundary_review` | 240 | 185 | query_fetched |
| `flavin_monooxygenase_oxygen_transfer` | `source_candidate` | 240 | 179 | query_fetched |
| `flavin_dehydrogenase_reductase_oos` | `cofactor_confounded_oos_negative` | 240 | 147 | query_fetched |
| `fe_s_flavin_combined_systems` | `boundary_review` | 240 | 201 | query_fetched |
| `dehydrogenase_reductase_oos_broad` | `cofactor_confounded_oos_negative` | 240 | 181 | query_fetched |
| `oxidase_like_boundary` | `boundary_review` | 240 | 160 | query_fetched |
| `nitrogen_redox_oxygen_sulfur_boundary` | `boundary_review` | 240 | 211 | query_fetched |
| `misc_oxidoreductase_boundary` | `boundary_review` | 240 | 173 | query_fetched |
| `iron_sulfur_broad_boundary` | `boundary_review` | 240 | 150 | query_fetched |

## Candidate Matrix Sample

| candidate | lane | terminal state | locators | coordinate | cofactors | next action |
| --- | --- | --- | ---: | --- | --- | --- |
| `uniprot:Q6UVY6` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 8 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q01740` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P31513` | `oxygenase` | `import_ready_preview` | 2 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q6ZNB7` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q14534` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P49326` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P33261` | `oxygenase` | `import_ready_preview` | 1 | experimental_pdb_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:O15229` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 10 | experimental_pdb_coordinate_provenance_available | flavin | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q9Y2Z9` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q99518` | `oxygenase` | `locator_ready_candidate` | 3 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:P31512` | `oxygenase` | `import_ready_preview` | 1 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P51589` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6QHC5` | `oxygenase` | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | none | Run locator sourcing/repair from curated features or reviewed literature. |
| `uniprot:P00439` | `oxygenase` | `import_ready_preview` | 4 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P07101` | `oxygenase` | `import_ready_preview` | 8 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:O95992` | `oxygenase` | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | none | Run locator sourcing/repair from curated features or reviewed literature. |
| `uniprot:Q86W10` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P17752` | `oxygenase` | `import_ready_preview` | 9 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P19021` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 23 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P08684` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q7Z449` | `oxygenase` | `import_ready_preview` | 1 | afdb_predicted_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P09172` | `oxygenase` | `import_ready_preview` | 8 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P11712` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8IWU9` | `oxygenase` | `import_ready_preview` | 4 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P14679` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q15800` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q7RTP6` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 36 | experimental_pdb_coordinate_provenance_available | flavin | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q9Y6A2` | `oxygenase` | `import_ready_preview` | 1 | experimental_pdb_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9BU89` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P20813` | `oxygenase` | `locator_ready_candidate` | 2 | experimental_pdb_coordinate_provenance_available | heme | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:Q6ZWL3` | `oxygenase` | `import_ready_preview` | 2 | afdb_predicted_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P22680` | `oxygenase` | `import_ready_preview` | 1 | experimental_pdb_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q5TCH4` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O94851` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 14 | experimental_pdb_coordinate_provenance_available | flavin | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P11509` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8TDZ2` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q99807` | `oxygenase` | `import_ready_preview` | 9 | experimental_pdb_coordinate_provenance_available | nad_or_nadp | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P05093` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9HBI6` | `oxygenase` | `import_ready_preview` | 8 | afdb_predicted_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P75898` | `oxygenase` | `import_ready_preview` | 3 | experimental_pdb_coordinate_provenance_available | flavin | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9EQ76` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8HYJ9` | `oxygenase` | `import_ready_preview` | 2 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P36365` | `oxygenase` | `import_ready_preview` | 2 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P50285` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P97501` | `oxygenase` | `import_ready_preview` | 2 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P19099` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 2 | experimental_pdb_coordinate_provenance_available | heme | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q9SZY8` | `oxygenase` | `locator_repair_candidate` | 0 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Repair range/ambiguous locators to exact residue positions before preflight. |
| `uniprot:Q9CXI3` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9LFM5` | `oxygenase` | `locator_repair_candidate` | 0 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Repair range/ambiguous locators to exact residue positions before preflight. |
| `uniprot:Q9SVU0` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9SS04` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q08477` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q02928` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8VZ59` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A8MRX0` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q9SXE1` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q94K43` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P78329` | `oxygenase` | `import_ready_preview` | 2 | afdb_predicted_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P52020` | `oxygenase` | `import_ready_preview` | 6 | afdb_predicted_coordinate_provenance_available | flavin | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:O15528` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P52019` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P80645` | `oxygenase` | `coordinate_ready_pending_locator` | 0 | experimental_pdb_coordinate_provenance_available | none | Run locator sourcing/repair from curated features or reviewed literature. |
| `uniprot:O01404` | `oxygenase` | `import_ready_preview` | 6 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9LMA1` | `oxygenase` | `locator_ready_candidate` | 1 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:P97872` | `oxygenase` | `import_ready_preview` | 8 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q8K4C0` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q54XS1` | `oxygenase` | `import_ready_preview` | 3 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q8R1S0` | `oxygenase` | `import_ready_preview` | 1 | afdb_predicted_coordinate_provenance_available | flavin | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P11344` | `oxygenase` | `import_ready_preview` | 6 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q4QQV7` | `oxygenase` | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | none | Run locator sourcing/repair from curated features or reviewed literature. |
| `uniprot:Q91WN4` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P90925` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O88867` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P17276` | `oxygenase` | `import_ready_preview` | 4 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q8K2I3` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P24529` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q86B61` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P04177` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 8 | experimental_pdb_coordinate_provenance_available | none | Do not import; preserve as duplicate/current-registry conflict evidence. |
| `uniprot:Q564G3` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8R2F2` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P16331` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P17289` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9XTQ6` | `oxygenase` | `locator_ready_candidate` | 8 | afdb_predicted_coordinate_provenance_available | none | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:P04176` | `oxygenase` | `import_ready_preview` | 5 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9Z0F5` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P14925` | `oxygenase` | `blocked_duplicate_or_current_registry_conflict` | 24 | experimental_pdb_coordinate_provenance_available | none | Do not import; preserve as duplicate/current-registry conflict evidence. |
| `uniprot:P09810` | `oxygenase` | `import_ready_preview` | 9 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P51869` | `oxygenase` | `import_ready_preview` | 2 | afdb_predicted_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P17532` | `oxygenase` | `import_ready_preview` | 9 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P10731` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P97467` | `oxygenase` | `import_ready_preview` | 22 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P18459` | `oxygenase` | `import_ready_preview` | 3 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9CX98` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9FLC8` | `oxygenase` | `import_ready_preview` | 1 | afdb_predicted_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q64237` | `oxygenase` | `import_ready_preview` | 9 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q05754` | `oxygenase` | `import_ready_preview` | 9 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P15101` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q86BA1` | `oxygenase` | `coordinate_repair_candidate` | 19 | coordinate_provenance_missing | flavin | Find AFDB/PDB or alternate coordinate provenance for the exact locators. |
| `uniprot:P83388` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P32476` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P33274` | `oxygenase` | `import_ready_preview` | 2 | afdb_predicted_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q8CGU9` | `oxygenase` | `import_ready_preview` | 4 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9CRA4` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9VUF8` | `oxygenase` | `import_ready_preview` | 1 | afdb_predicted_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q10RE2` | `oxygenase` | `locator_repair_candidate` | 0 | afdb_predicted_coordinate_provenance_available | flavin,nad_or_nadp | Repair range/ambiguous locators to exact residue positions before preflight. |
| `uniprot:O81346` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q501D8` | `oxygenase` | `import_ready_preview` | 1 | afdb_predicted_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q6TBX7` | `oxygenase` | `import_ready_preview` | 1 | experimental_pdb_coordinate_provenance_available | heme | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:B6BQB2` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:F1MH07` | `oxygenase` | `import_ready_preview` | 18 | afdb_predicted_coordinate_provenance_available | flavin | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:F1RA39` | `oxygenase` | `import_ready_preview` | 6 | afdb_predicted_coordinate_provenance_available | flavin | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P90986` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8CJ19` | `oxygenase` | `import_ready_preview` | 32 | afdb_predicted_coordinate_provenance_available | flavin | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q8VYI1` | `oxygenase` | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | none | Run locator sourcing/repair from curated features or reviewed literature. |
| `uniprot:P38169` | `oxygenase` | `import_ready_preview` | 10 | experimental_pdb_coordinate_provenance_available | flavin | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:D3ZBP4` | `oxygenase` | `import_ready_preview` | 17 | afdb_predicted_coordinate_provenance_available | flavin | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9AST3` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P47120` | `oxygenase` | `import_ready_preview` | 12 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9SM02` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:F4JLZ6` | `oxygenase` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |

## Next Mechanical Continuation

- Run current-countable structural duplicate screens and label-factory review only on `import_ready_preview` rows; keep OOS/confounded negative rows as preserved signal unless a human family decision explicitly reverses them.
- For repair buckets, prioritize exact locator repair before coordinate download work when AFDB/PDB provenance is already present.
