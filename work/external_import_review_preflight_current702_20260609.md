# External Import Review Preflight - current702

Controlled import-review preflight over the Wave 2 external materialization review surface: the carried-forward import-ready preview rows plus the expanded repair queue. No production registry, import file, ontology, split, threshold, or model artifact was edited.

## Summary

- Preview rows: 600
- Repair-surface rows: 11895
- Total review-surface rows: 12495
- Controlled import-review ready rows: 275
- Repair/conflict queue rows: 12220
- Final human batch approval: A final controlled human batch approval could cover 275 machine-clean rows at once rather than row-by-row; production registry authorization and label-factory gates remain outside this preflight.
- Production import authorized here: False

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `controlled_import_review_ready` | 275 |
| `needs_structural_duplicate_screen` | 1 |
| `needs_family_policy_review` | 0 |
| `repairable_locator_blocker` | 1096 |
| `repairable_coordinate_blocker` | 5179 |
| `duplicate_current702_conflict` | 203 |
| `duplicate_external_conflict` | 1275 |
| `reject/OOS_preserve_signal` | 1562 |
| `hard_blocked_with_next_action` | 2904 |

## Review Scope Counts

| scope | count |
| --- | ---: |
| `import_ready_preview` | 600 |
| `materialization_repair_surface` | 11895 |

## Lane Counts

| lane | count |
| --- | ---: |
| ATPase/transporter OOS hard negative | 158 |
| B12 adenosylcobalamin enzymes | 25 |
| B12/cobalamin broad enzymes | 87 |
| FMO/flavin monooxygenase boundary | 98 |
| Fe-S/flavin combined boundary | 104 |
| Fe-S/flavin combined systems | 226 |
| PLP aminotransferase | 60 |
| PLP broad cofactor context | 116 |
| PLP children | 102 |
| PLP cofactor-confounded non-target | 15 |
| PLP decarboxylase | 80 |
| PLP lyase/eliminase | 111 |
| PLP lyase/racemase boundary | 63 |
| PLP racemase/epimerase | 113 |
| PLP sulfur lyase boundary | 112 |
| Rossmann/NAD fold-confounded controls | 63 |
| SAM methyltransferase non-radical control | 56 |
| SAM-dependent radical-like boundary | 3 |
| adjacent SAM methyltransferase negative | 55 |
| adjacent high-yield amidase/deaminase | 12 |
| adjacent high-yield lyase/isomerase | 14 |
| adjacent methylcobalamin negative | 61 |
| adjacent non-PLP decarboxylase negative | 93 |
| amidase/deaminase controls | 189 |
| carbon-carbon lyase/decarboxylase | 75 |
| cobalamin radical rearrangement | 56 |
| cobalamin/B12 radical enzymes | 72 |
| coupled PLP adenosylcobalamin aminomutase | 116 |
| dehydratase/hydratase lyase | 134 |
| dehydrogenase/reductase OOS boundary | 25 |
| dehydrogenase/reductase OOS controls | 172 |
| flavin dehydrogenase boundary | 139 |
| flavin dehydrogenase/reductase boundary | 2 |
| flavin monooxygenase | 94 |
| flavin redox boundary | 142 |
| glycoside hydrolase | 179 |
| glycoside/fold-confounded OOS controls | 294 |
| glycoside/nucleoside | 554 |
| glycosyltransferase boundary | 204 |
| heme peroxidase/oxidase boundary | 111 |
| heme peroxidase/oxidase-like | 459 |
| hydrolase-like fold-confounded negative | 181 |
| isomerase controls | 153 |
| isomerase/racemase/epimerase | 54 |
| kinase/phosphotransferase | 272 |
| ligase/synthetase abstention probe | 210 |
| lyase controls | 119 |
| metal hydrolase | 1185 |
| metal hydrolase Mg/Mn controls | 205 |
| metal hydrolase amidase/peptidase boundary | 220 |
| metal-cofactor non-target enzyme | 203 |
| metal/fold-confounded OOS controls | 288 |
| near-orphan reviewed proteins | 119 |
| near-orphan/no-reliable-structure | 350 |
| no reliable structure pressure | 236 |
| no-reliable-structure enzyme tail | 199 |
| non-serine protease OOS boundary | 145 |
| nucleoside/nucleotide hydrolase boundary | 161 |
| nucleotide phosphoryl-transfer boundary | 215 |
| oxygenase redox | 105 |
| phosphatase/phosphoryl hydrolase | 199 |
| phosphoryl transfer | 113 |
| phosphoryl transfer kinase-like | 128 |
| phosphoryl transfer/phosphatase | 608 |
| phosphoryl/fold-confounded OOS controls | 253 |
| radical SAM | 22 |
| radical SAM iron-sulfur | 210 |
| radical SAM named families | 120 |
| radical-SAM/cobalamin | 99 |
| redox oxygen/sulfur | 810 |
| sulfur oxidoreductase | 182 |
| terpene synthase/lyase | 208 |
| transferase tail outside current fingerprints | 79 |

