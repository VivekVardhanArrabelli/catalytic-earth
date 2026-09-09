# Hourly source review: POX decision and polymer-role correction

Start: 2026-09-09T16:07:04Z. Parent owns Git and the cooperative lock.
Owner: `01a086ec-0ced-7bf3-92ae-3e0448bdb035:83aa4384-3910-4370-82c7-6d8c7d78fffc`.
Base: `4613df97790c555eb7719612ade412e035042bc4` on clean synchronized main.
Working branch: `codex/polymer-role-20260909` (renamed before publication from
`codex/pox-portability-20260909` after the scientific pivot).
Previous main CI run 34372455283 passed all four jobs. No open PR or recovery
work existed; parent fetched and fast-forwarded clean main under the lock.

## POX portability decision

Question: would candidate 4FEG/H89-prime support a consequential crop omission
through the unchanged assembly engine? Expected gain: a portability/use decision;
stop if evidence, actual use or shared representation does not justify a packet.

The parent's initial search of src/scripts/docs found only the 6HA3 consumer.
The representation lane corrected that incomplete search: legacy
`artifacts/v3_geometry_features_1025.json`, entry `m_csa:274`, uses 1POW and
`structure.py:pocket_context_from_atoms` without assembly expansion. Thus an
adjacent POX consumer exists; absence of any POX consumer is not the conclusion.

Both the agent and parent reproduced one retained 1POW example through the
unchanged `project_assembly` engine. Source:
`artifacts/v3_foldseek_coordinates_1000/pdb_1POW.cif`, SHA-256
`fdba1a836cd0ccbdf544bcd2e85827a71d034286cc84603b6c67f4494fbcf026`.
Assembly 1, model 1, E60 OE1/OE2 at operator 1 versus H89 ND1/NE2 in the same
label chain gives selected minimum distances A: 6.246179 Å at operator 1 and
2.808878 Å at operator 2; B: 6.573127 and 2.886452 Å. This is geometric evidence
for an omitted copy in the deposited-only legacy representation, not a trusted
biological template or a 4FEG result. The exact spec/result is in the Git-local
run receipt companion `83aa4384-pox-adjacent-check.json`.

The retained Nature study describes 4FEG as a WT Breslow-intermediate state
with ordinary hydrogen bonds. Its MAP analogue binding, anaerobic pyruvate/FAD
single-turnover processing, and artificial DCPIP turnover are separate
endpoints. H89 mutants are not a 4FEG mutant structure or a partner-only
perturbation. The 6HA3 reviewed-context wrapper requires assay-specific NMR and
reporter fields; low-level coordinate reuse does not prove full-packet reuse.

Decision: no 4FEG capture/packet. Its specific copy identity and omission remain
untested, not disproved. Deprioritize further same-paper geometry because the
new polymer-role defect below has more immediate corrective value under the
current atlas brief. No old predictor work queue is restarted.

## M0970 source question and adjudication

Question: is the current growing-polymer acceptor role correct, and what does
primary evidence establish about elongation direction? Expected gain: a
source-bound role correction or retained ambiguity that changes future polymer
representation. Stop after role/direction adjudication; no invented X00676,
numeric chain length, full stepwise mechanism or processivity.

Finding: Huang et al. 2012 (PMID 22493270, PMC3340074, DOI
10.1073/pnas.1203900109) places the growing glycan at donor S2 and incoming
lipid II at acceptor S1 in its proposed SaMGT model. Its 3VMT analogue has a
GalNAc position-4 hydroxyl inversion and is described as unable to serve as an
E100 substrate. The construct, analogue and source-model limits stay explicit.

Perlstein et al. 2007 (PMID 17914829, PMC3206585, DOI 10.1021/ja075965y)
provides a discriminating reducing-end direction test using longer Gal-capped
oligomers with/without lipid II. The short capped Lipid II/IV tests alone do not
determine direction because their uncapped substrates can self-condense. The
four tested PGT domains do not directly test Q99T05/SaMGT. Current M-CSA
mechanism-1 prose reverses the textual attacking role relative to the primary
model; mechanism 2 describes the acceptor attacking the donor. Preserve this
source conflict and all existing exact-instance abstentions.

The packet at `data/atlas/polymer_context/m0970/` stores chemistry and source
findings. `build_atlas50_state_probe.py --query-case M0970` exposes the current
role and its own source references beside the case. All three inherited
reports stay byte-identical, as do their gate permissions. The current view
changes only role wording and adjacent provenance, not states or permissions.

| Lane | Contribution and final state |
| --- | --- |
| Source, with bounded extraction child | Checked retained POX sources; then independently reviewed M0970 primary sources and final artifact/docs. Accepted after exact section-locator corrections. Child stopped. |
| Representation | Found legacy 1POW consumer, reproduced unchanged-engine example; reviewed generic current-state view. Required validation of every report binding and role-level source references. Both fixed; final code review accepted. |
| Parent | Acquired/counts sources, adjudicated priority and source conflicts, wrote data/current view, integrated and verified; sole Git/lock owner. |

Source and representation agents used gpt-5.6-sol / ultra. Review was informed,
can contain correlated errors, and is not independent human review. The final
review pins bind source-accepted annotations and inventory. No editing worker
was used; no worker acquired sources or changed Git/lock state.

## Reuse, budget and remaining work

- Representation: case-specific chemistry stays in data; no enzyme-ID branch
  was added. Role depends on reaction context, not compound identity alone.
- Curation: one correction serves three pinned historical generations without
  manual rewrites or reacquisition of each. No timed speedup is claimed.
- Added value: prevents a role reversal and a nonproductive analogue transfer.
  Underlying biology is already in incumbent sources; this is a project
  correction, not a biological discovery or design-performance result.
- Continue `atlas50.computational-panel-review.2026-09-05`: inherited 21 measured
  captures / 1,125,005 bytes plus seven requests / 349,400 bytes (including one
  empty 404), total 28 / 1,474,405. Historical browser checks remain unmetered.
  `human-tkt-e160q-6ha3-geometry-function` stays at seven / 3,004,884.
- Frozen kernels, protected registries and exposure history are unchanged.
  No new protein, reaction, mechanism, project experiment or evidence tier.
- Next useful action: decide whether the source-proposed elongation model can
  be represented as a symbolic chain transition under the existing generic
  state contract without resolving X00676 or inventing processivity. Expected
  gain: a justified symbolic drafting scope or a precise representation stop.
  Do not repeat the resolved role/analogue review or extend same-paper geometry.

The marked current handoff and Git-local run receipt hold final verification,
publication and release state. No self-hash follow-up commit is required.
