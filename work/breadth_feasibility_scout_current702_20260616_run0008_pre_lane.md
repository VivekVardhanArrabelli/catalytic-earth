# Breadth Feasibility Scout — is 10k diverse bronze reachable from reviewed Swiss-Prot?

Run: 2026-06-17T00:11:18Z

Non-destructive recon (no registry, no labels). Replaces the scaling-plan cap-math
estimate with real reviewed-Swiss-Prot supply + reaction-diversity numbers for
candidate mechanism families beyond the current 12 (non-hydrolase first).

## Verdict

- **ten_k_diverse_positive_bronze_NOT_reachable_from_reviewed_swissprot_alone**
- 10k diverse positive bronze plausible from reviewed Swiss-Prot: **False**
- Current combined positive bronze is 7032 across 45 fingerprints. Beyond those, 14 candidate families are clean (distinct + floor-reachable + non-redundant), 3 are distinct but below the 100-floor on the cofactor-handle-reachable supply, and 1 are redundant with an existing lane. Adding the clean families' capped, novelty-discounted supply projects to ~9673 diverse POSITIVE bronze -- a gap of 327 to 10k. Two honesty discounts shrink even this: 9 of the clean families are reaction-poor (ortholog padding -- many entries, few distinct reactions), so the diversity-discounted new bronze is only ~1786 (not the headline cap-sum); and 8 families have a weak cofactor handle (it reaches <25% of the EC supply ceiling -- NAD(P) dehydrogenases are the big one, since NAD is a cosubstrate, not a UniProt COFACTOR comment), so their large EC supply is NOT reachable by the current cofactor-anchored gate without a new sequence-motif/EC-only handle. Net: reviewed Swiss-Prot yields low thousands of diverse POSITIVE bronze, not 10k; closing the gap needs either diverse novelty-gated OOS + bronze->silver depth counted toward 10k, or sources beyond reviewed Swiss-Prot.
- **Recommendation:** Re-target: reviewed Swiss-Prot alone does not yield 10k diverse POSITIVE bronze. Source the clean non-hydrolase families to broaden chemistry (non_heme_iron_2og_dioxygenase, cytochrome_p450_monooxygenase, copper_oxidoreductase, molybdopterin_oxidoreductase), and define 10k as positives + diverse novelty-gated OOS + bronze->silver depth, OR bring in sources beyond reviewed Swiss-Prot (TrEMBL/UniRef clusters, BRENDA, structure-anchored families). Keep the positive set diverse, not padded.

## Tally

- Candidate families probed: 18.
- Clean families (distinct + floor-reachable + non-redundant): **14**.
- Distinct but below the 100-floor: 3.
- Redundant with an existing lane: 1.
- Current combined positive bronze: 7032.
- Estimated NEW clean diverse bronze: **2641**.
- Projected positive bronze (clean only): **9673** (+subfloor: 9721).
- Gap to 10k positive bronze: **327**.

## Clean families (by estimated admissible bronze)

| Family | reviewed supply | est. bronze | labels/rxn (≤) | cap | disambiguation handle |
| --- | --- | --- | --- | --- | --- |
| non_heme_iron_2og_dioxygenase | 870 | 250 | 6.944 | 250 | non-heme Fe(II) + 2-oxoglutarate + EC 1.14.11.* (HxD..H triad; not heme, not flavin) |
| sam_methyltransferase | 691 | 250 | 83.333 | 250 | S-adenosyl-L-methionine + EC 2.1.1.* + NO [4Fe-4S] (distinguishes from radical-SAM) |
| glycosyltransferase | 10281 | 250 | 2.451 | 250 | sugar-nucleotide donor (UDP/GDP-sugar) + EC 2.4.* (acceptor-diverse) |
| coa_acyltransferase | 7728 | 250 | 3.049 | 250 | coenzyme A / acyl-CoA + EC 2.3.1.* |
| cofactor_independent_isomerase | 5273 | 250 | 4.902 | 250 | no cofactor; catalytic Glu/His/Lys acid-base + EC 5.3.* (apo-confirmable) |
| molybdopterin_oxidoreductase | 460 | 230 | 6.97 | 250 | molybdopterin / Mo-cofactor + EC 1.1.3/1.2.3/1.8.3/1.97 (distinct Mo center) |
| cytochrome_p450_monooxygenase | 780 | 150 | 2.273 | 150 | heme-thiolate (Cys ligand) + EC 1.14.14/1.14.15 (NOT EC 1.11.1 peroxidase, NOT flavin) |
| atp_phosphotransferase_kinase | 21822 | 150 | 5.0 | 150 | ATP + Mg2+ + EC 2.7.* (phosphoryl DONOR -> distinguishes from hydrolase P-O cleavage) |
| thiamine_diphosphate_enzyme | 1262 | 150 | 6.818 | 150 | thiamine diphosphate (ThDP) + Mg2+ (distinguishes from PLP at shared EC 4.1.1) |
| zinc_lyase_hydratase | 488 | 150 | 7.143 | 150 | catalytic Zn2+ + EC 4.2.1.* (lyase, NOT hydrolase EC 3) |
| class_ii_metal_aldolase | 846 | 150 | 3.947 | 150 | divalent metal (Zn/Co) + EC 4.1.2/4.1.3 (class-II aldol; not Schiff-base class-I) |
| enolase_superfamily_lyase | 915 | 150 | 150.0 | 150 | Mg2+ + enolase-superfamily EC 4.2.1.11/5.1/4.2.1 (TIM-barrel) |
| metal_racemase_epimerase_non_plp | 2141 | 150 | 2.679 | 150 | Mg/Mn (or cofactorless) + EC 5.1.* AND NO PLP (distinguishes from PLP racemase 5.1.1) |
| copper_oxidoreductase | 222 | 111 | 9.25 | 250 | copper (type-1/2/3) + EC 1.10.3/1.4.3 (no heme, no flavin) |

