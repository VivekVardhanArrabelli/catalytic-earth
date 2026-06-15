# Task spec — restore representation separability after the new-family lanes (2026-06-15)

Hand-off spec. The fix below is ALREADY VALIDATED by a read-only measure-first prototype on the
live sharded registry (numbers are real, not estimated). Implement it in
`src/catalytic_earth/mechanism_representation_loop.py` (+ tests). Owner: whichever automation
owns the representation module — do NOT have two writers on this file at once.

## Problem (measured 2026-06-15)

The new family lanes (aldehyde_dehydrogenase, alpha_beta_hydrolase_esterase_lipase,
ser_thr_protein_phosphatase, had_like_phosphatase) were added FASTER than the reaction-center
vocabulary, so families collapsed and dragged neighbours down. Overall leave-one-out
self-consistency regressed **0.755 -> 0.713**, and the regression was ACCOMMODATED by lowering
test thresholds (e.g. `nad_p_dehydrogenase` assertion `>0.85 -> >0.5`; `metallophosphomonoesterase`
flipped from `>0.8` to `<0.4`) rather than fixed. Collapsed/dragged families:

- `ser_thr_protein_phosphatase` 0.000 (fires only `bc_phosphomonoester` -> identical to small-molecule phosphomonoesterase)
- `alpha_beta_hydrolase_esterase_lipase` 0.200 (no ester-hydrolysis class -> nothing to separate on)
- `glycoside_hydrolase` 0.500 (no glycoside-hydrolysis class; spuriously fires bc_carbon_carbon_lyase)
- `nad_p_dehydrogenase` 0.547 (aldehyde_dehydrogenase shares `bc_redox_hydride`, steals members)

Root cause = missing leakage-safe reaction-center vocabulary. Fix = add it (same pattern as the
2026-06-14 C-C lyase fix). Derive ONLY from the Rhea substrate->product equation; never EC/name/
prose/fingerprint/substrate-identity/fold.

## The fix: 4 leakage-safe classes (+3 feature dims; `acc_protein` is reused)

Add `bc_ester_hydrolysis`, `bc_glycoside_hydrolysis` to `BOND_CHANGE_CLASSES` (they are
hydrolyses), `bc_aldehyde_oxidation` to `NONHYDROLYTIC_BOND_CLASSES` (it is a redox). Reuse the
existing `acc_protein` (in `PHOSPHOACCEPTOR_CLASSES`) for protein dephosphorylation — no new dim.

Tokenize on Rhea's ` + ` separator (regex `\s\+\s`) so charged ions (`H(+)`, `NH4(+)`) stay
intact — a bare `+` split shreds them (this is the bug that bit the C-C lyase work).

### 1. bc_ester_hydrolysis  (detect in classify_reaction_bond_change; water already on LHS there)
Fires for ester/lipase hydrolysis (triacylglycerol, sterol ester, phospholipid -> alcohol +
carboxylate/fatty acid). Logic on the lowercased equation:
- `h2o` in LHS tokens; AND
- NOT (`nad` or `nadp` anywhere)  # exclude aldehyde dehydrogenase, which also makes a carboxylate
- AND `[protein]` NOT in equation
- AND no free `phosphate`/`diphosphate` product token
- AND ( `'fatty acid'` substring in RHS  OR  any RHS token endswith `'oate'` or == `'acetate'` )

### 2. bc_glycoside_hydrolysis  (classify_reaction_bond_change)
Fires for O-/N-glycoside hydrolysis (oligosaccharide or glycoside + H2O -> sugar + aglycone):
- `h2o` in LHS tokens; AND
- ( any RHS token contains a free monosaccharide name in
  {`d-glucose`,`d-mannose`,`d-galactose`,`d-glucosamine`,`n-acetyl`,`d-xylose`,`l-fucose`,
   `d-fructose`,`d-galactosamine`}
  OR the LHS contains a glycosidic marker: `'(1->'` or `'glucosid'` or `'glycosid'` or `'galactosid'` )

Note: this also fixes `glycoside_hydrolase` spuriously firing `bc_carbon_carbon_lyase` — keep
both classes; the glycoside class gives it the distinguishing feature.

### 3. acc_protein on protein dephosphorylation  (classify_reaction_bond_change)
Distinguishes `ser_thr_protein_phosphatase` from small-molecule `metallophosphomonoesterase`
(the `[protein]` trick, mirroring the kinase `acc_protein`). When the phosphomonoester-hydrolysis
conditions hold AND:
- `[protein]` in equation AND `phospho` in LHS AND free `phosphate` product
then ADD `acc_protein` to the returned class set (alongside `bc_phosphomonoester`).

### 4. bc_aldehyde_oxidation  (classify_reaction_nonhydrolytic; redox bucket)
Separates aldehyde dehydrogenase (aldehyde + NAD+ + H2O -> carboxylate + NADH; CONSUMES water)
from generic NAD redox (alcohol -> ketone; no water). Reuse the `nad_ox`/`nad_red` booleans
already computed there:
- ( `nad(+)` or `nadp(+)` in eqn ) AND ( `nadh` or `nadph` in eqn )  # an NAD redox pair
- AND `h2o` in LHS tokens

