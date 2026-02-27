# Coronary Artery Inflammation: Field Context and Biological Mechanisms

**Project**: PCAT Segmentation Pipeline — MolloiLab  
**Date**: February 2026  
**Scope**: The biology of coronary artery inflammation, its role in atherosclerosis, the paracrine signalling between vessel wall and perivascular fat, and the clinical evidence base that motivates PCAT/FAI measurement.

---

## 1. Paradigm Shift: Atherosclerosis as an Inflammatory Disease

### 1.1 The Historical View (Lipid-Centric)

Until the 1990s, atherosclerosis was conceptualised primarily as a **lipid storage disorder**: LDL cholesterol accumulates in the arterial intima, forms fatty streaks, and progressively obstructs the lumen. Treatment focused on lipid lowering (statins).

While lipid lowering reduces MACE by ~35%, a large **residual cardiovascular risk** remains even after optimal statin therapy. This gap drove the search for alternative pathways.

### 1.2 The Inflammatory Hypothesis

> Ross R. "Atherosclerosis — an inflammatory disease." *New England Journal of Medicine*. 1999;340:115–126.

Ross established the **"response-to-injury" hypothesis**: the primary trigger for atherosclerosis is endothelial injury (from oxidised LDL, hemodynamic shear stress, hypertension, smoking), which activates an inflammatory cascade:

1. Endothelial activation → upregulation of adhesion molecules (VCAM-1, ICAM-1, E-selectin)
2. Monocyte recruitment → differentiation into macrophages
3. Macrophages engulf oxidised LDL → foam cells
4. Foam cells secrete pro-inflammatory cytokines (IL-1β, IL-6, TNF-α)
5. Smooth muscle cell migration and proliferation → fibrous cap formation
6. Plaque vulnerability determined by cap thickness vs. inflammatory burden

### 1.3 Causal Proof: The CANTOS Trial

> Ridker PM et al. "Antiinflammatory therapy with canakinumab for atherosclerotic disease." *New England Journal of Medicine*. 2017;377:1119–1131.

**CANTOS** (Canakinumab Anti-inflammatory Thrombosis Outcome Study) enrolled 10,061 patients with prior MI and elevated hsCRP. Patients received canakinumab (IL-1β antibody) or placebo on top of optimal statin therapy:

- **Primary result**: Canakinumab reduced MACE by **15%** at 50 mg (p=0.021) and **14%** at 150 mg (p=0.031)
- Effect was **independent of LDL cholesterol** (LDL did not change)
- This was the first proof that targeting inflammation — not lipids — reduces cardiovascular events

**Implication for FAI**: If inflammation is a direct causal driver of MACE, then a non-invasive imaging biomarker of coronary inflammation (FAI) should predict future events. CRISP-CT confirmed this.

### 1.4 The Inflammasome Pathway

> Libby P et al. "Inflammation and Atherosclerosis Circulation." *Circulation*. 2021. Also: Libby P, *Nature* 2021.

The **NLRP3 inflammasome** is the central molecular sensor of danger signals in atherosclerotic plaques:

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

## 2. Perivascular Adipose Tissue as a Paracrine Signalling Hub

### 2.1 Anatomy

**Pericoronary adipose tissue (PCAT)** is the adipose tissue immediately surrounding the coronary arteries, between the coronary vessels and the epicardial surface. It is:
- Distinct from **epicardial adipose tissue (EAT)**: the full fat depot within the pericardial sac
- Distinct from **paracardial fat**: fat outside the pericardium
- The most relevant compartment for vessel wall-specific inflammatory signals because it lacks a fascial barrier between the fat and the adventitia

PCAT is vascularised by the vasa vasorum and shares the same microvascular supply as the adventitia, creating a direct exchange pathway for paracrine mediators.

### 2.2 Vasocrine Signalling: Vessel Wall → Fat

When the coronary artery is inflamed:

1. Adventitial macrophages and smooth muscle cells secrete **IL-6, TNF-α, CXCL10, VEGF**
2. These mediators diffuse outward into adjacent PCAT
3. IL-6 and TNF-α suppress adipocyte differentiation:
   - Inhibit **PPARγ** (master transcription factor for fat cell maturation)
   - Inhibit **C/EBPα** (co-factor for adipogenesis)
   - Inhibit **FABP4** (fatty acid binding protein, marker of mature adipocyte)
4. Adipocytes remain immature, smaller, with less stored lipid
5. **Result on CT**: fat voxels shift from lipid-dominant (HU ≈ −90 to −70) toward more aqueous composition (HU ≈ −60 to −40) — this is the FAI signal

