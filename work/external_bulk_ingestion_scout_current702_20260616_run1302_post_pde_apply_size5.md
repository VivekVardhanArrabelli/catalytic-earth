# External Bulk Ingestion Scout - current702

Read-only scale-out scout over reviewed Swiss-Prot/UniProt rows with structured residue/cofactor evidence, AFDB/PDB coordinate provenance, and Rhea/EC provenance. All countable-looking rows remain provisional until `ce-external-admission-16-validation` validates the gate.

## Summary

- Candidate rows: 35
- Provisional import-preview rows: 10
- Fetch failures: 0
- Validation passed: True
- Requested max records per lane: 5
- Rhea fallback enabled: False

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 17 |
| `coordinate_ready_pending_locator` | 3 |
| `locator_ready_candidate` | 5 |
| `provisional_external_countable_preflight_candidate` | 10 |

## Family/Lane Counts

| family/lane | blocked_duplicate_or_current_registry_conflict | coordinate_ready_pending_locator | locator_ready_candidate | provisional_external_countable_preflight_candidate |
| --- | ---: | ---: | ---: | ---: |
| PLP children | 4 | 0 | 0 | 1 |
| glycoside/nucleoside | 0 | 2 | 0 | 3 |
| metal hydrolase | 3 | 0 | 2 | 0 |
| near-orphan/no-reliable-structure | 4 | 1 | 0 | 0 |
| phosphoryl transfer | 2 | 0 | 0 | 3 |
| radical-SAM/cobalamin | 4 | 0 | 1 | 0 |
| redox oxygen/sulfur | 0 | 0 | 2 | 3 |

## Source Retrieval And Limits

- UniProt single-query size limit used by this CLI: 500
- Pagination implemented: False
- Coordinate downloads performed: False
- Failure counts by source: `{}`

## Candidate Matrix

