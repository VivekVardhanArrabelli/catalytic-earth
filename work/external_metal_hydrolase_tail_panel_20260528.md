# Metal Hydrolase Tail/Boundary External Stress Panel - 2026-05-28

Run time: 2026-05-28T08:15:32Z

Review-only validation-panel design and source/evidence scouting. No labels, registries, ontologies, thresholds, production scoring, imports, model outputs, model training, or coordinate downloads were changed.

Outputs:

- `artifacts/v3_external_metal_hydrolase_tail_panel_20260528.json`
- `work/external_metal_hydrolase_tail_panel_20260528.md`

## Bottom Line

The broad v1 `metal_dependent_hydrolase` parent is useful as a metal-water router signal, but this panel should not treat it as a terminal chemistry label until it survives hard boundary tests. The risky collapses are zinc peptide hydrolysis versus phosphatase/nuclease chemistry, MBL/amidohydrolase metal-count differences, FGly/sulfatase and carbonic-anhydrase special cases, and Mg/nucleotide or nonhydrolytic metal false positives.

The manifest freezes 74 rows/leads: 59 M-CSA/local rows and 15 external UniProt/PDB metadata leads. All rows remain non-countable in this artifact.

## Prior Decision Reuse

- 22 positive expert/trace artifacts supply the MPP, prolidase, 5-prime nucleotidase, lambda exonuclease, PvuII, AMP product-context, and methionyl aminopeptidase statuses.
- 66 remaining triage supplies sulfatase/FGly, stromelysin, botulinum/leishmanolysin zincin, colicin nuclease, vesicle ATPase, adenosinetriphosphatase, and dUTPase review-only statuses.
- 210 current-target rejections supply myosin ATPase and nonhydrolytic metal/redox hard negatives.
- External source scouting used UniProt REST metadata and public PDB cross-references only; no coordinates were downloaded.

## Counts

### Lane

| Lane | Rows |
| --- | ---: |
| `binuclear_metallohydrolase_amidohydrolase` | 8 |
| `carbonic_anhydrase_dehydratase_boundary` | 8 |
| `metal_dependent_nonhydrolytic_negative` | 6 |
| `metallo_beta_lactamase_like` | 5 |
| `ntpase_nucleotide_hydrolase_boundary` | 10 |
| `nuclease_phosphoesterase` | 9 |
| `phosphatase_phosphoesterase` | 10 |
| `sulfatase_fgly_metal_boundary` | 5 |
| `zinc_metalloprotease_zincin` | 13 |

### Candidate role

| Candidate role | Rows |
| --- | ---: |
| `external_hard_negative` | 3 |
| `external_positive_lead` | 12 |
| `near_family_hard_negative` | 1 |
| `oos_hard_negative` | 13 |
| `positive_anchor` | 29 |
| `review_only_positive_lead` | 16 |

### Readiness tier

| Readiness tier | Rows |
| --- | ---: |
| `gold` | 38 |
| `review-only` | 13 |
| `silver` | 23 |

### Geometry class

| Geometry class | Rows |
| --- | ---: |
| `apo_or_holo_override_geometry` | 3 |
| `apo_or_missing_metal` | 3 |
| `loose_open_conformation` | 1 |
| `loose_open_or_interdomain_geometry` | 2 |
| `loose_open_or_oligomer_geometry` | 1 |
| `loose_or_acid_base_plus_metal_locality` | 1 |
| `nonhydrolytic_active_site` | 1 |
| `nonhydrolytic_dehydration_geometry` | 4 |
| `nonhydrolytic_dioxygenase_geometry` | 1 |
| `nonhydrolytic_metal_hydration_geometry` | 1 |
| `nonhydrolytic_oxidase_geometry` | 1 |
| `nonhydrolytic_redox_geometry` | 2 |
| `nucleotide_context_review_needed` | 1 |
| `product_context_confounded` | 1 |
| `tight_active_site_geometry` | 40 |
| `tight_active_site_review_needed` | 1 |
| `tight_active_site_with_wide_substrate_flanking_residues` | 1 |
| `tight_nucleotide_active_site_not_hydrolytic_parent` | 6 |
| `tight_nucleotide_active_site_parent_collision` | 1 |
| `tight_or_inhibitor_bound_review_needed` | 1 |
| `wide_focus_pair_but_local_metal_context` | 1 |

