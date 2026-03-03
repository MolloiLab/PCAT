# The Proxy Problem: Pericoronary Adipose Tissue, the Measurement Crisis in Coronary Inflammation Imaging, and the Case for Composition-Based Biomarkers

**Project**: PCAT — MolloiLab, University of California, Irvine
**Author**: Shu Nie
**Date**: March 2026

---

The CANTOS and COLCOT trials established inflammation as a causal, treatable driver of cardiovascular disease, transforming it from hypothesis to therapeutic target. This success created an imperative: a non-invasive biomarker capable of localising coronary inflammation to specific vessels, monitoring treatment response, and stratifying residual risk. Pericoronary adipose tissue attenuation — the fat attenuation index — emerged to meet this need, achieving FDA clearance and demonstrating hazard ratios of 9 to 30 for cardiac mortality across cohorts exceeding 40,000 patients. Yet the field now confronts an uncomfortable possibility: a biomarker can predict outcomes robustly without accurately measuring the biological process it claims to capture — and this distinction, between proxy and measurement, determines whether coronary inflammation imaging will mature into a mechanistic tool or remain a sophisticated correlate.

---

## 1. The Inflammation Hypothesis Succeeds

Atherosclerosis spent a century as a lipid storage disorder. Ross's 1999 reformulation — atherosclerosis as an inflammatory disease, driven by endothelial injury and a self-amplifying cascade of monocyte recruitment, foam cell formation, and cytokine secretion — reframed the problem but left it therapeutically orphaned (Ross 1999). Statins reduced events by approximately 35%, yet a large residual cardiovascular risk persisted in optimally treated patients, unaccounted for by any modifiable lipid parameter.

The CANTOS trial resolved this ambiguity with a direct experiment. Ridker and colleagues randomised 10,061 patients with prior myocardial infarction and elevated high-sensitivity C-reactive protein to canakinumab, a monoclonal antibody targeting interleukin-1β, or placebo — on top of optimal statin therapy (Ridker et al. 2017). The 150 mg dose reduced major adverse cardiovascular events by 15% (p = 0.031) without altering LDL cholesterol. For the first time, an intervention that targeted inflammation alone, leaving lipids untouched, reduced cardiovascular events. The implication was unambiguous: residual cardiovascular risk is, at least in part, inflammatory risk.

Two colchicine trials converted this insight into clinical practice. COLCOT demonstrated a 23% reduction in MACE in post-MI patients (Tardif et al. 2019), and LoDoCo2 showed a 31% reduction in chronic coronary artery disease (Nidorf et al. 2020). Together, these three randomised controlled trials — targeting distinct nodes of the inflammatory cascade — represent convergent evidence of the highest order. The causal role of inflammation in atherosclerotic events is no longer a hypothesis; it is an established therapeutic axis.

This success, however, created a measurement problem. Systemic biomarkers such as hsCRP and IL-6 reflect whole-body inflammatory burden and cannot localise inflammation to a specific coronary artery. 18F-FDG PET offers metabolic imaging of inflammation but suffers from poor spatial resolution, cardiac and respiratory motion artefacts, and myocardial uptake that confounds coronary assessment. What the field required was a vessel-specific, non-invasive readout — a measurement that could distinguish an inflamed left anterior descending artery from an uninflamed one in the same patient. Pericoronary adipose tissue attenuation was proposed as precisely this measurement.

---

## 2. The Predictive Triumph

The biological basis for pericoronary fat as an inflammation sensor is elegant. The coronary arteries are embedded in a thin shell of adipose tissue that shares its microvascular supply — the vasa vasorum — with the arterial adventitia. When the vessel wall is inflamed, adventitial macrophages and smooth muscle cells secrete interleukin-6, tumour necrosis factor-α, CXCL10, and VEGF. These mediators diffuse outward into the adjacent fat, suppressing PPARγ and C/EBPα — the master transcription factors for adipocyte maturation — and inhibiting FABP4, a marker of lipid-loaded mature adipocytes (Antonopoulos et al. 2017). The adipocytes remain immature, smaller, with less stored lipid and more intracellular water. On CT, this phenotypic shift increases attenuation: fat voxels migrate from approximately −90 HU (lipid-dominant) toward −60 HU (aqueous). The fat attenuation index (FAI), defined as the mean Hounsfield unit value of pericoronary fat within the −190 to −30 HU window, quantifies this shift.

