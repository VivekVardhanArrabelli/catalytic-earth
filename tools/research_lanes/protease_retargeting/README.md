# Fixed-target protease evidence

**A peptide sequence alone does not identify the design problem.** In the
September 21, 2026 v3 of [Chen et al.](https://www.biorxiv.org/content/10.1101/2025.11.20.689622v3.full),
TDPr3 and TDPn3 target the same peptide but different bonds. Their pipelines
also differ. They are not a controlled comparison of approaches to one fixed
cleavage site.

The [source-scoped record](fixed_target_evidence.json) preserves that distinction
alongside reporter versus purified full-length substrate context, restricted
substrate preference, controls, and an unresolved figure-caption identity.
It is exposed research evidence, outside the packaged/canonical Atlas. No
runtime, protected registry, benchmark or performance claim is changed. No
TDP-construct coordinates or productive-geometry evidence are represented here.

| Selected construct and substrate context | Intended cut after peptide residue | Source-assigned cuts after peptide residues |
| --- | --- | --- |
| TDPr3, reporter substrate | 5 | 5 and 3 |
| TDPn3, reporter substrate | 7 | 3 and 7 |
| TDPn3, full-length monomeric preparation | 7 | 7 |
| TDPn3, full-length oligomeric preparation | 7 | 7 |

Positions count the 12-residue peptide from 1. Assignments come from
supplementary Table S2 for selected constructs, separately from the campaign
screens; they do not supply detection limits or prove absence
of every other product. The record also preserves uncertainty from Table S2's
generic cis-screen title; it does not label the TDPr3 MS row a trans assay.
The full-length site is in the disordered C-terminal
region. A disordered accessible site is not excluded by Problem 8's wording;
these assays nevertheless do not demonstrate endogenous cleavage in living cells.

The source qualitatively reports that TDPr3 retains its original substrate
preference. The results text attributes
better target preference to TDPn3, but the Fig. 5b caption names TDPr3; that
conflict remains explicit. The 48-redesign and 113-de-novo screen sizes do not
provide reported cohort hit rates, and the selected full-length lead cannot
become a 1/113 estimate. Buffer-only and catalytic-base-knockout controls are
recorded separately for both full-length preparations. Values from the older
PMC v1 are not carried forward.

## Use the record

This query identifies the exact-site comparison problem without a new consumer:

```sh
python3 - <<'PY'
import json
from pathlib import Path
p = Path('tools/research_lanes/protease_retargeting/fixed_target_evidence.json')
d = json.loads(p.read_text())
for campaign in d['campaigns']:
    if 'intended_cut_after_residue' in campaign:
        print(campaign['construct'], campaign['intended_cut'])
print(d['construction_decision']['decision'])
PY
```

**Construction decision:** keep sequence, intended bond, observed products and
assay context separate before extracting transferable recognition constraints.
The next question is what can change target preference while preserving
productive geometry at the *same* specified bond. The current handoff owns
the next assignment. These are published observations, not project experiments
or evidence that Atlas outperforms direct source use.

Source URLs, versions and captured-body hashes are in the JSON. Full source
bodies remain in the local run receipt, not redistributed here. Computational
source and representation checks do not constitute independent expert review.
