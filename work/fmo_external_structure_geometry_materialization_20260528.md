# FMO External Structure Geometry Materialization - 2026-05-28

Run time: 2026-05-28T05:20:00Z

Review-only external structure/materialization pass for the six requested FMO candidates. No labels, registries, ontology files, thresholds, production scoring, model outputs, or imports were changed.

## Bottom Line

The minimum goal is not met: zero candidates are clean non-duplicate geometry-supported review rows under an exact-coordinate policy.

- No high-priority non-duplicate candidate has an exact experimental coordinate with both flavin and substrate/analog/product geometry.
- P12015, Q93TJ5, and Q01740 are non-duplicate/source-admissible leads but exact coordinates available in this pass are AlphaFold protein-only models with no ligand geometry.
- H3JQW0 and O15229 have exact FAD-bearing PDB coordinates, but both are duplicate/family holds under prior terminal evidence; neither can become a clean non-duplicate review row in this pass.
- P23262 has an exact PDB coordinate, but it is apo/no-flavin for this geometry pass and also overlaps the aromatic hydroxylase lane represented by m_csa:131/m_csa:551.

## Candidate Table

| Priority | Candidate | Selected coordinate | Coordinate state | Flavin | Substrate/analog/product | Geometry clean | Duplicate/leakage result | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `uniprot:P12015` cyclohexanone monooxygenase | AlphaFold:AF-P12015-F1 | predicted_model_no_ligand | absent | absent | false | hard_negative_gate_pass | hold |
| 2 | `uniprot:H3JQW0` OTEMO | pdb:3UOY | flavin_only_holo | FAD | absent | false | duplicate_hold | hold |
| 3 | `uniprot:Q93TJ5` 4-hydroxyacetophenone monooxygenase | AlphaFold:AF-Q93TJ5-F1 | predicted_model_no_ligand | absent | absent | false | hard_negative_gate_pass | hold |
| 4 | `uniprot:Q01740` human FMO1 | AlphaFold:AF-Q01740-F1 | predicted_model_no_ligand | absent | absent | false | hard_negative_gate_pass | hold |
| 5 | `uniprot:O15229` kynurenine 3-monooxygenase | pdb:5X68 | flavin_only_holo | FAD | absent | false | duplicate_hold | hold |
| 6 | `uniprot:P23262` salicylate 1-monooxygenase | pdb:6BZ5 | apo_or_no_flavin | absent | absent | false | duplicate_hold | hold |

## Row Notes

### 1. `uniprot:P12015` cyclohexanone monooxygenase
- Source: AlphaFold:AF-P12015-F1 (AlphaFold); coordinate path `artifacts/v3_fmo_external_structure_coordinates_20260528/afdb_P12015.cif`; SHA256 `812a0a04f5019131efa223aa9df09b113d07a43004f3751c68d56524171c4d8e`.
- Provenance: https://alphafold.ebi.ac.uk/entry/P12015; coordinate URL: https://alphafold.ebi.ac.uk/files/AF-P12015-F1-model_v6.cif.
- Exact-coordinate status: UniProt P12015 had no exact PDB cross-reference in the 2026-05-28 API check; exact public coordinate selected was AlphaFold v6.
- Ligands: flavin absent; NAD(P) absent; substrate/analog/product absent; other nonwater none.
- Flavin state: absent.
- Active-site mapping: No ligand-centered pocket extracted; exact model has no FAD, NADP(H), substrate, analog, or product coordinates.
- Source-free geometry: no flavin reactive atom geometry measured from this coordinate.
- Geometry clean: false - Exact candidate coordinate is a predicted protein-only model, so source-free C4a/C4X/N5 and substrate geometry cannot be measured. Homologous ligand-bound CHMO PDBs exist but map to other UniProt accessions and were not used as exact P12015 evidence.
- Duplicate/leakage risk: m_csa:131 `no duplicate; CHMO is carbonyl Baeyer-Villiger oxygen insertion, not aromatic hydroxylation`; m_csa:132 `no duplicate; CHMO is FAD/NADPH BVMO, not FMN-linked alkanal monooxygenase`; m_csa:551 `no duplicate; CHMO is lactone-forming BVMO, not phenol aromatic hydroxylase`; m_csa:973 `no duplicate; CHMO is single-component FAD/NADPH BVMO, not two-component FMNH2 sulfur monooxygenase`; same-family `highest-priority BVMO representative; overlaps broadly with HAPMO and OTEMO as BVMO chemistry but not with current canonical/proposed FMO rows`.
- Decision: hold - no coordinate flavin ligand; exact coordinate is AlphaFold/predicted protein-only; no substrate/analog/product ligand in selected coordinate; no exact experimental PDB with bound flavin/substrate found in local+UniProt/RCSB cross-reference review.