## All probes (incl. floor-blocked + redundant)

EC ceiling = reviewed count for the EC prefixes with NO cofactor filter; capture = cofactor-handle-reachable supply ÷ EC ceiling. rxn-poor = ortholog-padded (labels/distinct-reaction over the warning threshold).

| Family | handle supply | EC ceiling | capture | distinct-EC/sample | est. bronze | floor? | rxn-poor? | redundant? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| nad_p_short_chain_dehydrogenase_reductase | 7 | 7804 | 0.001 | 1/7 | 4 | False | False | False |
| non_heme_iron_2og_dioxygenase | 870 | 874 | 0.995 | 36/200 | 250 | True | True | False |
| cytochrome_p450_monooxygenase | 780 | 1145 | 0.681 | 66/200 | 150 | True | False | False |
| copper_oxidoreductase | 222 | 1264 | 0.176 | 12/200 | 111 | True | True | False |
| molybdopterin_oxidoreductase | 460 | 781 | 0.589 | 33/200 | 230 | True | True | False |
| manganese_iron_superoxide_dismutase | 1 | 470 | 0.002 | 1/1 | 0 | False | False | False |
| sam_methyltransferase | 691 | 14325 | 0.048 | 3/200 | 250 | True | True | False |
| glycosyltransferase | 10281 | 10996 | 0.935 | 102/200 | 250 | True | False | False |
| atp_phosphotransferase_kinase | 21822 | 34140 | 0.639 | 30/200 | 150 | True | True | False |
| coa_acyltransferase | 7728 | 9981 | 0.774 | 82/200 | 250 | True | False | False |
| thiamine_diphosphate_enzyme | 1262 | 7020 | 0.18 | 22/200 | 150 | True | True | False |
| zinc_lyase_hydratase | 488 | 8582 | 0.057 | 21/200 | 150 | True | True | False |
| class_ii_metal_aldolase | 846 | 1921 | 0.44 | 38/200 | 150 | True | False | False |
| enolase_superfamily_lyase | 915 | 8582 | 0.107 | 1/200 | 150 | True | True | False |
| cofactor_independent_isomerase | 5273 | 5087 | 1.037 | 51/200 | 250 | True | True | False |
| metal_racemase_epimerase_non_plp | 2141 | 2319 | 0.923 | 56/200 | 150 | True | False | False |
| atp_amide_ligase | 13599 | 12835 | 1.06 | 73/200 | 0 | False | False | True |
| biotin_dependent_carboxylase | 88 | 4071 | 0.022 | 10/88 | 44 | False | True | False |

## Method + guardrails

- Supply: uniprot x-total-results header count per narrow EC/cofactor lane.
- Reaction diversity: distinct full-EC count over a <= 200-row sample (sampled LOWER bound on reaction diversity -> labels/reaction is a conservative UPPER bound on redundancy).
- Cap math: cap = 150 when chemistry is confusable with a sibling, else 250 (the Stage-2 lesson: filling confusable lanes to the ceiling manufactures redundancy).
- Redundancy check: EC-prefix overlap vs coverage_redundancy_audit.FINGERPRINT_SOURCING_SIGNATURES; an overlap is NOT redundant when a different annotated cofactor separates the lane at the import gate.
- No registry written; no labels created; EC/cofactor used for supply/scope estimation only, never as a predictive feature.
