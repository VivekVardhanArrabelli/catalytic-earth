# Pocket Detection Generalization Scout

Generated: 2026-05-28

## Scope

This was a read-only scout for whether Catalytic Earth could eventually use predicted active-site/pocket neighborhoods instead of M-CSA-provided catalytic residue coordinates. No labels, registries, ontologies, thresholds, production scoring, imports, or model outputs were edited.

The requested disk safety floor was not met before the scout started: local `df` showed about 4.7 GiB available, below the 10 GiB minimum. Because of that, and because no pocket predictor was installed, I did not run a pocket prediction smoke sample or download tools.

## Local Inventory

- P2Rank: not available on `PATH` as `p2rank` or `prank`.
- fpocket: not available on `PATH`.
- BioPython: `import Bio` failed in the active Python environment.
- RDKit: `import rdkit` failed in the active Python environment.
- Foldseek executable: not available on `PATH`, but Foldseek coordinate/readiness/TM artifacts are present.
- General predicted pocket sidecars: none found locally.
- Existing pocket-like artifacts: review-only proxy artifacts exist for metal phosphatase and SDR lanes, and current geometry artifacts include `pocket_context`.

Important distinction: the existing `pocket_context` in `artifacts/v3_geometry_features_700.json` is an 8 A neighborhood around known M-CSA catalytic residues. It is useful as a feature baseline and evaluation reference, but it is not an independent pocket prediction.

Relevant local data:

- Current labels: 702.
- Foldseek readiness rows: 702.
- Local Foldseek coordinate CIFs: 692 in `artifacts/v3_foldseek_coordinates_1000/`.
- Local structure files under `artifacts/`: 1186.
- Geometry entries in `artifacts/v3_geometry_features_700.json`: 699.
- Current rows with pocket descriptors from the existing M-CSA-centered geometry: 698.
- Active-site encoder minimal-ready rows from the prior spec: 679/702, including 135/140 heldout rows.

## Safe Sample Protocol

Use a five-row smoke sample only after restoring disk headroom and installing a pinned predictor environment. Candidate rows all have known catalytic residues, local selected structures, and resolved coordinates:

| Entry | Family | Split | Structure | Local coordinate | Resolved residues | Cofactor family |
|---|---|---|---|---|---:|---|
| `m_csa:3` NAD(P)H dehydrogenase (quinone) | flavin dehydrogenase/reductase | heldout | `1D4A` | `artifacts/v3_foldseek_coordinates_1000/pdb_1D4A.cif` | 3 | flavin |
| `m_csa:11` deoxyribonuclease IV | metal hydrolase | in-distribution | `1QUM` | `artifacts/v3_foldseek_coordinates_1000/pdb_1QUM.cif` | 11 | metal ion |
| `m_csa:37` prostaglandin-endoperoxide synthase | heme oxidase/peroxidase | in-distribution | `5COX` | `artifacts/v3_foldseek_coordinates_1000/pdb_5COX.cif` | 7 | heme |
| `m_csa:66` D-alanine transaminase | PLP enzyme | in-distribution | `1DAA` | `artifacts/v3_foldseek_coordinates_1000/pdb_1DAA.cif` | 4 | PLP |
| `m_csa:131` 4-hydroxybenzoate 3-monooxygenase | flavin monooxygenase | heldout | `1DOC` | `artifacts/v3_foldseek_coordinates_1000/pdb_1DOC.cif` | 5 | flavin |

Protocol:

1. Run P2Rank as the primary predictor on the local CIFs; run fpocket as an optional comparator after verified CIF-to-PDB conversion.
2. Keep top-k pockets for `k = 1, 3, 5`.
3. Extract neighborhoods at 8, 10, and 12 A from each predicted pocket center or pocket point set; use 10 A as the primary radius.
4. Score M-CSA catalytic residues only as held-out gold labels: any residue captured, fraction captured, and all residues captured.
5. Score ligand/cofactor capture from local HETATM records: cofactor family captured in the same predicted pocket neighborhood.
6. Classify failures as no structure, parse failure, no pocket, top-1 miss, top-3 miss, ligand-only capture, catalytic-only/no-cofactor capture, chain mismatch, apo selected structure, diffuse surface false positive, split active site, or single-residue gold site not informative.

