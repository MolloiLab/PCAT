# Literature Review: PCAT Quantification, Material Decomposition, and Coronary CT Imaging

**Project**: PCAT Segmentation Pipeline — MolloiLab  
**Date**: March 2026  
**Purpose**: Comprehensive paper-by-paper literature review organised by topic — covering FAI methodology, technical confounders, material decomposition, XCAT simulation, coronary centerline extraction, and commercial PCAT tools. Synthesised from ~103 papers across two source folders.

---

## 1. FAI Foundational Studies

### 1.1 Antonopoulos et al. 2017 — Histological Validation of FAI

> Antonopoulos AS, Sanna F, Sabharwal N, et al. "Detecting human coronary inflammation by imaging perivascular fat." *Science Translational Medicine*. 2017;9(398):eaal2658.

- **Study**: n=453 cardiac surgery patients with matched CT and perivascular fat biopsies
- **Key finding**: CT attenuation of pericoronary fat directly corresponds to adipocyte lipid content; inflamed vessels have adjacent fat with smaller lipid droplets, reduced PPARγ/FABP4 expression, and increased IL-6/TNF-α
- **Innovation**: First histological proof that FAI reflects genuine biological phenotypic shift, not artifact
- **Clinical relevance**: Established the molecular mechanism underlying FAI — vasocrine signalling from inflamed vessel wall suppresses adipogenesis in adjacent PCAT

### 1.2 Oikonomou et al. 2018 — CRISP-CT (FAI Prognostic Validation)

> Oikonomou EK, Marwan M, Desai MY, et al. *Lancet*. 2018;392(10151):929–939. PMID: 30170852

- **Study**: n=1,872 patients undergoing clinically indicated CCTA; derivation (Erlangen) + validation (Cleveland Clinic) cohorts
- **Key findings**: RCA-FAI independently predicted cardiac death at 5 years (HR 9.04, 95% CI 2.12–38.6); optimal cutoff −70.1 HU by ROC (AUC=0.76)
- **Technical specifications adopted by field**: Fat window −190 to −30 HU; VOI = outer vessel wall + 1× diameter; proximal 40 mm (LAD/LCX), 10–50 mm (RCA)
- **Reproducibility**: ICC 0.987 intra-, 0.980 interobserver
- **Impact**: This paper defined the entire FAI measurement methodology used by essentially all subsequent studies

### 1.3 Oikonomou et al. 2023 — ORFAN Trial / CaRi-Heart

> Oikonomou EK et al. *Nature Cardiovascular Research*. 2023.

- **Study**: n=3,324 prospective CCTA cohort
- **Key findings**: CaRi-Heart AI score (integrating FAI + shape features + calcification) outperformed ASCVD PCE, Synoptic Risk Score, and CACS alone
- **Clinical impact**: Demonstrated AI-enhanced FAI as the strongest non-invasive predictor of MACE in intermediate-risk patients
- **Commercial deployment**: CaRi-Heart by Caristo Diagnostics (Oxford, UK), FDA-cleared

---

## 2. Anti-Inflammatory Trials (Clinical Motivation)

### 2.1 CANTOS — Ridker et al. 2017

> Ridker PM et al. *NEJM* 2017;377:1119–1131. n=10,061.

- Canakinumab (IL-1β antibody) reduced MACE by 15% independent of LDL cholesterol
- First proof of causality for inflammation in cardiovascular events
- Mechanistic pathway: IL-1β → IL-6 → CRP → plaque destabilisation

### 2.2 COLCOT — Tardif et al. 2019

> Tardif JC et al. *NEJM* 2019. n=4,745 post-MI patients.

- Low-dose colchicine (0.5 mg/day) reduced MACE by 23%
- Same NLRP3/IL-1β pathway as canakinumab, but cheaper and safer
- Colchicine now guideline-recommended for secondary prevention

### 2.3 LoDoCo2 — Nidorf et al. 2020

> Nidorf SM et al. *NEJM* 2020. n=5,522 chronic CAD.

- Colchicine reduced MACE by 31% in stable CAD
- Confirmed anti-inflammatory benefit extends beyond acute MI setting
- Together with COLCOT, establishes the treatment pathway that FAI-guided risk stratification enables

---

## 3. FAI Technical Confounders

### 3.1 Tube Voltage Effects