The FAI increase therefore reflects a **genuine molecular phenotypic shift** in the fat cells, not a measurement artifact.

### 2.3 Paracrine Signalling: Fat → Vessel Wall

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

### 2.4 Why PCAT Is More Informative Than Systemic Inflammatory Markers

| Marker | What it reflects | Limitations |
|---|---|---|
| hsCRP (serum) | Systemic inflammation | Non-specific; elevated in infection, obesity, any inflammation |
| IL-6 (serum) | Systemic cytokine burden | Same; not vessel-specific |
| **FAI (CT)** | **Per-vessel, local coronary inflammation** | Specific to individual coronary artery; spatial resolution to individual vessel |

FAI is the only clinical measurement that localises inflammation to a **specific coronary artery segment** non-invasively. This is critical for lesion-specific risk stratification — a stenotic LAD with high FAI is a different risk entity than the same stenosis with low FAI.

---

## 3. PCAT vs. Epicardial Adipose Tissue (EAT)

### 3.1 Measurement Differences

| Feature | PCAT | EAT |
|---|---|---|
| **Spatial scope** | ~3–5 mm shell around specific vessel segment | Entire pericardial sac |
| **Measurement unit** | Mean HU (attenuation = FAI) | Total volume (cm³) |
| **Clinical signal** | Per-vessel acute inflammatory state | Whole-heart chronic metabolic risk |
| **Segmentation** | Vessel-specific VOI (centerline-based) | Pericardial sac segmentation |
| **Key paper** | Oikonomou 2018, *Lancet* | Iacobellis, multiple reviews |
| **Commercial tool** | CaRi-Heart (Caristo), ShuKun PCAT | Multiple EAT volume tools |

### 3.2 Are They Measuring the Same Thing?

No. Correlation between EAT volume and RCA-FAI is moderate at best (r ≈ 0.3–0.4). A patient with:
- **High EAT volume, low FAI**: metabolically obese, but coronary arteries not actively inflamed
- **Low EAT volume, high FAI**: lean but with focal plaque-driven coronary inflammation

Both PCAT and EAT are independently associated with MACE in multivariate models — they measure complementary biological processes.

---

## 4. Spatial Heterogeneity of Coronary Inflammation

### 4.1 Why Proximal Segments Matter

The proximal coronary segments (LAD 0–40 mm, LCX 0–40 mm, RCA 10–50 mm) are the clinical focus because:
1. **Most plaques form here**: hemodynamic shear stress patterns at bifurcations and proximal curves create preferential plaque deposition
2. **Clinical consequence**: proximal stenoses cause more downstream ischemia than distal stenoses
3. **CT resolution**: proximal vessels are larger (3–5 mm diameter) → better SNR for FAI measurement

### 4.2 Lesion-Specific PCAT (ShuKun Approach)

Rather than fixed proximal segments, measuring PCAT adjacent to each individual plaque provides:
- **Higher specificity**: PCAT around a stable fibrous plaque may be low even in the same vessel as an unstable plaque with high PCAT
- **Better MACE prediction**: the PCAT signal is strongest immediately adjacent to the vulnerable plaque, not averaged across the full proximal segment

This is an active research frontier; our pipeline currently implements the validated fixed-segment approach from CRISP-CT.

### 4.3 RCA vs. LAD vs. LCX: Different Biology

The clinical literature focuses primarily on RCA-FAI because:
- RCA has the most pericoronary fat (largest fat depot, cleaner VOI)
- LAD runs in the anterior interventricular groove — also well-studied
- LCX runs in the atrioventricular groove adjacent to the left atrial wall, making VOI contamination from non-adipose tissue more common

This explains the pipeline observation: LCX tends to have lower fat voxel counts than LAD even in patients with comparable coronary disease burden.

---

## 5. Clinical Evidence Base: Key Trials and Studies

### 5.1 CANTOS (Anti-inflammatory therapy, causal proof)

> Ridker et al. *NEJM* 2017. n=10,061. MACE −15% with canakinumab (IL-1β antibody).

**Relevance**: Proves inflammation is a causal driver of MACE, not merely associated. Validates the clinical rationale for measuring coronary inflammation.

### 5.2 CRISP-CT (FAI validation, foundational)

> Oikonomou et al. *Lancet* 2018. n=1,872. RCA-FAI HR 9.04 for cardiac death.

**Relevance**: Defines the exact technical parameters used in our pipeline. The FAI threshold of −70.1 HU comes from this study's ROC analysis.

### 5.3 ORFAN (AI-enhanced FAI, prospective)