Antonopoulos and colleagues validated this mechanism histologically in 453 cardiac surgery patients, demonstrating that perivascular fat adjacent to inflamed coronary segments showed reduced lipid droplet size (p < 0.001), reduced PPARγ expression (−2.3-fold), reduced FABP4 (−1.8-fold), and increased IL-6 (+3.1-fold) and TNF-α (+2.7-fold) (Antonopoulos et al. 2017). The biological plausibility was established: coronary inflammation genuinely alters the molecular phenotype of adjacent fat, and CT can detect this alteration.

What followed was a decade of predictive validation that few biomarkers in cardiovascular imaging have matched. The CRISP-CT study — a dual-centre retrospective analysis of 1,872 patients from Erlangen and Cleveland — showed that RCA-FAI independently predicted cardiac death at five-year follow-up with a hazard ratio of 9.04 (95% CI 2.12–38.6, p = 0.003), adding incremental prognostic value beyond the coronary artery calcium score, Gensini score, and Framingham Risk Score (Oikonomou et al. 2018). An ROC-derived threshold of −70.1 HU separated high- from low-risk patients with an AUC of 0.76 for cardiac death. Reproducibility was excellent: intraobserver ICC 0.987, interobserver 0.980.

The ORFAN programme extended this to population scale. Chan and colleagues analysed 40,091 consecutive CCTA patients from eight NHS hospitals, with a median follow-up of 2.7 years (Chan et al. 2024). The findings were striking: 81.1% of patients had no obstructive coronary artery disease, yet this group accounted for 66.3% of all MACE and 63.7% of cardiac deaths — demonstrating that inflammatory risk extends far beyond stenosis-based evaluation. Patients with three inflamed coronary arteries (defined by elevated FAI Score) had a hazard ratio of 29.8 for cardiac mortality compared with those with no inflamed arteries. The AI-integrated risk score (CaRi-Heart) achieved a net reclassification improvement of 0.38 for cardiac mortality.

These numbers are formidable. A hazard ratio of 29.8 in a cohort of 40,000 patients is not a statistical artefact. The subsequent FDA clearance of CaRi-Plaque in March 2025, assignment of CPT codes (0992T and 0993T), and Medicare reimbursement for 2026 represent the logical endpoint of predictive validation done well. By every standard of clinical epidemiology, FAI predicts cardiovascular events.

The question that would fracture the field was not whether FAI predicts outcomes, but what it is that FAI actually measures.

---

## 3. The Measurement Problem: Proxy, Signal, or Artefact?

### 3.1 The inverse problem

Every CT-based tissue measurement confronts the same inverse problem. The scanner does not measure biology directly; it measures X-ray attenuation, which is a composite function:

$$\text{HU}_{\text{measured}} = f(\text{tissue composition}) + g(\text{imaging parameters}) + \varepsilon$$

where *f* encodes the biological signal of interest (water content, lipid fraction, inflammatory state), *g* encodes systematic bias from tube voltage, reconstruction kernel, scanner model, contrast timing, patient habitus, and cardiac phase, and *ε* represents stochastic noise. The clinical goal is to isolate *f*. The fundamental question for any HU-based biomarker is whether *f* dominates the measurement — or whether *g* is large enough to overwhelm, distort, or masquerade as biology.

This question is not new to CT physics. Alvarez and Macovski demonstrated in 1976 that X-ray attenuation in tissue is a composite of photoelectric absorption and Compton scattering, making Hounsfield units inherently ambiguous for tissue characterisation — different combinations of these two physical processes can produce identical HU values (Alvarez & Macovski 1976). The entire intellectual history of dual-energy CT, spectral CT, and photon-counting CT is a progressive attempt to resolve this ambiguity by acquiring data at multiple energies and decomposing the composite signal into its material constituents. The PCAT field, however, developed in isolation from this physics tradition, building its biomarker on precisely the single-energy composite signal that the broader CT community had spent four decades learning to distrust.

### 3.2 The magnitude of *g*

The evidence that *g* is large relative to *f* has accumulated from multiple independent groups, each quantifying a different component of the technical bias:

**Tube voltage.** Nie and Molloi demonstrated a 21.9% variance in pericoronary fat HU values across 80–135 kVp for tissue of identical composition (Nie & Molloi 2025). Boussoussou and colleagues found an 8 HU shift between 100 and 120 kVp within their cohort (Boussoussou et al. 2023). These magnitudes are clinically meaningful: the biological signal of interest — the shift from non-inflamed (approximately −85 HU) to inflamed (approximately −70 HU) fat — spans roughly 15 HU. A confounder that accounts for 8–20 HU of variance is not a minor nuisance; it is the same order of magnitude as the signal itself.