#### Ma et al. 2020 — PCAT Reference Values

> Ma R, Vliegenthart R, et al. Groningen. n=493 consecutive CCTA.

- Established reference values: LAD −92.4 HU, LCX −88.4 HU, RCA −90.2 HU
- **FAI increases linearly with tube voltage** — less negative at higher kV
- Provided first population-based reference ranges stratified by vessel and protocol
- **Relevance to our study**: Demonstrates that absolute HU values are protocol-dependent

#### Etter et al. 2022 — Phantom kVp Study

> Etter M et al. 2022.

- Physical CT phantom study quantifying tube voltage effects on PCAT mean attenuation (PCATMA)
- **Conversion factors relative to 120 kVp**: 1.267 (80 kVp), 1.08 (100 kVp), 0.947 (140 kVp)
- Demonstrates that the same physical fat material gives different HU at different kV settings
- **Relevance**: Directly validates our claim that FAI is protocol-dependent

### 3.2 Reconstruction Algorithm Effects

#### Lisi et al. 2025 — Kernel and Iterative Reconstruction

> Lisi C et al. 2025. n=100.

- Compared FAI across different reconstruction kernels and iterative reconstruction levels
- Found up to **33 HU intra-individual variation** between reconstructions
- Same patient can be classified "inflamed" or "non-inflamed" depending on reconstruction choice
- **Clinical impact**: This is a larger variation than the ~10 HU difference between healthy and inflamed PCAT, making FAI unreliable across reconstruction algorithms

### 3.3 Contrast Perfusion Timing

#### Wu et al. 2025 — Perfusion Confounds

> Wu C, Wilson D, Rajagopalan S, et al. Case Western. n=135 CT perfusion patients.

- **~7 HU swing** in PCAT HU from contrast timing differences alone
- **~15% change in PCAT volume** between perfusion phases
- **78% of radiomic features** change >10% between phases
- **Relevance**: Even within a single scan session, PCAT measurements are confounded by contrast bolus dynamics. Material decomposition separates iodine from tissue composition, eliminating this confound.

### 3.4 Patient Body Habitus

#### Nie & Molloi 2025 — Body Size Effects

> Nie A, Molloi S. *Int J Cardiovasc Imaging* 2025;41:1091–1101.

- **3.6% HU variance** between small, medium, and large patient sizes for identical tissue composition
- **21.9% HU variance** across 80–135 kV
- Beam hardening and scatter increase with body size, shifting HU independently of tissue composition
- **Water fraction (material decomposition) remained consistent** across all sizes and voltages

---

## 4. PCD-CT and Spectral CT Studies

### 4.1 Zurich NAEOTOM Alpha Studies (Alkadhi, Eberhard, Mergen)

Multiple studies from the Zurich group (2022–2025) systematically evaluated PCAT measurement on the Siemens NAEOTOM Alpha photon-counting detector CT:

- PCD-CT produces systematically different HU values than conventional CT for the same tissue
- VMI at 70 keV approximates conventional 120 kVp but is not identical
- Kernel selection on PCD-CT significantly affects FAI
- Ultra-high resolution mode (0.2 mm pixels) improves spatial resolution but affects noise characteristics
- **Conclusion**: FAI thresholds from conventional CT cannot be directly applied to PCD-CT without recalibration

### 4.2 Engel et al. 2026 — FAI on PCD-CT with Plaque Correlation

> Engel et al. *J Clin Med* 2026.

- First study applying the −70.1 HU FAI threshold on PCD-CT
- FAI ≥ −70.1 HU associated with more lipid-rich, non-calcified plaques (vulnerable morphology)
- Confirms FAI signal is biologically meaningful on PCD-CT, but absolute calibration differs from conventional CT

### 4.3 Mannheim PCD-CT Radiomics (Ayx, Froelich, Nörenberg)

> Ayx I et al. 2022–2024. Multiple studies.

- PCD-CT radiomic texture analysis of pericoronary fat
- Spectral imaging enables richer feature extraction (energy-bin-specific textures)
- But also introduces additional variability from energy selection
- **Relevance**: Highlights that more sophisticated measurements amplify the protocol-dependence problem — further motivation for composition-based (material decomposition) approaches

---

## 5. Material Decomposition and Compositional Analysis

