# External Stress-Panel Roadmap - 2026-05-28

Review-only outputs:

- `artifacts/v3_external_stress_panel_roadmap_20260528.json`
- `work/external_stress_panel_roadmap_20260528.md`

No labels, registries, ontologies, thresholds, imports, production scoring,
model training, or model outputs were edited. The roadmap defines validation
panels only.

## Goal

Build external or M-CSA-plus-external panels that test whether the evidence
router generalizes beyond M-CSA without inflating labels from weak words like
cofactor, hydrolase, oxygenase, PLP, heme, metal, glycan, fold, or EC class.

A successful panel does not have to import labels. A clean zero-pass can still
be successful if the router abstains or rejects for evidence-complete reasons
and does not fail because required sequence, Foldseek, active-site, or terminal
review evidence was missing.

## Provenance Tiers

| Tier | Meaning | Allowed use |
| --- | --- | --- |
| `tier_A_mcsa_curated` | M-CSA curated active-site/mechanism row or current registry row | Anchor positive or hard-negative control |
| `tier_B_external_curated` | External row with curated active-site residues, structure mapping, sequence and Foldseek controls | External validation positive |
| `tier_C_external_incomplete` | External row with reaction/EC or structure evidence but missing one or more blockers | Sourcing backlog only |
| `tier_D_control_only` | OOS, exact-overlap, near-duplicate, or mismatch row | Rejection/abstention control only |

## Panels

| Panel | Type | Main risk tested | Success signal |
| --- | --- | --- | --- |
| Flavin/redox boundary | M-CSA plus external | FAD/FMN, NAD(P)H, Fe-S, O2, or oxygenase wording leaking into FMO | FMO requires peroxyflavin oxygen insertion; flavodiiron NO reductase, radical flavin-Fe-S, and covalent FAD adduct rows reject or abstain |
| Metal hydrolase tails | M-CSA plus external | Collapsing phosphatase/nuclease, MBL-like, FGly/sulfatase, NTPase, and carbonic anhydrase into one metal label | Parent metal-water rows route, tail-specific rows split or abstain, serine/glycoside controls route away |
| PLP child mechanisms | M-CSA plus external | PLP cofactor presence hiding aminotransferase/decarboxylase/racemase/lyase/coupled B12 differences | PLP parent evidence is recognized, but child calls require reaction-center evidence; PLP+B12 abstains or routes to review-only coupled proposal |
| Heme redox boundaries | M-CSA plus external | Heme, O2, peroxide, and oxygenase terms mixing peroxidase, terminal oxidase, and oxygenase routes | Router names the oxygen activation locus and routes flavin/non-heme oxygenases away |
| Glycoside/carbohydrate enzymes | External-first with M-CSA OOS anchors | Hydrolase or glycan wording collapsing into metal/serine hydrolase labels | Glycoside rows depend on acidic dyad, glycosidic bond, sugar-pocket, and metal-absence evidence |

## Required Controls Per Panel

Every panel needs the same gate sequence before it can produce a meaningful
router result:

1. Freeze a no-decision manifest with candidate positives, near-family hard
   negatives, and OOS controls.
2. Run sequence-neighbor checks against current M-CSA references, external
   all-vs-all rows, and UniRef90/50 or UniRef-wide duplicate controls.
3. Run Foldseek-neighbor checks against current countable rows and selected OOS
   controls.
4. Extract active-site evidence from structures or curated residue packets.
5. Run the router in review-only validation mode and report correct route,
   abstention, and hard-negative regression outcomes.

## Panel Notes

### Flavin/redox boundary

Candidate positives are clean FMO rows (`m_csa:131`, `m_csa:132`, future
review-only `m_csa:551`, `m_csa:973`) and ordinary flavin hydride-transfer rows
such as `m_csa:3`, `m_csa:6`, and `m_csa:110`. Hard negatives include
`m_csa:497` flavodiiron NO reductase, `m_csa:750` radical flavin-Fe-S
dehydratase, `m_csa:123` covalent FAD-adduct APS reductase, and heme oxygenase
controls. The decisive extractor is peroxyflavin plus substrate oxygen
insertion, not FAD/FMN or O2 alone.

### Metal hydrolase tails

Candidate slices are phosphatase/nuclease/phosphoesterase, MBL-like
amidohydrolase, FGly/sulfatase, NTPase/nucleotide hydrolase, and carbonic
anhydrase. Existing M-CSA anchors cover nuclease/phosphoesterase and MBL-like
chemistry; FGly/sulfatase (`m_csa:661`), NTPase, and carbonic anhydrase remain
review-only acquisition tails. The key extraction need is metal count/ligands,
water or hydroxide, substrate atom attacked, and phosphate/sulfate/nucleotide or
carbonate context.

### PLP child mechanisms

Candidate slices are aminotransferases (`m_csa:66`, `m_csa:249`, `m_csa:854`),
decarboxylases (`m_csa:482`, `m_csa:860`, `m_csa:937`),
racemase/epimerase (`m_csa:213`, `m_csa:330`), lyase/eliminase (`m_csa:186`,
`m_csa:855`, external `Q96I15` only after evidence completion), and coupled
PLP+B12 aminomutase (`m_csa:737`). Hard negatives include non-PLP Schiff-base
lyases such as `P06746` and radical/coupled PLP rows that should not become
plain PLP child positives.

### Heme redox boundaries

Candidate slices are peroxidase/catalase-like rows (`m_csa:239`, `m_csa:250`),
heme-copper terminal oxidase (`m_csa:124`), and heme oxygenase/P450 rows
(`m_csa:133`, `m_csa:699`, `m_csa:795`). Hard negatives are flavin
monooxygenases and non-heme oxygenases. Success requires the router to name the
oxygen activation locus: heme, heme-copper, flavin, or non-heme metal.

### Glycoside/carbohydrate enzymes

This is the external-first panel. Candidate positives are not countable yet:
`Q6NSJ0` alpha-galactosidase, `P29372` DNA glycosylase, `P34949`
mannose-6-phosphate isomerase, `P33025` pseudouridine-5'-phosphate
glycosidase, and M-CSA OOS glycosidase anchors such as `m_csa:19`, `m_csa:393`,
`m_csa:400`, `m_csa:436`, `m_csa:471`, and `m_csa:475`. The panel is successful
only if glycosidic-bond and acidic-dyad evidence routes these away from generic
metal or serine hydrolase collapse.

## Next Artifact To Build

The next useful artifact is a no-decision manifest for one panel at a time,
starting with flavin/redox or glycoside/carbohydrate. Both have the best local
control context and the clearest label-inflation failure modes.
