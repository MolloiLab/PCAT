# Oxford Translational Cardiovascular Research Group — Pericoronary/Perivascular Adipose Tissue Literature Review

> **PI: Prof. Charalambos Antoniades, MD PhD FRCP FESC**
> BHF Chair of Cardiovascular Medicine, University of Oxford
> Division of Cardiovascular Medicine, Radcliffe Department of Medicine
> Founder & Director, Caristo Diagnostics Ltd.

---

## Table of Contents

- [Research Trajectory Overview](#research-trajectory-overview)
- [Key Investigators & Roles](#key-investigators--roles)
- [Paper Catalogue](#paper-catalogue)
  - [Phase 1: PVAT Biology & Paracrine Signaling (2013–2016)](#phase-1-pvat-biology--paracrine-signaling-20132016)
  - [Phase 2: Conceptual Reviews & Frameworks (2017)](#phase-2-conceptual-reviews--frameworks-2017)
  - [Phase 3: FAI Discovery & CRISP-CT Validation (2017–2018)](#phase-3-fai-discovery--crisp-ct-validation-20172018)
  - [Phase 4: Expansion — Radiomics, Psoriasis, WNT5A (2019)](#phase-4-expansion--radiomics-psoriasis-wnt5a-2019)
  - [Phase 5: Clinical Translation & AI Integration (2020–2023)](#phase-5-clinical-translation--ai-integration-20202023)
  - [Phase 6: Large-Scale Validation & Standardization (2024–2026)](#phase-6-large-scale-validation--standardization-20242026)
- [Patent](#patent)
- [Software & Commercial Translation](#software--commercial-translation)
- [Summary Statistics](#summary-statistics)
- [Journal Impact Factor Reference](#journal-impact-factor-reference)

---

## Research Trajectory Overview

The Oxford group's pericoronary adipose tissue (PCAT) research follows a clear bench-to-bedside trajectory spanning over a decade:

```
2013–2016  PVAT BIOLOGY           Paracrine signaling (adiponectin, PPAR-γ, redox)
    │                              between perivascular fat and vascular wall
    ▼
  2017     LANDMARK DISCOVERY      Fat Attenuation Index (FAI) — Science Transl Med
    │                              CT imaging detects coronary inflammation via PVAT
    ▼
  2018     CLINICAL VALIDATION     CRISP-CT Study — The Lancet
    │                              FAI predicts cardiac mortality in 3,912 patients
    ▼
  2019     EXPANSION               Radiotranscriptomic signature (FRP) — Eur Heart J
    │                              ML-derived radiomic profile; psoriasis as model
    ▼
2020–2023  AI & DEEP LEARNING      Automated EAT quantification, FAI-Score
    │                              standardization, ESC consensus statement
    ▼
2024–2026  LARGE-SCALE REGISTRY    ORFAN — The Lancet (40,091 patients)
                                   Cost-effectiveness; FDA/CE regulatory pathway
```

**Core innovation:** The group discovered that inflamed coronary arteries send paracrine signals that inhibit lipid accumulation in surrounding adipocytes, creating a detectable CT attenuation gradient — the **Fat Attenuation Index (FAI)**. This was extended to a machine learning **Fat Radiomic Profile (FRP)** and eventually standardized as the **FAI-Score** for clinical deployment through Caristo Diagnostics.

---

## Key Investigators & Roles

| Investigator | Role | Key Contributions |
|---|---|---|
| **Charalambos Antoniades** | Principal Investigator, Senior/Corresponding Author on virtually all papers | Conceived FAI concept; leads translational pipeline from biology → imaging → AI → clinical deployment; co-founded Caristo Diagnostics |
| **Alexios S. Antonopoulos** | Core Team — First author on landmark papers | Led the original FAI discovery paper (2017 Sci Transl Med); adiponectin/PVAT biology; systematic reviews |
| **Evangelos K. Oikonomou** | Core Team — First author on CRISP-CT and FRP papers | Led CRISP-CT analysis (2018 Lancet); developed radiotranscriptomic FRP (2019 EHJ); adipose tissue reviews |
| **Keith M. Channon** | Senior Co-Investigator | Oxford Cardiovascular Medicine; vascular biology expertise; co-PI on major grants |
| **Stefan Neubauer** | Senior Co-Investigator | Cardiac MRI/imaging expertise; Oxford Centre for Clinical Magnetic Resonance Research |
| **Cheerag Shirodaria** | Co-Investigator, Co-founder of Caristo | Clinical cardiology; cardiac CT imaging; co-director Caristo Diagnostics |
| **Marios Margaritis** | Early-career researcher | Adiponectin/eNOS signaling (2013 Circulation); PPAR-γ pathway (2016 Circ Res) |
| **Ioannis Akoumianakis** | Early-career researcher | WNT5A/vascular redox biology (2019 Sci Transl Med); PVAT therapeutic targets review |
| **Christos P. Kotanidis** | Postdoctoral researcher | Radiomic analyses; PVAT imaging methodology |
| **Keith W.S. Chan** | Clinical researcher | ORFAN study first author (2024 Lancet); FAI-Score standardization |
| **Hayley W. West** | Postdoctoral researcher | Deep learning EAT segmentation (2023 JACC Cardiovasc Imaging) |
| **Marios Sagris / Spiridon Simantiris** | Collaborators (Athens) | Systematic review & meta-analysis of FAI (2022 EHJ Cardiovasc Imaging) |
| **John Deanfield** | External collaborator (UCL) | Residual inflammatory risk; clinical trial design |
| **Daniel S. Berman / Milind Y. Desai** | External collaborators (Cedars-Sinai / Cleveland Clinic) | US validation cohorts; imaging expertise |

---

## Paper Catalogue

### Phase 1: PVAT Biology & Paracrine Signaling (2013–2016)

These foundational papers established the biological basis for PVAT-vascular cross-talk, demonstrating bidirectional paracrine signaling between perivascular fat and the coronary arterial wall.

| # | Year | Title | Journal (IF) | Citations | Type | Summary |
|---|------|-------|-------------|-----------|------|---------|
| 1 | 2013 | Interactions Between Vascular Wall and Perivascular Adipose Tissue Reveal Novel Roles for Adiponectin in the Regulation of Endothelial Nitric Oxide Synthase Function in Human Vessels | *Circulation* (35.5) | ~321 | Original Research | In 677 CABG patients, demonstrated that PVAT-derived adiponectin restores eNOS coupling via PI3K/Akt phosphorylation and BH4 bioavailability, establishing the **outside-to-inside** paracrine signaling concept. |
| 2 | 2014 | Reciprocal Effects of Systemic Inflammation and Brain Natriuretic Peptide on Adiponectin Biosynthesis in Adipose Tissue of Patients With Ischemic Heart Disease | *Arterioscler Thromb Vasc Biol* (8.4) | — | Original Research | Showed that systemic inflammation suppresses adiponectin biosynthesis in adipose tissue, while BNP upregulates it — linking heart failure neurohormones to adipose tissue biology. |
| 3 | 2015 | Adiponectin as a Link Between Type 2 Diabetes and Vascular NADPH Oxidase Activity in the Human Arterial Wall: The Regulatory Role of Perivascular Adipose Tissue | *Diabetes* (7.7) | ~241 | Original Research | In 386 CABG patients, identified adiponectin as the molecular link between T2D and vascular oxidative stress. T2D impairs PVAT adiponectin secretion, leading to increased NADPH oxidase activity in the arterial wall. |
| 4 | 2016 | Mutual Regulation of Epicardial Adipose Tissue and Myocardial Redox State by PPAR-γ/Adiponectin Signalling | *Circulation Research* (20.1) | ~158 | Original Research | Discovered the **inside-to-outside** signaling axis: myocardial oxidative stress generates 4-HNE that diffuses into epicardial fat, upregulating adiponectin via PPAR-γ — a protective feedback loop. |

**Phase 1 Significance:** Established that PVAT is not inert insulation but an active endocrine organ with bidirectional communication to the vascular wall. This biological foundation underpinned the later insight that inflammation-induced changes in PVAT composition could be detected by imaging.

---

### Phase 2: Conceptual Reviews & Frameworks (2017)

A burst of comprehensive reviews that synthesized the group's biological findings and positioned them within the broader cardiovascular field, setting the stage for the FAI imaging breakthrough.

| # | Year | Title | Journal (IF) | Citations | Type | Summary |
|---|------|-------|-------------|-----------|------|---------|
| 5 | 2017 | The role of epicardial adipose tissue in cardiac biology: classic concepts and emerging roles | *J Physiology* (5.5) | ~162 | Review | Comprehensive review of epicardial fat biology — from embryological origin to its roles in thermogenesis, mechanical protection, metabolic buffering, and paracrine signaling to myocardium. |
| 6 | 2017 | The interplay between adipose tissue and the cardiovascular system: is fat always bad? | *Cardiovascular Research* (10.2) | ~148 | Review | Challenged the dogma that all fat is detrimental; reviewed protective vs. pathological roles of different adipose depots in cardiovascular disease. |
| 7 | 2017 | 'Dysfunctional' adipose tissue in cardiovascular disease: a reprogrammable target or an innocent bystander? | *Br J Pharmacol* (7.3) | — | Review | Reviewed the concept of adipose tissue "dysfunction" and its potential as a therapeutic target through reprogramming of adipocyte phenotype. |
| 8 | 2017 | Perivascular adipose tissue as a regulator of vascular disease pathogenesis: identifying novel therapeutic targets | *Br J Pharmacol* (7.3) | ~73 | Review | Synthesized evidence on bidirectional PVAT-vascular signaling (adipokines, chemokines, ROS) and identified therapeutic targets within this cross-talk. |
| 9 | 2017 | Unravelling the adiponectin paradox: novel roles of adiponectin in the regulation of cardiovascular disease | *Br J Pharmacol* (7.3) | ~134 | Review | Addressed the "adiponectin paradox" (high levels associated with poor outcomes in HF) and proposed context-dependent roles of adiponectin in cardiovascular disease. |

---

### Phase 3: FAI Discovery & CRISP-CT Validation (2017–2018)

The two landmark papers that defined the field: the discovery of FAI and its clinical validation for cardiac mortality prediction.

| # | Year | Title | Journal (IF) | Citations | Type | Summary |
|---|------|-------|-------------|-----------|------|---------|
| **10** | **2017** | **Detecting human coronary inflammation by imaging perivascular fat** | ***Science Transl Med*** **(17.1)** | **~872** | **Original Research** | **THE FOUNDATIONAL PAPER.** Developed FAI from 453 cardiac surgery patients. Showed inflamed vessels send cytokines that inhibit lipid accumulation in PVAT preadipocytes, creating a 3D CT attenuation gradient. FAI validated in 273 CTA subjects — detects subclinical CAD, dynamic inflammation changes, and vulnerable plaques in ACS. |
| **11** | **2018** | **Non-invasive detection of coronary inflammation using computed tomography and prediction of residual cardiovascular risk (the CRISP CT study)** | ***The Lancet*** **(168.9)** | **~838** | **Original Research** | **CLINICAL VALIDATION.** Post-hoc analysis of 3,912 patients from Erlangen (Germany) and Cleveland (USA). Perivascular FAI around RCA with cutoff ≥ −70.1 HU independently predicted all-cause and cardiac mortality beyond traditional risk factors and calcium scoring. Established FAI as a prognostic biomarker. |
| 12 | 2018 | The role of adipose tissue in cardiovascular health and disease | *Nature Reviews Cardiology* (41.7) | ~396 | Review | Definitive review covering adipose depot biology, the obesity paradox, PVAT-cardiovascular cross-talk, and the emerging clinical potential of FAI as a biomarker. |
| 13 | 2018 | Perivascular adipose tissue and coronary atherosclerosis | *Heart* (5.0) | ~113 | Review | Focused review on PCAT's role in coronary atherosclerosis and how FAI captures inflammation-induced changes in adipocyte lipid content. |

---

### Phase 4: Expansion — Radiomics, Psoriasis, WNT5A (2019)

Extended FAI into machine learning radiomics, demonstrated its utility in systemic inflammatory disease (psoriasis), and continued uncovering PVAT biology.

| # | Year | Title | Journal (IF) | Citations | Type | Summary |
|---|------|-------|-------------|-----------|------|---------|
| **14** | **2019** | **A novel machine learning-derived radiotranscriptomic signature of perivascular fat improves cardiac risk prediction using coronary CT angiography** | ***European Heart J*** **(39.3)** | **~400** | **Original Research** | **ML BREAKTHROUGH.** Introduced the Fat Radiomic Profile (FRP) — 1,391 radiomic features trained against histological ground truth (fibrosis, microvascular density). FRP captures chronic PVAT remodeling beyond acute inflammation (FAI alone). Validated in SCOT-HEART cohort. |
| 15 | 2019 | Association of Biologic Therapy With Coronary Inflammation in Patients With Psoriasis as Assessed by Perivascular Fat Attenuation Index | *JAMA Cardiology* (14.8) | ~197 | Original Research | Used FAI to show that biologic therapy (anti-TNF/anti-IL-17) reduces coronary inflammation in psoriasis patients — first demonstration of FAI as a treatment-response biomarker. |
| 16 | 2019 | Imaging residual inflammatory cardiovascular risk | *European Heart J* (39.3) | ~145 | Review | Positioned FAI within the "residual inflammatory risk" framework — patients on optimal therapy who remain at elevated risk due to undetected coronary inflammation. |
| 17 | 2019 | Atherosclerosis affecting fat: What can we learn by imaging perivascular adipose tissue? | *J Cardiovasc Computed Tomography* (3.3) | ~102 | State-of-the-Art Review | Comprehensive review of how atherosclerosis alters PVAT composition and how CT imaging can detect these changes. Reviews FAI methodology and prognostic evidence. |
| 18 | 2019 | Computed Tomography: Assessment of Coronary Inflammation and Other Plaque Features | *Arterioscler Thromb Vasc Biol* (8.4) | ~35 | Review | Technical review of CT-based coronary inflammation assessment including FAI, high-risk plaque features, and emerging plaque characterization methods. |
| 19 | 2019 | Detecting Coronary Inflammation With Perivascular Fat Attenuation Imaging: Making Sense From Perivascular Attenuation Maps | *JACC Cardiovasc Imaging* (12.8) | ~33 | Editorial | Editorial discussing the interpretation of perivascular attenuation maps and how FAI translates biological signals into clinically actionable information. |
| 20 | 2019 | Adipose tissue-derived WNT5A regulates vascular redox signaling in obesity via USP17/RAC1-mediated activation of NADPH oxidases | *Science Transl Med* (17.1) | — | Original Research | In 1,004 patients, identified WNT5A as a key PVAT-derived adipokine in obesity that activates vascular NADPH oxidase via USP17/RAC1 pathway. WNT5A independently associated with calcified plaque progression. |

---

### Phase 5: Clinical Translation & AI Integration (2020–2023)

Transition from research biomarker to clinical-grade tool: FAI-Score standardization, deep learning automation, AI-Risk integration, and ESC consensus endorsement.

| # | Year | Title | Journal (IF) | Citations | Type | Summary |
|---|------|-------|-------------|-----------|------|---------|
| 21 | 2020 | Perivascular Fat Attenuation Index Stratifies Cardiac Risk Associated With High-Risk Plaques in the CRISP-CT Study | *JACC* (21.7) | ~87 | Original Research (Letter) | Demonstrated FAI provides **incremental** risk stratification when combined with high-risk plaque (HRP) features. Patients with high FAI + HRP had 7.3× higher cardiac mortality vs. low FAI + no HRP. |
| 22 | 2020 | Artificial intelligence in medical imaging: A radiomic guide to precision phenotyping of cardiovascular disease | *Cardiovascular Research* (10.2) | ~77 | Review | Comprehensive review of AI/radiomics in cardiovascular CT imaging — covers radiomic feature extraction, ML classifiers, and clinical applications including PVAT analysis. |
| 23 | 2021 | Assessing Cardiovascular Risk by Using the Fat Attenuation Index in Coronary CT Angiography | *Radiol: Cardiothoracic Imaging* (4.5) | ~62 | Review | Practical review of FAI methodology, biological basis, clinical validation studies (CRISP-CT, SCOT-HEART), and integration into the AI-Risk classifier. |
| 24 | 2021 | Standardized measurement of coronary inflammation using cardiovascular computed tomography: integration in clinical care as a prognostic medical device | *Cardiovascular Research* (10.2) | ~33 | Original Research | Described the technical pipeline for standardizing FAI measurement across different CT scanners and protocols — the foundation for the CaRi-Heart medical device. |
| 25 | 2021 | Perivascular fat imaging by computed tomography (CT): a virtual guide | *Br J Pharmacol* (7.3) | ~38 | Review / Technical Guide | Practical guide to PVAT imaging by CT — covers acquisition protocols, segmentation methods, measurement standardization, and pitfalls. |
| 26 | 2022 | Pericoronary fat attenuation index — a new imaging biomarker and its diagnostic and prognostic utility: a systematic review and meta-analysis | *EHJ Cardiovasc Imaging* (6.2) | — | Systematic Review & Meta-Analysis | Meta-analysis of 20 studies (7,797 patients). FAI significantly higher around culprit lesions (MD = 4.50 HU) and predictive of MACE (HR = 3.29, 95% CI: 1.88–5.76). |
| 27 | 2022 | Pericardial adiposity is independently linked to adverse cardiovascular phenotypes: a CMR study of 42,598 UK Biobank participants | *EHJ Cardiovasc Imaging* (6.2) | ~22 | Original Research | Large UK Biobank CMR study showing pericardial fat volume independently associated with adverse cardiac remodeling, atrial fibrillation, and heart failure. |
| 28 | 2023 | Deep-Learning for Epicardial Adipose Tissue Assessment With Computed Tomography: Implications for Cardiovascular Risk Prediction | *JACC Cardiovasc Imaging* (12.8) | ~77 | Original Research | Deep learning network for automated EAT quantification from CCTA (trained on 3,720 ORFAN scans). AI-derived EAT volume and attenuation independently predicted all-cause mortality and MACE. |
| 29 | 2023 | Role of Human Epicardial Adipose Tissue-Derived miR-92a-3p in Myocardial Redox State | *JACC* (21.7) | ~19 | Original Research | Identified miR-92a-3p as an EAT-derived microRNA that modulates myocardial oxidative stress — a new molecular mediator in the fat-heart cross-talk. |
| 30 | 2023 | Perivascular adipose tissue as a source of therapeutic targets and clinical biomarkers (ESC Working Group Consensus Statement) | *European Heart J* (39.3) | — | Consensus Statement | **ESC-endorsed** consensus standardizing PVAT definitions, reviewing biology, and evaluating FAI/FRP as clinical biomarkers. Framework for PVAT-targeted therapeutics. |

---

### Phase 6: Large-Scale Validation & Standardization (2024–2026)

Culmination: world's largest CT registry validation, health economics, and regulatory-grade standardization.

| # | Year | Title | Journal (IF) | Citations | Type | Summary |
|---|------|-------|-------------|-----------|------|---------|
| **31** | **2024** | **Inflammatory risk and cardiovascular events in patients without obstructive coronary artery disease: the ORFAN multicentre cohort study** | ***The Lancet*** **(168.9)** | — | **Original Research** | **LARGEST VALIDATION.** 40,091 patients from the ORFAN registry. FAI-Score and AI-Risk independently predict MACE even in patients without obstructive CAD. High FAI-Score = 9.5× cardiac mortality risk in patients with minimal plaque. Changed management in 45% of patients. |
| 32 | 2024 | Using artificial intelligence to study atherosclerosis from computed tomography imaging: A state-of-the-art review | *Atherosclerosis* (5.3) | — | Review | Comprehensive review of AI applications in coronary CT — plaque characterization, PVAT analysis, risk prediction, and clinical integration. |
| 33 | 2025 | FAI-Score: A robust measure of coronary inflammation independent of technical scan parameters | — | — | Original Research | Demonstrated FAI-Score's robustness across different CT scanners, acquisition protocols, and reconstruction kernels — critical for multi-center clinical deployment. |
| 34 | 2025 | Pericoronary Adipose Tissue Imaging and the Need for Standardized Measurement of Coronary Inflammation: Translating PCAT Attenuation Gradients Into FAI Score for Clinical Use | *JACC Cardiovasc Imaging* (12.8) | — | Editorial | Discusses the necessity of converting raw PCAT attenuation into the standardized FAI-Score (adjusted for scanner, anatomy, demographics) for reproducible clinical use. |
| 35 | 2025 | Cost-effectiveness of a novel AI technology to quantify coronary inflammation and cardiovascular risk in patients undergoing routine CCTA | *EHJ Quality of Care and Clinical Outcomes* (4.6) | — | Original Research (Health Economics) | Markov decision-analytic model (3,393 patients). AI-guided strategy cost-effective at ICER £1,371–3,244. Predicted 11% reduction in MI, 12% reduction in cardiac death through better-targeted prevention. |
| 36 | 2026 | Imaging and Quantification of Perivascular Adipose Tissue | *Arterioscler Thromb Vasc Biol* (8.4) | — | Review | Latest review on PVAT imaging and quantification methods across modalities. |

---

## Patent

| Patent | Title | Inventors | Filed | Granted | Licensee |
|--------|-------|-----------|-------|---------|----------|
| **US 10,695,023 B2** | Methods for detecting coronary inflammation by analysis of perivascular adipose tissue | Charalambos Antoniades et al. | 2017 | June 30, 2020 | Caristo Diagnostics (exclusive license) |

**Related patent applications:** PCT/GB2017/053262, GB2018/1818049.7, GR20180100490, GR20180100510

The patent covers:
- The Fat Attenuation Index (FAI) measurement methodology
- Radiotranscriptomic profiling of perivascular adipose tissue
- Methods for non-invasive detection of coronary inflammation from CT images

---

## Software & Commercial Translation

### Caristo Diagnostics Ltd.

- **Founded:** Spin-out from University of Oxford
- **Founders:** Charalambos Antoniades, Cheerag Shirodaria
- **Website:** [caristo.com](https://www.caristo.com)

### Products

| Product | Function | Regulatory Status |
|---------|----------|-------------------|
| **CaRi-Heart** (FAI-Score) | Measures coronary inflammation from routine CCTA by computing standardized FAI-Score for each coronary artery. Integrates with AI-Risk classifier for personalized cardiac mortality prediction. | CE Mark (MDR, CE2797), UKCA, Australia. **Investigational use only in the US** (FDA pending). |
| **CaRi-Plaque** | Automated coronary plaque and stenosis quantification | CE Mark, UKCA, **FDA 510(k) cleared** (K242240, 2025) |
| **AI-Risk Classifier** | Integrates FAI-Score + plaque burden + clinical factors into an individualized cardiac risk score | Part of CaRi-Heart platform |

### Key Milestones
- **2017:** FAI concept published (Science Translational Medicine)
- **2018:** CRISP-CT clinical validation (The Lancet)
- **2019:** Fat Radiomic Profile (FRP) developed (European Heart Journal)
- **2020:** US Patent granted (US 10,695,023)
- **2021:** CE Mark certification; CaRi-Heart standardized measurement published
- **2022:** UKCA marking; NHS pilot deployment
- **2023:** ESC Working Group consensus statement endorsing PVAT biomarkers
- **2024:** ORFAN registry (40,091 patients) published in The Lancet
- **2025:** CaRi-Plaque FDA cleared; cost-effectiveness demonstrated; FAI-Score robustness validated

### Clinical Impact
- FAI-Score showed **20× increased risk** of cardiac mortality for high-inflammation patients
- Among patients with minimal/no plaque: **9.5× cardiac mortality risk**, **5.5× MACE risk**
- AI-Risk classification **changed management decisions in 45%** of patients
- Cost-effective at conventional willingness-to-pay thresholds (ICER £1,371–3,244)

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total papers in collection | 36 |
| Original research articles | 19 |
| Review articles | 12 |
| Consensus statements | 1 |
| Systematic reviews / meta-analyses | 1 |
| Editorials / commentaries | 2 |
| Health economics | 1 |
| Patents | 1 |
| Software products | 3 (CaRi-Heart, CaRi-Plaque, AI-Risk) |

### Publication Venues (by frequency)
- European Heart Journal (×4)
- JACC / JACC Cardiovasc Imaging (×5)
- British Journal of Pharmacology (×4)
- The Lancet (×2)
- Science Translational Medicine (×2)
- Circulation / Circ Research / Circ Cardiovasc Imaging (×3)
- Cardiovascular Research (×3)
- Others (×13)

### Top-Cited Papers
1. **Antonopoulos et al. 2017** — *Sci Transl Med* — **~872 citations** (FAI discovery)
2. **Oikonomou et al. 2018** — *The Lancet* — **~838 citations** (CRISP-CT)
3. **Oikonomou et al. 2019** — *Eur Heart J* — **~400 citations** (Radiotranscriptomic FRP)
4. **Oikonomou & Antoniades 2018** — *Nat Rev Cardiol* — **~396 citations** (Adipose tissue review)
5. **Margaritis et al. 2013** — *Circulation* — **~321 citations** (Adiponectin/eNOS)

---

## Journal Impact Factor Reference

| Journal | IF (2024) |
|---------|-----------|
| The Lancet | 168.9 |
| Nature Reviews Cardiology | 41.7 |
| European Heart Journal | 39.3 |
| Circulation | 35.5 |
| JACC | 21.7 |
| Science Translational Medicine | 17.1 |
| JAMA Cardiology | 14.8 |
| JACC: Cardiovascular Imaging | 12.8 |
| Circulation Research | 20.1 |
| Cardiovascular Research | 10.2 |
| Arterioscler Thromb Vasc Biol | 8.4 |
| Diabetes | 7.7 |
| British Journal of Pharmacology | 7.3 |
| EHJ Cardiovasc Imaging | 6.2 |
| J Physiology | 5.5 |
| Atherosclerosis | 5.3 |
| Heart | 5.0 |
| EHJ Quality of Care | 4.6 |
| Radiol: Cardiothoracic Imaging | 4.5 |
| J Cardiovasc Computed Tomography | 3.3 |

---

*Last updated: March 11, 2026*
*Citation counts from Semantic Scholar (approximate, as of early 2026)*
