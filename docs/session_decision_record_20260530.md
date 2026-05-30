# Catalytic Earth Session Decision Record

Date: 2026-05-30

Scope: the reasoning and decisions made in one working session, in sequence.
This is a record of what was established, what was chosen, and why. It exists
so agents can reconstruct the line of reasoning without chat context.

Re-derive, do not trust blindly. Numbers below are as reported in-session;
confirm each against committed artifacts before building on them.

## Session Arc

The session started with calibration curves back and a real unresolved question:
if geometry already wins, what is the learned phase for? It ended with a clearer
answer. Geometry wins on the structures we have and fails on the structures we
are ultimately building for. The missing piece is reconstructable: predicted
structures delete cofactor/ligand evidence, and sequence can recover part of
that channel. The session moved from model-ranking confusion to a bounded
multi-channel route policy, demonstrated at a zero-leak operating point on the
predicted-geometry heldout, then reframed the long-term architecture around a
measurable mechanism relationship space rather than closed-set label accuracy.

## D1: Do Not Scale Models First

Evidence: Wave 1 representation shootout. Geometry and Foldseek led; ESM-2,
ESM-C, ProtT5, and SaProt trailed on mechanism-level prediction. Two confounds
were identified: method-by-representation, because the same ESM-C representation
scored very differently under logistic-head and cosine-NN readouts, and a
non-standardized geometry join.

Decision: treat Wave 1 as a structural-neighborhood diagnostic, not a
leaderboard. Do not reach for bigger models until decoder and join confounds are
killed.

Ruled out: "learned reps are weak, scale them." That was premature because the
decoder/readout was doing much of the apparent damage.

## D2: The Geometry Gap Is Calibration, Not Discrimination

Evidence: Wave 1.2 geometry-logistic head was correct on answered primary calls
but abstained on many rows whose correct label sat just under threshold. The
geometry baseline was later re-scored on the standardized heldout join and
recovered the canonical primary set with no pure-OOS false positives. An
OOS-aware MLP bought only a small number of rows and stalled.

Decision: the residual gap to the hand router is gating/calibration, not a
missing nonlinearity. Stop adding model capacity to close this specific gap.

## D3: Stop Chasing Hand-Router Parity On M-CSA

Reasoning: matching the hand router on M-CSA overfits to the family already
solved. It is especially suspect when the remaining gap is threshold/gating,
because a threshold tuned to M-CSA's score distribution will not necessarily
transfer. More deeply, the hand router uses per-class hand-authored
fingerprints and structurally cannot call a mechanism nobody wrote a fingerprint
for.

Decision: the real generalization test is leave-one-mechanism-out transfer, not
hand-router parity. This remains deferred until there are enough mechanism
classes or a candidate-class synthesis mechanism.

## D4: Deployment Is Bare Sequence To Predicted Geometry

Reasoning: the unsolved set, enzymes with no assigned mechanism, is
overwhelmingly the set without experimental structure. M-CSA supplies
experimental geometry at train/eval time; deployment supplies predicted
geometry.

Decision: treat predicted-geometry numbers as the real deployment-side numbers.
Experimental-geometry numbers are teacher-side. Architecture choices must answer
to the sequence-to-predicted-geometry input distribution.

## D5: The Information Ceiling

Evidence: the M-CSA heldout was folded from AlphaFoldDB and re-run on predicted
geometry. AF2 is apo, so there were zero proximal ligand rows. The hand router
dropped from the clean experimental-coordinate result to a lower predicted
geometry result with wrong non-abstained primary calls and OOS/secondary leakage.
The wrong calls were cofactor-defined and directional, such as heme or flavin
being pulled toward metal hydrolase. Training heads in-domain on predicted
geometry did not recover the edge.

Insight: this is an information ceiling, not a modeling ceiling. AF2 deletes the
cofactor channel. If the discriminating feature is absent from the input, model
capacity cannot recover it.

Decision: stop modeling this gap directly. Reconstruct the missing cofactor
channel.

## D6: Reconstruct The Cofactor Channel From Sequence

Evidence: clean cofactor-presence labels were derived from experimental ligand
context for most current702 rows. Mechanism-fingerprint cofactors were marked
circular and reference-only. K-mer logistic was poor, which was diagnosed as a
featurization failure rather than absence of signal: bag-of-k-mers cannot
represent discontinuous spatial binding motifs. External literature supports
metal/cofactor prediction from sequence using protein language model features.

Decision: reconstruct cofactor presence from sequence and fuse it back into the
predicted-geometry route policy. Borrow mature external predictors for weak
classes where support is small; train only where support is adequate. The
cofactor channel input must be sequence-only, not geometry-derived, or it will
not transfer to predicted-geometry deployment.

## D7: Channel Confirmed; Route Policy Is The Open Problem

Evidence: borrowed M-Ionic had useful heldout metal signal and recovered named
cofactor-defined predicted-geometry failures. Raw fusion recovered more calls
but leaked false positives. Suppression kept false positives low but abstained
more.

Decision: the cofactor channel is recoverable. The remaining problem is
calibrated multi-channel selective prediction, which is bounded engineering
rather than open research.

## D8: Beat The Frontier With Concordance, Not A Threshold

Reasoning: a single fusion threshold only slides along a one-score
precision/recall frontier. To move the frontier, add orthogonal information. The
geometry channel and sequence-cofactor channel have partly uncorrelated failure
modes, so a false positive passing a concordance gate needs both channels to err
the same way.

Decision: use a two-axis selective rule. Make a primary call only when geometry
is confident, cofactor evidence is confident, and the channels concur; abstain
otherwise. Use class-conditional cofactor trust, initially leaning on metal and
discounting weak organic-cofactor calls until their reliability is resolved.

