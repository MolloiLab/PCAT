# Coronary Artery Inflammation: Comprehensive Literature Review

**Project**: PCAT Segmentation Pipeline — MolloiLab  
**Date**: March 2026  
**Scope**: Comprehensive review of coronary artery inflammation biology, pericoronary adipose tissue (PCAT) as a biomarker, clinical evidence base, research trajectory, study design patterns, and patient selection methods — synthesised from ~103 papers.

---

## 1. Clinical Motivations for Investigating Pericoronary Adipose Tissue

### 1.1 The Residual Cardiovascular Risk Problem

Despite optimal lipid-lowering therapy with statins, a substantial **residual cardiovascular risk** persists. The CANTOS trial (Ridker et al., *NEJM* 2017, n=10,061) proved that this residual risk is driven by **inflammation independent of LDL cholesterol**: canakinumab (IL-1β antibody) reduced MACE by 15% without affecting LDL levels. This established inflammation as a direct, causal therapeutic target.

The clinical need is therefore to **identify patients with active coronary inflammation** who would benefit from anti-inflammatory therapy (colchicine, canakinumab) — but no widely available non-invasive test existed to localise inflammation to specific coronary arteries until FAI.

### 1.2 Why PCAT Is Uniquely Informative

Pericoronary adipose tissue provides a **vessel-specific, non-invasive readout of coronary inflammation** that systemic biomarkers cannot:

| Biomarker | Signal Source | Limitation |
|---|---|---|
| hsCRP (serum) | Systemic inflammation | Non-specific — elevated in infection, obesity, autoimmune disease |
| IL-6 (serum) | Systemic cytokine burden | Cannot localise to specific coronary artery |
| 18F-FDG PET | Metabolically active inflammation | Poor spatial resolution, cardiac/respiratory motion, myocardial uptake confounds |
| **FAI (CCTA)** | **Per-vessel local coronary inflammation** | Specific to individual coronary artery segment; spatial resolution to single vessel |

FAI is the only clinical measurement that localises inflammation to a **specific coronary artery segment** non-invasively. A stenotic LAD with high FAI is a fundamentally different risk entity than the same stenosis with low FAI.

### 1.3 The Treatment Pathway FAI Enables

The colchicine trials (COLCOT: Tardif et al., *NEJM* 2019, −23% MACE post-MI; LoDoCo2: Nidorf et al., *NEJM* 2020, −31% MACE in chronic CAD) established a cheap, safe anti-inflammatory agent. Combined with FAI, this creates a practical clinical pathway:

```
CCTA acquired → FAI computed per-vessel → FAI > −70.1 HU detected
        ↓
Classification: Active coronary inflammation
        ↓
Clinical action: Consider colchicine / statin intensification / earlier follow-up
```

This pathway is already deployed clinically via CaRi-Heart (Caristo Diagnostics, Oxford, UK) — the FDA-cleared commercial implementation of the Oxford FAI methodology.

### 1.4 Motivating Gaps in Current FAI Methodology

Despite clinical deployment, FAI has critical technical limitations that motivate our research:

1. **Protocol dependence**: FAI (HU-based) varies with tube voltage (21.9% variance across 80–135 kV; Nie & Molloi 2025), patient size (3.6% variance), reconstruction kernel (up to 33 HU intra-individual variation; Lisi et al. 2025), and iodine contrast timing (~7 HU swing; Wu et al. 2025)
2. **No universal threshold**: The −70.1 HU cutoff was validated at 120 kVp on conventional CT; it does not transfer to spectral/PCD-CT, VMI, or different reconstruction algorithms without recalibration
3. **Confounding by non-inflammatory factors**: Coronary CTA perfusion dynamics, cardiac phase, and patient body habitus all affect HU values independently of inflammation

These limitations directly motivate the **material decomposition approach** our lab is developing — protocol-independent quantification of tissue composition rather than protocol-dependent HU measurement.

---

## 2. Paradigm Shift: Atherosclerosis as an Inflammatory Disease

### 2.1 The Historical View (Lipid-Centric)

