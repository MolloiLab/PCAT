# Clinician Collaborator Instructions: PCAT Patient Selection & Data Collection

**Study**: Material Decomposition of Pericoronary Adipose Tissue Using Photon-Counting CT  
**PI**: Sabee Molloi, PhD — University of California, Irvine  
**Student Investigator**: Shu Nie  
**Date**: March 2026  
**Version**: 1.0

---

## Purpose of This Document

This is a **retrospective study** using existing PCCT CCTA scans already in your clinical database. We are NOT recruiting new patients or ordering new scans.

This document provides step-by-step instructions for the collaborating clinician who will help review existing scans, identify eligible patients, and extract the required clinical data from electronic medical records. The imaging analysis (material decomposition, FAI measurement) will be performed by the engineering team — **your role is patient identification, clinical data extraction, and coronary disease classification from existing records and images.**

---

## Study Overview (Brief)

We are comparing two methods of measuring pericoronary adipose tissue (fat around coronary arteries):

1. **FAI (Fat Attenuation Index)** — the current standard, measures Hounsfield Units of pericoronary fat
2. **Material decomposition** — our new method, measures the actual water/lipid composition of pericoronary fat

We need patients scanned on **photon-counting CT (PCCT)** with coronary CTA protocol. We need two types of comparisons:

- **Primary**: Within the same patient — compare fat around a diseased vessel vs. fat around a clean vessel
- **Secondary**: Between patients — compare patients with no coronary disease vs. patients with high-risk plaques

---

## What We Need From You

### Step 1: Retrospective Chart Review — Identify Eligible Patients

From your existing PCCT CCTA database, identify patients who were previously scanned and who meet **ALL** inclusion criteria and **NONE** of the exclusion criteria.

#### Inclusion Criteria (ALL must be met)

- [ ] Age ≥ 18 years
- [ ] Clinically indicated coronary CTA (not research-only scan)
- [ ] Scanned on photon-counting CT (Siemens NAEOTOM Alpha or equivalent)
- [ ] Standard coronary CTA protocol with contrast enhancement
- [ ] Multi-energy/spectral reconstruction data available in PACS
- [ ] Adequate image quality for pericoronary fat assessment (see quality notes below)

#### Exclusion Criteria (ANY one disqualifies)

- [ ] Prior coronary artery bypass grafting (CABG)
- [ ] Prior percutaneous coronary intervention (PCI) with stent(s)
- [ ] Pacemaker or implantable cardioverter-defibrillator (ICD)
- [ ] Prosthetic heart valve
- [ ] Known active myocarditis or pericarditis
- [ ] Known active vasculitis (e.g., Takayasu, Kawasaki)
- [ ] Active systemic infection at time of scan
- [ ] Known active malignancy (any type)
- [ ] Anomalous coronary artery origin from the wrong sinus
- [ ] Severe motion artifacts making coronary assessment unreliable
- [ ] Persistent or permanent atrial fibrillation (motion artifact confounder)
- [ ] Scan performed without contrast (non-contrast only)
- [ ] Congenital heart disease with altered coronary anatomy
- [ ] Pregnant at time of scan
- [ ] eGFR < 30 mL/min/1.73m² at time of scan (unless on dialysis)
- [ ] On systemic anti-inflammatory therapy at time of scan (colchicine, biologics, chronic corticosteroids) — see note below

#### Image Quality Notes

"Adequate image quality" means:
- The proximal and mid segments of LAD, LCx, and RCA are assessable
- Pericoronary fat is visible (not obscured by artifact, pericardial effusion, or minimal epicardial fat)
- If you can assign a CAD-RADS score confidently, the image quality is adequate

---

### Step 2: Classify Each Patient's Coronary Disease

For every eligible patient, please provide:

#### A. CAD-RADS Score (per SCCT CAD-RADS 2.0)

| CAD-RADS | Stenosis | Description |
|---|---|---|
| **0** | 0% | No plaque or stenosis |
| **1** | 1–24% | Minimal stenosis or plaque with no stenosis |
| **2** | 25–49% | Mild stenosis |
| **3** | 50–69% | Moderate stenosis |
| **4A** | 70–99% | Severe stenosis |
| **4B** | 70–99% in left main OR ≥ 70% in 3 vessels | Severe stenosis, left main or 3-vessel |
| **5** | 100% | Total occlusion |

#### B. Coronary Dominance

