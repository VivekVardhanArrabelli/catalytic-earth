# External Scaleout Shard - Near-Orphan Diversity current702

Read-only targeted external scaleout over reviewed Swiss-Prot rows. The shard targets sparse, no-reliable-structure, OOS, fold-confounded, and diverse mechanism rows instead of nearest-neighbor expansion.

## Family-Selection Rationale

Dense structural neighborhoods cannot prove the atlas north star. This shard therefore targets reviewed sparse-family, near-orphan, no-reliable-structure, OOS hard-negative, fold-confounded, cofactor-confounded non-target, terpene, lyase, isomerase, transferase, and ligase/synthetase rows that force abstention or explicit family review rather than nearest-neighbor transfer.

## Summary

- Candidate rows: `3022`
- Unique non-duplicate candidate rows: `2821`
- Target met (>=2,000): `True`
- Stretch met: `False`
- Import-ready preview rows: `142`
- Provisional rows: `7`
- Repair/materialization candidate rows: `156`
- Reject/OOS preserve-signal rows: `319`
- Near-orphan signal rows: `637`
- No-structure/no-reliable-structure rows: `204`
- OOS/fold/cofactor hard-negative rows: `1306`
- Duplicate/current/prior conflicts: `201`
- Fetch/source failure rows: `2196`
- Validation passed: `True`

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 201 |
| `coordinate_ready_pending_locator` | 99 |
| `coordinate_repair_candidate` | 5 |
| `hard_blocked_with_next_action` | 2197 |
| `import_ready_preview` | 142 |
| `locator_ready_candidate` | 50 |
| `locator_repair_candidate` | 2 |
| `provisional_external_countable_preflight_candidate` | 7 |
| `reject/OOS_preserve_signal` | 319 |

## Diversity Bins

| diversity bin | terminal counts |
| --- | --- |
| `carbon_carbon_lyase_decarboxylase` | `{'blocked_duplicate_or_current_registry_conflict': 35, 'coordinate_ready_pending_locator': 1, 'hard_blocked_with_next_action': 168, 'import_ready_preview': 12}` |
| `cofactor_confounded_non_target` | `{'blocked_duplicate_or_current_registry_conflict': 30, 'hard_blocked_with_next_action': 151, 'reject/OOS_preserve_signal': 31}` |
| `diverse_lyase_hydratase` | `{'blocked_duplicate_or_current_registry_conflict': 17, 'coordinate_ready_pending_locator': 6, 'coordinate_repair_candidate': 1, 'hard_blocked_with_next_action': 142, 'import_ready_preview': 42, 'locator_ready_candidate': 1}` |
| `fold_confounded_hydrolase_like` | `{'blocked_duplicate_or_current_registry_conflict': 7, 'hard_blocked_with_next_action': 147, 'reject/OOS_preserve_signal': 65}` |
| `fold_confounded_metal_nonhydrolase` | `{'blocked_duplicate_or_current_registry_conflict': 5, 'hard_blocked_with_next_action': 150, 'reject/OOS_preserve_signal': 64}` |
| `fold_confounded_protease_boundary` | `{'blocked_duplicate_or_current_registry_conflict': 8, 'hard_blocked_with_next_action': 155, 'reject/OOS_preserve_signal': 54}` |
| `isomerase_transferase_tail` | `{'blocked_duplicate_or_current_registry_conflict': 62, 'coordinate_ready_pending_locator': 4, 'hard_blocked_with_next_action': 324, 'import_ready_preview': 39, 'locator_ready_candidate': 7}` |
| `ligase_synthetase_oos` | `{'hard_blocked_with_next_action': 163, 'reject/OOS_preserve_signal': 56}` |
| `near_orphan_low_annotation` | `{'blocked_duplicate_or_current_registry_conflict': 4, 'coordinate_ready_pending_locator': 35, 'hard_blocked_with_next_action': 172, 'locator_ready_candidate': 7}` |
| `near_orphan_uncharacterized` | `{'blocked_duplicate_or_current_registry_conflict': 27, 'coordinate_ready_pending_locator': 18, 'hard_blocked_with_next_action': 160, 'locator_ready_candidate': 15}` |
| `no_reliable_structure_tail` | `{'blocked_duplicate_or_current_registry_conflict': 1, 'coordinate_ready_pending_locator': 33, 'hard_blocked_with_next_action': 140, 'locator_ready_candidate': 16, 'locator_repair_candidate': 2, 'provisional_external_countable_preflight_candidate': 7}` |
| `terpene_lyase` | `{'blocked_duplicate_or_current_registry_conflict': 4, 'coordinate_ready_pending_locator': 2, 'coordinate_repair_candidate': 4, 'hard_blocked_with_next_action': 155, 'import_ready_preview': 49, 'locator_ready_candidate': 4}` |
| `transport_atpase_oos` | `{'blocked_duplicate_or_current_registry_conflict': 1, 'hard_blocked_with_next_action': 170, 'reject/OOS_preserve_signal': 49}` |

