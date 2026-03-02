# PCAT Research Context: Biomarker Validation, Material Decomposition, and Simulation Study Design

**Project**: PCAT Segmentation Pipeline — MolloiLab  
**Date**: March 2026  
**Scope**: Clinical validation evidence for FAI, its technical limitations, material decomposition as a superior alternative, XCAT phantom simulation methodology, and validation of the current MolloiLab study design.

---

## 1. FAI as a Validated Cardiovascular Biomarker

### 1.1 The CRISP-CT Study (Foundational)

> Oikonomou EK, Marwan M, Desai MY, et al. *Lancet*. 2018;392(10151):929–939. PMID: 30170852

CRISP-CT enrolled 1,872 patients undergoing clinically indicated CCTA. Key findings:

- **RCA-FAI** independently predicted cardiac death at 5-year follow-up: HR 9.04 (95% CI 2.12–38.6, p=0.003)
- FAI added incremental prognostic value beyond CACS, Gensini score, and Framingham Risk Score
- **FAI cut-off: −70.1 HU** identified by ROC analysis (AUC = 0.76 for cardiac death)
- Reproducibility: ICC = 0.987 intraobserver, 0.980 interobserver

**Technical specification:**

| Parameter | Specification |
|---|---|
| Fat HU window | −190 to −30 HU |
| VOI radial extent | Outer vessel wall + 1× mean vessel diameter |
| LAD/LCX segment | Proximal 40 mm from ostium |
| RCA segment | 10–50 mm (skip first 10 mm for aortic root pulsation artifact) |
| FAI computation | Mean HU of all voxels in VOI within fat window |

### 1.2 Mechanistic Histological Validation

> Antonopoulos AS et al. *Science Translational Medicine*. 2017. n=453 cardiac surgery patients.

Matched CT-histology specimens validated the molecular mechanism. Perivascular fat adjacent to inflamed coronary segments showed:

- Significantly reduced **lipid droplet size** (p < 0.001)
- Reduced adipogenic transcription factors: **PPARγ** (−2.3-fold), **FABP4** (−1.8-fold), **C/EBPα**
- Increased pro-inflammatory cytokines: **IL-6** (+3.1-fold), **TNF-α** (+2.7-fold), **CXCL10**

This confirms FAI reflects a genuine biological shift — not a measurement artifact. The shift is reversible: anti-inflammatory treatment normalises FAI.

### 1.3 ORFAN Trial (AI Score Validation)

> Oikonomou EK et al. *Nature Cardiovascular Research*. 2023. n=3,324.

The ORFAN prospective trial tested **CaRi-Heart** (Caristo Diagnostics):

- CaRi-Heart AI risk score outperformed ASCVD PCE score, SRS, and CACS alone
- Added incremental value in intermediate-risk patients (10-year ASCVD 7.5–20%)
- Integrates FAI + shape features + coronary calcification into a single AI risk score

**Clinical implication**: Per-vessel FAI values are the raw input to downstream AI models like CaRi-Heart.

### 1.4 PCAT Volume vs. PCAT Attenuation

| Measure | Definition | Biological Meaning | Clinical Correlation |
|---|---|---|---|
| **PCAT attenuation (FAI)** | Mean HU of fat-range voxels in proximal VOI | Acute inflammatory phenotypic shift | Future MACE, cardiac death, plaque vulnerability |
| **PCAT volume** | Total cm³ of fat-range voxels in VOI | Size of the pericoronary fat depot | Metabolic syndrome, obesity, chronic risk |

These are partially independent: high volume + low FAI (obese, not inflamed) vs. low volume + high FAI (lean, actively inflamed) are distinct clinical phenotypes.

---

## 2. The Problem with FAI: Protocol Dependence

### 2.1 Evidence for Protocol-Dependent Variation

The core limitation of FAI is that it measures **Hounsfield Units** — a physical attenuation measurement that depends on acquisition and reconstruction parameters. Multiple studies have quantified this:

