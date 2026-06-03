# Source-Free Event-Axis Linker DRAFT — Reviewer Sign-Off Packet (current702)

Run: 2026-06-03  ·  Path A (author event axis)  ·  token `event_residue_role:proton_transfer|electrostatic_stabiliser`

DRAFT for your sign-off. Produced by a deterministic, **label-blind** structural rubric over the 53 approved
source-free locators (residue identity + contacting atoms + distance + source-free role hints only). No label,
fingerprint, EC/Rhea, source text, curated role, or target name was used as input. Nothing is gate-consumable
until you sign off; no heldout read, no threshold applied.

## Rubric (uniform, source-free)
- **electrostatic_stabiliser**: cationic (Arg/Lys) or His side chain — or backbone-amide/polar donor — contacting an anionic phosphate/carboxylate O (oxyanion stabilisation).
- **proton_transfer**: His→metal or ring-redox atom (general acid/base); Asp/Glu→metal (base / water activator); Lys→PLP C4A (Schiff-base shuttle); Cys/Tyr→reactive atom.
- A row's token fires only when BOTH roles are evidenced. Confidence = electrostatic-stabiliser strength (distance-scaled) gated by the best co-located proton-transfer axis.

## Result
- Token PRESENT (both roles, draft linker): **14** rows
- Token ABSENT (insufficient source-free evidence): **39** rows — treated as token=absent, not blocked
- Fired set is 12 in-scope + 2 boundary-OOS; the in-scope skew emerged from structure (label not used).
- Confidences are modest (0.21–0.47): honest limit of inferring proton-transfer roles from cofactor-proximity locators.

## The 14 token-present rows — full evidence (sign off / reject per row)

### m_csa:418  (P37821)  — fingerprint: `plp_dependent_enzyme`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.468
  - **ARG281** (conf 0.468)
    - role: cationic ARG NH2 stabilises anionic phosphate O O1P at 2.674A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.325A
  - **THR121** (conf 0.231)
    - role: H-bond donor THR OG1 (oxyanion-hole-like) at O2P 2.495A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.325A
  - **SER272** (conf 0.207)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O3P 2.686A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.325A
  - **SER270** (conf 0.19)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O3P 2.812A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.325A

### m_csa:545  (Q7M523)  — fingerprint: `plp_dependent_enzyme`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.455
  - **LYS54** (conf 0.455)
    - role: cationic LYS NZ stabilises anionic phosphate O O2P at 2.721A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.322A
  - **THR202** (conf 0.241)
    - role: H-bond donor THR OG1 (oxyanion-hole-like) at O3P 2.421A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.322A
  - **THR205** (conf 0.224)
    - role: H-bond donor THR OG1 (oxyanion-hole-like) at O2P 2.547A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.322A

### m_csa:750  (P55792)  — fingerprint: `out_of_scope`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.397
  - **ARG156** (conf 0.397)
    - role: cationic ARG NH2 stabilises anionic phosphate O O2P at 2.876A [role_hint:flavin_redox_contact_candidate]
    - axis: co-located proton-transfer axis: His O->N5 (ring redox/proton site) general acid/base at 2.699A
  - **LYS153** (conf 0.389)
    - role: cationic LYS NZ stabilises anionic phosphate O O1A at 2.95A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: His O->N5 (ring redox/proton site) general acid/base at 2.699A

### m_csa:714  (P0ABI8)  — fingerprint: `heme_peroxidase_oxidase`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.333
  - **HIS411** (conf 0.333)
    - role: His ND1 (cationic form) stabilises anionic phosphate O O2A at 2.447A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.21A

