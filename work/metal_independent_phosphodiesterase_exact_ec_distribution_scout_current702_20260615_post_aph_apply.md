# Metal-independent PDE Exact-EC Distribution Scout

Run: 2026-06-15 automation `ce-nad-glyco-floor-expansion`

## Result

This is a non-destructive source-count scout. It wrote no registry rows, created no labels, and
does not count EC as mechanism evidence.

The broad reviewed EC 3.1.4 surface is not an apply-ready PDE supply source. A cursor sample of
`(reviewed:true) AND (ec:3.1.4.*)` fetched 1086 records and was dominated by generic `3.1.4.-`,
phospholipase/phosphodiesterase boundary rows, sphingomyelinases, ENPP/pyrophosphatases, and small
exact cyclic-nucleotide subfamilies.

Top exact EC counts in the reviewed EC 3.1.4 sample:

| EC | count | interpretation |
| --- | ---: | --- |
| 3.1.4.- | 570 | generic/boundary-heavy; not a source wall |
| 3.1.4.11 | 67 | phosphoinositide phospholipase C boundary |
| 3.1.4.4 | 58 | phospholipase D boundary |
| 3.1.4.35 | 55 | cGMP-specific PDE subfamily, small after non-metal filter |
| 3.1.4.14 | 51 | acyl-carrier-protein phosphodiesterase boundary |
| 3.1.4.53 | 44 | cAMP-specific PDE subfamily, small after non-metal filter |
| 3.1.4.17 | 39 | cyclic-nucleotide PDE, small after non-metal filter |
| 3.1.4.12 | 36 | sphingomyelin phosphodiesterase boundary |
| 3.1.4.52 | 23 | cyclic-di-GMP PDE, subscale |
| 3.1.4.37 | 15 | 2',3'-cyclic-nucleotide phosphodiesterase, subscale |
| 3.1.4.58 | 12 | RNA 2',3'-cyclic phosphodiesterase, subscale |

Candidate split counts after the current non-metal filter:

| candidate split | reviewed count |
| --- | ---: |
| broad EC 3.1.4 reviewed | 1086 |
| broad EC 3.1.4 non-metal | 490 |
| EC 3.1.4.17 cyclic-nucleotide PDE non-metal | 6 |
| EC 3.1.4.35 cGMP PDE non-metal | 7 |
| EC 3.1.4.53 cAMP PDE non-metal | 2 |
| EC 3.1.4.52 cyclic-di-GMP PDE non-metal | 18 |
| EC 3.1.4.59 cyclic-di-AMP PDE non-metal | 0 |
| EC 3.1.4.37 CNPase non-metal | 15 |
| EC 3.1.4.58 RNA 2',3'-cyclic PDE non-metal | 12 |
| protein_name cyclic nucleotide phosphodiesterase non-metal | 8 |
| protein_name cyclic phosphodiesterase non-metal | 44 |
| protein_name phosphodiesterase excluding phospholipase non-metal | 178 |

## Interpretation

The exact cyclic-nucleotide EC splits are too small for a 150-row clean batch. The broader name/EC
windows are larger but boundary-heavy and already failed the reviewed/tier-2 preview gates. Do not
retry the same PDE source handles as a mass-growth path.

## Next Action

A safe PDE mutation now requires a new mechanism-bearing source wall beyond EC/name counts, or the
automation should pivot to a different high-yield family/source-tier strategy. Any future PDE scout
should explicitly separate cyclic-nucleotide PDE, 2',3'-cyclic-nucleotide PDE, ACP/phospholipase
boundaries, sphingomyelinase boundaries, ENPP/nucleotide pyrophosphatase rows, and metal-dependent
metallophosphoesterase/nuclease rows before previewing labels.