## Materialization And Provenance Blockers

| bucket | count |
| --- | ---: |
| `duplicate_or_current_conflict` | 201 |
| `hard_materialization_or_source_blocker` | 2197 |
| `reaction_or_family_review_pending` | 50 |
| `reject_oos_or_confounded_signal` | 319 |
| `repairable_coordinate_blocker` | 5 |
| `repairable_locator_blocker` | 101 |
| `source_preflight_import_ready_preview` | 142 |
| `source_preflight_provisional` | 7 |

## Source Query Coverage

| lane | diversity bin | boundary role | fetched | unique queued | status |
| --- | --- | --- | ---: | ---: | --- |
| `near_orphan_uncharacterized_reviewed` | `near_orphan_uncharacterized` | `near_orphan_source_candidate` | 220 | 220 | query_fetched |
| `near_orphan_low_annotation_reviewed` | `near_orphan_low_annotation` | `near_orphan_source_candidate` | 220 | 218 | query_fetched |
| `terpene_synthase_lyase` | `terpene_lyase` | `sparse_family_source_candidate` | 220 | 218 | query_fetched |
| `isomerase_racemase_epimerase_mutase` | `isomerase_transferase_tail` | `sparse_family_source_candidate` | 220 | 216 | query_fetched |
| `glycosyl_methyl_transferase_tail` | `isomerase_transferase_tail` | `sparse_family_source_candidate` | 220 | 220 | query_fetched |
| `carbon_carbon_lyase_decarboxylase` | `carbon_carbon_lyase_decarboxylase` | `sparse_family_source_candidate` | 220 | 216 | query_fetched |
| `dehydratase_hydratase_lyase` | `diverse_lyase_hydratase` | `sparse_family_source_candidate` | 220 | 209 | query_fetched |
| `ligase_synthetase_oos_abstention` | `ligase_synthetase_oos` | `oos_hard_negative` | 220 | 219 | query_fetched |
| `transport_atpase_oos_hard_negative` | `transport_atpase_oos` | `oos_hard_negative` | 220 | 220 | query_fetched |
| `hydrolase_fold_confounded_negative` | `fold_confounded_hydrolase_like` | `fold_confounded_hard_negative` | 220 | 219 | query_fetched |
| `metalloprotein_nonhydrolase_fold_confounded` | `fold_confounded_metal_nonhydrolase` | `fold_confounded_hard_negative` | 220 | 219 | query_fetched |
| `plp_non_target_cofactor_confounded` | `cofactor_confounded_non_target` | `cofactor_confounded_non_target_enzyme` | 220 | 155 | query_fetched |
| `sam_methyltransferase_nonradical_confounded` | `cofactor_confounded_non_target` | `cofactor_confounded_non_target_enzyme` | 220 | 57 | query_fetched |
| `cysteine_aspartic_metallo_protease_boundary` | `fold_confounded_protease_boundary` | `fold_confounded_hard_negative` | 220 | 217 | query_fetched |
| `no_reliable_structure_reviewed_enzyme_tail` | `no_reliable_structure_tail` | `no_reliable_structure_source_candidate` | 220 | 199 | query_fetched |

