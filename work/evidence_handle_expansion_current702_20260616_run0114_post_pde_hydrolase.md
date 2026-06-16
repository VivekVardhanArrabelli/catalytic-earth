# Evidence-Handle Expansion — recover within-Swiss-Prot supply the cofactor handle misses

Run: 2026-06-16T12:07:54Z

Non-destructive recon (no registry, no labels). Measures how much reviewed supply each
alternative within-Swiss-Prot corroborator handle recovers per family. EC is scope only
(never a corroborator); keyword / binding-site / active-site are reviewed annotation used
for SCOPE/admission only (excluded_context, never predictive).

## Headline

- Families probed: 6.
- Handle-blocked families unlocked by a better handle: **4** (nad_p_dehydrogenase_ec_1_1_1, nad_p_oxidoreductase_broad_ec_1, biotin_dependent_carboxylase_ec_6_4_1, glycosyltransferase_ec_2_4).
- Reviewed supply recovered over current cofactor handles: **63967**.
- Additional reachable POSITIVE bronze (capped, discounted): **741** (counted as positive_bronze only — never merged with OOS / silver).
- Across 6 families, broadening the corroborator handle beyond cc_cofactor recovers ~63967 reviewed entries the cofactor handle misses (RAW and illustrative -- the broad EC 1.* lane overlaps the EC 1.1.1 lane, so supply pools OVERLAP and this is headroom, not additive distinct supply), and ~741 additional reachable POSITIVE bronze once the cap + novelty discount are applied (the bounded, non-inflated figure) -- 4 families cross the 100-floor only with the better handle. This is real reviewed supply, not source expansion: it is counted as positive_bronze and never merged with OOS / silver. The winning handles (keyword / binding-site / active-site) are the corroborators to wire into the import gate per family BEFORE admitting sources beyond reviewed Swiss-Prot; the big pools (broad oxidoreductase) must be split by EC-subclass into capped lanes, not sourced as one bucket.

## Per-family handle recovery

| Family | EC ceiling | current handle | best corroborator | recovered | uplift | reachable bronze (uplift) |
| --- | --- | --- | --- | --- | --- | --- |
| nad_p_dehydrogenase_ec_1_1_1 | 7804 | 7 | functional_keyword | 7700 | 7693 | 150 (+146) |
| nad_p_oxidoreductase_broad_ec_1 | 36245 | 50 | binding_site | 28669 | 28619 | 150 (+125) |
| sam_methyltransferase_ec_2_1_1 | 14325 | 691 | functional_keyword | 14279 | 13588 | 250 (+0) |
| non_heme_iron_2og_dioxygenase_ec_1_14_11 | 874 | 854 | functional_keyword | 869 | 15 | 250 (+0) |
| biotin_dependent_carboxylase_ec_6_4_1 | 4071 | 60 | binding_site | 3831 | 3771 | 250 (+220) |
| glycosyltransferase_ec_2_4 | 11259 | None | functional_keyword | 10281 | 10281 | 250 (+250) |

## Candidate handles measured per family

| Family | handle | supply | recovery vs EC ceiling |
| --- | --- | --- | --- |
| nad_p_dehydrogenase_ec_1_1_1 | functional_keyword | 7700 | 0.987 |
| nad_p_dehydrogenase_ec_1_1_1 | binding_site | 7234 | 0.927 |
| nad_p_dehydrogenase_ec_1_1_1 | active_site | 5588 | 0.716 |
| nad_p_oxidoreductase_broad_ec_1 | functional_keyword | 18597 | 0.513 |
| nad_p_oxidoreductase_broad_ec_1 | binding_site | 28669 | 0.791 |
| nad_p_oxidoreductase_broad_ec_1 | active_site | 16393 | 0.452 |
| sam_methyltransferase_ec_2_1_1 | functional_keyword | 14279 | 0.997 |
| sam_methyltransferase_ec_2_1_1 | binding_site | 11454 | 0.8 |
| sam_methyltransferase_ec_2_1_1 | active_site | 4672 | 0.326 |
| non_heme_iron_2og_dioxygenase_ec_1_14_11 | functional_keyword | 869 | 0.994 |
| non_heme_iron_2og_dioxygenase_ec_1_14_11 | binding_site | 846 | 0.968 |
| non_heme_iron_2og_dioxygenase_ec_1_14_11 | active_site | 66 | 0.076 |
| biotin_dependent_carboxylase_ec_6_4_1 | functional_keyword | 88 | 0.022 |
| biotin_dependent_carboxylase_ec_6_4_1 | binding_site | 3831 | 0.941 |
| biotin_dependent_carboxylase_ec_6_4_1 | active_site | 1621 | 0.398 |
| glycosyltransferase_ec_2_4 | functional_keyword | 10281 | 0.913 |
| glycosyltransferase_ec_2_4 | binding_site | 5488 | 0.487 |
| glycosyltransferase_ec_2_4 | active_site | 2224 | 0.198 |

## Recommended entry-level corroborators (not header-countable — wire at sourcing)

- **nad_p_dehydrogenase_ec_1_1_1**: Rhea NAD(P)(+)/NAD(P)H participant in the catalytic-activity reaction, Rossmann GxGxxG dinucleotide-binding sequence motif.
- **nad_p_oxidoreductase_broad_ec_1**: Rhea NAD(P) participant + EC-subclass-specific reaction, subclass-specific active-site residue roles.
- **sam_methyltransferase_ec_2_1_1**: Rhea S-adenosyl-L-methionine + S-adenosyl-L-homocysteine participant pair, no [4Fe-4S] (separates from radical-SAM).
- **non_heme_iron_2og_dioxygenase_ec_1_14_11**: Rhea 2-oxoglutarate + succinate + CO2 participant, HxD..H facial-triad residue roles.
- **biotin_dependent_carboxylase_ec_6_4_1**: biotinyl-lysine (K-biotin) modified-residue feature, Rhea hydrogencarbonate + ATP participant.
- **glycosyltransferase_ec_2_4**: Rhea UDP/GDP-sugar donor participant, DxD motif (GT-A) / GT-B two-domain signature.

## Guardrails

- All handles are reviewed annotation used for SCOPE/admission only (they belong in excluded_context, never predictive features) -- the same basis as the existing cofactor+EC handle. EC is scope only and is NOT counted as a corroborator.
- No registry written; no labels created; frozen current702 preserved.
