# Fold-Augmented P23007 Alternate-Accession Scout - current702

Run: 2026-06-02T17:19:46Z

Review-only scout for source-backed alternate UniProt accessions that could resolve the m_csa:78/P23007 AlphaFoldDB-unavailable policy blocker. It records candidates only; no replacement is authorized.

## Status

- fold_augmented_p23007_alternate_accession_scout_ready_policy_review_only
- Candidate alternate accessions: 4
- Candidates with AFDB: 4
- Pattern-compatible candidates: 4
- Replacement authorized now: 0
- Deployment blockers cleared now: 0

## Candidates

| accession | id | organism | length | pattern compatible | authorized |
| --- | --- | --- | ---: | ---: | ---: |
| O75390 | CISY_HUMAN | Homo sapiens | 466 | True | False |
| P00889 | CISY_PIG | Sus scrofa | 464 | True | False |
| Q8VHF5 | CISY_RAT | Rattus norvegicus | 466 | True | False |
| Q9CZU6 | CISY_MOUSE | Mus musculus | 464 | True | False |

## Interpretation

- The P23007 blocker has reviewed citrate-synthase alternate accessions with AlphaFoldDB models and matching active-site/oxaloacetate-binding feature patterns, but no replacement is authorized by this artifact.
- Choose whether an orthologous reviewed citrate-synthase accession can substitute for P23007 under a deployment coordinate policy; if yes, fetch the chosen AFDB coordinate and rerun the fold channel without changing thresholds.