Until the 1990s, atherosclerosis was conceptualised primarily as a **lipid storage disorder**: LDL cholesterol accumulates in the arterial intima, forms fatty streaks, and progressively obstructs the lumen. Treatment focused on lipid lowering (statins). While lipid lowering reduces MACE by ~35%, a large residual cardiovascular risk remains even after optimal statin therapy. This gap drove the search for alternative pathways.

### 2.2 The Inflammatory Hypothesis

> Ross R. "Atherosclerosis — an inflammatory disease." *New England Journal of Medicine*. 1999;340:115–126.

Ross established the **"response-to-injury" hypothesis**: the primary trigger is endothelial injury (from oxidised LDL, hemodynamic shear stress, hypertension, smoking), which activates an inflammatory cascade:

1. Endothelial activation → upregulation of adhesion molecules (VCAM-1, ICAM-1, E-selectin)
2. Monocyte recruitment → differentiation into macrophages
3. Macrophages engulf oxidised LDL → foam cells
4. Foam cells secrete pro-inflammatory cytokines (IL-1β, IL-6, TNF-α)
5. Smooth muscle cell migration and proliferation → fibrous cap formation
6. Plaque vulnerability determined by cap thickness vs. inflammatory burden

### 2.3 Causal Proof: The CANTOS Trial

> Ridker PM et al. *NEJM* 2017;377:1119–1131. n=10,061.

CANTOS enrolled patients with prior MI and elevated hsCRP. Canakinumab (IL-1β antibody) or placebo was given on top of optimal statin therapy:

- **Primary result**: MACE reduced by **15%** at 150 mg (p=0.031)
- Effect was **independent of LDL cholesterol** (LDL did not change)
- Dose-dependent reduction in hsCRP, IL-6
- First proof that targeting inflammation — not lipids — reduces cardiovascular events

### 2.4 The Inflammasome Pathway

> Libby P et al. *Circulation* 2021; *Nature* 2021.

The **NLRP3 inflammasome** is the central molecular sensor in atherosclerotic plaques:

```
Cholesterol crystals / oxidised LDL
        ↓
  NLRP3 inflammasome activation
        ↓
  Caspase-1 activation
        ↓
  IL-1β + IL-18 maturation & secretion
        ↓
  Downstream: IL-6, CRP, MMP secretion
        ↓
  Fibrous cap thinning → plaque vulnerability
```

NLRP3 is detectable in perivascular fat macrophages adjacent to vulnerable plaques — directly linking the fat compartment to the vessel wall inflammatory milieu that FAI measures.

---

## 3. Perivascular Adipose Tissue as a Paracrine Signalling Hub

### 3.1 Anatomy

**Pericoronary adipose tissue (PCAT)** is the adipose tissue immediately surrounding the coronary arteries, between the coronary vessels and the epicardial surface:
- Distinct from **epicardial adipose tissue (EAT)**: the full fat depot within the pericardial sac
- Distinct from **paracardial fat**: fat outside the pericardium
- Lacks a fascial barrier between the fat and the adventitia → direct exchange pathway
- Vascularised by the vasa vasorum, sharing the same microvascular supply as the adventitia

### 3.2 Vasocrine Signalling: Vessel Wall → Fat

When the coronary artery is inflamed:

1. Adventitial macrophages and smooth muscle cells secrete **IL-6, TNF-α, CXCL10, VEGF**
2. These mediators diffuse outward into adjacent PCAT
3. IL-6 and TNF-α suppress adipocyte differentiation:
   - Inhibit **PPARγ** (master transcription factor for fat cell maturation)
   - Inhibit **C/EBPα** (co-factor for adipogenesis)
   - Inhibit **FABP4** (fatty acid binding protein, marker of mature adipocyte)
4. Adipocytes remain immature, smaller, with less stored lipid
5. **Result on CT**: fat voxels shift from lipid-dominant (HU ≈ −90 to −70) toward more aqueous composition (HU ≈ −60 to −40) — this is the FAI signal

