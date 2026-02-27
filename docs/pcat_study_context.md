# PCAT Research Context: Biomarker Validation, Radiomics, and Simulation Study Design

**Project**: PCAT Segmentation Pipeline — MolloiLab  
**Date**: February 2026  
**Scope**: Clinical validation evidence for FAI, radiomic extensions, spectral CT considerations, and simulation study design context for the MolloiLab pipeline.

---

## 1. FAI as a Validated Cardiovascular Biomarker

### 1.1 The CRISP-CT Study (Foundational)

> Oikonomou EK, Marwan M, Desai MY, et al. "Non-invasive detection of coronary inflammation using computed tomography and prediction of residual cardiovascular risk." *Lancet*. 2018;392(10151):929–939. PMID: 30170852

CRISP-CT (Cardiovascular RISk Prediction using CT) enrolled 1,872 patients undergoing clinically indicated CCTA. Key findings:

- **RCA-FAI** independently predicted cardiac death at 5-year follow-up: HR 9.04 (95% CI 2.12–38.6, p=0.003)
- FAI added incremental prognostic value beyond:
  - Coronary artery calcium score (CACS)
  - CT-angiographic Gensini score
  - Framingham Risk Score
- **FAI cut-off: −70.1 HU** for RCA was identified as the optimal threshold by ROC analysis (AUC = 0.76 for cardiac death)
- Reproducibility: ICC = 0.987 intraobserver, 0.980 interobserver

**Technical specification (adopted verbatim by our pipeline):**

| Parameter | Specification |
|---|---|
| Fat HU window | −190 to −30 HU |
| VOI radial extent | Outer vessel wall + 1× mean vessel diameter |
| LAD/LCX segment | Proximal 40 mm from ostium |
| RCA segment | 10–50 mm (proximal 40 mm, skip first 10 mm to avoid aortic root pulsation artifact) |
| FAI computation | Mean HU of all voxels in VOI within fat window |

### 1.2 Mechanistic Histological Validation

The molecular mechanism was validated in matched CT-histology specimens from patients undergoing cardiac surgery. Perivascular fat sampled adjacent to angiographically inflamed coronary segments showed:

- Significantly reduced **lipid droplet size** (p < 0.001)
- Reduced expression of adipogenic transcription factors: **PPARγ** (−2.3-fold), **FABP4** (−1.8-fold), **C/EBPα**
- Increased pro-inflammatory cytokines: **IL-6** (+3.1-fold), **TNF-α** (+2.7-fold), **CXCL10**

This confirms the CT HU elevation reflects a genuine biological shift — adipocytes adjacent to inflamed vessels inhibit lipid accumulation in response to inflammatory paracrine signals from the vessel wall. The shift is *reversible*: anti-inflammatory treatment normalises FAI.

### 1.3 ORFAN Trial (AI Score Validation)

> Oikonomou EK et al. "A novel machine learning-derived radiotranscriptomic signature of perivascular fat improves cardiac risk prediction using coronary CT angiography." *Nature Cardiovascular Research*. 2023.

The ORFAN (Oxford Risk Factors And Non-invasive imaging) prospective trial (n=3,324) tested **CaRi-Heart** (Caristo Diagnostics), the AI-enhanced FAI platform:

- CaRi-Heart AI risk score outperformed conventional risk predictors including:
  - ASCVD Pooled Cohort Equations (PCE) score
  - Synoptic Risk Score (SRS)
  - CACS alone
- Added incremental value in intermediate-risk patients (10-year ASCVD 7.5–20%)
- Key advance: CaRi-Heart integrates FAI + shape features + coronary calcification into a single AI risk score

**Clinical implication**: Per-vessel FAI values (what our pipeline computes) are the raw input to the CaRi-Heart model. Our pipeline output is directly usable as input to such downstream AI models.

### 1.4 PCAT Volume vs. PCAT Attenuation (Two Distinct Phenotypes)

These are biologically distinct and partially independent measurements:

| Measure | Definition | Biological Meaning | Clinical Correlation |
|---|---|---|---|
| **PCAT attenuation (FAI)** | Mean HU of fat-range voxels in proximal VOI | Acute inflammatory phenotypic shift in adipocytes adjacent to vessel | Future MACE, cardiac death, plaque vulnerability |
| **PCAT volume** | Total cm³ of fat-range voxels in VOI | Size of the pericoronary fat depot | Metabolic syndrome, obesity, chronic risk, EAT volume |

A patient can have:
- **High volume, low FAI**: large depot, but not actively inflamed (obese, metabolically unhealthy but no acute coronary inflammation)
- **Low volume, high FAI**: small depot but highly inflamed (lean patient with active plaque inflammation)

Our pipeline computes both via `compute_pcat_stats()`:
- FAI → `stats["hu_mean"]`
- Volume → `stats["n_fat_voxels"] × voxel_volume_cm3` (derivable from spacing_mm)

