# PLP Child-Mechanism External Stress Panel 20260528

Validation-panel design and source/evidence scouting only. No labels, registries, ontologies, thresholds, production scoring, imports, or model outputs were edited.

## Scope And Inputs

- Candidate rows/leads: 50 across requested 30-80 range.
- Disk guardrail: the first `df` check reported about 4.8 GiB free, but environment cleanup/pruning recovered space before artifact write; 20.76 GiB was available at write time. This run performed no large downloads and wrote only small text/JSON artifacts.
- Main local inputs: current702 labels, geometry features, fold/coordinate readiness, sequence-NN manifest, learned retrieval manifest interface, PLP aminotransferase mini-campaign rollups, m_csa:737 coupled PLP-cobalamin schema decision, and prior Q9BXD5/P06746 Schiff-base controls.
- External spot checks used official M-CSA and UniProt REST metadata only; structure availability is represented as local selected PDB IDs or public PDB references, not newly downloaded coordinates.

## Readiness By Stratum

| Stratum | Tier | Rows | What It Can Test | Missing Evidence |
| --- | --- | ---: | --- | --- |
| `aminotransferase` | silver | 11 | positive child stratum and parent PLP cofactor-control slice | source-free amino-donor/acceptor atom mapping and external-aldimine/product-state annotation; fold-diverse external positives that pass targeted current-PLP duplicate screens; child-specific negatives inside the same PLP fold after cofactor/name ablation |
| `decarboxylase` | bronze | 3 | positive child stratum with ornithine/dealkylglycine decarboxylase controls | source-free carboxylate-position evidence and CO2-loss reaction-center annotation; at least three additional fold-diverse PLP decarboxylase positives; near-family PLP lyase/racemase controls with similar PLP internal aldimine geometry |
| `racemase_epimerase` | bronze | 2 | positive child stratum plus non-PLP racemase OOS contrast | more PLP racemase/epimerase positives outside the alanine/serine pair; source-free dual-face acid/base geometry and stereochemical product-state evidence; tests that reject non-PLP racemase wording without relying on PLP presence alone |
| `lyase_eliminase` | bronze | 9 | positive child stratum, including beta-elimination and C-S/N-S cleavage | source-free leaving-group atom and quinonoid/external-aldimine state evidence; evidence-complete external Q96I15-like lyase rows before use as support; hard negatives where lyase wording is non-PLP or heme/flavin-associated |
| `beta_gamma_replacement` | bronze | 5 | positive child stratum for beta/gamma substitution and replacement chemistry | explicit beta/gamma atom mapping with entering and leaving group identities; substrate/analog complexes that distinguish replacement from simple elimination; cross-stratum negatives from aminotransferases and decarboxylases in similar PLP folds |
| `plp_adjacent_boundary` | review-only | 7 | near-family hard negatives for requested children inside the broad PLP parent | negative labels or evaluation-only child exclusions for PLP-parent rows outside requested strata; ablation tests showing cofactor recognition alone does not trigger a child mechanism |
| `coupled_plp_adenosylcobalamin_aminomutase` | review-only | 1 | coupled-cofactor boundary and beta-lysine aminomutase schema-gap sentinel | dedicated coupled PLP-adenosylcobalamin ontology/fingerprint specification; independent positive exemplars beyond m_csa:737; PLP-only, cobalamin-only, and radical-SAM aminomutase controls under a leakage-audited schema |
| `cobalamin_only_boundary` | review-only | 2 | near-family hard negatives for coupled PLP+B12 and PLP child rows | paired split design with m_csa:737 after coupled-family schema exists; geometry channel that distinguishes absent PLP from coupled PLP+B12 active sites |
| `non_plp_schiff_base_hard_negative` | silver | 8 | hard negatives for PLP and child strata under Schiff-base/name leakage | source-free Schiff-base axis extraction for current M-CSA control rows; Foldseek/current-countable duplicate screens for external Q9BXD5 and P06746 control rows; negative-control calibration against PLP lyases after text/name ablation |
| `non_plp_racemase_oos_control` | bronze | 1 | OOS control for racemase wording without PLP | more non-PLP racemase/epimerase controls with local coordinate evidence |
| `non_plp_aminomutase_boundary` | bronze | 1 | aminomutase-name hard negative outside PLP/B12 | additional MIO/radical-SAM/non-PLP aminomutase controls with structure and split assignments |

## Candidate Rows

Full row metadata is in the JSON artifact. This table keeps the review surface compact.