**Reconstruction kernel.** Lisi and colleagues showed that reconstructing the same raw data with different kernels and iterative reconstruction levels produced up to 33 HU of intra-individual variation in FAI — more than twice the biological signal range (Lisi et al. 2024). Sharper kernels (Bv56) yielded −106 ± 2 HU; smooth kernels with iterative reconstruction (Qr36 + QIR4) yielded −87 ± 9 HU. The same patient, from the same scan, could be classified as inflamed or non-inflamed depending solely on the reconstruction algorithm selected by the technologist.

**Contrast timing.** Wu and colleagues at Case Western used dynamic CT perfusion to show that pericoronary fat attenuation varied by approximately 7 HU across different contrast perfusion phases within the same scan session, and that 78% of radiomic features changed by more than 10% between phases (Wu et al. 2025). This is particularly damaging because contrast timing is not standardised across clinical sites, varies with cardiac output and injection rate, and is rarely reported in published FAI studies.

**Scanner platform.** Boussoussou's cross-scanner validation showed a 15 HU difference in average PCAT attenuation between a GE CardioGraphe and a Philips Brilliance for the same patient population (Boussoussou et al. 2023). Tremamunno and colleagues confirmed that photon-counting CT and conventional energy-integrating detector CT produce systematically different FAI values for the same patient (Tremamunno et al. 2025). The −70.1 HU threshold, derived on specific scanners at specific protocols, cannot be transported across platforms without recalibration.

**Patient habitus.** Nie and Molloi found 3.6% HU variance attributable to patient size alone (Nie & Molloi 2025). Boussoussou found BMI contributed −0.4 HU per kg/m² (Boussoussou et al. 2023). In obese patients — precisely the population at highest cardiovascular risk — beam hardening and scatter shift HU values in ways that mimic or mask the biological signal.

**Partial volume effects.** Hell and Achenbach at Erlangen argued that variations in pericoronary fat CT density are primarily attributable to partial volume effects and image interpolation rather than tissue composition or metabolic activity (Hell et al. 2016). PCAT attenuation decreased with increasing distance from the vessel and from proximal to distal segments — a gradient consistent with contamination from the contrast-enhanced lumen. Li and colleagues confirmed that PCAT density is highest within 0.5 mm of the lumen and decreases with distance, with measurements within 0.75 mm susceptible to partial volume artefacts (Li et al. 2025).

Taken individually, each of these confounders has been acknowledged and, to varying degrees, addressed. Taken collectively, they pose a more fundamental challenge: the total technical variance (*g*) is comparable in magnitude to the total biological variance (*f*). The signal-to-noise ratio of FAI as a biological measurement may be close to unity.

### 3.3 The taxonomy of deconvolution strategies

The field's response to this challenge has been a series of increasingly sophisticated attempts to separate *f* from *g* — each making different assumptions about how to handle the confounders:

| Strategy | Representative work | How *g* is handled | Core assumption | Limitation |
|---|---|---|---|---|
| **Ignore** | Oxford CRISP-CT (2018) | Assume *g* ≪ *f* | Biology dominates | Fails across protocols |
| **Single correction** | Etter et al. (2022) | kVp conversion factors | Only kVp matters | Other confounders persist |
| **Multi-factor correction** | FAI Score (Antoniades 2025) | Regression adjustment | *g* is capturable by regression | Residual confounding; requires calibration |
| **Feature enrichment** | Radiomics (ShuKun, Cedars-Sinai) | Extract more from same HU data | Additional signal in texture | *g* contaminates all features |
| **Domain expansion** | PCATMA (Li et al. 2025) | Remove fat threshold | More complete sampling | Still HU-based |
| **Domain exit** | Material decomposition (Nie & Molloi 2025) | Measure composition, not attenuation | Physics-based separation | Requires multi-energy CT |

What this taxonomy reveals is a continuum from pragmatic acceptance of confounders to their systematic elimination. Every strategy to the left of material decomposition operates within the HU domain and therefore inherits its fundamental ambiguity. Each is a more sophisticated attempt to untangle a mixture that was never designed to be untangled — because Hounsfield units encode both biology and physics inseparably. Material decomposition sidesteps the problem by measuring in the composition domain (water fraction, lipid fraction), where imaging parameters have no systematic effect.

