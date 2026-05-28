# FMO structure geometry audit - 2026-05-27

Review-only audit using existing local candidate packets, geometry features, cofactor coverage artifacts, and materialized coordinates. No registry, label, threshold, ontology, PLM, model-output, or training changes were made.

The candidate scout artifact is now present and was inspected alongside the acquisition packet/closure and packet3 closure. The detailed rows below keep the acquisition-packet candidates and add the scout's closest flavin redox/halogenase boundary controls needed to distinguish FMO oxygenation from generic flavin redox chemistry.

## Readout

| Entry | Selected structure | Local ligand evidence | Geometry support | Review need |
| --- | --- | --- | --- | --- |
| m_csa:551 (phenol 2-monooxygenase) | pdb:1FOH | FAD; substrate/analog IPH | supports FMO | yes |
| m_csa:973 (DszC protein) | pdb:3X0Y | FMN | ambiguous | yes |
| m_csa:141 (4-cresol dehydrogenase (hydroxylating)) | pdb:1DII | FAD; HEC, CL | supports generic flavin redox | no |
| m_csa:109 (dihydroorotate oxidase (class II)) | pdb:1D3G | FMN; ORO/product-state redox ligand | supports generic flavin redox | no |
| m_csa:978 (D-arginine dehydrogenase) | pdb:3NYE | FAD; IAR substrate/imino analog | supports generic flavin redox | no |
| m_csa:977 (tryptophan 7-halogenase) | pdb:2AR8 | FAD/CTE in selected-PDB artifact; local coordinate absent | unavailable | yes |
| m_csa:128 (Photinus-luciferin 4-monooxygenase (ATP-hydrolysing)) | pdb:1BA3 | no flavin; MBR only | unavailable | no |

## Entry Notes

### m_csa:551 - phenol 2-monooxygenase
- Selected structure: `pdb:1FOH` at `artifacts/v3_foldseek_coordinates_1000/pdb_1FOH.cif`
- Active-site summary: Chain A: Asp54 electrostatic stabiliser; Arg281 electrostatic stabiliser; Tyr289 steric role; Pro364 activator/electrostatic stabiliser.
- Flavin reactive atom context: Mapped chain A FAD C4X is nearest to Pro364 CB at 4.87 A and Tyr289 OH at 4.99 A; mapped-chain phenol/IPH is 7.10 A from FAD C4X. Other asymmetric-unit copies in the same local coordinate show shorter FAD C4X to IPH distances of 4.58 to 4.65 A, but those copies are not the currently mapped M-CSA chain in the existing geometry artifact.
- Oxygenation/C4a proxy evidence: FAD and phenol/IPH are both proximal to the mapped active site in the existing geometry feature artifact (FAD min 4.318 A; IPH min 5.235 A). This supports FMO-like cofactor plus substrate context, but the selected coordinate lacks a C4a-hydroperoxy state and needs visual review before any C4a claim.
- Geometry support: `supports_fmo`
- Blockers: No NADPH/NADP ligand is present; no C4a-hydroperoxy/peroxide flavin state is present; mapped-chain FAD C4X to phenol/IPH nearest distance is 7.10 A.

### m_csa:973 - DszC protein
- Selected structure: `pdb:3X0Y` at `artifacts/v3_foldseek_coordinates_1000/pdb_3X0Y.cif`
- Active-site summary: Chain A: His92, Tyr96, Asn129, Ser163, His388, and His391 form the mapped proton-transfer/hydrogen-bonding residue set.
- Flavin reactive atom context: Mapped chain A FMN C4A is near Tyr96 OH at 3.37 A, Ser163 OG at 3.69 A, and His391 NE2 at 4.23 A; the selected coordinate contains no non-flavin substrate or analog near the FMN site.
- Oxygenation/C4a proxy evidence: FMN C4A has an FMO-compatible residue cluster, but no substrate/analog, dioxygen, or C4a-peroxy state is present.
- Geometry support: `ambiguous`
- Blockers: No substrate/analog; no NADPH/NADP ligand; no C4a-hydroperoxy/peroxide flavin state.

### m_csa:141 - 4-cresol dehydrogenase (hydroxylating)
- Selected structure: `pdb:1DII` at `artifacts/v3_foldseek_coordinates_1000/pdb_1DII.cif`
- Active-site summary: Chains A/C include Ala49/Met50 heme-side electron relay residues and Tyr367, Glu380, Tyr384, Asp167, Glu177, Glu286, His436, Tyr473, Arg474, and Arg512 around the flavoprotein-side redox site.
- Flavin reactive atom context: Mapped FAD C4X is nearest to Glu380 OE2 at 5.47 A and Arg474 NH1 at 5.70 A; the coordinate also contains a covalent Tyr384 OH to FAD C8M link and proximal heme C/HEC support.
- Oxygenation/C4a proxy evidence: No substrate/analog or peroxyflavin state is present; FAD plus heme C and the covalent FAD-Tyr linkage support electron-transfer/redox chemistry instead.
- Geometry support: `supports_generic_flavin_redox`
- Blockers: No substrate/analog; no C4a-hydroperoxy/peroxide flavin state; FAD/heme/covalent-FAD context favors redox interpretation.

