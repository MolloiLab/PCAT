# Clinical Study Design Guidance for PCAT Material Decomposition

**Project**: PCAT — MolloiLab, University of California, Irvine  
**Author**: Shu Nie  
**Date**: March 2026  
**Purpose**: How the field defines "healthy" vs. "diseased" PCAT, how "culprit" lesions are identified, and practical guidance for designing a **retrospective** clinical validation study using existing PCCT CCTA scans with material decomposition — including the control group problem, group selection strategies, inclusion/exclusion criteria, and study design templates.

---

## Table of Contents

**Part I — How the Field Defines Groups**

- [1. Three Strategies for Defining "Healthy vs. Diseased"](#1-three-strategies-for-defining-healthy-vs-diseased)
- [2. How "Culprit Lesion" is Operationally Defined](#2-how-culprit-lesion-is-operationally-defined)
- [3. Why This Matters for the Simulation Study](#3-why-this-matters-for-the-simulation-study)
- [4. Comparison Table: Definitions Across Study Types](#4-comparison-table-definitions-across-study-types)

**Part II — Designing Your Clinical Study**

- [5. The Control Group Problem in CCTA](#5-the-control-group-problem-in-ccta)
- [6. Five Group Selection Strategies](#6-five-group-selection-strategies)
- [7. Standard Inclusion and Exclusion Criteria](#7-standard-inclusion-and-exclusion-criteria)
- [8. Recommended Design for PCCT Material Decomposition Study](#8-recommended-design-for-pcct-material-decomposition-study)

---

# Part I — How the Field Defines Groups

## 1. Three Strategies for Defining "Healthy vs. Diseased"

Every clinical PCAT study must define what counts as "inflamed" and what counts as "healthy." There are three fundamentally different strategies used in the literature, and **none of them use known tissue composition as ground truth.** This is the gap the simulation study fills.

### 1.1 Strategy 1: Within-Patient, Vessel-Level Comparison (Most Common)

Compare PCAT around a "culprit" coronary lesion vs. a "non-culprit" segment **in the same patient**. The logic: the culprit caused the event, so the fat around it should be more inflamed than fat around a non-culprit vessel.

| Study | Population | How "culprit" was defined | Key finding |
|---|---|---|---|
| Li et al. 2025 (*J Comput Assist Tomogr*, n=120) | 80 ACS + 40 stable CAD | Invasive coronary angiography (ICA) — lesion causing the clinical event | FAI higher around culprit plaques than non-culprit; effect modified by stenosis severity |
| Yang et al. 2025 (*Eur J Radiol Open*, n=230) | NSTEMI patients | ICA — lesion responsible for the index NSTEMI event | FAI at culprit lesion ("FAIlesion") higher than non-culprit; proposed lesion-level FAI as better discriminator |
| Sagris et al. 2022 (meta-analysis, n=7,797) | 20 studies pooled | Varied — each study used its own culprit definition | FAI consistently higher around unstable vs. stable plaques |

**Limitation**: "Culprit" is defined by clinical presentation and angiography, not by tissue biology. A culprit lesion is one that caused symptoms — this is a clinical endpoint, not a direct measurement of inflammation. Two lesions with identical tissue composition could be classified differently depending on which one ruptured first.

### 1.2 Strategy 2: Outcome-Based Retrospective Stratification

Enrol a large cohort of CCTA patients, measure FAI at baseline, follow them for years, then retrospectively stratify by who had cardiovascular events (MACE/cardiac death) and who did not.

| Study | Population | Follow-up | How "diseased" was defined | Key finding |
|---|---|---|---|---|
| CRISP-CT (Oikonomou 2018, n=1,872) | CCTA patients | 5 years | Cardiac death or MACE during follow-up | FAI > −70.1 HU → HR 9.04 for cardiac death |
| ORFAN (Chan 2024, n=40,091) | CCTA patients | 2.7–7.7 years | All-cause mortality, cardiac death | 3 inflamed arteries vs. none → HR 29.8 |

**Limitation**: "Diseased" is defined **retrospectively by outcome**, not by a pre-defined biological state. Patients who had events are labelled "diseased" — but the inflammation that caused their event may have resolved, progressed, or been unrelated to PCAT. There is no tissue-level confirmation that FAI was measuring inflammation rather than some other process.

### 1.3 Strategy 3: Histological Ground Truth

Two studies have used histological examination as ground truth for FAI validation — one in surgical patients and one post-mortem.

| Study | Population | How "inflamed" was defined | Key findings |
|---|---|---|---|
| Antonopoulos et al. 2017 (*Sci Transl Med*, n=453) | Cardiac surgery patients | Histology — PPARγ expression, lipid droplet size, IL-6/TNF-α levels, UCP1 expression | Inflamed fat: reduced PPARγ (−2.3-fold), reduced FABP4 (−1.8-fold), increased IL-6 (+3.1-fold), increased TNF-α (+2.7-fold), smaller lipid droplets. HU correlated with these markers. |
| Ocana et al. 2025 (*Int J Cardiol*, n=35) | Post-mortem — sudden cardiac death from ACS | Histology of fatal culprit plaques — intraplaque inflammation, adventitial inflammation, vasa vasorum density | FAI higher at culprit vs. control vessels (−62.5 vs. −68.5 HU, p=0.003). **However, within culprit lesions, FAI did NOT distinguish those with vs. without local histopathological inflammation (p=0.378).** Napkin-ring sign (p=0.049) and plaque enhancement (p=0.024) were better associated with histological inflammation than FAI. |

**Antonopoulos 2017 limitation**: Surgical population (severe disease, often multivessel), not representative of the broader CCTA population. The biopsy is epicardial fat near the aortic root, not precisely the same pericoronary fat measured by FAI. Sample handling may alter tissue properties.

**Ocana 2025 limitation**: Post-mortem population — hemodynamic changes after death may alter tissue properties. Small sample (n=35). Post-mortem CT angiography (MPMCTA), not clinical CCTA. However, the key finding — that FAI distinguishes culprit from non-culprit vessels but cannot distinguish inflamed from non-inflamed culprit lesions — suggests FAI may be a marker of plaque vulnerability rather than a specific inflammation measurement.

**Why Ocana 2025 matters for your study**: This is the strongest evidence that FAI measures *something* related to high-risk disease but may NOT be specifically measuring inflammation at the tissue level. Material decomposition, by measuring actual tissue composition, could potentially discriminate what FAI cannot.

---

## 2. How "Culprit Lesion" is Operationally Defined

Since Strategy 1 (within-patient comparison) is the most common study design, the definition of "culprit" matters enormously. In practice, studies use a hierarchy of criteria:

**Gold standard — Invasive Coronary Angiography (ICA):**
- The lesion that caused the acute coronary syndrome (ACS)
- Identified by: angiographic appearance (thrombus, abrupt vessel cutoff, TIMI flow grade 0–1) combined with clinical presentation (chest pain, ST-segment changes on ECG, troponin elevation)
- In practice: interventional cardiologist identifies the culprit during the emergent catheterisation

**CT-based high-risk plaque features (used when ICA is not available):**

| Feature | Criterion | What it indicates |
|---|---|---|
| Positive remodeling | Remodeling index (RI) > 1.1 | Outward vessel expansion accommodating plaque growth |
| Low-attenuation plaque (LAP) | Plaque attenuation < 30 HU | Lipid-rich necrotic core |
| Spotty calcification | Calcification < 3 mm within plaque | Micro-calcification (inflammatory marker) |
| Napkin-ring sign | Low-attenuation core with higher-attenuation rim | Thin-cap fibroatheroma (TCFA) on CT |

**SCOT-HEART finding**: LAP burden > 4% → 5-fold MI risk (HR 4.65). This threshold may be useful for identifying high-risk segments in CCTA-only cohorts.

**Intravascular imaging (OCT/IVUS) — rarely used for PCAT studies but important to know:**
- **TCFA (thin-cap fibroatheroma)**: Cap thickness < 65 μm AND lipid arc > 90° (OCT)
- **Plaque rupture**: Cap discontinuity visible in ≥ 2 consecutive OCT frames
- **IVUS**: Plaque burden, necrotic core area, minimum lumen area

---

## 3. Why This Matters for the Simulation Study

**No previous study defines "inflamed" vs. "healthy" by actual tissue composition.** Every clinical study defines "diseased" by:
- Clinical outcome (who had a heart attack → therefore "inflamed")
- Angiographic appearance (which lesion looks culprit → therefore "inflamed" around it)
- Histology (only Antonopoulos 2017, surgical population only)

**The simulation study is unique because it defines inflammation AT THE COMPOSITIONAL LEVEL.** The exact water/lipid fractions of healthy vs. inflamed PCAT are set, giving something no clinical study has: **known ground truth tissue composition.**

This is a strength, not a limitation. Use it in the discussion:

> "A fundamental challenge in validating CT-based PCAT measurements is the absence of compositional ground truth. Clinical studies define 'inflamed' pericoronary fat by clinical endpoints (ACS presentation, cardiovascular events) or invasive imaging (angiographic culprit identification), not by measured tissue composition. Consequently, the relationship between FAI and actual tissue water/lipid content remains incompletely characterised. Simulation provides the essential controlled conditions in which the tissue composition is known exactly, enabling direct evaluation of whether a given measurement can detect composition differences of clinical relevance."

---

## 4. Comparison Table: Definitions Across Study Types

| Criterion | Strategy 1 (Within-patient) | Strategy 2 (Outcome-based) | Strategy 3 (Histology) | **Simulation Study** |
|---|---|---|---|---|
| What defines "diseased"? | Culprit lesion (ICA/clinical) | Cardiac event (MACE/death) | Histological markers (PPARγ, IL-6) | **Known tissue composition (water/lipid fractions)** |
| Ground truth type | Clinical endpoint | Clinical endpoint | Biological endpoint | **Compositional ground truth** |
| Within-patient control? | Yes (non-culprit vessel) | No (between-patient) | Partial (adjacent tissue / contralateral vessel) | **Yes (same phantom, different composition)** |
| Protocol standardised? | Single-centre protocol | Multi-centre, variable | Single-centre | **Systematically varied** |
| Can confirm what FAI measures? | No — circular (FAI validates FAI) | No — correlation, not mechanism | Partially — Antonopoulos: HU correlates with histological markers; Ocana: FAI distinguishes culprit vessels but NOT inflamed vs. non-inflamed culprit lesions | **Yes — known input vs. measured output** |
| Limitations | Culprit ≠ most inflamed; just the one that ruptured | Reverse causation; confounders | Surgical / post-mortem populations; biopsy location; small samples | Simulation; not clinical |

---

# Part II — Designing Your Clinical Study

## 5. The Control Group Problem in CCTA

**The fundamental problem**: Truly healthy people don't get CCTA. Every patient referred for CCTA has symptoms (chest pain, dyspnoea) or risk factors (diabetes, family history, abnormal stress test). This means every "control" in CCTA research is someone who was sick enough to warrant imaging but happened to have clean coronaries.

**How the field handles it**: Nobody uses truly healthy controls. Instead, studies define a spectrum from "lowest-risk within the referred population" to "highest-risk," and compare endpoints of that spectrum. The terminology matters:

| Term used | What it actually means | Who is excluded |
|---|---|---|
| "Healthy controls" | CAD-RADS 0, no visible plaque | Anyone with plaque, but they still had symptoms |
| "Normal coronaries" | No stenosis ≥ 25%, calcium score 0 | Detectable atherosclerosis, but subclinical disease may exist |
| "Low-risk" | Non-obstructive CAD (< 50% stenosis) | Obstructive disease, but early atherosclerosis is present |
| "Stable CAD" | Known disease, no recent ACS event | ACS patients, but chronic inflammation may be ongoing |

**Key insight**: The label "healthy" in CCTA research is always relative. Studies that claim "healthy controls" are using patients who had clinical indications for imaging but no detectable disease on that specific scan. Acknowledge this explicitly in your methods.

### How Specific Studies Define "No Disease"

| Study | "Clean" definition | Criteria |
|---|---|---|
| Ma et al. 2020 (reference values) | Calcium score 0 + no plaque on CCTA | Excluded anomalous coronary origin |
| Boussoussou et al. 2023 | Calcium score 0 | n=1,652 from routine CCTA referrals |
| Kahmann et al. 2024 (PCCT radiomics) | No CAD on PCCT | 18 patients matched by age/sex/risk to 18 with CAD |
| Varga-Szemes 2021 (PCCT phantom + in vivo) | Agatston score < 60 | Low-to-intermediate pretest probability per guidelines |
| Xu et al. 2024 (PCAT in non-CHD) | No coronary heart disease | n=785, still had clinical indication for CCTA |

---

## 6. Five Group Selection Strategies

### Strategy A: Within-Patient Vessel Comparison (Strongest)

Compare different **vessels** in the **same patient**. One vessel has disease, another doesn't. Each patient is their own control.

| Precedent | Design | n |
|---|---|---|
| Li et al. 2025 | Culprit vessel FAI vs. non-culprit vessel FAI in ACS patients | 80 ACS + 40 stable |
| Yang et al. 2025 | FAI_lesion at culprit vs. non-culprit in NSTEMI | 230 |

**Strengths**: Eliminates ALL inter-patient confounders (BMI, age, medication, scanner, contrast timing). The cleanest possible comparison — same scan, same patient, different vessel.

**Limitation**: Requires patients with single-vessel or dominant-vessel disease. Patients with diffuse multivessel disease don't have a "clean" vessel for comparison.

**For your PCCT study**: Material decomposition of PCAT around the diseased vessel vs. the clean vessel, same patient, same scan. Show water fraction differs between vessels.

### Strategy B: CAD-RADS 0 vs. High-Risk Plaque (Between-Patient)

Split the cohort by disease burden on CCTA.

| Group | Definition | Typical criteria |
|---|---|---|
| **"Pseudo-healthy"** | CAD-RADS 0 | No visible plaque, no stenosis, ± calcium score 0 |
| **"Diseased"** | CAD-RADS 3–5 | ≥ 50% stenosis, OR high-risk plaque features (≥ 2 of: positive remodeling, LAP < 30 HU, spotty calcification, napkin-ring sign) |

**Precedent**: Chen et al. 2021 (dual-layer spectral CT) used high-risk plaque features (≥ 2 features) to define "diseased" group for PCAT comparison. This is the closest published design to what you'd do with PCCT material decomposition.

**Matching**: Must match groups by age, sex, BMI, and cardiovascular risk factors (hypertension, diabetes, smoking, statin use). Propensity matching preferred.

### Strategy C: ACS vs. Stable CAD (Clinical Presentation)

| Group | Definition |
|---|---|
| **"Diseased"** | ACS patients (STEMI, NSTEMI, unstable angina) |
| **"Control"** | Stable angina or stable CAD, matched by age/sex/BMI |

**Precedent**: Kuneman et al. 2023 — 66 ACS patients vs. 132 stable CAD patients, 1:2 propensity-matched for age, sex, cardiac risk factors.

**Limitation**: Stable CAD patients still have disease — they're not "healthy." This compares acute inflammation (ACS) vs. chronic/quiescent disease, not inflamed vs. uninflamed.

### Strategy D: Plaque Feature Stratification (No "Healthy" Group Needed)

Don't split by patient — split by **plaque characteristics**:

| Group | Definition |
|---|---|
| **High-risk plaque** | ≥ 2 of: positive remodeling (RI > 1.1), LAP (< 30 HU), spotty calcification (< 3 mm), napkin-ring sign |
| **Non-high-risk plaque** | Plaque present but no high-risk features |

**Precedent**: Chen et al. 2021 (dual-layer spectral detector CT, n=104). Compared PCAT spectral features between high-risk vs. non-high-risk plaque groups.

**Strength**: Sidesteps the "no healthy controls" problem entirely. Both groups have disease, but one has active/vulnerable disease.

### Strategy E: Quartile-Based (Population Stratification)

Don't pre-define groups at all. Measure FAI or material decomposition in everyone, then compare top vs. bottom quartiles.

**Precedent**: CRISP-CT used quartile-based comparisons. ORFAN stratified by number of inflamed arteries (0, 1, 2, 3).

**Limitation**: Circular when applied to FAI (using FAI to define groups, then testing FAI). NOT circular for material decomposition — you can stratify by FAI quartile and then ask whether water fraction differs between FAI-high and FAI-low groups.

---

## 7. Standard Inclusion and Exclusion Criteria

Based on published PCAT studies, these are the criteria most commonly used:

### Typical Inclusion Criteria

| Criterion | Rationale | Used by |
|---|---|---|
| Clinically indicated CCTA | Ethical justification; no research-only scans | All studies |
| Age ≥ 18 | Standard | All studies |
| Adequate image quality for PCAT measurement | PCAT requires clear fat delineation | All studies |
| Complete clinical records | Need disease history, medications, labs | Most studies |

### Typical Exclusion Criteria

| Criterion | Rationale | Used by |
|---|---|---|
| Prior CABG or PCI (stents) | Metal artifacts confound PCAT measurement | Li 2025, Kuneman 2023, Chen 2021 |
| Pacemaker or prosthetic valve | Artifact | Kahmann 2024, Varga-Szemes 2021 |
| Known myocarditis, vasculitis, active systemic infection | Non-coronary inflammation confounds PCAT | Multiple |
| Anomalous coronary artery origin | Abnormal anatomy prevents standardised measurement | Ma 2020 |
| Poor image quality (motion artifacts, insufficient contrast) | Unreliable measurements | All studies |
| Persistent or permanent atrial fibrillation | Motion artifact on CCTA | Feasibility studies, Kahmann 2024 |
| Known malignancy | Systemic inflammation confounder | Chen 2021 |
| Pregnancy at time of scan | Radiation exposure; altered hemodynamics | Standard for all CT studies |
| eGFR < 30 mL/min/1.73m² (unless on dialysis) | Contrast nephropathy risk; altered fluid balance may affect PCAT | Standard for contrast CT studies |
| Systemic anti-inflammatory therapy at time of scan | Colchicine, biologics, chronic corticosteroids directly alter PCAT composition — the variable being measured. Fiolet 2025 (LoDoCo2 substudy) showed colchicine's effect on PCAT is the very question under investigation | Recommended for composition studies |

### PCCT-Specific Considerations

| Criterion | Rationale |
|---|---|
| PCCT scan protocol standardised (kVp, mAs, kernel) | Material decomposition accuracy depends on protocol |
| Sufficient pericoronary fat volume for ROI placement | Small patients or minimal epicardial fat → unreliable measurement |
| Multi-energy reconstruction available | Required for material decomposition |

---

## 8. Recommended Design for PCCT Material Decomposition Study

> **Study type**: Retrospective analysis of existing PCCT CCTA scans with clinical data extracted from electronic medical records. No new patient recruitment or imaging is required.

### Primary Design: Within-Patient Vessel Comparison

This is the **strongest** design for a first clinical validation paper because it:
- Mirrors the simulation study (healthy vs. inflamed PCAT, same "scanner")
- Eliminates inter-patient confounders
- Is the most common design in the field (reviewers expect it)
- Requires modest sample size (each patient provides paired data)

**Protocol**:
1. From existing PCCT CCTA database, select patients with **single-vessel or dominant-vessel** coronary disease (one vessel with significant stenosis or high-risk plaque, at least one clean vessel)
2. **Definition of "clean vessel"**: CAD-RADS 0 in that coronary territory — no visible plaque or stenosis. This is stricter than "no significant stenosis" and follows Ma et al. 2021, who compared arteries "with plaque" vs. "without plaque."
3. For each patient, measure:
   - **Water fraction** (material decomposition) of PCAT around the diseased vessel
   - **Water fraction** of PCAT around the clean vessel
   - **FAI (HU)** of PCAT around both vessels
4. Primary analysis: Paired comparison (Wilcoxon signed-rank or paired t-test) of water fraction between diseased vs. clean vessel
5. Secondary analysis: Same comparison for FAI (HU) — expect FAI to show a difference too, but show that it's confounded across patients/protocols while water fraction is not

**Methods paragraph you can adapt**:

> "This retrospective study reviewed existing PCCT CCTA scans from [institution] acquired between [date range]. Truly healthy controls are unavailable in CCTA populations, as all patients were referred for clinical indications. We employed a within-patient vessel-level comparison, measuring pericoronary adipose tissue composition around both the diseased coronary vessel (defined by [CAD-RADS ≥ 3 / high-risk plaque features / ICA-confirmed culprit]) and an uninvolved vessel (CAD-RADS 0 in that territory, no visible plaque or stenosis) in the same patient. This paired design eliminates inter-patient confounders including age, sex, BMI, medication use, and imaging protocol. Clinical data were extracted retrospectively from electronic medical records."

### Secondary Design: CAD-RADS 0 vs. High-Risk Plaque (Between-Patient)

Use this as a **supplementary analysis** or if within-patient comparison is not feasible for all patients:

**Protocol**:
1. From the same retrospective database:
2. **Group A** (pseudo-healthy): CAD-RADS 0, calcium score 0
3. **Group B** (diseased): ≥ 2 high-risk plaque features (positive remodeling, LAP < 30 HU, spotty calcification, napkin-ring sign)
4. Match 1:1 or 1:2 by age (± 5 years), sex, BMI (± 3 kg/m²), hypertension (Y/N), diabetes (Y/N), statin use (Y/N). Propensity score matching is preferred over manual matching for reproducibility.
5. Compare water fraction and FAI between groups

### The Narrative Arc: Simulation → Clinical

The two papers form a logical sequence:

| | Simulation Paper (current) | Clinical Paper (next) |
|---|---|---|
| **Ground truth** | Known tissue composition (XCAT phantom) | Clinical endpoints (CAD-RADS, plaque features) |
| **What it proves** | Material decomposition CAN detect composition differences that FAI cannot | Material decomposition DOES detect composition differences in real patients |
| **Limitation addressed** | "Only simulation" | "Now validated in vivo" |
| **Control** | Same phantom, different composition | Same patient, different vessel (or matched groups) |

**One-sentence bridge for grant/paper**: "Having established under controlled simulation conditions that material decomposition detects inflammation-related PCAT composition changes that HU-based FAI cannot (Nie & Molloi 2025), this retrospective study validates the approach in vivo using photon-counting CT in patients with and without coronary artery disease."

### Sample Size Considerations

The minimum target of n ≥ 30 per group is based on comparable PCCT PCAT studies:
- Kahmann 2024: n=36 total (18 CAD + 18 matched controls)
- Tremamunno 2025: n=40 (intra-individual PCD vs. EID comparison)
- Chen 2021: n=104 (dual-layer spectral CT, larger but different technology)

n=30 per group is the minimum for adequate statistical power in paired comparisons. **A formal power calculation is required before finalising the study** — base it on the expected effect size for water fraction differences between healthy and inflamed PCAT from Nie & Molloi 2025 simulation results. If the expected effect size is small (< 0.5 SD), consider increasing to n=40–50 per group.

For the within-patient paired design, power requirements are lower than for between-patient comparisons because inter-patient variability is eliminated.

### Group C Definition Justification

Group C is defined as "CAD-RADS 3–5, OR ≥ 2 high-risk plaque features in any vessel." This means a patient with CAD-RADS 3 (50–69% stenosis) but zero high-risk plaque features is still classified as "high-risk."

**Justification**: CAD-RADS ≥ 3 represents ≥ 50% stenosis, which is an established independent risk factor for MACE regardless of plaque morphology. The OR criterion ensures that both anatomically significant disease (by stenosis severity) and morphologically high-risk disease (by plaque features) are captured. This is consistent with Chen et al. 2021, who used ≥ 2 high-risk features, and with CAD-RADS 2.0 guidelines, which classify ≥ 50% stenosis as warranting further investigation.

---

## References

### Part I — Healthy vs. Diseased Definitions

1. Li Y et al. "Evaluation of Perivascular Fat Attenuation Index to Better Identify Culprit Lesions in Acute Coronary Syndrome According to Stenosis Severity." *J Comput Assist Tomogr* 2025. [DOI](https://doi.org/10.1097/RCT.0000000000001694)
2. Yang L et al. "Lesion-specific pericoronary fat attenuation index for identifying culprit lesions in patients with non-ST-segment elevation myocardial infarction." *Eur J Radiol Open* 2025;14:100621. [DOI](https://doi.org/10.1016/j.ejro.2024.100621)
3. Sagris M et al. "Pericoronary fat attenuation index — meta-analysis." *Eur Heart J Cardiovasc Imaging* 2022;23:1535–1544. [DOI](https://doi.org/10.1093/ehjci/jeac174)
4. Oikonomou EK et al. "CRISP-CT: Non-invasive detection of coronary inflammation using CT." *Lancet* 2018;392:929–939. [DOI](https://doi.org/10.1016/S0140-6736(18)31114-0)
5. Chan K et al. "ORFAN: Pericoronary adipose tissue attenuation and mortality." *Lancet* 2024. [DOI](https://doi.org/10.1016/S0140-6736(24)01811-9)
6. Antonopoulos AS et al. "Detecting human coronary inflammation by imaging perivascular fat." *Sci Transl Med* 2017;9:eaal2658. [DOI](https://doi.org/10.1126/scitranslmed.aal2658)
7. Ocana G et al. "Coronary CT angiography-derived pericoronary fat attenuation index: Post-mortem histopathological correlation in fatal plaques." *Int J Cardiol* 2025;435:133388. [DOI](https://doi.org/10.1016/j.ijcard.2025.133388)

### Part II — Clinical Study Design References

8. Nie S, Molloi S. "Quantification of Water and Lipid Composition of Perivascular Adipose Tissue Using Coronary CT Angiography: A Simulation Study." *Int J Cardiovasc Imaging* 2025;41:1091–1101. [DOI](https://doi.org/10.1007/s10554-025-03358-5)
9. Chen Q et al. "Quantification of pericoronary adipose tissue attenuation using dual-layer spectral detector CT to detect vulnerable plaques." *Diagn Interv Radiol* 2021;27:791–797. [DOI](https://doi.org/10.5152/dir.2021.20677)
10. Kuneman JH et al. "Pericoronary adipose tissue attenuation in patients with acute coronary syndrome versus stable coronary artery disease." *Circ Cardiovasc Imaging* 2023;16:e015408. [DOI](https://doi.org/10.1161/CIRCIMAGING.123.015408)
11. Kahmann SL et al. "Interrelation of pericoronary adipose tissue texture and coronary artery disease in cardiac photon-counting CT." *Front Cardiovasc Med* 2024;11:1399917. [DOI](https://doi.org/10.3389/fcvm.2024.1399917)
12. Varga-Szemes A et al. "Epicardial adipose tissue attenuation and fat attenuation index: phantom study and in vivo measurements with photon-counting CT." *Acad Radiol* 2021. [DOI](https://doi.org/10.1016/j.acra.2021.07.023)
13. Ma R et al. "Towards reference values of pericoronary adipose tissue attenuation: impact of coronary artery and tube voltage in coronary CT angiography." *Eur Radiol* 2020;30:6838–6846. [DOI](https://doi.org/10.1007/s00330-020-07069-0)
14. Boussoussou M et al. "The effect of patient and imaging characteristics on pericoronary adipose tissue attenuation." *JCCT* 2023;17:52–59. [DOI](https://doi.org/10.1016/j.jcct.2022.09.006)
15. Xu L et al. "Relationship between different clinical characteristics and pericoronary adipose tissue attenuation values in patients without coronary heart disease." *BMC Cardiovasc Disord* 2024;24:348. [DOI](https://doi.org/10.1186/s12872-024-04021-0)
16. Tremamunno G et al. "Photon-counting vs. energy-integrating detector CT — FAI not comparable." *Acad Radiol* 2025;32(3). [DOI](https://doi.org/10.1016/j.acra.2024.11.055)
17. Cury RC et al. "CAD-RADS 2.0 — Coronary Artery Disease Reporting and Data System." *Radiology: Cardiothoracic Imaging* 2022;4(5):e220183. [DOI](https://doi.org/10.1148/ryct.220183)