### Provenance tier

| Provenance tier | Rows |
| --- | ---: |
| `tier_A_mcsa_curated` | 45 |
| `tier_B_external_curated` | 12 |
| `tier_D_control_only` | 17 |

## Candidate Rows

| # | Row | Lane | Role | Tier | Geometry | Structure | Metal/Ligand State | Expected Router Behavior |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `m_csa:171` carboxypeptidase A | `zinc_metalloprotease_zincin` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1M4L` | single Zn metalloprotease active site; local Zn in selected structure | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 2 | `m_csa:176` thermolysin | `zinc_metalloprotease_zincin` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1KEI` | single catalytic Zn in thermolysin active site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 3 | `m_csa:596` deuterolysin | `zinc_metalloprotease_zincin` | `positive_anchor` | `silver` | `tight_active_site_geometry` | `1EB6` | Zn present; deuterolysin zincin geometry noted in current registry | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 4 | `m_csa:623` neprilysin | `zinc_metalloprotease_zincin` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1R1J` | Zn present in selected 1R1J; clean imported prior decision | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 5 | `m_csa:626` bontoxilysin | `zinc_metalloprotease_zincin` | `review_only_positive_lead` | `silver` | `tight_active_site_geometry` | `1EPW` | Zn present; botulinum neurotoxin zincin active-site motif | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 6 | `m_csa:668` leishmanolysin | `zinc_metalloprotease_zincin` | `review_only_positive_lead` | `silver` | `tight_active_site_geometry` | `1LML` | Zn present; leishmanolysin metalloprotease | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 7 | `m_csa:641` anthrax lethal factor endopeptidase | `zinc_metalloprotease_zincin` | `positive_anchor` | `silver` | `apo_or_holo_override_geometry` | `1PWV` | selected structure apo, prior holo override supported Zn metalloprotease | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 8 | `m_csa:657` mitochondrial processing peptidase | `zinc_metalloprotease_zincin` | `review_only_positive_lead` | `review-only` | `loose_or_acid_base_plus_metal_locality` | `1HR6` | Zn local to beta-subunit active site but direct residue-locality rule... | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 9 | `m_csa:591` stromelysin 1 | `zinc_metalloprotease_zincin` | `review_only_positive_lead` | `review-only` | `tight_or_inhibitor_bound_review_needed` | `1HFS` | Zn metalloprotease/inhibitor context present in selected structure | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 10 | `m_csa:87` urease | `binuclear_metallohydrolase_amidohydrolase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1FWJ` | binuclear Ni urease center with carbamylated lysine | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 11 | `m_csa:157` hydroxyacylglutathione hydrolase | `binuclear_metallohydrolase_amidohydrolase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1QH5` | Zn metallohydrolase center in glyoxalase II/MBL fold | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 12 | `m_csa:379` Xaa-Pro aminopeptidase | `binuclear_metallohydrolase_amidohydrolase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1A16` | Mn-bound Xaa-Pro aminopeptidase active site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 13 | `m_csa:447` glutamate carboxypeptidase | `binuclear_metallohydrolase_amidohydrolase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1CG2` | Zn carboxypeptidase active site; current registry high confidence | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 14 | `m_csa:710` cytosine deaminase (bacterial) | `binuclear_metallohydrolase_amidohydrolase` | `positive_anchor` | `silver` | `tight_active_site_geometry` | `1RA0` | Fe amidohydrolase-superfamily deaminase; Fe-activated water attack | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 15 | `m_csa:720` creatininase | `binuclear_metallohydrolase_amidohydrolase` | `positive_anchor` | `silver` | `tight_active_site_geometry` | `1J2U` | binuclear Zn creatininase active site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 16 | `m_csa:917` methionyl aminopeptidase | `binuclear_metallohydrolase_amidohydrolase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1XGM` | Co ions at catalytic sites in selected structure | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 17 | `m_csa:1001` Prolidase (Xaa-Pro dipeptidase) | `binuclear_metallohydrolase_amidohydrolase` | `review_only_positive_lead` | `review-only` | `loose_open_or_oligomer_geometry` | `5M4G` | four Mn ions present but active-site role-pair locality unresolved | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 18 | `m_csa:43` purple acid phosphatase | `phosphatase_phosphoesterase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `4KBP` | mixed Fe/Zn purple acid phosphatase site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 19 | `m_csa:44` alkaline phosphatase | `phosphatase_phosphoesterase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1ALK` | Zn/Mg alkaline phosphatase site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 20 | `m_csa:159` aryldialkylphosphatase | `phosphatase_phosphoesterase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1HZY` | Zn aryldialkylphosphatase site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 21 | `m_csa:406` protein phosphatase 2B | `phosphatase_phosphoesterase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1AUI` | Fe/Zn protein phosphatase 2B active site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 22 | `m_csa:472` serine/threonine-protein phosphatase 5 | `phosphatase_phosphoesterase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1S95` | two Mn ions plus phosphate in selected structure | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 23 | `m_csa:577` inositol-phosphate phosphatase | `phosphatase_phosphoesterase` | `positive_anchor` | `silver` | `apo_or_holo_override_geometry` | `1IMA` | selected Gd/inhibitor context had prior holo override support | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 24 | `m_csa:611` 5'-nucleotidase (bacterial) | `phosphatase_phosphoesterase` | `review_only_positive_lead` | `review-only` | `loose_open_conformation` | `1USH` | Zn ions present but open-domain geometry made focus pair distant | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 25 | `m_csa:812` 5'-nucleotidase (mitochondrial) | `phosphatase_phosphoesterase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1Q91` | Mg/phosphate/DPB context in selected structure | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 26 | `m_csa:904` 3'(2'),5'-bisphosphate nucleotidase | `phosphatase_phosphoesterase` | `review_only_positive_lead` | `review-only` | `product_context_confounded` | `1QGX` | Mg/phosphate/AMP/SO4 context but AMP product triggered nucleotide-tra... | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 27 | `m_csa:160` exodeoxyribonuclease III | `nuclease_phosphoesterase` | `positive_anchor` | `silver` | `apo_or_missing_metal` | `1AKO` | selected structure lacks local metal ligand codes despite M-CSA nucle... | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 28 | `m_csa:163` ribonuclease HI | `nuclease_phosphoesterase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1RDD` | Mg RNase H active site in selected structure | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 29 | `m_csa:395` nuclease P1 | `nuclease_phosphoesterase` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1AK0` | Zn nuclease P1 active site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 30 | `m_csa:791` colicin-E9 | `nuclease_phosphoesterase` | `review_only_positive_lead` | `silver` | `tight_active_site_with_wide_substrate_flanking_residues` | `1FR2` | Zn HNH nuclease center; flanking DNA residues give wide CA-pair geometry | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 31 | `m_csa:838` Colicin-E7 | `nuclease_phosphoesterase` | `review_only_positive_lead` | `silver` | `tight_active_site_geometry` | `1ZNV` | Ni/Zn-surrogate HNH nuclease metal state | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 32 | `m_csa:836` exodeoxyribonuclease (lambda-induced) | `nuclease_phosphoesterase` | `review_only_positive_lead` | `review-only` | `apo_or_missing_metal` | `1AVQ` | selected lambda exonuclease structure lacks biological metal; alterna... | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 33 | `m_csa:897` type II site-specific deoxyribonuclease PvuII | `nuclease_phosphoesterase` | `positive_anchor` | `silver` | `apo_or_holo_override_geometry` | `1PVI` | selected PvuII structure apo, prior two-Mg holo override supported po... | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 34 | `m_csa:927` type II site-specific deoxyribonuclease FokI | `nuclease_phosphoesterase` | `review_only_positive_lead` | `review-only` | `apo_or_missing_metal` | `2FOK` | selected FokI geometry lacks local ligand codes in current feature row | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 35 | `m_csa:15` beta-lactamase (Class B1) | `metallo_beta_lactamase_like` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1ZNB` | Zn class B1 beta-lactamase active site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 36 | `m_csa:258` beta-lactamase (Class B1) | `metallo_beta_lactamase_like` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1SML` | Zn class B1 beta-lactamase active site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 37 | `m_csa:158` cerebroside-sulfatase | `sulfatase_fgly_metal_boundary` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1AUK` | FGly/FGL and Mg sulfatase state in selected structure | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 38 | `m_csa:661` arylsulfatase | `sulfatase_fgly_metal_boundary` | `review_only_positive_lead` | `review-only` | `wide_focus_pair_but_local_metal_context` | `1HDH` | Ca/SO4 context with sulfatase chemistry but 66 queue kept review-only | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 39 | `m_csa:951` N-sulfoglucosamine sulfohydrolase | `sulfatase_fgly_metal_boundary` | `review_only_positive_lead` | `review-only` | `tight_active_site_review_needed` | `4MHX` | FGP/Ca sulfatase state in selected structure | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 40 | `m_csa:178` H+-transporting two-sector ATPase (F-type, mitochondrial) | `ntpase_nucleotide_hydrolase_boundary` | `oos_hard_negative` | `gold` | `tight_nucleotide_active_site_not_hydrolytic_parent` | `1BMF` | ADP/Mg F-type ATPase context | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 41 | `m_csa:179` chaperonin ATPase | `ntpase_nucleotide_hydrolase_boundary` | `oos_hard_negative` | `gold` | `tight_nucleotide_active_site_not_hydrolytic_parent` | `1Q3S` | ADP chaperonin ATPase context | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 42 | `m_csa:533` G-protein alpha subunit, group I (GTPase) | `ntpase_nucleotide_hydrolase_boundary` | `oos_hard_negative` | `gold` | `tight_nucleotide_active_site_not_hydrolytic_parent` | `1BH2` | GTPase switch context with GSP analog | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 43 | `m_csa:534` myosin ATPase | `ntpase_nucleotide_hydrolase_boundary` | `oos_hard_negative` | `gold` | `tight_nucleotide_active_site_not_hydrolytic_parent` | `1VOM` | ADP/Mg/vanadate myosin ATPase context | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 44 | `m_csa:535` protein-synthesizing GTPase (elongation factor Tu) | `ntpase_nucleotide_hydrolase_boundary` | `near_family_hard_negative` | `review-only` | `tight_nucleotide_active_site_parent_collision` | `4PC7` | GNP/Mg EF-Tu context currently broad-parent positive | reject_or_abstain_from metal_dependent_hydrolase despite local family simil... |
| 45 | `m_csa:642` vesicle-fusing ATPase | `ntpase_nucleotide_hydrolase_boundary` | `review_only_positive_lead` | `review-only` | `loose_open_or_interdomain_geometry` | `1NSF` | ATP/Mg context in vesicle-fusing ATPase | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 46 | `m_csa:656` adenosinetriphosphatase | `ntpase_nucleotide_hydrolase_boundary` | `review_only_positive_lead` | `review-only` | `nucleotide_context_review_needed` | `1KAZ` | K ion present; nucleotide hydrolase mechanism but selected ligand sta... | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 47 | `m_csa:844` dUTP diphosphatase | `ntpase_nucleotide_hydrolase_boundary` | `review_only_positive_lead` | `review-only` | `loose_open_or_interdomain_geometry` | `1DUP` | expected cofactor absent in selected dUTPase structure | route_or_abstain_in_review_only_until missing geometry/holo/product-state e... |
| 48 | `m_csa:216` carbonate dehydratase (alpha class) | `carbonic_anhydrase_dehydratase_boundary` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1CA2` | Zn-bound water/hydroxide in alpha carbonic anhydrase | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 49 | `m_csa:516` carbonate dehydratase (gamma class) | `carbonic_anhydrase_dehydratase_boundary` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1QRG` | Zn-bound gamma carbonic anhydrase site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 50 | `m_csa:517` carbonate dehydratase (beta class) | `carbonic_anhydrase_dehydratase_boundary` | `positive_anchor` | `gold` | `tight_active_site_geometry` | `1I6P` | Zn-bound beta carbonic anhydrase site | route_to_parent_metal_dependent_hydrolase_when metal-water and scissile-bon... |
| 51 | `m_csa:54` 3-dehydroquinate dehydratase (type I) | `carbonic_anhydrase_dehydratase_boundary` | `oos_hard_negative` | `gold` | `nonhydrolytic_dehydration_geometry` | `1QFE` | no metal hydrolase ligand state; Schiff-base/dehydration context | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 52 | `m_csa:55` 3-dehydroquinate dehydratase (type II) | `carbonic_anhydrase_dehydratase_boundary` | `oos_hard_negative` | `gold` | `nonhydrolytic_dehydration_geometry` | `1GU1` | acid/base dehydration context, no metal-water hydrolysis | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 53 | `m_csa:361` aldoxime dehydratase | `carbonic_anhydrase_dehydratase_boundary` | `oos_hard_negative` | `gold` | `nonhydrolytic_dehydration_geometry` | `3A15` | heme aldoxime dehydratase active site | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 54 | `m_csa:750` 4-hydroxybutanoyl-CoA dehydratase | `carbonic_anhydrase_dehydratase_boundary` | `oos_hard_negative` | `gold` | `nonhydrolytic_dehydration_geometry` | `1U8V` | FAD/Fe-S radical dehydratase state | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 55 | `m_csa:57` nitrile hydratase | `metal_dependent_nonhydrolytic_negative` | `oos_hard_negative` | `gold` | `nonhydrolytic_metal_hydration_geometry` | `2AHJ` | Fe nitrile hydratase with modified Cys ligands | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 56 | `m_csa:995` oxalate oxidase | `metal_dependent_nonhydrolytic_negative` | `oos_hard_negative` | `gold` | `nonhydrolytic_oxidase_geometry` | `2ET1` | metal oxidase context, no scissile-bond hydrolysis | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 57 | `m_csa:925` Nitrate reductase [NADH] | `metal_dependent_nonhydrolytic_negative` | `oos_hard_negative` | `gold` | `nonhydrolytic_redox_geometry` | `2BII` | molybdopterin/redox nitrate reductase context | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 58 | `m_csa:936` protocatechuate 3,4-dioxygenase | `metal_dependent_nonhydrolytic_negative` | `oos_hard_negative` | `gold` | `nonhydrolytic_dioxygenase_geometry` | `3PCA` | Fe/catechol dioxygenase context | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 59 | `m_csa:997` lanthanide-dependent methanol dehydrogenase | `metal_dependent_nonhydrolytic_negative` | `oos_hard_negative` | `gold` | `nonhydrolytic_redox_geometry` | `6FKW` | lanthanide/PQQ methanol dehydrogenase active site | reject_or_abstain_from metal_dependent_hydrolase; use as route-away control |
| 60 | `uniprot:P12821` Angiotensin-converting enzyme | `zinc_metalloprotease_zincin` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `1O86,1O8A,1UZE` | two Zn-dependent peptidase domains; UniProt reviewed EC 3.4.15.1 | review_only external positive lead; no import or countable support until du... |
| 61 | `uniprot:P08253` 72 kDa type IV collagenase / MMP2 | `zinc_metalloprotease_zincin` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `1CK7,1CXW,1EAK` | Zn metalloprotease with MMP catalytic domain and structural Zn/Ca sites | review_only external positive lead; no import or countable support until du... |
| 62 | `uniprot:P45452` Collagenase 3 / MMP13 | `zinc_metalloprotease_zincin` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `1EUB,1FLS,1FM1` | Zn metalloprotease; UniProt reviewed MMP collagenase | review_only external positive lead; no import or countable support until du... |
| 63 | `uniprot:P00800` Thermolysin | `zinc_metalloprotease_zincin` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `1FJ3,1FJO,1FJQ` | Zn thermolysin metalloprotease; reviewed EC 3.4.24.27 | review_only external positive lead; no import or countable support until du... |
| 64 | `uniprot:C7C422` Metallo-beta-lactamase NDM-1 | `metallo_beta_lactamase_like` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `3PG4,3RKJ,3RKK` | binuclear Zn metallo-beta-lactamase; reviewed EC 3.5.2.6 | review_only external positive lead; no import or countable support until du... |
| 65 | `uniprot:Q79MP6` Metallo-beta-lactamase VIM-like enzyme | `metallo_beta_lactamase_like` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `1DDK,1JJE,1JJT` | Zn metallo-beta-lactamase; reviewed EC 3.5.2.6 | review_only external positive lead; no import or countable support until du... |
| 66 | `uniprot:P52699` Metallo-beta-lactamase IMP-1 | `metallo_beta_lactamase_like` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `1DD6,1VGN,1WUO` | Zn metallo-beta-lactamase IMP-1; reviewed EC 3.5.2.6 | review_only external positive lead; no import or countable support until du... |
| 67 | `uniprot:P00918` Carbonic anhydrase 2 | `carbonic_anhydrase_dehydratase_boundary` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `12CA,1A42,1AM6` | Zn-water reversible carbonate dehydratase; reviewed EC 4.2.1.1 | review_only external positive lead; no import or countable support until du... |
| 68 | `uniprot:P15289` Arylsulfatase A | `sulfatase_fgly_metal_boundary` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `1AUK,1E1Z,1E2S` | FGly/formylglycine sulfatase with metal stabilization; reviewed EC 3.... | review_only external positive lead; no import or countable support until du... |
| 69 | `uniprot:P22304` Iduronate 2-sulfatase | `sulfatase_fgly_metal_boundary` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `5FQL,6IOZ` | FGly sulfatase family; reviewed EC 3.1.6.13 | review_only external positive lead; no import or countable support until du... |
| 70 | `uniprot:P00634` Alkaline phosphatase | `phosphatase_phosphoesterase` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `1AJA,1AJB,1AJC` | Zn/Mg alkaline phosphatase; reviewed EC 3.1.3.1 | review_only external positive lead; no import or countable support until du... |
| 71 | `uniprot:P0A7Y4` Ribonuclease HI | `nuclease_phosphoesterase` | `external_positive_lead` | `silver` | `tight_active_site_geometry` | `1F21,1G15,1GOA` | Mg-dependent RNase H phosphodiester hydrolysis; reviewed EC 3.1.26.4 | review_only external positive lead; no import or countable support until du... |
| 72 | `uniprot:P0A6P9` Enolase | `metal_dependent_nonhydrolytic_negative` | `external_hard_negative` | `gold` | `nonhydrolytic_active_site` | `1E9I,2FYM,3H8A` | Mg-dependent lyase/dehydratase, not hydrolysis; reviewed EC 4.2.1.11 | review_only external hard negative; no import and should route away or abstain |
| 73 | `uniprot:P01112` GTPase HRas | `ntpase_nucleotide_hydrolase_boundary` | `external_hard_negative` | `gold` | `tight_nucleotide_active_site_not_hydrolytic_parent` | `121P,1AA9,1AGP` | Mg/GTPase switch protein; reviewed EC 3.6.5.2 | review_only external hard negative; no import and should route away or abstain |
| 74 | `uniprot:P61586` Transforming protein RhoA | `ntpase_nucleotide_hydrolase_boundary` | `external_hard_negative` | `gold` | `tight_nucleotide_active_site_not_hydrolytic_parent` | `1A2B,1CC0,1CXZ` | Mg/GTPase switch protein; reviewed EC 3.6.5.2 | review_only external hard negative; no import and should route away or abstain |