The critical insight is that this is not a novel intellectual move. It is precisely the transition that the broader CT physics community made decades ago — from single-energy HU to dual-energy material decomposition — when confronted with the identical limitation in other tissue characterisation problems (Alvarez & Macovski 1976; Grönberg et al. 2020). The PCAT field is arriving at a conclusion that CT physics established in 1976: Hounsfield units are an insufficient basis for quantitative biological characterisation.

---

## 4. The Paradoxes and What They Diagnose

The disagreements within the PCAT field are not merely technical disputes about measurement error. They are symptoms of a deeper structural problem — the confusion of predictive validity with construct validity — and each paradox, properly understood, illuminates a different facet of this confusion.

### 4.1 Predictive validity versus construct validity

**Predictive validity** asks: does this measurement associate with outcomes? FAI has strong predictive validity — HR 9.04 (CRISP-CT), HR 29.8 (ORFAN). **Construct validity** asks: does this measurement capture the biological construct it claims to represent — in this case, coronary inflammation? These are independent properties. A measurement can have high predictive validity and low construct validity simultaneously. Body mass index predicts cardiovascular death without measuring cardiovascular disease. Neighbourhood zip code predicts life expectancy without measuring health. In each case, the measurement is a *proxy* — statistically associated with outcomes through a web of correlated factors — rather than a *measure* of the underlying biology.

The question for FAI is whether it occupies this same quadrant: high predictive validity, uncertain construct validity.

### 4.2 The Correction Paradox

As statistical correction for confounders becomes more rigorous, the biological signal disappears. Boussoussou and colleagues demonstrated this directly: in 1,652 patients with zero calcium score, the univariable association between PCAT attenuation and non-calcified plaque was statistically significant (+2 HU, p < 0.001). After multivariable adjustment for imaging parameters (kVp, pixel spacing, CNR) and patient characteristics (sex, BMI, heart rate), the association vanished entirely (p = 0.93) (Boussoussou et al. 2023).

This finding admits two interpretations, and the distinction between them is the crux of the field's unresolved debate. The first interpretation is that FAI's apparent biological signal is an artefact of confounding — larger patients receive higher kVp, producing higher FAI, and independently have more coronary disease. Remove the confounding pathway and no biological signal remains. The second interpretation is that the correction over-adjusts: some of the variance attributed to confounders is genuinely biological (inflammation causes tissue changes that alter scanner interactions), and removing it eliminates real signal along with artefact.

What is not in dispute is that the confounders account for most of the variance. Boussoussou's regression model identified tube voltage (+8 HU per step), pixel spacing (+32 HU per mm³), heart rate (−0.2 HU per bpm), BMI (−0.4 HU per kg/m²), and sex (+1 HU for male) as significant independent predictors of PCAT attenuation — and none of these are inflammation.

The Correction Paradox is diagnostic: it reveals that a measurement in which confounders account for more variance than biology is, at best, a noisy biological signal and, at worst, an artefact that happens to correlate with outcomes through shared confounders.

### 4.3 The Treatment Paradox

FAI predicts cardiac mortality with HR 29.8. Colchicine reduces MACE by 31%. Yet colchicine does not change FAI.

The LoDoCo2 CT substudy — a pre-specified cross-sectional analysis of 151 patients from the 5,522-patient parent trial — found no difference in PCAT attenuation between colchicine and placebo after a median of 28.2 months of treatment (−79.5 vs −78.7 HU, p = 0.236) (Fiolet et al. 2025). Neither hsCRP nor IL-6 correlated with PCAT attenuation in either treatment arm.

If FAI measured coronary inflammation, and colchicine reduced coronary inflammation sufficiently to prevent 31% of events, then FAI should have decreased in the colchicine arm. It did not. This failure has three possible explanations. First, colchicine may act through a pathway — neutrophil-mediated, inflammasome-downstream — that does not alter adipocyte phenotype and therefore does not change the CT-visible signal. Second, the 151-patient substudy may have been underpowered to detect a real change. Third, FAI may not measure inflammation with sufficient sensitivity to detect treatment effects, functioning as a risk marker (correlating with baseline risk) but not as a treatment-response marker (tracking therapeutic change).

The Treatment Paradox is diagnostic: it reveals the distinction between a proxy (which predicts who will have events) and a measure (which detects the mechanism by which treatment prevents them). A biomarker that cannot detect the effect of a proven therapy on the construct it claims to measure has uncertain construct validity, regardless of how well it predicts outcomes.