### 5.1 Ding & Molloi 2021 — DECT Plaque Material Decomposition

> Ding Y, Molloi S. "Characterization of arterial plaque composition with dual-energy computed tomography." 2021.

- Three-material decomposition (water, lipid, calcium) for coronary artery plaques using DECT
- Validated against known phantom compositions
- Established the lab's methodology for CT material decomposition in coronary structures
- **Direct predecessor** to the PVAT material decomposition work

### 5.2 Nie & Molloi 2025 — PVAT Water-Lipid-Protein Decomposition

> Nie A, Molloi S. *Int J Cardiovasc Imaging* 2025;41:1091–1101.

- Computational simulation of Canon Aquilion One 320-slice scanner
- 10 water-lipid-protein inserts in anthropomorphic thorax phantom (QRM)
- Three-material decomposition: water, lipid, protein (protein fixed at 2.17%)
- **Results**: Water fraction RMSE 0.01–0.64%; RMSD 2.94–6.05%
- **Key demonstration**: Water fraction is protocol-independent (consistent across 80–135 kV and all patient sizes); HU is not (21.9% kV variance, 3.6% size variance)
- Healthy PVAT water fraction 20–30%; diseased 25–35% (~5% difference detectable)
- **Limitations**: FBP only, no bowtie filter, no motion artifacts, cylindrical phantom (not anatomically realistic)

### 5.3 Mendonça & Lamb 2014 — Multi-Material DECT Framework

> Mendonça PRS, Lamb P. "A flexible method for multi-material decomposition of dual-energy CT images." *TMI* 2014.

- Mathematical framework for decomposing DECT data into 3+ materials
- Volume conservation constraint: material fractions sum to 1
- Known material attenuation coefficients (mass attenuation × density) at each energy
- Solve constrained optimization for material fractions per voxel
- **Foundation paper** for multi-material decomposition methodology

### 5.4 Xue et al. 2021 — Single-Energy CT Multi-Material Decomposition

> Xue Y et al. "Multi-material decomposition for single-energy CT using material sparsity constraint." 2021.

- Extended material decomposition to **single-energy CT** — does not require DECT or spectral data
- Exploits material sparsity assumption: most voxels contain ≤ 2–3 dominant materials
- Iterative optimization with L1 regularization on material fractions
- **Relevance**: Enables material decomposition on conventional single-energy CCTA scans (the vast majority of clinical installations), not just spectral CT

### 5.5 Valand et al. 2026 — Physics-Informed Material Composition (Spectral CT)

> Valand S et al. "Truth-based physics-informed material composition estimation in spectral CT." 2026.

- Deep learning approach to material composition estimation
- Uses known phantom compositions as "truth" training targets
- Physics-informed architecture enforces mass attenuation physics in the network
- Achieves higher accuracy than conventional analytical decomposition
- **Relevance**: Represents the next generation of material decomposition methods; applicable to our spectral CT work

---

## 6. XCAT Phantom and Virtual Imaging Trials

### 6.1 XCAT 3.0 — Dahal et al. 2025

> Dahal S, Segars WP, et al. Duke University. 2025.

- **2,500+ unique phantoms** representing population demographics (age, sex, BMI, organ sizes)
- Automated anatomical segmentation framework
- Realistic cardiac anatomy: coronary arteries, epicardial fat, pericardium, myocardium
- Parameterised organs with physiological motion models (cardiac cycle, respiration)
- Gold standard for CT simulation and virtual imaging trials
- **Why critical for our study**: Provides anatomically realistic coronary geometry and pericoronary fat distribution that simple cylindrical phantoms cannot

### 6.2 Sauer et al. 2024 — Computational Coronary Plaques (DC-GAN)

> Sauer TJ, Samei E, et al. Duke CVIT. 2024.

- Generated realistic virtual coronary artery plaques using Deep Convolutional Generative Adversarial Networks (DC-GAN)
- Plaques inserted into XCAT phantoms for virtual imaging trials
- Demonstrated feasibility of simulating coronary pathology in computational phantoms
- **Validates our approach**: If plaques can be computationally inserted, so can inflamed PCAT

### 6.3 Salinas et al. 2025 — Body Composition Transformation

> Salinas ML et al. Duke. 2025.