#### Tube Voltage (kVp) Effects
- **Nie & Molloi 2025**: 21.9% HU variance across 80–135 kV for identical tissue composition
- **Ma et al. 2020**: FAI increases linearly with tube voltage (less negative at higher kV)
- **Etter et al. 2022**: Required conversion factors relative to 120 kVp: 1.267 (80 kVp), 1.08 (100 kVp), 0.947 (140 kVp)

#### Reconstruction Kernel and Algorithm
- **Lisi et al. 2025**: Up to **33 HU intra-individual variation** between reconstruction kernels and iterative reconstruction levels
- This means the same patient scanned once but reconstructed with different kernels can be classified as "inflamed" or "non-inflamed" depending on the reconstruction choice

#### Patient Body Habitus
- **Nie & Molloi 2025**: 3.6% HU variance between small, medium, and large patient sizes for identical tissue
- Beam hardening and scatter increase with body size

#### Contrast Timing and Perfusion
- **Wu et al. 2025**: ~**7 HU swing** in PCAT HU from contrast timing differences; ~**15% PCAT volume change**; **78% of radiomic features change >10%** between perfusion phases
- Bolus timing, injection rate, and cardiac output all affect iodine distribution

#### Scanner Platform
- Different detector technologies (conventional EID vs PCD-CT) produce systematically different HU values for the same tissue
- PCD-CT (NAEOTOM Alpha) studies from Zurich (Alkadhi, Eberhard, Mergen 2022–2025) show FAI values are not directly comparable to conventional CT without calibration

### 2.2 Clinical Impact of Protocol Dependence

The FAI threshold of **−70.1 HU** was validated on specific scanner platforms with specific protocols. When this threshold is applied to:
- Different tube voltages → misclassification
- Different reconstruction algorithms → misclassification
- Different scanner platforms → misclassification
- Longitudinal monitoring (protocol changes between scans) → unreliable trend detection

**This is the fundamental clinical problem our study addresses**: a biomarker that changes with the measurement protocol rather than with the disease state is unreliable for clinical decision-making.

### 2.3 The Need for a Protocol-Independent Biomarker

All the confounders above affect **HU values** but do NOT change the **actual tissue composition**. Inflamed PCAT has:
- More water content (~5% higher water fraction)
- Less lipid content (reduced triglyceride storage)
- Higher collagen/protein content (fibrotic remodelling)

These compositional differences are physical properties of the tissue that do not change with tube voltage, reconstruction kernel, or patient size. A measurement method that directly quantifies **tissue composition** rather than **attenuation** would be inherently protocol-independent.

This is exactly what **material decomposition** provides.

---

## 3. Material Decomposition: The Protocol-Independent Alternative

### 3.1 Principle

Material decomposition expresses each voxel as a weighted combination of basis materials (e.g., water, lipid, collagen, iodine) rather than a single integrated HU value. The decomposition exploits the energy-dependent attenuation of different materials:

- **Dual-energy CT (DECT)**: Two energy spectra → two-material decomposition (water + iodine, or fat + non-fat)
- **Photon-counting detector CT (PCD-CT)**: Multiple energy bins → multi-material decomposition
- **Single-energy CT with constraints**: Material decomposition possible with prior knowledge (e.g., fixed protein fraction)

### 3.2 Lab's Previous Work: Coronary Plaque Material Decomposition

> Ding Y, Molloi S. "Characterization of arterial plaque composition with dual-energy computed tomography." *2021*.

The lab demonstrated three-material decomposition (water, lipid, calcium) for coronary artery plaques using dual-energy CT. This established:
- Material decomposition methodology for coronary structures
- Accuracy validation against known phantom compositions
- Feasibility for clinical CCTA data

### 3.3 Lab's Previous Paper: Water-Lipid-Protein Decomposition for PVAT

> Nie A, Molloi S. "Quantification of Water and Lipid Composition of Perivascular Adipose Tissue Using Coronary CT Angiography: A Simulation Study." *Int J Cardiovasc Imaging* 2025;41:1091–1101.