The FAI increase reflects a **genuine molecular phenotypic shift** in the fat cells, validated histologically by Antonopoulos et al. (2017, *Science Translational Medicine*, n=453 cardiac surgery patients): perivascular fat sampled adjacent to inflamed coronary segments showed reduced lipid droplet size (p<0.001), reduced PPARγ (−2.3-fold), reduced FABP4 (−1.8-fold), and increased IL-6 (+3.1-fold) and TNF-α (+2.7-fold).

### 3.3 Paracrine Signalling: Fat → Vessel Wall

In obesity and metabolic syndrome, the PVAT itself becomes dysfunctional:

| Normal PVAT | Dysfunctional PVAT (obese/inflamed) |
|---|---|
| Secretes **adiponectin** (anti-inflammatory, vasodilatory) | Adiponectin ↓ |
| Secretes **NO** (endothelial relaxation) | NO ↓ |
| Secretes **omentin** (insulin-sensitising) | Leptin ↑ |
| Low macrophage infiltration (M2 phenotype) | High macrophage infiltration (M1 phenotype) |
| — | IL-6, TNF-α, FABP4 ↑ |
| — | Reactive oxygen species ↑ |

This creates a **bidirectional amplification loop**: inflamed vessels trigger PCAT dysfunction, which in turn secretes pro-inflammatory mediators that further accelerate plaque development.

### 3.4 Vasa Vasorum and Microvascular Inflammation

The **vasa vasorum** — the microvascular network supplying the coronary arterial wall — plays a key role in PCAT inflammation. Studies using micro-CT and histology (Kwon et al. 2015; Ritman & Lerman 2007) have shown:

- Neovascularisation of vasa vasorum (adventitial angiogenesis) precedes and promotes atherosclerotic plaque development
- Inflamed vasa vasorum provide the route for inflammatory cell infiltration into the vessel wall and adjacent PCAT
- PCAT surrounding vessels with dense vasa vasorum networks shows higher HU (more inflammation)
- This microvasculature is the physical conduit for the vasocrine signalling described above

---

## 4. PCAT vs. Epicardial Adipose Tissue (EAT)

### 4.1 Measurement Differences

| Feature | PCAT | EAT |
|---|---|---|
| **Spatial scope** | ~3–5 mm shell around specific vessel segment | Entire pericardial sac |
| **Measurement unit** | Mean HU (attenuation = FAI) | Total volume (cm³) |
| **Clinical signal** | Per-vessel acute inflammatory state | Whole-heart chronic metabolic risk |
| **Segmentation** | Vessel-specific VOI (centerline-based) | Pericardial sac segmentation |
| **Key paper** | Oikonomou 2018, *Lancet* | Iacobellis, multiple reviews |
| **Commercial tool** | CaRi-Heart (Caristo), ShuKun PCAT | Multiple EAT volume tools |

### 4.2 Are They Measuring the Same Thing?

No. Correlation between EAT volume and RCA-FAI is moderate at best (r ≈ 0.3–0.4). A patient with:
- **High EAT volume, low FAI**: metabolically obese, but coronary arteries not actively inflamed
- **Low EAT volume, high FAI**: lean but with focal plaque-driven coronary inflammation

Both PCAT and EAT are independently associated with MACE in multivariate models — they measure complementary biological processes.

---

## 5. Spatial Heterogeneity of Coronary Inflammation

### 5.1 Why Proximal Segments Matter

The proximal coronary segments (LAD 0–40 mm, LCX 0–40 mm, RCA 10–50 mm) are the clinical focus because:
1. **Most plaques form here**: hemodynamic shear stress patterns at bifurcations and proximal curves create preferential plaque deposition
2. **Clinical consequence**: proximal stenoses cause more downstream ischemia
3. **CT resolution**: proximal vessels are larger (3–5 mm diameter) → better SNR for FAI

### 5.2 Lesion-Specific PCAT

Rather than fixed proximal segments, measuring PCAT adjacent to each individual plaque provides:
- **Higher specificity**: PCAT around a stable fibrous plaque may be low even in the same vessel as an unstable plaque with high PCAT
- **Better MACE prediction**: the PCAT signal is strongest immediately adjacent to the vulnerable plaque (Huang et al. 2025, ShuKun)

