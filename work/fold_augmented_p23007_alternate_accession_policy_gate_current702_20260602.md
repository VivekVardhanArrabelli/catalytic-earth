# Fold-Augmented P23007 Alternate-Accession Policy Gate - current702

Run: 2026-06-02T22:13:42Z

Review-only policy gate for the Lever 3 m_csa:78/P23007 predicted-coordinate blocker. It composes the alternate-accession scout and remaining-blocker decision matrix into explicit candidate authorization decisions without fetching coordinates, substituting accessions, rerunning fold/TM scoring, or changing thresholds.

## Status

- fold_augmented_p23007_alternate_accession_policy_gate_ready_review_only
- Candidate alternate accessions: 4
- Policy-review-ready candidates: 4
- Candidates with AFDB: 4
- Pattern-compatible candidates: 4
- Replacement authorized now: 0
- Coordinate fetch authorized now: 0
- Deployment blockers cleared now: 0

## Candidate Policy Rows

| accession | id | organism | AFDB | pattern compatible | review ready | authorized |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| O75390 | CISY_HUMAN | Homo sapiens | True | True | True | False |
| P00889 | CISY_PIG | Sus scrofa | True | True | True | False |
| Q8VHF5 | CISY_RAT | Rattus norvegicus | True | True | True | False |
| Q9CZU6 | CISY_MOUSE | Mus musculus | True | True | True | False |

## Policy Contract

- Required fields: entry_id, blocked_accession, selected_alternate_accession, alternate_uniprotkb_id, organism, alphafold_db_model_version, active_site_position_mapping, ligand_or_binding_position_mapping, source_url, source_record_version_or_date, reviewer_decision, coordinate_fetch_plan
- Acceptance criteria: selected alternate is reviewed and AlphaFoldDB-backed, active-site and oxaloacetate-binding patterns remain compatible with P23007 source features, reviewer explicitly authorizes substitution before coordinate fetch, fold channel is rerun after authorization without changing thresholds
- Forbidden predictive inputs: mechanism_text, EC_ID, Rhea_ID, benchmark_label, source_id, target_name, heldout_label

## Interpretation

- The P23007 blocker has four AFDB-backed, pattern-compatible alternate accessions ready for policy review, but no alternate accession, coordinate fetch, or fold-channel rerun is authorized now.
- Approve exactly one alternate accession or reject the substitution path; only after approval should its AFDB coordinate be fetched and the fold channel rerun at the fixed threshold.
