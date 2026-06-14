# Coverage + Redundancy Audit And Balance-Capped Acquisition Policy

Run: 2026-06-14T04:01:16Z

Non-destructive, metadata-only audit of all combined labels (7636 = 702 frozen current702 + 6934 expansion bronze). No registry is written and no label is emitted. Redundancy is measured from annotation metadata only (no mmseqs / no embeddings / no network).

## Class balance (seed fingerprints, combined)

- Seed positives: 5667; out_of_scope: 1696; positive:OOS = 3.3414.
- Fingerprint Gini 0.1872 / normalized entropy 0.9832; max/min(nonzero) ratio 3.08 (308 vs 100).
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
| radical_sam_enzyme | 1 | 213 | 214 | 23 | 9.26 |
| cobalamin_radical_rearrangement | 3 | 141 | 144 | 15 | 9.4 |
| nad_p_dehydrogenase | 0 | 150 | 150 | 88 | 1.7 |
| glycosyltransferase | 0 | 250 | 250 | 394 | 0.63 |
| glycoside_hydrolase | 0 | 150 | 150 | 93 | 1.61 |
| sam_methyltransferase | 0 | 250 | 250 | 129 | 1.94 |
| cytochrome_p450_monooxygenase | 0 | 250 | 250 | 498 | 0.5 |
| non_heme_iron_2og_dioxygenase | 0 | 250 | 250 | 100 | 2.5 |
| coa_acyltransferase | 0 | 250 | 250 | 452 | 0.55 |
| cofactor_independent_isomerase | 0 | 150 | 150 | 59 | 2.54 |
| molybdopterin_oxidoreductase | 0 | 250 | 250 | 38 | 6.58 |
| copper_oxidoreductase | 0 | 140 | 140 | 25 | 5.6 |
| metal_racemase_epimerase_non_plp | 0 | 150 | 150 | 86 | 1.74 |
| atp_amide_ligase | 0 | 150 | 150 | 89 | 1.69 |
| class_ii_metal_aldolase | 0 | 150 | 150 | 46 | 3.26 |
| thiamine_diphosphate_enzyme | 0 | 150 | 150 | 24 | 6.25 |
| zinc_lyase_hydratase | 0 | 100 | 100 | 6 | 16.67 |
| biotin_dependent_carboxylase | 0 | 100 | 100 | 8 | 12.5 |
| nucleoside_diphosphate_kinase | 0 | 100 | 100 | 10 | 10.0 |
| deoxynucleoside_kinase | 0 | 100 | 100 | 7 | 14.29 |
| askha_sugar_acetate_kinase | 0 | 100 | 100 | 9 | 11.11 |
| ghmp_small_molecule_kinase | 0 | 100 | 100 | 4 | 25.0 |
| pfka_phosphofructokinase | 0 | 100 | 100 | 2 | 50.0 |
| pfkb_ribokinase_family | 0 | 150 | 150 | 16 | 9.38 |
| manganese_iron_superoxide_dismutase | 0 | 100 | 100 | 1 | 100.0 |

## Near-duplicate / saturation read (metadata proxy)

- Cluster key: (fingerprint_or_scope, full_ec, organism, sequence_length_bin).
- Measurable rows: 6780; clusters (size >= 3): 123; rows in clusters: 489 (0.0721 of measurable).
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
- Reaction-saturated (over reaction-aware cap, rate 8): ['cobalamin_radical_rearrangement', 'pfkb_ribokinase_family', 'radical_sam_enzyme'] (surplus 72).
- Total deficit to floor (next-batch positive target): 0.