---

## 2. PCAT Radiomics: Beyond Mean HU

### 2.1 ShuKun Technology Approach

> Huang et al. PMID 41163958, 2025 — Lesion-specific PCAT radiomics for MACE prediction  
> PMID 39696214, 2025 — PCAT radiomics in stable CAD

ShuKun's commercial pipeline extracts **93 radiomic features** from the PCAT VOI per lesion segment (not just proximal fixed segments). The feature set follows IBSI (Image Biomarker Standardisation Initiative) convention:

| Feature Class | Count | Examples |
|---|---|---|
| First-order statistics | ~18 | Mean, median, min, max, energy, entropy, skewness, kurtosis, percentiles (10th, 90th) |
| GLCM (co-occurrence matrix) | ~24 | Contrast, correlation, entropy, homogeneity, cluster shade |
| GLSZM (size zone matrix) | ~16 | Small zone emphasis, large zone high grey level emphasis |
| GLRLM (run length matrix) | ~16 | Run length non-uniformity, long run emphasis, short run low grey level |
| NGTDM (neighbourhood tone) | ~5 | Coarseness, complexity, busyness, contrast |
| GLDM (dependence matrix) | ~14 | Dependence variance, dependence entropy |

#### Downstream ML Pipeline
1. Feature selection: Pearson correlation filtering (|r| > 0.95) + Lasso regression (L1 regularisation)
2. Normalisation: Min-Max scaling per feature
3. Classification: **XGBoost** with 10-fold cross-validation
4. Outcome: MACE (Major Adverse Cardiovascular Events) at follow-up

**Lesion-specific vs. segment-specific**: ShuKun measures PCAT around individual plaques identified by CT-FFR < 0.8, not just fixed proximal segments. This is conceptually more targeted: inflamed PCAT is most clinically relevant when it is *directly adjacent to a culprit lesion*.

### 2.2 Adding Radiomics to Our Pipeline (Future Upgrade)

The `pyradiomics` library (IBSI-compliant, Python) would add the full 93-feature set with ~10 lines of code:

```python
import radiomics
from radiomics import featureextractor

extractor = radiomics.featureextractor.RadiomicsFeatureExtractor()
extractor.enableAllFeatures()

# Convert VOI mask to SimpleITK
import SimpleITK as sitk
vol_sitk  = sitk.GetImageFromArray(volume.astype(np.float32))
mask_sitk = sitk.GetImageFromArray(voi_mask.astype(np.int32))
vol_sitk.SetSpacing([sx, sy, sz])
mask_sitk.SetSpacing([sx, sy, sz])

features = extractor.execute(vol_sitk, mask_sitk)
# features is a dict with ~100 keys, all pyradiomics_ prefixed
```

This would be added to `pcat_segment.py::compute_pcat_stats()`.

---

## 3. Spectral CT and FAI: Important Calibration Note

### 3.1 What Is Spectral CT

Standard CCTA acquires data at a single effective energy (~120 kVp polychromatic beam). Spectral CT platforms acquire data at multiple energies simultaneously:

| Platform | Technology | Vendor |
|---|---|---|
| Dual Energy CT (DECT) | Two X-ray tubes at 80+140 kVp | Siemens, GE, Canon, Philips |
| Dual-layer CT | Single X-ray source, energy-resolving detector | Philips IQon |
| Photon-counting detector CT (PCD-CT) | Single photon counting at multiple energy thresholds | Siemens NAEOTOM Alpha |

Spectral CT enables **material decomposition**: each voxel is expressed as a combination of two or three basis materials (water, iodine, fat, calcium). This is more specific than integrated HU.

### 3.2 Virtual Monoenergetic Images (VMI)

Spectral CT reconstructions include **Virtual Monoenergetic Images (VMI)** at a user-specified keV (e.g., 70 keV). VMI simulates a monochromatic X-ray beam at that energy, providing:
- Noise characteristics closer to standard CT
- Reduced beam-hardening artifact (especially near calcium/contrast)
- More reproducible HU values independent of tube voltage protocol

**Relevance to our patients**: The DICOM series label `mono 70 keV` in the Rahaf patients indicates these are VMI reconstructions from a spectral acquisition — likely dual-energy or PCD-CT. This has a direct implication for the FAI threshold:

> The **−190 to −30 HU fat window** was validated on conventional 120 kVp polychromatic CCTA. On VMI at 70 keV, fat voxels are expected to shift slightly — approximately **+5 to +15 HU** more positive — because the lower effective energy increases the attenuation difference between fat (low Z) and water. The −70.1 HU cut-off has not been formally validated on VMI data.

### 3.3 Water-Lipid Decomposition as a Superior PCAT Marker

