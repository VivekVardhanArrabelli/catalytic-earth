# External Heme Redox Boundary Panel - 2026-05-28

Run time: 2026-05-28T07:28:13Z

Review-only outputs:

- `artifacts/v3_external_heme_redox_boundary_panel_20260528.json`
- `work/external_heme_redox_boundary_panel_20260528.md`

No labels, registries, ontologies, thresholds, imports, production scoring,
model outputs, or model training were changed. Disk was already below the
requested 10 GiB floor (`df` showed 5.5 GiB free), so this pass performed no
large downloads and only wrote small text/JSON files.

## Bottom Line

The broad v1 `heme_peroxidase_oxidase` parent is chemically real but too broad
for child routing. It currently mixes classical peroxidases, catalases,
heme-copper terminal oxidases, P450/heme oxygenases, heme reductases/electron
transfer enzymes, and multiheme redox enzymes. A useful stress panel should
force the router to name the oxygen activation locus, not just the cofactor:
peroxide at heme, H2O2 disproportionation, heme-Cu O2 reduction,
heme-thiolate O2 insertion, heme-as-substrate oxygenase, flavin oxygenation, or
non-heme metal/copper chemistry.

## Candidate Manifest

The JSON freezes 46 candidate rows/leads:

- Current M-CSA heme anchors and boundaries: `m_csa:37`, `124`, `133`, `208`,
  `239`, `250`, `399`, `473`, `573`, `581`, `694`, `699`, `709`, `714`, `735`,
  `758`, `795`, `903`, `935`, `944`.
- External heme packet leads/controls: `P11678`, `P04040`, `P13029`, `Q939D2`,
  `P14532`, `K7N5M8`, `I2DBY1`, `Q47KB1`, `Q9UR19`, `Q02567`, `P06181`,
  `P49012`, `P39597`, `P31545`, `Q39034`.
- Hard negatives/OOS controls: non-heme iron/pterin/copper/luciferase rows
  `m_csa:129`, `130`, `134`, `135`, `547`, `128`; flavin or flavin-heme
  boundary rows `m_csa:131`, `551`, `973`, `141`; and expert-OOS
  flavodiiron `m_csa:497`.

Best review-ready external positives are `uniprot:P14532` and `uniprot:K7N5M8`.
Both remain non-countable: `P14532` is mechanism-match review-ready after exact
PDB/source-free heme geometry and no current-countable structural duplicate;
`K7N5M8` is duplicate-clear against current countable selected structures but
still needs label-policy/human-review gates and better exact ligand-state
confirmation.

## Child-Stratum Readiness

`heme.peroxidase_catalase_like` has enough current support for a review-only
pilot, matching Packet 3, but not a benchmark. It needs expert approval,
child-specific proximal/distal residue extraction, and peroxide-state evidence.

Catalase/catalase-peroxidase should not be merged blindly into classical
donor-oxidizing peroxidases. `m_csa:573` plus external catalase/KatG leads are
review-only until the panel records H2O2 disproportionation and KatG dual
function/covalent-adduct evidence.

Heme-copper terminal oxidase has strong M-CSA anchors (`m_csa:124`, `714`,
`735`) but needs an explicit child reopened from Packet 3's no-use
`heme.oxidase_oxygenase_like` state. Required evidence is heme-Cu binuclear
ligands, proton-channel residues, and O2-to-water terminal acceptor state.

P450/heme oxygenase rows are boundary controls now. They are current broad-parent
heme rows, but they should be hard negatives for peroxidase/catalase and
terminal-oxidase child calls until expert policy decides whether they become a
separate heme oxygenase/P450 child or parent-only boundary.

Non-heme oxygenases are review-only OOS controls. They become benchmark-ready
only after the evidence contract can name non-heme Fe, Rieske/non-heme Fe,
pterin/iron, copper, flavin, or luciferase loci and freeze expected route-away
or abstention behavior.

## Learned-Representation Value Add

Value add means the learned/site representation does something a heme/cofactor
shortcut cannot do:

- Rescue `m_csa:250` as heme peroxidase despite a wrong Foldseek nearest
  neighbor.
- Split terminal oxidases (`m_csa:124`, `714`, `735`) from peroxidases by
  heme-Cu/O2-to-water evidence.
- Route P450 and heme oxygenase rows away from peroxidase/catalase despite heme
  and O2 language.
- Reject non-heme Fe, copper, flavin, and luciferase oxygenases despite
  oxygenase/O2 vocabulary.
- Preserve duplicate holds as controls rather than inflating external support.

Cofactor-only failure is any result that calls a row child-positive merely
because heme, O2, peroxide, oxidase, or oxygenase terms are present.

## Verification Targets

- JSON parse: `artifacts/v3_external_heme_redox_boundary_panel_20260528.json`
- CLI validation: `PYTHONPATH=src python -m catalytic_earth.cli validate`
- Whitespace: `git diff --check`
