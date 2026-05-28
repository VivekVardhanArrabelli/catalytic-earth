# FMO External Source-Evidence Acquisition - 2026-05-28

Run time: 2026-05-28T05:13:19Z

Scope: external source-evidence review for the six prioritized FMO candidates only. No labels, registries, ontology files, thresholds, production scoring, model outputs, imports, or geometry materialization were changed. All conclusions here are non-countable source evidence only.

## Bottom Line

Clean source-only leads for later source-free geometry and review packets:

- `uniprot:P12015` CHMO / cyclohexanone monooxygenase
- `uniprot:Q93TJ5` HAPMO / 4-hydroxyacetophenone monooxygenase
- `uniprot:Q01740` human FMO1 / dimethylaniline or soft-nucleophile monooxygenase

Boundary holds despite positive FMO source chemistry:

- `uniprot:H3JQW0` OTEMO: source-positive BVMO, but prior duplicate/leakage and BVMO-lane redundancy keep it on hold.
- `uniprot:O15229` KMO: source-positive FAD/NADPH hydroxylase, but prior high-TM duplicate/leakage against `m_csa:131` keeps it on hold.
- `uniprot:P23262` salicylate 1-monooxygenase: source-positive FAD/NADH C4a-hydroperoxyflavin enzyme, but same-family aromatic hydroxylase overlap with `m_csa:131` and `m_csa:551` keeps it on hold.

No candidate is rejected as `reject_not_fmo`. No candidate is countable now.

## Evidence Table

| Priority | Candidate | Source evidence | Duplicate risk | Disposition |
| --- | --- | --- | --- | --- |
| 1 | `uniprot:P12015` CHMO | Reviewed UniProt/Rhea FAD/NADPH/O2 lactone reaction; source reports one FAD per subunit and 4a-hydroperoxyflavin during Baeyer-Villiger oxygen insertion. | Low against `m_csa:131`, `132`, `551`, `973`; broad BVMO overlap only. | `source_clean_for_geometry` |
| 2 | `uniprot:H3JQW0` OTEMO | Reviewed UniProt/Rhea FAD/NADPH/O2 BVMO reaction; PDB structures include FAD and FAD/NADP states; open structural paper supports flavin-peroxide/Criegee BVMO cycle. | Broad BVMO overlap plus prior local duplicate/leakage terminal context. | `source_boundary_hold` |
| 3 | `uniprot:Q93TJ5` HAPMO | Reviewed UniProt/Rhea FAD/NADPH/O2 ester-forming BVMO reaction; sources report noncovalent FAD per subunit and NADPH-coupled substrate oxygenation. | Low direct duplicate risk; broad BVMO overlap only. | `source_clean_for_geometry` |
| 4 | `uniprot:Q01740` human FMO1 | Reviewed UniProt/Rhea FAD/NADPH or NADH soft-nucleophile oxygenation reactions; human FMO1 source directly reports stable C4a-hydroperoxyflavin after NADPH/O2. | Low; partial sulfur-oxygenation theme overlap with `m_csa:973` but different class and reductive system. | `source_clean_for_geometry` |
| 5 | `uniprot:O15229` KMO | Reviewed UniProt/Rhea FAD/NADPH/O2 kynurenine hydroxylation; human KMO PDB has FAD; KMO source supports flavin C4a peroxide/hydroperoxide hydroxylation model. | High against `m_csa:131` from prior source-free terminal evidence; family overlap with `m_csa:551`. | `source_boundary_hold` |
| 6 | `uniprot:P23262` salicylate 1-monooxygenase | Reviewed UniProt/Rhea FAD/NADH/O2 oxidative decarboxylation; source explicitly assigns C4a-hydroperoxyflavin-mediated catechol formation. | Same-family aromatic hydroxylase overlap with `m_csa:131` and `m_csa:551`. | `source_boundary_hold` |

## Candidate Notes

### `uniprot:P12015` CHMO

