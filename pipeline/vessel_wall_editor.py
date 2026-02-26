"""
vessel_wall_editor.py
Interactive matplotlib tool for reviewing and adjusting coronary artery vessel wall radii.

Usage:
    python vessel_wall_editor.py --dicom /path/to/patient/dir --seeds seeds/patient_X.json --vessel LAD --output overrides/patient_X_LAD.json

Interface:
  - Shows a cross-sectional view at each centerline point
  - Two adjustable circular overlays (inner = lumen wall, outer = adventitia/PCAT boundary)
  - Navigate between centerline points with arrow keys
  - Adjust radii with bracket keys
  - Apply current radii to all points with 'a' key
  - Save adjusted radii to JSON with 's' key

Output JSON format:
{
  "LAD": {
    "inner_radii_mm": [...],
    "outer_radii_mm": [...]
  }
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import matplotlib
matplotlib.use("TkAgg")  # Use interactive backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline.dicom_loader import load_dicom_series
from pipeline.centerline import (
    compute_vesselness, extract_centerline_seeds, clip_centerline_by_arclength,
    estimate_vessel_radii, load_seeds, VESSEL_CONFIGS
)


class VesselWallEditor:
    """
    Interactive vessel wall editor for adjusting inner and outer radii at each centerline point.
    
    Displays axial cross-sectional view with two adjustable circular overlays:
    - Red dashed circle for inner radius (lumen wall)
    - Yellow dashed circle for outer radius (PCAT boundary)
    """

    def __init__(
        self,
        volume: np.ndarray,
        spacing_mm: List[float],
        centerline_ijk: np.ndarray,
        radii_mm: np.ndarray,
        vessel_name: str,
        output_path: str | Path
    ):
        self.volume = volume
        self.spacing_mm = spacing_mm  # [sz, sy, sx]
        self.centerline_ijk = centerline_ijk
        self.vessel_name = vessel_name
        self.output_path = Path(output_path)
        self.shape = volume.shape  # (Z, Y, X)

        # Initialize radii
        self.inner_radii_mm = radii_mm.copy()  # From estimate_vessel_radii
        self.outer_radii_mm = radii_mm * 2.0   # Matches build_tubular_voi convention

        # Navigation state
        self.current_idx = 0
        self.num_points = len(centerline_ijk)

        # Window/level
        self.ww = 600   # window width
        self.wl = 50    # window level (center)
        
        # Cross-section size in mm
        self.crop_size_mm = 40.0
        
        # Track changes
        self.has_changes = False
        
        self._build_figure()
        self._connect_events()

    def _build_figure(self):
        self.fig = plt.figure(figsize=(12, 10))
        self.fig.suptitle(
            f"PCAT Vessel Wall Editor — {self.vessel_name}\n"
            "Keys: ←/→ prev/next point  [/] decrease/increase inner  {{/}} decrease/increase outer  "
            "a=apply to all  s=save  q=quit",
            fontsize=10,
        )

        # Layout: image + status
        gs = self.fig.add_gridspec(
            2, 1,
            height_ratios=[8, 1],
            hspace=0.1,
        )

        self.ax_image = self.fig.add_subplot(gs[0, 0])
        self.ax_status = self.fig.add_subplot(gs[1, 0])

        self.ax_image.set_title(f"Cross-sectional view at centerline point", fontsize=10)
        self.ax_image.axis("off")
        self.ax_status.axis("off")

        # Initialize image object
        self._update_image()
        self._update_status_bar()

    def _get_cross_section(self):
        """Extract a square crop around the current centerline point."""
        point_ijk = self.centerline_ijk[self.current_idx]
        z, y, x = point_ijk

        # Calculate crop size in voxels (isotropic in x,y plane)
        crop_size_vox = int(self.crop_size_mm / self.spacing_mm[2])
        
        # Extract axial slice at Z
        axial_slice = self.volume[z, :, :]
        
        # Calculate crop boundaries
        y_min = max(0, y - crop_size_vox // 2)
        y_max = min(self.shape[1], y + crop_size_vox // 2)
        x_min = max(0, x - crop_size_vox // 2)
        x_max = min(self.shape[2], x + crop_size_vox // 2)
        
        # Crop the slice
        crop = axial_slice[y_min:y_max, x_min:x_max]
        
        # Store offset for circle positioning
        self.crop_offset = (y_min, x_min)
        self.center_in_crop = (y - y_min, x - x_min)
        
        return crop

    def _update_image(self):
        """Update the displayed cross-section and circles."""
        self.ax_image.clear()
        self.ax_image.axis("off")
        
        # Get cross-section
        crop = self._get_cross_section()
        
        # Apply window/level
        lo = self.wl - self.ww / 2
        hi = self.wl + self.ww / 2
        crop_display = np.clip(crop, lo, hi)
        
        # Display the crop
        self.im = self.ax_image.imshow(
            crop_display, cmap="gray", aspect="equal",
            vmin=lo, vmax=hi, origin="upper"
        )
        
        # Get current radii in voxels
        inner_r_vox = self.inner_radii_mm[self.current_idx] / self.spacing_mm[2]
        outer_r_vox = self.outer_radii_mm[self.current_idx] / self.spacing_mm[2]
        
        # Draw circles
        center = (self.center_in_crop[1], self.center_in_crop[0])  # matplotlib uses (x, y)
        
        # Inner circle (red dashed)
        inner_circle = patches.Circle(
            center, inner_r_vox, fill=False,
            edgecolor='red', linestyle='--', linewidth=2,
            label=f"Inner: {self.inner_radii_mm[self.current_idx]:.1f}mm"
        )
        self.ax_image.add_patch(inner_circle)
        
        # Outer circle (yellow dashed)
        outer_circle = patches.Circle(
            center, outer_r_vox, fill=False,
            edgecolor='yellow', linestyle='--', linewidth=2,
            label=f"Outer: {self.outer_radii_mm[self.current_idx]:.1f}mm"
        )
        self.ax_image.add_patch(outer_circle)
        
        # Add legend
        self.ax_image.legend(loc="upper right", fontsize=8)
        
        # Set title with current point info
        point_ijk = self.centerline_ijk[self.current_idx]
        self.ax_image.set_title(
            f"Point {self.current_idx+1}/{self.num_points} at [{point_ijk[0]}, {point_ijk[1]}, {point_ijk[2]}]",
            fontsize=9
        )
        
        self._update_status_bar()
        self.fig.canvas.draw_idle()

    def _update_status_bar(self):
        self.ax_status.clear()
        self.ax_status.axis("off")
        
        inner_r = self.inner_radii_mm[self.current_idx]
        outer_r = self.outer_radii_mm[self.current_idx]
        
        msg = (
            f"  Point: {self.current_idx+1}/{self.num_points}  |  "
            f"Inner radius: {inner_r:.2f}mm  |  "
            f"Outer radius: {outer_r:.2f}mm  |  "
            f"Vessel: {self.vessel_name}  |  "
            f"{'[MODIFIED]' if self.has_changes else ''}"
        )
        
        self.ax_status.text(
            0.5, 0.5, msg,
            ha="center", va="center",
            transform=self.ax_status.transAxes,
            fontsize=9,
            bbox=dict(facecolor="black", alpha=0.7, edgecolor="none", pad=3),
            color="white" if not self.has_changes else "yellow"
        )

    def _connect_events(self):
        self.fig.canvas.mpl_connect("key_press_event", self._on_key)

    def _on_key(self, event):
        key = event.key
        
        if key == "left":
            # Previous point
            if self.current_idx > 0:
                self.current_idx -= 1
                self._update_image()
        elif key == "right":
            # Next point
            if self.current_idx < self.num_points - 1:
                self.current_idx += 1
                self._update_image()
        elif key == "[":
            # Decrease inner radius
            self.inner_radii_mm[self.current_idx] = max(0.1, self.inner_radii_mm[self.current_idx] - 0.1)
            self.has_changes = True
            self._update_image()
        elif key == "]":
            # Increase inner radius
            self.inner_radii_mm[self.current_idx] += 0.1
            self.has_changes = True
            self._update_image()
        elif key == "{":
            # Decrease outer radius
            self.outer_radii_mm[self.current_idx] = max(
                self.inner_radii_mm[self.current_idx] + 0.1,
                self.outer_radii_mm[self.current_idx] - 0.1
            )
            self.has_changes = True
            self._update_image()
        elif key == "}":
            # Increase outer radius
            self.outer_radii_mm[self.current_idx] += 0.1
            self.has_changes = True
            self._update_image()
        elif key == "a":
            # Apply current radii to all points
            self.inner_radii_mm[:] = self.inner_radii_mm[self.current_idx]
            self.outer_radii_mm[:] = self.outer_radii_mm[self.current_idx]
            self.has_changes = True
            self._update_image()
            print(f"[vessel_wall_editor] Applied current radii to all points")
        elif key == "A":
            # Apply current inner/outer ratio to all points
            current_ratio = self.outer_radii_mm[self.current_idx] / self.inner_radii_mm[self.current_idx]
            self.outer_radii_mm[:] = self.inner_radii_mm * current_ratio
            self.has_changes = True
            self._update_image()
            print(f"[vessel_wall_editor] Applied current ratio ({current_ratio:.2f}) to all points")
        elif key == "s":
            self._save()
            return
        elif key == "q":
            if self.has_changes:
                print("[vessel_wall_editor] You have unsaved changes. Press 's' to save or 'q' again to quit.")
                self.fig.canvas.mpl_connect("key_press_event", self._on_quit_confirm)
            else:
                plt.close(self.fig)
                return
        elif key == "w":
            self.ww = min(self.ww + 50, 3000)
            self._update_image()
        elif key == "W":
            self.ww = max(self.ww - 50, 50)
            self._update_image()
        elif key == "l":
            self.wl += 20
            self._update_image()
        elif key == "L":
            self.wl -= 20
            self._update_image()

    def _on_quit_confirm(self, event):
        if event.key == "q":
            plt.close(self.fig)
            return

    def _save(self):
        """Save radii to JSON file."""
        output = {
            self.vessel_name: {
                "inner_radii_mm": self.inner_radii_mm.tolist(),
                "outer_radii_mm": self.outer_radii_mm.tolist()
            }
        }
        
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"[vessel_wall_editor] Saved radii to {self.output_path}")
        self.has_changes = False
        self._update_status_bar()
        self.fig.canvas.draw_idle()

    def run(self):
        print(f"\n=== PCAT Vessel Wall Editor ===")
        print(f"Vessel: {self.vessel_name}")
        print(f"Centerline points: {self.num_points}")
        print("\nControls:")
        print("  ←/→    Previous/next centerline point")
        print("  [/]    Decrease/increase inner radius by 0.1mm")
        print("  {{/}}   Decrease/increase outer radius by 0.1mm")
        print("  a/A     Apply current radii/ratio to all points")
        print("  s       Save to JSON file")
        print("  w/W     Adjust window width")
        print("  l/L     Adjust window level")
        print("  q       Quit (prompts if unsaved changes)")
        print("\nStarting editor...\n")
        plt.show()


def main():
    epilog = """