## Install And Run Requirements

P2Rank is the best first predictor because the current release line supports mmCIF input and runs as a standalone command-line tool. Future environment should pin P2Rank 2.5.1 or newer and Java 17 or later. Example command:

```bash
prank predict -threads 1 -o artifacts/pocket_smoke/p2rank_m_csa3 \
  -f artifacts/v3_foldseek_coordinates_1000/pdb_1D4A.cif
```

fpocket can be installed from conda-forge or built from source. On macOS Apple Silicon, the upstream build uses the `MACOSXARM64` architecture flag. If the selected fpocket build requires PDB input, convert local CIFs in `work/` and do not duplicate all structures. Example command after conversion:

```bash
fpocket -f work/pocket_smoke/pdb_1D4A.pdb
```

BioPython should be installed for robust mmCIF/PDB parsing and conversion:

```bash
python -m pip install biopython
```

RDKit is optional for ligand chemistry normalization, not required for first-pass residue recall:

```bash
python -m pip install rdkit
```

Expected resource profile:

- Tiny 5-row smoke: single CPU, 1-4 threads, minutes after installation; about 20-200 MB incremental disk depending on whether predictor packages and outputs are retained locally.
- current702 run: CPU batch, 8-16 threads recommended, likely hours; about 500 MB to 2 GB incremental disk if retaining compact prediction outputs and avoiding duplicated coordinate sidecars.
- No run should start unless `df -h .` shows at least 10 GiB available.

External install docs checked: P2Rank GitHub, fpocket GitHub, Biopython download page, and RDKit installation docs.

## Future Metrics

Primary pocket recall:

- Top-1 and top-3 any-catalytic-residue recall.
- Top-1 and top-3 fraction of catalytic residues captured.
- Top-1 and top-3 all-catalytic-residues captured.

Cofactor/ligand metrics:

- Required cofactor capture for top-1 and top-3.
- Ligand captured without catalytic residue rate.
- Catalytic residue captured without required cofactor rate.

False positive metrics:

- Extra pocket residue count per predicted pocket.
- Diffuse surface false positive rate.
- Buffer/noncanonical ligand capture rate.
- Chain/entity mismatch rate.

Active-site encoder impact:

- Rows recoverable without M-CSA coordinates.
- Pocket-neighborhood descriptor shift versus M-CSA-centered descriptors.
- Feature completeness delta for local pocket and cofactor features.
- Heldout macro F1 delta in a review-only ablation.
- OOS false non-abstention delta.

## No-Go Conditions

Do not scale pocket extraction if any of these hold:

- Disk is below 10 GiB available before installation or output generation.
- Predictor version, command, and output schema are not pinned.
- M-CSA catalytic coordinates are used as predictor inputs rather than evaluation labels.
- More than 5 percent of sampled local structures fail predictor parsing.
- Top-3 any-catalytic-residue recall is below 0.80 on a smoke/validation subset.
- Required cofactor capture is below 0.70 on holo rows with local cofactor evidence.
- Chain/entity mismatches exceed 2 percent or cannot be diagnosed automatically.
- Apo structure-selection failures dominate and no holo-preference policy is approved.
- Pocket-derived features inflate active-site encoder availability without improving heldout diagnostics.
- Any next step requires label, registry, ontology, threshold, import, production scoring, or model-output edits.

## Bottom Line

Catalytic Earth has enough local current702 structures and M-CSA-coordinate gold labels to test an independent pocket-detection path. It is not ready to scale today: the active environment lacks P2Rank/fpocket/BioPython/RDKit, no general predicted-pocket sidecars are present, and disk headroom is already below the requested floor.
