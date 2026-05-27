# Packet 3 V2 Sublabel Closure - 2026-05-27

This closure is proposal-only and review-only. No v2 sublabel is canonical, production-ready, or countable in benchmark metrics without human expert approval.

## Counts

- Source child labels accounted for: 25
- Final dispositions: {'abstention_probe_unresolved_bucket': 3, 'canary_only_underpowered_candidate': 7, 'demoted_mixed_chemistry_do_not_use': 1, 'future_acquisition_target': 6, 'review_only_v2_pilot_candidate': 8}
- Eval use now: {'abstention_probe_only': 3, 'canary_only': 7, 'do_not_use': 2, 'future_acquisition_target': 5, 'pilot_only': 8}
- Canonical registry-ready child labels: 0

## Child-Label Dispositions

| Child label | Support | Final disposition | Eval use now | Next action |
| --- | ---: | --- | --- | --- |
| `ser_his_acid.lipase_esterase_cutinase_like` | 19 | `review_only_v2_pilot_candidate` | `pilot_only` | Keep proposed name for a non-metric pilot; require expert approval before registry or benchmark use. |
| `ser_his_acid.perhydrolase_haloperoxidase_caveat` | 1 | `canary_only_underpowered_candidate` | `canary_only` | Keep as caveat canary; acquire more perhydrolase/haloperoxidase support before any pilot. |
| `ser_his_acid.serine_protease_peptidase_like` | 10 | `review_only_v2_pilot_candidate` | `pilot_only` | Keep proposed name for a non-metric pilot; require expert approval before registry or benchmark use. |
| `ser_his_acid.unresolved_acyl_enzyme_hydrolase` | 12 | `abstention_probe_unresolved_bucket` | `abstention_probe_only` | Split into named acyl-enzyme child families before pilot; use current bucket only to probe abstention. |
| `metal_hydrolase.amidohydrolase_deaminase_like` | 7 | `review_only_v2_pilot_candidate` | `pilot_only` | Keep proposed name for a non-metric pilot; require expert approval before registry or benchmark use. |
| `metal_hydrolase.carbonic_anhydrase_dehydratase_like` | 3 | `canary_only_underpowered_candidate` | `canary_only` | Keep as carbonic-anhydrase-like canary; acquire more support and expert-bound the dehydratase chemistry. |
| `metal_hydrolase.metallo_beta_lactamase_like` | 3 | `canary_only_underpowered_candidate` | `canary_only` | Keep as MBL-like canary; acquire broader lactamase/non-lactam metal hydrolase controls before pilot use. |
| `metal_hydrolase.ntpase_nucleotide_hydrolase_tail` | 1 | `future_acquisition_target` | `future_acquisition_target` | Acquire more NTPase/nucleotide hydrolase examples before naming a child pilot. |
| `metal_hydrolase.phosphoesterase_nuclease_or_phosphatase_like` | 35 | `review_only_v2_pilot_candidate` | `pilot_only` | Keep proposed name for a non-metric pilot; optionally split phosphatase versus nuclease after expert review. |
| `metal_hydrolase.sulfatase_fgly_like` | 1 | `future_acquisition_target` | `future_acquisition_target` | Acquire more FGly/sulfatase rows before any child pilot; keep as v2 design question. |
| `metal_hydrolase.unresolved_metal_water_hydrolase` | 20 | `abstention_probe_unresolved_bucket` | `abstention_probe_only` | Split into named metal-water child mechanisms before pilot; use only as abstention probe now. |
| `metal_hydrolase.zinc_metalloprotease_or_metallopeptidase_like` | 13 | `review_only_v2_pilot_candidate` | `pilot_only` | Keep proposed name for a non-metric pilot; require expert approval before registry or benchmark use. |
| `plp.coupled_plp_radical_or_cobalamin_boundary` | 2 | `canary_only_underpowered_candidate` | `canary_only` | Preserve coupled PLP plus radical/cobalamin signal; do not collapse into ordinary PLP or cobalamin buckets. |
| `plp.decarboxylase` | 4 | `canary_only_underpowered_candidate` | `canary_only` | Use only as underpowered PLP decarboxylase canary; acquire more support before pilot metrics. |
| `plp.lyase_eliminase_synthase` | 11 | `review_only_v2_pilot_candidate` | `pilot_only` | Keep proposed name for a non-metric pilot; require expert approval before registry or benchmark use. |
| `plp.phosphorylase_acid_catalysis_caveat` | 1 | `canary_only_underpowered_candidate` | `canary_only` | Keep as caveat canary; acquire support and expert-bound the acid catalysis role before pilot use. |
| `plp.racemase_epimerase` | 2 | `canary_only_underpowered_candidate` | `canary_only` | Use only as underpowered racemase/epimerase canary; acquire additional PLP stereochemistry rows before pilot. |
| `plp.transaminase_aminotransferase` | 5 | `review_only_v2_pilot_candidate` | `pilot_only` | Keep proposed name for a non-metric pilot; require expert approval before registry or benchmark use. |
| `plp.unresolved_plp_chemistry` | 6 | `abstention_probe_unresolved_bucket` | `abstention_probe_only` | Split unresolved PLP rows into named PLP mechanisms before pilot; use only as abstention probe now. |
| `flavin.boundary_monooxygenase_like_review_needed` | 2 | `future_acquisition_target` | `future_acquisition_target` | Keep monooxygenase boundary separate; acquire clean FMO rows and do not absorb into generic flavin reductase/OOS. |
| `flavin.dehydrogenase_oxidase_hydride_transfer` | 47 | `demoted_mixed_chemistry_do_not_use` | `do_not_use` | Split into clean hydride transfer, Fe-S/electron-relay coupled chemistry, covalent FAD-adduct chemistry, and radical dehydratase before pilot use. |
| `flavin.unresolved_flavin_redox` | 1 | `future_acquisition_target` | `future_acquisition_target` | Acquire more unresolved flavin redox examples and split from hydride-transfer and monooxygenase boundaries. |
| `heme.peroxidase_catalase_like` | 20 | `review_only_v2_pilot_candidate` | `pilot_only` | Keep proposed name for a non-metric pilot; require expert approval before registry or benchmark use. |
| `flavin.monooxygenase_like_boundary_against_secondary_probe` | 2 | `future_acquisition_target` | `future_acquisition_target` | Keep as secondary/FMO boundary acquisition target; do not absorb into generic flavin reductase or OOS. |
| `heme.oxidase_oxygenase_like` | 0 | `future_acquisition_target` | `do_not_use` | Terminal no-use for current packet; acquire heme oxidase/oxygenase examples before reopening. |

## Decision Notes

- `flavin.dehydrogenase_oxidase_hydride_transfer` is demoted because the support pool mixes multiple flavin chemistries.
- Flavin monooxygenase remains secondary and underpowered; it is an acquisition target, not a generic flavin reductase/OOS bucket.
- Coupled PLP plus radical/cobalamin signals are preserved as coupled-cofactor canaries.
- Sulfatase/FGly, MBL-like, carbonic-anhydrase-like, NTPase tails, and unresolved metal-water hydrolases remain v2 design questions unless support and chemistry become decisive.