This is the **direct predecessor** to the current study. Key details:

#### Study Design
- **Phantom**: Computational simulation of Canon Aquilion One 320-slice CT scanner
- **Tissue model**: Anthropomorphic thorax phantom (QRM) with 10 water-lipid-protein inserts
- **Patient sizes**: Small, medium, large (to test body habitus effects)
- **Tube voltages**: 80, 100, 120, 135 kV
- **Decomposition**: Three-material (water, lipid, protein) with protein fixed at 2.17%
- **Reconstruction**: FBP only

#### Key Results
| Metric | Value | Significance |
|---|---|---|
| **Water fraction RMSE** | 0.01–0.64% | Sufficient precision to detect 5% clinical threshold |
| **Water fraction RMSD** | 2.94–6.05% | Robust across conditions |
| **HU variance across 80–135 kV** | 21.9% | Demonstrates protocol dependence of HU |
| **HU variance across patient sizes** | 3.6% | Additional confounding |
| **Healthy PVAT water fraction** | 20–30% | Baseline range |
| **Diseased PVAT water fraction** | 20–35% (~5% increase) | Detectable clinical difference |

#### Key Conclusions
1. **Material decomposition (water fraction) is protocol-independent**: same composition yields same water fraction regardless of kV or patient size
2. **FAI (HU) is protocol-dependent**: same tissue gives different HU at different kV and patient sizes
3. Water fraction precision (RMSE 0.01–0.64%) is sufficient to detect the ~5% water increase that characterises inflamed PCAT

#### Acknowledged Limitations (addressed by current study)
1. FBP reconstruction only (clinical practice uses iterative reconstruction)
2. No bowtie filter in simulation
3. No cardiac motion artifacts
4. Single-energy CT only (not spectral/DECT)
5. Simple cylindrical phantom geometry (not anatomically realistic)
6. **Limitation #5 is directly addressed by the current study's use of XCAT phantoms**

### 3.4 Multi-Material Decomposition Methods in the Literature

#### Mendonça & Lamb (2014)
> "A flexible method for multi-material decomposition of dual-energy CT images."

Established the mathematical framework for multi-material decomposition from dual-energy CT data. Uses volume conservation constraint and known material attenuation coefficients to solve for 3+ material fractions from 2 energy measurements.

#### Xue et al. (2021)
> "Multi-material decomposition for single-energy CT using material sparsity constraint."

Extended material decomposition to **single-energy CT** by exploiting the assumption that most voxels contain only 2–3 materials (sparsity constraint). This is directly relevant to our approach — enabling material decomposition without requiring dual-energy or spectral CT.

#### Valand et al. (2026)
> "Truth-based physics-informed material composition estimation in spectral CT."

Developed physics-informed deep learning for material composition estimation in spectral CT. Uses known phantom compositions as "truth" targets for training, achieving higher accuracy than conventional decomposition. Relevant as a next-generation approach our lab could adopt.

---

## 4. Current Study: XCAT Phantom + Material Decomposition for PCAT Inflammation

### 4.1 Study Purpose

The current study extends Nie & Molloi (2025) by:
1. Using **XCAT phantoms** (anatomically realistic, population-representative) instead of simple cylindrical phantoms
2. Simulating **pericoronary adipose inflammation** as increased water content in PCAT
3. Creating matched **healthy vs. diseased** phantom pairs
4. Decomposing simulated CT scans into **water, lipid, collagen, and iodine** components
5. Demonstrating that inflamed PCAT has measurably more water than healthy PCAT
6. Showing that this difference is **NOT detectable by traditional FAI** (HU varies across protocols) but **IS detectable by material decomposition** (composition is protocol-independent)

### 4.2 Innovation Statement

**No existing study has combined XCAT phantoms with multi-material decomposition for PCAT inflammation detection.**