- Systematic variation of XCAT phantom body composition
- Demonstrated that tissue composition can be parameterised to represent different clinical scenarios
- BMI, organ fat content, and subcutaneous fat distribution can be independently varied
- **Supports our methodology**: Varying PCAT water/lipid content between healthy and diseased states is consistent with established phantom manipulation techniques

---

## 7. Meta-Analyses and Systematic Reviews

### 7.1 Sagris et al. 2022 — FAI in Unstable vs Stable Plaques

> Sagris M et al. 2022. 20 studies, n=7,797.

- FAI significantly higher around unstable (vulnerable) plaques vs stable plaques across all 20 studies
- Confirms FAI signal is robust and reproducible across diverse populations and scanner platforms
- Effect size consistent across study designs (retrospective, prospective, cross-sectional)

### 7.2 Additional Systematic Reviews

Multiple systematic reviews (2020–2025) have consistently confirmed:
- FAI adds incremental prognostic value beyond conventional risk factors
- FAI is reproducible (ICC > 0.95) when protocol is standardised
- FAI is NOT reproducible across protocols (kernel, kV, scanner platform)
- This paradox — excellent reproducibility within protocol, poor reproducibility across protocols — is the core motivation for our material decomposition approach

---

## 8. PCAT Radiomics Studies

### 8.1 ShuKun Technology — Huang et al. 2025

> Huang et al. PMID 41163958. 2025.

- Lesion-specific PCAT radiomics for MACE prediction
- 93 radiomic features per VOI (IBSI-compliant)
- Downstream ML: Pearson filtering → Lasso → XGBoost (10-fold CV)
- Demonstrated that radiomic features outperform single FAI value for MACE prediction
- **Commercial product**: ShuKun "Peri-coronary Adipose Tissue Analysis Tool"

### 8.2 Cedars-Sinai / Monash Group

- Multiple studies (2019–2025) on PCAT radiomics and ML models
- Integration with CT-FFR for functional-anatomical assessment
- Statin effects on PCAT radiomic features (potential for treatment monitoring)

### 8.3 Radiomic Instability Problem

Per Wu et al. (2025): 78% of radiomic features change >10% between perfusion phases. This means:
- Radiomic models trained on one protocol may not generalise
- Feature selection must account for protocol-related variance
- Material decomposition maps could provide more stable radiomic inputs

---

## 9. Coronary Centerline Extraction Algorithms

### 9.1 Rotterdam Benchmark Framework

> Schaap M et al. *Med Image Anal* 2009;13:701–714.

Standardised evaluation metrics: OV (Overlap), OF (Overlap at Forking), OT (Overlap at Tips), AI (Average Interslice distance). Benchmarked 13 algorithms on 32 CTA datasets.

### 9.2 Classical Methods

#### Minimal Path / Fast Marching
- Cohen & Kimmel (1997), Deschamps & Cohen (2001)
- Globally optimal path via wavefront propagation through cost field
- O(n log n) with heap; used in our pipeline (scikit-fmm)

#### Optimally Oriented Flux (OOF) Filter
- Law & Chung, *ECCV* 2008; Jerman et al. 2015
- Flux through spherical surface (vs Hessian eigenvalues in Frangi)
- 2–3× faster than Frangi, better boundary detection
- No maintained Python implementation as of 2026

### 9.3 Deep Learning Methods (2024–2025)

| Method | Architecture | OV | Speed |
|---|---|---|---|
| Zhang et al. (PMID 39888471) | Actor-Critic (continuous RL) | 95.7% | Seconds (GPU) |
| Liu et al. (SPIE 13407) | Dual lightweight 3D CNN | ~95% | 8–15s |
| BEA-CACE (PMID 40751109) | Double-DQN + 3D dilated CNN | — | — |
| CenterlineNet (Rjiba 2020) | Patch-based CNN | — | — |

### 9.4 Speed Comparison

| Method | Speed | Hardware |
|---|---|---|
| Frangi + Fast Marching (ROI-cropped) | ~10–30s | CPU M3 |
| OOF + Fast Marching | ~3–8s | CPU |
| Lightweight CNN | 8–15s | GPU |
| Deep RL | Seconds | GPU |
| Siemens syngo.via Tool #2 | ~208s/case | Clinical |

---

## 10. Commercial PCAT Software

