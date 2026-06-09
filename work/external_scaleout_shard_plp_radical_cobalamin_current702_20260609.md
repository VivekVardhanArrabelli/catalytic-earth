# External Scaleout Shard - PLP/Radical/Cobalamin current702

PLP, radical-SAM, and cobalamin/B12 families stress proton-transfer, electron-transfer, radical, and cofactor-context axes that shallow geometry or representation-only approaches miss; adjacent SAM, non-PLP decarboxylase, methylcobalamin, and Schiff-base controls preserve cofactor-confounded negatives.

## Summary

- Candidate rows: 1606
- Target floor met: True
- Import-ready preview rows: 168
- Duplicate/current conflicts: 252
- Fetch failures: 67
- Validation passed: True

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 252 |
| `coordinate_ready_pending_locator` | 17 |
| `hard_blocked_with_next_action` | 4 |
| `import_ready_preview` | 168 |
| `locator_ready_candidate` | 69 |
| `provisional_external_countable_preflight_candidate` | 784 |
| `reject/OOS_preserve_signal` | 292 |
| `repairable_coordinate_blocker` | 11 |
| `repairable_locator_blocker` | 9 |

## Mechanism-Axis Coverage

| axis | count |
| --- | ---: |
| `cofactor_confounded_negative_axis` | 341 |
| `cofactor_context_axis` | 1382 |
| `electron_transfer_axis` | 387 |
| `proton_transfer_axis` | 931 |
| `radical_axis` | 579 |

## Family/Lane Counts

| family/lane | blocked_duplicate_or_current_registry_conflict | coordinate_ready_pending_locator | hard_blocked_with_next_action | import_ready_preview | locator_ready_candidate | provisional_external_countable_preflight_candidate | reject/OOS_preserve_signal | repairable_coordinate_blocker | repairable_locator_blocker |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B12 adenosylcobalamin enzymes | 1 | 0 | 0 | 3 | 1 | 18 | 0 | 3 | 0 |
| B12/cobalamin broad enzymes | 33 | 4 | 0 | 9 | 15 | 48 | 0 | 1 | 9 |
| PLP aminotransferase | 64 | 0 | 0 | 13 | 0 | 39 | 0 | 0 | 0 |
| PLP broad cofactor context | 14 | 1 | 0 | 33 | 3 | 57 | 0 | 0 | 0 |
| PLP decarboxylase | 42 | 0 | 0 | 21 | 7 | 49 | 0 | 1 | 0 |
| PLP lyase/eliminase | 13 | 2 | 0 | 42 | 0 | 56 | 0 | 2 | 0 |
| PLP racemase/epimerase | 1 | 0 | 1 | 16 | 0 | 94 | 0 | 1 | 0 |
| PLP sulfur lyase boundary | 1 | 3 | 0 | 18 | 2 | 90 | 0 | 0 | 0 |
| SAM-dependent radical-like boundary | 0 | 0 | 0 | 1 | 2 | 0 | 0 | 0 | 0 |
| adjacent SAM methyltransferase negative | 41 | 0 | 0 | 0 | 0 | 0 | 71 | 0 | 0 |
| adjacent methylcobalamin negative | 0 | 0 | 0 | 0 | 0 | 0 | 112 | 0 | 0 |
| adjacent non-PLP decarboxylase negative | 8 | 0 | 0 | 0 | 0 | 0 | 109 | 0 | 0 |
| cobalamin radical rearrangement | 6 | 7 | 3 | 4 | 1 | 39 | 0 | 0 | 0 |
| coupled PLP adenosylcobalamin aminomutase | 1 | 0 | 0 | 1 | 0 | 114 | 0 | 0 | 0 |
| radical SAM | 4 | 0 | 0 | 0 | 19 | 0 | 0 | 1 | 0 |
| radical SAM iron-sulfur | 23 | 0 | 0 | 5 | 12 | 70 | 0 | 1 | 0 |
| radical SAM named families | 0 | 0 | 0 | 2 | 7 | 110 | 0 | 1 | 0 |

## Materialization Blockers

| bucket | count |
| --- | ---: |
| `coordinate_ready_pending_locator` | 17 |
| `coordinate_repair` | 11 |
| `duplicate_conflict` | 252 |
| `hard_blocked_with_next_action` | 4 |
| `import_ready_preview` | 168 |
| `locator_ready_candidate` | 69 |
| `locator_repair` | 9 |
| `provisional_preflight` | 784 |
| `reject/OOS_preserve_signal` | 292 |

## Source Retrieval

- Total fetched search records before row materialization: 2251
- UniProt/Rhea fallback performed: False
- Coordinate downloads performed: False

| source | error type | count |
| --- | --- | ---: |
| `uniprot_entry` | `TimeoutError` | 67 |

## Source Queries

