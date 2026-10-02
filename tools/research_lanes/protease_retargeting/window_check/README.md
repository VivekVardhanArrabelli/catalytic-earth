# TDPn3 substrate-window comparison

**Prepared, not executed.** Does adding the two omitted assay residues change
the predicted pose at the same G7–M8 bond? This is the next available
computational test of transferring the short substrate model to a longer
context. The separate Zn45 Y152F/I kinetic question still needs matched
experimental evidence; this comparison cannot answer it.

The [10-residue input](tdpn3_rf3_window_10mer.json) and
[12-residue input](tdpn3_rf3_window_12mer.json) contain the same exact published
187-residue TDPn3 sequence and disconnected `[Zn+2].O` chemical input. Only
`ALQSSWGMMG` versus `ALQSSWGMMGML` changes. They use the native JSON format of
[pinned RF3](https://github.com/RosettaCommons/foundry/blob/0932f1cb165ae7d413c11b1a7acc04ee31758817/models/rf3/README.md).
RF3 is a new predictor for this case; the short-window condition is an internal
reference, not reproduction of the published AF3 prediction.

The [decision record](tdpn3_rf3_window_decision.json) fixes two seeds, five
samples per seed per condition, and all other settings before results:
20 assigned structures, no templates or pose restraints, no rescue sampling.
Both native inputs must first preserve sequence, connectivity, ligand identity
and chemical graph. Record the actual parser atom map and checkpoint hash.

Report every prediction and missing assignment. The primary measurement is
Zn–G7 carbonyl-O distance, using the source's <3.2 Å contact filter only as a
computational diagnostic. Full catalytic distances, water placement, competing
carbonyl contacts and native confidence accompany it. The descriptive outcome
rules require all 20 assigned outputs; missingness cannot create a favorable
or unfavorable contact classification.

Zn outside the H146/H150/E45 site makes its carbonyl contact uninformative about
catalytic-site recognition. Water outside a plausible catalytic arrangement
prevents a catalytic-preorganization interpretation even if that contact is
retained. The input's disconnected SMILES does not impose coordination.

Adding M11/L12 also moves the free terminus, so this test cannot isolate a
terminal-charge mechanism. Neither free peptide reproduces the fusion reporter
or folded full-length target. A consistent difference can reject unchanged
geometry transfer **within RF3**; a null or inconclusive result cannot validate
activity, specificity, Atlas benefit or success at Problem 8.

The user approved one bounded Prime Intellect A100 run ($5 total, 45 minutes),
which is provisioning at this checkpoint. Native parsing and inference remain
unexecuted; input preparation is not an experiment result.

The [remote driver](rf3_native_gate.py) uses RF3's actual input parser and
checks the pinned parser/engine sources, sequences, ordinary peptide bonds,
and disconnected Zn/water charge identity. Its default mode loads no model
weights. The [command sequence](rf3_remote_commands.sh) runs that gate first,
then the two fixed seeds only with an explicit local checkpoint and recorded
content hash. Both files passed syntax checks; their native execution remains
unverified. The driver records all 20 assignments before importing RF3, so a
failed import or chemistry gate cannot erase the experiment denominator.

On an authorized, prepared remote host, set `CE_RF3_DRIVER`,
`CE_RF3_INPUT_DIR`, `CE_RF3_OUT` (a fresh destination), `CE_RF3_CKPT`, and
`CE_RF3_CKPT_SHA256`; optionally set `CE_RF3_FOUNDRY` to the exact pinned
checkout. Then run `bash rf3_remote_commands.sh`. This command does not install
software, download weights, provision or terminate a machine. The owner must
enforce the authorized rental deadline through the provider.
