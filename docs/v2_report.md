# Catalytic Earth V2 Research Report

## Status

This is a computational research artifact. Candidate enzymes are hypotheses
for expert review, not validated functions.

## Knowledge Graph

- Nodes: 1513
- Edges: 1475
- Node types: {'catalytic_residue': 330, 'ec_number': 48, 'm_csa_entry': 50, 'mechanism_text': 63, 'protein': 51, 'rhea_reaction': 53, 'structure': 918}

## Mechanism Benchmark

- Records: 50
- Leakage control: EC numbers, Rhea identifiers, and source entry ids are blocked from allowed features.

## Baseline Retrieval

- Method: token_overlap_baseline
- Fingerprints: 6

## Inconsistency Prototype

- Issues: 10
- Issue types: {'ec_mismatch': 2, 'missing_rhea_mapping': 8}

## Dark Hydrolase Campaign

- Candidates scored: 100
- Campaign scope: unreviewed UniProt hydrolase records scored for a
  Ser-His-Asp/Glu hydrolase-like computational signature.

## Top Candidate Accessions

- B4DQI4: score 12, motifs 1, length 188
- A0A060XT47: score 11, motifs 2, length 367
- A0A2U9BLL4: score 11, motifs 2, length 361
- A0A3B4XCC2: score 11, motifs 2, length 371
- A0A3B5B1G1: score 11, motifs 2, length 366
- A0A3N0YZ51: score 11, motifs 2, length 366
- A0A3Q0R634: score 11, motifs 2, length 323
- A0A3Q1EVE8: score 11, motifs 2, length 387
- A0A3Q3E319: score 11, motifs 2, length 369
- A0A3Q3MHQ1: score 11, motifs 2, length 368

## Limitations

- The benchmark uses seed fingerprint retrieval, not expert-labeled mechanism classes.
- Motif-based mining is a weak baseline and can produce many false positives.
- AlphaFold/PDB cross-references indicate structural availability, not catalytic competence.
- Wet-lab validation is required before any functional claim.

## Next Work

- Post-V2 work has already added geometry-aware active-site retrieval, curated
  positive/out-of-scope mechanism labels, ligand/cofactor context, and
  substrate-pocket descriptors, plus cofactor coverage audit artifacts.
- The current active benchmark is the 375-label geometry slice. It has 0 hard
  negatives, 0 near misses, and 0 out-of-scope false non-abstentions at
  calibrated abstention, with 3 evidence-limited in-scope abstentions
  (`m_csa:132`, `m_csa:353`, and `m_csa:372`) and 0 actionable in-scope
  failures after cofactor coverage and label-scope audit. Retained
  evidence-limited positives are audit-visible as `m_csa:41`, `m_csa:108`, and
  `m_csa:160`.
- A 400-entry label-expansion queue has been generated for the next curation
  pass, with 25 unlabeled candidate rows and 22 ready review entries.
- Expand dark-enzyme campaigns beyond generic hydrolases.
