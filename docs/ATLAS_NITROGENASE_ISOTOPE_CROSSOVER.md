# Nitrogenase gas and solvent isotope discrimination

Lukoyanov et al. report two opposite-solvent EPR contrasts in wild-type
*Azotobacter vinelandii* nitrogenase. With ordinary water held fixed, replacing
H2 gas with D2 narrows the trapped g1 = 2.15 feature. With heavy water held
fixed, replacing D2 with H2 broadens it. The source interprets these observations
as gas-derived bridge isotopes persisting in the assigned E4 state despite the
opposite solvent isotope.

The [primary manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC5024552/),
DOI [10.1021/jacs.6b06362](https://doi.org/10.1021/jacs.6b06362), supplies the
two comparisons in paragraph P28 and Figure 8A. The
[source packet](../data/atlas/study_context/nitrogenase_2016/source_qualification.json)
binds the retained XML, exact paragraph/caption locators and their text hashes.
It separates observations from the authors' mechanistic interpretation.

```sh
python scripts/query_atlas_perturbations.py --control-relation nitrogenase_2016:WT:gas-solvent-isotope-crossover --verify-witnesses
```

The existing repository consumer returns one assessed system relation. Its two
rows each retain a test and reference condition, giving four explicitly named
conditions without inventing four absolute linewidth measurements.

| Fixed solvent | Test gas | Reference gas | Source-reported test feature |
| --- | --- | --- | --- |
| H2O | 0.1 atm N2 + 0.9 atm D2 | 0.1 atm N2 + 0.9 atm H2 | Narrower |
| D2O | 0.1 atm N2 + 0.9 atm H2 | 0.1 atm N2 + 0.9 atm D2 | Broader |

Figure 8 specifies stirring. General Methods gives 50 micromolar MoFe protein
and 75 micromolar Fe protein for X-band samples, 20–25 seconds of turnover,
then freezing in liquid nitrogen. EPR was measured at 12 K; that is not the
turnover temperature. The complete turnover mixture, exact assayed sequence,
isotope purity and biological replicate statistics are not supplied in the
inspected main-text scope. Four to eight scans are instrument scans.

The state assignment uses WT H/D-sensitive EPR features and WT deuterium ENDOR,
with correspondence to earlier variant hydride characterization (P17–P20,
Figure 5). The authors could not obtain satisfactory strongly coupled proton
ENDOR for WT in H2O. Thus the relation preserves a source-assigned E4(4H) state
with two bridging hydrides, without claiming a complete independently measured
WT hydride tensor or an atom-resolved geometry.

The crossover is evidence against complete equilibration of the assigned
bridge isotopes with solvent before trapping in these experiments. Gas origin,
oxidative addition and solvent nonexchange are mechanistic interpretations
using the state assignment and broader spectroscopy. The two width comparisons
do not themselves track H2 cleavage, N2 release or elementary bond events.
Every arm contains N2, so they do not supply a no-N2 control. The paper's
E4(2N2H) label is a diazene-reduction-level assignment with unknown structure
and coordination geometry. Numerical widths, isotope fractions, exchange-rate
bounds, photolysis rates and thermodynamic estimates are outside this relation.

This adds primary WT state/isotope information absent from M0212's coarse
source pathway. It does not establish a source-step, accession, assayed-sequence
or 1N2C correspondence, and it changes no M0212 chemistry. Figure 8B photolysis
and Figure 9 cryoannealing have different interventions and are not imported
into the isotope relation.

The existing `system_assessment` operation resolves source rows, assay and
assessed evidence. A shared paired-context check now requires the row's test
and reference IDs to match two distinct nested conditions; swapped, missing or
fabricated membership fails. It adds no nitrogenase-specific code or arithmetic.
The consumer serves both metal-substitution and gas/solvent isotope questions.
Source selection, pair declarations and chemical interpretation remain manual;
matching IDs cannot authenticate the isotope labels or interpretation. No
curation-time saving or general mechanistic inference is established. This is
CE-050 source annotation: two qualitative paired assertions, zero new proteins,
net reactions, mechanism steps or project experiments.

The [acquisition ledger](../data/atlas/study_context/nitrogenase_2016/acquisition_receipts.json)
records three requests and 136,555 raw response-body bytes for this distinct
2016 primary-study batch. The closed Spatzal2011 batch and all prior budgets
remain unchanged. Article bodies stay in the Git-common source cache; the
repository contains factual paraphrases and provenance. This repository query
is not added to the installed wheel or promoted to independent review,
experimental admission or design validation.

## Cryoannealing links source-assigned states without assigning elementary rates

The same manuscript reports following EPR signals from four assigned states
during relaxation of a frozen WT sample. P34–P35 interpret loss of E4(2N2H)
as kinetically coupled to formation of E4(4H), the Janus state, in the
oxidative-addition direction of the proposed reversible activation equilibrium.
The source also describes onward relaxation through E2 to E0. Formation in
that model does not establish a net rise in the Janus signal.

```sh
python scripts/query_atlas_perturbations.py --model-link nitrogenase_2016:WT:cryoannealing_state_coupling --verify-witnesses
```

This existing model query returns two qualitative state-specific views of one
reported cryoannealing experiment, one source-assigned coupling, and the
previously reviewed WT hydride-state assignment. Both directional rate slots
remain unassigned. The [primary projection](../data/atlas/study_context/nitrogenase_2016/cryoannealing_evidence.json)
and [model relation](../data/atlas/study_context/nitrogenase_2016/model_context.json)
keep the measured signal, assigned chemical state and mechanistic
interpretation separate.

| Evidence layer | Supported scope |
| --- | --- |
| Primary experimental report | EPR time courses for the assigned E4(2N2H) and E4(4H) states were monitored during cryoannealing. No raw series or net Janus rise is projected. |
| Source interpretation | Nitrogenous-state loss and Janus formation are kinetically coupled; this is the authors' interpretation, not a directly measured bond event. |
| Conditions | Figure 9 describes WT low N2 pressure, approximately 0.05 atm, turnover in H2O followed by frozen-solid annealing at −50 °C. These are distinct from the stirred 0.1 atm isotope experiments. |
| Quantitation | The source scales E4 intensities to concentrations using its three-step model. This does not provide independent populations with which to validate that model. |

The retained Figure 9 caption reports stretched/distributed decay fitting;
its time constants are not elementary rate constants. The actual Figure 9
and Chart 3 images, raw points and original fitting procedures have not been
inspected here. No curve shape, time-constant-to-arrow mapping, fit, rate ratio
or population balance is reconstructed. The selected edge is not a closed
two-state system: onward relaxation and EPR-silent populations remain outside
its two projected endpoints. The 12 K setting applies to the referenced Janus
EPR readout, not annealing or turnover, and the other states use separately
cited readout protocols.

The shared consumer binds each declared state observation to its source assay
and incident transition. This prevents transferring a time course to another
experimental phase while retaining the existing observation/model machinery.
Case-specific chemistry remains in data. Source interpretation and applicability
still require manual review; no curation-time saving or autonomous inference
is measured. This is a modest extension of CE-050, not a complete nitrogenase
mechanism, direct H2 uptake/N2 release measurement, exact cluster geometry,
independent review or design result. It consumes no new source requests;
the existing study batch remains at three requests and 136,555 bytes.