| # | fingerprint | status | combined | deficit | surplus | action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | metal_dependent_hydrolase | OVER_CAP | 308 | 0 | 58 | CAP / PAUSE -- 58 over the 250 ceiling; dedup toward distinct reactions before adding any |
| 2 | askha_sugar_acetate_kinase | BALANCED | 100 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 3 | atp_amide_ligase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 4 | biotin_dependent_carboxylase | BALANCED | 100 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 5 | class_ii_metal_aldolase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 6 | coa_acyltransferase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 7 | cobalamin_radical_rearrangement | BALANCED | 144 | 0 | 0 | TRIM -- 21 over the reaction-aware cap 120 (15 distinct reactions x rate 8); demote redundant orthologs toward reaction diversity, do not source more |
| 8 | cofactor_independent_isomerase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 9 | copper_oxidoreductase | BALANCED | 140 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 10 | cytochrome_p450_monooxygenase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 11 | deoxynucleoside_kinase | BALANCED | 100 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 12 | flavin_dehydrogenase_reductase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 13 | flavin_monooxygenase | BALANCED | 116 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 14 | ghmp_small_molecule_kinase | BALANCED | 100 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 15 | glycoside_hydrolase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 16 | glycosyltransferase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 17 | heme_peroxidase_oxidase | BALANCED | 119 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 18 | manganese_iron_superoxide_dismutase | BALANCED | 100 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 19 | metal_racemase_epimerase_non_plp | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 20 | metallo_amidohydrolase_deaminase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 21 | metallopeptidase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 22 | metallophosphoesterase_nuclease | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 23 | metallophosphomonoesterase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 24 | molybdopterin_oxidoreductase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 25 | nad_p_dehydrogenase | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 26 | non_heme_iron_2og_dioxygenase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 27 | nucleoside_diphosphate_kinase | BALANCED | 100 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 28 | pfka_phosphofructokinase | BALANCED | 100 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 29 | pfkb_ribokinase_family | BALANCED | 150 | 0 | 0 | TRIM -- 22 over the reaction-aware cap 128 (16 distinct reactions x rate 8); demote redundant orthologs toward reaction diversity, do not source more |
| 30 | plp_dependent_enzyme | BALANCED | 147 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 31 | radical_sam_enzyme | BALANCED | 214 | 0 | 0 | TRIM -- 29 over the reaction-aware cap 184 (23 distinct reactions x rate 8); demote redundant orthologs toward reaction diversity, do not source more |
| 32 | sam_methyltransferase | BALANCED | 250 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 33 | ser_his_acid_hydrolase | BALANCED | 129 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 34 | thiamine_diphosphate_enzyme | BALANCED | 150 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |
| 35 | zinc_lyase_hydratase | BALANCED | 100 | 0 | 0 | HOLD -- at balance; only add if a new reaction/organism is gained |

### Sourcing hints per fingerprint (coverage accounting only, never predictive)

