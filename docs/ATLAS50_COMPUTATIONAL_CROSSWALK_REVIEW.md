# Atlas-50 computational crosswalk review

**Status:** agent-produced proposal overlay, dated 2026-09-05. It is not a human or expert review submission, does not change the frozen Phase A/B checkpoint, and does not authorize a tier lift or scientific completion claim.

## Outcome

All 57 Phase-A crosswalk rows and their 57 Phase-B review packets were inspected at row level. Every fingerprint definition, machine classification and rationale, all thirteen source slots, and the corresponding Phase-B packet were checked. Current official M-CSA records were checked for every M-CSA handle already present in Phase A; selected high-impact omissions were also checked.

The result is **15 provisional**, **26 unresolved for lack of named source targets**, and **16 requiring a concrete correction**. These are computational dispositions, not review decisions. All Phase-B packets remain unreviewed.

The main issue is not the number of documents. It is that the source acquisition boundary cannot answer the Section 10.1 question. The Phase-A source index is built from the 40 panel candidates plus Atlas-3/Atlas-10 selections. It does not index the broader incumbent mechanism stack. As a result, 33 of 57 rows have no M-CSA record, while 32 have all thirteen source slots empty and no M-CSA, EC, InterPro, or CATH target. An empty row therefore means not present in this bounded selection index; it does not mean no upstream object exists.

The historical 702-row data/registries/curated_mechanism_labels.json exposes useful candidate locators, including 83 broad metal-hydrolase, 42 Ser-His hydrolase, 48 flavin-redox, 31 PLP, and 20 heme-redox assignments. Those are prior automation outputs, not gold labels. This review uses them only to locate records for authoritative checking.

## Decision-changing corrections

1. **Reject M0049 from the PLP row.** [M-CSA 49](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/49/) is a pyruvoyl-dependent histidine decarboxylase. It does not use PLP. The M0049-derived EC, ChEBI, UniProt, PDB, CATH, and lookup bundle must not survive as positive PLP evidence. [M-CSA 482](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/482/) is a real PLP-dependent decarboxylase locator, but its mechanism is non-detailed and it remains only one branch.
2. **Name the object on both sides of every relation.** Aggregation, specialization, and interoperability bridge are target-dependent and can overlap. Add relation_targets carrying source key, source object or fingerprint ID, and relation. Permit an unresolved machine-draft state or define a precedence rule.
3. **Fix row 21 internal contradiction.** Its rationale says M0052 is deliberately paired with M0222, while the row and Phase-B packet contain only M0052. [M0052](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/52/) is class II and [M0222](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/222/) is the same-EC class-I Schiff-base mechanism. Add M0222 as explicit counterevidence or delete the pairing claim.
4. **Separate heme from copper coverage.** M0133 is [P450cam](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/133/), not a heme-peroxidase representative. Use a direct peroxidase such as [M0239](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/239/) for row 12. Move laccase from the heme row to copper oxidoreductase and review [M0390](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/390/) there.
5. **Rebuild both beta-lactamase rows by class.** M0002 covers [Class A](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/2/) only, while row 45 spans Classes A, C, and D. Add [Class C M0257](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/257/) and [Class D M0210](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/210/) or narrow the row. Row 49 has no positive M-CSA handle despite detailed [M0015](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/15/) and [M0016](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/16/) Class-B1 mechanisms. The broad current rows are aggregation proposals, subject to a human split decision.
6. **Withdraw DHFR exact_duplicate at the current scope.** [M0112](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/112/) is a bacterial DHFR mechanism object, while the fingerprint explicitly spans chromosomal, resistant, human, and bifunctional contexts. The M-CSA mechanism also describes conserved water as the N5 proton donor, with Asp26 tuning the network; the fingerprint currently assigns direct proton donation to Asp/Glu. Narrow the scope or use aggregation, and correct the proton role before equivalence review.
7. **Populate direct disulfide-reductase incumbents.** Row 56 is empty although [M0006 glutathione reductase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/6/) and [M0381 thioredoxin reductase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/381/) exist. Their different relay/domain arrangements support aggregation at the row current breadth.
8. **Keep M0138 negative for Mn/Fe SOD.** [M0138](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/138/) is Cu/Zn SOD. A current official API filter for EC 1.15.1.1 returned only that entry. A human must choose whether the Mn/Fe row is a genuinely missing M-CSA mechanism concept or a bridge from EC/Rhea and literature; specialization currently has no named target.
9. **Add the omitted exact-reaction NDPK locator.** [M0150](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/150/) is a detailed nucleoside-diphosphate kinase mechanism. Its existence makes row 25 empty specialization claim unreviewable and raises an exact-duplicate question at the declared granularity.