### 10.1 CaRi-Heart (Caristo Diagnostics)

- Oxford methodology commercialised; FDA-cleared
- Implements CRISP-CT specifications exactly
- AI-enhanced: integrates FAI + shape features + calcification into composite risk score
- Deployed in clinical sites (UK NHS, select international)

### 10.2 ShuKun Technology

- Beijing-based; companion to CoronaryDoc®-FFR
- Lesion-specific PCAT (around individual stenoses, not just proximal segments)
- 93-feature radiomic extraction + XGBoost ML pipeline
- Proprietary coronary tree extraction (likely DL-based)

### 10.3 Siemens syngo.via

> Weichsel J et al. *Eur Radiol* 2024. PMID: 38248031

Two generations compared:

| Feature | Tool #1 (v5.0.2) | Tool #2 (DL successor) |
|---|---|---|
| Automation | Semi-automated (manual correction) | Fully automated DL |
| Processing time | ~459 s/case | ~208 s/case (55% faster) |
| Inter-observer variability | 22.8% | 2.3% (10× more reproducible) |

Key insight: DL-based centerline extraction reduces variability 10× and time 55%.

---

## 11. Summary: Papers by Topic

### FAI Definition and Validation

| Paper | Year | n | Key Contribution |
|---|---|---|---|
| Antonopoulos et al. *Sci Transl Med* | 2017 | 453 | Histological validation of FAI |
| Oikonomou et al. *Lancet* (CRISP-CT) | 2018 | 1,872 | FAI prognostic validation, −70.1 HU cutoff |
| Oikonomou et al. *Nat CV Res* (ORFAN) | 2023 | 3,324 | CaRi-Heart AI score |
| Engel et al. *J Clin Med* | 2026 | — | FAI on PCD-CT |

### Anti-Inflammatory Trials

| Paper | Year | n | Key Contribution |
|---|---|---|---|
| Ridker et al. *NEJM* (CANTOS) | 2017 | 10,061 | IL-1β causal role in MACE |
| Tardif et al. *NEJM* (COLCOT) | 2019 | 4,745 | Colchicine −23% MACE post-MI |
| Nidorf et al. *NEJM* (LoDoCo2) | 2020 | 5,522 | Colchicine −31% MACE in chronic CAD |

### FAI Technical Confounders

| Paper | Year | Key Finding |
|---|---|---|
| Ma et al. (Groningen) | 2020 | Reference values, kV-dependent FAI |
| Etter et al. | 2022 | kVp conversion factors for PCATMA |
| Lisi et al. | 2025 | 33 HU variation across kernels |
| Wu et al. (Case Western) | 2025 | 7 HU perfusion timing swing, 78% radiomic instability |
| Nie & Molloi (*IJCI*) | 2025 | 21.9% kV variance, 3.6% body size variance |

### Material Decomposition

| Paper | Year | Key Contribution |
|---|---|---|
| Mendonça & Lamb | 2014 | Multi-material DECT decomposition framework |
| Xue et al. | 2021 | Single-energy CT multi-material decomposition |
| Ding & Molloi | 2021 | DECT coronary plaque decomposition |
| Nie & Molloi (*IJCI*) | 2025 | PVAT water-lipid-protein decomposition |
| Valand et al. | 2026 | Physics-informed DL material composition |

### XCAT and Virtual Imaging

| Paper | Year | Key Contribution |
|---|---|---|
| Dahal et al. (Duke) | 2025 | XCAT 3.0 with 2,500+ phantoms |
| Sauer et al. (Duke CVIT) | 2024 | DC-GAN computational coronary plaques |
| Salinas et al. (Duke) | 2025 | Body composition transformation in XCAT |

### Spectral CT and PCD-CT

| Paper | Year | Key Contribution |
|---|---|---|
| Zurich group (multiple) | 2022–2025 | NAEOTOM Alpha PCAT evaluation |
| Mannheim group (multiple) | 2022–2024 | PCD-CT radiomic texture analysis |
| Engel et al. | 2026 | FAI threshold on PCD-CT |

### PCAT Radiomics and ML

| Paper | Year | Key Contribution |
|---|---|---|
| Huang et al. (ShuKun) PMID 41163958 | 2025 | 93-feature PCAT radiomics for MACE |
| Cedars-Sinai / Monash (multiple) | 2019–2025 | PCAT ML models, statin effects |
| Sagris et al. (meta-analysis) | 2022 | FAI in unstable vs stable plaques, n=7,797 |

