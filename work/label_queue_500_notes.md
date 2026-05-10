# 500-Entry Label Queue Notes

These are curation notes for `artifacts/v3_label_expansion_candidates_500.json`
and the factory-generated `artifacts/v3_active_learning_review_queue_500.json`.
They are not registry labels yet. Use them to start the next bounded label pass,
but route every decision through `artifacts/v3_expert_review_export_500.json`
and `import-label-review` before counting formal labels.

## Queue State

- Curated labels already present: 475.
- Candidate rows beyond the curated slice: 25.
- Candidate groups: 9.
- Ready label-review rows after PLP/prenyl context updates: 21.
- Geometry entries: 499.
- Structure-mapping issues: 8 total, 7 already covered by existing labels.

## High-Confidence Seed Candidates

- `m_csa:482` 2,2-dialkylglycine decarboxylase (pyruvate):
  likely `plp_dependent_enzyme`. The `5PA` ligand is now mapped to PLP context,
  and retrieval ranks PLP first with local ligand support.
- `m_csa:486` polynucleotide 5'-phosphatase:
  likely `metal_dependent_hydrolase`. Mechanism text describes divalent-cation
  coordination and phosphate hydrolysis.
- `m_csa:494` propanediol dehydratase:
  likely `cobalamin_radical_rearrangement`, but treat carefully. The selected
  structure carries B12 only as structure-wide context, not local context
  (`B12` nearest active-site distance is 8.349 A), so labeling it positive may
  expose a structure/cofactor evidence gap.
- `m_csa:495` type II site-specific deoxyribonuclease, BgII:
  likely `metal_dependent_hydrolase`. Mechanism text describes Mg-assisted
  water activation and phosphodiester cleavage.
- `m_csa:497` nitric-oxide reductase (FMN):
  likely `flavin_dehydrogenase_reductase`. Retrieval has local FMN support and
  ranks flavin dehydrogenase/reductase first.

## Likely Out-Of-Scope Controls

- `m_csa:477` picornain 3C: cysteine protease Cys-His-Glu triad, outside the
  current Ser-His-Asp/Glu hydrolase seed.
- `m_csa:478` chitinase GH18: glycosidic hydrolase/substrate-assisted sugar
  chemistry.
- `m_csa:479` 4-alpha-glucanotransferase: glycosyl transfer/glycosidic
  chemistry.
- `m_csa:480` polygalacturonase: glycosidic-link hydrolysis, not the current
  metal-hydrolase seed.
- `m_csa:481` tryptophan-tRNA ligase: ATP-dependent aminoacyl-transfer/ligation.
- `m_csa:483` galactarolactone cycloisomerase: beta-elimination/cycloisomerase.
- `m_csa:484` protein farnesyltransferase: Zn-associated prenyl transfer, not
  hydrolysis; retrieval now applies FII/prenyl counterevidence.
- `m_csa:485` prephenate dehydratase: dehydration/decarboxylation.
- `m_csa:487` GDP-mannose 4,6-dehydratase: NADP-linked dehydratase chemistry.
- `m_csa:488` L-rhamnose isomerase: sugar isomerase/hydride-shift chemistry.
- `m_csa:490` dihydrofolate reductase: NADPH hydride transfer.
- `m_csa:491` 6,7-dihydropteridine reductase: NADH hydride transfer.
- `m_csa:492` carboxymethylenebutenolidase: Cys-His-Asp lactonase/hydrolase;
  likely outside current seeds but worth noting as a future thiol-hydrolase
  seed candidate.
- `m_csa:493` tRNA pseudouridine synthase: N-glycosidic cleavage/rearrangement.
- `m_csa:496` NAD(P)+ transhydrogenase: nicotinamide hydride transfer.
- `m_csa:498` glutathione synthase (eukaryotic): ATP-dependent ligase.
  Retrieval still ranks metal hydrolase first at `0.3949`, below the current
  `0.4115` abstention threshold, because local ADP/Mg context partially
  resembles metal-assisted phosphate chemistry.
- `m_csa:499` 3,2-trans-enoyl-CoA isomerase: enoyl-CoA isomerization.
- `m_csa:500` alcohol dehydrogenase (class II): Zn/NAD hydride chemistry.
- `m_csa:501` alcohol dehydrogenase (class V): likely Zn-dependent ADH
  homology, no selected structure positions.
- `m_csa:502` galactarate dehydratase: enolase-like dehydratase/elimination.

## Scorer Context Added Before Labeling

- `5PA` is now treated as a PLP-family ligand so `m_csa:482` ranks as a
  ligand-supported PLP hit.
- `FII` and farnesyltransferase text now trigger nonhydrolytic prenyl-transfer
  counterevidence, dropping `m_csa:484` below the current abstention threshold.
