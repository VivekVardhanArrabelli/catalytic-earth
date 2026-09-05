# Atlas-50 computational panel review

**Status:** agent-generated review aid; zero human reviewers; no Phase B review coverage; no tier upgrade; no selection freeze.

This bounded pass checked all 40 Phase B panel packets against the live official M-CSA API and examined official RCSB structure metadata for six decision-relevant rows. It does not replace the real-human review required by `review_spec.json`. Every row remains unreviewed under that contract, and every suggested action below is a **HOLD** for attributable human adjudication.

## What was verified

All 40 rows exactly matched the live M-CSA response for EC numbers, UniProt IDs, PDB IDs, CATH IDs, numeric ChEBI IDs, detailed/non-detailed status, and mechanism-proposal count. This is a source-transcription result, not a scientific endorsement of any gate. M0970's non-ChEBI placeholder `X00676` was inspected separately and excluded from the numeric ChEBI comparison.

The M-CSA receipt was retrieved on 2026-09-05 from the exact 40-ID official API query, was 721,603 bytes, and had SHA-256 `0fdb9641822cfb78c095e0f4f54d2b81f92c54c854ae03b53892b20988b562cf`. Targeted RCSB entry and entity receipts are recorded with URLs, byte counts, and hashes in `data/atlas/atlas50/computational_review/panel_review.json`. Total external response data for this pass was 1,125,005 bytes, below the 30 MiB ceiling. No raw upstream response or article body is committed.

The five machine-draft gates were inspected across the queue. The source transcription and bounded provenance receipts are verified. Diversity remains a machine-draft stratification judgment. The identifiers-and-links rights boundary remains intact. Shared-representation and tier readiness remain scientifically unresolved, with the six rows below needing priority review. The three non-detailed entries M0767, M0851, and M0935 retain mandatory Tier 1 and Tier 2 abstention; M0204 retains its Tier 2 abstention.

## Priority HOLD queue

