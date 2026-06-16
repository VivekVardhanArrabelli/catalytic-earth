# Metal-independent Phosphodiesterase Sharp Handle Count Scout

Run: 2026-06-16T12:23:30Z

Non-destructive UniProt header-count scout. No labels or registries were written. EC, keyword, name, active-site, and binding-site handles are source/scope only and remain excluded context if later used in a preview.

## Result

- Handles probed: 9.
- Broad hydrolase baseline: 490 reviewed rows; this baseline already previewed to 17 admitted rows.
- Best sharper non-baseline handle: `actsite_catalytic_non_metal` with 119 reviewed rows before disambiguation/novelty.
- Handles >=100 raw rows: 2.
- Handles >=150 raw rows: 1 (only the broad baseline).

## Counts

| Handle | reviewed count |
| --- | ---: |
| `broad_ec314_hydrolase_non_metal` | 490 |
| `actsite_catalytic_non_metal` | 119 |
| `cyclic_nucleotide_exact_ecs_non_metal` | 58 |
| `binding_catalytic_non_metal` | 40 |
| `gdpd_domain_name_non_metal` | 22 |
| `glycerophosphodiester_name_non_metal` | 22 |
| `phospholipase_d_non_metal` | 22 |
| `ribonuclease_t2_non_metal_boundary` | 17 |
| `nucleotide_pyrophosphatase_non_metal_boundary` | 2 |

## Decision

- Apply authorized: False.
- Reason: This is a count scout only. The broad hydrolase baseline has 490 raw rows but already previewed to 17 admitted rows. The best sharper non-baseline reviewed handle has 119 raw rows before disambiguation/novelty, below the 150 preferred batch gate and unlikely to close the 100 PDE floor after holds.
- Next: Do not rerun these reviewed handles for apply. Design a truly new PDE source wall or move to a beyond-reviewed source-tier expansion through full gates.