### 5.3 RCA vs. LAD vs. LCX: Different Biology

The clinical literature focuses primarily on RCA-FAI because:
- RCA has the most pericoronary fat (largest fat depot, cleaner VOI)
- LAD runs in the anterior interventricular groove — also well-studied
- LCX runs in the atrioventricular groove adjacent to the left atrial wall → VOI contamination more common

Reference values (Ma et al. 2020, Groningen): LAD −92.4 HU, LCX −88.4 HU, RCA −90.2 HU. FAI increases linearly with tube voltage.

---

## 6. Research Trajectory: Timeline and Key Research Groups

### 6.1 Chronological Development

| Year | Milestone | Group | Key Paper |
|---|---|---|---|
| 1999 | Atherosclerosis defined as inflammatory disease | Ross (multiple) | Ross R, *NEJM* 1999 |
| 2005 | PVAT macrophage infiltration characterised | Henrichot et al. | *ATVB* 2005 |
| 2007–2015 | Vasa vasorum role in atherosclerosis established | Ritman & Lerman (Mayo) | Multiple reviews |
| 2016–2017 | Vasospastic angina linked to PVAT inflammation (18F-FDG PET) | Shimokawa group (Sendai/Tohoku) | Ohyama et al. 2016–2017 |
| 2017 | CANTOS trial proves causal role of IL-1β in MACE | Ridker (Brigham) | *NEJM* 2017 |
| 2017 | FAI concept introduced with histological validation (n=453) | Antoniades (Oxford) | Antonopoulos et al., *Sci Transl Med* 2017 |
| 2018 | **CRISP-CT**: FAI validated as prognostic biomarker (n=1,872, HR 9.04) | Antoniades/Oikonomou (Oxford), Marwan/Achenbach (Erlangen) | Oikonomou et al., *Lancet* 2018 |
| 2019 | COLCOT trial: colchicine reduces MACE post-MI (−23%) | Tardif (Montreal Heart) | *NEJM* 2019 |
| 2020 | LoDoCo2: colchicine in chronic CAD (−31% MACE) | Nidorf | *NEJM* 2020 |
| 2020 | PCAT reference values established per vessel, per kV | Ma, Vliegenthart (Groningen) | Ma et al. 2020 |
| 2021 | Lab's material decomposition for coronary plaque (DECT) | Ding, Molloi (UCI) | Ding et al. 2021 |
| 2022 | Phantom study: PCATMA affected by kVp and reconstruction | Etter et al. | Etter et al. 2022 |
| 2022 | Meta-analysis: FAI higher in unstable vs stable plaques (n=7,797, 20 studies) | Sagris et al. | Sagris et al. 2022 |
| 2022–2024 | PCD-CT (NAEOTOM Alpha) FAI studies begin | Zurich (Alkadhi, Eberhard, Mergen), Mannheim (Ayx, Froelich) | Multiple 2022–2024 |
| 2023 | ORFAN trial: CaRi-Heart AI-FAI outperforms conventional risk scores (n=3,324) | Oikonomou (Oxford) | *Nat CV Res* 2023 |
| 2024–2025 | PCAT confounds quantified: perfusion timing, kernel effects | Wu, Rajagopalan (Case Western); Lisi et al. | Wu et al. 2025; Lisi et al. 2025 |
| 2025 | XCAT 3.0 with 2500+ phantoms for virtual imaging trials | Dahal, Segars (Duke) | Dahal et al. 2025 |
| 2025 | Computational coronary plaques via DC-GAN for virtual imaging | Sauer, Samei (Duke CVIT) | Sauer et al. 2024 |
| 2025 | **Lab's previous paper**: water-lipid-protein decomposition for PVAT (simulation) | Nie, Molloi (UCI) | *Int J Cardiovasc Imaging* 2025;41:1091–1101 |
| 2025 | PCAT radiomics with 93-feature ML for MACE prediction | ShuKun/Huang et al. | Huang et al. 2025 |
| 2025–2026 | Body composition transformation in XCAT phantoms | Salinas et al. (Duke) | Salinas et al. 2025 |
| 2026 | Truth-based physics-informed material composition in spectral CT | Valand et al. | Valand et al. 2026 |
| 2026 | **Current study**: XCAT phantom + material decomposition for PCAT inflammation | Nie, Molloi (UCI) | *In preparation* |

