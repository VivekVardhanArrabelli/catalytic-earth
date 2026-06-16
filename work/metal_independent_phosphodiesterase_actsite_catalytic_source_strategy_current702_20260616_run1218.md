# Metal-independent Phosphodiesterase ACT_SITE Catalytic Source Strategy

Run: 2026-06-16T12:39:00Z

## Result

- Hole state: `metal_independent_phosphodiesterase` remains 0/100 before any apply.
- New lane: `metal_independent_pde_ec_3_1_4_actsite_catalytic_non_metal`.
- Preview fetched 40 reviewed rows, found 2 target labels, admitted 2, held 4 off-target labels, held 23 rows for missing mechanism corroboration, and skipped 11 rows.
- Row guardrail audit problem rows: 0.
- Floor after applying this preview would be 2; floor reached: false.

## Decision

- Apply authorized: false.
- Reason: the ACT_SITE + catalytic-activity source handle is row-clean but admits only 2 target PDE rows and would leave the 100-row floor open.
- EC, ACT_SITE presence, catalytic-activity presence, protein name, and source prose remain source/admission context only. They are excluded context and are never predictive features.

## Next Action

- Do not apply or rerun the same reviewed EC/name/PLD/Hydrolase/ACT_SITE PDE handles. Build a sharper PDE source wall outside these tested windows, or use a preregistered beyond-reviewed source-tier expansion through full gates before any apply.
