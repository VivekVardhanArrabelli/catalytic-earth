# External Scaleout Shard - Metal Phosphoryl Glycoside current702

Read-only targeted external scaleout over reviewed Swiss-Prot rows. The shard targets metal, phosphoryl-transfer, glycoside/nucleoside, and confounded-control failure modes rather than random candidate volume and performs no production import.

## Family-Selection Rationale

Earlier experiments showed predicted-geometry recovery, source-free active-site materialization, fold/cofactor confounding, and countable-admission routing as central scaleout risks. This shard therefore targets metal hydrolase subfamilies, phosphatases, kinases, phosphotransferases, phosphodiesterases, glycoside/nucleoside hydrolases, glycosyltransferases, and explicit ATPase/GTPase, glycan-binding, and metal-transport OOS controls.

## Summary

- Candidate rows: `4423`
- Unique non-duplicate candidate rows: `4060`
- Target met (>=2,000): `True`
- Stretch met (>=4,000): `True`
- Import-ready preview rows: `1049`
- OOS preserve-signal rows: `656`
- Active-site/ligand-confounded signal rows: `2102`
- Duplicate/current/prior conflicts: `363`
- Fetch/source failure rows: `1670`
- Validation passed: `True`

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 363 |
| `coordinate_ready_pending_locator` | 170 |
| `coordinate_repair_candidate` | 5 |
| `hard_blocked_with_next_action` | 1675 |
| `import_ready_preview` | 1049 |
| `locator_ready_candidate` | 500 |
| `locator_repair_candidate` | 5 |
| `reject/OOS_preserve_signal` | 656 |

## Boundary Classes Covered

| boundary class | terminal counts |
| --- | --- |
| `glycan_binding_oos_boundary` | `{'blocked_duplicate_or_current_registry_conflict': 3, 'hard_blocked_with_next_action': 82, 'reject/OOS_preserve_signal': 222}` |
| `glycoside_nucleoside_bond_cleavage` | `{'blocked_duplicate_or_current_registry_conflict': 73, 'coordinate_ready_pending_locator': 25, 'coordinate_repair_candidate': 1, 'hard_blocked_with_next_action': 180, 'import_ready_preview': 181, 'locator_ready_candidate': 143}` |
| `glycosyltransferase` | `{'blocked_duplicate_or_current_registry_conflict': 77, 'coordinate_ready_pending_locator': 50, 'coordinate_repair_candidate': 2, 'hard_blocked_with_next_action': 89, 'import_ready_preview': 74, 'locator_ready_candidate': 9}` |
| `metal_binding_transport_oos_boundary` | `{'hard_blocked_with_next_action': 73, 'reject/OOS_preserve_signal': 218}` |
| `metal_hydrolase_subfamily` | `{'blocked_duplicate_or_current_registry_conflict': 44, 'coordinate_ready_pending_locator': 32, 'coordinate_repair_candidate': 2, 'hard_blocked_with_next_action': 750, 'import_ready_preview': 172, 'locator_ready_candidate': 175, 'locator_repair_candidate': 3}` |
| `nucleotide_hydrolysis_fold_confounded_oos` | `{'blocked_duplicate_or_current_registry_conflict': 4, 'hard_blocked_with_next_action': 88, 'reject/OOS_preserve_signal': 216}` |
| `nucleotidyltransferase_polymerase_boundary` | `{'blocked_duplicate_or_current_registry_conflict': 18, 'coordinate_ready_pending_locator': 30, 'hard_blocked_with_next_action': 92, 'import_ready_preview': 97, 'locator_ready_candidate': 68, 'locator_repair_candidate': 1}` |
| `phosphodiesterase_nuclease_boundary` | `{'blocked_duplicate_or_current_registry_conflict': 8, 'coordinate_ready_pending_locator': 15, 'hard_blocked_with_next_action': 83, 'import_ready_preview': 148, 'locator_ready_candidate': 62, 'locator_repair_candidate': 1}` |
| `phosphoryl_hydrolysis_transfer` | `{'blocked_duplicate_or_current_registry_conflict': 19, 'coordinate_ready_pending_locator': 11, 'hard_blocked_with_next_action': 97, 'import_ready_preview': 152, 'locator_ready_candidate': 41}` |
| `phosphoryl_transfer_kinase` | `{'blocked_duplicate_or_current_registry_conflict': 117, 'coordinate_ready_pending_locator': 7, 'hard_blocked_with_next_action': 141, 'import_ready_preview': 225, 'locator_ready_candidate': 2}` |

## Materialization Blockers

| bucket | count |
| --- | ---: |
| `duplicate_or_current_conflict` | 363 |
| `hard_materialization_or_source_blocker` | 1675 |
| `reaction_or_family_review_pending` | 500 |
| `reject_oos_or_confounded_signal` | 656 |
| `repairable_coordinate_blocker` | 5 |
| `repairable_locator_blocker` | 175 |
| `source_preflight_import_ready_preview` | 1049 |