HOW TO USE
----------
This tool allows radiologists to review and fine-tune vessel wall boundaries
for coronary arteries after the automated pipeline has extracted centerlines
and estimated initial radii.

STEP-BY-STEP
  1. The tool loads the DICOM volume and vessel seeds from the JSON file.
  
  2. It extracts the centerline and estimates initial radii using the same
     algorithms as the main pipeline.
  
  3. An axial cross-sectional view is shown at each centerline point with
     two circles:
     - Red dashed circle: inner radius (lumen wall)
     - Yellow dashed circle: outer radius (PCAT boundary)
  
  4. Use arrow keys to navigate between centerline points.
  
  5. Adjust radii at each point:
     [/] keys adjust inner radius (lumen wall)
     {{/}} keys adjust outer radius (PCAT boundary)
  
  6. Press 'a' to apply current radii values to all points, or 'A' to apply
     the current inner/outer ratio to all points.
  
  7. Press 's' to save the adjusted radii to a JSON file that can be used
     as an override by run_pipeline.py.
  
KEYBOARD SHORTCUTS
  ← / →       Navigate to previous/next centerline point
  [ / ]       Decrease/increase inner radius by 0.1mm
  { / }       Decrease/increase outer radius by 0.1mm
  a           Apply current inner and outer radii to all points
  A           Apply current inner/outer ratio to all points
  s           Save radii to JSON file
  w / W       Window width wider/narrower (adjust contrast)
  l / L       Window level brighter/darker (adjust brightness)
  q           Quit (prompts if unsaved changes)

