# ePK false-positive hunter handoff

- Started: 2026-05-20T14:16:23Z
- Ended: 2026-05-20T15:05:26Z
- Measured minutes: 49.05
- Primary outcome: evidence_against
- Rule under attack: `epk_mek_erk_tyr_or_n_terminal_substrate_mode_counteraxis_v0` with `epk_mek_erk_source_free_topology_ambiguity_counteraxis_v0`.
- Production claim allowed: false
- Labels/fingerprints changed: false

## Search surface
- atpase_transport: 110 rows, 0 exact counterexamples, 2 substrate-mode hits, 0 topology-clear hits.
- walker_a_confirmation: 75 rows, 0 exact counterexamples, 7 substrate-mode hits, 0 topology-clear hits.
- non_epk_atp_mg_enzymes: 110 rows, 0 exact counterexamples, 7 substrate-mode hits, 0 topology-clear hits.

Total reviewed: 295 rows, 281 unique PDB IDs. Seed attack IDs included: 7CAG, 8BMS, 9L3M, 9L3U, 7ZE5. No raw coordinate files were written; mmCIFs were fetched in memory and reduced to compact distance/context evidence.

## Result
No exact counterexample survived the current topology counteraxis. The bounded surface is exhausted for this run, so the outcome is `evidence_against`, not production safety evidence.

## Pressure cases
These non-ePK ATP/Mg rows satisfy the substrate-mode shape locally but are blocked by same-chain topology ambiguity:

- 4BJR: Crystal structure of the complex between Prokaryotic Ubiquitin-like Protein Pup and its Ligase PafA; ATP PG to TYR62 OH = 4.182 A; Mg = 3.512 A; topology_blocked=True (same-chain)
- 4G5Y: Crystal Structure of Mycobacterium tuberculosis Pantothenate synthetase in a ternary complex with ATP and N,N-DIMETHYLTHIOPHENE-3-SULFONAMIDE; ATP PG to TYR82 OH = 3.697 A; Mg = 3.41 A; topology_blocked=True (same-chain)
- 4KFT: Structure of the genome packaging NTPase B204 from Sulfolobus turreted icosahedral virus 2 in complex with ATP-gammaS; AGS PB to SER18 OG = 4.423 A; Mg = 3.281 A; topology_blocked=True (same-chain)
- 5J1J: Structure of FleN-AMPPNP complex; ANP PG to THR25 OG1 = 5.258 A; Mg = 3.213 A; topology_blocked=True (same-chain)
- 5TT6: T4 RNA Ligase 1 (K99M); ATP PG to TYR37 OH = 3.297 A; Mg = 3.13 A; topology_blocked=True (same-chain)
- 6NOO: Structure of Cyanothece McdA-AMPPNP complex; ATP PG to THR16 OG1 = 5.401 A; Mg = 3.244 A; topology_blocked=True (same-chain)
- 6NOP: Structure of Cyanothece McdA(D38A)-ATP complex; ATP PG to THR16 OG1 = 5.327 A; Mg = 3.254 A; topology_blocked=True (same-chain)
- 6U1D: Thermus thermophilus D-alanine-D-alanine ligase in complex with ATP, D-alanine-D-alanine, Mg2+ and Rb+; ATP PG to TYR229 OH = 5.5 A; Mg = 3.023 A; topology_blocked=True (same-chain)
- 6U1E: Thermus thermophilus D-alanine-D-alanine ligase in complex with ATP, D-alanine-D-alanine, Mg2+ and Rb+; ATP PG to TYR229 OH = 5.833 A; Mg = 3.085 A; topology_blocked=True (same-chain)
- 8P53: Cryo-EM structure of the c-di-GMP-free FleQ-FleN master regulator complex of P. aeruginosa; ACP PG to THR25 OG1 = 5.017 A; Mg = 3.45 A; topology_blocked=True (same-chain)
- 9M1F: Crystal structure of E. coli tryptophanyl-tRNA synthetase complexed with chuangxinmycin and ATP in closed-closed state; ATP PG to SER13 OG = 3.82 A; Mg = 3.278 A; topology_blocked=True (same-chain)
- 9M1G: Crystal structure of E. coli tryptophanyl-tRNA synthetase complexed with chuangxinmycin and ATP in open-closed state; ATP PG to SER13 OG = 4.091 A; Mg = 3.315 A; topology_blocked=True (same-chain)
- 9NBO: Closed conformation of ArsA from L. ferriphilum in complex with MgATP and arsenite; ATP PG to THR23 OG1 = 5.14 A; Mg = 3.584 A; topology_blocked=True (same-chain)
- 9NBW: Closed conformation of ArsA from L. ferriphilum in complex with MgATP and arsenite at 1.5 minute time point; ATP PG to THR23 OG1 = 5.517 A; Mg = 3.899 A; topology_blocked=True (same-chain)

## Interpretation
The corrected rule read matters: current topology ambiguity blocks candidate-chain equals ATP-associated-chain hits. The apparent counterexamples `5TT6`, `6NOO`, and `9NBW` were therefore demoted to pressure cases after matching the exact same-chain topology behavior in `src/catalytic_earth/labels.py`.

## Next query
Target cross-chain non-ePK ATP/Mg complexes where the hydroxyl acceptor is on a different polymer chain from the ATP-associated chain, with Tyr or auth_seq_id <= 25 Ser/Thr/Tyr geometry and no reciprocal cross-chain pair.

## Files
- `artifacts/research_lanes/epk_false_positive_hunter/stress_summary_20260520.json`
- `artifacts/research_lanes/epk_false_positive_hunter/epk_false_positive_hunter_runs.jsonl`
- `tools/research_lanes/epk_false_positive_hunter/atpase_substrate_mode_stress.py`
