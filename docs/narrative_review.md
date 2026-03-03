# Narrative Review: Why Material Decomposition for PCAT, and How to Write This Paper

**Project**: PCAT — MolloiLab, University of California, Irvine  
**Author**: Shu Nie  
**Date**: March 2026  
**Purpose**: Practical guide for writing and positioning the current XCAT + material decomposition study. Covers field context, what reviewers will ask, how to frame your contribution, and common mistakes to avoid.

---

## Table of Contents

- [1. The Story in 60 Seconds](#1-the-story-in-60-seconds)
- [2. What the Field Established (What You Build On)](#2-what-the-field-established-what-you-build-on)
- [3. What the Field Got Wrong (Why Your Study Matters)](#3-what-the-field-got-wrong-why-your-study-matters)
- [4. How Other Papers Frame FAI Limitations (Diplomatic Language)](#4-how-other-papers-frame-fai-limitations-diplomatic-language)
- [5. What Your Previous Paper Already Showed](#5-what-your-previous-paper-already-showed)
- [6. What This Study Adds (The Gap You Fill)](#6-what-this-study-adds-the-gap-you-fill)
- [7. What Reviewers Will Ask and How to Answer](#7-what-reviewers-will-ask-and-how-to-answer)
- [8. Common Mistakes in Simulation Papers (Avoid These)](#8-common-mistakes-in-simulation-papers-avoid-these)
- [9. How to Write Each Section](#9-how-to-write-each-section)
- [10. Numbers You Must Know by Heart](#10-numbers-you-must-know-by-heart)
- [11. Competing Approaches and How to Discuss Them](#11-competing-approaches-and-how-to-discuss-them)
- [12. Positioning Checklist Before Submission](#12-positioning-checklist-before-submission)
- [13. How the Field Defines "Healthy vs. Diseased" PCAT](#13-how-the-field-defines-healthy-vs-diseased-pcat-and-why-it-matters-for-your-study)

---

## 1. The Story in 60 Seconds

Here is the complete argument your paper needs to make, in plain language:

1. **Coronary inflammation causes heart attacks.** Three randomised trials (CANTOS, COLCOT, LoDoCo2) proved this by showing that anti-inflammatory drugs reduce cardiac events independently of cholesterol.

2. **The field needs a way to detect coronary inflammation non-invasively.** FAI (Fat Attenuation Index) was proposed as this tool — it measures the Hounsfield Unit of fat around coronary arteries, where inflamed fat appears less negative (more watery) on CT.

3. **FAI predicts outcomes impressively.** HR 9.04 for cardiac death (CRISP-CT, n=1,872), HR 29.8 for 3 inflamed arteries (ORFAN, n=40,091). FDA cleared. Medicare reimbursement.

4. **But FAI has a measurement problem.** The HU value it relies on changes by 8–33 HU depending on tube voltage, reconstruction kernel, contrast timing, scanner model, and patient size. The biological signal (inflamed vs. healthy fat) is only ~15 HU. So the "noise" from imaging parameters is as large as the "signal" from biology.

5. **This means FAI may be measuring the scanner, not the patient.** When Boussoussou et al. corrected for imaging parameters, the association between PCAT and coronary plaque vanished entirely (p=0.93). Colchicine reduces cardiac events by 31% but does not change FAI (p=0.236).

6. **Material decomposition solves this.** Instead of measuring HU (which mixes biology and physics), material decomposition measures the actual water and lipid fractions of tissue. These fractions don't change with tube voltage or patient size — they are intrinsic tissue properties.

7. **Your previous paper showed this works for PCAT composition.** Water fraction RMSE 0.01–0.64% across protocols, while HU varied by 21.9%.

8. **This paper extends it to inflammation detection.** Using XCAT phantoms, you simulate healthy vs. inflamed PCAT (inflamed = more water), decompose into water/lipid/collagen/iodine, and show that material decomposition detects the difference across all protocols while FAI cannot reliably do so.

**One-sentence summary for your abstract**: "Material decomposition provides protocol-independent quantification of pericoronary adipose tissue composition, enabling reliable detection of inflammation-related changes that HU-based FAI cannot distinguish from technical confounders."

---

## 2. What the Field Established (What You Build On)

You are not challenging the field — you are building on it. Your introduction should clearly credit these established facts:

### 2.1 Inflammation is causal (cite these three)
- **CANTOS** (Ridker, *NEJM* 2017): Canakinumab (IL-1β antibody) reduced MACE by 15% without changing LDL. n=10,061.
- **COLCOT** (Tardif, *NEJM* 2019): Colchicine reduced MACE by 23% post-MI.
- **LoDoCo2** (Nidorf, *NEJM* 2020): Colchicine reduced MACE by 31% in chronic CAD.

### 2.2 The biological basis is real (cite this one)
- **Antonopoulos 2017** (*Sci Transl Med*): Histological validation in 453 cardiac surgery patients. Inflamed PCAT had reduced PPARγ (−2.3-fold), reduced FABP4 (−1.8-fold), increased IL-6 (+3.1-fold), increased TNF-α (+2.7-fold), and smaller lipid droplets. This is genuine biology — coronary inflammation really does change the molecular phenotype of adjacent fat.

### 2.3 FAI predicts clinical outcomes (cite these)
- **CRISP-CT** (Oikonomou, *Lancet* 2018): HR 9.04 for cardiac death, n=1,872. Threshold −70.1 HU.
- **ORFAN extended** (Chan, *Lancet* 2024): HR 29.8 (3 inflamed arteries vs. none), n=40,091.
- **Sagris meta-analysis** (2022): 20 studies, n=7,797, FAI higher around unstable vs. stable plaques.

**Why this matters for your paper**: You are NOT saying FAI is useless. You are saying FAI has a measurement limitation that material decomposition can address. Reviewers will reject your paper if they think you're dismissing FAI entirely.

---

## 3. What the Field Got Wrong (Why Your Study Matters)

This section is the core of your argument. These are the numbers you need to cite to justify your study:

### 3.1 The confounders are as large as the signal

The FAI "signal" for inflammation is roughly 15 HU (from ~−85 HU healthy to ~−70 HU inflamed). Compare this to the technical confounders:

| Confounder | Magnitude | Source |
|---|---|---|
| Tube voltage (80–135 kVp) | **21.9% HU variance** = ~8–20 HU shift | Nie & Molloi 2025; Boussoussou 2023 (+8 HU per kVp step) |
| Reconstruction kernel | **Up to 33 HU** intra-individual variation | Lisi et al. 2024 (*Eur Radiol*) |
| Contrast timing | **~7 HU swing** + 78% radiomic instability | Wu et al. 2025 (*J Clin Med*) |
| Scanner platform | **15 HU** between scanners | Boussoussou 2023 (GE vs. Philips) |
| Patient size | **3.6% HU variance** | Nie & Molloi 2025 |
| Partial volume | Signal decreases with distance from lumen — consistent with physics, not biology | Hell et al. 2016 (*JCCT*) |

**Key sentence you can use in your paper**: "The biological signal of interest (~15 HU) is comparable in magnitude to, and in some cases smaller than, the technical variance introduced by routine differences in imaging protocol."

### 3.2 When you correct for confounders, the biological signal disappears

**Boussoussou et al. 2023** (*JCCT*, n=1,652, zero calcium score):
- Univariable: PCAT +2 HU with plaque, p<0.001
- After correcting for kVp, pixel spacing, BMI, heart rate, CNR: **p=0.93** — zero association

The strongest predictors of PCAT attenuation were all technical: tube voltage (+8 HU per step), pixel spacing (+32 HU per mm³), heart rate (−0.2 HU/bpm), BMI (−0.4 HU per kg/m²).

### 3.3 FAI cannot detect the effect of proven anti-inflammatory treatment

**Fiolet et al. 2025** (LoDoCo2 CT substudy, *Heart*, n=151):
- Colchicine 0.5 mg daily for 28 months vs. placebo
- PCAT attenuation: −79.5 HU vs. −78.7 HU, **p=0.236**
- No correlation between hsCRP/IL-6 and PCAT attenuation

Despite colchicine reducing MACE by 31% in the parent trial, FAI did not detect any change.

### 3.4 The threshold doesn't transfer across scanners

The −70.1 HU threshold (CRISP-CT) was validated on specific scanners at specific protocols. Tremamunno et al. (2025) confirmed that photon-counting CT and conventional CT produce systematically different FAI values for the same patient. The threshold cannot be applied across platforms without recalibration.

---

## 4. How Other Papers Frame FAI Limitations (Diplomatic Language)

This is critical. You need to critique FAI without alienating the Oxford group or the reviewers who use FAI clinically. Here is how successful papers do it:

### 4.1 Acknowledge first, then limit

**Pattern**: "FAI has demonstrated [impressive result] in [large cohort]. However, [specific technical limitation] raises questions about [specific aspect]."

**Example you can adapt**: "FAI has demonstrated robust prognostic value across large multi-centre cohorts, with hazard ratios of 9.04 for cardiac death (CRISP-CT) and 29.8 for multi-vessel inflammation (ORFAN). However, recent evidence that imaging parameters account for comparable or greater variance than biology (Boussoussou et al., Lisi et al., Wu et al.) suggests that the measurement may conflate technical and biological signals."

### 4.2 Frame limitations as "technical considerations," not failures

**Don't say**: "FAI is unreliable" or "FAI fails to measure inflammation"  
**Say**: "HU-based measurements are inherently sensitive to acquisition parameters, which may limit the reliability of FAI across heterogeneous clinical protocols"

**Don't say**: "The colchicine study proves FAI doesn't work"  
**Say**: "The LoDoCo2 CT substudy's negative finding (p=0.236) raises the question of whether HU-based measurements have sufficient sensitivity to detect treatment-induced changes in pericoronary adipose tissue composition"

### 4.3 Position your work as complementary, not replacement

**Don't say**: "Material decomposition replaces FAI"  
**Say**: "Material decomposition provides a complementary approach that measures tissue composition directly, potentially enabling protocol-independent characterisation of PCAT"

### 4.4 Use the Tan et al. 2023 framing

The JACC review (Tan et al. 2023, Baker Heart + Cedars-Sinai) already said PCAT is "not ready for prime time." You can cite this instead of making the critique yourself:

"As noted by Tan et al. (JACC 2023), significant knowledge gaps remain in the measurement standardisation of PCAT attenuation, and further validation is needed before routine clinical adoption."

### 4.5 Even Oxford acknowledges the problem

Chan & Antoniades (2025, editorial comment) proposed the "FAI Score" — adjusting raw FAI for technical and demographic factors. **This is Oxford itself admitting that raw FAI is protocol-dependent.** You can cite this supportively: "The development of FAI Score (Chan & Antoniades 2025) reflects the field's recognition that raw PCAT attenuation requires standardisation."

---

## 5. What Your Previous Paper Already Showed

Your first paper (Nie & Molloi, *Int J Cardiovasc Imaging* 2025) established:

| What was shown | Key result |
|---|---|
| Water fraction measurement is accurate | RMSE 0.01–0.64% across 80–135 kVp |
| HU is protocol-dependent | 21.9% variance across kVp, 3.6% across patient sizes |
| Material decomposition is protocol-independent | Same composition → same water fraction regardless of protocol |
| Three-material decomposition works | Water, lipid, protein decomposition demonstrated |

**What it did NOT show** (and what your current paper must add):
- Did not simulate inflammation (healthy vs. diseased PCAT)
- Did not use anatomically realistic phantoms (XCAT)
- Did not include iodine as a fourth material (contrast agent)
- Did not directly demonstrate that inflammation is detectable by composition but not by HU
- Did not show collagen as a decomposition basis material

**Be careful**: Your current paper must be a genuine extension, not a repetition. The key new contribution is showing that **inflammation-induced composition changes are detectable by material decomposition but not reliably detectable by FAI** across protocols. This is the experiment the field needs.

---

## 6. What This Study Adds (The Gap You Fill)

### 6.1 The logical gap in the field

The field is stuck in a loop:
1. FAI predicts outcomes → but is FAI measuring inflammation or confounders?
2. Correct for confounders → signal disappears → was there a signal?
3. Extract more features (radiomics) → features are equally confounded
4. Everyone calls for "standardisation" → but HU is fundamentally ambiguous

**No one has directly tested**: If you measure tissue composition (not HU), can you detect the inflammation-related change that FAI claims to measure? This is your experiment.

### 6.2 What your paper demonstrates

1. **Ground truth**: XCAT phantom with known tissue compositions — healthy PCAT vs. inflamed PCAT (higher water content, simulating immature adipocytes)
2. **The FAI failure**: When you scan the same healthy vs. inflamed tissue at different protocols, HU values overlap — the "inflamed" tissue at one protocol looks identical to "healthy" tissue at another protocol
3. **The material decomposition success**: Water/lipid fractions correctly distinguish healthy from inflamed PCAT regardless of protocol
4. **Protocol independence**: The composition measurement doesn't change with kVp, patient size, or other acquisition parameters

### 6.3 Why this matters clinically

Frame it this way:
- Multi-site clinical trials need protocol-independent measurements
- Longitudinal monitoring (before/after treatment) requires that changes reflect biology, not scanner drift
- The field needs a measurement that can answer: "Did the inflammation actually change, or did the scanner parameters change?"

---

## 7. What Reviewers Will Ask and How to Answer

Based on how simulation studies in this field are reviewed, expect these questions:

### Q1: "This is a simulation — how does it translate to clinical reality?"

**Prepare this answer**: "This study establishes the theoretical performance limits of material decomposition for PCAT composition quantification under controlled conditions. Clinical validation with in vivo patient data is the necessary next step, which we acknowledge as a limitation. However, simulation provides the essential proof-of-concept that cannot be obtained in vivo, where ground truth tissue composition is unknown."

**Framing**: Call it "proof-of-concept" or "feasibility study," not "validation."

### Q2: "XCAT phantoms don't represent real patient variability"

**Prepare this answer**: "While XCAT phantoms provide anatomically realistic cardiac geometry, they represent simplified models of clinical variability. We tested across three patient sizes (small, medium, large) and four tube voltages (80, 100, 120, 135 kVp) to capture the primary sources of protocol variation. Full representation of anatomical and pathological variability requires clinical validation."

### Q3: "Your inflammation model is too simple — real inflammation isn't a uniform water content increase"

**Prepare this answer**: "We modelled inflammation as a shift in water-lipid ratio based on the histologically validated finding that inflamed adipocytes retain more water and less lipid (Antonopoulos et al. 2017). While real inflammation is heterogeneous and includes cellular infiltration, extracellular matrix changes, and angiogenesis, the water content increase is the primary CT-detectable signature. Our model captures the dominant signal component relevant to CT-based detection."

### Q4: "Material decomposition requires dual-energy or photon-counting CT — this limits clinical applicability"

**Prepare this answer**: "Multi-energy CT is increasingly available clinically, with photon-counting CT (Siemens NAEOTOM Alpha) deployed at major centres and dual-energy CT widely available. Material decomposition of pericoronary adipose tissue is technically feasible on current clinical hardware. The question is whether the measurement provides sufficient benefit to justify the acquisition requirement."

### Q5: "You didn't compare against FAI Score (the corrected version), only raw FAI"

**Prepare this answer**: "Our comparison is against the physical measurement (HU) that underlies all FAI variants, including FAI Score. FAI Score applies statistical corrections to HU values, which may reduce but cannot eliminate protocol dependence. Material decomposition operates in a fundamentally different domain where protocol effects are eliminated by physics, not by statistics."

### Q6: "You don't show any clinical outcome data"

**Prepare this answer**: "This study establishes construct validity — demonstrating that material decomposition accurately measures the tissue composition change associated with inflammation. Predictive validity (association with clinical outcomes) is a subsequent research question. We note that the field's current challenge is not insufficient outcome data (ORFAN: n=40,091) but uncertain construct validity of the underlying measurement."

### Q7: "How do you know your 5% water fraction threshold corresponds to clinically relevant inflammation?"

**Prepare this answer**: Based on Antonopoulos et al. (2017), the histologically confirmed composition change from healthy to inflamed PCAT involves reduced lipid content and increased water. Your previous paper (Nie & Molloi 2025) established that the clinically relevant water fraction range is 17–37%, with inflammation expected to alter values by approximately 5%. Cite the histological evidence directly.

---

## 8. Common Mistakes in Simulation Papers (Avoid These)

### 8.1 Overclaiming clinical applicability

❌ "This method will enable clinical detection of inflammation"  
✅ "This computational framework demonstrates feasibility under controlled conditions; clinical validation is needed"

❌ "Material decomposition is superior to FAI"  
✅ "Material decomposition provides protocol-independent composition measurement, which may complement existing HU-based approaches"

### 8.2 Dismissing FAI entirely

❌ "FAI is fundamentally flawed and should not be used clinically"  
✅ "FAI has demonstrated strong prognostic value. The measurement limitations identified here suggest that composition-based approaches may provide complementary information"

### 8.3 Not acknowledging your own limitations honestly

Reviewers expect these limitations in your discussion. If you don't include them, reviewers will think you're hiding weaknesses:

1. **Simulation, not clinical**: "This study used simulated CT data; clinical validation with patient data is required"
2. **Simplified inflammation model**: "Inflammation was modelled as uniform water content changes, which simplifies the complex biological heterogeneity of pericoronary inflammation"
3. **No outcome data**: "This study does not assess predictive validity (association with cardiovascular outcomes)"
4. **Hardware requirement**: "Material decomposition requires multi-energy CT, which may limit widespread adoption compared to conventional single-energy CCTA"
5. **No noise/artifact modeling**: If applicable — acknowledge what wasn't modelled (scatter, beam hardening complexity, etc.)

### 8.4 Self-plagiarism from your first paper

Your current paper extends Nie & Molloi 2025. Make sure:
- The methods section describes what is NEW (XCAT anatomy, inflammation simulation, 4-material decomposition, direct FAI comparison)
- Do NOT copy the protocol-independence argument verbatim from the first paper
- Reference the first paper for established methods: "As previously described (Nie & Molloi 2025), material decomposition..."
- The results must show NEW findings (inflammation detection) not just re-demonstrate protocol independence

### 8.5 Using "prove" or "demonstrate superiority"

Simulation studies **cannot** prove clinical superiority. Use:
- "suggests," "indicates," "supports the feasibility of"
- "under simulated conditions," "in this computational framework"
- "warrants further investigation," "motivates clinical validation"

### 8.6 Forgetting to frame your study within the broader trajectory

The field has a pattern: HU-based measurement → discover confounders → propose corrections → eventually switch to composition-based measurement. This happened in:
- **Renal stone characterisation**: Single-energy HU → dual-energy composition (uric acid vs. calcium)
- **Gout diagnosis**: HU crystal detection → dual-energy urate mapping
- **Hepatic fat**: Unenhanced HU → proton-density fat fraction (MRI) / multi-energy decomposition
- **Iron overload**: HU → material decomposition

Your paper is part of this broader trajectory. Mention it briefly in the discussion — it legitimises your approach by showing it's not an isolated idea but part of an established methodological evolution in CT imaging.

---

## 9. How to Write Each Section

### 9.1 Introduction (4 paragraphs)

**Paragraph 1 — The clinical problem**: Coronary inflammation causes cardiovascular events (cite CANTOS, COLCOT, LoDoCo2). Need for non-invasive vessel-specific measurement. FAI was proposed as this measurement. 2–3 sentences.

**Paragraph 2 — FAI's success**: FAI predicts outcomes (cite CRISP-CT, ORFAN). FDA cleared. Biologically plausible (cite Antonopoulos 2017). 2–3 sentences. This shows you respect the field.

**Paragraph 3 — The measurement problem**: However, HU-based measurements are protocol-dependent (cite specific numbers: 21.9%, 33 HU, 7 HU, 15 HU between scanners). The biological signal (~15 HU) is comparable to technical variance. After confounder correction, association with plaque disappears (cite Boussoussou). Colchicine doesn't change FAI (cite Fiolet). 4–5 sentences.

**Paragraph 4 — Your contribution**: Material decomposition measures tissue composition directly, eliminating protocol dependence. Previous work (Nie & Molloi 2025) demonstrated protocol-independent water fraction measurement. This study extends that work to show that inflammation-induced composition changes are detectable by material decomposition but not reliably by HU-based FAI. 2–3 sentences.

### 9.2 Methods

Be extremely precise. Reviewers of simulation papers scrutinise methods heavily. Include:
- XCAT phantom parameters (version, cardiac phase, anatomy details)
- Tissue compositions used (exact water/lipid/collagen/iodine fractions for healthy vs. inflamed)
- How inflammation was modelled (cite Antonopoulos 2017 for biological basis)
- CT simulation parameters (kVp values, patient sizes, noise levels)
- Material decomposition algorithm (cite your lab's method)
- FAI computation (use Oxford protocol: −190 to −30 HU window)
- Statistical analysis

### 9.3 Results

Show two things side by side:
1. **FAI fails across protocols**: Same tissue, different protocols → different HU → different FAI classification
2. **Material decomposition succeeds across protocols**: Same tissue, different protocols → same water/lipid fractions → correct classification

Use a figure showing the overlap problem: plot HU distributions of healthy and inflamed PCAT at different kVp — show that they overlap. Then plot water fraction distributions — show clear separation.

### 9.4 Discussion (5 paragraphs)

**Paragraph 1 — Summary of findings**: What you found, plainly stated.

**Paragraph 2 — Context in the field**: How this relates to the known measurement problem. Cite the confounder studies. Cite Boussoussou and Fiolet. Frame material decomposition as addressing a recognised limitation.

**Paragraph 3 — Clinical implications**: What this means for multi-site trials, longitudinal monitoring, and treatment response assessment. Be measured — use "could," "may," "potentially."

**Paragraph 4 — Comparison with other approaches**: How material decomposition compares to FAI Score (statistical correction), radiomics (more features from same confounded data), PCATMA (threshold-free but still HU-based). Don't trash them — note what each does and doesn't solve.

**Paragraph 5 — Limitations and future work**: (See Section 8.3 above for the list.) End with: "Clinical validation with in vivo patient data is the essential next step."

---

## 10. Numbers You Must Know by Heart

These are the numbers you will need in your introduction, discussion, and when responding to reviewers. Memorise them:

### Clinical evidence (establishes why inflammation matters)
| Number | What it is | Source |
|---|---|---|
| 15% MACE reduction | Canakinumab (anti-IL-1β), independent of LDL | CANTOS, Ridker 2017 |
| 23% MACE reduction | Colchicine, post-MI | COLCOT, Tardif 2019 |
| 31% MACE reduction | Colchicine, chronic CAD | LoDoCo2, Nidorf 2020 |

### FAI prognostic evidence (establishes that FAI predicts outcomes)
| Number | What it is | Source |
|---|---|---|
| HR 9.04 | RCA-FAI for cardiac death, 5y follow-up | CRISP-CT, Oikonomou 2018 |
| HR 29.8 | 3 inflamed arteries vs. none, cardiac mortality | ORFAN, Chan 2024 |
| −70.1 HU | FAI threshold, AUC 0.76 | CRISP-CT |
| n=40,091 | Largest FAI cohort | ORFAN extended |

### Technical confounders (establishes the measurement problem)
| Number | What it is | Source |
|---|---|---|
| 21.9% | HU variance across 80–135 kVp | Nie & Molloi 2025 |
| 33 HU | Intra-individual variation from kernel choice | Lisi et al. 2024 |
| 7 HU | Swing from contrast timing | Wu et al. 2025 |
| 78% | Radiomic features unstable across perfusion phases | Wu et al. 2025 |
| 15 HU | Difference between scanners (same patients) | Boussoussou 2023 |
| +8 HU/step | Per kVp step | Boussoussou 2023 |
| −0.4 HU/kg/m² | BMI effect | Boussoussou 2023 |
| 3.6% | HU variance from patient size | Nie & Molloi 2025 |
| ~15 HU | The entire biological signal (healthy → inflamed) | Derived from −85 to −70 HU range |

### Key negative findings (establishes that the problem is real)
| Number | What it is | Source |
|---|---|---|
| p=0.93 | PCAT-plaque association after confounder correction | Boussoussou 2023 |
| p=0.236 | Colchicine effect on PCAT after 28 months | Fiolet (LoDoCo2 substudy) 2025 |

### Your results (what you bring)
| Number | What it is | Source |
|---|---|---|
| 0.01–0.64% | Water fraction RMSE across protocols | Nie & Molloi 2025 |
| Protocol-independent | Same composition → same water fraction | Nie & Molloi 2025 |

---

## 11. Competing Approaches and How to Discuss Them

### 11.1 FAI Score (Oxford, Antoniades)

**What it does**: Adjusts raw FAI for technical factors (kVp, kernel), anatomical factors (vessel size), and demographics (age, sex, BMI) using regression.

**Acknowledge**: "FAI Score represents a meaningful advance in standardisation, reducing protocol-dependent variability through statistical correction."

**Critique**: "However, regression-based correction assumes that confounders can be fully captured by the model's covariates. Residual confounding from unmeasured or incompletely modelled factors may persist. Material decomposition eliminates protocol dependence through physics rather than statistics, avoiding the assumption that all confounders have been identified and correctly modelled."

**Note**: FAI Score is proprietary (CaRi-Heart/Caristo Diagnostics), which limits independent validation.

### 11.2 PCATMA (Li et al. 2025)

**What it does**: Removes the fat HU threshold (−190 to −30), measuring mean attenuation of ALL tissue in the pericoronary VOI.

**Acknowledge**: "PCATMA addresses the limitation that the fat threshold may exclude relevant tissue."

**Critique**: "PCATMA remains an HU-based measurement and therefore inherits all protocol-dependent confounders."

### 11.3 PCAT Radiomics (ShuKun, multiple Chinese groups)

**What it does**: Extracts 93–1,103 texture features from the PCAT VOI using GLCM, GLRLM, GLSZM, etc.

**Acknowledge**: "Radiomic approaches capture spatial heterogeneity beyond mean HU, achieving strong internal validation (C-index up to 0.873)."

**Critique**: "However, all radiomic features are extracted from confounded HU data. Wu et al. (2025) showed that 78% of features are unstable across contrast perfusion phases. Enriching the feature space without addressing the underlying data limitation risks amplifying protocol-specific patterns rather than biological signals."

### 11.4 kVp Conversion Factors (Etter et al. 2022, Zurich)

**What it does**: Provides multiplication factors to convert FAI between kVp settings (e.g., multiply by 1.267 for 80 kVp to approximate 120 kVp).

**Acknowledge**: "Conversion factors address the largest single confounder and are straightforward to implement."

**Critique**: "This approach corrects only for tube voltage, leaving kernel, contrast timing, scanner, and patient size effects unaddressed."

---

## 12. Positioning Checklist Before Submission

Before submitting your paper, check that you have:

### Framing
- [ ] Acknowledged FAI's prognostic success (CRISP-CT, ORFAN) in the introduction
- [ ] NOT dismissed FAI as "wrong" or "useless"
- [ ] Positioned material decomposition as "complementary" or "addressing a recognised limitation"
- [ ] Cited Tan et al. 2023 (JACC) for the "not ready for prime time" framing
- [ ] Cited Chan & Antoniades 2025 (editorial) as evidence that even FAI proponents recognise the standardisation problem
- [ ] Used "proof-of-concept" or "feasibility" language for your simulation study

### Technical
- [ ] Clearly distinguished what is NEW vs. what was in Nie & Molloi 2025
- [ ] Used specific numbers (21.9%, 33 HU, p=0.93, p=0.236) rather than vague statements
- [ ] Followed the Oxford FAI protocol (−190 to −30 HU) for your FAI comparison
- [ ] Explained why you chose your specific tissue compositions for healthy/inflamed
- [ ] Showed both the FAI failure and the material decomposition success side-by-side

### Limitations (all must appear in your discussion)
- [ ] Simulation study, not clinical validation
- [ ] Simplified inflammation model
- [ ] No clinical outcome data
- [ ] Requires multi-energy CT hardware
- [ ] XCAT represents simplified anatomy

### Differentiation from previous paper
- [ ] New: XCAT phantom (anatomically realistic) vs. simple phantom
- [ ] New: Inflammation simulation (healthy vs. diseased)
- [ ] New: 4-material decomposition (water/lipid/collagen/iodine) vs. 3-material
- [ ] New: Direct demonstration that inflammation is detectable by composition but not by HU
- [ ] Referenced first paper for established methods, not re-derived

---

## 13. How the Field Defines "Healthy vs. Diseased" PCAT (and Why It Matters for Your Study)

This is critical for understanding the field and for positioning your simulation study. Every clinical PCAT study must define what counts as "inflamed" and what counts as "healthy." There are three fundamentally different strategies used in the literature, and **none of them use known tissue composition as ground truth.** This is the gap your study fills.

### 13.1 Strategy 1: Within-Patient, Vessel-Level Comparison (Most Common)

Compare PCAT around a "culprit" coronary lesion vs. a "non-culprit" segment **in the same patient**. The logic: the culprit caused the event, so the fat around it should be more inflamed than fat around a non-culprit vessel.

| Study | Population | How "culprit" was defined | Key finding |
|---|---|---|---|
| Li et al. 2025 (*J Comput Assist Tomogr*, n=120) | 80 ACS + 40 stable CAD | Invasive coronary angiography (ICA) — lesion causing the clinical event | FAI higher around culprit plaques than non-culprit; effect modified by stenosis severity |
| Yang et al. 2025 (*Eur J Radiol Open*, n=230) | NSTEMI patients | ICA — lesion responsible for the index NSTEMI event | FAI at culprit lesion ("FAIlesion") higher than non-culprit; proposed lesion-level FAI as better discriminator |
| Sagris et al. 2022 (meta-analysis, n=7,797) | 20 studies pooled | Varied — each study used its own culprit definition | FAI consistently higher around unstable vs. stable plaques |

**Limitation**: "Culprit" is defined by clinical presentation and angiography, not by tissue biology. A culprit lesion is one that caused symptoms — this is a clinical endpoint, not a direct measurement of inflammation. Two lesions with identical tissue composition could be classified differently depending on which one ruptured first.

### 13.2 Strategy 2: Outcome-Based Retrospective Stratification

Enrol a large cohort of CCTA patients, measure FAI at baseline, follow them for years, then retrospectively stratify by who had cardiovascular events (MACE/cardiac death) and who did not.

| Study | Population | Follow-up | How "diseased" was defined | Key finding |
|---|---|---|---|---|
| CRISP-CT (Oikonomou 2018, n=1,872) | CCTA patients | 5 years | Cardiac death or MACE during follow-up | FAI > −70.1 HU → HR 9.04 for cardiac death |
| ORFAN (Chan 2024, n=40,091) | CCTA patients | 2.7–7.7 years | All-cause mortality, cardiac death | 3 inflamed arteries vs. none → HR 29.8 |

**Limitation**: "Diseased" is defined **retrospectively by outcome**, not by a pre-defined biological state. Patients who had events are labelled "diseased" — but the inflammation that caused their event may have resolved, progressed, or been unrelated to PCAT. There is no tissue-level confirmation that FAI was measuring inflammation rather than some other process.

### 13.3 Strategy 3: Histological Ground Truth (Antonopoulos 2017 Only)

**This is the only study with true biological ground truth.** Patients undergoing cardiac surgery (bypass grafting, valve replacement) donated pericoronary fat biopsies at the time of surgery. The biopsied fat was matched to pre-operative CT scans.

| Study | Population | How "inflamed" was defined | Key findings |
|---|---|---|---|
| Antonopoulos et al. 2017 (*Sci Transl Med*, n=453) | Cardiac surgery patients | Histology — PPARγ expression, lipid droplet size, IL-6/TNF-α levels, UCP1 expression | Inflamed fat: reduced PPARγ (−2.3-fold), reduced FABP4 (−1.8-fold), increased IL-6 (+3.1-fold), increased TNF-α (+2.7-fold), smaller lipid droplets. HU correlated with these markers. |

**Limitation**: This is a surgical population (severe disease, often multivessel), not representative of the broader CCTA population. The biopsy is epicardial fat near the aortic root, not precisely the same pericoronary fat measured by FAI. Sample handling may alter tissue properties.

### 13.4 How "Culprit Lesion" is Operationally Defined

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

### 13.5 Why This Matters for YOUR Study (Critical Positioning)

Here is the key insight to use in your paper:

**No previous study defines "inflamed" vs. "healthy" by actual tissue composition.** Every clinical study defines "diseased" by:
- Clinical outcome (who had a heart attack → therefore "inflamed")
- Angiographic appearance (which lesion looks culprit → therefore "inflamed" around it)
- Histology (only Antonopoulos 2017, surgical population only)

**Your simulation study is unique because you define inflammation AT THE COMPOSITIONAL LEVEL.** You set the exact water/lipid fractions of healthy vs. inflamed PCAT, giving you something no clinical study has: **known ground truth tissue composition.**

This is a strength, not a limitation. You can use it in your discussion:

> "A fundamental challenge in validating CT-based PCAT measurements is the absence of compositional ground truth. Clinical studies define 'inflamed' pericoronary fat by clinical endpoints (ACS presentation, cardiovascular events) or invasive imaging (angiographic culprit identification), not by measured tissue composition. Consequently, the relationship between FAI and actual tissue water/lipid content remains incompletely characterised. Simulation provides the essential controlled conditions in which the tissue composition is known exactly, enabling direct evaluation of whether a given measurement can detect composition differences of clinical relevance."

### 13.6 Table: Comparison of "Healthy vs. Diseased" Definitions

| Criterion | Strategy 1 (Within-patient) | Strategy 2 (Outcome-based) | Strategy 3 (Histology) | **Your Study** |
|---|---|---|---|---|
| What defines "diseased"? | Culprit lesion (ICA/clinical) | Cardiac event (MACE/death) | Histological markers (PPARγ, IL-6) | **Known tissue composition (water/lipid fractions)** |
| Ground truth type | Clinical endpoint | Clinical endpoint | Biological endpoint | **Compositional ground truth** |
| Within-patient control? | Yes (non-culprit vessel) | No (between-patient) | Partial (adjacent tissue) | **Yes (same phantom, different composition)** |
| Protocol standardised? | Single-centre protocol | Multi-centre, variable | Single-centre | **Systematically varied** |
| Can confirm what FAI measures? | No — circular (FAI validates FAI) | No — correlation, not mechanism | Partially — matches HU to biology | **Yes — known input vs. measured output** |
| Limitations | Culprit ≠ most inflamed; just the one that ruptured | Reverse causation; confounders | Surgical population; biopsy location | Simulation; not clinical |

---

## Key References

### Must-cite (your argument depends on these)

1. Ridker PM et al. "CANTOS." *NEJM* 2017;377:1119–1131. [DOI](https://doi.org/10.1056/NEJMoa1707914)
2. Tardif JC et al. "COLCOT." *NEJM* 2019;381:2497–2505. [DOI](https://doi.org/10.1056/NEJMoa1912388)
3. Nidorf SM et al. "LoDoCo2." *NEJM* 2020;383:1838–1847. [DOI](https://doi.org/10.1056/NEJMoa2021372)
4. Antonopoulos AS et al. "Detecting coronary inflammation by imaging perivascular fat." *Sci Transl Med* 2017;9:eaal2658. [DOI](https://doi.org/10.1126/scitranslmed.aal2658)
5. Oikonomou EK et al. "CRISP-CT." *Lancet* 2018;392:929–939. [DOI](https://doi.org/10.1016/S0140-6736(18)31114-0)
6. Chan K et al. "ORFAN extended." *Lancet* 2024. [DOI](https://doi.org/10.1016/S0140-6736(24)01811-9)
7. Nie S, Molloi S. "Water and lipid composition of PVAT." *Int J Cardiovasc Imaging* 2025;41:1091–1101. [DOI](https://doi.org/10.1007/s10554-025-03358-5)

### Must-cite (establishing the measurement problem)

8. Boussoussou M et al. "Patient and imaging characteristics affect PCAT." *JCCT* 2023. [DOI](https://doi.org/10.1016/j.jcct.2022.09.006)
9. Lisi C et al. "Kernel and reconstruction effects on FAI." *Eur Radiol* 2024. [DOI](https://doi.org/10.1007/s00330-024-11132-5)
10. Wu C et al. "Perfusion confounds on PCAT." *J Clin Med* 2025. [DOI](https://doi.org/10.3390/jcm14030769)
11. Fiolet ATL et al. "Colchicine does not change PCAT (LoDoCo2 substudy)." *Heart* 2025. [DOI](https://doi.org/10.1136/heartjnl-2024-325527)
12. Hell MM et al. "Pericoronary adipose tissue density — partial volume effects." *JCCT* 2016;10:52–60. [DOI](https://doi.org/10.1016/j.jcct.2015.07.011)
13. Tremamunno G et al. "PCD vs. EID CT — FAI not comparable." *Acad Radiol* 2025;32(3). [DOI](https://doi.org/10.1016/j.acra.2024.11.055)

### Should-cite (strengthens your argument)

14. Tan N et al. "PCAT: not ready for prime time." *JACC* 2023. [DOI](https://doi.org/10.1016/j.jacc.2022.12.021)
15. Chan & Antoniades. "Need for standardised measurement." 2025. (editorial) [DOI](https://doi.org/10.1093/eurheartj/ehaf012)
16. Ma R et al. "PCAT reference values." *Eur Radiol* 2020. [DOI](https://doi.org/10.1007/s00330-020-07069-0)
17. Etter M et al. "kVp conversion factors." *Eur Radiol* 2022. [DOI](https://doi.org/10.1007/s00330-022-09274-5)
18. Sagris M et al. "FAI meta-analysis." *Eur Heart J Cardiovasc Imaging* 2022. [DOI](https://doi.org/10.1093/ehjci/jeac174)
19. Shang J et al. "PCAT radiomics multicentre." *Cardiovasc Diabetol* 2025. [DOI](https://doi.org/10.1186/s12933-025-02913-3)

### Optional but useful (broader context)

20. Ross R. "Atherosclerosis — an inflammatory disease." *NEJM* 1999;340:115–126. [DOI](https://doi.org/10.1056/NEJM199901143400207)
21. Alvarez RE, Macovski A. "Energy-selective reconstructions." *Phys Med Biol* 1976;21:733–744. [DOI](https://doi.org/10.1088/0031-9155/21/5/002)
22. Li et al. "PCATMA vs FAI." *QIMS* 2025. [DOI](https://doi.org/10.21037/qims-24-828)