> Oikonomou et al. *Nature Cardiovascular Research* 2023. n=3,324.

**Relevance**: Shows AI integration of FAI outperforms all conventional risk scores for MACE prediction.

### 5.4 COLCOT and LoDoCo2 (Colchicine — anti-inflammatory without immunosuppression)

> Tardif JC et al. *NEJM* 2019 (COLCOT): colchicine (IL-1β/inflammasome inhibitor) −23% MACE after MI.  
> Nidorf SM et al. *NEJM* 2020 (LoDoCo2): colchicine −31% MACE in chronic CAD.

**Relevance**: These trials established low-dose colchicine as an evidence-based anti-inflammatory agent for CAD — cheaper and safer than canakinumab. The mechanistic pathway (NLRP3/IL-1β inhibition) is the same one that generates the FAI signal. This creates a direct clinical pathway: identify high-FAI patients → treat with colchicine.

### 5.5 PCD-CT and FAI (2026)

> Engel et al. *Journal of Clinical Medicine* 2026. — FAI ≥ −70.1 HU and plaque composition on photon-counting detector CT.

**Relevance**: First study applying the Oikonomou FAI threshold on PCD-CT data. Confirms that FAI ≥ −70.1 HU identifies more lipid-rich, non-calcified plaques (vulnerable morphology) on this next-generation scanner platform.

---

## 6. Implications for the MolloiLab Pipeline

### 6.1 What We Are Measuring

Every FAI value our pipeline produces reflects:
- The **inflammatory microenvironment** of the specific coronary artery segment
- The **paracrine output** of the vessel wall at that location
- The **maturation state** of the perivascular adipocytes (lipid-filled vs. aqueous-shifted)

This is not a technical CT measurement artifact — it is a biologically meaningful signal validated across multiple prospective cohorts.

### 6.2 Clinical Decision Pathway Enabled by Our Outputs

```
Pipeline output: RCA-FAI = −62 HU (> −70.1 threshold)
        ↓
Classification: HIGH RISK (⚠️  displayed in pipeline output)
        ↓
Clinical implication: Active coronary inflammation, elevated residual risk
        ↓
Potential action: Consider colchicine / statin intensification / earlier follow-up CCTA
```

This pathway is currently available in clinical practice where CaRi-Heart (Caristo Diagnostics) is deployed. Our pipeline computes the identical underlying measurement.

### 6.3 Known Confounders and Limitations

| Confounder | Impact | Mitigation |
|---|---|---|
| **Cardiac motion artifact** | Blurred voxels at boundary between vessel wall and fat | ECG-gated acquisition (all 3 patients have gated CCTA) |
| **Contrast spillover** | High-HU contrast in lumen can create beam-hardening halos that raise adjacent fat HU | Inner VOI margin (vessel wall excluded by centerline + radius) |
| **Partial volume** | Sub-mm vessels near spatial resolution limit → mixed voxels at boundary | VOI inner margin = vessel outer wall, not lumen |
| **Reconstruction algorithm** | Sharp kernels increase noise → broader HU distribution | Use smooth/medium reconstruction kernels for PCAT |
| **VMI energy** | Fat HU shifts with keV; −70.1 threshold validated at 120 kVp | Threshold validation at 70 keV VMI needed |
| **LCX anatomy** | VOI overlaps left atrial wall → non-adipose contamination | Report LCX with caveat; lower clinical weight |

---

## 7. Key References

1. Ross R. *NEJM* 1999;340:115–126 — Atherosclerosis as inflammatory disease
2. Libby P et al. *Circulation* 2021 — Inflammasome pathway and plaque vulnerability
3. Ridker PM et al. *NEJM* 2017 (CANTOS) — IL-1β causal role in MACE, n=10,061
4. Tardif JC et al. *NEJM* 2019 (COLCOT) — Colchicine −23% MACE post-MI
5. Nidorf SM et al. *NEJM* 2020 (LoDoCo2) — Colchicine −31% MACE in chronic CAD
6. Oikonomou EK et al. *Lancet* 2018. PMID 30170852 — CRISP-CT, FAI definition, −70.1 HU
7. Oikonomou EK et al. *Nature Cardiovascular Research* 2023 — CaRi-Heart, ORFAN trial
8. Engel et al. *J Clin Med* 2026 — FAI on PCD-CT, plaque vulnerability correlation
9. Iacobellis G. *Nature Reviews Endocrinology* 2015 — EAT biology and measurement
10. Henrichot E et al. *Arterioscler Thromb Vasc Biol* 2005 — PVAT macrophage infiltration and inflammation