### 2. `uniprot:H3JQW0` OTEMO
- Source: pdb:3UOY (PDB); coordinate path `artifacts/v3_fmo_external_structure_coordinates_20260528/pdb_3UOY.cif`; SHA256 `da10dc642948fec3a9350306ef1d2556c3fe534f1f0fa30fbf0c91a79b4e53e2`.
- Provenance: https://www.rcsb.org/structure/3UOY; coordinate URL: https://files.rcsb.org/download/3UOY.cif.
- Exact-coordinate status: Exact UniProt H3JQW0 PDB cross-reference; selected among 3UOY/3UOZ/3UP4/3UP5 NADP-containing structures because it has 2.00 A resolution.
- Ligands: flavin FAD; NAD(P) NAP; substrate/analog/product absent; other nonwater NA.
- Flavin state: oxidized_or_resting_FAD_no_reduced_or_peroxy_code_detected.
- Active-site mapping: Pocket extraction uses chain A FAD 551 reactive proxy C4X/N5 and source-free nearest-residue contacts: Trp48, Arg57, Leu58, Asp59, Thr60, Tyr65, Arg337.
- Source-free geometry: FAD A 551 has reactive atoms C4X, N5; C4 proxy to N5 distance 1.388 A.
  - C4X nearest protein contacts: ASP59:A OD1 4.126 A, TRP48:A CZ2 4.184 A, ARG337:A NH1 4.44 A, TYR65:A CE1 4.51 A; nearest nonwater nonflavin ligands: NAP 3.783 A, NA 29.58 A, FAD 42.065 A.
  - N5 nearest protein contacts: TRP48:A CH2 3.602 A, ASP59:A N 4.582 A, LEU58:A CA 4.637 A, ARG57:A O 4.694 A; nearest nonwater nonflavin ligands: NAP 2.905 A, NA 28.529 A, FAD 43.427 A.
- Geometry clean: false - Flavin/NADP site geometry is resolved, but the coordinate lacks substrate/analog/product and remains a duplicate/family hold from prior terminal evidence; peroxy absence is retained only as a coordinate-state caveat.
- Duplicate/leakage risk: m_csa:131 `no direct chemistry duplicate; OTEMO is BVMO oxygen insertion rather than aromatic hydroxylation`; m_csa:132 `no direct chemistry duplicate; OTEMO is FAD/NADPH BVMO rather than FMN-linked alkanal monooxygenase`; m_csa:551 `no direct chemistry duplicate; OTEMO is BVMO rather than phenol hydroxylase`; m_csa:973 `no direct chemistry duplicate; OTEMO is not two-component sulfur monooxygenase`; same-family `same broad BVMO lane as P12015 and Q93TJ5; lower priority than P12015 for non-duplicate acquisition diversity`.
- Decision: hold - no substrate/analog/product ligand in selected coordinate; duplicate/family hold from prior gate.