## Candidate Matrix Sample

| candidate | bin | terminal state | locators | coordinate | groups | next action |
| --- | --- | --- | ---: | --- | --- | --- |
| `uniprot:Q6P1W5` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q6ZU52` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q96LL4` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9NWQ9` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q6NUJ2` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6ZRI6` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 12 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q8IYJ2` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P0CG20` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q7Z695` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6ZUT1` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q94EH2` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q8NCU1` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q66K80` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P0C264` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9SCK3` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9FLT9` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P38922` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 4 | experimental_pdb_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P43610` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q8BM15` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:A8MRY9` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A0A7J6K629` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8QL26` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O13799` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O42976` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q5JRM2` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O13658` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6UWT4` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q8TB03` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9BV19` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9H6X5` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 2 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q8N8K9` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 6 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q96GX8` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q96F05` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6UXA7` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8WYQ4` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q5SRN2` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O94854` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 10 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q8GUH7` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | experimental_pdb_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q8N1D0` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P64581` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9W5D0` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 5 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P47137` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 3 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q12185` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | transferase | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:O14468` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q22836` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q08157` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P31058` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P0AFQ7` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P37621` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P40169` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P39983` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q12232` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6NSR3` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P38114` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q06417` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P40092` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q3UK37` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q69ZZ9` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A0A7J6KE60` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:B1MDC3` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 1 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:P16833` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O13968` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O74388` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 2 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:O43013` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 1 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:Q10324` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9P6L9` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O42869` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9UT00` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9UT12` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O14355` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q10332` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9USP9` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O94387` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:O13686` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q53FE4` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q5JPI3` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8IYS2` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8N0U7` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8N9M1` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8NEA5` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q96HA4` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9BY89` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9H972` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A1L168` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6P387` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6ZUJ4` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O60268` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q5SNV9` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q5T681` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8WW18` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9H425` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6ICG6` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8IV33` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q5SZD1` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q5VZ46` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8ND61` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A8K5M9` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q6ZVT6` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q49A92` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8N0U6` | `near_orphan_uncharacterized` | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | none | Do not import; preserve as duplicate/current conflict against prior external admission or scaleout artifacts. |
| `uniprot:D6RIA3` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q3MIX3` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8TAV5` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q8N2X6` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q86SI9` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:A1A4F0` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O43423` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q9XRX5` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O07617` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:O34948` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P0ADQ7` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P35719` | `near_orphan_uncharacterized` | `locator_ready_candidate` | 2 | afdb_predicted_coordinate_provenance_available | none | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:P38765` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P39523` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P47086` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P53918` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P54453` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:Q06537` | `near_orphan_uncharacterized` | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | none | Keep as near-orphan coordinate-ready row; find residue-level evidence before review. |
| `uniprot:Q9C8Z4` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |
| `uniprot:P36083` | `near_orphan_uncharacterized` | `hard_blocked_with_next_action` | 0 | entry_retrieval_failed_before_coordinate_check | none | Retry UniProt entry materialization for this accession before any locator, coordinate, or import review. |

## Blockers

- `source_preflight_provisional`: family-policy and structural duplicate review required before import-ready promotion.
- `repairable_locator_blocker`: exact residue locator or reaction/locator repair required before review.
- `repairable_coordinate_blocker`: AFDB/PDB coordinate provenance missing for otherwise useful locator evidence.
- `hard_materialization_or_source_blocker`: source entry retrieval, coordinate provenance, or no-reliable-structure policy is unresolved.
- `reject_oos_or_confounded_signal`: preserved hard-negative signal only.

## Next Mechanical Continuation

- Run current-countable structural duplicate screens and label-factory review only on `import_ready_preview` rows.
- For provisional near-orphan/no-reliable-structure rows, decide the family policy before any import-ready promotion.
- Retry UniProt entry materialization for hard-blocked rows before treating them as terminal no-structure evidence.