- FAD/FMN: FAD, one per subunit, supported by UniProt and PMID:1261545/PMID:7093214.
- Reductive activation: single-component FAD/NADPH BVMO; UniProt/Rhea reaction is cyclohexanone + NADPH + O2 to epsilon-caprolactone + NADP(+) + H2O. UniProt notes NADH is not used.
- O2 oxygen insertion: source evidence reports a 4a-hydroperoxyflavin intermediate and Baeyer-Villiger oxygen insertion into cyclohexanone.
- IDs: UniProt `P12015` reviewed; Rhea `RHEA:24068`; AlphaFold `AF-P12015-F1` v6; no PDB found in UniProt cross-references.
- Duplicate risk: low against all current rows; CHMO is a carbonyl/lactone BVMO rather than aromatic hydroxylase, FMNH2 alkanal luciferase, phenol hydroxylase, or two-component sulfur monooxygenase.
- Not a negative family: not dehydrogenase/reductase, oxidase-only, Fe-S relay, heme/P450, pterin/metal/copper oxygenase, or name-only monooxygenase because sources give FAD, NADPH, O2, 4a-hydroperoxyflavin, and oxygen-inserted lactone product.

Disposition: `source_clean_for_geometry`.

### `uniprot:H3JQW0` OTEMO

- FAD/FMN: FAD, one per subunit, supported by UniProt; PDB entries `3UOV`, `3UOX`, `3UOY`, `3UOZ`, `3UP4`, and `3UP5` include FAD, with several FAD/NADP complexes.
- Reductive activation: single-component type I FAD/NADPH BVMO, not the type II FMN/NADH camphor BVMO and not a reductase-only component.
- O2 oxygen insertion: UniProt/Rhea records lactonization of an oxocyclopentenylacetyl-CoA substrate. PMCID:PMC3302634 describes the BVMO cycle through reduced FAD, O2, a flavin-peroxide intermediate, Criegee intermediate, and lactone product.
- IDs: UniProt `H3JQW0` reviewed; Rhea `RHEA:33015`; PDB `3UOV`, `3UOX`, `3UOY`, `3UOZ`, `3UP4`, `3UP5`; AlphaFold `AF-H3JQW0-F1` v6.
- Duplicate risk: low direct chemistry duplicate against `m_csa:131`, `132`, `551`, and `973`, but high operational risk from prior local duplicate/leakage terminal context and overlap with the CHMO/HAPMO BVMO lane.
- Not a negative family: the source record is FAD/NADPH BVMO oxygen insertion, not ordinary flavin redox, oxidase-only, Fe-S relay, heme/P450, pterin/metal/copper, or name-only.

Disposition: `source_boundary_hold`.

### `uniprot:Q93TJ5` HAPMO

- FAD/FMN: FAD, one per subunit, supported by UniProt and PMID:11322873.
- Reductive activation: single-component FAD/NADPH BVMO; HAPMO sources report NADPH-dependent catalysis and tight coupling between NADPH oxidation and substrate oxygenation.
- O2 oxygen insertion: UniProt describes Baeyer-Villiger insertion into a carbon-carbon bond adjacent to a carbonyl. HAPMO literature places it in the peroxyflavin BVMO mechanism class.
- IDs: UniProt `Q93TJ5` reviewed; Rhea `RHEA:22916`; AlphaFold `AF-Q93TJ5-F1` v6; no PDB found in UniProt cross-references.
- Duplicate risk: low direct duplicate risk against current M-CSA FMO rows, though it should not be treated as a separate diversity axis from BVMO alone.
- Not a negative family: not a generic flavin dehydrogenase/reductase or oxidase-only enzyme because the product is an oxygen-inserted ester and the sources support FAD/NADPH/O2 BVMO chemistry.

Disposition: `source_clean_for_geometry`.

### `uniprot:Q01740` human FMO1