## Validated result (measure-first prototype, base LOO 0.7127 on the live registry)

Overall **0.7127 -> 0.7542 (+0.0415)**. Per family:
- `alpha_beta_hydrolase_esterase_lipase` 0.200 -> 0.680
- `glycoside_hydrolase` 0.500 -> 0.813
- `nad_p_dehydrogenase` 0.547 -> 0.960  (and `aldehyde_dehydrogenase` STAYS ~1.0)
- `ser_thr_protein_phosphatase` 0.000 -> 0.875
- minor, accepted: `had_like_phosphatase` -0.028, `metallophosphomonoesterase` -0.027

PRINCIPLED CEILING to DOCUMENT, not hack: `ser_his_acid_hydrolase` 0.908 -> 0.667. Cause:
alpha/beta-hydrolases and Ser-His acid hydrolases are BOTH Ser-His-Asp serine esterases — they
genuinely share ester-hydrolysis chemistry, so `bc_ester_hydrolysis` correctly fires for both and
blurs them. The residual separation is FOLD-level (alpha/beta-hydrolase fold vs others), exactly
like the fold-defined kinases — a reaction-equation representation cannot and should not force it.
Narrowing the ester rule to "lipase-only" does NOT help (22/87 ser_his rows are genuine
lipase/phospholipase reactions). Accept the cost; document it.

## Test re-baseline (tests/test_mechanism_representation_loop.py)

- Add classifier unit tests (positive + negative) for each new class:
  - ester: `a triacylglycerol + H2O = a diacylglycerol + a fatty acid + H(+)` -> fires;
    negatives: `octanal + NAD(+) + H2O = octanoate + NADH + 2 H(+)` (NAD -> NOT ester),
    `O-phospho-L-seryl-[protein] + H2O = L-seryl-[protein] + phosphate` (protein -> NOT ester).
  - glycoside: `DIMBOA beta-D-glucoside + H2O = DIMBOA + D-glucose` -> fires;
    negative: `a phosphate monoester + H2O = an alcohol + phosphate` -> not.
  - protein dephos: `O-phospho-L-seryl-[protein] + H2O = L-seryl-[protein] + phosphate` ->
    {`bc_phosphomonoester`,`acc_protein`}; negative small-molecule phosphomonoester -> no acc_protein.
  - aldehyde: `octanal + NAD(+) + H2O = octanoate + NADH + 2 H(+)` -> includes `bc_aldehyde_oxidation`;
    negative: `a secondary alcohol + NADP(+) = a ketone + NADPH + H(+)` (no water) -> only `bc_redox_hydride`.
- RESTORE the relaxed real-registry assertions UP to the validated reality:
  - `leave_one_out_self_consistency` > 0.74  (currently >0.7)
  - `nad_p_dehydrogenase` > 0.9   (currently relaxed to >0.5)
  - ADD: `alpha_beta_hydrolase_esterase_lipase` > 0.6; `ser_thr_protein_phosphatase` > 0.8;
    `glycoside_hydrolase` > 0.8; `aldehyde_dehydrogenase` >= 0.95
  - `ser_his_acid_hydrolase`: set to > 0.6 WITH a comment documenting the serine-esterase fold
    overlap as a principled ceiling (do not assert it back to 0.9).
  - `metallophosphomonoesterase`: the existing `<0.4` is a separate metal-phosphatase-cluster
    issue, NOT addressed here; leave it (or note it as a separate follow-up).

## Also (small, related coverage gap found 2026-06-15)

`coverage_redundancy_audit.FINGERPRINT_SOURCING_SIGNATURES` lists 40 families but the registry
has 41 — `ser_thr_protein_phosphatase` is MISSING. Add it (EC 3.1.3.16 / protein-phosphatase
scope; EC stays scope-only, never predictive), so the governor's reaction-saturation/coverage
view covers all 41 fingerprints. Coverage-accounting metadata only.

## Definition of done

- Frozen current702 byte-unchanged (no registry write at all — this is representation code only).
- `validate` ok (702 / 41 fp). `git diff --check` clean.
- Full offline suite = the known baseline failures, no NEW regressions, with the re-baselined
  assertions PASSING at the validated numbers.
- Leakage wall intact (new classes read only the Rhea substrate->product equation).
- Refresh docs/project_state.md + decision_log.md + work/handoff.md with the restore
  (0.713 -> ~0.754) and the documented ser_his serine-esterase fold ceiling.

## Why this matters for scaling (context)

This is the precondition for the already-added families to reach SILVER and be cleanly visible to
the discovery probe. Until the representation separates a family, its rows pile up as
`review_chemistry_disagrees` / low-cohesion bronze (un-promotable, un-discoverable). Land this
before sourcing more ester-hydrolase / phosphatase / NAD-redox-subtype families, or that growth is
un-promotable. See docs/discovery_and_de_novo_strategy.md for the broader "scale = diversity x
groundedness, and the representation must keep up" rationale.