### 3. `uniprot:Q93TJ5` 4-hydroxyacetophenone monooxygenase
- Source: AlphaFold:AF-Q93TJ5-F1 (AlphaFold); coordinate path `artifacts/v3_fmo_external_structure_coordinates_20260528/afdb_Q93TJ5.cif`; SHA256 `63f93156234cb2734c39106fa45467b81312008b4dff7d4e4c403525507ad63f`.
- Provenance: https://alphafold.ebi.ac.uk/entry/Q93TJ5; coordinate URL: https://alphafold.ebi.ac.uk/files/AF-Q93TJ5-F1-model_v6.cif.
- Exact-coordinate status: UniProt Q93TJ5 had no exact PDB cross-reference in the 2026-05-28 API check; misleading RCSB full-text hit 2GQ8 maps to Q8EEC8 OYE/FMNH2 oxidoreductase and was not selected.
- Ligands: flavin absent; NAD(P) absent; substrate/analog/product absent; other nonwater none.
- Flavin state: absent.
- Active-site mapping: No ligand-centered pocket extracted; exact model has no FAD, NADP(H), 4-hydroxyacetophenone, analog, or product coordinates.
- Source-free geometry: no flavin reactive atom geometry measured from this coordinate.
- Geometry clean: false - Exact candidate coordinate is a predicted protein-only model, so source-free C4a/C4X/N5 and substrate geometry cannot be measured.
- Duplicate/leakage risk: m_csa:131 `no duplicate; HAPMO is aryl ketone Baeyer-Villiger oxygen insertion, not aromatic ring hydroxylation`; m_csa:132 `no duplicate; HAPMO is FAD/NADPH BVMO, not FMN-linked alkanal monooxygenase`; m_csa:551 `no duplicate; HAPMO is carbonyl oxygen insertion, not phenol ortho hydroxylation`; m_csa:973 `no duplicate; HAPMO is not two-component sulfur monooxygenase`; same-family `same broad BVMO class as P12015, but a distinct aryl-ketone/HAPMO substrate lane; should not be counted as a separate diversity axis from BVMO by itself`.
- Decision: hold - no coordinate flavin ligand; exact coordinate is AlphaFold/predicted protein-only; no substrate/analog/product ligand in selected coordinate; no exact experimental PDB with bound flavin/substrate found in local+UniProt/RCSB cross-reference review.

### 4. `uniprot:Q01740` human FMO1
- Source: AlphaFold:AF-Q01740-F1 (AlphaFold); coordinate path `artifacts/v3_fmo_external_structure_coordinates_20260528/afdb_Q01740.cif`; SHA256 `0e1152bc44e76ebfb5f3fc25133569908b5f669cc13939c05fe25ad39ec402b9`.
- Provenance: https://alphafold.ebi.ac.uk/entry/Q01740; coordinate URL: https://alphafold.ebi.ac.uk/files/AF-Q01740-F1-model_v6.cif.
- Exact-coordinate status: UniProt Q01740 had no exact PDB cross-reference in the 2026-05-28 API check; RCSB text hits were other human monooxygenase families and were not selected.
- Ligands: flavin absent; NAD(P) absent; substrate/analog/product absent; other nonwater none.
- Flavin state: absent.
- Active-site mapping: No ligand-centered pocket extracted; exact model has no FAD, NADP(H), dimethylaniline/trimethylamine, analog, or product coordinates.
- Source-free geometry: no flavin reactive atom geometry measured from this coordinate.
- Geometry clean: false - Exact candidate coordinate is a predicted protein-only model, so source-free C4a/C4X/N5 and substrate geometry cannot be measured.
- Duplicate/leakage risk: m_csa:131 `no duplicate; FMO1 N/S oxygenation is distinct from aromatic hydroxylation`; m_csa:132 `no duplicate; FMO1 is class B FAD/NADPH xenobiotic FMO rather than FMN-linked alkanal monooxygenase`; m_csa:551 `no duplicate; FMO1 is not phenol aromatic hydroxylase`; m_csa:973 `partial chemistry overlap in sulfur oxygenation, but not duplicate: FMO1 is single-chain class B FAD/NADPH N/S oxygenation, while DszC is two-component FMNH2 sulfur monooxygenase`; same-family `unique class B mammalian FMO lane among current external candidates`.
- Decision: hold - no coordinate flavin ligand; exact coordinate is AlphaFold/predicted protein-only; no substrate/analog/product ligand in selected coordinate; no exact experimental PDB with bound flavin/substrate found in local+UniProt/RCSB cross-reference review.

### 5. `uniprot:O15229` kynurenine 3-monooxygenase
- Source: pdb:5X68 (PDB); coordinate path `artifacts/v3_fmo_external_structure_coordinates_20260528/pdb_5X68.cif`; SHA256 `ca83c13ce16a520d69f25b1d38f9f312ec38fe7e24d590f60c3ffd376923d2d2`.
- Provenance: https://www.rcsb.org/structure/5X68; coordinate URL: https://files.rcsb.org/download/5X68.cif.
- Exact-coordinate status: Exact UniProt O15229 PDB cross-reference; selected because it is the exact human KMO PDB cross-reference at 2.10 A.
- Ligands: flavin FAD; NAD(P) absent; substrate/analog/product absent; other nonwater none.
- Flavin state: oxidized_or_resting_FAD_no_reduced_or_peroxy_code_detected.
- Active-site mapping: Pocket extraction uses chain A FAD 401 reactive proxy C4X/N5 and source-free nearest-residue contacts: Ser53, Asn55, Leu56, Ala57, Arg111, Pro311, Gln315, Gly316, Met317.
- Source-free geometry: FAD A 401 has reactive atoms C4X, N5; C4 proxy to N5 distance 1.306 A.
  - C4X nearest protein contacts: LEU56:A CD2 3.595 A, ALA57:A N 4.804 A, GLN315:A NE2 4.929 A, GLY316:A N 5.122 A; nearest nonwater nonflavin ligands: FAD 27.644 A.
  - N5 nearest protein contacts: LEU56:A CD2 4.204 A, ASN55:A O 4.658 A, PRO311:A CG 4.658 A, SER53:A OG 4.87 A; nearest nonwater nonflavin ligands: FAD 27.932 A.
