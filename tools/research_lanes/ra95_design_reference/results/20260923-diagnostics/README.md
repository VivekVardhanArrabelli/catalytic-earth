# RA95 packing diagnosis — 2026-09-23

The packing stage preserves fixed residue identities and side-chain torsions,
but **does not preserve their Cartesian coordinates**. It reconstructs every
residue using backbone frames and idealized atom geometry. This explains how
the nine motif atoms moved 2.425 Å RMS despite unchanged C-alpha coordinates
and fixed-residue chi changes of at most 0.053449 degrees.

This is a source-traced explanation supported by the preserved coordinates;
no instrumented replay, corrected packing or new model run occurred.

| Measurement | Before packing | After packing |
| --- | ---: | ---: |
| A112 CA–CB–CG angle | 88.306° | 113.735° |
| A118 CA–CB–CG angle | 127.171° | 113.682° |
| Lys78 NZ–LLK C13 separation | 1.266973 Å | 1.509058 Å |

The unusual initial bond angles help explain the large terminal-atom shifts:
A112 OH moves 5.024 Å and A118 OH moves 2.673 Å. Copying the original fixed
coordinates back would also restore those unusual angles. That would not
establish a physically better structure or solve the later folding result.
The finding concerns the meaning of “fixed”; it is not evidence of an upstream
software defect.

The original generated reference has 36 intraligand `CONECT` records, but no
protein–ligand `CONECT` edge. Packing retains no `CONECT` records. The native
input's Lys–LLK edge was already absent from the generated PDB before packing;
it remains witnessed in the original RFdiffusion2 input tensors. Do not
attribute that earlier omission to LigandMPNN or interpret coordinate proximity
as a complete chemical graph.

Chai consumed only the generated FASTA, so packed coordinates and connectivity
were not passed into its five predictions. The packing diagnosis does not
explain or repair their catalytic-site rearrangement. The next relevant control
is the [known-active parent](../../parent_control/README.md), using its apo
reference and the same protein-only prediction settings.

## Reproduction and source evidence

[packing-checks.json](packing-checks.json) is recomputed from the unchanged
tracked continuation bundle using only Python's standard library:

```bash
python3 tools/research_lanes/ra95_design_reference/results/20260923-diagnostics/inspect_packing.py
```

The bundle hash is checked before reading its original reference and packed
PDB members. The calculation reports every selected motif displacement, all
fixed-residue chi changes, both tyrosine angle changes, C-alpha/ligand coordinate
identity and connectivity counts. An independent calculation on the retained
outputs agreed on the motif RMSD and maximum displacement.

The executed upstream revision is `d365cbf4db3958814a9f8e4f6f94fa309dfebc2b`:

- [run.py](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/fused_mpnn/run.py#L454)
  passes the fixed-residue mask into packing and writes its returned coordinates.
- [sc_utils.py](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/fused_mpnn/sc_utils.py#L193)
  retains true fixed-residue chis, then builds atom14 coordinates from backbone
  frames and literature geometry (also applied during packing updates).
- [data_utils.py](https://github.com/RosettaCommons/RFdiffusion2/blob/d365cbf4db3958814a9f8e4f6f94fa309dfebc2b/fused_mpnn/data_utils.py#L111)
  writes that full protein coordinate tensor plus copied ligand atoms.

Original outputs and their earlier report are preserved unchanged. These are
post hoc diagnostic measurements, not new activity or design-success evidence.