## Lane Terminal Counts

| lane | terminal counts |
| --- | --- |
| ATPase/transporter OOS hard negative | `{'hard_blocked_with_next_action': 110, 'reject/OOS_preserve_signal': 48}` |
| B12 adenosylcobalamin enzymes | `{'repairable_coordinate_blocker': 25}` |
| B12/cobalamin broad enzymes | `{'duplicate_current702_conflict': 3, 'repairable_coordinate_blocker': 71, 'repairable_locator_blocker': 13}` |
| FMO/flavin monooxygenase boundary | `{'duplicate_current702_conflict': 1, 'duplicate_external_conflict': 87, 'repairable_coordinate_blocker': 4, 'repairable_locator_blocker': 6}` |
| Fe-S/flavin combined boundary | `{'duplicate_current702_conflict': 6, 'duplicate_external_conflict': 89, 'repairable_coordinate_blocker': 9}` |
| Fe-S/flavin combined systems | `{'duplicate_current702_conflict': 5, 'duplicate_external_conflict': 3, 'hard_blocked_with_next_action': 54, 'needs_structural_duplicate_screen': 1, 'repairable_coordinate_blocker': 153, 'repairable_locator_blocker': 10}` |
| PLP aminotransferase | `{'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 6, 'repairable_coordinate_blocker': 52}` |
| PLP broad cofactor context | `{'duplicate_current702_conflict': 7, 'duplicate_external_conflict': 6, 'repairable_coordinate_blocker': 102, 'repairable_locator_blocker': 1}` |
| PLP children | `{'controlled_import_review_ready': 6, 'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 3, 'repairable_coordinate_blocker': 2, 'repairable_locator_blocker': 89}` |
| PLP cofactor-confounded non-target | `{'duplicate_external_conflict': 1, 'hard_blocked_with_next_action': 9, 'reject/OOS_preserve_signal': 5}` |
| PLP decarboxylase | `{'duplicate_current702_conflict': 2, 'repairable_coordinate_blocker': 78}` |
| PLP lyase/eliminase | `{'duplicate_current702_conflict': 8, 'duplicate_external_conflict': 2, 'repairable_coordinate_blocker': 99, 'repairable_locator_blocker': 2}` |
| PLP lyase/racemase boundary | `{'repairable_coordinate_blocker': 63}` |
| PLP racemase/epimerase | `{'duplicate_current702_conflict': 1, 'hard_blocked_with_next_action': 1, 'repairable_coordinate_blocker': 111}` |
| PLP sulfur lyase boundary | `{'duplicate_current702_conflict': 1, 'repairable_coordinate_blocker': 108, 'repairable_locator_blocker': 3}` |
| Rossmann/NAD fold-confounded controls | `{'reject/OOS_preserve_signal': 63}` |
| SAM methyltransferase non-radical control | `{'duplicate_external_conflict': 1, 'hard_blocked_with_next_action': 37, 'reject/OOS_preserve_signal': 18}` |
| SAM-dependent radical-like boundary | `{'repairable_coordinate_blocker': 3}` |
| adjacent SAM methyltransferase negative | `{'duplicate_external_conflict': 1, 'reject/OOS_preserve_signal': 54}` |
| adjacent high-yield amidase/deaminase | `{'repairable_coordinate_blocker': 12}` |
| adjacent high-yield lyase/isomerase | `{'controlled_import_review_ready': 10, 'duplicate_current702_conflict': 1, 'repairable_coordinate_blocker': 2, 'repairable_locator_blocker': 1}` |
| adjacent methylcobalamin negative | `{'reject/OOS_preserve_signal': 61}` |
| adjacent non-PLP decarboxylase negative | `{'duplicate_current702_conflict': 6, 'reject/OOS_preserve_signal': 87}` |
| amidase/deaminase controls | `{'duplicate_current702_conflict': 9, 'duplicate_external_conflict': 2, 'reject/OOS_preserve_signal': 178}` |
| carbon-carbon lyase/decarboxylase | `{'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 21, 'hard_blocked_with_next_action': 39, 'repairable_coordinate_blocker': 12, 'repairable_locator_blocker': 1}` |
| cobalamin radical rearrangement | `{'duplicate_current702_conflict': 3, 'duplicate_external_conflict': 1, 'hard_blocked_with_next_action': 1, 'repairable_coordinate_blocker': 44, 'repairable_locator_blocker': 7}` |
| cobalamin/B12 radical enzymes | `{'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 53, 'repairable_coordinate_blocker': 16, 'repairable_locator_blocker': 1}` |
| coupled PLP adenosylcobalamin aminomutase | `{'duplicate_current702_conflict': 1, 'repairable_coordinate_blocker': 115}` |
| dehydratase/hydratase lyase | `{'duplicate_current702_conflict': 9, 'duplicate_external_conflict': 8, 'hard_blocked_with_next_action': 74, 'repairable_coordinate_blocker': 37, 'repairable_locator_blocker': 6}` |
| dehydrogenase/reductase OOS boundary | `{'duplicate_external_conflict': 25}` |
| dehydrogenase/reductase OOS controls | `{'duplicate_current702_conflict': 10, 'duplicate_external_conflict': 157, 'reject/OOS_preserve_signal': 5}` |
| flavin dehydrogenase boundary | `{'duplicate_current702_conflict': 3, 'duplicate_external_conflict': 130, 'reject/OOS_preserve_signal': 6}` |
| flavin dehydrogenase/reductase boundary | `{'duplicate_external_conflict': 2}` |
| flavin monooxygenase | `{'duplicate_current702_conflict': 1, 'duplicate_external_conflict': 9, 'repairable_coordinate_blocker': 66, 'repairable_locator_blocker': 18}` |
| flavin redox boundary | `{'duplicate_current702_conflict': 5, 'duplicate_external_conflict': 12, 'hard_blocked_with_next_action': 45, 'repairable_coordinate_blocker': 75, 'repairable_locator_blocker': 5}` |
| glycoside hydrolase | `{'controlled_import_review_ready': 1, 'duplicate_current702_conflict': 1, 'duplicate_external_conflict': 3, 'hard_blocked_with_next_action': 1, 'repairable_coordinate_blocker': 159, 'repairable_locator_blocker': 14}` |
| glycoside/fold-confounded OOS controls | `{'hard_blocked_with_next_action': 76, 'reject/OOS_preserve_signal': 218}` |
| glycoside/nucleoside | `{'controlled_import_review_ready': 39, 'duplicate_current702_conflict': 15, 'duplicate_external_conflict': 48, 'hard_blocked_with_next_action': 111, 'repairable_coordinate_blocker': 205, 'repairable_locator_blocker': 136}` |
| glycosyltransferase boundary | `{'duplicate_external_conflict': 20, 'hard_blocked_with_next_action': 7, 'repairable_coordinate_blocker': 121, 'repairable_locator_blocker': 56}` |
| heme peroxidase/oxidase boundary | `{'duplicate_current702_conflict': 4, 'duplicate_external_conflict': 101, 'repairable_coordinate_blocker': 6}` |
| heme peroxidase/oxidase-like | `{'duplicate_current702_conflict': 5, 'duplicate_external_conflict': 6, 'hard_blocked_with_next_action': 166, 'repairable_coordinate_blocker': 256, 'repairable_locator_blocker': 26}` |
| hydrolase-like fold-confounded negative | `{'duplicate_external_conflict': 12, 'hard_blocked_with_next_action': 114, 'reject/OOS_preserve_signal': 55}` |
| isomerase controls | `{'duplicate_current702_conflict': 15, 'duplicate_external_conflict': 33, 'reject/OOS_preserve_signal': 105}` |
| isomerase/racemase/epimerase | `{'duplicate_current702_conflict': 4, 'duplicate_external_conflict': 16, 'repairable_coordinate_blocker': 33, 'repairable_locator_blocker': 1}` |
| kinase/phosphotransferase | `{'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 51, 'hard_blocked_with_next_action': 47, 'repairable_coordinate_blocker': 166, 'repairable_locator_blocker': 6}` |
| ligase/synthetase abstention probe | `{'duplicate_current702_conflict': 1, 'duplicate_external_conflict': 4, 'hard_blocked_with_next_action': 152, 'reject/OOS_preserve_signal': 53}` |
| lyase controls | `{'duplicate_current702_conflict': 5, 'duplicate_external_conflict': 22, 'reject/OOS_preserve_signal': 92}` |
| metal hydrolase | `{'controlled_import_review_ready': 105, 'duplicate_current702_conflict': 10, 'duplicate_external_conflict': 12, 'hard_blocked_with_next_action': 576, 'repairable_coordinate_blocker': 424, 'repairable_locator_blocker': 58}` |
| metal hydrolase Mg/Mn controls | `{'controlled_import_review_ready': 1, 'duplicate_current702_conflict': 1, 'duplicate_external_conflict': 3, 'hard_blocked_with_next_action': 5, 'repairable_coordinate_blocker': 191, 'repairable_locator_blocker': 4}` |
| metal hydrolase amidase/peptidase boundary | `{'controlled_import_review_ready': 4, 'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 1, 'repairable_coordinate_blocker': 213}` |
| metal-cofactor non-target enzyme | `{'duplicate_external_conflict': 6, 'hard_blocked_with_next_action': 134, 'reject/OOS_preserve_signal': 63}` |
| metal/fold-confounded OOS controls | `{'duplicate_current702_conflict': 2, 'hard_blocked_with_next_action': 72, 'reject/OOS_preserve_signal': 214}` |
| near-orphan reviewed proteins | `{'duplicate_external_conflict': 2, 'repairable_coordinate_blocker': 35, 'repairable_locator_blocker': 82}` |
| near-orphan/no-reliable-structure | `{'controlled_import_review_ready': 27, 'duplicate_external_conflict': 4, 'hard_blocked_with_next_action': 162, 'repairable_coordinate_blocker': 34, 'repairable_locator_blocker': 123}` |
| no reliable structure pressure | `{'duplicate_external_conflict': 12, 'hard_blocked_with_next_action': 21, 'repairable_coordinate_blocker': 203}` |
| no-reliable-structure enzyme tail | `{'duplicate_current702_conflict': 1, 'hard_blocked_with_next_action': 140, 'repairable_coordinate_blocker': 23, 'repairable_locator_blocker': 35}` |
| non-serine protease OOS boundary | `{'hard_blocked_with_next_action': 108, 'reject/OOS_preserve_signal': 37}` |
| nucleoside/nucleotide hydrolase boundary | `{'duplicate_current702_conflict': 2, 'hard_blocked_with_next_action': 3, 'repairable_coordinate_blocker': 146, 'repairable_locator_blocker': 10}` |
| nucleotide phosphoryl-transfer boundary | `{'controlled_import_review_ready': 1, 'duplicate_current702_conflict': 2, 'repairable_coordinate_blocker': 190, 'repairable_locator_blocker': 22}` |
| oxygenase redox | `{'duplicate_current702_conflict': 1, 'duplicate_external_conflict': 103, 'repairable_coordinate_blocker': 1}` |
| phosphatase/phosphoryl hydrolase | `{'duplicate_external_conflict': 5, 'hard_blocked_with_next_action': 1, 'repairable_coordinate_blocker': 185, 'repairable_locator_blocker': 8}` |
| phosphoryl transfer | `{'controlled_import_review_ready': 6, 'duplicate_current702_conflict': 3, 'duplicate_external_conflict': 4, 'repairable_coordinate_blocker': 5, 'repairable_locator_blocker': 95}` |
| phosphoryl transfer kinase-like | `{'duplicate_external_conflict': 8, 'hard_blocked_with_next_action': 5, 'repairable_coordinate_blocker': 112, 'repairable_locator_blocker': 3}` |
| phosphoryl transfer/phosphatase | `{'controlled_import_review_ready': 1, 'duplicate_current702_conflict': 13, 'duplicate_external_conflict': 23, 'hard_blocked_with_next_action': 149, 'repairable_coordinate_blocker': 367, 'repairable_locator_blocker': 55}` |
| phosphoryl/fold-confounded OOS controls | `{'duplicate_external_conflict': 1, 'hard_blocked_with_next_action': 52, 'reject/OOS_preserve_signal': 200}` |
| radical SAM | `{'duplicate_external_conflict': 2, 'repairable_coordinate_blocker': 20}` |
| radical SAM iron-sulfur | `{'duplicate_current702_conflict': 1, 'duplicate_external_conflict': 14, 'repairable_coordinate_blocker': 195}` |
| radical SAM named families | `{'repairable_coordinate_blocker': 120}` |
| radical-SAM/cobalamin | `{'controlled_import_review_ready': 27, 'duplicate_current702_conflict': 2, 'duplicate_external_conflict': 4, 'repairable_coordinate_blocker': 7, 'repairable_locator_blocker': 59}` |
| redox oxygen/sulfur | `{'controlled_import_review_ready': 47, 'duplicate_current702_conflict': 15, 'duplicate_external_conflict': 28, 'hard_blocked_with_next_action': 254, 'repairable_coordinate_blocker': 372, 'repairable_locator_blocker': 94}` |
| sulfur oxidoreductase | `{'duplicate_current702_conflict': 5, 'duplicate_external_conflict': 75, 'repairable_coordinate_blocker': 61, 'repairable_locator_blocker': 41}` |
| terpene synthase/lyase | `{'duplicate_current702_conflict': 1, 'duplicate_external_conflict': 5, 'hard_blocked_with_next_action': 143, 'repairable_coordinate_blocker': 57, 'repairable_locator_blocker': 2}` |
| transferase tail outside current fingerprints | `{'duplicate_external_conflict': 28, 'hard_blocked_with_next_action': 35, 'repairable_coordinate_blocker': 13, 'repairable_locator_blocker': 3}` |