| Row | Stratum | Role | Tier | Structure | PLP/LLP State | Sequence/Foldseek Expectation |
| --- | --- | --- | --- | --- | --- | --- |
| `m_csa:249` | `aminotransferase` | `positive` | silver | 1DTY | plp_family_holo_or_analog_state | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `m_csa:411` | `aminotransferase` | `positive` | silver | 1AY4 | plp_family_holo_or_analog_state | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `m_csa:424` | `aminotransferase` | `positive` | silver | 1BJO | covalent_lysine_plp_internal_aldimine_or_llp_state | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `m_csa:66` | `aminotransferase` | `positive` | silver | 1DAA | plp_family_holo_or_analog_state | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `m_csa:854` | `aminotransferase` | `positive` | silver | 1OHV | plp_family_holo_or_analog_state | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `uniprot:P50457` | `aminotransferase` | `external_positive_like_terminal_duplicate_control` | silver | 7JH3 | covalent_lysine_plp_internal_aldimine_or_llp_state | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `uniprot:P53555` | `aminotransferase` | `external_positive_like_terminal_duplicate_control` | silver | 3DOD | plp_family_holo_or_analog_state | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `uniprot:P96060` | `aminotransferase` | `external_positive_like_insufficient_evidence_control` | silver | 1M32 | no_plp_family_ligand_observed_in_selected_structure | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `uniprot:Q72LL6` | `aminotransferase` | `external_positive_like_terminal_duplicate_control` | silver | 2EGY | no_plp_family_ligand_observed_in_selected_structure | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `uniprot:Q8TD30` | `aminotransferase` | `external_positive_like_terminal_duplicate_control` | silver | 3IHJ | plp_family_holo_or_analog_state | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `uniprot:Q9Y617` | `aminotransferase` | `external_positive_like_terminal_duplicate_control` | silver | 3E77 | plp_family_holo_or_analog_state | expect same-fold PLP aminotransferase neighbors; child-readiness requires separation from PLP lyases, decarboxylases,... |
| `m_csa:383` | `beta_gamma_replacement` | `positive` | bronze | 1A50 | plp_family_holo_or_analog_state | expect structural neighbor bleed between beta/gamma PLP lyases and replacement enzymes; readiness requires substrate-... |
| `m_csa:449` | `beta_gamma_replacement` | `positive` | bronze | 1CL1 | covalent_lysine_plp_internal_aldimine_or_llp_state | expect structural neighbor bleed between beta/gamma PLP lyases and replacement enzymes; readiness requires substrate-... |
| `m_csa:759` | `beta_gamma_replacement` | `positive` | bronze | 1CS1 | covalent_lysine_plp_internal_aldimine_or_llp_state | expect structural neighbor bleed between beta/gamma PLP lyases and replacement enzymes; readiness requires substrate-... |
| `m_csa:865` | `beta_gamma_replacement` | `positive` | bronze | 1OAS | plp_family_holo_or_analog_state | expect structural neighbor bleed between beta/gamma PLP lyases and replacement enzymes; readiness requires substrate-... |
| `m_csa:933` | `beta_gamma_replacement` | `positive` | bronze | 2TPL | covalent_lysine_plp_internal_aldimine_or_llp_state | expect structural neighbor bleed between beta/gamma PLP lyases and replacement enzymes; readiness requires substrate-... |
| `m_csa:62` | `cobalamin_only_boundary` | `near_family_hard_negative` | review-only | 1REQ | cobalamin_without_plp_observed | expect cobalamin radical neighbors without PLP; should remain outside PLP child strata |
| `m_csa:63` | `cobalamin_only_boundary` | `near_family_hard_negative` | review-only | 1CB7 | cobalamin_without_plp_observed | expect cobalamin radical neighbors without PLP; should remain outside PLP child strata |
| `m_csa:737` | `coupled_plp_adenosylcobalamin_aminomutase` | `boundary_positive_review_only` | review-only | 1XRS | coupled_plp_and_cobalamin_context | expect cobalamin/radical rearrangement and PLP pocket signals together; production child calls must abstain or route ... |
| `m_csa:482` | `decarboxylase` | `positive` | bronze | 1D7R | plp_family_holo_or_analog_state | expect high structural similarity within ODC-like decarboxylases and possible PLP-fold neighbors outside decarboxylat... |
| `m_csa:860` | `decarboxylase` | `positive` | bronze | 1ORD | plp_family_holo_or_analog_state | expect high structural similarity within ODC-like decarboxylases and possible PLP-fold neighbors outside decarboxylat... |
| `m_csa:937` | `decarboxylase` | `positive` | bronze | 7ODC | plp_family_holo_or_analog_state | expect high structural similarity within ODC-like decarboxylases and possible PLP-fold neighbors outside decarboxylat... |
| `m_csa:186` | `lyase_eliminase` | `positive` | bronze | 1PWH | plp_family_holo_or_analog_state | expect mixed PLP-fold neighbors and name leakage; valid child signal must distinguish elimination from replacement/ad... |
| `m_csa:286` | `lyase_eliminase` | `positive` | bronze | 2Z67 | plp_family_holo_or_analog_state | expect mixed PLP-fold neighbors and name leakage; valid child signal must distinguish elimination from replacement/ad... |
| `m_csa:305` | `lyase_eliminase` | `positive` | bronze | 1ET0 | plp_family_holo_or_analog_state | expect mixed PLP-fold neighbors and name leakage; valid child signal must distinguish elimination from replacement/ad... |
| `m_csa:410` | `lyase_eliminase` | `positive` | bronze | 1AX4 | covalent_lysine_plp_internal_aldimine_or_llp_state | expect mixed PLP-fold neighbors and name leakage; valid child signal must distinguish elimination from replacement/ad... |
| `m_csa:418` | `lyase_eliminase` | `positive` | bronze | 1B8G | plp_family_holo_or_analog_state | expect mixed PLP-fold neighbors and name leakage; valid child signal must distinguish elimination from replacement/ad... |
| `m_csa:742` | `lyase_eliminase` | `positive` | bronze | 1QZ9 | plp_family_holo_or_analog_state | expect mixed PLP-fold neighbors and name leakage; valid child signal must distinguish elimination from replacement/ad... |
| `m_csa:855` | `lyase_eliminase` | `positive` | bronze | 1I29 | plp_family_holo_or_analog_state | expect mixed PLP-fold neighbors and name leakage; valid child signal must distinguish elimination from replacement/ad... |
| `m_csa:956` | `lyase_eliminase` | `positive` | bronze | 2ZR8 | plp_family_holo_or_analog_state | expect mixed PLP-fold neighbors and name leakage; valid child signal must distinguish elimination from replacement/ad... |
| `uniprot:Q96I15` | `lyase_eliminase` | `external_lead_missing_evidence` | review-only | 3GZC | no_plp_family_ligand_observed_in_selected_structure | expect mixed PLP-fold neighbors and name leakage; valid child signal must distinguish elimination from replacement/ad... |
| `m_csa:245` | `non_plp_aminomutase_boundary` | `hard_negative` | bronze | 2RJR | no_plp_family_ligand_observed_in_selected_structure | expect MIO/non-PLP active-site context; should stay outside PLP and coupled PLP+B12 child strata |
| `m_csa:1` | `non_plp_racemase_oos_control` | `oos_control` | bronze | 1B73 | no_plp_family_ligand_observed_in_selected_structure | expect no PLP-family neighbor requirement; should abstain from PLP racemase despite racemase name |
| `m_csa:148` | `non_plp_schiff_base_hard_negative` | `hard_negative` | silver | 1ONR | no_plp_family_ligand_observed_in_selected_structure | expect no PLP-family cofactor signal; any PLP child hit would likely be cofactor/name leakage or generic Schiff-base ... |
| `m_csa:222` | `non_plp_schiff_base_hard_negative` | `hard_negative` | silver | 2QUT | no_plp_family_ligand_observed_in_selected_structure | expect no PLP-family cofactor signal; any PLP child hit would likely be cofactor/name leakage or generic Schiff-base ... |
| `m_csa:230` | `non_plp_schiff_base_hard_negative` | `hard_negative` | silver | 1GZG | no_plp_family_ligand_observed_in_selected_structure | expect no PLP-family cofactor signal; any PLP child hit would likely be cofactor/name leakage or generic Schiff-base ... |
| `m_csa:243` | `non_plp_schiff_base_hard_negative` | `hard_negative` | silver | 1HO1 | no_plp_family_ligand_observed_in_selected_structure | expect no PLP-family cofactor signal; any PLP child hit would likely be cofactor/name leakage or generic Schiff-base ... |
| `m_csa:267` | `non_plp_schiff_base_hard_negative` | `hard_negative` | silver | 1DHP | no_plp_family_ligand_observed_in_selected_structure | expect no PLP-family cofactor signal; any PLP child hit would likely be cofactor/name leakage or generic Schiff-base ... |
| `m_csa:54` | `non_plp_schiff_base_hard_negative` | `hard_negative` | silver | 1QFE | no_plp_family_ligand_observed_in_selected_structure | expect no PLP-family cofactor signal; any PLP child hit would likely be cofactor/name leakage or generic Schiff-base ... |
| `uniprot:P06746` | `non_plp_schiff_base_hard_negative` | `external_hard_negative_review_only` | silver | 1BPX | no_plp_family_ligand_observed_in_selected_structure | expect no PLP-family cofactor signal; any PLP child hit would likely be cofactor/name leakage or generic Schiff-base ... |
| `uniprot:Q9BXD5` | `non_plp_schiff_base_hard_negative` | `external_hard_negative_review_only` | silver | 6ARH | no_plp_family_ligand_observed_in_selected_structure | expect no PLP-family cofactor signal; any PLP child hit would likely be cofactor/name leakage or generic Schiff-base ... |
| `m_csa:147` | `plp_adjacent_boundary` | `near_family_hard_negative` | review-only | 1LS3 | plp_family_holo_or_analog_state | expect PLP cofactor and sometimes close structural neighbors; child model must abstain unless requested-child reactio... |
| `m_csa:195` | `plp_adjacent_boundary` | `near_family_hard_negative` | review-only | 2GSA | pyridoxamine_or_plp_product/intermediate_state | expect PLP cofactor and sometimes close structural neighbors; child model must abstain unless requested-child reactio... |
| `m_csa:205` | `plp_adjacent_boundary` | `near_family_hard_negative` | review-only | 1GPB | plp_family_holo_or_analog_state | expect PLP cofactor and sometimes close structural neighbors; child model must abstain unless requested-child reactio... |
| `m_csa:358` | `plp_adjacent_boundary` | `near_family_hard_negative` | review-only | 2A5H | plp_family_holo_or_analog_state | expect PLP cofactor and sometimes close structural neighbors; child model must abstain unless requested-child reactio... |
| `m_csa:419` | `plp_adjacent_boundary` | `near_family_hard_negative` | review-only | 1B9H | plp_family_holo_or_analog_state | expect PLP cofactor and sometimes close structural neighbors; child model must abstain unless requested-child reactio... |
| `m_csa:430` | `plp_adjacent_boundary` | `near_family_hard_negative` | review-only | 1BS0 | no_plp_family_ligand_observed_in_selected_structure | expect PLP cofactor and sometimes close structural neighbors; child model must abstain unless requested-child reactio... |
| `m_csa:762` | `plp_adjacent_boundary` | `near_family_hard_negative` | review-only | 1FC4 | plp_family_holo_or_analog_state | expect PLP cofactor and sometimes close structural neighbors; child model must abstain unless requested-child reactio... |
| `m_csa:213` | `racemase_epimerase` | `positive` | bronze | 1L6G | plp_family_holo_or_analog_state | expect sparse sequence support and same-structure/fold conflicts for serine racemase versus serine ammonia-lyase; chi... |
| `m_csa:330` | `racemase_epimerase` | `positive` | bronze | 2ZR8 | plp_family_holo_or_analog_state | expect sparse sequence support and same-structure/fold conflicts for serine racemase versus serine ammonia-lyase; chi... |