- Geometry clean: false - FAD site geometry is resolved, but the coordinate lacks substrate/analog/product and prior terminal evidence marks KMO as duplicate/leakage against m_csa:131; peroxy and NADPH absence are retained as coordinate-state caveats, not sole blockers.
- Duplicate/leakage risk: m_csa:131 `strong duplicate/leakage risk: prior targeted current-FMO rescue screen found high-TM structural hit to pdb:1DOC / m_csa:131`; m_csa:132 `no meaningful structural overlap in prior current-FMO rescue screen`; m_csa:551 `family overlap: KMO and phenol 2-monooxygenase both support FAD/NAD(P)H aromatic hydroxylation-like FMO chemistry`; m_csa:973 `no duplicate; KMO aromatic hydroxylation is distinct from two-component sulfur monooxygenation`; same-family `same broad aromatic hydroxylase source lane as P23262 and current m_csa:131/m_csa:551 support`.
- Decision: hold - no substrate/analog/product ligand in selected coordinate; duplicate/family hold from prior gate; prior high-TM duplicate/leakage against m_csa:131.

### 6. `uniprot:P23262` salicylate 1-monooxygenase
- Source: pdb:6BZ5 (PDB); coordinate path `artifacts/v3_fmo_external_structure_coordinates_20260528/pdb_6BZ5.cif`; SHA256 `50d395af45c32afdd07713a1998663d5cb821381a2e234bacf2c8045acbc74c4`.
- Provenance: https://www.rcsb.org/structure/6BZ5; coordinate URL: https://files.rcsb.org/download/6BZ5.cif.
- Exact-coordinate status: Exact UniProt P23262 PDB cross-reference; selected exact coordinate has no FAD/FMN despite source evidence for FAD-dependent catalysis.
- Ligands: flavin absent; NAD(P) absent; substrate/analog/product absent; other nonwater EDO, GOL, IOD, SO4.
- Flavin state: absent.
- Active-site mapping: No flavin-centered pocket extracted; exact PDB contains buffer/ion ligands but no FAD/FMN and no salicylate/catechol ligand.
- Source-free geometry: no flavin reactive atom geometry measured from this coordinate.
- Geometry clean: false - Exact coordinate lacks flavin and substrate/product ligands, so C4a/C4X/N5 geometry cannot be measured; same-family aromatic hydroxylase overlap with m_csa:131/m_csa:551 remains a duplicate-risk blocker.
- Duplicate/leakage risk: m_csa:131 `family overlap: both are FAD-dependent aromatic hydroxylase/decarboxylating hydroxylase-like rows using reduced flavin plus O2`; m_csa:132 `no duplicate; salicylate 1-monooxygenase is FAD/NADH aromatic hydroxylation/decarboxylation, not FMN alkanal monooxygenase`; m_csa:551 `family overlap: both support FAD-dependent phenolic/aromatic hydroxylation through C4a-hydroperoxyflavin chemistry`; m_csa:973 `no duplicate; salicylate hydroxylation/decarboxylation is distinct from two-component sulfur oxygenation`; same-family `same broad aromatic hydroxylase lane as O15229 and current m_csa:131/m_csa:551 support`.
- Decision: hold - no coordinate flavin ligand; no substrate/analog/product ligand in selected coordinate; duplicate/family hold from prior gate; same-family aromatic hydroxylase overlap with m_csa:131/m_csa:551.

## Guardrail

This artifact is materialization and geometry support only. It does not promote candidates, import labels, edit registries/ontology files, change thresholds, change production scoring, change model outputs, or add imports.