| candidate | lane | terminal state | locators | coordinate | duplicate status | next action |
| --- | --- | --- | ---: | --- | --- | --- |
| `uniprot:Q495T6` | metal hydrolase | `blocked_duplicate_or_current_registry_conflict` | 6 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:A4D2B0` | metal hydrolase | `blocked_duplicate_or_current_registry_conflict` | 7 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:Q96TA2` | metal hydrolase | `locator_ready_candidate` | 10 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:O75844` | metal hydrolase | `locator_ready_candidate` | 4 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:Q6GQQ9` | metal hydrolase | `blocked_duplicate_or_current_registry_conflict` | 13 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:P21912` | redox oxygen/sulfur | `provisional_external_countable_preflight_candidate` | 14 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:Q8S7E1` | redox oxygen/sulfur | `provisional_external_countable_preflight_candidate` | 8 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:Q9BUE6` | redox oxygen/sulfur | `locator_ready_candidate` | 3 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:Q9MBA1` | redox oxygen/sulfur | `provisional_external_countable_preflight_candidate` | 8 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:Q9UMS0` | redox oxygen/sulfur | `locator_ready_candidate` | 2 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:Q9Y617` | PLP children | `blocked_duplicate_or_current_registry_conflict` | 23 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:Q9Y600` | PLP children | `provisional_external_countable_preflight_candidate` | 1 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:P23721` | PLP children | `blocked_duplicate_or_current_registry_conflict` | 7 | experimental_pdb_coordinate_provenance_available | exact_current702_accession_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate/current-registry conflict evidence. |
| `uniprot:P04181` | PLP children | `blocked_duplicate_or_current_registry_conflict` | 13 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:Q96255` | PLP children | `blocked_duplicate_or_current_registry_conflict` | 7 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:P0ADR8` | glycoside/nucleoside | `coordinate_ready_pending_locator` | 0 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Run locator sourcing/repair from curated features or reviewed literature. |
| `uniprot:P0AF12` | glycoside/nucleoside | `provisional_external_countable_preflight_candidate` | 4 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:Q7XA67` | glycoside/nucleoside | `provisional_external_countable_preflight_candidate` | 6 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:Q9T0I8` | glycoside/nucleoside | `provisional_external_countable_preflight_candidate` | 6 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:Q8RY23` | glycoside/nucleoside | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Run locator sourcing/repair from curated features or reviewed literature. |
| `uniprot:Q969G6` | phosphoryl transfer | `blocked_duplicate_or_current_registry_conflict` | 13 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:P32189` | phosphoryl transfer | `blocked_duplicate_or_current_registry_conflict` | 23 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:P55263` | phosphoryl transfer | `provisional_external_countable_preflight_candidate` | 11 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:P27144` | phosphoryl transfer | `provisional_external_countable_preflight_candidate` | 12 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:A2RU49` | phosphoryl transfer | `provisional_external_countable_preflight_candidate` | 1 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Stage only as provisional preview; wait for ce-external-admission-16-validation before any countable import. |
| `uniprot:A0A6B9HEI0` | radical-SAM/cobalamin | `blocked_duplicate_or_current_registry_conflict` | 16 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:Q99707` | radical-SAM/cobalamin | `blocked_duplicate_or_current_registry_conflict` | 17 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:A6H5Y3` | radical-SAM/cobalamin | `blocked_duplicate_or_current_registry_conflict` | 17 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:Q9Z2Q4` | radical-SAM/cobalamin | `blocked_duplicate_or_current_registry_conflict` | 17 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:O60494` | radical-SAM/cobalamin | `locator_ready_candidate` | 20 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:Q6P1W5` | near-orphan/no-reliable-structure | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:Q6ZU52` | near-orphan/no-reliable-structure | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:Q96LL4` | near-orphan/no-reliable-structure | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:Q9NWQ9` | near-orphan/no-reliable-structure | `blocked_duplicate_or_current_registry_conflict` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / exact_external_pilot_accession_overlap | Do not import; preserve as duplicate of the external pilot row. |
| `uniprot:Q6NUJ2` | near-orphan/no-reliable-structure | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap / no_exact_external_pilot_accession_or_sequence_sha_overlap | Keep as near-orphan coordinate-ready row; find residue-level evidence before review. |

## Source Queries

| lane | records | query |
| --- | ---: | --- |
| metal hydrolase | 5 | `(reviewed:true) AND (ec:3.*) AND ((protein_name:metallo) OR (protein_name:zinc) OR (protein_name:metal) OR (cc_cofactor:zinc))` |
| redox oxygen/sulfur | 5 | `(reviewed:true) AND ((ec:1.14.*) OR (ec:1.8.*) OR (protein_name:oxygenase) OR (protein_name:sulfur) OR (keyword:"Iron-sulfur") OR (cc_cofactor:heme))` |
| PLP children | 5 | `(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR (keyword:"Pyridoxal phosphate") OR (protein_name:aminotransferase) OR (protein_name:decarboxylase))` |
| glycoside/nucleoside | 5 | `(reviewed:true) AND ((ec:3.2.*) OR (ec:2.4.*) OR (protein_name:glycosidase) OR (protein_name:nucleosidase))` |
| phosphoryl transfer | 5 | `(reviewed:true) AND ((ec:2.7.*) OR (protein_name:phosphotransferase) OR (protein_name:kinase))` |
| radical-SAM/cobalamin | 5 | `(reviewed:true) AND ((protein_name:"radical SAM") OR (keyword:"S-adenosyl-L-methionine") OR (keyword:Cobalamin) OR (protein_name:cobalamin) OR (cc_cofactor:cobalamin))` |
| near-orphan/no-reliable-structure | 5 | `(reviewed:true) AND ((protein_name:uncharacterized) OR (protein_name:hypothetical) OR (annotation_score:1))` |

## Query Plan To Continue

| lane | next action |
| --- | --- |
| metal hydrolase | Rerun this lane with --max-records-per-lane 10; keep Rhea fallback disabled unless reaction provenance is the limiter. |
| redox oxygen/sulfur | Rerun this lane with --max-records-per-lane 10; keep Rhea fallback disabled unless reaction provenance is the limiter. |
| PLP children | Rerun this lane with --max-records-per-lane 10; keep Rhea fallback disabled unless reaction provenance is the limiter. |
| glycoside/nucleoside | Rerun this lane with --max-records-per-lane 10; keep Rhea fallback disabled unless reaction provenance is the limiter. |
| phosphoryl transfer | Rerun this lane with --max-records-per-lane 10; keep Rhea fallback disabled unless reaction provenance is the limiter. |
| radical-SAM/cobalamin | Rerun this lane with --max-records-per-lane 10; keep Rhea fallback disabled unless reaction provenance is the limiter. |
| near-orphan/no-reliable-structure | Rerun this lane with --max-records-per-lane 10; keep Rhea fallback disabled unless reaction provenance is the limiter. |