## Proposed relation representation

~~~json
{
  "relation_targets": [
    {
      "source_key": "mcsa",
      "target_id": "M0150",
      "relation": "candidate_exact_duplicate",
      "applicability": "species-general equivalence unresolved",
      "evidence_status": "official_entry_checked"
    }
  ],
  "computational_disposition": "requires_human_decision"
}
~~~

This makes the classification falsifiable. It also prevents an empty source slot from being interpreted as evidence of genuine absence.

## Inspection depth and limits

- **Every row:** fingerprint definition, machine rationale/class, thirteen source-slot states, and matching Phase-B packet.
- **Every existing M-CSA handle:** current official entry identity, overall reaction, and detailed/non-detailed mechanism flag through the public [M-CSA API](https://www.ebi.ac.uk/thornton-srv/m-csa/download/).
- **Selected omissions:** official M-CSA entry pages for the high-impact corrections above and additional row-level locators recorded in the JSON artifact.
- **Locator only:** historical automation assignments from the 702-row local registry. They were not treated as scientific truth.
- **Not run:** new Rhea row retrieval, EC-BLAST, EnzymeMap, MechFind, EzMechanism, EnzyMM, InterPro/Pfam/CATH reassignment, or literature full-text review.
- **Access bound:** no literature bodies were downloaded or committed. Measured temporary M-CSA/API payloads were below 0.5 MiB per request; raw payloads remain outside the repository.

## All 57 rows

P means the machine class is plausible only provisionally. U means the relation cannot be assessed without a named incumbent target. R means this audit found a concrete correction. Official locator means the entry page was checked for identity; it still does not prove family-wide equivalence.

| # | Fingerprint | Machine class | Disposition / proposed class | Phase-A M-CSA | Next focused human question |
|---:|---|---|---|---|---|
| 1 | ser_his_acid_hydrolase | aggregation | P - provisional | M0173, M0723 | Do M0173/M0723 define only the protease branch, and which incumbent entries cover the non-protease branches? |
| 2 | metal_dependent_hydrolase | aggregation | U - unresolved | none | Which incumbent mechanism objects define the parent umbrella, and should this coarse parent disappear after the v2 split? |
| 3 | metallopeptidase | specialization | U - unresolved | none | Is this a specialization of row 2, an aggregation of peptidase mechanisms, or both under a stated precedence rule? |
| 4 | metallophosphoesterase_nuclease | specialization | U - unresolved | none | Which one- or two-metal nuclease objects bound this fingerprint, and does small-molecule phosphodiesterase chemistry belong in the same row? |
| 5 | metallophosphomonoesterase | specialization | U - unresolved | none | Do PPP, PPM, alkaline, and purple-acid phosphatases share enough mechanism to remain one specialization? |
| 6 | metallo_amidohydrolase_deaminase | aggregation | U - unresolved | none | Should beta-lactamases remain here once row 49 has direct class-B objects? |
| 7 | plp_dependent_enzyme | aggregation | R - correction | M0049; M0482 official locator | Which verified PLP entries cover transamination, decarboxylation, racemization, and elimination without collapsing them? |
| 8 | radical_sam_enzyme | aggregation | P - provisional | M0767 | Which radical outcomes must be separate mechanism objects, and what evidence is adequate when M-CSA is non-detailed? |
| 9 | cobalamin_radical_rearrangement | specialization | U - unresolved; alternatives aggregation, specialization | M0062 | Does this row aggregate distinct AdoCbl rearrangements, or is there a named source parent of which it is narrower? |
| 10 | flavin_monooxygenase | aggregation | P - provisional | M0132 | Which flavin-peroxide oxygen-transfer branches require separate applicability rules? |
| 11 | flavin_dehydrogenase_reductase | aggregation | P - provisional | M0139 | Should the xanthine-dehydrogenase FAD module be represented separately from its Mo reaction centre? |
| 12 | heme_peroxidase_oxidase | aggregation | R - correction | M0133; M0239 official locator | Should this row be restricted to heme peroxidases/oxidases, with P450 and laccase handled by rows 13 and 18? |
| 13 | cytochrome_p450_monooxygenase | specialization | P - provisional | M0133 | Is P450 a specialization of a heme-redox parent, or an aggregation of distinct P450 reaction mechanisms at the chosen granularity? |
| 14 | non_heme_iron_2og_dioxygenase | specialization | P - provisional | M0129 | Which Fe(II)/2OG subclasses share ordered steps versus only cofactor logic? |
| 15 | coa_acyltransferase | aggregation | U - unresolved | none | Which architectures share the same acyl-transfer object, and which require separate mechanisms? |
| 16 | cofactor_independent_isomerase | unsupported_or_ill_defined | P - provisional | M0081 | Can this negative bucket be replaced by named pericyclic, acid-base, and racemase mechanism objects? |
| 17 | molybdopterin_oxidoreductase | aggregation | P - provisional | M0107, M0121, M0139 | Should Mo-centre chemistry and downstream electron-transfer modules be separate linked objects? |
| 18 | copper_oxidoreductase | aggregation | R - correction | M0135; M0390 official locator | Which copper-centre subclasses need distinct mechanism objects? |
| 19 | metal_racemase_epimerase_non_plp | aggregation | R - correction | M0187 | Is metal required by this fingerprint, and do mutarotases belong in the same object? |
| 20 | atp_amide_ligase | aggregation | U - unresolved | none | Which activation intermediates and oligomeric states justify separate mechanisms? |
| 21 | class_ii_metal_aldolase | specialization | R - correction | M0052; M0222 official locator | Should class-I M0222 be a required negative comparator for the class-II metal fingerprint? |
| 22 | zinc_lyase_hydratase | aggregation | P - provisional | M0216 | Which zinc hydration/dehydration chemistries share more than metal-activated water? |
| 23 | biotin_dependent_carboxylase | aggregation | U - unresolved | none | Is the fingerprint one catalytic cycle with linked components, or several mechanism objects? |
| 24 | deoxynucleoside_kinase | specialization | U - unresolved | M0588 official locator | Does the row aggregate substrate-specific kinases, or specialize a named kinase object? |
| 25 | nucleoside_diphosphate_kinase | specialization | R - correction; alternatives exact_duplicate, specialization | M0150 official locator | Is species-general NDPK the same mechanism object as M0150, or does the project require a broader applicability object? |
| 26 | askha_sugar_acetate_kinase | interoperability_bridge | U - unresolved | none | Which exact family and reaction identifiers does this bridge connect? |
| 27 | ghmp_small_molecule_kinase | interoperability_bridge | U - unresolved | none | Which GHMP members share catalytic steps rather than only architecture? |
| 28 | pfka_phosphofructokinase | specialization | U - unresolved | none | Is this an exact reaction object, a fold specialization, or both? |
| 29 | pfkb_ribokinase_family | interoperability_bridge | U - unresolved | none | Which exact PfkB family identifiers and EC/Rhea reactions are bridged? |
| 30 | thiamine_diphosphate_enzyme | aggregation | P - provisional | M0106, M0219 | Which common ThDP steps can be shared without transferring reaction-specific steps? |
| 31 | nad_p_dehydrogenase | aggregation | P - provisional | M0007, M0139 | Should NAD(P) hydride transfer be a reusable module rather than a family-wide mechanism? |
| 32 | glycosyltransferase | aggregation | P - provisional | M0970 | Which donor, acceptor, and processivity differences require distinct objects? |
| 33 | glycoside_hydrolase | aggregation | P - provisional | M0203 | Which glycoside-hydrolase families can share arrow environments safely? |
| 34 | sam_methyltransferase | aggregation | U - unresolved | none | Which acceptor atom and substrate classes define separate mechanisms? |
| 35 | manganese_iron_superoxide_dismutase | specialization | R - correction; alternatives genuinely_missing_concept, interoperability_bridge | M0138 negative | Is the classification relative to M-CSA mechanism coverage or to the whole source stack? |
| 36 | terpene_cyclase_synthase | aggregation | U - unresolved | none | Which initiation modes and metal requirements define distinct mechanisms? |
| 37 | protein_kinase_ser_thr_tyr | interoperability_bridge | U - unresolved | M0282 official locator, M0760 official locator | Which exact protein-kinase object and substrate-residue objects are being bridged? |
| 38 | had_like_phosphatase | specialization | R - correction | none | Is the Asp-phosphoenzyme intermediate sufficient to make this a distinct specialization? |
| 39 | aldehyde_dehydrogenase | specialization | R - correction | M0803 official locator | Does this row exclude GAPDH-type phosphorylating aldehyde oxidation? |
| 40 | alpha_beta_hydrolase_esterase_lipase | specialization | R - correction; alternatives specialization, interoperability_bridge | none | Is the primary relation a mechanism specialization or an interoperability bridge from fold to chemistry? |
| 41 | ser_thr_protein_phosphatase | specialization | R - correction | none | Does this row aggregate PPP, PPM, and calcineurin mechanisms despite being narrower than row 5? |
| 42 | n_ribosyl_hydrolase | specialization | U - unresolved | none | Which substrate and leaving-group differences change the mechanism object? |
| 43 | metal_independent_phosphodiesterase | unsupported_or_ill_defined | R - correction | none | Which concrete metal-independent family supports this fingerprint? |
| 44 | aminoglycoside_phosphotransferase | specialization | U - unresolved | none | Do position-specific APH subfamilies share one transferable mechanism? |
| 45 | serine_beta_lactamase | specialization | R - correction -> aggregation | M0002; M0210 official locator, M0257 official locator | Should this fingerprint be split by Ambler serine class? |
| 46 | short_chain_dehydrogenase_reductase | specialization | U - unresolved | none | Which SDR substrates and reaction directions preserve the same catalytic network? |
| 47 | aldo_keto_reductase | specialization | U - unresolved | none | Which AKR subfamilies share the same hydride/proton geometry? |
| 48 | aminoglycoside_acetyltransferase | specialization | U - unresolved | none | Should AAC(1), AAC(3), AAC(2-prime), and AAC(6-prime) be distinct objects? |
| 49 | metallo_beta_lactamase | specialization | R - correction -> aggregation | M0015 official locator, M0016 official locator | Should B1, B2, and B3 be split by zinc stoichiometry and catalytic network? |
| 50 | peroxiredoxin_thiol_peroxidase | aggregation | P - provisional | M0851 | Should GPx and peroxiredoxin be separate linked objects? |
| 51 | paps_sulfotransferase | aggregation | U - unresolved | none | Which acceptor classes and topologies require separate mechanisms? |
| 52 | glutathione_s_transferase | aggregation | U - unresolved | none | Which GST activities are true GSH conjugation versus other chemistry? |
| 53 | aminoacyl_trna_synthetase | aggregation | U - unresolved | M0481 official locator, M0235 official locator | Which aminoacylation steps are shared across classes I and II? |
| 54 | acid_coa_ligase | specialization | U - unresolved | none | Which substrate scopes share the acyl-adenylate and thioester-forming steps? |
| 55 | cysteine_protease | aggregation | P - provisional | M0174 | Which clans share a transferable Cys-His catalytic network? |
| 56 | flavin_disulfide_reductase | specialization | R - correction -> aggregation | M0006 official locator, M0381 official locator | Should each disulfide reductase substrate/relay architecture be a separate mechanism object? |
| 57 | dihydrofolate_reductase | exact_duplicate | R - correction -> aggregation | M0112 | What object granularity makes this exact, and is the conserved water the explicit N5 proton donor in the fingerprint? |

## Human review queue

The smallest useful review sequence is:

1. Confirm rejection of M0049 and choose a four-branch PLP comparison set.
2. Decide the relation target and precedence rule before reviewing the remaining classification labels.
3. Resolve M0052 versus M0222 as an explicit same-EC/different-mechanism pair.
4. Decide the row-12/13/18 boundary for peroxidase, P450, and laccase chemistry.
5. Split or aggregate serine beta-lactamase Classes A/C/D and metallo Classes B1/B2/B3.
6. Decide whether DHFR is exact only at overall-operation granularity and correct the N5 proton donor.
7. Decide whether Mn/Fe SOD is missing from M-CSA or represented as a cross-source bridge.
8. Review M0006/M0381 for the flavin-disulfide row and M0150 for NDPK.
9. Then fill the 25 targetless rows, starting with the metal-hydrolase v2 children and the three bridge rows.

Each decision should record the compared object IDs, the granularity of equivalence, and one reason the decision could fail. A valid Phase-B submission can cite this overlay as computational preparation, but the submission must still come from an attributable human reviewer after actual review.

## Artifacts

- Machine-readable row audit: data/atlas/atlas50/computational_review/crosswalk_review.json
- Frozen input: data/atlas/atlas50/phase_a/crosswalk_draft.json
- Human review queue: data/atlas/atlas50/phase_b/crosswalk_review_queue.json

The JSON artifact contains the per-row issue, proposed correction, focused human question, Phase-A source-slot inventory, authoritative M-CSA checks, discovery locators, input hashes, and the exact claim boundary.
