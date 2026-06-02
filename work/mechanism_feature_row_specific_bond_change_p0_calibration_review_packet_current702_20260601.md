# Mechanism Feature Row-Specific Bond-Change P0 Calibration Review Packet - current702

Run: 2026-06-02T06:44:57Z

Manual review packet for the calibration-assigned P0 rows that block the partial row-specific train/cal feature sidecar from supporting a no-template rerun.

## Status

- p0_calibration_review_packet_ready_manual_only
- Packet rows: 4
- Event rows: 16
- Critical violations: 0

## Rows

### m_csa:186

- Split: calibration
- Priority: P0.1_calibration_coverage_unblocker
- Reasons: calibration_coverage_absent, adds_unmaterialized_event_type
- Event types: bond_broken, bond_order_changed
- Blockers: review_status_not_approved

| event | confidence | mapped residues | source span |
| --- | --- | ---: | --- |
| bond_broken | medium | 1 | This PLP-depenedent reaction occurs via the initial elimination of water to form an enamine intermediate. |
| bond_order_changed | medium | 1 | This intermediate then undergoes tautomerisation to an imine form and finally the C-N bond is hydrolysed. |

Allowed decisions: approve_as_source_evidence_for_train_cal_features, rewrite_events_and_keep_review_pending, reject_for_row_specific_feature_consumption

### m_csa:147

- Split: calibration
- Priority: P0.1_calibration_coverage_unblocker
- Reasons: calibration_coverage_absent, adds_unmaterialized_event_type
- Event types: bond_order_changed, proton_transfer
- Blockers: review_status_not_approved, multi_event_mechanism_review

| event | confidence | mapped residues | source span |
| --- | --- | ---: | --- |
| bond_order_changed | medium | 1 | The serine substrate first forms the external aldimine by displacing Lys229 from the internal aldimine. |
| proton_transfer | medium | 2 | Glu57 abstracts the C3-OH proton, initiating the loss of formaldehyde from the intermediate leaving behind the glycine-quinoid aldimine. |
| bond_order_changed | medium | 1 | This rearranges to form the glycine aldimine. |
| bond_order_changed | medium | 1 | This intermediate is broken down by nucleophilic attack of Lys229 at the imine functionality, displacing glycine and reforming the internal aldimine, the enzyme resting state. |

Allowed decisions: approve_as_source_evidence_for_train_cal_features, rewrite_events_and_keep_review_pending, reject_for_row_specific_feature_consumption

### m_csa:6

- Split: calibration
- Priority: P0.1_calibration_coverage_unblocker
- Reasons: calibration_coverage_absent
- Event types: electron_transfer, proton_transfer
- Blockers: review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review

| event | confidence | mapped residues | source span |
| --- | --- | ---: | --- |
| electron_transfer | low | 0 | Initially, the enzyme is in the oxidised state, with its redox active cysteines 58 and 63 forming a disulphide bond to each other. |
| electron_transfer | low | 0 | A hydride is transferred from NAD(P)H to FAD, a process facilitated by Glu201, Lys66 and Tyr197, as demonstrated by mutagenesis and structural studies. |
| electron_transfer | low | 0 | From there the electron makes an SN2 attack on the sulfur atom of Cys63, causing Cys58 to be displaced as thiolate. |
| electron_transfer | low | 0 | This residue is now ready to attack the substrate, which in all cases except mercuric reductase is another disulphide bond. |
| proton_transfer | medium | 2 | His467 from the other subunit of the dimer has an essential role here, as shown by mutagenesis; first it seems to withdraw a proton from Cys58, activating the latter residue for... |

Allowed decisions: approve_as_source_evidence_for_train_cal_features, rewrite_events_and_keep_review_pending, reject_for_row_specific_feature_consumption

### m_csa:133

- Split: calibration
- Priority: P0.1_calibration_coverage_unblocker
- Reasons: calibration_coverage_absent
- Event types: bond_formed, electron_transfer, proton_transfer
- Blockers: review_status_not_approved, multi_event_mechanism_review, low_confidence_event_review

| event | confidence | mapped residues | source span |
| --- | --- | ---: | --- |
| electron_transfer | low | 0 | Putidaredoxin donates a single electron to the Fe(III) centre of the heme cofactor, forming Fe(II), which in turn donates the electron to the dioxygen substrate .Putidaredoxin t... |
| electron_transfer | low | 0 | Both Heme and Iron donate single electrons to the bound peroxo moiety, which eliminates water and initiates a proton transfer relay through the same chain as used previously. |
| proton_transfer | medium | 3 | The iron-bound oxy group abstracts a hydrogen from the camphor substrate. |
| bond_formed | medium | 1 | In the final step, the camphor radical initiates a homolytic substitution, hydroxylating the intermediate to form 5-hydroxycamphor. |
| electron_transfer | low | 0 | The iron centre accepts a single electron and water displaces the product. |

Allowed decisions: approve_as_source_evidence_for_train_cal_features, rewrite_events_and_keep_review_pending, reject_for_row_specific_feature_consumption

## Interpretation

- The calibration-review packet is ready for manual decisions; it records no approvals and changes no feature contract.
- A human reviewer should approve, rewrite, or reject these calibration rows in the source-evidence sidecar, then rerun the strict/readiness/materialization artifacts.
