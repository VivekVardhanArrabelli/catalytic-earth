Automation ID: ce-nad-glyco-floor-expansion
STARTED_AT=2026-06-13T22:02:05Z
STARTED_LOCAL=Sat Jun 13 17:02:05 CDT 2026
BUDGET_SECONDS=3300
Status: validation/docs closeout in progress.

Latest completed work:
- Added source-window controls to CoA, P450, and molybdopterin source runners.
- Applied 107 gated bronze rows to data/registries/external_bronze_labels.json only:
  molybdopterin +43, P450 +2, CoA +62.
- Counts: external bronze 6645, combined 7347, combined seed surface 5651, gap to 10k seed surface 4349.
- Honest counters: positive_bronze_count 5634; oos_bronze_count 1696; silver_ready_count 0; silver_confirmed_count 17; projected_provisional_count 0.
- Capped families after this run: molybdopterin_oxidoreductase 250/250, cytochrome_p450_monooxygenase 250/250, coa_acyltransferase 250/250.
- Remaining under-floor families: pfkb_ribokinase_family 46/100, biotin_dependent_carboxylase 84/100, glycoside_hydrolase 84/100.

Validation completed:
- Focused pytest: 329 passed, 14 subtests passed.
- PYTHONPATH=src python -m catalytic_earth.cli validate: passed.
- JSON artifact parse checks: passed.
- git diff --check: passed.