| lane | group | unique candidates | pages | query |
| --- | --- | ---: | ---: | --- |
| PLP aminotransferase | `plp` | 116 | 1 | `(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR (keyword:"Pyridoxal phosphate")) AND ((protein_name:aminotransferase) OR (ec:2.6.*))` |
| PLP decarboxylase | `plp` | 120 | 1 | `(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR (keyword:"Pyridoxal phosphate")) AND ((protein_name:decarboxylase) OR (ec:4.1.1.*))` |
| PLP lyase/eliminase | `plp` | 115 | 1 | `(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR (keyword:"Pyridoxal phosphate")) AND ((protein_name:lyase) OR (protein_name:eliminase) OR (protein_name:dehydratase) OR (ec:4.4.*) OR (ec:4.3.*))` |
| PLP racemase/epimerase | `plp` | 113 | 1 | `(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR (keyword:"Pyridoxal phosphate")) AND ((protein_name:racemase) OR (protein_name:epimerase) OR (ec:5.1.1.*))` |
| PLP sulfur lyase boundary | `plp` | 114 | 1 | `(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR (keyword:"Pyridoxal phosphate")) AND ((protein_name:cystathionine) OR (protein_name:cysteine) OR (protein_name:tryptophanase))` |
| PLP broad cofactor context | `plp` | 108 | 1 | `(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR (keyword:"Pyridoxal phosphate"))` |
| radical SAM | `radical_sam` | 24 | 1 | `(reviewed:true) AND (protein_name:"radical SAM")` |
| radical SAM iron-sulfur | `radical_sam` | 111 | 1 | `(reviewed:true) AND (keyword:"S-adenosyl-L-methionine") AND (keyword:"Iron-sulfur")` |
| radical SAM named families | `radical_sam` | 120 | 1 | `(reviewed:true) AND ((protein_name:anaerobic) OR (protein_name:activating) OR (protein_name:spore) OR (protein_name:biotin) OR (protein_name:lipoate)) AND (keyword:"S-adenosyl-L-methionine")` |
| SAM-dependent radical-like boundary | `radical_sam` | 3 | 1 | `(reviewed:true) AND ((protein_name:"SAM-dependent") OR (protein_name:"S-adenosylmethionine")) AND ((protein_name:radical) OR (keyword:Radical))` |
| cobalamin radical rearrangement | `cobalamin` | 60 | 1 | `(reviewed:true) AND ((cc_cofactor:cobalamin) OR (keyword:Cobalamin) OR (protein_name:cobalamin) OR (protein_name:"vitamin B12")) AND ((protein_name:mutase) OR (protein_name:rearrangement) OR (protein_name:aminomutase) OR (protein_name:dehydratase))` |
| B12 adenosylcobalamin enzymes | `cobalamin` | 26 | 1 | `(reviewed:true) AND ((protein_name:adenosylcobalamin) OR (protein_name:"coenzyme B12") OR (cc_cofactor:adenosylcobalamin))` |
| B12/cobalamin broad enzymes | `cobalamin` | 119 | 1 | `(reviewed:true) AND ((cc_cofactor:cobalamin) OR (keyword:Cobalamin) OR (protein_name:cobalamin) OR (protein_name:"vitamin B12"))` |
| coupled PLP adenosylcobalamin aminomutase | `cobalamin_plp_coupled` | 116 | 1 | `(reviewed:true) AND ((protein_name:aminomutase) OR (protein_name:"lysine 5,6-aminomutase")) AND ((cc_cofactor:cobalamin) OR (cc_cofactor:"pyridoxal phosphate") OR (keyword:Cobalamin) OR (keyword:"Pyridoxal phosphate"))` |
| adjacent SAM methyltransferase negative | `adjacent_cofactor_confounded_negative` | 112 | 1 | `(reviewed:true) AND ((keyword:"S-adenosyl-L-methionine") OR (protein_name:methyltransferase)) AND (protein_name:methyltransferase) NOT (protein_name:radical)` |
| adjacent non-PLP decarboxylase negative | `adjacent_cofactor_confounded_negative` | 117 | 1 | `(reviewed:true) AND (protein_name:decarboxylase) NOT (keyword:"Pyridoxal phosphate") NOT (cc_cofactor:"pyridoxal phosphate")` |
| adjacent methylcobalamin negative | `adjacent_cofactor_confounded_negative` | 112 | 1 | `(reviewed:true) AND ((cc_cofactor:cobalamin) OR (keyword:Cobalamin) OR (protein_name:cobalamin)) AND (protein_name:methyltransferase)` |
| adjacent Schiff-base non-PLP negative | `adjacent_cofactor_confounded_negative` | 0 | 1 | `(reviewed:true) AND (protein_name:"Schiff-base") NOT (keyword:"Pyridoxal phosphate")` |

## Next Mechanical Continuation

Continue this lane by increasing `--max-pages-per-query` before raising `--max-records-per-query`; prioritize non-duplicate import-ready and provisional rows for source-free structural duplicate screens, then repair locator/coordinate blockers. Do not import directly from this shard.