### m_csa:109 - dihydroorotate oxidase (class II)
- Selected structure: `pdb:1D3G` at `artifacts/v3_foldseek_coordinates_1000/pdb_1D3G.cif`
- Active-site summary: Chain A: Asn255, Asn188, Asn116, Thr189, Phe120, Lys226, and Ser186 form the mapped electrostatic/hydrogen-bonding redox site.
- Flavin reactive atom context: FMN C4A is 3.38 A from ORO C4 and 3.50 A from ORO C5; FMN N5 is 3.64 A from ORO C6 and 3.71 A from ORO N1, with nearest matched active-site contacts from Asn255, Lys226, Asn116, and Phe120.
- Oxygenation/C4a proxy evidence: No peroxyflavin/O2 state is present; the geometry is substrate/product-to-FMN redox geometry.
- Geometry support: `supports_generic_flavin_redox`
- Blockers: No C4a-hydroperoxy/peroxide flavin state; ORO/product-state context supports oxidase/dehydrogenase chemistry; no NADPH/NADP ligand.

### m_csa:978 - D-arginine dehydrogenase
- Selected structure: `pdb:3NYE` at `artifacts/v3_foldseek_coordinates_1000/pdb_3NYE.cif`
- Active-site summary: Chain A: Tyr59, Tyr255, Glu93, His54, Ser51, and Ala52 form the mapped transition-state/electrostatic/steric residue set.
- Flavin reactive atom context: FAD C4X is 3.16 A from IAR N and FAD N5 is 2.97 A from IAR C/O, placing the imino-arginine analog directly against the flavin redox face.
- Oxygenation/C4a proxy evidence: No oxygenation pocket, O2/peroxide ligand, or hydroperoxyflavin state is present; the local coordinate supports dehydrogenase/redox or covalent-adduct boundary chemistry, not monooxygenase oxygen atom transfer.
- Geometry support: `supports_generic_flavin_redox`
- Blockers: No C4a-hydroperoxy/peroxide flavin state; substrate analog pose is redox/adduct-like; no NADPH/NADP ligand.

### m_csa:977 - tryptophan 7-halogenase
- Selected structure: `pdb:2AR8`; local coordinate file is absent from `artifacts/v3_foldseek_coordinates_1000`.
- Active-site summary: Chain A: Lys79 activator/hydrogen-bond donor/proton donor; Glu346 proton acceptor.
- Flavin reactive atom context: Not computable from local coordinates. The selected-PDB geometry artifact reports FAD/CTE/CL, with CTE proximal to the active-site residues and FAD outside the 6 A proximal-ligand cutoff.
- Oxygenation/C4a proxy evidence: Review-only source context supports flavin halogenase chemistry, not tryptophan monooxygenation.
- Geometry support: `unavailable`
- Blockers: Local coordinate absent; candidate scout marks blocked wrong chemistry; no local C4a/peroxide geometry can be reviewed.

### m_csa:128 - Photinus-luciferin 4-monooxygenase (ATP-hydrolysing)
- Selected structure: `pdb:1BA3` at `artifacts/v3_foldseek_coordinates_1000/pdb_1BA3.cif`
- Active-site summary: Chain A: Arg218, Thr343, Lys529, Thr343 duplicate role row, Lys443, and His245 are mapped as electrostatic or hydrogen-bonding residues for ATP/luciferin chemistry.
- Flavin reactive atom context: Unavailable: the selected coordinate contains no FAD/FMN/LLF-like flavin ligand.
- Oxygenation/C4a proxy evidence: Unavailable for flavin oxygenation; local coordinate has bromoform/MBR but no flavin cofactor and no C4a proxy atom.
- Geometry support: `unavailable`
- Blockers: No flavin ligand; MBR is bromoform, not a flavin monooxygenase substrate analog; candidate packet marks the row not_FMO.

## Bottom Line

`m_csa:551` is the strongest local structure-level FMO support because FAD and phenol/IPH are both present in the active-site context. `m_csa:973` is FMO-compatible but ambiguous without substrate/analog or peroxyflavin state. The added scout boundary rows (`m_csa:109`, `m_csa:141`, `m_csa:978`) show local flavin geometry consistent with generic redox chemistry, not C4a-peroxy oxygenation. `m_csa:977` and `m_csa:128` remain review/blocker rows, not FMO support.

Generated UTC: 2026-05-28T02:45:17Z
