# Glycoside Hydrolase Floor Top-up Live Fetch Blocker

Run: 2026-06-13T17:29:16Z

- Status: optional second top-up preview blocked; no second registry write.
- Completed earlier in this run: +27 glycoside hydrolase bronze rows, external bronze 6449 -> 6476, combined 7178, glycoside hydrolase 45 -> 72.
- `--max-records-per-lane 650` failed before any artifact because the runner caps the value at 500.
- `--max-records-per-lane 500` was interrupted for closeout after no artifact was written; traceback showed it in `fetch_uniprot_entry` TLS/connect work.
- Remaining floors: PfkB 46/100, glycoside hydrolase 72/100, biotin 84/100.

## Next exact action

- Retry the 500-row glycoside hydrolase preview early in a run, or add paging/resume support before attempting deeper windows. Keep EC/name/Rhea/keyword/prose/feature handles excluded from predictive evidence and apply only after novelty/dedup/governor/trust-tier/cap checks pass.