- Right-dominant / Left-dominant / Co-dominant

This affects which vessel supplies the posterior descending artery and is required for proper risk stratification.

#### C. Per-Vessel Assessment (Critical — We Need This for Each Vessel)

For **each** of the three major coronary arteries (LAD, LCx, RCA), please record:

| Data Point | LAD | LCx | RCA |
|---|---|---|---|
| Maximum stenosis (%) | ___ | ___ | ___ |
| Plaque present? (Y/N) | ___ | ___ | ___ |
| Plaque type (calcified / non-calcified / mixed) | ___ | ___ | ___ |
| Positive remodeling? (RI > 1.1) (Y/N) | ___ | ___ | ___ |
| Low-attenuation plaque (< 30 HU)? (Y/N) | ___ | ___ | ___ |
| Spotty calcification (< 3 mm)? (Y/N) | ___ | ___ | ___ |
| Napkin-ring sign? (Y/N) | ___ | ___ | ___ |
| Pericoronary fat assessable? (Y/N) | ___ | ___ | ___ |

**Why per-vessel?** Our primary analysis compares pericoronary fat composition around a diseased vessel vs. a clean vessel in the same patient. We need to know which vessels are diseased and which are clean.

#### D. Which Vessel is the "Culprit" (if applicable)

If the patient presented with ACS (STEMI, NSTEMI, unstable angina):
- Which vessel was the culprit? (based on ICA if available, or clinical presentation + CT features)
- Was ICA performed? (Y/N)
- If ICA: TIMI flow grade at culprit? Thrombus visible? (Y/N)

If the patient did NOT present with ACS:
- Mark "N/A" — no culprit vessel designation needed

#### E. Scan-Related Clinical Data

These are clinical variables at the time of scan that affect image quality and pericoronary fat measurement:

| Variable | Value |
|---|---|
| Heart rate during scan (bpm) | ___ |
| Beta-blocker given before scan? (Y/N) | ___ |
| If yes: drug, dose, route, timing | ___ |
| Nitroglycerin given before scan? (Y/N) | ___ |

**Note**: Technical scan parameters (kVp, mAs, contrast volume, injection rate, reconstruction kernel) will be extracted from DICOM headers by the engineering team — you do NOT need to collect these.

---

### Step 3: Extract Clinical Data Per Patient

For each eligible patient, please fill in the following. All data should reflect the patient's status **at the time of the CCTA scan**.

#### Demographics

| Variable | Value |
|---|---|
| Age (years) | ___ |
| Sex (M/F) | ___ |
| Height (cm) | ___ |
| Weight (kg) | ___ |
| BMI (kg/m²) | ___ |
| Race/Ethnicity | ___ |

#### Cardiovascular Risk Factors

| Risk Factor | Present? (Y/N) | Details |
|---|---|---|
| Hypertension | ___ | On medication? (Y/N) |
| Diabetes mellitus | ___ | Type 1 / Type 2; HbA1c if available |
| Hyperlipidemia / Dyslipidemia | ___ | On statin? (Y/N); which statin, dose |
| Current smoker | ___ | Pack-years if available |
| Former smoker | ___ | Years since quit |
| Family history of premature CAD | ___ | First-degree relative, age < 55 (M) or < 65 (F) |
| Obesity (BMI ≥ 30) | ___ | |

#### Clinical Presentation (Indication for CCTA)

- [ ] Chest pain — typical angina
- [ ] Chest pain — atypical
- [ ] Dyspnoea
- [ ] Abnormal stress test
- [ ] Risk stratification (asymptomatic, high risk)
- [ ] Pre-operative cardiac evaluation
- [ ] ACS work-up (STEMI / NSTEMI / unstable angina)
- [ ] Other: _______________

#### Medications at Time of Scan

| Medication Class | Taking? (Y/N) | Specific Drug & Dose (if available) |
|---|---|---|
| Statin | ___ | ___ |
| Aspirin | ___ | ___ |
| Beta-blocker | ___ | ___ |
| ACE inhibitor / ARB | ___ | ___ |
| Calcium channel blocker | ___ | ___ |
| Anticoagulant (warfarin, DOAC) | ___ | ___ |
| Anti-inflammatory (colchicine, NSAIDs) | ___ | ___ |
| Metformin / other diabetes meds | ___ | ___ |

#### Laboratory Values (if available, closest to scan date)

