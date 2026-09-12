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
and Figure 9 cryoannealing have different interventions and are not imported.

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