### 6.2 Major Research Groups

#### Oxford / Antoniades Group
**Lead**: Charalambos Antoniades, Evangelos Oikonomou  
**Contributions**: Defined FAI, conducted CRISP-CT and ORFAN trials, commercialised CaRi-Heart (Caristo Diagnostics). The foundational group for PCAT as a clinical biomarker.  
**Key papers**: Antonopoulos et al. *Sci Transl Med* 2017; Oikonomou et al. *Lancet* 2018; Oikonomou et al. *Nat CV Res* 2023

#### Erlangen / Achenbach Group
**Lead**: Stephan Achenbach, Mohamed Marwan  
**Contributions**: CRISP-CT derivation cohort, early PCD-CT FAI studies.  
**Key papers**: Oikonomou et al. *Lancet* 2018 (co-authors); Engel et al. *J Clin Med* 2026

#### Cedars-Sinai / Monash (Dey, Lin, Wong, Nicholls)
**Contributions**: PCAT radiomics, ML models for MACE prediction, statin effects on PCAT, integration with CT-FFR.  
**Key papers**: Multiple 2019–2025 on PCAT radiomics and ML

#### Zurich / Alkadhi Group
**Lead**: Hatem Alkadhi, Katharina Eberhard, André Mergen  
**Contributions**: Systematic evaluation of PCAT on PCD-CT (NAEOTOM Alpha), kernel and reconstruction effects on FAI.  
**Key papers**: Eberhard et al. 2022–2025; Mergen et al. 2022–2025 (NAEOTOM Alpha series)

#### Groningen / Vliegenthart Group
**Lead**: Rozemarijn Vliegenthart, Riemer Ma  
**Contributions**: Established PCAT reference values per vessel per kV, low-kV imaging effects, lesion-specific PCAT.  
**Key papers**: Ma et al. 2020 (reference values); van Assen et al. 2021

#### Case Western / Rajagopalan Group
**Lead**: Sanjay Rajagopalan, Chris Wu, David Wilson  
**Contributions**: Quantified PCAT confounds — contrast perfusion timing, volume changes, radiomic feature instability.  
**Key papers**: Wu et al. 2025 (perfusion confounds: 7 HU timing swing, ~15% volume change, 78% radiomic features change >10%)

#### Duke CVIT / Segars-Samei Group
**Lead**: W. Paul Segars, Ehsan Samei, Ehsan Abadi  
**Contributions**: XCAT phantom development (3.0 with 2500+ phantoms), computational coronary plaques (DC-GAN), virtual imaging trials framework.  
**Key papers**: Dahal et al. 2025 (XCAT 3.0); Sauer et al. 2024 (computational plaques); Salinas et al. 2025 (body composition)

#### Sendai / Shimokawa Group (Tohoku University)
**Lead**: Hiroaki Shimokawa  
**Contributions**: First to link PVAT inflammation to vasospastic angina using 18F-FDG PET, non-atherosclerotic coronary inflammation.  
**Key papers**: Ohyama et al. 2016–2017

#### Mannheim / Ayx-Froelich Group
**Lead**: Isabelle Ayx, Matthias Froelich, Nörenberg  
**Contributions**: PCD-CT radiomic texture analysis of PCAT, spectral imaging effects.  
**Key papers**: Ayx et al. 2022–2024

#### MolloiLab / UCI (Our Group)
**Lead**: Sabee Molloi, Anqi Nie  
**Contributions**: Material decomposition for coronary plaque (DECT, 2021), water-lipid-protein decomposition for PVAT (2025), current XCAT-based simulation study.  
**Key papers**: Ding et al. 2021; Nie & Molloi 2025 (*Int J Cardiovasc Imaging* 41:1091–1101); current study in preparation

