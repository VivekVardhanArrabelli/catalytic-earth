# Off-M-CSA In-Scope Recovery Feasibility

Run: 2026-06-28T14:40:00Z
Status: `blocked_offmcsa_recovery_no_local_labeled_nonmcsa_positive_structures`

## Question

- Is there a locally available surface that is non-M-CSA, carries a trusted mechanism fingerprint, and has a structure, so off-M-CSA in-scope fold-NN recovery can be measured?

## Completed Half

- Off-M-CSA OOS rejection: `fold_nn_abstention_signal_generalizes_off_mcsa`.

## Inventory

- Structured surfaces scanned: 42.
- Distinct non-M-CSA structured accessions: 248.
- Labelled non-M-CSA positives supplied: 0.
- Usable labelled non-M-CSA positives with structure: 0.

### Top surfaces by non-M-CSA structures

- external_materialization_wave2_coordinates_current702_20260609: 248 structures, 121 non-M-CSA accessions.
- v3_external_structural_coordinates_1025_all30: 30 structures, 28 non-M-CSA accessions.
- v3_prospective_external_minicampaign_structural_coordinates_20260520: 11 structures, 11 non-M-CSA accessions.
- v3_external_structural_coordinates_1025: 10 structures, 10 non-M-CSA accessions.
- family_panel_source_backed_coordinates_current702_20260601: 20 structures, 7 non-M-CSA accessions.
- v3_external_hard_negative_new_candidate_structural_coordinates_1025: 8 structures, 7 non-M-CSA accessions.
- v3_flavin_dehydrogenase_deep_packet_structural_coordinates_20260521: 7 structures, 7 non-M-CSA accessions.
- v3_flavin_dehydrogenase_second_deep_packet_structural_coordinates_20260521: 7 structures, 7 non-M-CSA accessions.

## Blocker

- Local structured surfaces are M-CSA/current702; the only non-M-CSA structures are external negatives (used for the abstention test) and unlabeled import candidates. The non-M-CSA positives (bronze/SwissProt expansion) carry mechanism labels but have no local structures.

## Unblock Plan

1. Select a sample of trusted bronze-admitted non-M-CSA positives whose admission does not depend on structure (so fold-NN recovery stays non-circular), each mapped to a true fingerprint family present in the M-CSA train atlas.
2. Materialize their AlphaFold CIFs (a bounded download requiring explicit authorization; respect the disk and no-large-download guardrails).
3. foldseek easy-search the sample against the M-CSA train in-scope atlas (reuse the staged 132-target atlas) and build a recovery readout: does the fold nearest neighbour carry the true fingerprint, and at what fold-NN score, versus the abstention frontier.
- Guardrails: No heldout rows; no threshold selected; bronze labels are evaluation targets only, never model features; registry untouched.

## Decision Needed

- Materializing AlphaFold structures for labelled non-M-CSA positives is a download and needs explicit authorization before the recovery half can be measured.

## Guardrails

- Read-only inventory; no download, no registry/label/threshold/model change, no heldout read.