## Decision Gates

- Each promoted child must have at least six gold/silver positives across at least three sequence/Foldseek clusters, with no single cluster contributing more than half of positives.
- Each child must have within-parent PLP sibling hard negatives and non-PLP Schiff-base/OOS controls in the same evaluation split design.
- Source-free geometry must identify PLP/LLP/PMP state plus the child reaction-center evidence: amino transfer donor/acceptor, decarboxylated carboxylate, racemization dual-face acid/base, elimination leaving group, or beta/gamma replacement entering/leaving group.
- External positive-like rows must clear exact sequence, UniRef-style, and Foldseek/TM duplicate screens before they count as support.
- PLP plus adenosylcobalamin aminomutase rows must abstain or route to the coupled review-only family until a dedicated schema and scorer exist.
- No child threshold or registry change is allowed until text/name/EC/cofactor-only ablations show signal survives without PLP recognition alone.

## Learned Representation Requirements

- Create evaluation-only child-stratum labels separate from production labels and keep them out of the canonical registry until gates pass.
- Materialize a row-level feature table with selected structure, active-site residue roles, PLP/LLP/PMP state, substrate/analog ligand state, sequence split, Foldseek nearest neighbors, and child/control role.
- Compute learned embeddings and geometry features under ablations that mask EC/name/reaction prose/cofactor-family fields; compare against cofactor-only and sequence-only baselines.
- Use cluster-preserving train/test splits based on sequence and Foldseek/TM neighbors before reporting child metrics.
- Report macro child F1, per-child AUROC/average precision, sibling-confusion matrix, OOS false-positive rate, and coupled-family abstention rate.

## Source Links

- M-CSA API query used for current rows: https://www.ebi.ac.uk/thornton-srv/m-csa/api/entries/?format=json&entries.mcsa_ids=1%2C54%2C62%2C63%2C66%2C147%2C148%2C186%2C195%2C205%2C213%2C222%2C230%2C243%2C245%2C249%2C267%2C286%2C305%2C330%2C358%2C383%2C410%2C411%2C418%2C419%2C424%2C430%2C449%2C482%2C737%2C742%2C759%2C762%2C854%2C855%2C860%2C865%2C933%2C937%2C956
- UniProt spot checks: https://rest.uniprot.org/uniprotkb/Q96I15.json, https://rest.uniprot.org/uniprotkb/Q9BXD5.json, https://rest.uniprot.org/uniprotkb/P06746.json
- Representative public structure pages are recorded per row in `source_urls.rcsb_structure` inside the JSON artifact.
