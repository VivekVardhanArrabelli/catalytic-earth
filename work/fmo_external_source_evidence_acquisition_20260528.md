# FMO External Source Evidence Acquisition

Run time: 2026-05-28T04:12:00Z

Scope: source-evidence acquisition for the six priority external FMO candidates only. No labels, registries, ontology files, thresholds, production scoring, model outputs, imports, or source-free geometry were changed. No candidate is counted as label support in this run.

## Bottom line

All six priority candidates are source-clean enough to proceed to source-free structure/geometry and review-packet work:

| priority | candidate | source disposition | duplicate-risk focus |
| --- | --- | --- | --- |
| 1 | `uniprot:P12015` CHMO | `source_clean_for_geometry` | Low to medium against `m_csa:131`/`m_csa:551`; BVMO chemistry is distinct from aromatic hydroxylation. |
| 2 | `uniprot:H3JQW0` OTEMO | `source_clean_for_geometry` | Low against requested M-CSA rows, but prior broader structural leakage exists outside this source run. |
| 3 | `uniprot:Q93TJ5` HAPMO | `source_clean_for_geometry` | Low to medium against aromatic hydroxylase rows; BVMO ester-forming chemistry is distinct. |
| 4 | `uniprot:Q01740` human FMO1 | `source_clean_for_geometry` | Low; class B soft-nucleophile oxygenation, not local aromatic or reduced-FMN rows. |
| 5 | `uniprot:O15229` KMO | `source_clean_for_geometry` | High import-gate risk against `m_csa:131` from prior local structural screen. |
| 6 | `uniprot:P23262` salicylate 1-monooxygenase | `source_clean_for_geometry` | Medium to high against `m_csa:131` and `m_csa:551`; needs strict duplicate/leakage handling. |

Machine-readable artifact: `artifacts/v3_fmo_external_source_evidence_acquisition_702_20260528.json`.

## Candidate Evidence

### `uniprot:P12015` CHMO

- Cofactor: reviewed UniProt P12015 records FAD for cyclohexanone monooxygenase.
- Reductant mode: single-component FAD/NADPH reductive activation; no partner reductase or reduced-FMN supply.
- Oxygen insertion: UniProt/Rhea `RHEA:24068` records cyclohexanone + NADPH + O2 to hexano-6-lactone. CHMO mechanism literature supports C4a-peroxyflavin/C4a-hydroperoxyflavin and Criegee-type Baeyer-Villiger oxygen insertion.
- Reaction summary: cyclohexanone -> epsilon-caprolactone/hexano-6-lactone.
- Public identifiers: UniProtKB:P12015 reviewed; Rhea:24068; AlphaFold AF-P12015-F1; no PDB cross-reference on the reviewed UniProt entry.
- Duplicate risk: low to medium against `m_csa:131` and `m_csa:551`; low against `m_csa:132` and `m_csa:973`.
- Not a negative family: product is an oxygen-inserted lactone, not ordinary flavin dehydrogenase, oxidase-only chemistry, Fe-S relay, heme/P450, pterin/metal/copper oxygenase, or name-only monooxygenase.

Disposition: `source_clean_for_geometry`.

### `uniprot:H3JQW0` OTEMO

- Cofactor: reviewed UniProt H3JQW0 records FAD; OTEMO primary structure work reports FAD and FAD/NADP(+) structures.
- Reductant mode: single-component FAD/NADPH BVMO; no partner reductase or reduced-FMN supply.
- Oxygen insertion: UniProt/Rhea `RHEA:33015` records NADPH/O2 oxygen insertion into an oxocyclopentenylacetyl-CoA substrate; BVMO sources support flavin-peroxide/Criegee intermediate chemistry.
- Reaction summary: oxocyclopentenylacetyl-CoA substrate -> lactone-like pyranone acetyl-CoA product.
- Public/local identifiers: UniProtKB:H3JQW0 reviewed; Rhea:33015; PDB 3UOV, 3UOX, 3UOY, 3UOZ, 3UP4, 3UP5; AlphaFold AF-H3JQW0-F1; pre-existing local `afdb_H3JQW0.cif` was noted but not geometry-scored.
- Duplicate risk: low against `m_csa:131`, `m_csa:132`, `m_csa:551`, and `m_csa:973`; however prior full-current structural screening recorded broader duplicate/leakage outside those four rows.
- Not a negative family: lactonizing BVMO oxygen insertion with FAD/NADPH structure context, not ordinary reductase, oxidase-only, Fe-S relay, heme/P450, pterin/metal/copper oxygenase, or name-only monooxygenase.

Disposition: `source_clean_for_geometry`, with prior duplicate/leakage caveat carried forward.

### `uniprot:Q93TJ5` HAPMO

- Cofactor: reviewed UniProt Q93TJ5 records FAD; primary HAPMO sources describe a FAD-containing Baeyer-Villiger monooxygenase.
- Reductant mode: single-component FAD/NADPH reductive activation; no partner reductase or reduced-flavin supply.
- Oxygen insertion: UniProt/Rhea `RHEA:22916` records 4'-hydroxyacetophenone + NADPH + O2 to 4-acetoxyphenol; HAPMO sources describe a peroxyflavin intermediate generated from reduced flavin and O2.
- Reaction summary: 4'-hydroxyacetophenone -> 4-acetoxyphenol.
- Public identifiers: UniProtKB:Q93TJ5 reviewed; Rhea:22916; AlphaFold AF-Q93TJ5-F1; no PDB cross-reference on the reviewed UniProt entry.
- Duplicate risk: low to medium against `m_csa:131`/`m_csa:551`; low against `m_csa:132`/`m_csa:973`.
- Not a negative family: ester-forming BVMO oxygen insertion, not dehydrogenase/reductase, oxidase-only, Fe-S relay, heme/P450, pterin/metal/copper oxygenase, or name-only monooxygenase.

