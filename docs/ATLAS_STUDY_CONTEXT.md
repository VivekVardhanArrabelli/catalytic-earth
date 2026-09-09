# Atlas study-context packets

Study-context packets connect a deposited arrangement to measured observations
only at the identity and evidence strength directly supported by the retained
sources. They sit beside Atlas source drafts: they do not change frozen Atlas-3,
Atlas-10, or current702 rows, and they do not increase an Atlas evidence tier.

The first packet covers human transketolase E160Q with the F6P-ThDP adduct in
PDB 6HA3. It supplies a reproducible coordinate projection and separates three
experimental endpoints:

- acid-quench NMR intermediate accumulation;
- pre-steady-state reversible F6P-ThDP formation kinetics; and
- steady-state X5P/R5P turnover.

This distinction matters because the turnover substrate context is not the
deposited F6P donor state. The packet joins the first two observations to the
arrangement only as same-study, same-reported-variant associations; it does not
claim identical preparations or conditions, crystal-to-solution state identity,
or geometry-to-rate causation.

Run the deterministic validation with:

```bash
python scripts/validate_atlas_study_context.py
```

The validator reads chemistry selections from the packet, parses the retained
mmCIF with the shared strict parser, recomputes selected atom facts and geometry,
checks component-dictionary bonds separately from deposited connections, and
requires the review pins to remain current.