- FAD/FMN: FAD, supported by UniProt and human FMO1 source evidence.
- Reductive activation: single-chain class B FAD FMO; UniProt/Rhea records NADPH reactions for trimethylamine and N,N-dimethylaniline, plus NADPH and NADH reactions for hypotaurine.
- O2 oxygen insertion: PMID:34509493 directly reports a stable C4a-hydroperoxyflavin intermediate of human FMO1 after NADPH reduction in O2; UniProt/Rhea records N-oxide and hypotaurine-to-taurine oxygenation products.
- IDs: UniProt `Q01740` reviewed; Rhea `RHEA:69819`, `RHEA:74111`, `RHEA:31979`, `RHEA:24468`; AlphaFold `AF-Q01740-F1` v6; no PDB found in UniProt cross-references.
- Duplicate risk: low against `m_csa:131`, `132`, and `551`; partial sulfur-oxygenation theme overlap with `m_csa:973`, but FMO1 is single-chain FAD/NAD(P)H class B FMO while DszC is two-component reduced-FMN sulfur monooxygenase.
- Not a negative family: explicitly FAD/NAD(P)H FMO chemistry; no heme/P450, Fe-S relay, pterin, metal, copper, oxidase-only, or name-only mechanism.

Disposition: `source_clean_for_geometry`.

### `uniprot:O15229` KMO

- FAD/FMN: FAD, supported by UniProt and PMID:10672018/PMID:29429898; PDB `5X68` is human KMO and includes FAD.
- Reductive activation: single-component FAD/NADPH monooxygenase; UniProt/Rhea records L-kynurenine + NADPH + O2 to 3-hydroxy-L-kynurenine.
- O2 oxygen insertion: KMO structural source supports a flavin C4a peroxide/hydroperoxide intermediate in the hydroxylation model.
- IDs: UniProt `O15229` reviewed; Rhea `RHEA:20545`; PDB `5X68`; AlphaFold `AF-O15229-F1` v6.
- Duplicate risk: high against canonical `m_csa:131` from prior source-free terminal duplicate/leakage evidence; family overlap with `m_csa:551`.
- Not a negative family: source evidence supports FAD/NADPH/O2 hydroxylation, not generic flavin redox, oxidase-only, Fe-S relay, heme/P450, pterin/metal/copper, or name-only chemistry.

Disposition: `source_boundary_hold`.

### `uniprot:P23262` salicylate 1-monooxygenase

- FAD/FMN: FAD, supported by UniProt and PMID:34965488/PMCID:PMC8824312.
- Reductive activation: single-component FAD/NADH monooxygenase; no partner reductase or reduced-FMN shuttle is required.
- O2 oxygen insertion: PMID:34965488 explicitly states that reduced flavin activates O2 and that salicylate undergoes oxidative decarboxylation by a C4a-hydroperoxyflavin intermediate to catechol.
- IDs: UniProt `P23262` reviewed; Rhea `RHEA:11004`; PDB `6BZ5`; AlphaFold `AF-P23262-F1` v6. RCSB nonpolymer entities retrieved for `6BZ5` did not include FAD, so do not use that coordinate as a holo-FAD claim from this pass.
- Duplicate risk: same-family aromatic hydroxylase overlap with `m_csa:131` and `m_csa:551`; low against `m_csa:132` and `m_csa:973`.
- Not a negative family: source evidence explicitly identifies FAD/NADH, O2 activation, C4a-hydroperoxyflavin, and substrate oxygenation/decarboxylation.

Disposition: `source_boundary_hold`.

## Source Systems

- UniProt REST: reviewed status, FAD cofactor, catalytic activities, Rhea/PDB/AlphaFold cross-references.
- Rhea: reaction IDs carried by UniProt catalytic activity records.
- RCSB PDB data API: public structure titles, resolutions, and checked ligands for OTEMO, KMO, and salicylate hydroxylase structures.
- AlphaFold DB API: model IDs and v6 model URLs for all six candidates.
- NCBI PubMed E-utilities and PMC: primary/open source evidence for FAD, NADPH/NADH, C4a/peroxyflavin, and substrate oxygenation.

## Next Action

Only `uniprot:P12015`, `uniprot:Q93TJ5`, and `uniprot:Q01740` should proceed to a later source-free geometry/review-packet run. Keep `uniprot:H3JQW0`, `uniprot:O15229`, and `uniprot:P23262` on source-boundary hold. Do not import labels or count any candidate from this artifact.
