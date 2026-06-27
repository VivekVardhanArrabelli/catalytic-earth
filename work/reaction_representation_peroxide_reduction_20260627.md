# Reaction-representation work — peroxide-reduction bond-change class (2026-06-27)

User-directed: "reaction representation work please" — invest in modeling the chemistry
directly so the source-free representation stops collapsing confusable families, rather
than trading representation quality for breadth. This is the MAP's "big bet" lever.

## The problem (diagnosed empirically)

Adding `cysteine_protease` (EC 3.4.22) on 2026-06-27 collapsed `peroxiredoxin_thiol_peroxidase`
from sc 0.833 → 0.0 in the leakage-safe representation. A registry-wide diagnostic showed the
deeper cause: **many families carry a Rhea reaction that earns no bond-change class at all.**
The reaction representation has two classifiers — `classify_reaction_bond_change` (hydrolysis;
requires water as a *reactant*) and `classify_reaction_nonhydrolytic` (transfer/redox/lyase) —
and **neither had a class for peroxide reduction**, where water is a *product*.

So the cofactor-free peroxidatic thiol peroxidases (peroxiredoxin/GPx), whose Rhea equation is
`a hydroperoxide + [thioredoxin]-dithiol = an alcohol + [thioredoxin]-disulfide + H2O`, received
**no cofactor class and no bond-change class** — an all-but-empty vector indistinguishable from
the cofactor-free hydrolases (proteases/esterases). When the 150-row cysteine_protease family
landed in that same empty corner, it dominated the cluster and absorbed peroxiredoxin.

## The fix (leakage-safe, ~10 lines)

Added a `bc_peroxide_reduction` reaction-center class to `classify_reaction_nonhydrolytic`:
a hydroperoxide / H2O2 consumed on the **substrate** side (O–O reductive cleavage). It reads
**only the Rhea substrate→product equation** — never EC/name/prose/lane/fingerprint — exactly
like every other bond-change class. Two correctness guards:

- `"superoxide"` contains the substring `"peroxide"`, so superoxide dismutase (`2 O2(.-) + 2 H(+)
  = O2 + H2O2`, peroxide a *product*) is explicitly excluded — no false positive.
- Both the spelled-out `(hydro)peroxide` and the `h2o2` formula notation are matched.

## Result (PYTHONHASHSEED=0; sc magnitudes are seed-stable)

| fingerprint | before | after |
| --- | --- | --- |
| **peroxiredoxin_thiol_peroxidase** | 0.0 | **0.947** ← recovered |
| heme_peroxidase_oxidase | 0.889 | **0.97** ← sharpened (bonus) |
| cysteine_protease | 0.94 | 0.94 (unchanged) |
| ser_his_acid_hydrolase | 0.0 | 0.0 (unchanged) |
| alpha_beta_hydrolase_esterase_lipase | 0.68 | 0.68 (unchanged) |
| glutathione_s_transferase | 0.95 | 0.95 (unchanged) |
| **overall leave-one-out** | **0.699** | **0.718** |

The class fires on exactly the right rows: peroxiredoxin 150/150, plus heme peroxidases that
reduce H2O2 (which separate on heme anyway). Zero family regressions.

## The honest residual limit

`cysteine_protease` (0.94) and `ser_his_acid_hydrolase` (0.0) are **unchanged** — and a reaction
representation **cannot** fix them, because they carry **no Rhea reaction at all** (peptide-bond
hydrolysis is generic and unannotated in Rhea). Separating that pair would need a
catalytic-residue-**identity** feature (catalytic Cys vs Ser), but the current bronze rows do not
carry it — the active-site annotations have null descriptions. That is the next axis, not a
reaction-representation axis.

## Roadmap (from the diagnostic)

`artifacts/v3_reaction_representation_peroxide_reduction_separability_20260627.json` records the
full per-family `rxn_unclassified` gap. The largest gaps (molybdopterin, PAPS-sulfotransferase,
radical-SAM) are **not** cofactor-free — they already separate on their cofactor, so an added
bond-change class is belt-and-suspenders, not a rescue. The prominent remaining **cofactor-free**
family with an unclassified reaction is `metal_independent_phosphodiesterase`; it is the next
candidate where modeling the chemistry directly could recover separability the same way.

## Verification

- `classify_reaction_nonhydrolytic` unit test added (peroxiredoxin Trx form, GPx H2O2 form, SOD
  exclusion, hydrolase non-fire).
- Representation-loop test updated to the recovered baseline and confirmed robust across
  PYTHONHASHSEED 0/7/42.
- Leakage guardrails unchanged (`ec_name_prose_lane_used: False`); no labels, registries,
  ontology, thresholds, or imports were touched — this is a pure representation change.

---

## Extension: glycerophosphodiester hydrolysis (same session)

User-directed follow-up ("extend reaction representation"). The diagnostic's next prominent
**cofactor-free** collapse was `metal_independent_phosphodiesterase` (sc **0.072**): its dominant
reaction `sn-glycerol 3-phosphocholine + H2O = sn-glycerol 3-phosphate + choline` is a genuine
phosphodiester hydrolysis, but `bc_phosphodiester` only recognised nucleic-acid / cyclic
phosphodiesters, so the glycerophospho head-group enzymes (GDPD, sphingomyelinase, phospholipase D)
earned no reaction-center class and collapsed into the cofactor-free cluster.

**Fix:** extend `bc_phosphodiester` to fire when a phospholipid head group is **released** —
free choline/ethanolamine, or standalone phosphocholine/phosphoethanolamine — matched as an
**exact product term**. The exact-term match is the key precision guard: phospholipase A *retains*
the phosphocholine on its lyso-product (`a 1-acyl-sn-glycero-3-phosphocholine`), and ATG4 proteases
act on `[protein]`-phosphatidylethanolamine conjugates — neither releases a free head group, so
neither false-fires. (A first, looser substring version regressed cysteine_protease 0.94→0.82 and
alpha_beta 0.68→0.59; the exact-term version eliminates both regressions.)

**Result (PYTHONHASHSEED=0):**

| fingerprint | before | after |
| --- | --- | --- |
| **metal_independent_phosphodiesterase** | 0.072 | **0.968** ← recovered |
| cysteine_protease | 0.94 | 0.94 (no regression) |
| alpha_beta_hydrolase_esterase_lipase | 0.68 | 0.68 (no regression) |
| **overall leave-one-out** | 0.718 | **0.733** |

## Cumulative outcome

Two leakage-safe reaction-center classes lifted overall LOO **0.699 → 0.718 → 0.733** and recovered
the two prominent cofactor-free collapses (peroxiredoxin 0.0→0.947, metal_independent PDE
0.072→0.968) with zero regressions. The roadmap's remaining-cofactor-free list is now **empty** —
every cofactor-free family with ≥10 rows now earns a reaction-center class. The only families the
reaction representation still cannot separate are `cysteine_protease` / `ser_his_acid_hydrolase`,
which carry no Rhea reaction at all (the catalytic-residue-identity axis, not a reaction axis).