---

## 7. Study Design Patterns in PCAT Research

### 7.1 Study Types Used

| Study Type | Proportion | Examples |
|---|---|---|
| **Retrospective cohort** | ~60% | CRISP-CT, most single-centre PCAT studies |
| **Prospective cohort** | ~15% | ORFAN, some NAEOTOM Alpha studies |
| **Meta-analysis / systematic review** | ~10% | Sagris et al. 2022 (20 studies, n=7,797) |
| **Phantom / simulation** | ~10% | Etter et al. 2022, Nie & Molloi 2025, current study |
| **Case-control** | ~5% | ACS vs. stable angina comparisons |

### 7.2 PCAT Measurement Methodology

Nearly all clinical PCAT studies follow the **Oxford/CRISP-CT protocol**:
- Fat HU window: −190 to −30 HU
- VOI: outer vessel wall + 1× mean vessel diameter, proximal 40 mm (LAD/LCX) or 10–50 mm (RCA)
- Primary metric: Mean HU of fat-range voxels = FAI
- Threshold: −70.1 HU (high-risk)

Variations:
- **Lesion-specific PCAT** (ShuKun): VOI around individual plaques, not fixed proximal segments
- **Volumetric PCAT**: Total fat-range voxel volume in cm³ (complementary to FAI)
- **Radiomic PCAT**: 93-feature extraction per VOI (GLCM, GLRLM, GLSZM, NGTDM, GLDM)

### 7.3 Imaging Protocols

| Protocol Element | Most Common | Variations |
|---|---|---|
| Scanner | 64–320 slice MDCT | PCD-CT (NAEOTOM Alpha), DECT |
| Tube voltage | 120 kVp | 80, 100, 135, 140 kVp; VMI 40–190 keV |
| Reconstruction | FBP or hybrid IR | ADMIRE, SAFIRE, DLIR; soft vs sharp kernels |
| Contrast | Iodinated (300–400 mgI/mL) | Bolus tracking or test bolus |
| ECG gating | Retrospective or prospective | Prospective preferred for dose reduction |
| Phase | Best diastole (60–75% R-R) | Systole in high HR patients |

### 7.4 Phantom/Simulation Study Designs

| Study | Phantom Type | Key Variables | Main Finding |
|---|---|---|---|
| Etter et al. 2022 | Physical CT phantom | Tube voltage (80/100/120/140 kVp), reconstruction algorithm | PCATMA conversion factors: 1.267 (80 kVp), 1.08 (100 kVp), 0.947 (140 kVp) |
| Nie & Molloi 2025 | Computational (Canon Aquilion One simulation) | 10 water-lipid-protein inserts, 3 patient sizes, 80–135 kV | Water fraction RMSE 0.01–0.64%; HU varies 21.9% with kV, 3.6% with patient size |
| Sauer et al. 2024 | Computational coronary plaques (DC-GAN) | Plaque morphology, composition | Generated realistic virtual plaques for imaging trials |
| Dahal et al. 2025 | XCAT 3.0 (2500+ phantoms) | Anatomical variability, automated segmentation | Population-representative phantom library |

---

## 8. Patient Selection Methods in PCAT Studies

### 8.1 Common Inclusion Criteria

Most clinical PCAT studies select patients from **CCTA databases** with the following criteria:

| Criterion | Typical Requirement | Rationale |
|---|---|---|
| Indication | Clinically indicated CCTA for suspected/known CAD | Ensure clinical relevance |
| Image quality | Adequate for coronary assessment (motion score ≤ 2) | FAI requires clear vessel-fat boundary |
| Contrast enhancement | Adequate opacification (aortic root >250 HU) | Ensure proper contrast timing |
| ECG gating | Successful gating with evaluable phase | Motion-free reconstruction |
| Age | Typically >18 years, often >40 years | CAD prevalence |

### 8.2 Common Exclusion Criteria

