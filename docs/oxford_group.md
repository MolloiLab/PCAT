# Oxford Group: Pericoronary Adipose Tissue Research Program

> **Principal Investigator: Prof. Charalambos Antoniades, MD PhD FRCP FESC**
> British Heart Foundation Chair of Cardiovascular Medicine, University of Oxford
> Founder and Director, Caristo Diagnostics Ltd.

## Abbreviation Glossary

| Term | Full Name |
|------|-----------|
| PVAT | Perivascular Adipose Tissue |
| FAI | Fat Attenuation Index |
| FAI-Score | Fat Attenuation Index Score (scanner-adjusted, age/sex-normalized) |
| FRP | Fat Radiomic Profile |
| EAT | Epicardial Adipose Tissue |
| CABG | Coronary Artery Bypass Grafting |
| CCTA | Coronary Computed Tomography Angiography |
| CT | Computed Tomography |
| MRI | Magnetic Resonance Imaging |
| PET | Positron Emission Tomography |
| HU | Hounsfield Units |
| RCA | Right Coronary Artery |
| LAD | Left Anterior Descending Artery |
| LCx | Left Circumflex Artery |
| IMA | Internal Mammary Artery |
| CAD | Coronary Artery Disease |
| ACS | Acute Coronary Syndrome |
| AMI | Acute Myocardial Infarction |
| MACE | Major Adverse Cardiovascular Events |
| HR | Hazard Ratio |
| AUC | Area Under the Curve |
| NRI | Net Reclassification Improvement |
| ICC | Intraclass Correlation Coefficient |
| ICER | Incremental Cost-Effectiveness Ratio |
| QALY | Quality-Adjusted Life Year |
| eNOS | Endothelial Nitric Oxide Synthase |
| BH4 | Tetrahydrobiopterin |
| 4-HNE | 4-Hydroxynonenal |
| MDA | Malondialdehyde |
| PPARγ | Peroxisome Proliferator-Activated Receptor Gamma |
| ADIPOQ | Adiponectin Gene |
| NADPH | Nicotinamide Adenine Dinucleotide Phosphate |
| NOX | NADPH Oxidase |
| RAC1 | Ras-related C3 Botulinum Toxin Substrate 1 |
| WNT5A | Wingless-Type Family Member 5A |
| FZD2 | Frizzled-2 Receptor |
| USP17 | Ubiquitin-Specific Peptidase 17 |
| SFRP5 | Secreted Frizzled-Related Protein 5 |
| PI3K | Phosphoinositide 3-Kinase |
| Akt | Protein Kinase B |
| AMPK | Adenosine Monophosphate-Activated Protein Kinase |
| SNP | Single Nucleotide Polymorphism |
| VPCI | Volumetric Perivascular Characterization Index |
| hsCRP | High-Sensitivity C-Reactive Protein |
| NICE | National Institute for Health and Care Excellence |
| NHS | National Health Service |
| ESC | European Society of Cardiology |
| RCT | Randomized Controlled Trial |
| GWAS | Genome-Wide Association Study |
| SaMD | Software as a Medical Device |
| MDR | Medical Device Regulation (European) |
| CE | Conformité Européenne |
| FDA | Food and Drug Administration (United States) |
| HPLC | High-Performance Liquid Chromatography |
| FMD | Flow-Mediated Dilation |
| BNP | B-type Natriuretic Peptide |
| PASI | Psoriasis Area and Severity Index |
| VSMC | Vascular Smooth Muscle Cell |
| PEG-SOD | Polyethylene Glycol-Conjugated Superoxide Dismutase |

## Table of Contents

