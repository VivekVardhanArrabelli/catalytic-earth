# Coverage + Redundancy Audit And Balance-Capped Acquisition Policy

Run: 2026-06-13T00:30:14Z

Non-destructive, metadata-only audit of all combined labels (4574 = 702 frozen current702 + 3872 expansion bronze). No registry is written and no label is emitted. Redundancy is measured from annotation metadata only (no mmseqs / no embeddings / no network).

## Class balance (seed fingerprints, combined)

- Seed positives: 2596; out_of_scope: 1696; positive:OOS = 1.5307.
- Fingerprint Gini 0.1657 / normalized entropy 0.9813; max/min(nonzero) ratio 2.66 (308 vs 116).
- Below floor: [].
- Above cap: ['metal_dependent_hydrolase'].
- Absent from expansion (holes): [].

| Fingerprint | frozen | expansion | combined | distinct rxn | labels/rxn |
| --- | --- | --- | --- | --- | --- |
| metal_dependent_hydrolase | 83 | 225 | 308 | 76 | 2.96 |
| metallopeptidase | 0 | 150 | 150 | 27 | 5.56 |
| metallophosphoesterase_nuclease | 0 | 150 | 150 | 52 | 2.88 |
| metallophosphomonoesterase | 0 | 150 | 150 | 120 | 1.25 |
| metallo_amidohydrolase_deaminase | 0 | 150 | 150 | 57 | 2.63 |
| ser_his_acid_hydrolase | 42 | 87 | 129 | 205 | 0.42 |
| plp_dependent_enzyme | 31 | 116 | 147 | 146 | 0.79 |
| heme_peroxidase_oxidase | 20 | 99 | 119 | 26 | 3.81 |
| flavin_monooxygenase | 2 | 114 | 116 | 65 | 1.75 |
| flavin_dehydrogenase_reductase | 48 | 202 | 250 | 206 | 0.98 |
| radical_sam_enzyme | 1 | 132 | 133 | 23 | 5.74 |
| cobalamin_radical_rearrangement | 3 | 141 | 144 | 15 | 9.4 |
| nad_p_dehydrogenase | 0 | 150 | 150 | 88 | 1.7 |
| glycosyltransferase | 0 | 250 | 250 | 394 | 0.63 |
| sam_methyltransferase | 0 | 250 | 250 | 129 | 1.94 |

## Near-duplicate / saturation read (metadata proxy)

- Cluster key: (fingerprint_or_scope, full_ec, organism, sequence_length_bin).
- Measurable rows: 3718; clusters (size >= 3): 97; rows in clusters: 407 (0.1095 of measurable).
- Top redundancy clusters (same enzyme/organism/length, near-dup orthologs):

| size | scope | full EC | organism | len bin |
| --- | --- | --- | --- | --- |
| 17 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0400-0499 |
| 13 | heme_peroxidase_oxidase | 1.11.1.7 | Arabidopsis thaliana (Mouse-ear cress) | 0300-0399 |
| 13 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0700-0799 |
| 11 | glycosyltransferase | 2.4.1.17 | Homo sapiens (Human) | 0500-0599 |
| 10 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0300-0399 |
| 9 | out_of_scope | 3.1.3.16 | Homo sapiens (Human) | 0300-0399 |
| 9 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0500-0599 |
| 8 | metal_dependent_hydrolase | 3.4.24.- | Homo sapiens (Human) | 0700-0799 |
| 8 | out_of_scope | 2.7.10.1 | Homo sapiens (Human) | 0900-0999 |
| 8 | sam_methyltransferase | 2.1.1.- | Homo sapiens (Human) | 0300-0399 |
| 7 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 0600-0699 |
| 7 | out_of_scope | 2.7.11.1 | Homo sapiens (Human) | 1200-1299 |

## Prioritized, balance-capped acquisition targets

Close HOLES first (esp. fingerprints absent from the expansion), then raise UNDER-floor fingerprints, while CAPPING over-supplied ones and deduplicating them toward distinct reactions. Pause broad out_of_scope draining (kinase/phosphatase/glycoside lanes are already saturated) until the positive holes are closed -- the binding constraint is diverse positive supply, not raw count.

- Holes: [].
- Under floor: [].
- Over cap: ['metal_dependent_hydrolase'].
- Total deficit to floor (next-batch positive target): 0.