| Candidate | Verified evidence | Why the current decision needs review | Suggested action |
|---|---|---|---|
| [M0064](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/64/) DNA topoisomerase III | M-CSA marks the reaction polymeric and shows single-stranded DNA on both sides. [RCSB 1D6M](https://data.rcsb.org/rest/v1/core/entry/1D6M) contains only the P14294 protein polymer entity and no DNA entity. | The selected structure does not ground the DNA/topological state, and the projected generic reaction object does not yet show how initial versus final topology is encoded. | **HOLD proposed inclusion and Tier 0/Tier 2 expectations** until a generic topology/reaction-state contract and applicable evidence are demonstrated. |
| [M0106](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/106/) pyruvate dehydrogenase E1 | M-CSA consumes a protein-tethered lipoyl-lysine residue. [RCSB 1W85](https://data.rcsb.org/rest/v1/core/entry/1W85) contains E1 alpha P21873, E1 beta P21874, and E2 binding-domain entity P11961. | The M-CSA source identity is correctly transcribed as E1 only, but the structure and reaction applicability require explicit E2 carrier/domain context. | **HOLD proposed inclusion and Tier 2** until tethered-carrier identity/state is generic and P11961 is scoped as structure context rather than M-CSA identity. |
| [M0107](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/107/) aerobic carbon monoxide dehydrogenase | M-CSA identifies P19919/P19920/P19921 and an electron path through Mo-Cu, two iron-sulfur clusters, FAD, and an external acceptor. [RCSB 1N62](https://data.rcsb.org/rest/v1/core/entry/1N62) has the matching three protein entities. | This row passes representation while M0212 fails for the same generic class of coupled component, metallocluster, and state-transition provenance. No source-neutral distinction is documented. | **HOLD proposed inclusion** and apply the same generic contract test used for M0212. |
| [M0212](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/212/) nitrogenase | M-CSA identifies P07328/P07329/P00459 with ATP/ADP, nitrogen/hydrogen/ammonium, and iron-sulfur states. [RCSB 1N2C](https://data.rcsb.org/rest/v1/core/entry/1N2C) contains the two MoFe-protein entities and iron-protein entity in an ADP-tetrafluoroaluminate-stabilized complex. | The evidence supports the existing generic-contract blocker and establishes the comparison that M0107 must also pass. | **HOLD current fail-closed exclusion** until the generic coupled-component, nucleotide, and metallocluster-state contract is validated. |
| [M0753](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/753/) imidazole glycerol phosphate synthase | The exact M-CSA reaction uses free ammonium and identifies only HisF Q9X0C6. [RCSB 2A0N](https://data.rcsb.org/rest/v1/core/entry/2A0N) is likewise HisF alone. | The packet's channel/allostery blocker concerns the full synthase complex, but the selected source handle does not contain HisH or a channelled intermediate. Applicability must be resolved before representation. | **HOLD current fail-closed exclusion**; first distinguish the isolated HisF half-reaction from the coupled complex, then assess the generic channel-state contract. |
| [M0970](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/970/) peptidoglycan glycosyltransferase | M-CSA contains a polymeric reactant name, non-ChEBI product placeholder `X00676`, two detailed proposals, and an `is_polymeric=false` flag. [RCSB 3VMT](https://data.rcsb.org/rest/v1/core/entry/3VMT) is a monofunctional glycosyltransferase with a Lipid II analog. | The exact source does not establish a balanced reaction instance, chain length, initiation/elongation boundary, or processivity. | **HOLD current fail-closed exclusion** until a generic polymer reaction-instance contract and adjudicated reaction source exist. |

The paper DOI links recorded in the JSON are M-CSA-surfaced reference metadata. Their article bodies were not inspected, so they are pointers for human review rather than claim-level verification.

## Full 40-row coverage

`Targeted` means official reaction/structure metadata was inspected beyond transcription. `Transcription` means all five gates and the packet boundaries were inspected, but only the listed source fields were independently checked; scientific outcomes remain unresolved.

| # | Candidate | Phase A proposal | Depth | Tier boundary | Computational action |
|---:|---|---|---|---|---|
| 1 | [M0001 Glutamate racemase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/1/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 2 | [M0007 Isocitrate dehydrogenase (NADP+)](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/7/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 3 | [M0014 Vanadate-dependent chloride peroxidase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/14/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 4 | [M0031 Thymidylate synthase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/31/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 5 | [M0034 Catechol 2,3-dioxygenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/34/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 6 | [M0049 Histidine decarboxylase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/49/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 7 | [M0050 Orotidine 5'-phosphate decarboxylase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/50/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 8 | [M0052 Fructose-bisphosphate aldolase, class II](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/52/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 9 | [M0064 DNA topoisomerase III](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/64/) | include | Targeted | Tier 0/Tier 2 held | HOLD before freeze |
| 10 | [M0081 Chorismate mutase AroQ class](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/81/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 11 | [M0099 Cytochrome-dependent methanol dehydrogenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/99/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 12 | [M0106 Pyruvate dehydrogenase E1](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/106/) | include | Targeted | Tier 2 held | HOLD before freeze |
| 13 | [M0107 Aerobic carbon monoxide dehydrogenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/107/) | include | Targeted | Tier 1/Tier 2 held | HOLD before freeze |
| 14 | [M0121 Sulfite oxidase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/121/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 15 | [M0126 Cytochrome-c3 hydrogenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/126/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 16 | [M0127 Ferredoxin hydrogenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/127/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 17 | [M0128 Firefly luciferase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/128/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 18 | [M0129 Taurine dioxygenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/129/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 19 | [M0132 Alkanal monooxygenase (FMN-linked)](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/132/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 20 | [M0133 Cytochrome P450cam](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/133/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 21 | [M0135 Peptidylglycine monooxygenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/135/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 22 | [M0139 Xanthine dehydrogenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/139/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 23 | [M0145 Isopenicillin N synthase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/145/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 24 | [M0174 Papain](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/174/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 25 | [M0190 Isopentenyl-diphosphate delta-isomerase, type I](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/190/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 26 | [M0191 Protein disulfide isomerase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/191/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 27 | [M0204 Uroporphyrinogen-III synthase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/204/) | include | Transcription | Tier 2 abstention retained | HOLD for human review |
| 28 | [M0212 Nitrogenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/212/) | exclude blocked | Targeted | All tiers held | HOLD current exclusion |
| 29 | [M0219 Transketolase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/219/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 30 | [M0222 Fructose-bisphosphate aldolase, class I](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/222/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 31 | [M0753 Imidazole glycerol phosphate synthase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/753/) | exclude blocked | Targeted | All tiers held | HOLD exclusion; review source scope first |
| 32 | [M0767 Biotin synthase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/767/) | include | Transcription | Tier 1/Tier 2 abstention retained | HOLD for human review |
| 33 | [M0797 Ribulose-bisphosphate carboxylase/oxygenase, form II](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/797/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 34 | [M0851 Glutathione peroxidase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/851/) | include | Transcription | Tier 1/Tier 2 abstention retained | HOLD for human review |
| 35 | [M0907 Ribulose-bisphosphate carboxylase/oxygenase, form I](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/907/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 36 | [M0935 Nitric oxide synthase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/935/) | include | Transcription | Tier 1/Tier 2 abstention retained | HOLD for human review |
| 37 | [M0970 Peptidoglycan glycosyltransferase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/970/) | exclude blocked | Targeted | All tiers held | HOLD current exclusion |
| 38 | [M0980 Ferredoxin:thioredoxin reductase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/980/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 39 | [M0991 IspG](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/991/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |
| 40 | [M0997 Lanthanide-dependent methanol dehydrogenase](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/997/) | include | Transcription | Tiers 0/1/2 remain contingent | HOLD for human review |

## Review boundary and next action

The targeted evidence supports keeping all three machine-draft exclusions fail-closed. It adds three proposed inclusions, M0064, M0106, and M0107, to the priority HOLD queue because their representation or structure-applicability assumptions need a generic, cross-row explanation before freeze. M0753's blocker should be reviewed only after the exact source scope is established.

The next valid step is a real-human panel review using the Phase B intake contract, starting with these six rows and preserving unresolved outcomes. This agent artifact must not be counted as a submission or used to regenerate the freeze candidate by itself.