* [How They Built This: Research Architecture](#how-they-built-this-research-architecture)
* [Phase 1: The Biology (2013 to 2016)](#phase-1-the-biology-2013-to-2016)
* [Phase 2: Conceptual Framework Building (2017 Reviews)](#phase-2-conceptual-framework-building-2017-reviews)
* [Phase 3: Fat Attenuation Index, From Biology to Imaging (2017 to 2018)](#phase-3-fat-attenuation-index-from-biology-to-imaging-2017-to-2018)
* [Phase 4: Extending the Science (2019)](#phase-4-extending-the-science-2019)
* [Phase 5: Clinical Translation (2020 to 2023)](#phase-5-clinical-translation-2020-to-2023)
* [Phase 6: Population-Scale Validation (2024 to 2026)](#phase-6-population-scale-validation-2024-to-2026)
* [The Patent](#the-patent)
* [Caristo Diagnostics](#caristo-diagnostics)
* [Open Questions and Limitations](#open-questions-and-limitations)
* [Knowledge Gaps to Fill](#knowledge-gaps-to-fill)
* [Paper Catalogue](#paper-catalogue)

## How They Built This: Research Architecture

The Oxford program spans 13 years and follows a coherent logic: establish the biology in human tissue, translate it to an imaging readout, validate the imaging in large cohorts, standardize it for clinical use, and build the regulatory and economic evidence for adoption.

What makes it work is the tight coupling between bench science and clinical imaging. Each imaging claim traces back to a specific molecular mechanism demonstrated in human tissue. This is rare. Most imaging biomarkers are discovered empirically (statistical association with outcomes) and only later investigated mechanistically, if at all. The Oxford group worked the other direction: they understood why perivascular adipose tissue changes before they ever measured it on a computed tomography scan.

**The Coronary Artery Bypass Grafting Tissue Pipeline** is central to everything. Oxford's cardiac surgery service provides:

1. Internal mammary arteries with intact perivascular adipose tissue for ex vivo vascular experiments
2. Saphenous veins for vasomotor studies
3. Matched adipose tissue from multiple depots (the specific depots vary by study, as detailed in each phase)
4. Preoperative computed tomography imaging for imaging to histology correlation

Cumulative tissue biobank across papers: n=677 (2013), n=575 (2014), n=386 (2015), n=306 (2016), n=453+45+273 (2017), n=167 (2019 Fat Radiomic Profile), n=1,004 (2019 Wingless-Type 5A), n=1,246 (2023 miR-92a-3p). This represents thousands of matched tissue and imaging pairs, built up over a decade.

**How each paper connects to the next:**

```
2013 Adiponectin/eNOS → Outside-to-inside signaling established
  ↓ But what about NADPH oxidase specifically? And disease states?
2015 Adiponectin/NADPH oxidase in type 2 diabetes → Mendelian randomization, coculture proof
  ↓ But this is arteries only. What about the myocardium?
2016 Epicardial adipose tissue to myocardium signaling → Inside-to-outside loop completed
  ↓ Perivascular adipose tissue composition reflects vascular disease. Can imaging detect this?
2017 Fat Attenuation Index discovery → CT captures inflammation-induced PVAT changes
  ↓ Cross-sectional only. Does it predict future events?
2018 CRISP-CT → FAI predicts cardiac mortality in 3,912 patients
  ↓ FAI is dynamic and reversible. What about chronic structural damage?
2019 Fat Radiomic Profile → Radiomic texture captures fibrosis and vascularity
  ↓ What molecular pathways beyond adiponectin drive PVAT dysfunction?
2019 WNT5A → Second druggable axis identified
  ↓ How to standardize FAI across scanners for clinical use?
2021 FAI-Score → Scanner-adjusted, age/sex-normalized metric
  ↓ Does it hold at scale? Is it cost-effective?
2024 ORFAN → 40,091-patient validation
2025 Cost-effectiveness → ICER £1,371 to £3,244 per QALY
```

No paper repeats the previous one. Each answers a specific limitation and opens a new question.

## Phase 1: The Biology (2013 to 2016)

### Margaritis et al. 2013, Circulation | n=677+46 Coronary Artery Bypass Grafting patients

This paper established the core idea: perivascular adipose tissue and the vascular wall communicate bidirectionally through paracrine signals.

**Methods worth understanding in detail:**

1. **Brachial flow-mediated dilation measured the day before surgery** gives an in vivo endothelial function measure to correlate with ex vivo tissue findings. This bridge between clinical and bench data is a recurring design element throughout the program.

2. **Lucigenin chemiluminescence (5 μmol/L)** for vascular superoxide. The lower concentration reduces redox cycling artifacts inherent to higher doses. This concentration is used consistently across all Phase 1 papers.

3. **High-performance liquid chromatography for biopterins (tetrahydrobiopterin/dihydrobiopterin ratio)** quantifies endothelial nitric oxide synthase cofactor availability, which determines whether eNOS produces nitric oxide (coupled) or superoxide (uncoupled). This assay is technically demanding and specific to the Oxford group's longstanding expertise.

4. **Two adiponectin gene single nucleotide polymorphisms (rs17366568, rs266717)** used as Mendelian randomization instruments. These genetic variants alter circulating adiponectin levels, providing quasi-causal evidence without the confounding of observational data.

5. **4-Hydroxynonenal incubation of perivascular adipose tissue (30 μmol/L, 16 hours) with or without the Peroxisome Proliferator-Activated Receptor Gamma inhibitor T0070907 (10 μmol/L)** tests the reverse signal (vessel to fat).

6. **CD36 as positive control for PPARγ activity.** CD36 is a known PPARγ target gene. Its expression is quantified alongside ADIPOQ in every paper as an independent validator of PPARγ pathway activation. This consistent internal control is a methodological signature of the entire program.

**The 8-step logical chain:**

1. Circulating adiponectin correlates with endothelium-dependent (but not independent) vascular function, establishing specificity
2. Circulating adiponectin inversely correlates with vascular superoxide, BUT local PVAT adiponectin positively correlates with vascular superoxide. This paradox reveals two different regulatory systems
3. Circulating adiponectin tracks with remote fat depots (mesothoracic, subcutaneous) but NOT perivascular, confirming different regulation
4. PPARγ is the master regulator of ADIPOQ across all depots (correlation coefficients 0.344 to 0.976 across PPARγ target genes)
5. ADIPOQ SNPs predict circulating adiponectin and endothelial function, but do NOT predict PVAT adiponectin. This is critical: the genetic instruments affected adiponectin release from mesothoracic adipose tissue (the remote depot) but not from perivascular adipose tissue, meaning local PVAT production is driven by vascular redox signals that override genetic programming
6. Exogenous adiponectin (recombinant full-length, 10 μg/mL for 6 hours) restores eNOS coupling in ex vivo vessels
7. Dual mechanism: Phosphoinositide 3-Kinase/Protein Kinase B-mediated eNOS phosphorylation (blocked by wortmannin at 100 nmol/L) plus tetrahydrobiopterin biosynthesis (blocked by 2,4-Diamino-6-Hydroxypyrimidine). Importantly, DAHP did NOT block adiponectin's effect on eNOS phosphorylation; it only blocked BH4 increases. This dissociation proves the two mechanisms are independent
8. Vascular oxidative stress (4-HNE) upregulates PVAT adiponectin approximately 1.9-fold in peri-saphenous vein tissue and 1.7-fold in peri-internal mammary artery tissue via PPARγ. This is the reverse signal (vessel to fat)

**Tissue depots in this study:** 4 depots from a 248-patient subgroup: perivascular tissue around the internal mammary artery (peri-IMA-AT), perivascular tissue around the saphenous vein (peri-SV-AT), subcutaneous adipose tissue, and mesothoracic adipose tissue (attached to the pericardium). There is no separate "epicardial" depot in this study.

**What was new:** The bidirectional cross-talk concept. Previous work had shown PVAT releases adipokines that affect vessels (outside-to-inside). Nobody had shown the vessel signals back to the fat (inside-to-outside). The dissociation between circulating and local adiponectin, showing they have opposite associations with vascular superoxide, was a genuine insight that reframed the field.

**Hidden details:**

* The ex vivo vascular experiment sample sizes are small: saphenous vein rings n=9 pairs, internal mammary artery n=5 pairs for the adiponectin incubation experiments. 4-HNE protein adducts quantified in only 11 saphenous veins and 18 internal mammary arteries. PVAT 4-HNE incubations: n=6 each. These are the numbers behind the biological claims.
* Only 176 of 677 patients had biopterin data from both saphenous vein and internal mammary artery. The correlation between circulating adiponectin and the tetrahydrobiopterin ratio was described as "significant but weak."
* Sample size calculations were explicitly provided: 500 patients estimated for the clinical analysis, 150 for the tissue experiments. Both were exceeded.

**Honest limitations:**

1. 4-HNE at 30 μmol/L is a pharmacological concentration; physiological relevance at the tissue interface is assumed
2. No demonstration that adiponectin (a 30 kDa+ multimeric protein) actually diffuses from perivascular adipose tissue across the adventitia into the vessel wall. Paracrine delivery is assumed but never measured
3. 83% male; no sex-stratified analysis
4. The Mendelian randomization validates only the circulating (systemic) pathway, not the local paracrine pathway they emphasize as novel

### Antonopoulos et al. 2014, Arteriosclerosis Thrombosis and Vascular Biology | n=575+13+19

Often overlooked but scientifically elegant. This paper explained why adiponectin rises in heart failure patients despite its protective biology (the "adiponectin paradox").

**Four-arm study design:**

1. Cross-sectional study (n=575): 201 healthy, 173 coronary artery disease with ejection fraction above 50%, 135 coronary artery disease with ejection fraction 30 to 50%, 33 coronary artery disease with ejection fraction below 30%, 33 heart failure without coronary artery disease
2. 258 CABG patients with adipose tissue biopsies from femoral, subcutaneous, and thoracic depots
3. 13 CABG patients for ex vivo tissue incubation
4. 19 healthy volunteers randomized to *Salmonella typhi* vaccine (n=10) versus placebo (n=9) as an in vivo model of inducible low-grade inflammation

**Key findings:**

* B-type natriuretic peptide (1 nmol/L) reversed the suppressive effects of inflammatory stimulation (Interleukin-6 + Tumor Necrosis Factor Alpha) on PPARγ, CD36, and ADIPOQ in femoral adipose tissue. This explains the paradox: BNP, which is elevated in heart failure, drives adiponectin production as a compensatory mechanism.
* **Depot-specific inflammation responsiveness is a major finding.** Only femoral adipose tissue responded to inflammatory cytokines ex vivo. Thoracic and subcutaneous adipose tissue did NOT respond. The explanation: thoracic adipose tissue already had the highest CD68+ macrophage infiltration and the highest M1/M2 ratio (CCR7/CD206), making its PPARγ signaling unresponsive to further inflammatory challenge. Femoral adipose tissue had the least macrophage infiltration, the largest adipocyte size, and was therefore most responsive. This depot-specific responsiveness informed the 2015 paper's use of thoracic adipose tissue as a "control" for perivascular tissue.
* Adiponectin-to-flow-mediated dilation correlation weakened progressively with disease severity: strong in healthy subjects (r=0.323), weaker in coronary artery disease with ejection fraction above 50% (rho=0.245), weaker still with ejection fraction 35 to 50% (rho=0.168), and completely absent in heart failure (ejection fraction below 30% or non-ischemic). This progressive uncoupling has clinical implications for biomarker interpretation.
* The *S. typhi* vaccination model is an elegant in vivo approach. Vaccination induced Interleukin-6 increase as an early response and high-sensitivity C-reactive protein as a late response, and significantly reduced circulating adiponectin at 12 hours versus placebo. BNP levels remained unchanged, confirming that inflammation (not BNP) drove the decrease.
* Circulating adiponectin was NOT correlated with plasma hsCRP (r=-0.125, P=0.095) or serum IL-6 (r=0.089, P=0.239) in the CABG cohort. This surprising negative result challenges the simple "inflammation suppresses adiponectin" narrative and points to depot-specific mechanisms rather than a global systemic effect.

### Antonopoulos et al. 2015, Diabetes | n=386+67 Coronary Artery Bypass Grafting patients

Extended the 2013 work to NADPH oxidase specifically and to the disease context of type 2 diabetes.

**Key methodological advances over 2013:**

1. **Vas2870 (40 μmol/L)**, a specific NADPH oxidase inhibitor, allows isolation of NADPH oxidase-derived superoxide from total superoxide
2. **Thoracic adipose tissue (non-vessel-associated)** added as a control depot, positioned as a cleaner comparison than subcutaneous because it is in the thoracic cavity but not adjacent to any visible vessel
3. **Coculture system:** PVAT incubated with or without its matched internal mammary artery, with or without NADPH stimulation (100 μmol/L), with or without PEG-SOD (300 units/mL). This directly tested whether vascular NADPH oxidase activity signals to neighboring perivascular adipose tissue

**The finding that matters most:** In multivariable analysis including ADIPOQ genotype, type 2 diabetes loses independent prediction of NADPH oxidase activity (β=0.068, P=0.192) while the adiponectin gene genotype remains significant (β=-0.081, P=0.001). This is genuine Mendelian randomization evidence that type 2 diabetes's effect on vascular oxidative stress is mediated through adiponectin.

**Important negative finding:** Plasma malondialdehyde (a systemic oxidative stress marker) does NOT correlate with arterial NADPH oxidase-derived superoxide (r=0.076, P=0.448). Plasma 4-hydroxynonenal similarly showed no significant difference across normoglycemic, insulin-resistant, and type 2 diabetic groups. This is one of the most consequential observations in the entire program: systemic blood biomarkers cannot substitute for local tissue assessment. This finding recurs throughout their work and is the fundamental justification for imaging-based approaches.

**Two temporal mechanisms of adiponectin on NADPH oxidase:** Rapid (6 hours): Ras-related C3 botulinum toxin substrate 1 deactivation, preventing NADPH oxidase assembly at the membrane. Subacute (18 hours): p22phox protein downregulation. At 6 hours, p22phox gene expression was already reduced but protein levels were not yet affected. By 18 hours, both RAC1 effects persisted AND p22phox protein was significantly reduced.

**Hidden details:**

* Adiponectin receptor expression (AdipoR1, AdipoR2, and CDH13/T-cadherin) was preserved in type 2 diabetic vessels. This means the reduced Akt phosphorylation at serine 473 observed in type 2 diabetic internal mammary arteries is due to lower circulating adiponectin, not receptor downregulation, and exogenous adiponectin can still rescue the phenotype. This is directly relevant to therapeutic strategies.
* In the coculture experiments, PEG-SOD not only prevented NADPH-induced ADIPOQ upregulation but dropped ADIPOQ expression BELOW the baseline of PVAT cultured with its artery but without NADPH stimulation. This proves that even basal vascular superoxide production contributes to maintaining PVAT adiponectin expression. The coculture design (n=6 per group) is the strongest direct evidence for inside-to-outside signaling in the entire series.
* 4-HNE upregulated ADIPOQ by 63% in perivascular adipose tissue while malondialdehyde had no effect. This specificity for 4-HNE over MDA is maintained across all Phase 1 papers and suggests a specific receptor or uptake mechanism for 4-HNE in adipocytes that has not been identified.
* ADIPOQ genotype had no effect on plasma MDA (P not significant), reinforcing that systemic oxidative stress markers are disconnected from arterial wall oxidative stress.

### Antonopoulos et al. 2016, Circulation Research | n=247+59

Extended bidirectional signaling from the perivascular-artery axis to the epicardial adipose tissue-to-myocardium axis. This was the bridge from peripheral vascular biology to the cardiac compartment.

**The most important finding that distinguishes this paper from 2013 and 2015:** Adiponectin's effect on myocardial NADPH oxidase is mediated through AMP-Activated Protein Kinase (AMPK), NOT through Phosphoinositide 3-Kinase/Protein Kinase B as in arteries. Compound C (AMPK inhibitor) reversed adiponectin's protective effect on myocardial superoxide. This tissue-specific kinase switch (PI3K/Akt in arteries, AMPK in myocardium) is a subtle but important mechanistic finding that the program has not fully explored. It implies that therapeutic targeting of adiponectin signaling may need tissue-specific approaches.

**Three independent model systems for validation:**

1. Human ex vivo myocardial tissue paired with epicardial adipose tissue from cardiac surgery patients
2. mNOX2-transgenic mice (cardiac myocyte-specific NADPH oxidase 2 overexpression, 20-week-old males)
3. Pig model of rapid atrial pacing (4 weeks, generating atrial oxidative stress)

**Critical mechanistic insight:** Hydrogen peroxide SUPPRESSED ADIPOQ expression in epicardial adipose tissue. Only 4-hydroxynonenal (a lipid peroxidation product) works as the transferable paracrine signal. Malondialdehyde (another lipid peroxidation product) consistently had NO effect across this paper and the 2015 paper. This means that reactive oxygen species themselves are not the signal; rather, the specific downstream lipid peroxidation product 4-HNE is the transferable mediator. This specificity has never been mechanistically explained (no receptor identified) and represents an open question.

**Other important details:**

* In the mouse model, mNOX2-transgenic mice had increased 4-HNE (but not MDA) adducts in myocardium, upregulated ADIPOQ in pericardial adipose tissue but NOT subcutaneous adipose tissue. This tissue specificity is powerful in vivo evidence.
* In the pig model, rapid atrial pacing increased 4-HNE (but not MDA) and upregulated ADIPOQ in epicardial adipose tissue but NOT subcutaneous adipose tissue. Replication across species strengthens the finding.
* Adiponectin Receptor 1 (but not AdipoR2 or CDH13) correlated with myocardial NADPH oxidase activity. This receptor specificity in heart tissue differs from the vascular situation and deserves further investigation.
* The H9c2 coculture system (rat cardiac myocyte-derived cells exposed to NADPH for 2 hours, then cocultured with rat epicardial adipose tissue for 16 hours) showed that NADPH-stimulated cardiomyocytes upregulated ADIPOQ, PPARγ, and CD36 in cocultured EAT. This was blocked by PEG-SOD and Vas2870. Neither H9c2 cells alone nor NADPH alone had any effect; the combination was required.

### What Phase 1 Teaches Us

The biology rests on a specific experimental toolkit: organ bath physiology, lucigenin chemiluminescence, HPLC biopterins, Western blotting for signaling intermediates, dihydroethidium fluorescence microscopy, ex vivo coculture, and Mendelian randomization via adipokine gene variants. Understanding these methods, their strengths and their artifacts, is essential for evaluating and extending the work.

**Recurring methodological signatures across all Phase 1 papers:**

* Lucigenin consistently at 5 μmol/L for superoxide measurement
* CD36 as positive control for PPARγ activity in every experiment
* T0070907 at 10 μmol/L for PPARγ inhibition
* The same two ADIPOQ single nucleotide polymorphisms (rs17366568, rs266717) reused as Mendelian randomization instruments, applied progressively to eNOS coupling (2013), NADPH oxidase (2015), and myocardial NADPH oxidase (2016)
* 4-HNE at 30 μmol/L for 16 hours as the standard "inside-to-outside" signal stimulus
* MDA consistently negative across all experiments (a powerful specificity control)

The CABG patient population constrains generalizability. These are patients with advanced multi-vessel coronary artery disease, mean age approximately 65, 83% male, nearly all on statins and angiotensin-converting enzyme inhibitors. Whether bidirectional PVAT-vascular signaling operates similarly in early disease, younger patients, or women is an open question.

## Phase 2: Conceptual Framework Building (2017 Reviews)

Five reviews in a single year, across 4 journals. Their function was to synthesize the group's biological findings into a conceptual framework and identify the field's unresolved problems, which their upcoming work would address.

| Paper | Journal | Core Contribution |
|-------|---------|-------------------|
| "Epicardial Adipose Tissue in cardiac biology" | Journal of Physiology (Impact Factor 5.5) | Comprehensive EAT biology reference: embryology, thermogenesis, mechanical buffering, paracrine signaling |
| "Is fat always bad?" | Cardiovascular Research (10.2) | Argued fat has protective roles that become pathological through "reprogramming," the conceptual basis for FAI |
| "Dysfunctional adipose tissue" | British Journal of Pharmacology (7.3) | Introduced the concept that adipose dysfunction is a reprogrammable therapeutic target |
| "Perivascular adipose tissue as regulator of vascular disease" | British Journal of Pharmacology (7.3) | Mapped the full PVAT secretome and signaling pathways; identified therapeutic targets |
| "Unravelling the adiponectin paradox" | British Journal of Pharmacology (7.3) | Resolved why high adiponectin associates with poor outcomes in heart failure |

The adiponectin paradox resolution is worth understanding: epidemiological studies found elevated adiponectin in patients with worse cardiovascular outcomes, contradicting its known protective biology. The Oxford group's answer, that vascular oxidative stress upregulates PVAT adiponectin as a defense mechanism (inside-to-outside signaling), means elevated adiponectin in sick patients is a marker of the rescue response, not the disease itself. The 2014 paper added that B-type natriuretic peptide, which is elevated in heart failure, independently drives adiponectin production. This is a clean example of mechanistic biology resolving an epidemiological contradiction.

These reviews also systematically evaluated competing approaches. Epicardial adipose tissue volume studies (Framingham, Multi-Ethnic Study of Atherosclerosis, Rotterdam) had produced inconsistent results, partly because they treated EAT as a homogeneous depot. PET-CT could detect tissue inflammation but with poor spatial resolution and limited availability. Circulating biomarkers (hsCRP, Interleukin-6) lacked vessel-specificity. These were real limitations of existing methods, identified clearly before the group presented their alternative.

## Phase 3: Fat Attenuation Index, From Biology to Imaging (2017 to 2018)

### Antonopoulos et al. 2017, Science Translational Medicine | approximately 872 citations

The conceptual leap: if vascular inflammation changes PVAT adipocyte biology (inhibiting differentiation, reducing lipid accumulation), and CT attenuation depends on the lipid-to-water ratio in tissue, then CT can non-invasively detect vascular inflammation by measuring the attenuation of perivascular fat.

**Four-arm study design (each arm answers a different question):**

1. **Arm 1 (n=453 CABG):** Histological validation. Paired tissue biopsies and CT, showing that FAI correlates with adipocyte size, differentiation markers (PPARγ, CCAAT/Enhancer-Binding Protein Alpha, Fatty Acid-Binding Protein 4), and macrophage infiltration.
2. **Arm 2 (n=45 CABG):** Coculture proof. Aortic tissue pre-treated with angiotensin II (100 nM, 7 days) then cocultured with PVAT preadipocytes inhibits their lipid accumulation. Recombinant Tumor Necrosis Factor Alpha (4 ng/mL) + Interleukin-6 (25 ng/mL) + Interferon Gamma (20 ng/mL) directly suppress adipocyte differentiation genes.
3. **Arm 3 (n=273 CCTA subjects):** Clinical validation. FAI higher around culprit lesions in acute coronary syndrome, decreases on follow-up after stenting. FAI predicts coronary artery disease independently of calcium score.
4. **Arm 4 (n=22 ACS patients):** Culprit lesion identification. FAI increased by 8.76 ± 2.87 Hounsfield Units around culprit lesions compared to proximal segments. Area under the curve for detecting unstable plaques = 0.91 (0.80 to 1.00), P=0.0003.

**PET sub-study (n=39 to 40 subjects):** 18F-fluorodeoxyglucose uptake in subcutaneous adipose tissue correlated with FAI (Spearman rho=0.69, AUC=0.971 at a target-to-background ratio cutoff of 0.200). However, this AUC drops to 0.894 and 0.791 at other cutoffs, and the validation was in subcutaneous fat, NOT epicardial fat. The paper explains this: epicardial FAI is driven by local coronary signals rather than systemic inflammation, making PET validation in epicardial tissue inappropriate by the group's own logic.

**Measurement protocol defined here:**

1. Attenuation window: -190 to -30 Hounsfield Units
2. Perivascular adipose tissue = adipose tissue within radial distance equal to vessel diameter from outer wall
3. Right coronary artery: 10 to 50 mm from ostium (excludes proximal 10 mm to avoid aortic wall artifact)
4. Left anterior descending and left circumflex: proximal 40 mm
5. Analyzed in 3D concentric 1 mm layers radiating outward from the vessel wall, up to 20 mm

**Volumetric Perivascular Characterization Index:** A gradient-based metric calculated as [100 × (FAI_PVAT minus FAI_non-PVAT) / |FAI_PVAT|], where non-PVAT is the most distal concentric layer (20 mm from the right coronary artery wall). This self-normalizes against systemic metabolic factors because each patient's remote fat serves as their own reference. VPCI was superior to raw FAI for detecting soft (noncalcified) plaques, though both were only of "moderate diagnostic value" for vulnerable plaques by existing definitions.

**Hidden details that constrain interpretation:**

* FAI does NOT correlate with CD68 macrophage markers in epicardial fat (rho=0.180, P=0.096) or macrophage polarization (CCR7/MRC1, rho=-0.173, P=0.109). This means FAI is not a direct macrophage marker. It tracks adipocyte differentiation state, which is an indirect consequence of inflammation. This mechanistic distinction matters.
* Insulin resistance (HOMA-IR) associated with subcutaneous adipose tissue FAI but NOT epicardial FAI. This supports the claim that pericoronary fat changes are locally driven by coronary inflammation, not systemic metabolic disease.
* The ex vivo to in vivo FAI correlation was done in only 105 patients (a subgroup of Arm 1 who also had CCTA).
* The 5-week dynamic FAI claim (FAI decreases after stenting) is based on only n=5 myocardial infarction patients and n=5 stable coronary artery disease controls. Very small numbers for a dynamic biomarker claim.
* The paper explicitly acknowledges its main limitation: "the lack of data demonstrating predictive value for clinical outcomes." CRISP-CT was designed specifically to address this.

### Oikonomou et al. 2018, The Lancet (CRISP-CT) | n=3,912 | approximately 838 citations

Post-hoc analysis of two prospective cohorts: Erlangen, Germany (n=1,872, enrolled 2005 to 2009, median follow-up 72 months) and Cleveland Clinic, United States (n=2,040, enrolled 2008 to 2016, median follow-up 54 months). Five different CT scanners (3 Siemens, 1 Philips, 1 dual-source Siemens Force). All images analyzed blindly at the Oxford Academic Cardiovascular CT Core Lab (OXACCT) by three trained analysts.

**Key results:**

| Metric | Derivation (Erlangen) | Validation (Cleveland) |
|--------|----------------------|----------------------|
| Per-standard-deviation FAI (RCA), hazard ratio for cardiac mortality | 2.15 (1.33 to 3.48) | 2.06 (1.50 to 2.83) |
| FAI ≥ -70.1 HU, hazard ratio for cardiac mortality | 9.04 (3.35 to 24.40) | 5.62 (2.90 to 10.88) |
| C-statistic improvement | 0.913 to 0.962 | 0.763 to 0.838 |
| Net Reclassification Improvement for cardiac mortality | 0.94 | 0.72 |
| Technical parameters R-squared for FAI | approximately 0.05 | not reported |
| Intraclass Correlation Coefficient (intra/inter-observer) | 0.987 / 0.980 | not reported |

**The J-shaped relationship** is noteworthy: fractional polynomial modeling showed a non-linear FAI to mortality association. Extremely negative FAI (very fatty PVAT) may also be pathological, potentially reflecting lipomatous metaplasia or loss of normal adipocyte architecture. This motivated dichotomization at -70.1 HU (Youden's J statistic, yielding 85.0% specificity and 67.7% sensitivity) rather than treating FAI as purely linear.

**The positive predictive value at this cutoff is only 5.9%.** The negative predictive value is 99.5%. This means the test is far better at ruling out risk than confirming it. Among those flagged as "high risk," fewer than 6 in 100 actually died of cardiac causes. This asymmetry has practical implications for clinical deployment.

**Hidden details:**

* Left circumflex artery FAI was NOT significantly predictive of cardiac mortality in either cohort (derivation hazard ratio 1.32, P=0.24; validation hazard ratio 1.29, P=0.13). Only right coronary artery and left anterior descending were predictive. This exclusion of the left circumflex from prognostic models means an entire coronary territory is not assessed.
* Left main artery was excluded due to variable length. This is a practical limitation since left main disease carries the highest mortality risk.
* Mean FAI values were -75.1 HU (standard deviation 8.6) in derivation and -77.0 HU (standard deviation 8.5) in validation. The -70.1 cutoff is approximately 0.6 standard deviations above the mean. About 28 to 29% of the population falls above this cutoff.
* Only 26 cardiac deaths in the German derivation cohort (1.4%). The large hazard ratios are derived from very few events, and the event-to-variable ratio in the multivariable Cox model is low.
* Medication profiles differed dramatically between cohorts: Erlangen had 35% on statins versus Cleveland 40%; angiotensin-converting enzyme inhibitors/angiotensin receptor blockers 43% versus 29%; beta-blockers 45% versus 15%. This heterogeneity is both a strength (generalizability) and weakness (confounding).
* Among patients who started statins or aspirin after CCTA, FAI lost prognostic significance (adjusted hazard ratio 2.85, 95% confidence interval 0.44 to 18.49, P=0.25). This could mean the risk is treatable, or that the subgroup was too small for adequate statistical power (confidence interval spans nearly two orders of magnitude).
* Acute myocardial infarction was a secondary endpoint: FAI ≥ -70.1 associated with hazard ratio 5.08 (1.89 to 13.61, P=0.0012) in post-hoc analysis, linking abnormal FAI to plaque instability.
* There IS a brief high-sensitivity C-reactive protein reference in the paper: FAI correlated with hsCRP at rho=-0.11 (P=0.25) in an independent cohort of 107 individuals (described as unpublished data). The CRISP-CT cohorts themselves did not measure hsCRP.

## Phase 4: Extending the Science (2019)

### Fat Radiomic Profile, Oikonomou et al. 2019, European Heart Journal | approximately 400 citations

FAI captures acute inflammation (the lipid-to-water shift in perivascular adipose tissue). But PVAT also undergoes chronic structural changes, fibrosis and microvascular remodeling, that are irreversible. Mean attenuation cannot detect these. Texture analysis can.

**Radiotranscriptomic approach (Study 1, n=167 surgery patients):**

Paired CT radiomic features with tissue gene expression for three biological processes:
1. Tumor Necrosis Factor Alpha (TNFA) gene expression → inflammation
2. Collagen Type I Alpha 1 Chain (COL1A1) gene expression → fibrosis
3. Cluster of Differentiation 31 / Platelet Endothelial Cell Adhesion Molecule (CD31/PECAM1) gene expression → vascularity

Result: Mean attenuation (essentially FAI) was the best CT predictor of TNFA. But higher-order texture features matched or exceeded it for COL1A1 and CD31. Adding radiomics significantly improved detection of fibrosis (P=0.005) and vascularity (P=0.015) but NOT inflammation (P=0.35). This directly proves that texture features capture biology invisible to FAI.

**Critical tissue source caveat:** The radiotranscriptomic tissue was subcutaneous chest wall fat from the surgical incision site (segmented on three consecutive axial slices at the xiphoid process level), NOT pericoronary adipose tissue. The linkage between gene expression and CT features was established in a tissue depot different from the one being imaged clinically.

**Machine learning pipeline:**

1. 843 radiomic features per vessel × 2 vessels (right coronary artery + left coronary artery) = 1,686 features per patient, computed using the PyRadiomics library in 3D Slicer (version 4.9.0)
2. Stability filtering (ICC ≥ 0.9): 1,391 features retained
3. Correlation filtering (|Spearman rho| ≥ 0.9): 335 independent features
4. Recursive feature elimination with random forest and repeated five-fold cross-validation: 64 optimal features
5. Case-control training: 101 major adverse cardiovascular events cases matched 1:1 with 101 controls (matched for age, sex, risk factors, scanner, location, and tube voltage)
6. External validation AUC: 0.774 (0.622 to 0.926). The external validation set contained approximately 40 patients with approximately 20 events (very small, explaining the wide confidence interval)

**Clinical validation (SCOT-HEART trial, n=1,575):**

* Fat Radiomic Profile ≥ 0.63: adjusted hazard ratio 10.84 (5.06 to 23.22) for MACE (defined as cardiac death + non-fatal acute myocardial infarction, excluding revascularization; this is a harder endpoint than many studies)
* FRP-positive with high-risk plaque features: hazard ratio 43.33 (9.14 to 205.48)
* FRP-positive without high-risk plaque features: hazard ratio 32.44 (7.00 to 150.38). This is the most clinically important finding: patients with no high-risk plaque features but high FRP are at extremely elevated risk that would be completely missed by conventional plaque analysis
* FRP did NOT predict non-cardiac mortality (hazard ratio 0.58, P=0.28), demonstrating cardiac specificity
* FRP was completely independent of high-risk plaque features (rho=0.004, P=0.87) and only weakly correlated with calcium score (rho=0.07, P=0.007)
* Adding FRP to the traditional model improved the time-dependent AUC from 0.754 to 0.880 (delta 0.126, P<0.001)

**Temporal dissociation between FAI and FRP:** In acute myocardial infarction patients with serial CT (n=16 total, n=10 ST-elevation myocardial infarction for culprit-lesion analysis), FAI was elevated acutely around culprit lesions and decreased at 6-month follow-up (dynamic). FRP was elevated at both timepoints (stable/irreversible). This implies FAI tracks active inflammation while FRP tracks cumulative structural damage.

**Practical limitation:** Analysis time is approximately 45 minutes per patient for full segmentation and radiomic profile extraction. The authors projected this could be reduced to under 5 minutes with GPU cloud processing. The left circumflex artery was also excluded from FRP analysis.

### Psoriasis as a Treatment-Response Model, Elnabawi and Antoniades 2019, JAMA Cardiology | approximately 197 citations

n=134 patients with moderate-to-severe psoriasis: 82 on biologics (anti-Tumor Necrosis Factor, anti-Interleukin-12/23, anti-Interleukin-17), 52 untreated controls. Coronary computed tomography angiography at baseline and 1 year. All scans on the same 320-detector-row scanner (Toshiba Aquilion ONE ViSION), eliminating inter-scanner variability. FAI measured using the CaRi-Heart algorithm from Caristo Diagnostics.

Why this population is well-suited: chronic systemic inflammation with elevated cardiovascular risk, low traditional cardiovascular risk factors (median Framingham Risk Score only 3%), built-in control group, measurable treatment response via Psoriasis Area and Severity Index, and specific cytokine-targeted therapies enabling mechanistic dissection.

FAI decreased from -71.22 to -76.09 Hounsfield Units in the treatment group (P<0.001); no change in controls (-71.98 to -72.66, P=0.39). Effect present with both anti-TNF (baseline -71.25 to 1-year -75.49, P<0.001) and anti-IL-12/23 or anti-IL-17 pathways (baseline -71.18 to 1-year -76.92, P<0.001). Topical therapy alone had no effect, arguing for a systemic anti-inflammatory mechanism. Propensity score matching (n=45 pairs) replicated the finding.

**Hidden details:**

* The FAI improvement was present in patients both WITH and WITHOUT coronary atherosclerotic plaque (46 of 134 had plaque at baseline). This suggests the anti-inflammatory effect acts on the perivascular microenvironment independent of plaque presence.
* High-sensitivity C-reactive protein decreased concordantly with FAI in the treatment group (2.2 to 1.3 mg/L, P=0.03) but not controls, providing systemic biomarker concordance with the imaging finding.
* This was the first study to use FAI as a treatment-response biomarker for tracking pharmacological effects on coronary inflammation.
* Limitation: non-randomized, open-label design. The control group "elected not to receive biologic therapy," introducing selection bias. No hard cardiovascular outcomes were studied.

### Wingless-Type 5A Pathway, Akoumianakis et al. 2019, Science Translational Medicine

Their largest tissue study (n=1,004 cardiac surgery patients). Profiled all 19 Wnt ligands across 3 adipose depots and identified Wingless-Type Family Member 5A as the most highly expressed in perivascular adipose tissue (notably, WNT11 was the most abundant in thoracic and subcutaneous depots, a potentially significant unexplored finding).

**Complete signaling pathway mapped:** WNT5A binds Frizzled-2 receptor → activates non-canonical Planar Cell Polarity pathway (confirmed by JNK phosphorylation) → upregulates Ubiquitin-Specific Peptidase 17 (the most differentially regulated gene by WNT5A treatment) → mediates Ras-related C3 Botulinum Toxin Substrate 1 activation → activates NADPH Oxidase 1 and 2 via RAC1 and p47phox membrane translocation → generates superoxide → additionally causes eNOS uncoupling via tetrahydrobiopterin oxidation.

The USP17 deubiquitinase link was entirely new to vascular biology. The FZD2 specificity was confirmed by knockdown experiments: FZD2 knockdown (approximately 96% reduction) completely prevented WNT5A-induced oxidative stress, while FZD5 knockdown (approximately 65% reduction) only modestly reduced basal superoxide.

**Dose-dependent pathway specificity:** Physiological WNT5A (100 ng/mL, within the measured plasma range of 1 to 112 ng/mL) activates the non-canonical Planar Cell Polarity pathway; only supraphysiological doses (400 ng/mL) activate canonical Wnt/β-catenin signaling. This resolves prior contradictions about WNT5A being pro-versus anti-atherogenic.

**The real biomarker is the WNT5A/SFRP5 ratio**, not WNT5A alone. Secreted Frizzled-Related Protein 5 acts as a decoy receptor for Wnt ligands. Obesity shifts this ratio (high WNT5A, low SFRP5). SFRP5 co-incubation (300 ng/mL) reversed WNT5A effects in every experiment (arterial superoxide, vascular smooth muscle cell migration, VSMC phenotypic switch). Obesity also upregulates FZD2 and FZD5 receptors in human arteries, creating a double hit: more ligand AND more receptor sensitivity.

**Hidden details of major interest:**

* WNT5A induced a vascular smooth muscle cell phenotypic switch: loss of contractile markers (ACTA2, TAGLN/SM22α) and increased matrix metalloproteinase 9 to tissue inhibitor of metalloproteinases ratio. This is directly relevant to plaque instability and fibrous cap thinning, connecting WNT5A to the plaque vulnerability question.
* Microarray analysis identified 1,890 differentially expressed genes in WNT5A-treated VSMCs (Gene Expression Omnibus accession GSE109859: 1,057 upregulated, 833 downregulated, 135 involved in cell motility). This transcriptomic dataset has likely been underexplored.
* WNT5A does NOT change NOX1, NOX2, NOX4, or NOX5 gene expression. It activates existing NADPH oxidase enzymes via RAC1-mediated post-translational mechanisms rather than transcriptional upregulation. This is a mechanistically clean finding.
* The doxycycline-inducible Wnt5a overexpression mouse lost up to 15% body weight after 3 days of doxycycline, making it unsuitable for long-term atherosclerosis studies. This is a significant in vivo limitation that prevented direct demonstration of WNT5A driving atherosclerosis progression.
* **Important negative result:** In multivariable modeling for coronary artery disease prediction, the WNT5A/SFRP5 ratio lost independent association when traditional risk factors were included (only hypertension and hyperlipidemia remained independent). This means WNT5A is a mechanistic pathway mediator, not a standalone clinical biomarker.
* Power calculations were included and exceeded throughout: 933 patients needed for Study 1, 1,004 enrolled; 70 per group needed for Study 2, 70 enrolled.

## Phase 5: Clinical Translation (2020 to 2023)

### FAI + High-Risk Plaque Interaction (2020, Journal of the American College of Cardiology)

Re-analysis of CRISP-CT data in a 2×2 stratification: FAI (high/low at -70.1 HU) × high-risk plaque features (present/absent). 74 cardiac deaths total.

The key finding: **High-risk plaque without elevated FAI carries no excess cardiac mortality risk** (hazard ratio 1.00, P=0.98). But high FAI without high-risk plaque carries substantial risk (hazard ratio 5.62 to 5.65, P<0.001; note: the paper has a minor internal inconsistency between text and figure legend). The highest risk is when both are present (hazard ratio 7.29 to 7.33, P<0.001).

This implies that high-risk plaque morphology without active inflammation may represent stable remodeling, while inflammation, even without visible plaque pathology, identifies patients at risk. This challenges the plaque-centric paradigm in CCTA interpretation.

**Hidden details:**

* Cleveland sub-cohort sensitivity analysis (n=2,040) for composite of cardiac mortality + non-fatal myocardial infarction (n=65 events) showed the same pattern: FAI-high/HRP-negative still had hazard ratio 5.58, while FAI-low/HRP-positive had hazard ratio 0.83 (P=0.64).
* After further adjustment for coronary artery calcium (n=1,415), FAI-high without high-risk plaque features still had hazard ratio 8.45 (P=0.01), reinforcing independence from calcification burden.
* Limitation: post-hoc analysis of the same dataset, with per-cell event counts not reported.

### FAI-Score Standardization (2021, Cardiovascular Research)

Raw FAI depends on scanner, tube voltage, contrast protocol, patient age and sex, and specific artery. FAI-Score transforms raw FAI through age- and sex-specific nomograms adjusted for technical parameters, outputting population-referenced percentiles.

**The CaRi-Heart device pipeline:**

1. Deep learning network segments epicardial adipose tissue and perivascular space
2. Three trained analysts at the Oxford Academic Cardiovascular CT Core Lab check and edit segmentations (not fully automated)
3. Raw FAI computed for proximal right coronary artery, left anterior descending, and left circumflex
4. FAI-Score calculated (adjusted for technical and demographic parameters)
5. CaRi-Heart Risk: 8-year cardiac mortality probability integrating FAI-Score + clinical risk factors + plaque burden

AUC 0.809 for 8-year cardiac mortality. Optimism-corrected AUC = 0.809 (95% confidence interval 0.805 to 0.814). Trained on the United States cohort (Cleveland, n=2,040), externally validated in the European cohort (Erlangen, n=1,872). Delta C-statistic of 0.085 (P=0.01) in the US cohort and 0.149 (P<0.001) in the European cohort. Negative predictive value 99.3% for CaRi-Heart Risk above 10%.

**Hidden details:**

* FAI-Score reclassified approximately 33% of patients (16% to higher risk, 17% to lower risk) compared to clinical risk factor models.
* FAI-Score shows a steep non-linear increase with age (visible in the nomogram curves), suggesting the inflammatory signal increases exponentially in older patients.
* No association between coronary calcium score and FAI-Score was found, confirming orthogonality with calcification.
* The relative risk at 95th percentile FAI-Score for the right coronary artery is 5.3×, higher than for left anterior descending (3.2×) or left circumflex (2.4×).
* The "0 to 100 scale" framing is an interpretation of the percentile approach; the 2021 paper itself presents percentile curves (10th, 25th, 50th, 75th, 90th) without explicitly naming it a 0 to 100 scale.

### Deep Learning Epicardial Adipose Tissue (2023, JACC Cardiovascular Imaging)

3D Residual U-Net trained on Oxford Risk Factors and Non-Invasive Imaging Study (ORFAN) CCTAs for automated epicardial adipose tissue segmentation. Positioned as complementary to FAI: epicardial adipose tissue volume predicts all-cause mortality including non-cardiac (a metabolic marker), while FAI predicts cardiac-specific events. Different risk dimensions from the same scan.

Also predicted atrial fibrillation, adding a second clinical application beyond coronary risk.

### European Society of Cardiology Consensus Statement (2023, European Heart Journal)

The ESC Working Group endorsed:

1. FAI-Score as the regulatory-cleared metric for coronary inflammation
2. The Oxford perivascular adipose tissue definition (radial distance = vessel diameter from outer wall)
3. CaRi-Heart version 2.5 by name
4. 75th, 90th, and 95th percentile cutoffs for risk stratification

Gaps identified by the consensus: (1) no randomized controlled trials of FAI-guided therapy, (2) per-lesion FAI not validated, (3) photon-counting CT needs recalibration, (4) non-coronary PVAT not validated, (5) no PVAT-specific drug delivery.

### miR-92a-3p (2023, Journal of the American College of Cardiology)

n=1,246 across 5 study arms (genome-wide association study for Mendelian randomization, animal models, cell culture, clinical outcomes with median 8-year follow-up via NHS Digital). Identified miR-92a-3p as an epicardial adipose tissue-derived microRNA that reduces myocardial NADPH oxidase by suppressing WNT5A/RAC1. This is arguably the most scientifically rigorous paper in the set.

**What makes it exceptional:**

* Uses genome-wide association study-based Mendelian randomization (unusual for a microRNA study). Single nucleotide polymorphisms associated with miR-92a-3p in epicardial adipose tissue affect EAT levels but NOT myocardial levels, and vice versa. This proves allele-specific and tissue-specific genetic regulation.
* miR-92a-3p's protective effect is cardiomyocyte-specific. It does NOT reduce NADPH oxidase-dependent superoxide in endothelial cells or cardiac fibroblasts. This selectivity is biologically surprising.
* Clinical outcomes: highest tertile of miR-92a-3p in epicardial adipose tissue showed hazard ratio 0.328 (95% confidence interval 0.11 to 0.98, P=0.046) for composite of cardiac mortality, myocardial infarction, and stroke.
* Also predicted postoperative atrial fibrillation (hazard ratio 0.56, 95% confidence interval 0.32 to 0.98, P=0.043).
* WNT5A/SFRP5 ratio in myocardium independently predicted outcomes (hazard ratio 3.941, P=0.003), providing bidirectional validation.
* Connects back to the 2019 WNT5A paper: miR-92a-3p suppresses WNT5A protein via 3'-UTR binding, linking the two pathways into one integrated axis.
* Limitation: mechanistic experiments used H9c2 rat cardiomyocyte-derived cells, not primary human cardiomyocytes.

## Phase 6: Population-Scale Validation (2024 to 2026)

### ORFAN Study, Chan et al. 2024, The Lancet | n=40,091

**Cohort A:** 40,091 consecutive patients from 8 National Health Service hospitals (2010 to 2021), median follow-up 2.7 years (interquartile range 1.4 to 5.3). **Cohort B:** 3,393 nested patients with 7.7-year follow-up (interquartile range 6.4 to 9.1) for AI-Risk validation. Events: 4,307 major adverse cardiovascular events, 1,754 cardiac deaths.

**Key results:**

| Measure | Hazard Ratio (95% Confidence Interval) |
|---------|---------------------------------------|
| Left anterior descending FAI-Score quartile 4 versus quartile 1, cardiac mortality | 20.20 (11.49 to 35.53) |
| 3 inflamed arteries versus 0, cardiac mortality | 29.8 (13.9 to 63.9) |
| AI-Risk very high versus low/medium, cardiac mortality | 6.75 (5.17 to 8.82) |

**Discrimination:** QRISK3 alone AUC=0.784 → plus CAD-RADS 2.0 stenosis grading: 0.789 (P=0.38, no improvement) → plus AI-Risk: 0.854 (P=7.7×10⁻⁷). Adding stenosis grading to traditional risk scores did not improve prediction. Adding inflammation assessment did.

**The central epidemiological finding:** 81.1% of patients had no obstructive coronary artery disease (32,533 of 40,091), yet this group accounted for 66.3% of all major adverse cardiovascular events (2,857 of 4,307) and 63.7% of cardiac deaths (1,118 of 1,754). Current practice sends these patients home reassured. FAI-Score identifies the high-risk subset within them.

**Strikingly, obstructive coronary artery disease itself has relatively modest hazard ratios:** 1.42 for cardiac mortality, 1.41 for MACE, 1.71 for myocardial infarction. The inflammation signal captured by FAI dwarfs the prognostic value of anatomical stenosis.

**Hidden details:**

* The dose-response of inflamed vessels is near-linear and striking: 1 inflamed vessel hazard ratio 13.0, 2 inflamed vessels hazard ratio 20.4, 3 inflamed vessels hazard ratio 29.8 for cardiac mortality. This additive pattern suggests independent inflammatory signals from each coronary territory.
* FAI-Score was prognostic even in patients with NO visible atheroma on CCTA (shown in supplementary appendix), meaning coronary inflammation is prognostic before any plaque appears.
* Post-hoc sensitivity analysis in 1,300 patients with non-contrast CT scans showed FAI-Score remained predictive after adjusting for coronary calcium score, confirming information orthogonal to calcification.
* AI-Risk was NOT retrained for the United Kingdom population due to regulatory restrictions on the locked model. This cross-continental validation (trained in US, validated in UK) is genuinely external.
* The population was 77.5% White, limiting generalizability to non-White populations.
* QRISK3 was developed from the same UK population (NHS Digital, same time period), giving it a strong baseline performance. The fact that AI-Risk improved upon it despite this home-field advantage is meaningful.
* Calibration: well-calibrated in non-obstructive coronary artery disease. Overestimates risk in obstructive CAD (because CCTA triggers interventions that reduce the risk the model predicts). Median follow-up of 2.7 years in Cohort A is short for an 8-year prediction model; the model extrapolates.

**Real-world NHS survey (n=744):** AI-Risk changed management in 45% (24% new statin initiation, 13% statin dose increase, 8% additional therapies).

### Cost-Effectiveness (2025, European Heart Journal: Quality of Care and Clinical Outcomes)

Hybrid decision-tree with population cohort Markov model, 3,393 patients, 3-month cycle length, 30-year lifetime horizon, 3.5% discount rate (standard NHS economic evaluation parameters).

AI-guided strategy: Incremental Cost-Effectiveness Ratio £1,371 to £3,244 per Quality-Adjusted Life Year (at device price points of £300 to £700). Predicted 11% myocardial infarction reduction, 12% cardiac death reduction, 22 fewer strokes (4% reduction), 68 fewer heart failure events (4% reduction). 100% of 1,000 probabilistic sensitivity analysis simulations fell below the NICE £20,000 per QALY threshold.

**Hidden details:**

* Even under pessimistic assumptions (50% reduction in statin effect, 50% reduction in risk reclassification accuracy, restriction to non-obstructive CAD only, full NICE guideline compliance as baseline), all Incremental Cost-Effectiveness Ratios remained below £6,592 per QALY.
* The colchicine scenario (adding colchicine to very-high-risk patients alongside statins) reduced the ICER to £1,837 per QALY, suggesting anti-inflammatory therapy adds clinical benefit within the economic model.
* A separate prospective comparison study of 1,214 consecutive patients found treatment initiation or intensification in 39% of patients beyond current NICE recommendations.
* **Key assumption:** Treatment effects of statins are modeled from the Cholesterol Treatment Trialists meta-analysis of 170,000 patients in 26 trials. Whether patients identified specifically by high FAI benefit equally from statins as those identified by other means is an extrapolation not yet tested in a randomized trial.
* This paper reads as a National Institute for Health and Care Excellence technology appraisal submission as much as a scientific paper.

### FAI-Score Robustness (2025, European Atherosclerosis Society conference abstract)

n=7,822 coronary computed tomography angiograms from one ORFAN site. FAI-Score stable within 0.5 units (on the percentile scale) across tube voltage, tube current, slice thickness, and scan phase, assessed using propensity-matched pairwise comparisons. This is a conference abstract, not a full peer-reviewed paper.

## The Patent

### US 10,695,023 B2 | Priority date August 15, 2014 | Filed August 14, 2015 | Granted June 30, 2020

**Filed by Oxford University Innovation Limited** (the university's technology transfer office), not by Caristo Diagnostics. Caristo holds an exclusive license.

**2 independent claims** (Claims 1 and 37), both requiring all of: computed tomography data → volumetric characterization using concentric layers from the outer vessel wall → radiodensity quantification per layer → comparison to baseline → administering a therapy based on results.

| Claim | Status | Method |
|-------|--------|--------|
| 1 | Independent | Concentric layer volumetric characterization + therapy administration |
| 14 | Dependent on Claim 1 | Adds VPCI-i: fold change plot → AUC calculation |
| 21 | Dependent on Claim 1 | Adds VPCI: PVAT minus non-PVAT radiodensity |
| 37 | Independent | Treatment guidance: CT → concentric layers → therapy administration |

**Key dependent claims:** 4 cm proximal right coronary artery segment starting 1 cm from ostium (Claim 4), specific arteries including non-coronary such as carotid and femoral (Claims 5 to 6), 1 mm thick concentric layers (Claim 7), various end-distance and baseline definitions (Claims 8 to 13).

**What the patent does NOT cover:**

1. Simple mean attenuation without concentric layer analysis (if you measure overall PVAT mean without the layer-by-layer spatial gradient approach, you are likely outside the claims)
2. Non-CT modalities (MRI, ultrasound, PET; the claims explicitly require "computed tomography")
3. Pure research or diagnostic use without the "administering a therapy" step (both independent claims terminate with therapy administration, which is a strategic weakness for enforcement against pure diagnostic applications)
4. Machine learning radiomic approaches (the Fat Radiomic Profile is not described in the patent)
5. FAI-Score nomogram or percentile calculation (a later development not in the patent)
6. Photon-counting CT material decomposition approaches (though note: "computed tomography" is broadly stated, so photon-counting CT using the concentric layer method could still fall within the claims)

The patent specification contains extensive biological data (Figures 13 to 20) showing the biological basis for why PVAT radiodensity changes with inflammation. This amount of biological validation is unusual for an imaging method patent.

**Related applications:** PCT/GB2017/053262, GB2018/1818049.7, GR20180100490, GR20180100510

## Caristo Diagnostics

| Product | Function | Status |
|---------|----------|--------|
| **CaRi-Heart** (FAI-Score + AI-Risk) | Coronary inflammation assessment from routine CCTA | CE Mark (Medical Device Regulation), UKCA, Australia. Investigational in United States |
| **CaRi-Plaque** | Automated plaque + stenosis quantification | CE Mark, UKCA, **FDA 510(k) cleared** (K242240, 2025) |
| **AI-Risk** | Integrated 8-year cardiac risk score | Part of CaRi-Heart platform |

Founders: Antoniades, Shirodaria, Channon, Neubauer (all senior academic cardiologists at Oxford). Multiple paper co-authors are also Caristo employees or consultants.

**Note on independence:** The entire evidence chain, from biomarker discovery to device development to clinical validation to consensus guidelines to health economics, has been produced by a group with direct financial interest in the product. Every paper discloses this. Independent validation by groups with no Caristo ties would substantially strengthen the evidence. This is not unusual for academic spinoffs (the inventors are best positioned to develop the technology), but it means the field needs external replication.

## Open Questions and Limitations

### Scientific

1. **Generalizability of the biology.** All mechanistic work comes from CABG patients: advanced coronary artery disease, approximately 83% male, mean age approximately 65, nearly all on statins. Does bidirectional PVAT-vascular signaling operate the same way in early subclinical disease? In women? In younger patients? In non-European populations (ORFAN was 77.5% White)?

2. **Adiponectin diffusion problem.** A 30 kDa+ multimeric protein is assumed to traverse the adventitia from PVAT to the vascular media/endothelium. This has never been directly demonstrated. The 2023 miR-92a-3p paper raises an alternative: the paracrine signal may be carried by microRNAs (much smaller) in exosomes rather than intact adiponectin protein.

3. **4-HNE specificity puzzle.** 4-Hydroxynonenal is the consistent inside-to-outside mediator across every Phase 1 paper. Malondialdehyde, another lipid peroxidation product, consistently has no effect. Hydrogen peroxide actually SUPPRESSES adiponectin. Yet no receptor or specific uptake mechanism for 4-HNE in adipocytes has been identified. How the tissue distinguishes between these reactive species remains unexplained.

4. **Tissue-specific signaling kinase switch.** In arteries, adiponectin works through PI3K/Akt (2013, 2015). In myocardium, it works through AMPK (2016). Both converge on RAC1/p47phox. The therapeutic implications of this difference (whether tissue-specific targeting is needed) have not been explored.

5. **FAI specificity for inflammation.** The biological model is: inflammation → cytokine-mediated inhibition of preadipocyte differentiation → less lipid accumulation → higher CT attenuation. But FAI does not correlate with macrophage markers (CD68) in epicardial fat. Other processes also alter adipocyte biology (fibrosis, edema, hemorrhage, metabolic stress). FAI may capture a composite signal, not purely inflammation.

6. **The left circumflex problem.** The left circumflex artery is excluded from most FAI analyses AND from the Fat Radiomic Profile due to variable anatomy and small caliber. LCx FAI was NOT predictive of cardiac mortality in CRISP-CT. Yet left circumflex disease causes real clinical events. Any PVAT imaging approach limited to the right coronary artery and left anterior descending misses a major coronary territory.

7. **PVAT browning/beige fat.** Perivascular adipose tissue can undergo brown-to-white conversion in disease states. Uncoupling Protein 1, β3-adrenergic receptors, and thermogenic capacity represent a parallel biology that the Oxford group has not deeply explored. Brown versus white fat has distinct imaging characteristics on both CT and MRI.

8. **WNT11 in remote depots.** The 2019 WNT5A paper showed WNT11 was the most abundant Wnt ligand in thoracic and subcutaneous adipose tissue. This non-canonical Wnt pathway activator has not been investigated further despite its prominence.

### Translational

9. **No randomized controlled trial evidence.** The ESC consensus identifies this as Gap #1. All evidence is observational. The 45% management change in ORFAN is uncontrolled. Whether FAI-guided decisions actually improve outcomes is unknown.

10. **Proprietary algorithm.** The FAI-to-FAI-Score transformation and the AI-Risk classifier are unpublished. Independent groups cannot reproduce or verify the computations. This is standard for commercial medical devices but limits scientific scrutiny.

11. **Standardization treadmill.** Each new scanner generation (especially photon-counting CT), contrast protocol variation, and reconstruction algorithm potentially requires recalibration. The 2025 robustness data is from one site and is a conference abstract, not peer-reviewed.

12. **Short follow-up in the largest study.** ORFAN Cohort A median follow-up is 2.7 years for an 8-year prediction model. Substantial extrapolation is required. Cohort B (7.7 years) is more appropriate but contains only 3,393 patients.

13. **Low positive predictive value.** At the -70.1 HU cutoff, positive predictive value is only 5.9%. FAI is far better at ruling out risk (negative predictive value 99.5%) than ruling it in. Clinical deployment must account for how to counsel the many false positives.

## Knowledge Gaps to Fill

To work at the level of this program, the following domains need to be understood in depth, not as a checklist but as interconnected knowledge:

**Vascular biology:** Endothelial nitric oxide synthase coupling and uncoupling (tetrahydrobiopterin cofactor chemistry), NADPH oxidase isoforms and assembly (NOX1/2/4/5, RAC1 and p47phox translocation), adipokine signaling (adiponectin receptors AdipoR1/AdipoR2/CDH13/T-cadherin, WNT5A/FZD2 non-canonical pathway, SFRP5 antagonism, PPARγ regulation), and redox signaling (4-HNE as the specific diffusible mediator, distinct from MDA and H2O2). The tissue-specific kinase switch (PI3K/Akt in arteries, AMPK in myocardium) and cell-type specificity (miR-92a-3p affecting cardiomyocytes but not endothelial cells or fibroblasts) add important layers.

**CT physics of fat imaging:** Why the -190 to -30 Hounsfield Unit window works (lipid phase approximately -190 HU, aqueous phase approximately -30 HU, fat tissue sits on this spectrum based on adipocyte lipid content). How tube voltage shifts the attenuation curve. How reconstruction kernels affect texture features. How contrast timing affects pericoronary measurements. How partial volume effects at the vessel-fat interface create artifacts. Why the left circumflex is unreliable (small caliber, variable anatomy).

**Radiomics methodology:** Feature types (first-order statistics versus Gray Level Co-occurrence Matrix / Gray Level Run Length Matrix / Gray Level Size Zone Matrix texture matrices versus wavelet transforms), stability analysis (intraclass correlation coefficient filtering), dimensionality reduction strategies, appropriate sample sizes for feature-to-event ratios (the Fat Radiomic Profile trained 335 features on 101 events), and the critical distinction between radiomic features that correlate with biology versus features that are measurement artifacts. The radiotranscriptomic approach (linking CT features to tissue gene expression) is the group's methodological innovation.

**Survival statistics:** Cox proportional hazards, time-dependent C-statistics, Net Reclassification Improvement / Integrated Discrimination Improvement for censored data, decision curve analysis (net clinical benefit), fractional polynomials for non-linear relationships, and competing risks modeling. Understanding where statistical choices affect conclusions is essential (the -70.1 HU cutoff was data-derived from Youden's J statistic, not pre-specified).

**Mendelian randomization:** The Oxford group uses ADIPOQ single nucleotide polymorphisms and genome-wide association study data as genetic instruments for causal inference. Understanding instrumental variable assumptions (relevance, independence, exclusion restriction), two-sample Mendelian randomization design, and pleiotropy tests is necessary to evaluate their causal claims. Their use of GWAS-based Mendelian randomization for miR-92a-3p (the 2023 paper) is a methodological advance.

**Regulatory and health economics:** CE marking (Medical Device Regulation) and FDA 510(k) / De Novo pathways for Software as a Medical Device. Markov decision-analytic models, Incremental Cost-Effectiveness Ratio / Quality-Adjusted Life Year calculations, National Institute for Health and Care Excellence technology appraisal requirements. These are the mechanics of clinical translation from discovery to reimbursement.

**Where opportunities lie:**

1. **MRI-based PVAT characterization.** The patent is CT-specific. MRI offers fat/water fraction, T1/T2 mapping, and diffusion-weighted imaging, potentially richer tissue characterization without ionizing radiation. No group has demonstrated PVAT inflammation detection by MRI.
2. **Non-coronary PVAT.** Carotid (stroke), aortic (aneurysm), femoral (peripheral artery disease): all clinically important, all acknowledged as unvalidated in the ESC consensus.
3. **Open-source reproducibility.** A transparent, publicly validated PVAT analysis pipeline would be scientifically complementary to the proprietary approach and would attract collaborators.
4. **Photon-counting CT / dual-energy CT.** Material decomposition enables direct fat/water/calcium separation, a fundamentally different measurement physics from conventional single-energy attenuation. Not covered by the patent unless using the concentric layer method.
5. **Diverse populations.** Women, non-White cohorts, younger patients with early disease. The ORFAN population was 77.5% White and the biology was established in approximately 83% male surgical cohorts.
6. **Prospective interventional evidence.** Even a small randomized controlled trial of PVAT-guided therapy would address the field's most significant evidence gap (ESC Gap #1).
7. **4-HNE receptor/mechanism.** Identifying how 4-HNE specifically signals to adipocytes (when MDA and H2O2 do not) would be a fundamental biological contribution.
8. **WNT11 biology in remote depots.** The most abundant Wnt ligand in thoracic and subcutaneous fat is unexplored.
9. **The VSMC phenotypic switch angle.** WNT5A drives contractile-to-synthetic VSMC conversion and increases matrix metalloproteinase 9. Connecting this to plaque vulnerability imaging (beyond the current FAI focus on adipocyte biology) could open a new dimension.

## Paper Catalogue

### Phase 1: Biology (2013 to 2016)

| # | Year | Title | Journal (Impact Factor) | Citations | Key Contribution |
|---|------|-------|------------------------|-----------|-----------------|
| 1 | 2013 | Adiponectin/eNOS in Human Vessels | *Circulation* (35.5) | approximately 321 | Bidirectional PVAT-vascular signaling; dual adiponectin mechanism. n=677+46. |
| 2 | 2014 | Systemic Inflammation and BNP on Adiponectin | *Arteriosclerosis Thrombosis and Vascular Biology* (8.4) | not available | BNP upregulates adiponectin; depot-specific inflammation responsiveness; S. typhi vaccination model. n=575+13+19. |
| 3 | 2015 | Adiponectin Links Type 2 Diabetes to NADPH Oxidase | *Diabetes* (7.7) | approximately 241 | NADPH oxidase-specific; Mendelian randomization; adiponectin receptor preservation in diabetes. n=386+67. |
| 4 | 2016 | Epicardial Adipose Tissue-Myocardial Redox via PPARγ/Adiponectin | *Circulation Research* (20.1) | approximately 158 | Inside-to-outside signaling in cardiac compartment; AMPK (not PI3K/Akt) in myocardium; three species validation. n=247+59. |

### Phase 2: Reviews (2017)

| # | Year | Title | Journal (Impact Factor) | Citations |
|---|------|-------|------------------------|-----------|
| 5 | 2017 | Epicardial Adipose Tissue in cardiac biology | *Journal of Physiology* (5.5) | approximately 162 |
| 6 | 2017 | Is fat always bad? | *Cardiovascular Research* (10.2) | approximately 148 |
| 7 | 2017 | Dysfunctional adipose tissue | *British Journal of Pharmacology* (7.3) | not available |
| 8 | 2017 | PVAT as vascular disease regulator | *British Journal of Pharmacology* (7.3) | approximately 73 |
| 9 | 2017 | Adiponectin paradox | *British Journal of Pharmacology* (7.3) | approximately 134 |

### Phase 3: Fat Attenuation Index and CRISP-CT (2017 to 2018)

| # | Year | Title | Journal (Impact Factor) | Citations | Key Contribution |
|---|------|-------|------------------------|-----------|-----------------|
| **10** | **2017** | **Detecting coronary inflammation by imaging perivascular fat** | ***Science Translational Medicine*** **(17.1)** | **approximately 872** | **FAI invention.** 4 study arms, n=453+45+273+22. |
| **11** | **2018** | **CRISP-CT** | ***The Lancet*** **(168.9)** | **approximately 838** | **Prognostic validation.** n=3,912. Hazard ratio 9.04 cardiac mortality. PPV 5.9%, NPV 99.5%. |
| 12 | 2018 | Adipose tissue in cardiovascular health and disease | *Nature Reviews Cardiology* (41.7) | approximately 396 | Definitive review positioning FAI. |
| 13 | 2018 | Perivascular adipose tissue and coronary atherosclerosis | *Heart* (5.0) | approximately 113 | Bridge paper: biology to imaging. PVAT definition. |

### Phase 4: Extension (2019)

| # | Year | Title | Journal (Impact Factor) | Citations | Key Contribution |
|---|------|-------|------------------------|-----------|-----------------|
| **14** | **2019** | **Radiotranscriptomic Fat Radiomic Profile** | ***European Heart Journal*** **(39.3)** | **approximately 400** | **Radiomic texture captures fibrosis + vascularity beyond FAI.** n=167+202+1,575. |
| 15 | 2019 | Biologic therapy and coronary inflammation in psoriasis | *JAMA Cardiology* (14.8) | approximately 197 | FAI as treatment-response biomarker. n=134. |
| 16 | 2019 | Imaging residual inflammatory cardiovascular risk | *European Heart Journal* (39.3) | approximately 145 | Clinical positioning review with Deanfield. |
| 17 | 2019 | Atherosclerosis affecting fat | *Journal of Cardiovascular Computed Tomography* (3.3) | approximately 102 | FAI methodology review. |
| 18 | 2019 | CT Assessment of Coronary Inflammation | *Arteriosclerosis Thrombosis and Vascular Biology* (8.4) | approximately 35 | Technical review. |
| 19 | 2019 | Making Sense From Perivascular Attenuation Maps | *JACC Cardiovascular Imaging* (12.8) | approximately 33 | Editorial and interpretation guide. |
| 20 | 2019 | WNT5A/USP17/RAC1 pathway | *Science Translational Medicine* (17.1) | not available | Second druggable axis; VSMC phenotypic switch; 1,890 differentially expressed genes. n=1,004. |

### Phase 5: Translation (2020 to 2023)

| # | Year | Title | Journal (Impact Factor) | Citations | Key Contribution |
|---|------|-------|------------------------|-----------|-----------------|
| 21 | 2020 | FAI + High-Risk Plaque Stratification | *Journal of the American College of Cardiology* (21.7) | approximately 87 | High-risk plaque without inflammation = no excess risk. n=3,912. |
| 22 | 2020 | AI Radiomic Guide | *Cardiovascular Research* (10.2) | approximately 77 | 16-point radiomic quality framework. |
| 23 | 2021 | FAI in Coronary CTA | *Radiology: Cardiothoracic Imaging* (4.5) | approximately 62 | Practical FAI measurement guide. |
| 24 | 2021 | Standardized FAI measurement | *Cardiovascular Research* (10.2) | approximately 33 | FAI-Score and CaRi-Heart specification. AUC 0.809. Reclassifies 33% of patients. |
| 25 | 2021 | PVAT imaging by CT: virtual guide | *British Journal of Pharmacology* (7.3) | approximately 38 | Measurement protocols and pitfalls. |
| 26 | 2022 | FAI Meta-Analysis | *European Heart Journal: Cardiovascular Imaging* (6.2) | not available | 20 studies, 7,797 patients. MACE hazard ratio 3.29. |
| 27 | 2022 | Pericardial Adiposity by Cardiac MRI | *European Heart Journal: Cardiovascular Imaging* (6.2) | approximately 22 | UK Biobank n=42,598. EAT volume → adverse remodeling, atrial fibrillation. |
| 28 | 2023 | Deep Learning Epicardial Adipose Tissue | *JACC Cardiovascular Imaging* (12.8) | approximately 77 | 3D Residual U-Net. Predicts mortality + atrial fibrillation. |
| 29 | 2023 | Epicardial Adipose Tissue-derived miR-92a-3p | *Journal of the American College of Cardiology* (21.7) | approximately 19 | miR-92a-3p suppresses WNT5A/RAC1 in myocardium. GWAS Mendelian randomization. n=1,246. |
| 30 | 2023 | ESC Consensus Statement | *European Heart Journal* (39.3) | not available | European Society of Cardiology endorses FAI-Score, CaRi-Heart, PVAT definition. |

### Phase 6: Validation (2024 to 2026)

| # | Year | Title | Journal (Impact Factor) | Citations | Key Contribution |
|---|------|-------|------------------------|-----------|-----------------|
| **31** | **2024** | **ORFAN Study** | ***The Lancet*** **(168.9)** | not available | **n=40,091.** Hazard ratio 20.20 cardiac mortality Q4 vs Q1. 81.1% non-obstructive CAD. |
| 32 | 2024 | AI in atherosclerosis CT | *Atherosclerosis* (5.3) | not available | Landscape review. |
| 33 | 2025 | FAI-Score robustness | Conference abstract | not available | Cross-scanner stability within 0.5 units. n=7,822. |
| 34 | 2025 | FAI-Score standardization editorial | *JACC Cardiovascular Imaging* (12.8) | not available | Case for standardized measurement. |
| 35 | 2025 | Cost-effectiveness of AI | *European Heart Journal: Quality of Care and Clinical Outcomes* (4.6) | not available | ICER £1,371 to £3,244 per QALY. 100% below NICE threshold. |
| 36 | 2026 | PVAT Imaging and Quantification | *Arteriosclerosis Thrombosis and Vascular Biology* (8.4) | not available | Latest methodological review. |

**Summary:** 36 papers | 19 original research | 12 reviews | 5 other (consensus, meta-analysis, editorial, health economics) | 1 US patent | 3 commercial products | approximately 50,000 patients validated | 8 publications in journals with impact factor above 15

*Last updated: March 13, 2026*