### m_csa:239  (P00433)  — fingerprint: `heme_peroxidase_oxidase`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.317
  - **ARG61** (conf 0.317)
    - role: cationic ARG NE stabilises anionic O O2D at 2.86A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.079A
  - **LYS204** (conf 0.292)
    - role: cationic LYS N stabilises anionic O O2D at 2.972A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.079A
  - **SER103** (conf 0.203)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O1A 2.718A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.079A
  - **GLN206** (conf 0.182)
    - role: H-bond donor GLN N (oxyanion-hole-like) at O2A 2.874A [role_hint:ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.079A

### m_csa:709  (P00431)  — fingerprint: `heme_peroxidase_oxidase`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.292
  - **HIS248** (conf 0.292)
    - role: His ND1 (cationic form) stabilises anionic phosphate O O2A at 2.68A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.062A
  - **LYS246** (conf 0.247)
    - role: cationic LYS N stabilises anionic O O2D at 3.177A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.062A
  - **SER252** (conf 0.201)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O1A 2.733A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.062A
  - **ASN251** (conf 0.178)
    - role: H-bond donor ASN ND2 (oxyanion-hole-like) at O2A 2.911A [role_hint:ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.062A

### m_csa:3  (P15559)  — fingerprint: `flavin_dehydrogenase_reductase`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.264
  - **HIS12** (conf 0.264)
    - role: His NE2 (cationic form) stabilises anionic phosphate O O2P at 2.723A [role_hint:flavin_redox_contact_candidate]
    - axis: co-located proton-transfer axis: Tyr OH->O2 proton donor at 2.729A
  - **ASN19** (conf 0.209)
    - role: H-bond donor ASN ND2 (oxyanion-hole-like) at O1P 2.669A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: Tyr OH->O2 proton donor at 2.729A

### m_csa:990  (Q8GS60)  — fingerprint: `flavin_dehydrogenase_reductase`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.261
  - **THR137** (conf 0.261)
    - role: H-bond donor THR OG1 (oxyanion-hole-like) at O1A 2.262A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: Tyr N->O2 proton donor at 2.51A
  - **GLN332** (conf 0.178)
    - role: H-bond donor GLN NE2 (oxyanion-hole-like) at O2P 2.912A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: Tyr N->O2 proton donor at 2.51A

### m_csa:250  (P04963)  — fingerprint: `heme_peroxidase_oxidase`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.254
  - **HIS126** (conf 0.254)
    - role: His N (cationic form) stabilises anionic phosphate O O2A at 2.89A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Cys SG->FE thiol proton/nucleophile at 2.28A
  - **SER129** (conf 0.208)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O1A 2.674A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Cys SG->FE thiol proton/nucleophile at 2.28A

### m_csa:211  (P38489)  — fingerprint: `flavin_dehydrogenase_reductase`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.252
  - **ARG207** (conf 0.252)
    - role: cationic ARG NH2 stabilises anionic phosphate O O3P at 2.679A [role_hint:flavin_redox_contact_candidate]
    - axis: co-located proton-transfer axis: GLU N->N5 general acid/base at reactive ring atom 2.987A
  - **ARG10** (conf 0.252)
    - role: cationic ARG NH1 stabilises anionic phosphate O O2P at 2.815A [role_hint:flavin_redox_contact_candidate]
    - axis: co-located proton-transfer axis: GLU N->N5 general acid/base at reactive ring atom 2.987A
  - **LYS205** (conf 0.252)
    - role: cationic LYS NZ stabilises anionic phosphate O O3P at 2.824A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: GLU N->N5 general acid/base at reactive ring atom 2.987A
  - **LYS14** (conf 0.252)
    - role: cationic LYS NZ stabilises anionic O O2 at 2.659A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: GLU N->N5 general acid/base at reactive ring atom 2.987A
  - **LYS74** (conf 0.252)
    - role: cationic LYS NZ stabilises anionic O O2 at 2.758A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: GLU N->N5 general acid/base at reactive ring atom 2.987A
  - **SER12** (conf 0.206)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O2P 2.692A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: GLU N->N5 general acid/base at reactive ring atom 2.987A

### m_csa:854  (P80147)  — fingerprint: `plp_dependent_enzyme`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.225
  - **SER165** (conf 0.225)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O2P 2.545A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.424A
  - **THR381** (conf 0.221)
    - role: H-bond donor THR OG1 (oxyanion-hole-like) at O3P 2.572A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.424A

### m_csa:419  (O52552)  — fingerprint: `plp_dependent_enzyme`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.219
  - **THR63** (conf 0.219)
    - role: H-bond donor THR OG1 (oxyanion-hole-like) at O1P 2.593A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.451A
  - **SER183** (conf 0.214)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O2P 2.63A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: Lys NZ->C4A Schiff-base proton shuttle at 1.451A

### m_csa:115  (Q9T0N8)  — fingerprint: `flavin_dehydrogenase_reductase`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.207
  - **SER106** (conf 0.207)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O1A 2.679A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: Tyr OH->O2 proton donor at 2.575A
  - **GLN110** (conf 0.202)
    - role: H-bond donor GLN O (oxyanion-hole-like) at O3B 2.72A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: Tyr OH->O2 proton donor at 2.575A
  - **THR174** (conf 0.2)
    - role: H-bond donor THR OG1 (oxyanion-hole-like) at O1P 2.738A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: Tyr OH->O2 proton donor at 2.575A
  - **SER527** (conf 0.196)
    - role: H-bond donor SER OG (oxyanion-hole-like) at O2B 2.766A [role_hint:flavin_binding_contact_candidate]
    - axis: co-located proton-transfer axis: Tyr OH->O2 proton donor at 2.575A

### m_csa:121  (P07850)  — fingerprint: `out_of_scope`
- event_type: proton_transfer · residue_role: electrostatic_stabiliser · top confidence: 0.205
  - **HIS69** (conf 0.205)
    - role: His NE2 (cationic form) stabilises anionic phosphate O O2A at 3.16A [role_hint:polar_or_catalytic_ligand_contact_candidate]
    - axis: co-located proton-transfer axis: His NE2->FE (metal-water activator) general acid/base at 2.032A

## The 39 token-absent rows

These lacked a source-free electrostatic-stabiliser and/or proton-transfer axis in the cofactor-anchored locator
(mostly metal-hydrolase and heme sites). They are recorded as token=absent (a valid feature value), not as blockers.

| row | fingerprint |
| --- | --- |
| m_csa:9 | out_of_scope |
| m_csa:32 | out_of_scope |
| m_csa:43 | metal_dependent_hydrolase |
| m_csa:44 | metal_dependent_hydrolase |
| m_csa:45 | out_of_scope |
| m_csa:46 | out_of_scope |
| m_csa:97 | metal_dependent_hydrolase |
| m_csa:109 | flavin_dehydrogenase_reductase |
| m_csa:131 | flavin_monooxygenase |
| m_csa:159 | metal_dependent_hydrolase |
| m_csa:163 | metal_dependent_hydrolase |
| m_csa:171 | metal_dependent_hydrolase |
| m_csa:180 | metal_dependent_hydrolase |
| m_csa:188 | out_of_scope |
| m_csa:220 | out_of_scope |
| m_csa:242 | metal_dependent_hydrolase |
| m_csa:311 | out_of_scope |
| m_csa:321 | metal_dependent_hydrolase |
| m_csa:323 | out_of_scope |
| m_csa:333 | out_of_scope |
| m_csa:352 | out_of_scope |
| m_csa:370 | out_of_scope |
| m_csa:384 | out_of_scope |
| m_csa:392 | out_of_scope |
| m_csa:397 | out_of_scope |
| m_csa:403 | metal_dependent_hydrolase |
| m_csa:497 | out_of_scope |
| m_csa:517 | metal_dependent_hydrolase |
| m_csa:526 | out_of_scope |
| m_csa:551 | flavin_dehydrogenase_reductase |
| m_csa:710 | metal_dependent_hydrolase |
| m_csa:853 | cobalamin_radical_rearrangement |
| m_csa:916 | metal_dependent_hydrolase |
| m_csa:994 | metal_dependent_hydrolase |
| m_csa:56 | out_of_scope |
| m_csa:199 | out_of_scope |
| m_csa:356 | out_of_scope |
| m_csa:480 | out_of_scope |
| m_csa:541 | out_of_scope |

## Honest assessment
- This is a faithful but **thin, low-confidence** source-free event axis. Only 14/53 rows carry the token; confidences are modest.
- The fired rows are mechanistically sensible (phosphate-cofactor enzymes: PLP/flavin/heme).
- Feeding this to the one-shot heldout read tests a weak feature. Options: (a) sign off and proceed (build surface → readiness → pause → heldout once), (b) reject specific weak rows first, (c) reconsider before spending the one-shot budget.

## Guardrails
Label-blind rubric; review-only; no locators copied; no event-axis linker materialized; no heldout read; no threshold applied.