### 4.4 The Validation-Critique Paradox

Oxford and Erlangen co-authored CRISP-CT — the foundational study establishing FAI as a prognostic biomarker. Yet Erlangen (Hell et al. 2016) published the most cited argument that pericoronary fat attenuation variations are primarily imaging artefacts. How can the same group both validate and undermine the biomarker?

The resolution is that these are not contradictions — they address different validity domains. Oxford's CRISP-CT demonstrated predictive validity: FAI predicts cardiac death. Erlangen's critique challenged construct validity: the signal may be artefactual. Both can be true simultaneously, because predictive validity does not require construct validity. A confounded measurement can predict outcomes if the confounders correlate with disease through non-causal pathways. The paradox dissolves once the two validity types are distinguished — but the field has not made this distinction explicit.

### 4.5 The Dimensionality Paradox

If a single number (mean HU) is insufficient, extracting more numbers from the same data should help. PCAT radiomics — extracting 93 to 1,103 texture features per volume of interest — represents this intuition. Shang and colleagues demonstrated improved MACE prediction with radiomics (C-index 0.873 training, 0.824 validation) versus clinical and traditional CCTA features combined with FAI (C-index 0.645) in a multicentre study of 777 ACS patients (Shang et al. 2025).

Yet Wu and colleagues showed that 78% of these radiomic features are unstable across contrast perfusion phases (Wu et al. 2025). The Dimensionality Paradox is that enriching the signal space equally enriches the noise space. Each additional feature extracted from HU data is independently contaminated by *g*. More features multiplied by the same confounders yields more opportunities for overfitting to protocol-specific patterns — which explains why radiomic models often achieve strong internal validation but fail external validation. The information-theoretic ceiling is set by the source data: no amount of feature engineering can extract biological information that the single-energy HU measurement did not encode in the first place.

### 4.6 Summary: the paradoxes as a diagnostic panel

| Paradox | Evidence | What it disconfirms |
|---|---|---|
| Correction | Boussoussou: p = 0.93 after adjustment | FAI as direct inflammation measure |
| Treatment | LoDoCo2 substudy: no FAI change despite 31% MACE reduction | FAI as treatment-responsive biomarker |
| Validation-Critique | Oxford/Erlangen co-authored CRISP-CT; Erlangen published partial volume critique | Reconcilability of prediction with measurement |
| Dimensionality | 78% radiomic instability across perfusion phases | More features = more information |

Individually, each paradox is interpretable as a technical limitation with a technical fix. Collectively, they constitute a *pattern* — and the pattern points toward a single diagnosis: FAI has strong predictive validity and uncertain construct validity. It is a proxy, not a measurement.

---

## 5. How Groups Design Their Studies — and Why They Disagree

The field's disagreements are not random; they are predictable consequences of the assumptions each research group brings to study design. Understanding the methodological DNA of the major groups reveals why the same data generates contradictory conclusions.

### The Pragmatists: Oxford

Antoniades and colleagues approach FAI as a clinical tool. Their design philosophy is outcome-driven: if FAI predicts cardiac mortality in 40,091 patients, the mechanism is secondary. Study designs emphasise large multicentre retrospective cohorts (CRISP-CT: Erlangen + Cleveland, n = 1,872; ORFAN: 8 NHS hospitals, n = 40,091) that maximise statistical power for outcome prediction. The progressive evolution from raw FAI to FAI Score (adjusted for technical and demographic factors) to AI-Risk (integrating plaque burden) reflects iterative engineering: each version addresses specific criticisms of the last.

The blind spot is that outcome prediction does not require, and cannot establish, construct validity. A confounded measurement can predict outcomes if the confounders correlate with disease — and many of the confounders do. Larger patients receive higher kVp, produce higher FAI, and independently have higher cardiovascular risk. The predictive chain runs through physics, not biology. The proprietary nature of CaRi-Heart further limits independent verification of whether FAI Score's adjustments genuinely separate *f* from *g* or merely redistribute their contributions.

### The Sceptics: Erlangen, Zurich, and Case Western

These groups share a physics-first epistemology: any biological claim must survive the null hypothesis that the signal is artefactual. Their study designs are characteristically within-subject — the same patient scanned with different protocols (Zurich), the same raw data reconstructed with different kernels (Lisi et al. 2024), the same vessel measured at different contrast phases (Case Western). This design isolates individual confounders with experimental precision.

