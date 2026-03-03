# How the Field Defines "Healthy vs. Diseased" PCAT

**Project**: PCAT — MolloiLab, University of California, Irvine  
**Author**: Shu Nie  
**Date**: March 2026  
**Purpose**: Analysis of how clinical PCAT studies define "healthy" vs. "diseased" pericoronary adipose tissue, how "culprit" vs. "non-culprit" lesions are operationally identified, and why the simulation study's compositional ground truth is unique.

---

## Table of Contents

- [1. Three Strategies for Defining "Healthy vs. Diseased"](#1-three-strategies-for-defining-healthy-vs-diseased)
- [2. How "Culprit Lesion" is Operationally Defined](#2-how-culprit-lesion-is-operationally-defined)
- [3. Why This Matters for Your Study (Critical Positioning)](#3-why-this-matters-for-your-study-critical-positioning)
- [4. Comparison Table](#4-comparison-table)

---

## 1. Three Strategies for Defining "Healthy vs. Diseased"

This is critical for understanding the field and for positioning your simulation study. Every clinical PCAT study must define what counts as "inflamed" and what counts as "healthy." There are three fundamentally different strategies used in the literature, and **none of them use known tissue composition as ground truth.** This is the gap your study fills.

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

### 1.3 Strategy 3: Histological Ground Truth (Antonopoulos 2017 Only)

**This is the only study with true biological ground truth.** Patients undergoing cardiac surgery (bypass grafting, valve replacement) donated pericoronary fat biopsies at the time of surgery. The biopsied fat was matched to pre-operative CT scans.

| Study | Population | How "inflamed" was defined | Key findings |
|---|---|---|---|
| Antonopoulos et al. 2017 (*Sci Transl Med*, n=453) | Cardiac surgery patients | Histology — PPARγ expression, lipid droplet size, IL-6/TNF-α levels, UCP1 expression | Inflamed fat: reduced PPARγ (−2.3-fold), reduced FABP4 (−1.8-fold), increased IL-6 (+3.1-fold), increased TNF-α (+2.7-fold), smaller lipid droplets. HU correlated with these markers. |

**Limitation**: This is a surgical population (severe disease, often multivessel), not representative of the broader CCTA population. The biopsy is epicardial fat near the aortic root, not precisely the same pericoronary fat measured by FAI. Sample handling may alter tissue properties.

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

## 3. Why This Matters for Your Study (Critical Positioning)

Here is the key insight to use in your paper:

**No previous study defines "inflamed" vs. "healthy" by actual tissue composition.** Every clinical study defines "diseased" by:
- Clinical outcome (who had a heart attack → therefore "inflamed")
- Angiographic appearance (which lesion looks culprit → therefore "inflamed" around it)
- Histology (only Antonopoulos 2017, surgical population only)

**Your simulation study is unique because you define inflammation AT THE COMPOSITIONAL LEVEL.** You set the exact water/lipid fractions of healthy vs. inflamed PCAT, giving you something no clinical study has: **known ground truth tissue composition.**

This is a strength, not a limitation. You can use it in your discussion:

> "A fundamental challenge in validating CT-based PCAT measurements is the absence of compositional ground truth. Clinical studies define 'inflamed' pericoronary fat by clinical endpoints (ACS presentation, cardiovascular events) or invasive imaging (angiographic culprit identification), not by measured tissue composition. Consequently, the relationship between FAI and actual tissue water/lipid content remains incompletely characterised. Simulation provides the essential controlled conditions in which the tissue composition is known exactly, enabling direct evaluation of whether a given measurement can detect composition differences of clinical relevance."

---

## 4. Comparison Table

| Criterion | Strategy 1 (Within-patient) | Strategy 2 (Outcome-based) | Strategy 3 (Histology) | **Your Study** |
|---|---|---|---|---|
| What defines "diseased"? | Culprit lesion (ICA/clinical) | Cardiac event (MACE/death) | Histological markers (PPARγ, IL-6) | **Known tissue composition (water/lipid fractions)** |
| Ground truth type | Clinical endpoint | Clinical endpoint | Biological endpoint | **Compositional ground truth** |
| Within-patient control? | Yes (non-culprit vessel) | No (between-patient) | Partial (adjacent tissue) | **Yes (same phantom, different composition)** |
| Protocol standardised? | Single-centre protocol | Multi-centre, variable | Single-centre | **Systematically varied** |
| Can confirm what FAI measures? | No — circular (FAI validates FAI) | No — correlation, not mechanism | Partially — matches HU to biology | **Yes — known input vs. measured output** |
| Limitations | Culprit ≠ most inflamed; just the one that ruptured | Reverse causation; confounders | Surgical population; biopsy location | Simulation; not clinical |