| fingerprint | EC prefixes | cofactor signature | lanes |
| --- | --- | --- | --- |
| metal_dependent_hydrolase | 3.4.24, 3.5.2, 3.1.3, 3.1.4 | catalytic divalent metal (Zn2+/Mn2+/Mg2+/Ni2+) | metal hydrolase |
| askha_sugar_acetate_kinase | 2.7.1 | ATP/Mg phosphoryl-transfer cosubstrate context with sugar, glycerol, or acetate acceptor | askha_sugar_acetate_kinase |
| atp_amide_ligase | 6.3 | ATP/Mg cosubstrate context; acyl-phosphate-like intermediate and C-N amide ligation | atp_amide_ligase |
| biotin_dependent_carboxylase | 6.4.1, 6.3.4 | protein-bound biotin / biotinyl-Lys plus ATP/Mg and hydrogencarbonate/CO2 carboxylation chemistry | biotin_dependent_carboxylase |
| class_ii_metal_aldolase | 4.1.2, 4.1.3 | Zn/Co/divalent metal; enolate-stabilized aldol C-C lyase chemistry | class_ii_metal_aldolase |
| coa_acyltransferase | 2.3.1 | CoA/acyl-CoA donor (dissociable thioester cosubstrate); acyl group transfer | coa_acyltransferase |
| cobalamin_radical_rearrangement | 5.4.99, 5.4.3, 4.2.1.28, 4.2.1.30, 4.3.1.7 | adenosylcobalamin / vitamin B12 (radical rearrangement) | cobalamin radical, plp_radical_cobalamin |
| cofactor_independent_isomerase | 5.3 | no cofactor; Rhea isomerization equation plus active-site/base context | cofactor_independent_isomerase |
| copper_oxidoreductase | 1.10.3, 1.4.3 | copper redox center; multicopper oxidase or copper amine oxidase oxygen/electron-transfer chemistry | copper_oxidoreductase |
| cytochrome_p450_monooxygenase | 1.14 | heme-thiolate plus O2/reductant cosubstrate; non-peroxidase P450 monooxygenation | cytochrome_p450_monooxygenase |
| deoxynucleoside_kinase | 2.7.1 | ATP/Mg phosphoryl-transfer cosubstrate context with deoxynucleoside acceptor specificity | deoxynucleoside_kinase |
| flavin_dehydrogenase_reductase | 1.3, 1.6, 1.8.1 | flavin (FAD/FMN), no heme; hydride/electron transfer | flavin redox boundary, flavin dehydrogenase/reductase |
| flavin_monooxygenase | 1.14.13, 1.14.14 | flavin (FAD/FMN), no heme; inserts one O | flavin monooxygenase |
| ghmp_small_molecule_kinase | 2.7.1 | ATP/Mg phosphoryl-transfer cosubstrate context with GHMP-family small-molecule acceptor | ghmp_small_molecule_kinase |
| glycoside_hydrolase | 3.2.1 | glycosidic substrate plus catalytic water/protonation context; glycosyltransferase, transglycosylase, phosphorylase, and lyase boundaries are held | glycoside_hydrolase |
| glycosyltransferase | 2.4 | nucleotide-sugar donor (UDP/GDP/dTDP/CMP-sugar; GT-A DxD metal or GT-B cleft) | glycosyltransferase |
| heme_peroxidase_oxidase | 1.11.1 | heme b / heme c (peroxidase) | heme peroxidase/oxidase-like |
| manganese_iron_superoxide_dismutase | 1.15.1.1 | Mn or Fe redox metal center for superoxide dismutation; Cu/Zn SOD, heme/peroxidase, and superoxide-reductase boundaries are held | manganese_iron_superoxide_dismutase |
| metal_racemase_epimerase_non_plp | 5.1 | non-PLP racemase/epimerase proton-transfer chemistry; metal or cofactorless active-site context | metal_racemase_epimerase_non_plp |
| metallo_amidohydrolase_deaminase | 3.5.2, 3.5.4, 3.5.1 | catalytic Zn2+ (mono/di-nuclear); non-peptide amide/amidine C-N hydrolysis | metallo amidohydrolase/deaminase |
| metallopeptidase | 3.4.24, 3.4.17, 3.4.11 | catalytic Zn2+ (HExxH / co-catalytic dizinc); peptide C-N hydrolysis | metallopeptidase |
| metallophosphoesterase_nuclease | 3.1.4, 3.1.11, 3.1.21, 3.1.26, 3.1.27, 3.1.31 | two-metal Mg2+/Mn2+ (sometimes Zn2+); phosphodiester P-O hydrolysis | metallophosphoesterase/nuclease |
| metallophosphomonoesterase | 3.1.3 | dinuclear Zn/Mg/Mn/Fe; phosphomonoester P-O hydrolysis (not Cys-PTP) | metallophosphomonoesterase |
| molybdopterin_oxidoreductase | 1 | molybdopterin / molybdenum cofactor redox center; Mo/W oxo-transfer or electron-transfer chemistry | molybdopterin_oxidoreductase |
| nad_p_dehydrogenase | 1.1.1 | NAD(P) cosubstrate (dissociable nicotinamide dinucleotide; Rossmann GxGxxG) | nad_p_dehydrogenase |
| non_heme_iron_2og_dioxygenase | 1.14.11 | Fe(II), 2-oxoglutarate, and O2 cosubstrates; non-heme 2OG oxygenation | non_heme_iron_2og_dioxygenase |
| nucleoside_diphosphate_kinase | 2.7.4.6 | NTP/NDP phosphoryl-transfer cosubstrates with active-site phosphohistidine relay | nucleoside_diphosphate_kinase |
| pfka_phosphofructokinase | 2.7.1 | ATP/Mg phosphoryl-transfer cosubstrate context with fructose-6-phosphate acceptor | pfka_phosphofructokinase |
| pfkb_ribokinase_family | 2.7.1 | ATP/Mg phosphoryl-transfer cosubstrate context with PfkB/ribokinase-family small-molecule acceptors such as ribose, adenosine, inosine, 1-phosphofructose, or hydroxymethylpyrimidine | pfkb_ribokinase_family |
| plp_dependent_enzyme | 2.6.1, 4.1.1, 4.3.1, 5.1.1, 4.4.1 | pyridoxal-5'-phosphate (PLP) Schiff base | PLP lyase/eliminase, PLP decarboxylase, PLP aminotransferase, PLP racemase/epimerase, PLP sulfur lyase boundary |
| radical_sam_enzyme | 1.97.1, 2.8.4, 4.1.99, 2.5.1 | [4Fe-4S] + S-adenosylmethionine (CX3CX2C motif) | radical SAM, plp_radical_cobalamin |
| sam_methyltransferase | 2.1.1 | SAM methyl donor / SAH product (dissociable methyl-transfer cosubstrate); no Fe-S radical-SAM context | sam_methyltransferase |
| ser_his_acid_hydrolase | 3.4.21, 3.1.1, 3.5.1 | no cofactor; Ser/Cys-His-Asp/Glu catalytic triad | serine/cysteine hydrolase, esterase/lipase triad |
| thiamine_diphosphate_enzyme | 2.2.1, 4.1.1, 1.2.4 | ThDP/Mg ylide cofactor context; decarboxylation, carbonyl transfer, or 2-oxoacid dehydrogenase E1 chemistry | thiamine_diphosphate_enzyme |
| zinc_lyase_hydratase | 4.2.1 | catalytic Zn2+; reversible water elimination/addition, carbonic anhydrase, or hydro-lyase chemistry | zinc_lyase_hydratase |

## Guardrails

- Frozen benchmark written: False.
- Expansion registry written: False.
- Labels emitted: 0.
- EC/lane/organism used for coverage accounting only, never predictive.
- Metadata-only: no network, no mmseqs, no embedding backend.