Erlangen's distance-from-lumen analysis (Hell et al. 2016) tested whether the FAI gradient follows physics (partial volume: signal decreases with distance from the contrast-enhanced lumen) or biology (inflammation diffusion: signal should peak at the adventitia, not the lumen edge). The gradient was consistent with partial volume. Zurich quantified reconstruction effects (up to 33 HU). Case Western quantified perfusion timing effects (7 HU swing, 78% radiomic instability).

The blind spot is that characterising the problem is not the same as solving it. These groups have established the floor of measurement uncertainty — any approach must exceed this floor to claim biological sensitivity — but they have not proposed a path forward beyond calling for standardisation.

### The Enrichers: ShuKun, Chinese multicentre groups, Cedars-Sinai

These groups reason that if a single summary statistic is insufficient, richer feature extraction should capture more biology. Their designs emphasise radiomic pipelines (93–1,103 features), machine learning (Lasso + XGBoost, random forest), and large multicentre cohorts that maximise statistical power for subgroup analyses.

The blind spot is foundational: all radiomic features are extracted from confounded HU data. Enriching the feature space without addressing the source data limitation is analogous to applying more sophisticated signal processing to a recording made with a broken microphone. The information content is bounded by the input, and no downstream analysis can recover information that was never encoded.

### The resolving approach: measurement-first development

The disagreements between these groups are irreconcilable within the HU domain because they are arguing about how much biology a fundamentally ambiguous measurement contains — and the answer depends on assumptions that cannot be tested with the measurement itself. The only way to determine whether FAI's predictive power derives from biology (*f*) or from confounders (*g*) is to measure *f* independently — through a method where *g* is eliminated by physics rather than by statistics.

Material decomposition provides this independent measurement. By acquiring data at multiple X-ray energies and decomposing each voxel into its constituent materials (water, lipid, collagen, iodine), material decomposition operates in the composition domain, where imaging parameters have no systematic effect (Nie & Molloi 2025). Water fraction RMSE of 0.01–0.64% across 80–135 kVp and three patient sizes demonstrates protocol independence — the same tissue composition yields the same water fraction regardless of how it is imaged. This is construct validity by design: the measurement has a known, physics-grounded relationship to the biological construct (tissue water content as a marker of adipocyte immaturity and inflammation).

The intellectual structure is important: material decomposition is not "better FAI." It is a measurement-first approach that establishes construct validity before testing predictive validity — inverting the order the field has followed. Whether composition-based PCAT biomarkers predict outcomes as well as, better than, or differently from HU-based FAI is an open empirical question. But it is the right question, because only a measurement with established construct validity can distinguish between biological risk and confounded correlation.

---

## 6. The Frontier and the Gap

### 6.1 What the field has established

Three propositions command strong, convergent evidence:

1. **Coronary inflammation causes cardiovascular events.** Three independent randomised controlled trials (CANTOS, COLCOT, LoDoCo2) targeting distinct inflammatory pathways all reduced MACE — convergent evidence at the highest level.

2. **FAI predicts cardiovascular events.** Multiple independent cohorts (CRISP-CT, ORFAN, Sagris meta-analysis of 20 studies and 7,797 patients, Sagoo meta-analysis of 17 studies and 57,862 patients) consistently demonstrate prognostic value — convergent evidence of predictive validity.

3. **FAI measurement is confounded.** Multiple independent groups (Boussoussou, Lisi, Wu, Hell, Tremamunno, Nie) have quantified technical confounders of comparable magnitude to the biological signal — convergent evidence of measurement limitations.

### 6.2 What the field has not established

Three questions remain open, and they are not peripheral — they define the field's structural uncertainty:

1. **Does FAI measure inflammation?** The histological validation (Antonopoulos et al. 2017) established that pericoronary fat phenotype changes with inflammation. It did not establish that the CT-measured HU change in a clinical setting reflects this biology rather than the confounders that shift HU by similar magnitudes. The Correction Paradox and Treatment Paradox cast doubt on the assumption that FAI's clinical signal is predominantly biological.

2. **Can FAI monitor treatment response?** The LoDoCo2 CT substudy's negative finding (p = 0.236) is a single, underpowered study — not definitive. But it is the only direct test, and it failed. Until a positive treatment-monitoring study is published, FAI's utility as a dynamic biomarker remains undemonstrated.