| # | fingerprint | status | combined | deficit | surplus | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | metal_dependent_hydrolase | OVER_CAP | 308 | 0 | 58 | CAP / PAUSE -- 58 over the 250 ceiling; dedup toward distinct reactions before adding any |
| 2 | cobalamin_radical_rearrangement | BALANCED | 144 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 3 | flavin_dehydrogenase_reductase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 4 | flavin_monooxygenase | BALANCED | 116 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 5 | glycosyltransferase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 6 | heme_peroxidase_oxidase | BALANCED | 119 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 7 | metallo_amidohydrolase_deaminase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 8 | metallopeptidase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 9 | metallophosphoesterase_nuclease | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 10 | metallophosphomonoesterase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 11 | nad_p_dehydrogenase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 12 | plp_dependent_enzyme | BALANCED | 147 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 13 | radical_sam_enzyme | BALANCED | 133 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 14 | sam_methyltransferase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 15 | ser_his_acid_hydrolase | BALANCED | 129 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |

### Sourcing hints per fingerprint (coverage accounting only, never predictive)

| fingerprint | EC prefixes | cofactor signature | lanes |
| --- | --- | --- | --- |
| metal_dependent_hydrolase | 3.4.24, 3.5.2, 3.1.3, 3.1.4 | catalytic divalent metal (Zn2+/Mn2+/Mg2+/Ni2+) | metal hydrolase |
| cobalamin_radical_rearrangement | 5.4.99, 5.4.3, 4.2.1.28, 4.2.1.30, 4.3.1.7 | adenosylcobalamin / vitamin B12 (radical rearrangement) | cobalamin radical, plp_radical_cobalamin |
| flavin_dehydrogenase_reductase | 1.3, 1.6, 1.8.1 | flavin (FAD/FMN), no heme; hydride/electron transfer | flavin redox boundary, flavin dehydrogenase/reductase |
| flavin_monooxygenase | 1.14.13, 1.14.14 | flavin (FAD/FMN), no heme; inserts one O | flavin monooxygenase |
| glycosyltransferase | 2.4 | nucleotide-sugar donor (UDP/GDP/dTDP/CMP-sugar; GT-A DxD metal or GT-B cleft) | glycosyltransferase |
| heme_peroxidase_oxidase | 1.11.1 | heme b / heme c (peroxidase) | heme peroxidase/oxidase-like |
| metallo_amidohydrolase_deaminase | 3.5.2, 3.5.4, 3.5.1 | catalytic Zn2+ (mono/di-nuclear); non-peptide amide/amidine C-N hydrolysis | metallo amidohydrolase/deaminase |
| metallopeptidase | 3.4.24, 3.4.17, 3.4.11 | catalytic Zn2+ (HExxH / co-catalytic dizinc); peptide C-N hydrolysis | metallopeptidase |
| metallophosphoesterase_nuclease | 3.1.4, 3.1.11, 3.1.21, 3.1.26, 3.1.27, 3.1.31 | two-metal Mg2+/Mn2+ (sometimes Zn2+); phosphodiester P-O hydrolysis | metallophosphoesterase/nuclease |
| metallophosphomonoesterase | 3.1.3 | dinuclear Zn/Mg/Mn/Fe; phosphomonoester P-O hydrolysis (not Cys-PTP) | metallophosphomonoesterase |
| nad_p_dehydrogenase | 1.1.1 | NAD(P) cosubstrate (dissociable nicotinamide dinucleotide; Rossmann GxGxxG) | nad_p_dehydrogenase |
| plp_dependent_enzyme | 2.6.1, 4.1.1, 4.3.1, 5.1.1, 4.4.1 | pyridoxal-5'-phosphate (PLP) Schiff base | PLP lyase/eliminase, PLP decarboxylase, PLP aminotransferase, PLP racemase/epimerase, PLP sulfur lyase boundary |
| radical_sam_enzyme | 1.97.1, 2.8.4, 4.1.99, 2.5.1 | [4Fe-4S] + S-adenosylmethionine (CX3CX2C motif) | radical SAM, plp_radical_cobalamin |
| sam_methyltransferase | 2.1.1 | SAM methyl donor / SAH product (dissociable methyl-transfer cosubstrate); no Fe-S radical-SAM context | sam_methyltransferase |
| ser_his_acid_hydrolase | 3.4.21, 3.1.1, 3.5.1 | no cofactor; Ser/Cys-His-Asp/Glu catalytic triad | serine/cysteine hydrolase, esterase/lipase triad |

## Guardrails

- Frozen benchmark written: False.
- Expansion registry written: False.
- Labels emitted: 0.
- EC/lane/organism used for coverage accounting only, never predictive.
- Metadata-only: no network, no mmseqs, no embedding backend.