## Source Query Coverage

| lane | boundary role | fetched | unique queued | status |
| --- | --- | ---: | ---: | --- |
| `metal_hydrolase_metallo_beta_lactamase` | `source_candidate` | 320 | 314 | query_fetched |
| `metal_hydrolase_zinc_metalloprotease` | `source_candidate` | 320 | 320 | query_fetched |
| `metal_hydrolase_amino_carboxypeptidase` | `source_candidate` | 320 | 317 | query_fetched |
| `metal_hydrolase_carbonic_anhydrase_lactonase` | `source_candidate` | 302 | 227 | query_fetched |
| `phosphatase_phosphomonoesterase` | `source_candidate` | 320 | 320 | query_fetched |
| `phosphodiesterase_nuclease_boundary` | `source_candidate` | 320 | 317 | query_fetched |
| `protein_kinase_phosphotransfer` | `source_candidate` | 320 | 320 | query_fetched |
| `small_molecule_phosphotransferase` | `source_candidate` | 320 | 172 | query_fetched |
| `nucleotidyltransferase_polymerase_boundary` | `boundary_review` | 320 | 306 | query_fetched |
| `glycoside_hydrolase` | `source_candidate` | 320 | 314 | query_fetched |
| `glycosyltransferase` | `source_candidate` | 320 | 301 | query_fetched |
| `nucleosidase_nucleotide_glycosidic_bond` | `source_candidate` | 320 | 289 | query_fetched |
| `p_loop_atpase_gtpase_oos` | `fold_cofactor_confounded_oos_negative` | 320 | 308 | query_fetched |
| `lectin_carbohydrate_binding_oos` | `binding_or_transport_oos_negative` | 320 | 307 | query_fetched |
| `metal_nucleotide_transport_oos` | `binding_or_transport_oos_negative` | 320 | 291 | query_fetched |

## Candidate Matrix Sample