| Criterion | Rationale |
|---|---|
| Prior CABG or coronary stenting in target vessel | Metal artifact contaminates VOI |
| Severe coronary calcification (Agatston >1000 in some studies) | Blooming artifact affects adjacent fat HU |
| Anomalous coronary anatomy | VOI construction assumes normal anatomy |
| Severe motion artifact | Unreliable fat-vessel boundary |
| BMI extremes (>40 or <18 in some studies) | Body habitus affects image quality and HU calibration |
| Active systemic infection or autoimmune disease | Confounds inflammatory signal |
| Recent cardiac surgery (<3 months) | Post-surgical inflammation confounds |

### 8.3 Outcome-Based Cohort Design

For prognostic studies (CRISP-CT, ORFAN):
- **Follow-up**: Minimum 1 year, typically 3–5 years (CRISP-CT: 5 years median)
- **Endpoints**: Cardiac death (primary in CRISP-CT), MACE (composite of cardiac death, MI, revascularisation)
- **Sample size**: n=500–2000 for adequate event rates (cardiac death rate ~2–5% at 5 years)
- **Multi-centre**: CRISP-CT used Erlangen (derivation) + Cleveland Clinic (validation)

### 8.4 Patient Data in Key Studies

| Study | n | Selection | Follow-up | Primary Endpoint |
|---|---|---|---|---|
| Antonopoulos et al. 2017 | 453 | Cardiac surgery patients with matched biopsies | Cross-sectional | Histological validation |
| CRISP-CT (Oikonomou 2018) | 1,872 | Clinically indicated CCTA | 5 years | Cardiac death (HR 9.04) |
| ORFAN (Oikonomou 2023) | 3,324 | Prospective CCTA cohort | Ongoing | MACE |
| Sagris et al. 2022 (meta) | 7,797 | 20 studies pooled | Variable | Unstable vs stable plaque |
| Ma et al. 2020 | 493 | Consecutive CCTA, no known CAD | Cross-sectional | Reference values |
| Wu et al. 2025 | 135 | CT perfusion patients | Cross-sectional | Perfusion timing confounds |
| Lisi et al. 2025 | 100 | Reconstruction algorithm comparison | Cross-sectional | Kernel effect on FAI |

---

## 9. Technical Confounders of FAI: Evidence Summary

### 9.1 Tube Voltage / kVp

- **Nie & Molloi 2025**: HU variance of 21.9% across 80–135 kV for identical tissue composition
- **Ma et al. 2020**: FAI increases linearly with tube voltage (less negative at higher kV)
- **Etter et al. 2022**: Conversion factors needed: 1.267 (80 kVp), 1.08 (100 kVp), 0.947 (140 kVp) relative to 120 kVp

### 9.2 Reconstruction Kernel and Algorithm

- **Lisi et al. 2025**: Up to 33 HU intra-individual variation between reconstruction kernels and iterative reconstruction levels
- **Zurich NAEOTOM studies**: Spectral CT kernel selection affects FAI significantly; VMI keV selection changes apparent attenuation

### 9.3 Patient Body Habitus

- **Nie & Molloi 2025**: 3.6% HU variance between small, medium, and large patient sizes for identical tissue
- Beam hardening and scatter increase with body size, shifting HU values

### 9.4 Contrast Timing and Perfusion

- **Wu et al. 2025**: ~7 HU swing in PCAT HU from contrast timing differences; ~15% PCAT volume change; 78% of radiomic features change >10% between perfusion phases
- Bolus timing, injection rate, and cardiac output all affect iodine distribution in the coronary artery lumen and adjacent PCAT

### 9.5 Cardiac Phase

- Different cardiac phases (systole vs diastole) produce different apparent PCAT attenuation due to volumetric compression and motion

### 9.6 Summary: Why Material Decomposition Is Needed

All these confounders affect **HU values** (the physical measurement underlying FAI) but do NOT affect the **actual tissue composition** (water, lipid, protein, iodine content). Material decomposition — decomposing each voxel into its constituent materials — is inherently protocol-independent because it measures composition, not attenuation.

---

## 10. Clinical Evidence Base: Key Trials and Studies

