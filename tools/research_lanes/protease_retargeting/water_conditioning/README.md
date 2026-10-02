This finite experiment asks whether fixing the source water position during scaffolding improves its recovery after sequence design and independent complex prediction. **Completed: eight new computational candidates and all 80 assigned RF3 predictions. The frozen result is no consistent water-conditioning advantage; [all results and the next decision](results_20261002/README.md) are retained.** The source baseline already contains water. It is not an Atlas efficacy comparison, reaction simulation, or activity prediction.

Eight assignments are frozen in `candidate_manifest.json`: four paired RFD3 seeds, one backbone and one public LigandMPNN sequence per arm and seed. Both arms use A187, the same full `ALQSSWGMMGML` substrate and G7–M8 anchors. Real native load/build checks passed after explicitly encoding Zn2+ and correcting the public residue-range syntax. Only water coordinate conditioning differs; native masking also zeroes that water's initial coordinates in the free arm.

The runner checks pinned input bytes and native consumer source, requires the remote native pair receipt, verifies MPNN's actual sequence masks, and extracts enzyme A and substrate B from the native output structure. It never treats concatenated MPNN FASTA as the enzyme. Exact generated sequences become unconditioned RF3 inputs, with a native chemistry/sequence/bond gate before RF3 weights load. Every candidate receives one monomer and one ES prediction batch of five samples. No coordinates, templates or MSA are supplied to RF3.

After the separately approved bootstrap, run:

```sh
python "$CE_P8_PACKAGE/run_prospective_designs.py" \
  --input-dir "$CE_P8_PACKAGE/inputs" \
  --foundry-root "$CE_P8_RUNTIME/foundry" \
  --out-dir "$CE_P8_RUNTIME/experiment" \
  --checkpoint-dir "$CE_P8_RUNTIME/checkpoints" \
  --checkpoint-receipt "$CE_P8_RUNTIME/checkpoint_receipts.json" \
  --native-pair-receipt "$CE_P8_RUNTIME/native_pair_verified.json" \
  --max-seconds 5400 --execute
```

Without `--execute`, this only validates source/input hashes and writes all assignments. An output directory must be new. The script provisions nothing, downloads nothing and retries nothing. The research lead owns the separate two-hour/$5 rental cap, provider termination and retrieval. RF3 starts only with at least 15 minutes remaining inside the runner limit; all missing assignments stay visible. A partial candidate failure never changes the denominator or authorizes replacement.

Primary readout is source-water recovery after independent ES prediction, using the source Zn/two-His frame and excluding water from alignment. All 40 ES outputs are needed for a complete primary comparison; the 40 monomer outputs remain essential context with separate missingness. Four paired median differences, not 40 correlated predictions, are the comparison units. Geometry recovery alone is not productive chemistry or measured function. The measurement script retains metal, water, catalytic donor, register, fold and confidence context.

Measure the complete assigned set without selecting native top-ranked copies:

```sh
python "$CE_P8_PACKAGE/measure_water_recovery.py" \
  --manifest "$CE_P8_RUNTIME/experiment/candidate_manifest.json" \
  --decision "$CE_P8_PACKAGE/prospective_water_constraint.json" \
  --source-pdb "$CE_P8_PACKAGE/source_motif.pdb" \
  --output "$CE_P8_RUNTIME/experiment/water_recovery_measurements.json"
```

Source data attribution and original author-software license are retained in
[design_input](../design_input/README.md). The
[native acceptance result](../native_gate_20261002/README.md) preserves both the
original failure and the explicit corrected input decision.

Weight sizes total 5.740 GB. Previous A100 RF3 inference required approximately 18–24 seconds per five-sample complex group; 80 outputs may require roughly 5–7 minutes plus loading under similar conditions. The author reports RFD3 around 1–2 minutes/backbone on an A4000; eight backbones suggest 8–16 minutes before setup/sequence design/evaluation. These were prospective planning estimates, not measured performance for this package. Actual execution completed all assignments; native output identities and the full prediction readout were checked. See the linked result for measured runtime, failures of geometry recovery and limitations.