| candidate | lane | terminal state | locators | coordinate | ligand groups | next action |
| --- | --- | --- | ---: | --- | --- | --- |
| `uniprot:P26918` | `metal_hydrolase_subfamily` | `blocked_duplicate_or_current_registry_conflict` | 7 | experimental_pdb_coordinate_provenance_available | zinc | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:A4D2B0` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:C7C422` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q7WYA8` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P52700` | `metal_hydrolase_subfamily` | `blocked_duplicate_or_current_registry_conflict` | 7 | experimental_pdb_coordinate_provenance_available | zinc | Do not import; preserve as duplicate/current-registry conflict evidence. |
| `uniprot:Q68D91` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P14488` | `metal_hydrolase_subfamily` | `blocked_duplicate_or_current_registry_conflict` | 8 | experimental_pdb_coordinate_provenance_available | zinc | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P04190` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P52699` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A0A0F7KYQ8` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q840P9` | `metal_hydrolase_subfamily` | `blocked_duplicate_or_current_registry_conflict` | 6 | experimental_pdb_coordinate_provenance_available | zinc | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:O08498` | `metal_hydrolase_subfamily` | `blocked_duplicate_or_current_registry_conflict` | 7 | experimental_pdb_coordinate_provenance_available | zinc | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P25910` | `metal_hydrolase_subfamily` | `blocked_duplicate_or_current_registry_conflict` | 8 | experimental_pdb_coordinate_provenance_available | zinc | Do not import; preserve as duplicate/current-registry conflict evidence. |
| `uniprot:Q5U7L7` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9X482` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q5B0C9` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P10425` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P27708` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q14117` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6PJP8` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9H816` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P16444` | `metal_hydrolase_subfamily` | `blocked_duplicate_or_current_registry_conflict` | 8 | experimental_pdb_coordinate_provenance_available | calcium,zinc | Do not import; preserve as duplicate/current-registry conflict evidence. |
| `uniprot:A5PJT0` | `metal_hydrolase_subfamily` | `import_ready_preview` | 8 | afdb_predicted_coordinate_provenance_available | zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q8BL86` | `metal_hydrolase_subfamily` | `import_ready_preview` | 8 | afdb_predicted_coordinate_provenance_available | zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q5F336` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P20054` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P31430` | `metal_hydrolase_subfamily` | `import_ready_preview` | 8 | afdb_predicted_coordinate_provenance_available | calcium,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q18990` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q46806` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8C7W7` | `metal_hydrolase_subfamily` | `import_ready_preview` | 1 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9CRB3` | `metal_hydrolase_subfamily` | `import_ready_preview` | 3 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9FMP3` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9LVM5` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P05990` | `metal_hydrolase_subfamily` | `import_ready_preview` | 73 | afdb_predicted_coordinate_provenance_available | calcium,magnesium,manganese,phosphoryl_or_nucleotide,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P77671` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q63150` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9JIC3` | `metal_hydrolase_subfamily` | `import_ready_preview` | 10 | afdb_predicted_coordinate_provenance_available | phosphoryl_or_nucleotide,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:B2RQC6` | `metal_hydrolase_subfamily` | `import_ready_preview` | 79 | afdb_predicted_coordinate_provenance_available | calcium,magnesium,manganese,phosphoryl_or_nucleotide,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:O32142` | `metal_hydrolase_subfamily` | `import_ready_preview` | 3 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P00811` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P05020` | `metal_hydrolase_subfamily` | `blocked_duplicate_or_current_registry_conflict` | 13 | experimental_pdb_coordinate_provenance_available | calcium,zinc | Do not import; preserve as duplicate/current-registry conflict evidence. |
| `uniprot:Q3SZM7` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q55DL0` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9EQF5` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P0AEB2` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P28273` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P31428` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P76341` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q4KLY6` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q94AP0` | `metal_hydrolase_subfamily` | `import_ready_preview` | 7 | afdb_predicted_coordinate_provenance_available | calcium,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P05364` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P14489` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P22412` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P37321` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P62593` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P71420` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P71778` | `metal_hydrolase_subfamily` | `import_ready_preview` | 1 | afdb_predicted_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q09HD0` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q45515` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q4VYA5` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A8IKD2` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O66990` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P05193` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P0AD64` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P28585` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P83772` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P9WGZ9` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P9WKD3` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q2TR58` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6XEC0` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8S3J3` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A0NLY7` | `metal_hydrolase_subfamily` | `import_ready_preview` | 5 | experimental_pdb_coordinate_provenance_available | manganese | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:O25001` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O87489` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P52682` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q48434` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8RSQ2` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9F663` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9RMT4` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A0A649V088` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A6T7D6` | `metal_hydrolase_subfamily` | `import_ready_preview` | 13 | afdb_predicted_coordinate_provenance_available | calcium,magnesium,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P08955` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P31429` | `metal_hydrolase_subfamily` | `import_ready_preview` | 8 | afdb_predicted_coordinate_provenance_available | calcium,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:P43477` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q0QLE9` | `metal_hydrolase_subfamily` | `import_ready_preview` | 7 | experimental_pdb_coordinate_provenance_available | calcium,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q5YXD6` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8KSA6` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q91437` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9KJY7` | `metal_hydrolase_subfamily` | `import_ready_preview` | 5 | experimental_pdb_coordinate_provenance_available | none | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9L4P2` | `metal_hydrolase_subfamily` | `import_ready_preview` | 8 | experimental_pdb_coordinate_provenance_available | calcium | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9P903` | `metal_hydrolase_subfamily` | `import_ready_preview` | 10 | experimental_pdb_coordinate_provenance_available | calcium,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:A0A5R8T042` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P13661` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P58329` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P81006` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q81WF0` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q93F76` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q96NU7` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O14841` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9XBN7` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9KJA8` | `metal_hydrolase_subfamily` | `import_ready_preview` | 7 | afdb_predicted_coordinate_provenance_available | zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9KJA9` | `metal_hydrolase_subfamily` | `import_ready_preview` | 7 | afdb_predicted_coordinate_provenance_available | zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9K303` | `metal_hydrolase_subfamily` | `import_ready_preview` | 7 | afdb_predicted_coordinate_provenance_available | zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9KJA7` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9KJB0` | `metal_hydrolase_subfamily` | `import_ready_preview` | 7 | afdb_predicted_coordinate_provenance_available | zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9RB01` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6AYD1` | `metal_hydrolase_subfamily` | `locator_ready_candidate` | 7 | afdb_predicted_coordinate_provenance_available | zinc | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:Q8BWY4` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q2HJB0` | `metal_hydrolase_subfamily` | `locator_ready_candidate` | 7 | afdb_predicted_coordinate_provenance_available | zinc | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:B0V2S2` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q18677` | `metal_hydrolase_subfamily` | `import_ready_preview` | 10 | afdb_predicted_coordinate_provenance_available | calcium,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q21773` | `metal_hydrolase_subfamily` | `import_ready_preview` | 10 | afdb_predicted_coordinate_provenance_available | calcium,zinc | Stage in import-ready preview only; still requires current-countable structural duplicate screening, label-factory review, and explicit production authorization before any import. |
| `uniprot:Q9FIZ7` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O32137` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q75WB5` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P20051` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P60495` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q06S87` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q7WY77` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P42084` | `metal_hydrolase_subfamily` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |

## Next Mechanical Continuation

- Run current-countable structural duplicate screens and label-factory review only on `import_ready_preview` rows; keep ATPase/GTPase, glycan-binding, transporter, and other OOS/confounded control rows as preserved signal unless a human family decision explicitly reverses them.
- For repair buckets, prioritize exact locator repair before coordinate download work when AFDB/PDB provenance is already present.
