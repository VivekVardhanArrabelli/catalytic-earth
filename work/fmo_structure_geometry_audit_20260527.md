# FMO structure geometry audit - 2026-05-27

Review-only audit using existing local candidate packets, geometry features, and materialized coordinates. No registry, label, threshold, ontology, PLM, or model-training changes were made.

The requested `artifacts/v3_fmo_mcsa_candidate_scout_702_20260527.json` file was not present locally; the audit used the two FMO acquisition packets, the packet3 closure, the foldseek readiness artifact, the existing geometry features, and the four local selected coordinates.

## Readout

| Entry | Selected structure | Local ligand evidence | Geometry support | Review need |
| --- | --- | --- | --- | --- |
| m_csa:551 (phenol 2-monooxygenase) | pdb:1FOH | FAD; substrate/analog IPH | supports FMO | yes |
| m_csa:973 (DszC protein) | pdb:3X0Y | FMN | ambiguous | yes |
| m_csa:141 (4-cresol dehydrogenase (hydroxylating)) | pdb:1DII | FAD; other HEC, CL | generic flavin redox | no |
| m_csa:128 (Photinus-luciferin 4-monooxygenase (ATP-hydrolysing)) | pdb:1BA3 | no flavin; other MBR | unavailable | no |

## Entry Notes

### m_csa:551 - phenol 2-monooxygenase
- Selected structure: `pdb:1FOH` at `artifacts/v3_foldseek_coordinates_1000/pdb_1FOH.cif`
- Active-site summary: Chain A: Asp54 electrostatic stabiliser; Arg281 electrostatic stabiliser; Tyr289 steric role; Pro364 activator/electrostatic stabiliser.
- Flavin reactive atom context: Mapped chain A FAD C4X is nearest to Pro364 CB at 4.87 A and Tyr289 OH at 4.99 A; mapped-chain phenol/IPH is 7.10 A from FAD C4X. Other asymmetric-unit copies in the same local coordinate show shorter FAD C4X to IPH distances of 4.58 to 4.65 A, but those copies are not the currently mapped M-CSA chain in the existing geometry artifact.
- Oxygenation/C4a proxy evidence: FAD and phenol/IPH are both proximal to the mapped active site in the existing geometry feature artifact (FAD min 4.318 A; IPH min 5.235 A). This gives structure-level cofactor plus substrate support for flavin monooxygenase chemistry, but the selected coordinate lacks a C4a-hydroperoxy state and the mapped-chain C4X-to-phenol distance needs visual review before any C4a claim.
- Geometry support: `supports_fmo`
- Blockers: No NADPH/NADP ligand is present in the selected coordinate.; No C4a-hydroperoxy/peroxide flavin state is present in the selected coordinate.; Mapped-chain FAD C4X to phenol/IPH nearest distance is 7.10 A; shorter ligand pose exists in other coordinate copies and needs structure review.

### m_csa:973 - DszC protein
- Selected structure: `pdb:3X0Y` at `artifacts/v3_foldseek_coordinates_1000/pdb_3X0Y.cif`
- Active-site summary: Chain A: His92 proton donor/acceptor; Tyr96 proton donor/acceptor; Asn129 hydrogen-bond acceptor; Ser163 proton donor/acceptor; His388 electrostatic stabiliser; His391 hydrogen-bond acceptor and proton donor/acceptor.
- Flavin reactive atom context: Mapped chain A FMN C4A is near Tyr96 OH at 3.37 A, Ser163 OG at 3.69 A, and His391 NE2 at 4.23 A; the selected coordinate contains no non-flavin substrate or analog near the FMN site.
- Oxygenation/C4a proxy evidence: FMN C4A has a plausible active-site residue cluster involving Tyr96, Ser163, and His391, which is compatible with an oxygenation pocket proxy. Because no substrate/analog, dioxygen, or C4a-peroxy state is present, the coordinate does not by itself distinguish FMO oxygenation from generic FMN redox.
- Geometry support: `ambiguous`
- Blockers: No substrate or substrate analog is present in the selected coordinate.; No NADPH/NADP ligand is present in the selected coordinate.; No C4a-hydroperoxy/peroxide flavin state is present in the selected coordinate.

### m_csa:141 - 4-cresol dehydrogenase (hydroxylating)
- Selected structure: `pdb:1DII` at `artifacts/v3_foldseek_coordinates_1000/pdb_1DII.cif`
- Active-site summary: Chains A/C: Ala49 and Met50 electron-relay/heme-side residues; Tyr367, Glu380, Tyr384, Asp167, Glu177, Glu286, His436, Tyr473, Arg474, and Arg512 form the flavoprotein-side acid/base and redox active-site set.
- Flavin reactive atom context: Mapped FAD C4X is nearest to Glu380 OE2 at 5.47 A and Arg474 NH1 at 5.70 A; the coordinate also contains a covalent Tyr384 OH to FAD C8M link reported at 1.357 A and proximal heme C/HEC support.
- Oxygenation/C4a proxy evidence: No substrate/analog or peroxyflavin state is present. The local structure is instead dominated by FAD plus heme C and a covalent FAD-Tyr redox linkage, which is structural support for flavin/heme electron-transfer chemistry rather than FMO oxygenation.
- Geometry support: `supports_generic_flavin_redox`
- Blockers: No substrate or substrate analog is present in the selected coordinate.; No C4a-hydroperoxy/peroxide flavin state is present in the selected coordinate.; Local coordinate contains FAD plus heme C and covalent FAD-Tyr linkage, favoring redox/electron-transfer interpretation.

### m_csa:128 - Photinus-luciferin 4-monooxygenase (ATP-hydrolysing)
- Selected structure: `pdb:1BA3` at `artifacts/v3_foldseek_coordinates_1000/pdb_1BA3.cif`
- Active-site summary: Chain A: Arg218, Thr343, Lys529, Thr343 duplicate role row, Lys443, and His245 are mapped as electrostatic or hydrogen-bonding residues for ATP/luciferin chemistry.
- Flavin reactive atom context: Unavailable: the selected coordinate contains no FAD/FMN/LLF-like flavin ligand.
- Oxygenation/C4a proxy evidence: Unavailable for flavin oxygenation: local coordinate has bromoform/MBR but no flavin cofactor and no C4a proxy atom.
- Geometry support: `unavailable`
- Blockers: No flavin ligand is present in the selected coordinate.; The local ligand MBR is bromoform, not a flavin monooxygenase substrate analog.; Candidate packet already marks this row not_FMO because the mechanism is ATP/luciferyl-adenylate oxygenation rather than flavin chemistry.

## Bottom Line

The strongest structure-level discriminator is `m_csa:551` because the local selected coordinate contains both FAD and phenol/IPH in the active-site context. `m_csa:973` remains FMO-compatible but structurally ambiguous without a substrate or peroxyflavin state. `m_csa:141` is structurally better explained as generic flavin/heme redox chemistry, and `m_csa:128` has no flavin geometry to audit.

Generated UTC: 2026-05-28T01:41:32Z
