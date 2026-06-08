# External Source Ingestion Pilot - current702

Read-only external-source ingestion pilot for reviewed Swiss-Prot rows, AFDB/PDB coordinate provenance, and Rhea/EC reaction provenance. No production registry, ontology, import, model, split, or threshold was edited.

## Summary

- Candidate rows: 28
- Import-preview preflight rows: 16
- Fetch failures: 0
- Validation passed: True

## Terminal State Counts

| terminal state | count |
| --- | ---: |
| `blocked_duplicate_or_current_registry_conflict` | 1 |
| `coordinate_ready_pending_locator` | 4 |
| `external_countable_preflight_candidate` | 16 |
| `locator_ready_candidate` | 7 |

## Family/Lane Counts

| family/lane | blocked_duplicate_or_current_registry_conflict | coordinate_ready_pending_locator | external_countable_preflight_candidate | locator_ready_candidate |
| --- | ---: | ---: | ---: | ---: |
| PLP children | 1 | 0 | 3 | 0 |
| glycoside/nucleoside | 0 | 0 | 2 | 2 |
| metal hydrolase | 0 | 0 | 0 | 4 |
| near-orphan/no-reliable-structure | 0 | 4 | 0 | 0 |
| phosphoryl transfer | 0 | 0 | 4 | 0 |
| radical-SAM/cobalamin | 0 | 0 | 3 | 1 |
| redox oxygen/sulfur | 0 | 0 | 4 | 0 |

## Candidate Matrix

| candidate | lane | terminal state | locators | coordinate | conflict | next action |
| --- | --- | --- | ---: | --- | --- | --- |
| `uniprot:Q495T6` | metal hydrolase | `locator_ready_candidate` | 6 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:A4D2B0` | metal hydrolase | `locator_ready_candidate` | 7 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:Q6GQQ9` | metal hydrolase | `locator_ready_candidate` | 13 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:Q9H8Y5` | metal hydrolase | `locator_ready_candidate` | 8 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:P09601` | redox oxygen/sulfur | `external_countable_preflight_candidate` | 6 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:P30519` | redox oxygen/sulfur | `external_countable_preflight_candidate` | 9 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:P29082` | redox oxygen/sulfur | `external_countable_preflight_candidate` | 4 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:Q9UGB7` | redox oxygen/sulfur | `external_countable_preflight_candidate` | 9 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:Q9Y617` | PLP children | `external_countable_preflight_candidate` | 23 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:P23721` | PLP children | `blocked_duplicate_or_current_registry_conflict` | 7 | experimental_pdb_coordinate_provenance_available | exact_current702_accession_overlap | Do not import; preserve as duplicate/current-registry conflict evidence. |
| `uniprot:P04181` | PLP children | `external_countable_preflight_candidate` | 13 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:Q96255` | PLP children | `external_countable_preflight_candidate` | 7 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:O00462` | glycoside/nucleoside | `locator_ready_candidate` | 3 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:O43598` | glycoside/nucleoside | `locator_ready_candidate` | 15 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:O60502` | glycoside/nucleoside | `external_countable_preflight_candidate` | 9 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:P04062` | glycoside/nucleoside | `external_countable_preflight_candidate` | 2 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:Q3T906` | phosphoryl transfer | `external_countable_preflight_candidate` | 10 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:Q969G6` | phosphoryl transfer | `external_countable_preflight_candidate` | 13 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:P32189` | phosphoryl transfer | `external_countable_preflight_candidate` | 23 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:Q9Y6K0` | phosphoryl transfer | `external_countable_preflight_candidate` | 9 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:A0A6B9HEI0` | radical-SAM/cobalamin | `locator_ready_candidate` | 16 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Attach Rhea/specific reaction provenance or route to family review. |
| `uniprot:Q99707` | radical-SAM/cobalamin | `external_countable_preflight_candidate` | 17 | experimental_pdb_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:A6H5Y3` | radical-SAM/cobalamin | `external_countable_preflight_candidate` | 17 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:Q9Z2Q4` | radical-SAM/cobalamin | `external_countable_preflight_candidate` | 17 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Stage in external import-preview artifact; run structural duplicate screen before import. |
| `uniprot:Q6P1W5` | near-orphan/no-reliable-structure | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Keep as near-orphan coordinate-ready row; find residue-level evidence before review. |
| `uniprot:Q6ZU52` | near-orphan/no-reliable-structure | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Keep as near-orphan coordinate-ready row; find residue-level evidence before review. |
| `uniprot:Q96LL4` | near-orphan/no-reliable-structure | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Keep as near-orphan coordinate-ready row; find residue-level evidence before review. |
| `uniprot:Q9NWQ9` | near-orphan/no-reliable-structure | `coordinate_ready_pending_locator` | 0 | afdb_predicted_coordinate_provenance_available | no_exact_current702_accession_or_sequence_sha_overlap | Keep as near-orphan coordinate-ready row; find residue-level evidence before review. |

## Source Queries

| lane | records | query |
| --- | ---: | --- |
| metal hydrolase | 4 | `(reviewed:true) AND (ec:3.*) AND ((protein_name:metallo) OR (protein_name:zinc) OR (protein_name:metal))` |
| redox oxygen/sulfur | 4 | `(reviewed:true) AND ((ec:1.14.*) OR (ec:1.8.*) OR (protein_name:oxygenase) OR (protein_name:sulfur))` |
| PLP children | 4 | `(reviewed:true) AND ((cc_cofactor:"pyridoxal phosphate") OR (keyword:"Pyridoxal phosphate") OR (protein_name:aminotransferase))` |
| glycoside/nucleoside | 4 | `(reviewed:true) AND (ec:3.2.*)` |
| phosphoryl transfer | 4 | `(reviewed:true) AND ((ec:2.7.*) OR (protein_name:phosphotransferase))` |
| radical-SAM/cobalamin | 4 | `(reviewed:true) AND ((protein_name:"radical SAM") OR (keyword:"S-adenosyl-L-methionine") OR (keyword:Cobalamin) OR (protein_name:cobalamin))` |
| near-orphan/no-reliable-structure | 4 | `(reviewed:true) AND (protein_name:uncharacterized)` |
