# Actual native RFD3 chemical and conditioning acceptance

The intact public RFD3 load/build/parse path was executed locally without a model or weights at Foundry commit `0932f1cb165ae7d413c11b1a7acc04ee31758817`. This record establishes that the proposed inputs can express the intended chemistry and the water-coordinate ablation in that consumer. It does not establish successful generation, catalytic activity, a reaction pathway, or an Atlas design advantage.

The unchanged original input completed native parsing but carried neutral Zn and interpreted the `A28-A30` sequence selector as only A28. The original failure is preserved in `native_chemical_acceptance.json` and `attempt-2` snapshots. An earlier empty-transform API attempt is also retained; it did not execute chemistry.

The explicit prospective corrections are in `corrected_inputs/correction_provenance.json`: PDB formal-charge columns for ZN1 set to `2+`; supported range syntax `A28-30`; and the two C1 coordinate masks `ALL` or `ZN1`. The prospective 12mer extension and fixed gap lengths were supplied before generation; they are not an author execution replay. The original `ZnO` component name and all source coordinates are preserved. No Zn–O bond is introduced.

Both corrected arms pass the actual native build: A187, B12 `ALQSSWGMMGML`, Zn charge+2, O charge0, both ligand species retained, all119 source enzyme atoms coordinate-fixed, and exactly the G7/M8 backbone atoms coordinate-fixed on B. Source catalytic roles map A293→A36(H), A294→A37(E), A297→A40(H), A377→A115(Y), A316→A152(E). The only between-arm annotation difference is the water O1 fixed-coordinate flag. Native construction clears that O coordinate to zero when free; every other coordinate is identical. Water is represented by neutral O without explicit hydrogens here.

The ordinary G7C–M8N bond is explicit in the native loaded graph. Native construction represents ordinary peptide connectivity without retaining that explicit edge in the final atom bond array; consecutive residue identities and fixed backbone geometry are preserved. This representation boundary is recorded, not declared a peptide-bond bug.

## Reproduce the gate

Use an official installation of the pinned Foundry checkout and its dependencies. No model checkpoint is needed. These scripts invoke the actual imported API; they do not copy a parser body or emulate the consumer. `--foundry-root` must point to the pinned checkout. The driver verifies the imported input API location and SHA256. Package versions are recorded, and a different Torch version is allowed rather than silently asserted equivalent.

```sh
python native_acceptance.py --foundry-root /path/to/foundry --source-receipt runtime_source_receipt.json --input corrected_inputs/water_fixed.json --output new-fixed-native
python native_acceptance.py --foundry-root /path/to/foundry --source-receipt runtime_source_receipt.json --input corrected_inputs/water_unfixed.json --output new-unfixed-native
python verify_native_pair.py --fixed new-fixed-native --free new-unfixed-native --source-pdb corrected_inputs/ALQSSWGMMGML78_Zn2plus.pdb --output new-pair-verification.json
```

Successful pair status is exactly `passed_actual_native_pair_checks`, with `model_execution: false`. Existing output paths fail rather than being overwritten. `--source-pdb` can be omitted for newly generated gate outputs; it resolves from the fixed gate receipt's input. For the retained snapshots, supply the local copied PDB explicitly because historical receipt paths remain immutable.

`native_snapshots.tar.gz` retains byte-identical original/portable native arrays and receipts. Extract it and run the verifier against `portable-fixed-native` and `portable-unfixed-native` with the copied PDB for a no-dependency receipt check. This verifies recorded results, while rerunning the driver above verifies the actual installed native API. The two are distinct.

## Provenance and limits

`runtime_source_receipt.json` pins the official source tar and every extracted source file. `runtime_package_receipts.json` pins downloaded PyPI payloads. `dependency_resolver.json`, the installation log, and `runtime_versions.txt` record the local environment, which inherited preexisting Conda Torch and other packages. `requirements.txt` and `constraints.txt` describe that local bounded install; the Torch constraint is not a new remote requirement. Exact retained package payloads total154,290,708 bytes and the official source body148,863,396 bytes. Earlier pip resolver traffic was not exactly metered, so these are not an exact all-setup traffic total. No runtime binaries, wheels, weights, or environment are included.

`native_acceptance_local_v1.py` and the original receipts remain unchanged. `driver_portability_receipt.json` records the portable rerun and semantic equality of all native snapshots; JSON annotation key order may differ while values do not.

`measurement_review.json` records six checks of the actual prospective measurement implementation: rigid-motion invariance, exact1Å displacement, two degenerate-frame rejections, five retained assigned samples rather than six including an aggregate, and all assigned denominators with an empty manifest. It establishes arithmetic and accounting only. `check_measurement.py` is the exact local check driver; its fixture paths refer to the recorded local run and prior retained results, so it is audit material rather than a standalone remote test command.