Material decomposition directly provides a **lipid density image** where each voxel's value reflects its triglyceride content. For PCAT:
- Normal fat: high lipid signal (predominantly triglycerides)
- Inflamed PCAT: reduced lipid signal (adipocytes shift toward aqueous phase)

This is a more specific signal than FAI HU because it is independent of partial-volume effects from adjacent soft tissue or contrast-enhanced lumen. It also removes the ambiguity from mixed-composition voxels that straddle the fat–vessel wall boundary.

**Research opportunity**: Our simulation study could directly compare:
1. Standard FAI (mean HU, −190 to −30 window) on VMI
2. Lipid density (from material decomposition map)
3. Ground-truth known composition (phantom)

This would be the first direct comparison of FAI vs. lipid-map for PCAT quantification accuracy.

---

## 4. Simulation Study Design Context

### 4.1 Purpose

The immediate application of this pipeline is a **simulation study** to characterise PCAT quantification accuracy on CCTA images. The pipeline is the measurement instrument: given a known ground-truth fat distribution (phantom or computational model), how accurately does the FAI extraction reproduce the ground-truth HU values?

### 4.2 Key Validation Questions

| Question | Test Design |
|---|---|
| Does the VOI construction correctly capture the pericoronary fat shell? | Compare VOI mask to manual ground-truth annotation |
| How does spatial resolution affect FAI accuracy? | Scan phantom at multiple resolution settings |
| What is the sensitivity to centerline positioning error? | Perturb seed positions by ±0.5–2 mm, measure FAI change |
| Does partial volume at vessel wall contaminate FAI? | Compare FAI at different VOI inner-radius margins |
| VMI vs. polychromatic: does HU threshold need recalibration? | Scan same phantom at 120 kVp and 70 keV VMI |

### 4.3 Phantom Composition Requirements

For a PCAT simulation phantom, the material must accurately reproduce the CT appearance of:
- **Normal PCAT**: HU approximately −90 to −70 (predominantly fat)
- **Inflamed PCAT**: HU approximately −60 to −50 (fat + inflammatory exudate)
- Coronary artery lumen: contrast-enhanced blood (~300–500 HU)
- Vessel wall: soft tissue (~50–70 HU)
- Background mediastinum: soft tissue + lung

Standard tissue-mimicking materials for CT phantoms:
- Fat equivalent: lard, vegetable shortening, or polymer foam (HU tunable −90 to −50)
- Soft tissue: gel or urethane mixtures (HU tunable 0–80)
- Blood/lumen: iodinated solution (HU adjustable with iodine concentration)

### 4.4 Expected Outputs from Our Pipeline for Validation

The pipeline currently produces per-vessel:
- `stats["hu_mean"]`: primary FAI measurement
- `stats["hu_std"]`: FAI variability
- `stats["fat_fraction"]`: fraction of VOI voxels in fat window
- `stats["n_fat_voxels"]`: VOI volume (multiplied by voxel volume → cm³)
- Radial HU profile (1 mm rings from vessel outer wall): identifies boundary contamination
- HU histogram: full distribution, not just mean

All of these are directly comparable to phantom ground-truth measurements for validation.

---

## 5. Quantitative PCAT Summary Across Vessels (Population Norms)

From the CRISP-CT validation cohort and subsequent publications, approximate normal reference ranges for FAI:

| Vessel | Normal FAI (HU) | Inflamed FAI (HU) | Risk Threshold |
|---|---|---|---|
| RCA | −85 to −70 | −70 to −40 | **−70.1 HU** (Oikonomou 2018) |
| LAD | −80 to −65 | −65 to −40 | ≈ −72 HU (less validated) |
| LCX | −85 to −70 | −70 to −40 | Similar to RCA (limited data) |

Note: LCX FAI is less reported in the literature because the LCX runs along the atrioventricular groove adjacent to the left atrial wall, making the pericoronary VOI prone to contamination from non-adipose tissue. This is consistent with our pipeline's lower fat voxel counts for LCX vs. LAD.

---

## 6. Key References

1. Oikonomou EK et al. *Lancet* 2018;392:929–939. PMID 30170852 — FAI methodology, CRISP-CT, −70.1 HU cut-off
2. Oikonomou EK et al. *Nature Cardiovascular Research* 2023 — CaRi-Heart AI score, ORFAN trial
3. Huang et al. PMID 41163958, 2025 — ShuKun 93-feature PCAT radiomics for MACE
4. PMID 39696214, 2025 — PCAT radiomics in stable CAD
5. Weichsel J et al. *Eur Radiol* 2024. PMID 38248031 — Siemens syngo.via DL comparison
6. Engel et al. *J Clin Med* 2026 — FAI ≥ −70.1 HU and plaque composition on PCD-CT
7. Eveson et al. *Br J Radiol* 2026 — Spectral CT and quantitative PCAT review
8. IBSI (Image Biomarker Standardisation Initiative) — Radiomic feature definitions