## Policy Blockers

| blocker | scope | ready rows affected |
| --- | --- | ---: |
| `production_registry_change_authorization_not_present` | `production_import` | 275 |
| `label_factory_gate_and_explicit_review_decision_not_run_here` | `production_import` | 275 |
| `full_foldseek_tm_current702_structural_duplicate_screen_not_computed` | `caveat` | 275 |

## Validation

- Validation passed: True
- JSON/count reconciliation passed: True
- Source provenance present for all preview rows: True
- Source provenance present for all review rows: True
- Source hashes present for all preview rows: True
- Source hashes present for all review rows: False
- Source-free locators present for all preview rows: False
- Coordinate hashes present for all preview rows: False
- Sequence hashes unique across preview: False
- Exact current702 coordinate/structure-ID overlaps: 1

## Review Queue

| candidate | lane | terminal state | blockers | next action |
| --- | --- | --- | --- | --- |
| `uniprot:P42694` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q68D91` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q5T1V6` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9Y2E5` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:O14638` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P49641` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P00813` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q01433` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q8NDL9` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9NZK5` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9UPW5` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:O00754` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P45381` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q01432` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:O76074` | metal hydrolase | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P21912` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q8S7E1` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9MBA1` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9NZ45` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9FYC2` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:O75306` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:O00217` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:O75251` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P0AC47` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q1QYU7` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P47985` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P21913` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q3T189` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9CQA3` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:A5PL98` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P07014` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P21801` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P21914` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q09545` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q8LB02` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q8LBZ7` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q6H4G3` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9FJP9` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:Q9ZR03` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| `uniprot:P77165` | redox oxygen/sulfur | `repairable_locator_blocker` | `coordinate_materialization_or_hash_missing`, `source_free_locator_sidecar_missing_or_not_ready` | Repair or rematerialize the source-free locator sidecar. |
| ... | ... | ... | ... | plus 12180 more rows |

## Outputs

- Preflight artifact: `artifacts/v3_external_import_review_preflight_current702_20260609.json`
- Ready preview: `artifacts/v3_external_import_review_ready_preview_current702_20260609.json`
- Repair/conflict queue: `artifacts/v3_external_import_review_repair_queue_current702_20260609.json`
