# Fold-Augmented Confounded Proxy Alternate Structure Source Contract - current702

Run: 2026-06-04T08:48:47Z

Review-only Lever 3 contract for clearing the four residual predicted-structure-unavailable rows after AFDB v1-v6 exhausted. It approves no provider, downloads no coordinates, imports no files, scores no rows, and does not rerun or tune the fixed threshold.

## Status

- fold_augmented_confounded_proxy_alternate_structure_source_contract_ready_for_source_approval
- Coordinate-source blockers: 4
- AFDB all-version 404 rows: 4
- Approved alternate structures now: 0
- Remaining non-coordinate full-channel blockers: 1
- Blockers: ['alternate_predicted_structure_provider_not_approved', 'row_level_predicted_coordinates_not_staged', 'fold_geometry_rescore_inputs_missing', 'fixed_threshold_audit_not_ready_to_rerun']

## Affected Rows

| row | accession | AFDB statuses | missing evidence |
| --- | --- | --- | --- |
| m_csa:416 | P07071 | v1:404, v2:404, v3:404, v4:404, v5:404, v6:404 | approved non-AFDB deployment-valid predicted-structure coordinate source |
| m_csa:562 | P07658 | v1:404, v2:404, v3:404, v4:404, v5:404, v6:404 | approved non-AFDB deployment-valid predicted-structure coordinate source |
| m_csa:586 | P00806 | v1:404, v2:404, v3:404, v4:404, v5:404, v6:404 | approved non-AFDB deployment-valid predicted-structure coordinate source |
| m_csa:637 | P04531 | v1:404, v2:404, v3:404, v4:404, v5:404, v6:404 | approved non-AFDB deployment-valid predicted-structure coordinate source |

## Source Contract

- Coordinate source must be predicted-structure evidence, not experimental PDB metadata, source labels, target names, mechanism text, EC/Rhea IDs, or curated label state.
- Provider/model/version/path/checksum provenance must be recorded without using atlas-family or mechanism assignment metadata as predictive features.
- Each staged coordinate must map to the row accession or an explicitly reviewed accession/isoform equivalence decision before scoring.
- Coordinates must be staged as review-only query inputs first; no registry, ontology, import, sidecar, or production threshold change is allowed by this contract.
- Rows must be rescored only through the existing predicted-structure-vs-train-atlas fold/geometry/cofactor channel at unchanged fixed threshold 0.44155.
- The final fixed-threshold audit cannot rerun until these four rows have approved coordinates and Q43088 has approved locator/geometry evidence.

## Pass/Fail

- Pass condition: All four coordinate-source blocker rows receive approved deployment-valid predicted coordinates with source-free provenance and are ready for fold/geometry rescore at unchanged threshold 0.44155.
- Fail conditions: Any row still lacks an approved predicted coordinate source; Any row uses experimental-PDB metadata, mechanism text, EC/Rhea IDs, labels, source IDs, or target names as predictive evidence; Any coordinate is staged without provider/model/version/path/checksum provenance; Any threshold, split, label, registry, ontology, or import is changed under this contract.

## Decision

- Alternate structure rows ready now: False
- Surface completeness ready after contract alone: False
- Fixed-threshold audit ready to rerun now: False
- Apply or change threshold now: False
- Next gate: Approve or stage provider-neutral predicted structures for P07071, P07658, P00806, and P04531. After those four rows and Q43088 locator evidence are source-free and approved, rerun only the fixed-threshold fold/geometry channel; do not retune threshold 0.44155.

## Interpretation

- AFDB auto-version fallback cannot clear any of the four remaining coordinate-source blockers. The next evidence type is not another AFDB retry; it is an approved non-AFDB deployment-valid predicted-structure source with source-free provenance.
- Create an approval packet for a provider-neutral predicted structure source, stage four local query coordinates with checksums, then rescore those rows only after Q43088's locator gate is also cleared.