### 10.1 CANTOS (Anti-inflammatory therapy, causal proof)
> Ridker et al. *NEJM* 2017. n=10,061. MACE −15% with canakinumab (IL-1β antibody).

**Relevance**: Proves inflammation is a causal driver of MACE, not merely associated. Validates the clinical rationale for measuring coronary inflammation.

### 10.2 CRISP-CT (FAI validation, foundational)
> Oikonomou et al. *Lancet* 2018. n=1,872. RCA-FAI HR 9.04 for cardiac death.

**Relevance**: Defines the exact technical parameters used in the pipeline. The FAI threshold of −70.1 HU comes from this study's ROC analysis.

### 10.3 ORFAN (AI-enhanced FAI, prospective)
> Oikonomou et al. *Nature Cardiovascular Research* 2023. n=3,324.

**Relevance**: Shows AI integration of FAI outperforms all conventional risk scores for MACE prediction.

### 10.4 COLCOT and LoDoCo2 (Colchicine)
> Tardif JC et al. *NEJM* 2019 (COLCOT): −23% MACE post-MI.  
> Nidorf SM et al. *NEJM* 2020 (LoDoCo2): −31% MACE in chronic CAD.

**Relevance**: Establishes colchicine as an evidence-based anti-inflammatory agent for CAD, creating the treatment pathway that FAI-guided stratification enables.

### 10.5 PCD-CT and FAI
> Engel et al. *J Clin Med* 2026. — FAI ≥ −70.1 HU and plaque composition on PCD-CT.

**Relevance**: First study applying the Oikonomou FAI threshold on PCD-CT data. Confirms that FAI ≥ −70.1 HU identifies more lipid-rich, non-calcified plaques (vulnerable morphology) on next-generation scanners.

### 10.6 Meta-Analyses
> Sagris et al. 2022. 20 studies, n=7,797. FAI significantly higher around unstable vs stable plaques.

**Relevance**: Confirms the FAI signal is robust and reproducible across diverse study populations and scanner platforms.

---

## 11. Key References

1. Ross R. *NEJM* 1999;340:115–126 — Atherosclerosis as inflammatory disease
2. Libby P et al. *Circulation* 2021 — Inflammasome pathway and plaque vulnerability
3. Ridker PM et al. *NEJM* 2017 (CANTOS) — IL-1β causal role in MACE, n=10,061
4. Tardif JC et al. *NEJM* 2019 (COLCOT) — Colchicine −23% MACE post-MI
5. Nidorf SM et al. *NEJM* 2020 (LoDoCo2) — Colchicine −31% MACE in chronic CAD
6. Antonopoulos AS et al. *Sci Transl Med* 2017 — FAI histological validation, n=453
7. Oikonomou EK et al. *Lancet* 2018 (CRISP-CT) — FAI definition, −70.1 HU, HR 9.04
8. Oikonomou EK et al. *Nat CV Res* 2023 — CaRi-Heart, ORFAN trial, n=3,324
9. Ma R et al. 2020 — PCAT reference values: LAD −92.4, LCX −88.4, RCA −90.2 HU
10. Sagris M et al. 2022 — Meta-analysis: FAI in unstable vs stable plaques, n=7,797
11. Wu C et al. 2025 — Perfusion confounds: 7 HU swing, 78% radiomic features affected
12. Lisi C et al. 2025 — Kernel/reconstruction effects: up to 33 HU intra-individual variation
13. Etter M et al. 2022 — Phantom kVp study: PCATMA conversion factors
14. Nie A, Molloi S. *Int J Cardiovasc Imaging* 2025;41:1091–1101 — Water-lipid-protein decomposition for PVAT
15. Engel et al. *J Clin Med* 2026 — FAI on PCD-CT, plaque vulnerability
16. Iacobellis G. *Nat Rev Endocrinol* 2015 — EAT biology and measurement
17. Henrichot E et al. *ATVB* 2005 — PVAT macrophage infiltration and inflammation
18. Ohyama K et al. 2016–2017 — PVAT inflammation in vasospastic angina (18F-FDG PET)