| Lab | Value | Date |
|---|---|---|
| hsCRP (mg/L) | ___ | ___ |
| Total cholesterol (mg/dL) | ___ | ___ |
| LDL (mg/dL) | ___ | ___ |
| HDL (mg/dL) | ___ | ___ |
| Triglycerides (mg/dL) | ___ | ___ |
| HbA1c (%) | ___ | ___ |
| Troponin (ng/mL) | ___ | ___ |
| BNP or NT-proBNP (pg/mL) | ___ | ___ |
| IL-6 (pg/mL) | ___ | ___ |
| Creatinine (mg/dL) / eGFR | ___ | ___ |

**Note**: hsCRP is the most important lab value for our study (systemic inflammation marker). If only one lab is available, prioritise hsCRP.

#### Coronary Calcium Score

| Variable | Value |
|---|---|
| Total Agatston score | ___ |
| LAD calcium score (if available) | ___ |
| LCx calcium score (if available) | ___ |
| RCA calcium score (if available) | ___ |

**Note**: Total Agatston score is the primary requirement. Per-vessel scores are helpful but not essential.

---

### Step 4: Group Assignment (We Will Do This Together)

Based on your coronary assessment, patients will fall into groups. **You do not need to assign groups yourself** — we will review together. But for reference:

| Group | Criteria | Minimum target n |
|---|---|---|
| **Group A — No disease** | CAD-RADS 0, calcium score 0, no plaque in any vessel | ≥ 30 |
| **Group B — Non-obstructive** | CAD-RADS 1–2 (plaque present, < 50% stenosis), no high-risk features | ≥ 30 |
| **Group C — Obstructive / High-risk** | CAD-RADS 3–5, OR ≥ 2 high-risk plaque features in any vessel | ≥ 30 |

**For within-patient analysis**: We especially need patients who have disease in ONE vessel but a clean vessel elsewhere (e.g., LAD stenosis but clean RCA). Please flag these patients.

---

## Frequently Asked Questions

**Q: What if a patient has borderline image quality?**  
A: Include them provisionally and note "borderline quality" in the comments. We will review the images together before final inclusion.

**Q: What if lab values are not available?**  
A: Include the patient anyway. Lab values are secondary. The imaging data is primary. Leave lab fields blank.

**Q: How far back can the lab values be from the scan date?**  
A: Ideally within 30 days of the CCTA. Up to 90 days is acceptable. Beyond that, note the date but we may not use the value.

**Q: Should I include patients with prior MI (but no stent)?**  
A: Yes — as long as they have no stent (PCI) or bypass (CABG). Prior MI without intervention is acceptable. Note the MI date and territory.

**Q: What about patients on colchicine or other anti-inflammatory therapy?**  
A: **Exclude them from the primary analysis.** Anti-inflammatory drugs directly affect pericoronary fat composition, which is the variable we are measuring. However, please still flag these patients separately — they may be useful for a sensitivity analysis. Record the drug, dose, and duration if you identify them.

**Q: How do I report plaque that's hard to classify?**  
A: Use your best clinical judgment. If uncertain about a high-risk feature (e.g., questionable napkin-ring sign), mark it as "uncertain" rather than Y or N. We can review together.

**Q: What counts as "anomalous coronary artery origin"?**  
A: Origin of the RCA or left coronary from the wrong aortic sinus (e.g., RCA from left sinus, LCA from right sinus). Normal anatomic variants (e.g., absent LCx with dominant RCA, or LCx arising from RCA) should be noted but do NOT exclude the patient.

---

## Data Delivery Format

Please provide data in a **spreadsheet** (Excel or CSV). One row per patient. Use the column headers from the tables above. Use de-identified patient IDs (MRN should NOT appear in the spreadsheet — use a separate linking log kept securely per IRB protocol).

For the imaging data (DICOM files), we will coordinate separately for transfer from PACS.

---

## Timeline & Contact

| Milestone | Target Date |
|---|---|
| Begin retrospective chart review | TBD |
| Complete eligible patient list | TBD |
| Complete clinical data extraction from EMR | TBD |
| Joint review of group assignments | TBD |

**Questions?** Contact Shu Nie at [email] or Sabee Molloi at [email].

---

## Acknowledgment

Your contribution to patient identification, clinical data extraction, and coronary disease classification is essential to this study and will be recognised with co-authorship per ICMJE criteria.