## Decision Gates

Keep broad v1 parent only if:

- Across gold/silver positive rows, source-free evidence must recover metal count, metal ligands, water/hydroxide activation, and scissile-bond atom class without relying on EC/name/cofactor text.
- False-positive rate on NTPase/GTPase/ATPase, kinase, carbonic/dehydratase, and nonhydrolytic metal controls must remain at or below 5 percent, with all high-confidence controls rejecting or abstaining.
- Loose/open, apo, and product-context rows must abstain or emit explicit evidence-blocker reasons rather than becoming confident parent positives.
- External positives may support broad v1 only after current-reference sequence and Foldseek duplicate screens pass and at least three non-M-CSA external rows per major lane have extracted active-site geometry.

Create child strata if:

- Create a child if a lane has at least six gold/silver positives across at least three sequence/Foldseek neighborhoods plus paired sibling hard negatives, and the child reaction-center evidence can be extracted source-free.
- Candidate children to evaluate first: zincin_metalloprotease, binuclear_amidohydrolase, phosphatase/nuclease_phosphoesterase, metallo_beta_lactamase_like, sulfatase_FGly, and carbonic_anhydrase_dehydratase.
- A child is required if broad parent routing is correct but sibling confusion exceeds 10 percent within gold/silver rows or if learned/geometry ablations show separable active-site evidence beyond metal presence.
- NTPase/nucleotide hydrolase should start as a boundary/offramp, not a positive child, unless the ontology explicitly admits nucleotide hydrolysis as a separate child with motor/switch controls.

