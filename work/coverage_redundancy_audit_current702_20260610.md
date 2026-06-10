# Coverage + Redundancy Audit And Balance-Capped Acquisition Policy

Run: 2026-06-10T03:55:40Z

Non-destructive, metadata-only audit of all combined labels (2412 = 702 frozen current702 + 1710 expansion bronze). No registry is written and no label is emitted. Redundancy is measured from annotation metadata only (no mmseqs / no embeddings / no network).

## Class balance (seed fingerprints, combined)

- Seed positives: 716; out_of_scope: 1696; positive:OOS = 0.4222.
- Fingerprint Gini 0.5119 / normalized entropy 0.781; max/min(nonzero) ratio 30.8 (308 vs 10).
- Below floor: ['cobalamin_radical_rearrangement', 'flavin_dehydrogenase_reductase', 'flavin_monooxygenase', 'heme_peroxidase_oxidase', 'radical_sam_enzyme', 'ser_his_acid_hydrolase'].
- Above cap: ['metal_dependent_hydrolase'].
- Absent from expansion (holes): ['ser_his_acid_hydrolase'].

| Fingerprint | frozen | expansion | combined | distinct rxn | labels/rxn |
| --- | --- | --- | --- | --- | --- |
| metal_dependent_hydrolase | 83 | 225 | 308 | 76 | 2.96 |
| ser_his_acid_hydrolase | 42 | 0 | 42 | 0 | None |
| plp_dependent_enzyme | 31 | 116 | 147 | 146 | 0.79 |
| heme_peroxidase_oxidase | 20 | 49 | 69 | 20 | 2.45 |
| flavin_monooxygenase | 2 | 41 | 43 | 30 | 1.37 |
| flavin_dehydrogenase_reductase | 48 | 39 | 87 | 77 | 0.51 |
| radical_sam_enzyme | 1 | 9 | 10 | 12 | 0.75 |
| cobalamin_radical_rearrangement | 3 | 7 | 10 | 8 | 0.88 |

## Near-duplicate / saturation read (metadata proxy)

- Cluster key: (fingerprint_or_scope, full_ec, organism, sequence_length_bin).
- Measurable rows: 1558; clusters (size >= 3): 54; rows in clusters: 254 (0.163 of measurable).
- Top redundancy clusters (same enzyme/organism/length, near-dup orthologs):

| size | scope | full EC | organism | len bin |
| --- | --- | --- | --- | --- |
| 17 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0400-0499 |
| 13 | heme_peroxidase_oxidase | 1.11.1.7 | Arabidopsis thaliana (Mouse-ear cress) | 0300-0399 |
| 13 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0700-0799 |
| 10 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0300-0399 |
| 9 | out_of_scope | 3.1.3.16 | Homo sapiens (Human) | 0300-0399 |
| 9 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0500-0599 |
| 8 | metal_dependent_hydrolase | 3.4.24.- | Homo sapiens (Human) | 0700-0799 |
| 8 | out_of_scope | 2.7.10.1 | Homo sapiens (Human) | 0900-0999 |
| 7 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0600-0699 |
| 7 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 1200-1299 |
| 5 | metal_dependent_hydrolase | 3.5.2.6 | Elizabethkingia meningoseptica (Chryseobacterium meningosepticum) | 0200-0299 |
| 5 | out_of_scope | 3.1.3.16,3.1.3.48 | Homo sapiens (Human) | 0300-0399 |

## Prioritized, balance-capped acquisition targets

Close HOLES first (esp. fingerprints absent from the expansion), then raise UNDER-floor fingerprints, while CAPPING over-supplied ones and deduplicating them toward distinct reactions. Pause broad out_of_scope draining (kinase/phosphatase/glycoside lanes are already saturated) until the positive holes are closed -- the binding constraint is diverse positive supply, not raw count.

- Holes: ['cobalamin_radical_rearrangement', 'radical_sam_enzyme', 'ser_his_acid_hydrolase'].
- Under floor: ['flavin_monooxygenase', 'heme_peroxidase_oxidase', 'flavin_dehydrogenase_reductase'].
- Over cap: ['metal_dependent_hydrolase'].
- Total deficit to floor (next-batch positive target): 339.

| # | fingerprint | status | combined | deficit | surplus | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | cobalamin_radical_rearrangement | HOLE | 10 | 90 | 0 | SOURCE ~90 more seed labels to reach the 100 floor |
| 2 | radical_sam_enzyme | HOLE | 10 | 90 | 0 | SOURCE ~90 more seed labels to reach the 100 floor |
| 3 | ser_his_acid_hydrolase | HOLE | 42 | 58 | 0 | SOURCE ~58 more seed labels to reach the 100 floor |
| 4 | flavin_monooxygenase | UNDER | 43 | 57 | 0 | SOURCE ~57 more seed labels to reach the 100 floor |
| 5 | heme_peroxidase_oxidase | UNDER | 69 | 31 | 0 | SOURCE ~31 more seed labels to reach the 100 floor |
| 6 | flavin_dehydrogenase_reductase | UNDER | 87 | 13 | 0 | SOURCE ~13 more seed labels to reach the 100 floor |
| 7 | metal_dependent_hydrolase | OVER_CAP | 308 | 0 | 58 | CAP / PAUSE -- 58 over the 250 ceiling; dedup toward distinct reactions before adding any |
| 8 | plp_dependent_enzyme | BALANCED | 147 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |

### Sourcing hints per fingerprint (coverage accounting only, never predictive)

| fingerprint | EC prefixes | cofactor signature | lanes |
| --- | --- | --- | --- |
| cobalamin_radical_rearrangement | 5.4.99, 5.4.3, 4.2.1.28, 4.2.1.30, 4.3.1.7 | adenosylcobalamin / vitamin B12 (radical rearrangement) | cobalamin radical, plp_radical_cobalamin |
| radical_sam_enzyme | 1.97.1, 2.8.4, 4.1.99, 2.5.1 | [4Fe-4S] + S-adenosylmethionine (CX3CX2C motif) | radical SAM, plp_radical_cobalamin |
| ser_his_acid_hydrolase | 3.4.21, 3.1.1, 3.5.1 | no cofactor; Ser/Cys-His-Asp/Glu catalytic triad | serine/cysteine hydrolase, esterase/lipase triad |
| flavin_monooxygenase | 1.14.13, 1.14.14 | flavin (FAD/FMN), no heme; inserts one O | flavin monooxygenase |
| heme_peroxidase_oxidase | 1.11.1 | heme b / heme c (peroxidase) | heme peroxidase/oxidase-like |
| flavin_dehydrogenase_reductase | 1.3, 1.6, 1.8.1 | flavin (FAD/FMN), no heme; hydride/electron transfer | flavin redox boundary, flavin dehydrogenase/reductase |
| metal_dependent_hydrolase | 3.4.24, 3.5.2, 3.1.3, 3.1.4 | catalytic divalent metal (Zn2+/Mn2+/Mg2+/Ni2+) | metal hydrolase |
| plp_dependent_enzyme | 2.6.1, 4.1.1, 4.3.1, 5.1.1, 4.4.1 | pyridoxal-5'-phosphate (PLP) Schiff base | PLP lyase/eliminase, PLP decarboxylase, PLP aminotransferase, PLP racemase/epimerase, PLP sulfur lyase boundary |

## Guardrails

- Frozen benchmark written: False.
- Expansion registry written: False.
- Labels emitted: 0.
- EC/lane/organism used for coverage accounting only, never predictive.
- Metadata-only: no network, no mmseqs, no embedding backend.
