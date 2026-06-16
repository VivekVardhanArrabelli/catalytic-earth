# Metal-independent Phosphodiesterase EC 3.1.4 Hydrolase Source Strategy

Run: 2026-06-16T12:07:09Z

## Result

- Hole state: ['metal_independent_phosphodiesterase'] with floor deficit 100.
- New lane: `metal_independent_pde_ec_3_1_4_hydrolase_non_metal`.
- Preview fetched 120 rows, found 17 target labels, admitted 17, held 22 off-target labels, and had 69 disambiguation holds.
- Row guardrail audit problem rows: 0.
- Floor after applying this preview would be 17; floor reached: False.

## Decision

- Apply authorized: False.
- Reason: Clean row audit passed, but the preview admits only 17 PDE rows and would leave the documented 100-row floor open; autonomous policy avoids tiny topups unless they close a documented floor/cap/blocker.
- Offset diagnostic: UniProt offset URL was emitted, but the applied-label sample duplicated window0; do not use this as independent apply authority.

## Next Action

- Do not apply the 17-row PDE hydrolase preview. Build a stronger PDE source wall outside the already-tested reviewed EC/name/PLD/hydrolase windows, or move to a preregistered source-tier/family expansion only through full gates.