3. **Is FAI's predictive power causal or confounded?** If FAI predicts outcomes primarily because its confounders (kVp, body size, scanner) correlate with cardiovascular risk factors, then FAI is a proxy — useful but not mechanistically informative. This question can only be answered by measuring the biological signal independently and testing whether it retains predictive power.

### 6.3 The specific gap

The gap is not "more research is needed." The gap is a specific logical consequence of the field's current structure:

The field validated prediction before establishing measurement. It now has a biomarker that predicts outcomes (predictive validity) but may not measure what it claims (construct validity). Every correction strategy within the HU domain — from kVp conversion factors to FAI Score to radiomics — is an attempt to statistically separate biology from physics in a signal where they are physically inseparable.

The experiment that would resolve this has three components:

1. **Measure composition directly** — using material decomposition to quantify water and lipid fractions of pericoronary fat, independent of imaging protocol.
2. **Test construct validity** — determine whether composition-based measurements differ between inflamed and non-inflamed coronary segments, using histological or intravascular imaging as the reference standard.
3. **Test predictive validity** — determine whether composition-based measurements predict cardiovascular events, and whether their predictive power derives from biology (*f*) or is an artefact of confounders (*g*) that have been eliminated by design.

This experiment would not merely validate a new biomarker. It would answer the question the field has deferred for a decade: is the predictive power of pericoronary fat attenuation biological, confounded, or some mixture of both?

### 6.4 The broader lesson

The PCAT field's trajectory is not unique. It recapitulates a pattern that has played out across CT-based tissue characterisation: a single-energy HU measurement shows clinical promise, confounders are discovered, correction strategies proliferate, and the field eventually transitions to multi-energy material decomposition. This happened in renal stone characterisation, gout diagnosis, hepatic fat quantification, and iron overload imaging. In each case, the transition from HU-based approximation to composition-based measurement resolved long-standing discrepancies and enabled standardised, protocol-independent quantification.

Pericoronary adipose tissue is the next domain where this transition is due.

---

The trajectory of coronary inflammation imaging traces an arc from biological insight through predictive triumph to a measurement crisis that the field cannot yet resolve within its current paradigm. The accumulating paradoxes — signal disappearance under rigorous correction, outcome prediction without treatment response, radiomic enrichment that amplifies noise rather than signal — are not technical problems awaiting technical fixes. They are structural consequences of building a biomarker on a measurement that conflates biology with physics. The question the field has answered is whether pericoronary fat attenuation predicts cardiovascular events. The question it cannot yet answer — and must — is whether what it measures is inflammation, or merely a proxy shaped as much by the scanner as by the artery.

---

## References

