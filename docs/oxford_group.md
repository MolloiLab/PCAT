# Oxford Group: Pericoronary Adipose Tissue Research Program

> **Principal Investigator: Prof. Charalambos Antoniades, MD PhD FRCP FESC**
> British Heart Foundation Chair of Cardiovascular Medicine, University of Oxford
> Founder and Director, Caristo Diagnostics Ltd.

<details>
<summary><strong>Abbreviation Glossary</strong> (click to expand)</summary>

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
| CAD | Coronary Artery Disease |
| ACS | Acute Coronary Syndrome |
| AMI | Acute Myocardial Infarction |
| MACE | Major Adverse Cardiovascular Events |
| HRP | High-Risk Plaque |
| HR | Hazard Ratio |
| AUC | Area Under the Curve |
| NRI | Net Reclassification Improvement |
| IDI | Integrated Discrimination Improvement |
| ICC | Intraclass Correlation Coefficient |
| ICER | Incremental Cost-Effectiveness Ratio |
| QALY | Quality-Adjusted Life Year |
| VPCI | Volumetric Perivascular Characterization Index |
| OXACCT | Oxford Academic Cardiovascular CT Core Lab |
| NICE | National Institute for Health and Care Excellence |
| NHS | National Health Service |
| ESC | European Society of Cardiology |
| RCT | Randomized Controlled Trial |
| SaMD | Software as a Medical Device |
| MDR | Medical Device Regulation (European) |
| CE | Conformité Européenne |
| FDA | Food and Drug Administration (United States) |
| GLCM | Gray Level Co-occurrence Matrix |
| GLRLM | Gray Level Run Length Matrix |
| GLSZM | Gray Level Size Zone Matrix |
| NGTDM | Neighbouring Gray-Tone Difference Matrix |
| PASI | Psoriasis Area and Severity Index |
| VSMC | Vascular Smooth Muscle Cell |
| QRISK3 | UK cardiovascular risk prediction algorithm (version 3) |
| CAD-RADS | Coronary Artery Disease Reporting and Data System |
| ORFAN | Oxford Risk Factors and Non-Invasive Imaging Study |

</details>

## Table of Contents