Specifically, this study is the first to:
1. Use anatomically realistic XCAT phantoms for PCAT simulation (vs. simple geometric phantoms)
2. Directly compare material decomposition vs. FAI for inflammation detection across multiple protocols
3. Demonstrate protocol-independent inflammation detection using compositional analysis
4. Extend material decomposition from 3 materials (water, lipid, protein) to 4 materials (water, lipid, collagen, iodine)

### 4.3 XCAT Phantom: Why It Matters

#### XCAT 3.0 (Dahal et al. 2025)
> Dahal S, Segars WP, et al. "XCAT 3.0." Duke University, 2025.

XCAT (eXtended CArdiac Torso) is the gold-standard computational human phantom for CT simulation:
- **2,500+ unique phantoms** spanning population demographics (age, sex, BMI, anatomy)
- Automated anatomical segmentation framework
- Realistic cardiac anatomy including coronary arteries, epicardial fat, pericardium
- Parameterised organ sizes and shapes
- Cardiac and respiratory motion models

**Advantage over previous study's phantom (QRM thorax)**: XCAT provides anatomically realistic coronary artery geometry, realistic pericoronary fat distribution, and population-representative body habitus variation — making results more clinically translatable.

#### Computational Coronary Plaques (Sauer et al. 2024)
> Sauer TJ, Samei E, et al. "Computational coronary artery plaques using DC-GAN for virtual imaging trials." Duke CVIT, 2024.

Demonstrated that realistic coronary artery plaques can be computationally generated and inserted into XCAT phantoms for virtual imaging trials. This validates the approach of simulating pathology in computational phantoms for CT imaging research.

#### Body Composition Transformation (Salinas et al. 2025)
> Salinas ML, et al. "Body composition transformation in XCAT phantoms." Duke, 2025.

Showed that XCAT phantom body composition can be systematically varied to represent different clinical scenarios — directly supporting our approach of varying PCAT composition between healthy and inflamed states.

### 4.4 Study Design

#### Phantom Construction
- **Healthy PCAT**: Water fraction 20–30% (predominantly lipid, normal adipocyte morphology)
- **Diseased (inflamed) PCAT**: Water fraction 25–35% (~5% increase, reflecting inflammatory phenotypic shift)
- Both embedded in anatomically realistic XCAT torso with coronary arteries, lumen contrast, myocardium

#### Simulated CT Protocols (to demonstrate protocol dependence of FAI)
| Variable | Values | Purpose |
|---|---|---|
| Tube voltage | 80, 100, 120, 135 kV | Demonstrate HU variation with kV |
| Patient size | Small, medium, large | Demonstrate HU variation with body habitus |
| Reconstruction | FBP, iterative reconstruction | Address limitation of previous study |
| Bowtie filter | With and without | Address limitation of previous study |

#### Analysis
1. **Traditional FAI**: Compute mean HU in fat window (−190 to −30 HU) for each phantom
2. **Material decomposition**: Decompose into water, lipid, collagen, iodine fractions
3. **Compare**: FAI between healthy and diseased across protocols (expected: HU differences confounded by protocol) vs. water fraction between healthy and diseased across protocols (expected: consistent ~5% difference regardless of protocol)

### 4.5 Expected Results

| Metric | Healthy PCAT | Inflamed PCAT | Difference | Protocol-Independent? |
|---|---|---|---|---|
| FAI (HU) at 80 kV | ~ −85 HU | ~ −75 HU | ~10 HU | ❌ Changes with kV |
| FAI (HU) at 120 kV | ~ −78 HU | ~ −68 HU | ~10 HU | ❌ Different absolute values |
| FAI (HU) at 135 kV | ~ −73 HU | ~ −63 HU | ~10 HU | ❌ Different absolute values |
| **Water fraction (decomposition)** | **~25%** | **~30%** | **~5%** | **✅ Same across all protocols** |

The key demonstration: the same tissue looks different on FAI depending on protocol, but material decomposition gives the same composition regardless. For longitudinal monitoring, inter-scanner comparisons, and multi-site trials, protocol-independent measurement is essential.