Done-bar: recover more than the suppression regime and leak less than raw
fusion, simultaneously.

## D9: Route Policy Closed

Evidence: false-positive attribution showed raw-fusion leakage was
OOS-concentrated. The concordance gate accepted more primary calls than
suppression while producing zero OOS/secondary false positives and zero
wrong-primary calls in the predicted-geometry heldout audit.

Decision: stop and report. The route-policy open problem is closed at the
bounded level tested: a deployable operating point is demonstrated on the
predicted-geometry heldout, not claimed at scale beyond it and not claimed to
survive unchanged once stronger organic-cofactor channels are added.

Primary artifacts:

- `artifacts/v3_predicted_geometry_fusion_fp_attribution_and_concordance_gate_current702_20260529.json`
- `work/predicted_geometry_fusion_fp_attribution_and_concordance_gate_current702_20260529.md`

## D10: Three Bets, Two-Lane Topology

Bets:

- Organic-cofactor resolution to lift the channel-quality ceiling.
- Leave-one-mechanism-out for the real generalization test.
- Targeted label expansion into underpowered dark bins such as
  `no_reliable_structure` and `low_structure_neighborhood_near_orphan`.

Collision: LOMO and expansion both touch evaluation split semantics in opposite
directions. LOMO needs a frozen snapshot; expansion adds rows. Running them
against shared mutable state would corrupt the transfer number.

Decision:

- Organic-cofactor resolution can run freely.
- LOMO must read a frozen snapshot tagged before expansion writes.
- Expansion must write to a separate branch/proposal and merge only after LOMO
  has its baseline.
- Agents report to a frozen state; humans integrate.
- No agent rewires route policy or rolls into the next lever on its own.

Snapshot used:

- `snapshot/concordance-gate-current702-20260530`
- `f393ad25c3959778c7e66a68974bcfee6c93f031`

## D11: Mechanism As A Physically Faithful Continuous Space

Agent returns:

- Organic-cofactor resolution lifted the ceiling and inverted the preliminary
  trust hierarchy: flavin and PLP separated well in aggregate, and heme was
  useful, while M-Ionic metal remained useful but no longer uniquely strongest.
  Caveat: row-level ESM cofactor scores were not retained, so only aggregate
  separability exists today. Gating must stay conservative until row-level
  sidecars are persisted and class-conditional weights are re-derived.
- LOMO did not show exact open-set recovery. This is a safe result, not a
  thesis failure: when asked to recover a mechanism class it has never seen and
  has no fingerprint for, the current system mostly abstains instead of
  misfiling into a known class.
- Targeted bin expansion was disciplined: it identified a small diagnostic batch
  for dark/near-orphan/OOS controls without imports, split changes, or dense-bin
  padding.

Architecture commitment:

Mechanism should be represented as a continuous mechanism-feature space, not
only as a closed set of labels. This space must answer to the physics of
mechanism-as-chemistry: electron flow, transition-state stabilization, proton
transfer, and bond making/breaking. It must not answer merely to the current
hand-feature list or to closed-set label accuracy.

De novo implication:

De novo is not a bolt-on. A physically faithful space has valid unoccupied
regions by construction. De novo is the same objective read out in an unoccupied
region. Candidate-class synthesis is deferred until the space is measurably
faithful and the closed-set atlas is trustworthy on a populated dark regime.

Measurement requirement:

The continuous space must ship with a faithfulness evaluation over held-out
relationships, not just held-out rows. Convergent pairs with the same chemistry
and unrelated folds should be near; divergent pairs with the same fold and
different chemistry should be far; OOS or unseen chemistry should abstain or sit
outside occupied clusters. This is the early de novo validity check.

Refined D11 pass policy:

- Hygiene pass: known relationship units behave correctly under rank-based,
  scale-free metrics.
- Real D11 pass: hygiene pass plus held-out-class placement works on predicted
  geometry using a cofactor-augmented representation with row-level cofactor
  scores.
- If row-level cofactor scores are missing, the real-pass tier is blocked, not
  passed or failed.
- Claims must remain bounded to the evaluated family set. Passing current702
  LOMO placement means the space organizes the current family set, not that it
  has proven general physical fidelity.

Next artifact:

- `artifacts/v3_mechanism_relationship_eval_v0_20260530.json`
- `work/mechanism_relationship_eval_v0_20260530.md`

## State At Session End

- The pipeline thesis holds end to end at the bounded level tested: geometry
  carries mechanism; predicted structure deletes cofactor evidence; sequence can
  reconstruct part of the missing channel; concordance can fuse the channels at
  a zero-leak operating point on the predicted-geometry heldout.
- The route-policy open problem is closed for the current predicted-geometry
  heldout.
- The long-term architecture is now a measurable mechanism relationship space,
  not a closed-label classifier.
- Open next items: row-level cofactor sidecar persistence and gate reweighting,
  targeted dark-bin expansion, safe-abstention LOMO reframing, and D11
  relationship-eval v0.

## Non-Negotiables

- M-CSA is eval/benchmark, never training data.
- Cofactor-presence labels come from experimental ligand context. Mechanism
  fingerprint cofactors are circular and reference-only.
- Cofactor head input is sequence-only, never geometry-derived.
- OOS false positives are a hard gate, not a tiebreaker.
- The deployment test is predicted geometry. Experimental-geometry numbers are
  teacher-side.
- The mechanism-feature space answers to mechanism chemistry, not to the
  hand-feature list or closed-set label accuracy.
- Abstention-on-novelty is the de novo precondition, not just a quality metric.