1. Ross R. "Atherosclerosis — an inflammatory disease." *NEJM* 1999;340:115–126. [DOI](https://doi.org/10.1056/NEJM199901143400207)
2. Ridker PM et al. "Antiinflammatory therapy with canakinumab for atherosclerotic disease (CANTOS)." *NEJM* 2017;377:1119–1131. [DOI](https://doi.org/10.1056/NEJMoa1707914)
3. Tardif JC et al. "Efficacy and safety of low-dose colchicine after myocardial infarction (COLCOT)." *NEJM* 2019;381:2497–2505. [DOI](https://doi.org/10.1056/NEJMoa1912388)
4. Nidorf SM et al. "Colchicine in patients with chronic coronary disease (LoDoCo2)." *NEJM* 2020;383:1838–1847. [DOI](https://doi.org/10.1056/NEJMoa2021372)
5. Antonopoulos AS et al. "Detecting human coronary inflammation by imaging perivascular fat." *Sci Transl Med* 2017;9:eaal2658. [DOI](https://doi.org/10.1126/scitranslmed.aal2658)
6. Oikonomou EK et al. "Non-invasive detection of coronary inflammation using CT and prediction of residual cardiovascular risk (CRISP-CT)." *Lancet* 2018;392:929–939. [DOI](https://doi.org/10.1016/S0140-6736(18)31114-0)
7. Oikonomou EK et al. "A novel machine learning-derived radiotranscriptomic map of perivascular biology (ORFAN)." *Nat Cardiovasc Res* 2023. [DOI](https://doi.org/10.1038/s44161-023-00246-8)
8. Chan K et al. "Inflammatory risk and cardiovascular events in patients without obstructive coronary artery disease (ORFAN extended)." *Lancet* 2024. [DOI](https://doi.org/10.1016/S0140-6736(24)01811-9)
9. Fiolet ATL et al. "Effect of low-dose colchicine on pericoronary inflammation and coronary plaque composition (LoDoCo2 CT substudy)." *Heart* 2025. [DOI](https://doi.org/10.1136/heartjnl-2024-325527)
10. Ma R et al. "Towards reference values of pericoronary adipose tissue attenuation." *Eur Radiol* 2020. [DOI](https://doi.org/10.1007/s00330-020-07069-0)
11. Sagris M et al. "Pericoronary fat attenuation index — meta-analysis." *Eur Heart J Cardiovasc Imaging* 2022. [DOI](https://doi.org/10.1093/ehjci/jeac174)
12. Wu C et al. "Perfusion confounds on pericoronary adipose tissue." *J Clin Med* 2025. [DOI](https://doi.org/10.3390/jcm14030769)
13. Lisi C et al. "Kernel and reconstruction effects on FAI." *Eur Radiol* 2024. [DOI](https://doi.org/10.1007/s00330-024-11132-5)
14. Etter M et al. "Phantom kVp study — PCATMA conversion factors." *Eur Radiol* 2022. [DOI](https://doi.org/10.1007/s00330-022-09274-5)
15. Nie S, Molloi S. "Quantification of water and lipid composition of perivascular adipose tissue using coronary CT angiography: a simulation study." *Int J Cardiovasc Imaging* 2025;41:1091–1101. [DOI](https://doi.org/10.1007/s10554-025-03358-5)
16. Hell MM, Achenbach S et al. "CT-based analysis of pericoronary adipose tissue density." *JCCT* 2016;10(1):52–60. [DOI](https://doi.org/10.1016/j.jcct.2015.07.011)
17. Boussoussou et al. "The effect of patient and imaging characteristics on CCTA-assessed pericoronary adipose tissue." *JCCT* 2023. [DOI](https://doi.org/10.1016/j.jcct.2022.09.006)
18. Tremamunno G et al. "Intra-individual differences in pericoronary FAI between PCD and EID CT." *Acad Radiol* 2025;32(3). [DOI](https://doi.org/10.1016/j.acra.2024.11.055)
19. Shang J et al. "PCAT radiomics multicentre study." *Cardiovasc Diabetol* 2025. [DOI](https://doi.org/10.1186/s12933-025-02913-3)
20. Li et al. "PCATMA vs FAI diagnostic comparison." *Quant Imaging Med Surg* 2025. [DOI](https://doi.org/10.21037/qims-24-828)
21. Li et al. "Partial volume effects on pericoronary fat measurements." 2025.
22. Tan N et al. "Pericoronary adipose tissue as a marker of cardiovascular risk." *JACC* 2023. [DOI](https://doi.org/10.1016/j.jacc.2022.12.021)
23. Chan & Antoniades. "Pericoronary adipose tissue imaging and the need for standardized measurement of coronary inflammation." 2025. (editorial comment) [DOI](https://doi.org/10.1093/eurheartj/ehaf012)
24. Alvarez RE, Macovski A. "Energy-selective reconstructions in X-ray computerized tomography." *Phys Med Biol* 1976;21(5):733–744. [DOI](https://doi.org/10.1088/0031-9155/21/5/002)
25. Grönberg F et al. "Photon-counting detector CT: unconstrained three-material decomposition." *Eur Radiol* 2020. [DOI](https://doi.org/10.1007/s00330-020-07126-8)
26. Sagoo MK et al. "PCAT attenuation and MACE: meta-analysis." *Eur J Radiol* 2026. [DOI](https://doi.org/10.1016/j.ejrad.2026.111974)
27. Libby P et al. "The changing landscape of atherosclerosis." *Circulation* 2021. [DOI](https://doi.org/10.1161/CIRCULATIONAHA.121.054137)
28. Henrichot E et al. "Production of chemokines by perivascular adipose tissue." *ATVB* 2005. [DOI](https://doi.org/10.1161/01.ATV.0000188508.40052.35)
29. Ding Y, Molloi S. "Material decomposition for coronary plaque using DECT." *Int J Cardiovasc Imaging* 2021. [DOI](https://doi.org/10.1007/s10554-024-03124-9)
30. Mergen V et al. "Epicardial adipose tissue attenuation and FAI on photon-counting detector CT." *AJR* 2021. [DOI](https://doi.org/10.2214/AJR.21.26930)