---

## 5. Spectral CT and PCAT: Calibration Context

### 5.1 Virtual Monoenergetic Images (VMI)

Spectral CT reconstructions include VMI at user-specified keV. VMI at 70 keV closely matches conventional 120 kVp CT in noise characteristics, but fat HU values shift approximately **+5 to +15 HU** due to energy-dependent attenuation differences. The −70.1 HU FAI threshold has not been validated on VMI data.

### 5.2 Photon-Counting Detector CT (PCD-CT)

PCD-CT (Siemens NAEOTOM Alpha, GE Revolution CT) provides simultaneous multi-energy data:
- VMI at any keV (40–190 keV)
- Material decomposition maps (water, iodine, lipid, calcium)
- Effective atomic number (Z-eff) maps
- Ultra-high resolution mode (0.2 mm pixels)

The Zurich group (Alkadhi, Eberhard, Mergen) has systematically evaluated PCD-CT for coronary imaging and FAI, showing that PCD-CT values are not directly comparable to conventional CT without calibration — further motivating protocol-independent approaches.

### 5.3 DECT Material Decomposition for PCAT

Dual-energy CT enables two-material decomposition (typically water + iodine, or fat + non-fat). For PCAT:
- **Fat fraction map**: each voxel's triglyceride content, independent of beam hardening
- **Iodine map**: contrast enhancement separate from tissue composition
- More specific than single-energy HU, but limited to 2 basis materials

Our approach extends this to **multi-material decomposition** (water + lipid + collagen + iodine), providing greater specificity for characterising the inflammatory phenotypic shift.

---

## 6. PCAT Radiomics: Beyond Mean HU

### 6.1 ShuKun Technology Approach

> Huang et al. 2025, PMID 41163958 — Lesion-specific PCAT radiomics for MACE prediction

ShuKun's commercial pipeline extracts **93 radiomic features** from the PCAT VOI per lesion:

| Feature Class | Count | Examples |
|---|---|---|
| First-order statistics | ~18 | Mean, median, energy, entropy, skewness, kurtosis, percentiles |
| GLCM (co-occurrence matrix) | ~24 | Contrast, correlation, entropy, homogeneity, cluster shade |
| GLSZM (size zone matrix) | ~16 | Small zone emphasis, large zone high grey level emphasis |
| GLRLM (run length matrix) | ~16 | Run length non-uniformity, long run emphasis |
| NGTDM (neighbourhood tone) | ~5 | Coarseness, complexity, busyness |
| GLDM (dependence matrix) | ~14 | Dependence variance, dependence entropy |

ML pipeline: Pearson correlation filtering → Lasso (L1) → XGBoost with 10-fold CV → MACE prediction.

### 6.2 Radiomic Feature Instability

A critical finding from **Wu et al. (2025)** is that **78% of radiomic features change >10%** between different contrast perfusion phases. This means radiomic models trained on one acquisition timing may not generalise to different timing protocols — the same protocol-dependence problem as FAI, but amplified across 93 features.

Material decomposition maps could provide more stable inputs for radiomic analysis, since composition is protocol-independent.

---

## 7. Population Norms and Reference Values

### 7.1 PCAT Reference Values by Vessel

From Ma et al. (2020, Groningen, n=493 consecutive CCTA without known CAD):

| Vessel | Mean FAI (HU) | SD | Range |
|---|---|---|---|
| LAD | −92.4 | ±6.1 | −110 to −75 |
| LCX | −88.4 | ±6.8 | −105 to −70 |
| RCA | −90.2 | ±5.9 | −108 to −72 |

FAI increases linearly with tube voltage. RCA has the most pericoronary fat and the cleanest VOI.

### 7.2 Inflamed vs. Normal Ranges