### Vasospastic Angina and PVAT

| Paper | Year | Key Contribution |
|---|---|---|
| Ohyama et al. (Tohoku/Sendai) | 2016–2017 | PVAT inflammation in vasospastic angina (18F-FDG PET) |

### Coronary Centerline Extraction

| Paper | Year | Key Contribution |
|---|---|---|
| Schaap et al. *Med Image Anal* | 2009 | Rotterdam benchmark framework |
| Law & Chung *ECCV* | 2008 | OOF filter |
| Zhang et al. PMID 39888471 | 2025 | Deep RL centerline (OV=95.7%) |
| Liu et al. SPIE 13407 | 2025 | Lightweight dual-CNN (8–15s) |
| Zhang et al. PMID 40751109 | 2025 | BEA-CACE double-DQN |

### Commercial Tools

| Paper | Year | Key Contribution |
|---|---|---|
| Weichsel et al. *Eur Radiol* PMID 38248031 | 2024 | Siemens syngo.via DL comparison (10× less variability) |
| CaRi-Heart (Caristo) | 2023 | FDA-cleared AI-enhanced FAI |
| ShuKun PCAT Tool | 2025 | Lesion-specific radiomics + CT-FFR |

---

## 12. Key References (Numbered)

1. Antonopoulos AS et al. *Sci Transl Med* 2017;9:eaal2658 — FAI histological validation
2. Oikonomou EK et al. *Lancet* 2018;392:929–939 — CRISP-CT, FAI definition, −70.1 HU
3. Oikonomou EK et al. *Nat CV Res* 2023 — CaRi-Heart AI score, ORFAN trial
4. Ridker PM et al. *NEJM* 2017;377:1119–1131 — CANTOS (IL-1β → MACE)
5. Tardif JC et al. *NEJM* 2019 — COLCOT (colchicine post-MI)
6. Nidorf SM et al. *NEJM* 2020 — LoDoCo2 (colchicine chronic CAD)
7. Ma R et al. 2020 — PCAT reference values per vessel per kV
8. Etter M et al. 2022 — Phantom kVp conversion factors
9. Lisi C et al. 2025 — Kernel reconstruction effects on FAI (33 HU variation)
10. Wu C et al. 2025 — Perfusion timing confounds (7 HU swing, 78% radiomic instability)
11. Sagris M et al. 2022 — Meta-analysis: FAI unstable vs stable plaques, n=7,797
12. Nie A, Molloi S. *Int J Cardiovasc Imaging* 2025;41:1091–1101 — PVAT water-lipid-protein decomposition
13. Ding Y, Molloi S. 2021 — DECT coronary plaque material decomposition
14. Mendonça PRS, Lamb P. 2014 — Multi-material DECT decomposition framework
15. Xue Y et al. 2021 — Single-energy CT multi-material decomposition
16. Valand S et al. 2026 — Physics-informed material composition in spectral CT
17. Dahal S, Segars WP et al. 2025 — XCAT 3.0 (2,500+ phantoms)
18. Sauer TJ, Samei E et al. 2024 — Computational coronary plaques (DC-GAN)
19. Salinas ML et al. 2025 — Body composition transformation in XCAT
20. Huang et al. PMID 41163958. 2025 — ShuKun 93-feature PCAT radiomics
21. Weichsel J et al. *Eur Radiol* 2024. PMID 38248031 — Siemens syngo.via comparison
22. Schaap M et al. *Med Image Anal* 2009;13:701–714 — Rotterdam centerline benchmark
23. Law MWK, Chung ACS. *ECCV* 2008 — OOF filter
24. Zhang et al. PMID 39888471. 2025 — Deep RL centerline extraction
25. Liu CC et al. SPIE 13407. 2025 — Lightweight CNN centerline
26. Engel et al. *J Clin Med* 2026 — FAI on PCD-CT
27. Ohyama K et al. 2016–2017 — PVAT inflammation in vasospastic angina
28. Ross R. *NEJM* 1999;340:115–126 — Atherosclerosis as inflammatory disease
29. Libby P et al. *Circulation* 2021 — Inflammasome pathway