TIPS
  - The cross-sectional view shows a ~40mm square crop around each point.
  - Window/level defaults to soft-tissue settings (W=600 L=50).
  - Inner radius typically represents the lumen wall boundary.
  - Outer radius represents the PCAT analysis boundary.
  - All changes are tracked; unsaved changes trigger a confirmation prompt.
"""
    parser = argparse.ArgumentParser(
        description="Interactive vessel wall editor for PCAT pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    parser.add_argument(
        "--dicom", required=True,
        help="Path to DICOM series directory for one patient"
    )
    parser.add_argument(
        "--seeds", required=True,
        help="Path to seed JSON file containing vessel ostium and waypoints"
    )
    parser.add_argument(
        "--vessel", required=True, choices=["LAD", "LCX", "RCA"],
        help="Vessel name to edit"
    )
    parser.add_argument(
        "--output", required=True,
        help="Output path for radii override JSON file"
    )
    args = parser.parse_args()

    print(f"[vessel_wall_editor] Loading DICOM from {args.dicom} ...")
    volume, meta = load_dicom_series(args.dicom)
    spacing_mm = meta["spacing_mm"]
    print(f"[vessel_wall_editor] Volume shape: {volume.shape}, spacing: {spacing_mm}")

    print(f"[vessel_wall_editor] Loading seeds from {args.seeds} ...")
    seeds = load_seeds(args.seeds)
    
    if args.vessel not in seeds:
        print(f"[vessel_wall_editor] ERROR: Vessel {args.vessel} not found in seeds file")
        print(f"[vessel_wall_editor] Available vessels: {list(seeds.keys())}")
        sys.exit(1)
    
    vessel_seeds = seeds[args.vessel]
    ostium_ijk = vessel_seeds["ostium_ijk"]
    waypoints_ijk = vessel_seeds["waypoints_ijk"]
    
    print(f"[vessel_wall_editor] Extracting centerline for {args.vessel} ...")
    
    # Compute vesselness on ROI around seeds
    all_seed_points = [ostium_ijk] + waypoints_ijk
    vesselness = compute_vesselness(volume, spacing_mm, seed_points=all_seed_points)
    
    # Extract centerline
    centerline_ijk = extract_centerline_seeds(
        volume, vesselness, spacing_mm, ostium_ijk, waypoints_ijk
    )
    
    # Clip to proximal segment
    vessel_config = VESSEL_CONFIGS[args.vessel]
    centerline_ijk = clip_centerline_by_arclength(
        centerline_ijk, spacing_mm,
        start_mm=vessel_config["start_mm"],
        length_mm=vessel_config["length_mm"]
    )
    
    print(f"[vessel_wall_editor] Centerline extracted: {len(centerline_ijk)} points")
    
    # Estimate initial radii
    radii_mm = estimate_vessel_radii(volume, centerline_ijk, spacing_mm)
    print(f"[vessel_wall_editor] Initial radii estimated: {radii_mm.mean():.2f} ± {radii_mm.std():.2f} mm")
    
    # Create and run editor
    editor = VesselWallEditor(
        volume, spacing_mm, centerline_ijk, radii_mm,
        args.vessel, args.output
    )
    editor.run()


if __name__ == "__main__":
    main()