Make `metal_dependent_hydrolase` router-only if:

- If broad parent evidence reliably detects metal-water chemistry but cannot decide attacked atom class or reaction family, keep metal_dependent_hydrolase as a router-only parent and require child/offramp decisions downstream.
- If FGly/sulfatase, carbonic anhydrase, or NTPase rows need special rules that conflict with phosphatase/nuclease/zincin positives, do not use the parent as a terminal production label.
- If external rows only pass because of metal/cofactor/name text and fail EC/name/cofactor ablations, freeze the parent as review-only routing evidence until child strata or negative offramps are specified.

## Validation Plan

- Run sequence-neighbor checks against current M-CSA references and external all-vs-all controls before promoting any external row.
- Run Foldseek/current-countable structure screens for every external lead and for local loose/open or apo/holo rows that need alternate structures.
- Extract metal count, metal ligands, water/hydroxide state, attacked atom, and substrate/analog state source-free from structures.
- Report parent route, child/offramp route, abstention, and hard-negative failure rates separately by lane and geometry class.

## Source Links

- UniProt REST batch template: https://rest.uniprot.org/uniprotkb/accessions?accessions=<accessions>&fields=accession,reviewed,protein_name,gene_names,organism_name,ec,xref_pdb,xref_alphafolddb,cc_catalytic_activity,cc_cofactor,ft_act_site,ft_binding
- M-CSA API example: https://www.ebi.ac.uk/thornton-srv/m-csa/api/entries/?format=json&entries.mcsa_ids=171
- RCSB structure pages are recorded per row in the JSON `source_urls` field.

## Verification Targets

- JSON parse: `artifacts/v3_external_metal_hydrolase_tail_panel_20260528.json`
- CLI validation: `PYTHONPATH=src python -m catalytic_earth.cli validate`
- Whitespace: `git diff --check`
