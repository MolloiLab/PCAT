# PCAT — Pericoronary Adipose Tissue Pipeline

Automatically measures fat around coronary arteries from a cardiac CT scan (CCTA). Outputs CPR images, HU histograms, radial profiles, and a per-vessel FAI summary.

---

## What does it do?

1. Finds your coronary arteries (LAD, LCX, RCA) automatically
2. Lets you review and refine the coronary seed locations
3. Lets you review and adjust the coronary artery centerlines and vessel wall contours
4. Generates the PCAT (pericoronary fat) volume and measures the **Fat Attenuation Index (FAI)**
5. Saves images and statistics you can review and report

> **FAI risk threshold: −70.1 HU.** Values above this (less negative) = higher cardiovascular inflammation risk (Oikonomou et al., Lancet 2018).

---

## Setup (one time)

```bash
git clone https://github.com/MolloiLab/PCAT.git
cd PCAT
pip install -r requirements.txt
```

Get a free TotalSegmentator research licence at:
`https://backend.totalsegmentator.com/license-academic/`

---

## Standard Workflow (semi-automatic, one command)

```bash
python pipeline/run_pipeline.py \
    --dicom Rahaf_Patients/1200.2 \
    --output output/patient_1200 \
    --prefix patient1200 \
    --auto-seeds
```

The pipeline runs all stages automatically and pauses at each review step:

### Stage 1 — Auto seed detection
TotalSegmentator detects the coronary artery locations (~30–60 s) and saves them to `seeds/`.

### Stage 2 — Seed Reviewer (opens automatically if no reviewed seeds exist)

A window opens showing 3 MPR planes with the auto-detected seeds overlaid.

| Key / Action | Effect |
|---|---|
| `1` / `2` / `3` | Switch active vessel (LAD / LCX / RCA) |
| Click on any plane | Move the selected seed to that location |
| `d` | Delete the current waypoint |
| `s` | **Save seeds & continue pipeline** |
| `q` | Quit without saving |
| Scroll wheel | Change slice |

> If reviewed seeds already exist from a previous run, this step is skipped automatically.

### Stage 3 — Coronary segmentation
TotalSegmentator segments the vessel walls using the reviewed seeds. Centerlines and radii are extracted.

### Stage 4 — Coronary Artery Contour Editor (opens automatically)

A window opens with the title **"=== PCAT Coronary Artery Contour Editor ==="** showing 3 MPR planes with vessel centerlines and wall contours overlaid.

**Vessel colors:** LAD = red · LCX = blue · RCA = green

| Key / Action | Effect |
|---|---|
| `1` / `2` / `3` | Switch active vessel |
| Click + drag a centerline point | Reposition that point; vessel mask updates on release |
| `[` / `]` | Decrease / increase radius at current point by 0.1 mm |
| `a` | Apply current radius to all points of the active vessel |
| `p` or "Add PCAT" button | Generate PCAT volume (outer = radius × 3) with semi-transparent yellow overlay |
| `s` | **Save contours & PCAT mask, continue pipeline** |
| `q` | Quit without saving |
| Scroll wheel | Change slice |

> Every drag or radius change immediately rebuilds the vessel mask, so the overlay always reflects your edits.

### Stage 5 — CPR Browser (opens automatically)

| Key / Action | Effect |
|---|---|
| Click on CPR panel | Jump to that vessel position |
| `←` / `→` | Step one point along the vessel |
| `s` | Save a PNG snapshot |
| `q` | Close and continue |

### Stage 6 — Statistics & output
FAI statistics are computed and all results are saved to `output/patient_1200/`.

---

## Fully Automatic Mode (batch / headless)

Use this for bulk processing or servers with no display.

```bash
python pipeline/run_pipeline.py \
    --dicom Rahaf_Patients/1200.2 \
    --output output/patient_1200 \
    --prefix patient1200 \
    --auto-seeds \
    --skip-editor \
    --skip-cpr-browser
```

**Run all patients at once:**

```bash
python pipeline/run_pipeline.py --batch --auto-seeds --skip-editor --skip-cpr-browser
```

> Do not use fully automatic mode for clinical reporting without a separate manual review step.

---

## Output files

All outputs land in the directory you set with `--output`:

| File | What it shows |
|------|--------------|
| `*_contours.json` | Adjusted centerlines and radii per vessel |
| `*_pcat_mask.npy` | Binary PCAT VOI mask (numpy array) |
| `*_cpr_fai.png` | CPR with FAI overlay — yellow/red = fat |
| `*_cpr_gray.png` | Grayscale CPR at 6 rotation angles |
| `*_cpr_native_rot*.png` | Curved CPR (Syngo.via style) |
| `*_hu_histogram.png` | HU distribution of fat voxels |
| `*_radial_profile.png` | Fat HU vs. distance from vessel wall |
| `*_summary.png` | Bar charts: FAI, fat fraction, voxel count |
| `*_results.json` | Numerical FAI statistics |

---

## Reading CPR images

- **Vessel runs top → bottom.** Top = ostium (origin), bottom = distal end.
- **Yellow/red regions** = pericoronary fat (FAI range −190 to −30 HU). Yellow = more negative HU (healthier). Red = less negative (more inflamed).
- **White dashed vertical line** = vessel centerline axis.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "too few centerline points" | Re-run and adjust seeds in the Seed Reviewer |
| NaN mean HU in results | No fat voxels in VOI; vessel may be heavily calcified |
| "only N vessels found" warning | Add the missing vessel manually in the Seed Reviewer |
| Seed Reviewer / Contour Editor won't open | Add `--skip-editor` (headless server) |
| TotalSegmentator fails | Place seeds manually: `python pipeline/seed_picker.py --dicom ... --output seeds/patient.json` |
| 3D render skipped | `pip install pyvista` |

---

## Patient data included

| Patient | DICOM folder | Slices |
|---------|-------------|--------|
| 1200 | `Rahaf_Patients/1200.2/` | 405 |
| 2 | `Rahaf_Patients/2.1/` | 149 |
| 317 | `Rahaf_Patients/317.6/` | 399 |

To add a new patient, change `--dicom` to the new DICOM folder and `--output` to a new folder.

---

## Adding multiple patients (batch)

Edit `PATIENT_CONFIGS` in `pipeline/run_pipeline.py`:

```python
PATIENT_CONFIGS = [
    {"patient_id": "1200", "dicom": "Rahaf_Patients/1200.2", "output": "output/patient_1200", "prefix": "patient1200"},
    {"patient_id": "999",  "dicom": "New_Patients/patient999", "output": "output/patient_999",  "prefix": "patient999"},
]
```

Then run:

```bash
python pipeline/run_pipeline.py --batch --auto-seeds
```
