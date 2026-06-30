# The Decisive Experiment — one pager (2026-06-30)

## 1. What we have done so far
- Built a **mechanism atlas**: given a protein structure, it returns a calibrated, abstaining, mechanism-level function call (with the catalytic residues), by matching against a curated set of mechanistically-characterised enzymes.
- **Validated it on independent gold** (labels from experimental EC, independent of structure): it recovers mechanism for heme 16/16, PLP 14/16, serine 13/16, with **zero confident wrong calls** — it abstains rather than err.
- **Showed it beats the cheap baseline**: structure-based transfer 0.70 vs. sequence-based 0.41 overall, and **2.5×** in the hard "twilight zone" where sequence methods get unreliable.
- **Found its one unique power** — assigning mechanism to proteins that sequence methods *can't* reach — is real but so far only a **2-of-2 existence proof**; that capability lives in the uncharacterised "dark" proteome, where no database has the answer. The lab is the only way to test it there.

## 2. What the experiment is
Take **one uncharacterised protein** that is:
- **dark** — no known function (so the answer exists nowhere; the lab is the first ground truth),
- **sequence-blind** — no usable BLAST/Pfam hit and no help from a protein-LM or an LLM guess,
- **atlas-confident** — the atlas makes a specific, falsifiable mechanism call (named enzyme class + the catalytic residues).

Express the protein and **assay for the predicted activity**, with a control that confirms the *specific* mechanism (the class-matched inhibitor or cofactor dependence), not just "some activity."

*The control that makes this a test of the atlas, not of any tool or LLM:* before the assay we record, in writing, that BLAST, Pfam, a protein-LM, and a blind LLM all **fail** on this exact protein. Only the atlas commits. So if the activity is confirmed, it can only be credited to the atlas.

## 3. How it helps the next step
- **If confirmed** → the first proof that the atlas correctly assigns function where **no existing method or database can**. That is the result that justifies scaling it across the dark proteome and that turns the project from a benchmark argument into a lab-confirmed capability — the asset for funding and collaboration.
- **If not** → we have cheaply learned the unique-capability claim doesn't hold in the extreme regime; we fall back to the atlas's *proven* value (accurate, abstaining, searchable mechanism transfer) and invest in broadening it instead.

Either way, one inexpensive experiment is the decision point.