* [Research Architecture](#research-architecture)
* [Biological Foundation (Summary)](#biological-foundation-summary)
* [CT Imaging Methodology](#ct-imaging-methodology)
* [Fat Attenuation Index: Discovery and Prognostic Validation](#fat-attenuation-index-discovery-and-prognostic-validation)
* [Fat Radiomic Profile: Beyond Mean Attenuation](#fat-radiomic-profile-beyond-mean-attenuation)
* [FAI as a Treatment-Response Biomarker](#fai-as-a-treatment-response-biomarker)
* [Standardization: From Raw FAI to FAI-Score](#standardization-from-raw-fai-to-fai-score)
* [Population-Scale Validation: ORFAN](#population-scale-validation-orfan)
* [Health Economics and Real-World Impact](#health-economics-and-real-world-impact)
* [The Patent](#the-patent)
* [Caristo Diagnostics](#caristo-diagnostics)
* [What Is NOT Published: Reproducibility Gaps](#what-is-not-published-reproducibility-gaps)
* [Open Questions and Limitations](#open-questions-and-limitations)
* [Opportunities for Competing Work](#opportunities-for-competing-work)
* [Paper Catalogue](#paper-catalogue)

## Research Architecture

The Oxford program spans 13 years and follows a coherent logic: establish the biology in human tissue (2013 to 2016), translate it to a computed tomography imaging readout (2017), validate that readout prognostically in large cohorts (2018 to 2024), standardize it for clinical use (2021 to 2025), and build the regulatory and economic evidence for adoption (2023 to 2025).

What makes it work is tight coupling between bench science and clinical imaging. Each imaging claim traces back to a specific molecular mechanism demonstrated in human tissue. Most imaging biomarkers are discovered empirically (statistical association with outcomes) and only later investigated mechanistically, if at all. The Oxford group worked the other direction: they understood why perivascular adipose tissue (PVAT) changes before they ever measured it on a CT scan.

```
2013-2016  Biology: bidirectional PVAT-vascular signaling established in human tissue
  ↓
2017       FAI invented: CT captures inflammation-induced PVAT changes (n=453+45+273+22)
  ↓
2018       CRISP-CT: FAI predicts cardiac mortality in 3,912 patients
  ↓
2019       FRP: radiomic texture captures fibrosis + vascularity beyond FAI
2019       FAI validated as treatment-response biomarker (psoriasis, n=134)
  ↓
2020       FAI + high-risk plaque interaction: inflammation contextualizes plaque risk
  ↓
2021       FAI-Score: scanner-adjusted, age/sex-normalized metric. CaRi-Heart device.
  ↓
2023       ESC endorses FAI-Score. Deep learning EAT segmentation. miR-92a-3p mechanism.
  ↓
2024       ORFAN: 40,091-patient NHS validation
  ↓
2025       Cost-effectiveness: ICER £1,371 to £3,244 per QALY. FAI-Score robustness data.
```

## Biological Foundation (Summary)

The imaging methodology rests on a biological model established across four papers (2013 to 2016) using tissue from over 1,900 coronary artery bypass grafting patients at Oxford. The core concept: vascular inflammation releases cytokines (Tumor Necrosis Factor Alpha, Interleukin-6, Interferon Gamma) that inhibit preadipocyte differentiation in surrounding perivascular adipose tissue, reducing lipid accumulation and shifting the tissue's CT attenuation toward less negative values. Simultaneously, the vessel signals back to the fat through 4-Hydroxynonenal (a lipid peroxidation product), which upregulates adiponectin production in PVAT via Peroxisome Proliferator-Activated Receptor Gamma. This bidirectional cross-talk means PVAT composition reflects the inflammatory state of the underlying vessel, and this is what CT detects.

A second druggable pathway was mapped in 2019 (n=1,004): Wingless-Type Family Member 5A from PVAT activates NADPH oxidase in vascular smooth muscle cells through a Frizzled-2/Ubiquitin-Specific Peptidase 17/RAC1 pathway. In 2023, miR-92a-3p was identified as an epicardial adipose tissue-derived microRNA that suppresses WNT5A in myocardium.

The biology matters for imaging interpretation because it constrains what the CT signal means: FAI tracks adipocyte differentiation state (an indirect consequence of inflammation), not macrophages directly. FAI does not correlate with CD68 macrophage markers in epicardial fat (rho=0.180, P=0.096).

## CT Imaging Methodology

### The Attenuation Window: -190 to -30 Hounsfield Units

The fundamental principle: adipose tissue attenuation falls between -190 and -30 HU, based on the lipid-to-water ratio within the tissue (Brooks 1977, "A quantitative theory of the Hounsfield unit"). Larger adipocytes with more intracellular lipid produce attenuation closer to -190 HU. Smaller, lipid-depleted adipocytes (as in inflamed tissue) produce attenuation closer to -30 HU. The Fat Attenuation Index is the mean attenuation of all voxels within this window in the defined perivascular region.

This window implicitly excludes contrast-enhanced lumen (typically above 200 HU) and dense calcified plaque (above 130 HU). However, partial volume voxels at the vessel-fat interface that fall within the -190 to -30 range due to averaging of fat and non-fat tissues are NOT explicitly excluded. No sensitivity analysis on alternative window bounds has been published.

### Perivascular Region Definition

PVAT is defined as adipose tissue within a **radial distance from the outer coronary artery wall equal to the diameter of the vessel**. This creates a concentric cylindrical shell around each artery:

1. **Right Coronary Artery (RCA):** 10 to 50 mm from the ostium. The proximal 10 mm is excluded to avoid aortic wall artifacts.
2. **Left Anterior Descending (LAD):** Proximal 40 mm.
3. **Left Circumflex (LCx):** Proximal 40 mm. However, LCx is excluded from most prognostic analyses due to variable anatomy and small caliber. LCx FAI was NOT significantly predictive of cardiac mortality in CRISP-CT (derivation hazard ratio 1.32, P=0.24; validation hazard ratio 1.29, P=0.13).
4. **Left main artery:** Excluded due to variable length.

### Concentric Layer Analysis

The perivascular space is segmented into **20 concentric cylindrical layers, each 1 mm thick**, extending outward from the outer vessel wall up to 20 mm. FAI is calculated independently for each layer. In both diseased and healthy arteries, FAI shifts progressively to more negative values (larger, more lipid-laden adipocytes) moving away from the vessel wall. The spatial gradient of this shift is the core measurement.

### Volumetric Perivascular Characterization Index (VPCI)

A gradient-based metric that self-normalizes against systemic metabolic factors:

**VPCI = [100 × (FAI_PVAT minus FAI_non-PVAT) / |FAI_PVAT|]**

Where FAI_non-PVAT is the attenuation of the most distal 1 mm concentric layer (20 mm from the vessel wall). Each patient's remote fat serves as their own reference, controlling for body composition and metabolic state.

A related metric, **VPCI-i**, integrates the fold-change plot across all layers (area under the spatial gradient curve). Both are described in the patent.

VPCI was superior to raw FAI for detecting soft (noncalcified) plaques, though both had only "moderate diagnostic value" for vulnerable plaques by existing definitions.

### What "Weighted" FAI Means (and What We Don't Know)

Multiple papers describe the CaRi-Heart implementation of FAI as "weighted three-dimensional attenuation gradients" enhanced by "machine learning-enhanced modelling," distinct from simple mean attenuation. The 2021 virtual guide paper states FAI is "corrected and weighted for technical CT scan characteristics, local coronary anatomy, background adipocyte size," and "interpreted using machine learning-enhanced modelling."

**The exact weighting scheme is never specified.** Whether this means distance-weighted, volume-weighted, or ML-predicted is unclear. The adjustment model form (linear, nonlinear, regression coefficients) is proprietary to Caristo Diagnostics. This means that the "FAI" computed by CaRi-Heart is not a simple mean of the -190 to -30 HU voxels; it incorporates undisclosed corrections.

### Scanner and Technical Parameter Effects

**Scanners tested across the program:**

| Study | Scanners | Vendors |
|-------|----------|---------|
| CRISP-CT (n=3,912) | 2×64 Definition Flash, 1×64 Sensation 64, 2×128 Definition Flash, 1×256 Brilliance iCT, 2×192 Somatom Force | Siemens, Philips |
| Psoriasis (n=134) | 320-detector Aquilion ONE ViSION | Canon/Toshiba |
| FAI-Score robustness (n=7,822) | Single UK site, scanners not specified | Not specified |

**Technical parameters accounted for:**
* Tube voltage: 100 and 120 kVp tested in CRISP-CT. FAI-Score stable within 0.5 units across tube voltages (2025 abstract).
* Tube current and slice thickness: tested in 2025 abstract, stable within 0.5 units.
* Cardiac phase (systolic vs diastolic): tested in 2025 abstract, stable.
* Technical parameters collectively account for approximately 5% of FAI variation (R-squared approximately 0.05, P<0.0001 in a multivariable model from CRISP-CT).

**NOT tested anywhere in the published literature:**
* Reconstruction kernel effects (a significant gap since kernel choice substantially affects CT attenuation)
* Contrast bolus timing effects (injection rate, iodine concentration, scan timing relative to contrast peak)
* GE scanners (never tested in any paper)
* Canon/Toshiba scanners (tested only in the single-scanner psoriasis study, not for cross-scanner comparison)
* Multi-site, multi-vendor systematic comparison

### Partial Volume and Artifact Handling

The -190 to -30 HU window implicitly excludes contrast-enhanced lumen and dense calcification, but:

* No explicit erosion step or buffer zone between the vessel wall and the first included PVAT voxel is described
* No protocol for handling calcified plaques that abut or intrude into the perivascular space
* No description of whether the outer vessel wall boundary is adjusted when plaque is present
* Motion artifacts are handled by standard cardiac CT gating plus quality control review by two or more investigators; 6 to 9% of scans were excluded for "technical considerations" in CRISP-CT (criteria not published)
* Spatial resolution limited by coronary artery motion (theoretical voxel size 0.35 mm squared on a 128-slice scanner, but not achievable in practice)

### Reproducibility

| Study | Intra-observer ICC | Inter-observer ICC |
|-------|-------------------|--------------------|
| CRISP-CT (2018) | 0.987 (P<0.001) | 0.980 (P<0.001) |
| CaRi-Heart FAI-Score RCA (2021) | not reported | 0.980 (P<0.001) |
| CaRi-Heart FAI-Score LAD (2021) | not reported | 0.990 (P<0.001) |
| CaRi-Heart FAI-Score LCx (2021) | not reported | 0.992 (P<0.001) |
| FRP (2019) | 0.995 (P<0.001) | 0.938 (P<0.001), n=15 scans, 3 operators |
| Psoriasis (2019) | 0.987 (P<0.001) | 0.980 (P<0.001) |

Note: FRP inter-observer analysis was based on only 15 scans.

### Analysis Platform

* Manual analysis (CRISP-CT, 2018): Aquarius Workstation version 4.4.11-13 (TeraRecon), blinded at the Oxford Academic Cardiovascular CT Core Lab (OXACCT)
* CaRi-Heart (2021 onward): cloud-based, proprietary. CT data sent from hospital PACS via gateway appliance. Reports returned electronically. Three trained OXACCT analysts performed quality control for the validation studies.
* No open-source implementation or algorithm pseudocode exists

## Fat Attenuation Index: Discovery and Prognostic Validation

### Discovery: Antonopoulos et al. 2017, Science Translational Medicine | approximately 872 citations

**Four-arm study design:**

| Arm | n | Purpose | Key Finding |
|-----|---|---------|-------------|
| 1 | 453 CABG | Histological validation | FAI correlates with adipocyte size, differentiation markers, macrophage infiltration |
| 2 | 45 CABG | Coculture proof | Inflamed aortic tissue inhibits preadipocyte lipid accumulation in coculture |
| 3 | 273 CCTA | Clinical validation | FAI higher around culprit lesions in acute coronary syndrome; predicts coronary artery disease independently of calcium score |
| 4 | 22 ACS | Culprit lesion detection | FAI increased by 8.76 ± 2.87 HU around culprit vs proximal segments; AUC 0.91 (0.80 to 1.00) |

**Positron emission tomography validation (n=39 to 40):** 18F-fluorodeoxyglucose uptake in subcutaneous adipose tissue correlated with FAI (Spearman rho=0.69, AUC=0.971 at target-to-background ratio cutoff of 0.200; AUC drops to 0.894 and 0.791 at other cutoffs). Validated in subcutaneous fat only, NOT epicardial fat. The group explains this is by design: epicardial FAI reflects local coronary signals, making systemic PET comparison inappropriate.

**Important negative result:** Insulin resistance (HOMA-IR) associated with subcutaneous FAI but NOT epicardial FAI. This supports the claim that pericoronary fat changes are locally driven by coronary inflammation, not systemic metabolic disease. FAI is not a marker of obesity (independent of BMI and waist-to-hip ratio).

**Dynamic behavior:** FAI around culprit lesions decreased at 5 weeks after stenting in n=5 myocardial infarction patients (P=0.04); n=5 stable coronary artery disease controls showed no change. Approximately 23.5% of acute coronary syndrome patients fail to reduce their perivascular FAI. The dynamic claim rests on very small numbers.

**The paper explicitly acknowledges its main limitation:** "the lack of data demonstrating predictive value for clinical outcomes." CRISP-CT was designed to address this.

### Prognostic Validation: Oikonomou et al. 2018, The Lancet (CRISP-CT) | n=3,912 | approximately 838 citations

**Study design:** Post-hoc analysis of two prospective cohorts: Erlangen, Germany (n=1,872, enrolled 2005 to 2009, median follow-up 72 months) and Cleveland Clinic, United States (n=2,040, enrolled 2008 to 2016, median follow-up 54 months). All images analyzed blindly at OXACCT.

**Key prognostic results:**

| Metric | Derivation (Erlangen) | Validation (Cleveland) |
|--------|----------------------|----------------------|
| Per-standard-deviation FAI (RCA), HR cardiac mortality | 2.15 (1.33 to 3.48) | 2.06 (1.50 to 2.83) |
| FAI ≥ -70.1 HU, HR cardiac mortality | 9.04 (3.35 to 24.40) | 5.62 (2.90 to 10.88) |
| C-statistic improvement | 0.913 to 0.962 (delta 0.049, P=0.0054) | 0.763 to 0.838 (delta 0.075, P=0.0069) |
| Net Reclassification Improvement for cardiac mortality | 0.94 (0.07 to 1.34) | 0.72 (0.34 to 1.07) |

**The -70.1 HU cutoff** was derived from this data using Youden's J statistic (maximizing sum of sensitivity and specificity) on time-dependent receiver operating characteristic analysis at the median follow-up of 72 months. Not pre-specified. Specificity 85.0%, sensitivity 67.7%, **positive predictive value only 5.9%**, negative predictive value 99.5%. FAI is far better at ruling out risk than ruling it in.

**J-shaped relationship:** Fractional polynomial modeling showed non-linear FAI to mortality association. Extremely negative FAI (very fatty PVAT) may also be pathological, potentially reflecting lipomatous metaplasia. This motivated dichotomization rather than linear treatment.

**Mean FAI values:** -75.1 HU (standard deviation 8.6) in derivation, -77.0 HU (standard deviation 8.5) in validation. The -70.1 cutoff is approximately 0.6 standard deviations above the mean; about 28 to 29% of the population falls above it.

**Event counts:** Only 26 cardiac deaths in the derivation cohort (1.4%), 48 in validation. Large hazard ratios from few events. The event-to-variable ratio in the multivariable Cox model is low.

**Medication differences between cohorts:** Statins 35% (Erlangen) vs 40% (Cleveland); ACE inhibitors/angiotensin receptor blockers 43% vs 29%; beta-blockers 45% vs 15%. This heterogeneity is both a strength (generalizability) and weakness (confounding).

**Treatment effect signal:** Among patients who started statins or aspirin after coronary computed tomography angiography, FAI lost prognostic significance (adjusted HR 2.85, 95% confidence interval 0.44 to 18.49, P=0.25). Wide confidence interval spanning nearly two orders of magnitude. Suggestive but underpowered.

**Secondary endpoint:** FAI ≥ -70.1 associated with acute myocardial infarction risk (HR 5.08, 1.89 to 13.61, P=0.0012) in post-hoc analysis.

**High-sensitivity C-reactive protein reference:** FAI correlated with hsCRP at rho=-0.11 (P=0.25) in a separate unpublished cohort of 107 individuals. CRISP-CT cohorts did not measure hsCRP. The weak, non-significant correlation supports FAI capturing local rather than systemic inflammation.

### FAI + High-Risk Plaque Interaction: 2020, Journal of the American College of Cardiology

Post-hoc 2×2 stratification of CRISP-CT: FAI (high/low at -70.1 HU) × high-risk plaque features (positive remodeling, low-attenuation plaque, spotty calcification, or napkin-ring sign). 74 cardiac deaths total.

| Group (RCA cutoff) | n | Adjusted HR cardiac mortality | P |
|---------------------|---|-------------------------------|---|
| FAI-low / HRP-negative (reference) | 2,234 | 1.00 | reference |
| FAI-low / HRP-positive | 726 | 1.00 (0.48 to 2.08) | 0.98 |
| FAI-high / HRP-negative | 755 | 5.62 (3.02 to 10.47) | <0.001 |
| FAI-high / HRP-positive | 197 | 7.29 (3.36 to 15.81) | <0.001 |

**The central insight:** High-risk plaque morphology without active inflammation carries NO excess cardiac mortality risk. Inflammation without visible plaque pathology identifies patients at substantial risk. Inflammation contextualizes plaque features, not the other way around.

**Sensitivity analysis:** Cleveland sub-cohort (n=2,040), composite endpoint cardiac mortality + non-fatal myocardial infarction (65 events): FAI-high/HRP-negative HR 5.58 (P<0.001); FAI-low/HRP-positive HR 0.83 (P=0.64). After additional adjustment for coronary artery calcium (n=1,415): FAI-high/HRP-negative still HR 8.45 (P=0.01).

## Fat Radiomic Profile: Beyond Mean Attenuation

### Oikonomou et al. 2019, European Heart Journal | approximately 400 citations

**The problem FAI cannot solve:** FAI captures acute inflammation (the lipid-to-water shift from cytokine-mediated inhibition of adipocyte differentiation). But PVAT also undergoes chronic structural changes (fibrosis and microvascular remodeling) that are irreversible. Mean attenuation is blind to tissue texture. Higher-order radiomic features are not.

### Radiotranscriptomic Validation (Study 1, n=167 surgery patients)

Paired CT radiomic features with tissue gene expression for three biological processes:

| Gene | Biological Process | Best CT predictor |
|------|-------------------|-------------------|
| TNFA (Tumor Necrosis Factor Alpha) | Inflammation | Mean attenuation (essentially FAI) |
| COL1A1 (Collagen Type I Alpha 1 Chain) | Fibrosis | Higher-order texture features |
| CD31/PECAM1 (Platelet Endothelial Cell Adhesion Molecule) | Vascularity | Higher-order texture features |

Adding radiomics to a model with clinical factors + FAI improved detection of fibrosis (P=0.005) and vascularity (P=0.015) but NOT inflammation (P=0.35). This proves texture features capture biology invisible to FAI.

**Critical tissue source caveat:** The tissue came from subcutaneous chest wall fat at the surgical incision site (segmented on three axial slices at the xiphoid process level), NOT pericoronary adipose tissue. The gene-expression-to-CT-feature linkage was established in a different depot from the one being imaged clinically.

### Radiomic Feature Extraction Pipeline

**Software:** 3D Slicer (version 4.9.0) with SlicerRadiomics extension incorporating the PyRadiomics library.

**Feature types extracted (843 per vessel):**

| Category | Examples | What They Capture |
|----------|---------|-------------------|
| First-order statistics | Mean, variance, skewness, kurtosis, percentiles | Overall attenuation distribution (no spatial information) |
| Gray Level Co-occurrence Matrix (GLCM) | Autocorrelation, entropy, correlation, cluster shade | Spatial relationships between voxel pairs in a given direction/distance |
| Gray Level Run Length Matrix (GLRLM) | Long/short run emphasis | Continuous voxels in one direction with similar gray level |
| Gray Level Size Zone Matrix (GLSZM) | Large/small area emphasis | Contiguous areas of similar gray level |
| Neighbouring Gray-Tone Difference Matrix (NGTDM) | Strength, contrast, busyness | Differences between a voxel and its neighborhood |
| Wavelet decompositions | Applied across all above features in 8 filter combinations (LLL, LLH, LHL, LHH, HLL, HLH, HHL, HHH) | High-frequency = discontinuities, texture edges; Low-frequency = coarse structure |

**Segmentation:** PVAT defined as voxels in -190 to -30 HU within radial distance equal to vessel diameter. RCA: anatomical segments 1, 2, 3. Left coronary artery: combined left main and proximal to mid LAD (segments 5, 6, 7). **Left circumflex NOT analyzed** (variable anatomy, small caliber).

### Feature Selection Pipeline

| Step | Input | Output | Method |
|------|-------|--------|--------|
| Extraction | Raw CT data | 843 features × 2 vessels = 1,686 per patient | PyRadiomics |
| Stability filtering | 1,686 features | 1,391 features (82.0% retained) | ICC ≥ 0.9 from n=15 scans |
| Correlation filtering | 1,391 features | 335 independent features | |Spearman rho| ≥ 0.9 removed, using findCorrelation from R caret package |
| Feature selection | 335 features | 64 optimal features | Recursive feature elimination with random forest, repeated 5-fold cross-validation (3 rounds) |
| Final model | 64 features | FRP probability score | Random forest classifier |

**Training data:** 101 major adverse cardiovascular events cases (cardiac death or non-fatal acute myocardial infarction within 5 years) matched 1:1 with 101 controls (matched for age, sex, risk factors, scanner, cohort location, tube voltage). Split 80% training / 20% external validation. FRP = output probability of belonging to the MACE group.

**Optimal cutoff:** FRP ≥ 0.63 (maximizing log-rank statistic in SCOT-HEART).

### Clinical Validation (SCOT-HEART, n=1,575)

Median follow-up 4.8 years (interquartile range 4.2 to 5.7). Endpoint: MACE defined as cardiac death + non-fatal acute myocardial infarction (revascularization excluded, making this a harder endpoint). Events: 1 cardiac death, 33 non-fatal acute myocardial infarction, 176 late revascularization, 32 non-cardiac deaths.

| Analysis | Adjusted HR (95% CI) | P |
|----------|---------------------|---|
| FRP per 0.01 increment, MACE | 1.12 (1.08 to 1.15) | <0.001 |
| FRP ≥ 0.63 vs < 0.63, MACE | 10.84 (5.06 to 23.22) | <0.001 |
| FRP-positive / HRP-positive vs FRP-negative / HRP-negative | 43.33 (9.14 to 205.48) | <0.001 |
| FRP-positive / HRP-negative (risk invisible to plaque analysis) | 32.44 (7.00 to 150.38) | <0.001 |
| FRP-negative / HRP-positive | 3.43 (1.89 to 6.21) | <0.001 |
| Non-cardiac mortality (specificity check) | 0.58 (0.22 to 1.56) | 0.28 |

**Discrimination improvement:** Traditional model AUC 0.754 (includes age, sex, systolic blood pressure, diabetes, smoking, body mass index, obstructive disease, total cholesterol, HDL, scanner type, high-risk plaque features, Agatston calcium score [log(CCS+1)]). Adding FRP: AUC 0.880 (delta 0.126, P<0.001).

**FRP is completely independent from plaque features:** Correlation with high-risk plaque rho=0.004 (P=0.87). Correlation with calcium score rho=0.07 (P=0.007, statistically significant but clinically negligible). FRP captures an entirely orthogonal risk dimension.

**Temporal dissociation between FAI and FRP:** In acute myocardial infarction patients with serial CT (n=16 total, n=10 ST-elevation myocardial infarction for culprit-lesion analysis), FAI elevated acutely and decreased at 6 months (dynamic, reversible). FRP elevated at both timepoints (stable, irreversible). FAI tracks active inflammation; FRP tracks cumulative structural damage.

**Practical limitations:**

* Processing time approximately 45 minutes per patient (projected to drop to under 5 minutes with GPU cloud processing)
* External validation set approximately 40 patients with approximately 20 events (very small, explaining the wide confidence interval 0.622 to 0.926)
* Only 34 MACE events in SCOT-HEART (1 cardiac death)
* Random forest hyperparameters (number of trees, max depth, min leaf size) not published
* Complete 64-feature list not enumerated (only top 20 shown by variable importance)
* No calibration plots or Hosmer-Lemeshow test
* No competing risk analysis despite non-cardiac deaths

### The 16-Point Radiomic Quality Framework (2020 Cardiovascular Research)

The Oxford group published a quality standard for cardiac CT radiomics, based on Lambin et al. (Nature Reviews Clinical Oncology, 2017). Key criteria:

1. Pre-defined image protocol and prospective registration
2. Segmentation robustness (ICC)
3. Sensitivity to technical acquisition parameters across scanners/vendors
4. Scan-rescan robustness
5. Normalization and standardization protocol
6. Algorithm selection rationale
7. Multiple comparisons and redundancy addressed
8. Multivariable models adjusted for traditional risk factors
9. Associations with known clinical variables explored
10. Risk group cutoffs defined a priori
11. Discrimination metrics appropriate to task
12. Calibration metrics presented
13. Internal AND external validation
14. Comparison to clinical gold standard with reclassification
15. Clinical utility and cost-effectiveness
16. Code/algorithm accessibility

This is self-referential (the same group proposing the standard that their own work aspires to meet), but the criteria themselves are reasonable. FRP meets criteria 1 through 3, 6 through 8, 10 through 14, but not 4 (no scan-rescan), 5 (normalization not described), 12 (no calibration), 15 (no cost analysis at time of FRP publication), or 16 (code not accessible).

## FAI as a Treatment-Response Biomarker

### Elnabawi and Antoniades 2019, JAMA Cardiology | n=134

n=134 patients with moderate-to-severe psoriasis: 82 on biologics (anti-Tumor Necrosis Factor, anti-Interleukin-12/23, anti-Interleukin-17), 52 untreated controls. Coronary computed tomography angiography at baseline and 1 year. All scans on the same 320-detector-row scanner (Canon/Toshiba Aquilion ONE ViSION), eliminating inter-scanner variability. FAI measured using CaRi-Heart algorithm. Low cardiovascular risk population (median Framingham Risk Score 3%).

| Group | Baseline FAI (HU) | 1-year FAI (HU) | P |
|-------|-------------------|-----------------|---|
| Biologics (n=82) | -71.22 | -76.09 | <0.001 |
| Anti-TNF subgroup | -71.25 | -75.49 | <0.001 |
| Anti-IL subgroup | -71.18 | -76.92 | <0.001 |
| Untreated controls (n=52) | -71.98 | -72.66 | 0.39 |
| Topical therapy only | no change | no change | not significant |

Propensity score matching (n=45 pairs) replicated the finding (P<0.001 for treated, P=0.95 for untreated, P=0.003 for interaction). High-sensitivity C-reactive protein decreased concordantly (2.2 to 1.3 mg/L, P=0.03 in treatment group). FAI improvement present in patients both WITH and WITHOUT coronary plaque at baseline (46 of 134 had plaque), suggesting the effect is on the perivascular microenvironment independent of plaque presence. Topical therapy alone had no effect, arguing for a systemic anti-inflammatory mechanism.

**Limitation:** Non-randomized, open-label. No hard cardiovascular outcomes. Selection bias (controls "elected not to receive biologic therapy").

### Other Treatment-Response Data

* After statin treatment: significant FAI reduction around noncalcified and mixed plaques at 1 year (reported in the 2021 virtual guide paper)
* CRISP-CT post-hoc: FAI lost prognostic significance in patients starting statins/aspirin after CCTA (suggestive of modifiable risk, though underpowered)

## Standardization: From Raw FAI to FAI-Score

### Oikonomou et al. 2021, Cardiovascular Research

**The problem:** Raw FAI depends on scanner model, tube voltage, contrast protocol, reconstruction algorithm, patient age, sex, body composition, and which artery is measured. A raw FAI of -72 HU on one scanner may not mean the same as -72 HU on another. FAI-Score solves this by transforming raw FAI through standardization.

### FAI-Score Definition

FAI-Score transforms raw FAI by adjusting for:

1. Technical scan parameters (tube voltage, possibly others)
2. Anatomical factors (fat distribution around the arteries, vessel-specific)
3. Biological characteristics (age, sex)

Output: age- and sex-specific percentile curves (nomograms) for each coronary artery (RCA, LAD, LCx). The nomograms were generated from pooled United States (n=2,040) and European (n=1,872) cohorts.

**What is NOT published about FAI-Score:**

* The mathematical transformation formula (linear regression? nonlinear? machine learning model?)
* Specific regression coefficients or weighting scheme
* How the "weighting" is applied per concentric layer
* The nomogram generation methodology (GAMLSS? quantile regression? other?)
* The actual HU values corresponding to the 75th, 90th, or 95th percentile FAI-Scores
* The complete input feature set beyond "tube voltage, anatomy, age, sex"

### CaRi-Heart Device Pipeline

| Step | Method | Automation |
|------|--------|------------|
| 1. Data transfer | DICOM from hospital PACS via gateway appliance | Automated |
| 2. EAT and perivascular space segmentation | Deep learning network (architecture not published) | Semi-automated (DL + human analyst review and edit) |
| 3. Coronary artery identification | Proprietary ML model (2025 abstract) | Automated |
| 4. Raw FAI computation | Proximal RCA (10 to 50 mm), LAD (40 mm), LCx (40 mm) | Automated |
| 5. FAI-Score computation | Adjustment for technical, anatomical, demographic parameters | Proprietary algorithm |
| 6. CaRi-Heart Risk computation | 8-year cardiac mortality probability integrating FAI-Score + modified Duke CAD index + clinical risk factors (diabetes, smoking, hyperlipidemia, hypertension) | CART classifier (chosen over k-nearest neighbor and naive Bayes via 10-fold cross-validation; accuracy 0.82) |
| 7. Report generation | Risk classification: Low/medium, High, Very high | Automated |

### AI-Risk Classification Thresholds

| Category | Criteria |
|----------|---------|
| Low/medium risk | AI-Risk <5% AND FAI-Score <75th percentile in LAD/RCA AND <95th percentile in LCx |
| High risk | AI-Risk 5% to <10% AND/OR FAI-Score in LAD/RCA between 75th and 90th percentile AND/OR FAI-Score in LCx above 95th percentile |
| Very high risk | AI-Risk ≥10% AND/OR FAI-Score in LAD/RCA above 90th percentile |

### FAI-Score vs Raw FAI: Why It Matters

**Unlike raw FAI (which lost prognostic significance for the left circumflex in CRISP-CT), FAI-Score retained prognostic value for ALL three vessels including the left circumflex.** This is a direct benefit of the standardization: removing technical and anatomical confounders recovers signal that was previously buried in noise.

### Validation

* AUC 0.809 for 8-year cardiac mortality. Optimism-corrected AUC = 0.809 (95% CI 0.805 to 0.814). Trained on US cohort (Cleveland), externally validated in European cohort (Erlangen).
* Delta C-statistic: 0.085 (P=0.01) in US, 0.149 (P<0.001) in European cohort over baseline clinical risk factor model.
* FAI-Score reclassified approximately 33% of patients (16% to higher risk, 17% to lower risk).
* Negative predictive value 99.3% for CaRi-Heart Risk above 10%.
* No association between coronary calcium score and FAI-Score, confirming orthogonality.
* FAI-Score shows a steep non-linear increase with age, suggesting inflammatory signal increases exponentially in older patients. Relative risk at 95th percentile: RCA 5.3×, LAD 3.2×, LCx 2.4×.

### European Society of Cardiology Consensus Statement (2023, European Heart Journal)

The ESC Working Group endorsed:

1. FAI-Score as the regulatory-cleared metric for coronary inflammation
2. The Oxford PVAT definition (radial distance = vessel diameter from outer wall)
3. CaRi-Heart version 2.5 by name
4. 75th, 90th, and 95th percentile cutoffs for risk stratification

**Gaps identified by the ESC consensus:**
1. No randomized controlled trials of FAI-guided therapy
2. Per-lesion FAI not validated
3. Photon-counting CT needs recalibration
4. Non-coronary PVAT not validated
5. No PVAT-specific drug delivery

## Population-Scale Validation: ORFAN

### Chan et al. 2024, The Lancet | n=40,091

The largest validation of CT-based coronary inflammation assessment. Registered as NCT05169333.

**Cohort A (n=40,091):** All consecutive clinically indicated coronary computed tomography angiograms from 8 NHS hospitals (Oxford, Bath, Papworth, Royal Brompton, Harefield, Leicester, Milton Keynes, Leeds), 2010 to 2021. Median follow-up 2.7 years (interquartile range 1.4 to 5.3). Outcomes linked via NHS Digital (Hospital Episode Statistics, Office for National Statistics, National Institute for Cardiovascular Outcomes Research). 77.5% White. Exclusions: NHS Digital opt-outs or no local CCTA report (n=4,709).

**Cohort B (n=3,393):** Nested from two hospitals with longest follow-up (Royal Brompton and Harefield), 2010 to 2015. Median follow-up 7.7 years (interquartile range 6.4 to 9.1). Additional exclusions: congenital heart disease (n=91), heart transplant evaluation (n=103), poor image quality (n=74).

**Events (Cohort A):** 4,307 MACE (10.7%), 1,754 cardiac deaths (4.4%), 1,898 non-fatal myocardial infarction (4.7%), 1,727 new heart failure (4.3%), 3,501 non-cardiac deaths (8.7%). MACE defined as composite of myocardial infarction, new heart failure, and cardiac death (ICD-10 codes from national databases; revascularization NOT part of primary endpoint).

### The Central Epidemiological Finding

81.1% of patients (32,533 of 40,091) had no obstructive coronary artery disease. This group accounted for **66.3% of all MACE** (2,857 of 4,307) and **63.7% of cardiac deaths** (1,118 of 1,754). Current practice sends these patients home reassured. FAI-Score identifies the high-risk subset.

Obstructive coronary artery disease itself has relatively modest hazard ratios: 1.42 for cardiac mortality, 1.41 for MACE, 1.71 for myocardial infarction. The inflammation signal captured by FAI dwarfs the prognostic value of anatomical stenosis grading.

### Key Prognostic Results

**FAI-Score quartile analysis (LAD, whole population, cardiac mortality):**

| Quartile | HR (95% CI) | P |
|----------|------------|---|
| Q1 (reference) | 1.00 | reference |
| Q2 | 3.87 (2.09 to 7.16) | <0.001 |
| Q3 | 8.30 (4.64 to 14.82) | <0.001 |
| Q4 | 20.20 (11.49 to 35.53) | <0.001 |

**Dose-response of inflamed vessels (cardiac mortality, vessels above 75th percentile FAI-Score):**

| Inflamed vessels | HR (95% CI) |
|-----------------|------------|
| 0 (reference) | 1.00 |
| 1 | 13.0 (5.85 to 28.8) |
| 2 | 20.4 (9.35 to 44.7) |
| 3 | 29.8 (13.9 to 63.9) |

This near-linear scaling suggests independent inflammatory contributions from each coronary territory.

**FAI-Score per 1 standard deviation, cardiac mortality (adjusted for cardiovascular risk factors + CAD-RADS 2.0):**

| Vessel | Total inflammatory risk HR | Residual inflammatory risk HR |
|--------|--------------------------|-------------------------------|
| LAD | 1.67 (1.58 to 1.76) | 1.30 (1.22 to 1.40) |
| LCx | 1.95 (1.83 to 2.07) | 1.43 (1.32 to 1.55) |
| RCA | 1.55 (1.47 to 1.63) | 1.25 (1.14 to 1.38) |

**AI-Risk classification (Cohort B, n=3,393, cardiac mortality):**

| Category | HR (95% CI) | P |
|----------|------------|---|
| Low/medium (reference) | 1.00 | reference |
| High | 2.47 (1.77 to 3.45) | <0.001 |
| Very high | 6.75 (5.17 to 8.82) | <0.001 |

### Discrimination

**10-year time-dependent AUC for cardiac mortality (Cohort B):**

| Model | AUC | P vs previous |
|-------|-----|---------------|
| QRISK3 alone | 0.784 | reference |
| QRISK3 + CAD-RADS 2.0 (stenosis grading) | 0.789 | 0.38 (no improvement) |
| QRISK3 + CAD-RADS 2.0 + AI-Risk | 0.854 | 7.7×10⁻⁷ |

Adding stenosis grading to traditional risk scores did NOT improve prediction. Adding inflammation assessment did.

QRISK3 was developed from the same NHS Digital data source as the outcomes in ORFAN, giving it a home-field advantage. AI-Risk was trained on US data and was NOT retrained for the UK population due to regulatory restrictions on the locked model. Despite this disadvantage, AI-Risk significantly improved discrimination.

**Reclassification (vs QRISK3, cardiac mortality):** NRI 0.38 (0.23 to 0.45), P<0.0001. IDI 0.028 (0.014 to 0.047), P<0.0001.

**Calibration:** Excellent alignment between predicted and observed events in the overall population and in those without obstructive coronary artery disease. Overestimates risk in obstructive disease (because CCTA triggers interventions that reduce the risk the model predicts).

### Statistical Methods

* Multivariable Cox regression. Schoenfeld residuals confirmed proportional hazards.
* Time-dependent AUC using methods of Blanche et al. (2013, Statistics in Medicine) for censored event times with competing risks.
* NRI (continuous) and IDI calculated with 200 bootstrap replications.
* Missing data: smoking status imputed using MICE package in R with CART method, based on patient demographics and smoking-related diseases at follow-up.
* No formal competing-risk analysis despite non-cardiac deaths exceeding cardiac deaths.
* Covariates: cardiovascular risk factors, medications (beta-blockers, calcium channel blockers, nitrates, statins, ACE inhibitors, ARBs, diuretics, digoxin, insulin, oral hypoglycemics, direct oral anticoagulants), history of myocardial infarction/revascularization, CAD-RADS 2.0.

### Additional Findings

* FAI-Score predictive even in patients with NO visible atheroma on CCTA (shown in appendix), meaning coronary inflammation is prognostic before any plaque appears.
* Post-hoc sensitivity analysis in 1,300 patients with non-contrast CT: FAI-Score remained predictive after adjusting for coronary calcium score.
* **Real-world NHS survey (n=744):** AI-Risk changed management in 45% of patients. Statin initiation 24%, statin dose increase 13%, additional treatments 8% (aspirin 2.4%, colchicine 8.3%, icosapent ethyl 0.4%).

### Meta-Analysis Context (Sagris et al. 2022, European Heart Journal Cardiovascular Imaging)

Systematic review of 20 studies (7,797 patients total, 9 in quantitative meta-analysis). Pooled FAI hazard ratio for MACE: 3.29 (1.88 to 5.76), I-squared 75% (high heterogeneity). Pooled mean difference for detecting unstable plaques: 4.50 HU (1.10 to 7.89), I-squared 88% (high heterogeneity). The high heterogeneity reflects differences in FAI measurement methods, populations, and endpoints across studies.

## Health Economics and Real-World Impact

### Tsiachristas et al. 2025, European Heart Journal: Quality of Care and Clinical Outcomes

Hybrid decision-tree with population-cohort Markov model. 3-month cycle length, 30-year lifetime horizon, 3.5% discount rate (standard NHS parameters). Two arms: standard care vs standard care + AI-Risk assessment.

**Data sources:** ORFAN Cohort B (n=3,393) for outcomes; 744-patient NHS survey for treatment changes; 1,214-patient prospective study for NICE guideline compliance; Cholesterol Treatment Trialists meta-analysis (170,000 participants, 26 trials) for statin effects.

**Base case results per 5,000 simulated patients (lifetime):**

| Outcome | Reduction |
|---------|-----------|
| Myocardial infarction | 96 fewer (11%) |
| Stroke | 22 fewer (4%) |
| Heart failure | 68 fewer (4%) |
| Cardiac death | 129 fewer (12%) |
| QALY gain per patient | 0.21 (0.18 to 0.24) |

**Cost-effectiveness:**

| AI-Risk price | ICER (£ per QALY) |
|---------------|-------------------|
| £300 | 1,371 (1,244 to 1,569) |
| £500 | 2,307 (2,036 to 2,596) |
| £700 | 3,244 (2,918 to 3,627) |

All well below NICE threshold of £20,000 to £30,000 per QALY. 100% of 1,000 probabilistic sensitivity analysis simulations fell below £20,000.

**Worst-case sensitivity analyses (all at £700 price):**

| Scenario | ICER |
|----------|------|
| Full NICE guideline compliance as baseline | £3,103 |
| 50% reduction in statin effectiveness | £6,592 |
| 50% reduction in risk reclassification accuracy | £6,522 |
| Non-obstructive CAD patients only | £2,898 |
| Adding colchicine to very-high-risk patients | £1,837 |

Even under the most pessimistic assumptions, all ICERs remain below £6,600.

**Key assumption:** The treatment benefit of statins (from the CTT meta-analysis) is assumed to apply equally to patients reclassified by AI-Risk. No trial has tested whether patients identified specifically by high FAI benefit more or less from statins than those identified by other means.

## The Patent

### US 10,695,023 B2 | Priority August 15, 2014 | Filed August 14, 2015 | Granted June 30, 2020

Filed by **Oxford University Innovation Limited** (the university's technology transfer office), not Caristo Diagnostics. Caristo holds an exclusive license.

**2 independent claims** (Claims 1 and 37). Both require ALL of: computed tomography data → volumetric characterization using concentric layers from the outer vessel wall → radiodensity quantification per layer → comparison to baseline → administering a therapy. Claims 14 and 21 are DEPENDENT on Claim 1 (adding VPCI-i integral calculation and VPCI subtraction method respectively).

**Key dependent claims:** 4 cm proximal RCA starting 1 cm from ostium (Claim 4), specific arteries including non-coronary such as carotid and femoral (Claims 5 to 6), 1 mm thick layers (Claim 7).

**What the patent does NOT cover:**

| Approach | Covered? | Why |
|----------|----------|-----|
| Simple mean PVAT attenuation without concentric layers | No | Claims require layer-by-layer spatial analysis |
| Non-CT modalities (MRI, ultrasound, PET) | No | Claims explicitly require "computed tomography" |
| Pure diagnostic/research use without therapy | No | Both independent claims terminate with "administering a therapy" (significant enforcement weakness) |
| Machine learning radiomics (FRP) | No | Not described in patent |
| FAI-Score nomogram/percentile calculation | No | Later development, not in patent |
| Photon-counting CT with material decomposition | Possibly | "Computed tomography" is broad, but material decomposition is a fundamentally different physics |

The patent specification contains extensive biological data (Figures 13 to 20), which is unusual for an imaging method patent and reflects the biology-first research architecture.

**Related applications:** PCT/GB2017/053262, GB2018/1818049.7, GR20180100490, GR20180100510

## Caristo Diagnostics

| Product | Function | Status |
|---------|----------|--------|
| **CaRi-Heart** (FAI-Score + AI-Risk) | Coronary inflammation from routine CCTA | CE Mark (MDR), UKCA, Australia. Investigational in US. |
| **CaRi-Plaque** | Automated plaque + stenosis quantification | CE Mark, UKCA, **FDA 510(k) cleared** (K242240, 2025) |
| **AI-Risk** | Integrated 8-year cardiac risk score | Part of CaRi-Heart platform |

Founders: Antoniades, Shirodaria, Channon, Neubauer. Data infrastructure: ORFAN (Oxford Risk Factors and Non-Invasive Imaging Study). Multiple paper co-authors are Caristo employees or consultants.

The entire evidence chain (biomarker discovery, device development, clinical validation, consensus guidelines, health economics) has been produced by a group with direct financial interest. Each paper discloses this. The evidence needs independent replication by groups without Caristo ties.

## What Is NOT Published: Reproducibility Gaps

This section collects everything that would be needed to independently reproduce or compete with the Oxford group's work but is not available in the published literature.

### Algorithm Internals

1. **FAI-Score transformation:** The exact mathematical formula converting raw FAI to FAI-Score is proprietary. The regression model form, coefficients, and weighting scheme are not disclosed.
2. **AI-Risk classifier:** Uses a CART model (classification and regression tree) but the internal structure, decision boundaries, and node weights are not published.
3. **CaRi-Heart segmentation DL model:** Architecture not specified. Training data size not specified. Segmentation accuracy metrics (Dice coefficient, intersection over union) not published.
4. **The "weighted" FAI:** Whether distance-weighted, volume-weighted, or ML-predicted is never clarified.
5. **FAI-Score percentile thresholds:** The actual HU values corresponding to the 75th, 90th, and 95th percentile FAI-Scores are embedded in the device, never published.
6. **FRP random forest:** Complete 64-feature list not enumerated. Hyperparameters not stated. Trained model not available for download.

### Technical Gaps

7. **Reconstruction kernel effects:** Never tested in any paper. Kernel choice substantially affects CT attenuation measurements.
8. **Contrast protocol effects:** Injection rate, iodine concentration, scan timing relative to contrast peak never tested.
9. **Scanner diversity:** GE scanners never tested. Canon/Toshiba tested only in one single-scanner study (psoriasis). No systematic cross-vendor comparison published.
10. **Partial volume handling:** No explicit erosion step or buffer at the vessel-fat interface described. No protocol for calcium-abutting-PVAT scenarios.
11. **Motion artifact criteria:** 6 to 9% scan exclusion rate, but specific criteria not published.

### Statistical Gaps

12. **Competing risks:** None of the outcome studies formally model competing risks, despite non-cardiac deaths exceeding cardiac deaths in ORFAN Cohort A (3,501 non-cardiac vs 1,754 cardiac).
13. **Treatment paradox:** Post-CCTA management changes (statin initiation, revascularization) attenuate the observed FAI/FRP effect. Acknowledged but never formally modeled (e.g., inverse probability of treatment weighting).
14. **FRP calibration:** No calibration plots or Hosmer-Lemeshow test for FRP.

### Data Access

15. **ORFAN individual patient data:** Available only by request to the Principal Investigator, reviewed by the ORFAN Publication and Data Sharing committee. The CIMAR gateway used for data transfer is a Caristo Diagnostics platform.
16. **Cost-effectiveness model:** Built in TreeAge Pro (proprietary software). Transition probabilities, utility values, and cost inputs in supplementary materials only.

## Open Questions and Limitations

### Imaging Science

1. **FAI specificity for inflammation.** The biological model is: inflammation → cytokine inhibition of preadipocyte differentiation → less lipid → higher attenuation. But other processes also alter adipocyte biology (fibrosis, edema, hemorrhage, metabolic stress). FAI may capture a composite signal. FAI does not correlate with macrophage markers (CD68) in epicardial fat.

2. **The left circumflex gap.** LCx is excluded from most analyses and from FRP entirely. LCx raw FAI was not predictive in CRISP-CT (though FAI-Score recovered LCx significance after standardization). Any approach limited to RCA and LAD misses a major territory. Left main is also excluded (variable length, highest-risk territory).

3. **Positive predictive value.** At the -70.1 HU cutoff, positive predictive value is only 5.9%. FAI is far better at ruling out risk (negative predictive value 99.5%) than confirming it. Clinical deployment must account for counseling the many false positives.

4. **Radiotranscriptomic tissue mismatch.** FRP's biological grounding (linking radiomic features to gene expression) was established in subcutaneous chest wall fat from surgical incisions, not in pericoronary adipose tissue. The assumption that the same feature-to-biology relationships hold in a different depot is unvalidated.

5. **Short follow-up extrapolation.** ORFAN Cohort A median follow-up is 2.7 years for an 8-year prediction model. Calibration in obstructive disease shows overestimation.

### Clinical Translation

6. **No randomized controlled trial.** ESC Gap #1. All evidence is observational. The 45% management change is uncontrolled. Whether FAI-guided therapy improves outcomes is unknown.

7. **Proprietary black box.** Independent groups cannot reproduce FAI-Score or AI-Risk computations. This is standard for commercial medical devices but limits scientific scrutiny and creates vendor lock-in.

8. **Scanner standardization treadmill.** Photon-counting CT, new reconstruction algorithms, and iterative reconstruction methods will require ongoing recalibration. The 2025 robustness data is a conference abstract from one site.

9. **Population diversity.** ORFAN was 77.5% White. Biology work was approximately 83% male. Generalizability to non-White populations, women, and younger patients with early disease is untested.

## Opportunities for Competing Work

1. **MRI-based PVAT characterization.** The patent is CT-specific. MRI offers fat/water fraction, T1/T2 mapping, and diffusion-weighted imaging: potentially richer tissue characterization without ionizing radiation. No group has demonstrated PVAT inflammation detection by MRI.

2. **Open-source, reproducible PVAT analysis.** A transparent, publicly validated pipeline (vessel segmentation, PVAT definition, FAI computation) would be scientifically complementary to the proprietary approach. Every specific number needed to reproduce "crude" FAI (the -190 to -30 window, radial distance = vessel diameter, proximal segments) IS published. What cannot be reproduced is the "corrected" FAI and FAI-Score.

3. **Photon-counting CT / dual-energy CT.** Material decomposition enables direct fat/water/calcium separation. Fundamentally different measurement physics from single-energy attenuation. Not covered by the patent unless using the concentric layer method. Could potentially quantify fat composition more precisely than the attenuation-window approach.

4. **Non-coronary PVAT.** Carotid (stroke), aortic (aneurysm), femoral (peripheral artery disease): all clinically important, all acknowledged as unvalidated in the ESC consensus. The patent claims cover non-coronary arteries (Claims 5 to 6), but the FAI-Score nomograms are coronary-specific.

5. **Reconstruction kernel and contrast timing.** These are the two largest untested confounders. A systematic study of kernel and contrast effects on PVAT attenuation would be a genuine contribution, potentially revealing failure modes the Oxford group has not addressed.

6. **Competing risk modeling.** No study in the Oxford program uses competing risk analysis. Given that non-cardiac deaths exceed cardiac deaths in ORFAN, a proper competing-risk framework (Fine-Gray or cause-specific hazards) could produce meaningfully different risk estimates.

7. **Diverse populations.** Women, non-White cohorts, younger patients with early disease. A PVAT study in a non-European population would have immediate scientific value.

8. **Prospective interventional evidence.** Even a small RCT of PVAT-guided therapy would address the field's most significant evidence gap.

9. **Interpretable radiomics.** FRP uses a 64-feature random forest that is a black box. A simpler, interpretable model (even if slightly less discriminating) would be scientifically more transparent and potentially more adoptable.

## Paper Catalogue

### Phase 1: Biology (2013 to 2016)

| # | Year | Title | Journal (Impact Factor) | Key Contribution |
|---|------|-------|------------------------|-----------------|
| 1 | 2013 | Adiponectin/eNOS in Human Vessels | *Circulation* (35.5) | Bidirectional PVAT-vascular signaling. n=677+46. |
| 2 | 2014 | Systemic Inflammation and BNP on Adiponectin | *ATVB* (8.4) | Depot-specific inflammation responsiveness; adiponectin paradox. n=575+13+19. |
| 3 | 2015 | Adiponectin Links Type 2 Diabetes to NADPH Oxidase | *Diabetes* (7.7) | Mendelian randomization proof; systemic biomarkers fail. n=386+67. |
| 4 | 2016 | EAT-Myocardial Redox via PPARγ/Adiponectin | *Circulation Research* (20.1) | AMPK pathway in myocardium (different from PI3K/Akt in arteries). n=247+59. |

### Phase 2: Reviews (2017)

| # | Year | Title | Journal (Impact Factor) |
|---|------|-------|------------------------|
| 5 | 2017 | Epicardial Adipose Tissue in cardiac biology | *Journal of Physiology* (5.5) |
| 6 | 2017 | Is fat always bad? | *Cardiovascular Research* (10.2) |
| 7 | 2017 | Dysfunctional adipose tissue | *British Journal of Pharmacology* (7.3) |
| 8 | 2017 | PVAT as vascular disease regulator | *British Journal of Pharmacology* (7.3) |
| 9 | 2017 | Adiponectin paradox | *British Journal of Pharmacology* (7.3) |

### Phase 3: FAI and CRISP-CT (2017 to 2018)

| # | Year | Title | Journal (Impact Factor) | Key Contribution |
|---|------|-------|------------------------|-----------------|
| **10** | **2017** | **Detecting coronary inflammation by imaging perivascular fat** | ***Science Translational Medicine*** **(17.1)** | **FAI invention.** 4 arms, n=453+45+273+22. VPCI. PET validation. |
| **11** | **2018** | **CRISP-CT** | ***The Lancet*** **(168.9)** | **Prognostic validation.** n=3,912. HR 9.04. PPV 5.9%, NPV 99.5%. |
| 12 | 2018 | Adipose tissue in cardiovascular health and disease | *Nature Reviews Cardiology* (41.7) | Definitive review positioning FAI. |
| 13 | 2018 | Perivascular adipose tissue and coronary atherosclerosis | *Heart* (5.0) | PVAT definition. Bridge from biology to imaging. |

### Phase 4: Extension (2019)

| # | Year | Title | Journal (Impact Factor) | Key Contribution |
|---|------|-------|------------------------|-----------------|
| **14** | **2019** | **Radiotranscriptomic Fat Radiomic Profile** | ***European Heart Journal*** **(39.3)** | **64-feature random forest captures fibrosis + vascularity beyond FAI.** n=167+202+1,575. |
| 15 | 2019 | Biologic therapy and coronary inflammation in psoriasis | *JAMA Cardiology* (14.8) | FAI as treatment-response biomarker. n=134. Single scanner. |
| 16 | 2019 | Imaging residual inflammatory cardiovascular risk | *European Heart Journal* (39.3) | Clinical positioning review with Deanfield. |
| 17 | 2019 | Atherosclerosis affecting fat | *Journal of Cardiovascular Computed Tomography* (3.3) | FAI methodology review. |
| 18 | 2019 | CT Assessment of Coronary Inflammation | *ATVB* (8.4) | Technical review. |
| 19 | 2019 | Making Sense From Perivascular Attenuation Maps | *JACC Cardiovascular Imaging* (12.8) | Interpretation guide. |
| 20 | 2019 | WNT5A/USP17/RAC1 pathway | *Science Translational Medicine* (17.1) | Second druggable axis; VSMC phenotypic switch. n=1,004. |

### Phase 5: Translation (2020 to 2023)

| # | Year | Title | Journal (Impact Factor) | Key Contribution |
|---|------|-------|------------------------|-----------------|
| 21 | 2020 | FAI + High-Risk Plaque Stratification | *JACC* (21.7) | HRP without inflammation = no excess risk. n=3,912. |
| 22 | 2020 | AI Radiomic Quality Framework | *Cardiovascular Research* (10.2) | 16-point radiomic quality standard. |
| 23 | 2021 | FAI in Coronary CTA: Practical Guide | *Radiology: Cardiothoracic Imaging* (4.5) | Dynamic behavior. Confounder discussion. |
| 24 | 2021 | Standardized FAI Measurement (CaRi-Heart) | *Cardiovascular Research* (10.2) | FAI-Score and CaRi-Heart specification. AUC 0.809. 33% reclassified. |
| 25 | 2021 | PVAT Imaging by CT: Virtual Guide | *British Journal of Pharmacology* (7.3) | Weighted FAI description. Measurement protocols. |
| 26 | 2022 | FAI Meta-Analysis | *EHJ Cardiovascular Imaging* (6.2) | 20 studies, 7,797 patients. MACE HR 3.29. I-squared 75%. |
| 27 | 2022 | Pericardial Adiposity by Cardiac MRI | *EHJ Cardiovascular Imaging* (6.2) | UK Biobank n=42,598. EAT volume → adverse remodeling, atrial fibrillation. |
| 28 | 2023 | Deep Learning EAT Segmentation | *JACC Cardiovascular Imaging* (12.8) | 3D Residual U-Net. Complementary to FAI. |
| 29 | 2023 | EAT-derived miR-92a-3p | *JACC* (21.7) | miR-92a-3p suppresses WNT5A/RAC1. GWAS Mendelian randomization. n=1,246. |
| 30 | 2023 | ESC Consensus Statement | *European Heart Journal* (39.3) | ESC endorses FAI-Score, CaRi-Heart, PVAT definition. 5 gaps identified. |

### Phase 6: Validation (2024 to 2026)

| # | Year | Title | Journal (Impact Factor) | Key Contribution |
|---|------|-------|------------------------|-----------------|
| **31** | **2024** | **ORFAN Study** | ***The Lancet*** **(168.9)** | **n=40,091.** HR 20.20 Q4 vs Q1. 81.1% non-obstructive. Dose-response. |
| 32 | 2024 | AI in atherosclerosis CT | *Atherosclerosis* (5.3) | Landscape review. |
| 33 | 2025 | FAI-Score robustness | Conference abstract | Stable within 0.5 units across technical parameters. n=7,822. |
| 34 | 2025 | FAI-Score standardization editorial | *JACC Cardiovascular Imaging* (12.8) | Case for standardized measurement. |
| 35 | 2025 | Cost-effectiveness of AI-Risk | *EHJ Quality of Care and Clinical Outcomes* (4.6) | ICER £1,371 to £3,244/QALY. 100% below NICE threshold. |
| 36 | 2026 | PVAT Imaging and Quantification | *ATVB* (8.4) | Latest methodological review. |

**Summary:** 36 papers | 19 original research | 12 reviews | 5 other (consensus, meta-analysis, editorial, health economics) | 1 US patent | 3 commercial products | approximately 50,000 patients validated | 8 publications in journals with impact factor above 15

*Last updated: March 13, 2026*