| Vessel | Normal FAI (HU) | Inflamed FAI (HU) | Risk Threshold |
|---|---|---|---|
| RCA | −85 to −70 | −70 to −40 | **−70.1 HU** (Oikonomou 2018) |
| LAD | −80 to −65 | −65 to −40 | ≈ −72 HU (less validated) |
| LCX | −85 to −70 | −70 to −40 | Similar to RCA (limited data) |

### 7.3 Water-Lipid Composition Reference Values

From Nie & Molloi (2025):

| PCAT State | Water Fraction | Lipid Fraction | Protein Fraction |
|---|---|---|---|
| Healthy | 20–30% | 68–78% | ~2.17% (fixed) |
| Inflamed | 25–35% | 63–73% | ~2.17% (fixed) |
| Difference | ~5% increase | ~5% decrease | Unchanged |

This ~5% water fraction difference is the signal our material decomposition approach aims to detect.

---

## 8. Implications for the MolloiLab Pipeline

### 8.1 Current Pipeline Output

The pipeline produces per-vessel:
- `stats["hu_mean"]`: primary FAI measurement
- `stats["hu_std"]`: FAI variability
- `stats["fat_fraction"]`: fraction of VOI voxels in fat window
- `stats["n_fat_voxels"]`: VOI volume (× voxel volume → cm³)
- Radial HU profile (1 mm rings from vessel outer wall)
- HU histogram: full distribution

### 8.2 Material Decomposition Extension

The current study adds material decomposition output:
- **Water fraction per voxel** → mean water fraction in PCAT VOI
- **Lipid fraction per voxel** → mean lipid fraction in PCAT VOI
- **Collagen fraction per voxel** → structural protein content
- **Iodine fraction per voxel** → contrast contamination detection

These are directly comparable to phantom ground-truth compositions, enabling rigorous validation.

### 8.3 Clinical Decision Pathway

```
CCTA acquired → Material decomposition applied → Water fraction computed per-vessel
        ↓
Water fraction > threshold (e.g., 30%) → Active coronary inflammation
        ↓
Clinical action: Consider colchicine / intensified therapy
        ↓
Advantage: Same threshold works regardless of scanner, kV, kernel, patient size
```

---

## 9. Key References

1. Oikonomou EK et al. *Lancet* 2018;392:929–939. PMID 30170852 — CRISP-CT, FAI methodology, −70.1 HU
2. Antonopoulos AS et al. *Sci Transl Med* 2017 — Histological validation, n=453
3. Oikonomou EK et al. *Nat CV Res* 2023 — CaRi-Heart AI score, ORFAN trial
4. Nie A, Molloi S. *Int J Cardiovasc Imaging* 2025;41:1091–1101 — Water-lipid-protein decomposition for PVAT
5. Ding Y, Molloi S. 2021 — DECT material decomposition for coronary plaque
6. Ma R et al. 2020 — PCAT reference values per vessel per kV
7. Etter M et al. 2022 — Phantom kVp study, PCATMA conversion factors
8. Lisi C et al. 2025 — Kernel/reconstruction effects, up to 33 HU variation
9. Wu C et al. 2025 — Perfusion confounds: 7 HU swing, 78% radiomic instability
10. Sagris M et al. 2022 — Meta-analysis: FAI in unstable vs stable plaques, n=7,797
11. Mendonça PRS, Lamb P. 2014 — Multi-material decomposition framework for DECT
12. Xue Y et al. 2021 — Multi-material decomposition for single-energy CT (sparsity constraint)
13. Valand S et al. 2026 — Truth-based physics-informed material composition in spectral CT
14. Dahal S, Segars WP et al. 2025 — XCAT 3.0, 2500+ phantoms
15. Sauer TJ, Samei E et al. 2024 — Computational coronary plaques via DC-GAN
16. Salinas ML et al. 2025 — Body composition transformation in XCAT phantoms
17. Huang et al. 2025, PMID 41163958 — ShuKun 93-feature PCAT radiomics for MACE
18. Engel et al. *J Clin Med* 2026 — FAI on PCD-CT, plaque vulnerability