Disposition: `source_clean_for_geometry`.

### `uniprot:Q01740` Human FMO1

- Cofactor: reviewed UniProt Q01740 records FAD.
- Reductant mode: single-component FAD/NADPH activation for dimethylaniline and trimethylamine reactions; one reviewed hypotaurine reaction also permits NADH. Not a two-component reduced-flavin system.
- Oxygen insertion: UniProt/Rhea records N,N-dimethylaniline N-oxide (`RHEA:24468`) and trimethylamine N-oxide (`RHEA:31979`) reactions; FMO oxidative-half-reaction literature supports stable C4a-hydroperoxyflavin oxygenating species.
- Reaction summary: soft nucleophiles such as N,N-dimethylaniline or trimethylamine -> N-oxide products.
- Public identifiers: UniProtKB:Q01740 reviewed; Rhea:24468, 31979, 69819, 74111; AlphaFold AF-Q01740-F1; no PDB cross-reference on the reviewed UniProt entry.
- Duplicate risk: low against `m_csa:131`, `m_csa:132`, and `m_csa:551`; low to medium mechanistic analogy against `m_csa:973` but not a two-component FMNH2 sulfur oxygenase.
- Not a negative family: FAD/NADPH soft-nucleophile monooxygenation, not ordinary reductase, oxidase-only, Fe-S relay, heme/P450, pterin/metal/copper oxygenase, or name-only monooxygenase.

Disposition: `source_clean_for_geometry`.

### `uniprot:O15229` KMO

- Cofactor: reviewed UniProt O15229 records FAD; public PDB cross-reference 5X68 provides human KMO structure context.
- Reductant mode: single-component FAD/NADPH reductive activation; not a two-component reduced-flavin oxygenase.
- Oxygen insertion: UniProt/Rhea `RHEA:20545` records L-kynurenine + NADPH + O2 to 3-hydroxy-L-kynurenine; KMO oxidative-half-reaction literature supports C4a-hydroperoxyflavin in the hydroxylation mechanism.
- Reaction summary: L-kynurenine -> 3-hydroxy-L-kynurenine.
- Public/local identifiers: UniProtKB:O15229 reviewed; Rhea:20545; PDB 5X68; AlphaFold AF-O15229-F1; pre-existing local `afdb_O15229.cif` was noted but not geometry-scored.
- Duplicate risk: high import-gate risk against `m_csa:131` because prior local structural screening found O15229 near pdb:1DOC/m_csa:131 with max pair TM 0.8122. Medium against `m_csa:551`; low against `m_csa:132`/`m_csa:973`.
- Not a negative family: hydroxylated kynurenine product from FAD/NADPH/O2 chemistry, not ordinary reductase, oxidase-only, Fe-S relay, heme/P450, pterin/metal/copper oxygenase, or name-only monooxygenase.

Disposition: `source_clean_for_geometry`, but any later review packet must foreground the prior duplicate/leakage blocker.

### `uniprot:P23262` Salicylate 1-Monooxygenase

- Cofactor: reviewed UniProt P23262 records FAD; public PDB cross-reference 6BZ5 is available.
- Reductant mode: single-component FAD/NADH reductive activation; not NADPH and not a partner-reductase reduced-FMN system.
- Oxygen insertion: UniProt/Rhea `RHEA:11004` records salicylate + NADH + O2 to catechol + CO2; NahG mechanism literature explicitly supports C4a-hydroperoxyflavin oxidative decarboxylation.
- Reaction summary: salicylate -> catechol + CO2.
- Public identifiers: UniProtKB:P23262 reviewed; Rhea:11004; PDB 6BZ5; AlphaFold AF-P23262-F1.
- Duplicate risk: medium to high against `m_csa:131` and `m_csa:551`; low against `m_csa:132` and `m_csa:973`.
- Not a negative family: one-component FAD/NADH flavoprotein monooxygenase with C4a-hydroperoxyflavin oxygen transfer, not ordinary reductase, oxidase-only, Fe-S relay, heme/P450, pterin/metal/copper oxygenase, or name-only monooxygenase.

Disposition: `source_clean_for_geometry`.

## Source URLs Used

- UniProt: P12015, H3JQW0, Q93TJ5, Q01740, O15229, P23262.
- Rhea: 24068, 33015, 22916, 24468, 31979, 69819, 74111, 20545, 11004.
- Structures/models: RCSB 3UOV/3UOX/3UOY/3UOZ/3UP4/3UP5, 5X68, 6BZ5; AlphaFold AF-P12015-F1, AF-H3JQW0-F1, AF-Q93TJ5-F1, AF-Q01740-F1, AF-O15229-F1, AF-P23262-F1.
- Mechanism sources: PubMed 11551214, 30030997, 22506764, 22267661, 12514023, 16049018, 7217103, 18443301, 32687799, 34965488; PMC 3302634, 152415, 111394, 4116332, 3736096, 8824312.

## Guardrail

This source-evidence artifact does not authorize geometry materialization, label import, registry migration, ontology edits, threshold changes, production scoring changes, model-output changes, or countable FMO support claims.
