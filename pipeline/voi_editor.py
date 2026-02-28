"""
voi_editor.py
Interactive matplotlib/Tkinter GUI for post-segmentation manual review and
editing of PCAT VOI masks.

Usage:
    python voi_editor.py --dicom /path/to/dicom --voi voi_mask.npy --vessel LAD --output edited.npy

Key improvements over original:
  - Tkinter mode toolbar (Paint / Erase / Threshold / Pan)
  - Live brush-cursor circle that follows the mouse
  - Threshold Paint mode: only marks FAI-range fat voxels (−190 to −30 HU)
  - Auto-VOI shown in blood-red; switches to yellow-green once any edit is made
  - Ctrl+scroll = zoom in/out per panel; middle-drag = pan
  - [ / ] keys for brush size (Photoshop/Krita convention); +/- also work
  - Scroll wheel alone = change slice (unchanged)
  - Undo stack up to 30 levels
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import deque

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline.dicom_loader import load_dicom_series


# ─────────────────────────────────────────
# Colour constants
# ─────────────────────────────────────────
_AUTO_VOI_RGBA   = [0.82, 0.10, 0.12, 0.45]   # blood-red  — auto-generated
_EDITED_VOI_RGBA = [0.85, 0.85, 0.10, 0.38]   # yellow-gold — after first manual edit
_BRUSH_CURSOR_COLOR = "#00FFFF"                # cyan
_THRESHOLD_CURSOR_COLOR = "#FF6600"            # orange — threshold mode


class VOIEditor:
    """
    Interactive 3-plane VOI mask editor for PCAT pipeline.

    Shows axial / coronal / sagittal MPR views with a semi-transparent VOI
    mask overlay.  A Tkinter toolbar above the matplotlib canvas provides
    one-click mode switching.  The brush cursor is drawn as a circle patch
    that follows the mouse.
    """

    # ─── Init ───────────────────────────────────────────────────────────────

    def __init__(
        self,
        volume: np.ndarray,
        voi_mask: np.ndarray,
        spacing_mm: List[float],
        vessel_name: str,
        output_path,
    ):
        self.volume   = volume
        self.voi_mask = voi_mask.astype(bool)
        self.original_voi_mask = voi_mask.astype(bool).copy()
        self.spacing_mm  = spacing_mm   # [sz, sy, sx]
        self.vessel_name = vessel_name
        self.output_path = Path(output_path)
        self.shape = volume.shape       # (Z, Y, X)

        # Slice indices
        self.z_slice = self.shape[0] // 2
        self.y_slice = self.shape[1] // 2
        self.x_slice = self.shape[2] // 2

        # Edit state
        self.brush_radius = 3
        self.painting     = False
        self.mode         = "paint"   # "paint" | "erase" | "threshold" | "pan"
        self._edited      = False     # becomes True on first paint stroke

        # Undo
        self.undo_stack = deque(maxlen=30)

        # Window / level
        self.ww = 600
        self.wl = 50

        # Pan state (per-axis): {ax: (x0, y0, xlim, ylim)}
        self._pan_state: dict = {}

        # Zoom limits cache (original, so we can reset)
        self._orig_xlim: dict = {}
        self._orig_ylim: dict = {}

        # Brush cursor patches: one Circle per axis
        self._cursor_patches: dict = {}

        self._build_figure()
        self._connect_events()
        self._add_tk_toolbar()

    # ─── Figure construction ─────────────────────────────────────────────────

    def _build_figure(self):
        self.fig = plt.figure(figsize=(19, 10))
        self.fig.patch.set_facecolor("#1a1a1a")

        gs = self.fig.add_gridspec(
            2, 4,
            width_ratios=[1, 1, 1, 0.55],
            height_ratios=[5, 1],
            hspace=0.06,
            wspace=0.08,
        )

        self.ax_axial    = self.fig.add_subplot(gs[0, 0])
        self.ax_coronal  = self.fig.add_subplot(gs[0, 1])
        self.ax_sagittal = self.fig.add_subplot(gs[0, 2])
        self.ax_info     = self.fig.add_subplot(gs[0, 3])
        self.ax_status   = self.fig.add_subplot(gs[1, :3])

        for ax in (self.ax_axial, self.ax_coronal, self.ax_sagittal,
                   self.ax_info, self.ax_status):
            ax.set_facecolor("#111111")

        titles = [
            ("Axial",    "scroll=slice  Ctrl+scroll=zoom  mid-drag=pan"),
            ("Coronal",  "scroll=slice  Ctrl+scroll=zoom  mid-drag=pan"),
            ("Sagittal", "scroll=slice  Ctrl+scroll=zoom  mid-drag=pan"),
        ]
        for ax, (plane, hint) in zip(
            [self.ax_axial, self.ax_coronal, self.ax_sagittal], titles
        ):
            ax.set_title(f"{plane}\n{hint}", fontsize=7, color="#bbbbbb", pad=3)
            ax.axis("off")

        self.ax_info.set_title("VOI Info", fontsize=9, color="#cccccc", pad=3)
        self.ax_info.axis("off")
        self.ax_status.axis("off")

        clim = self._clim()

        self.im_axial = self.ax_axial.imshow(
            self._axial_slice(), cmap="gray", aspect="equal",
            vmin=clim[0], vmax=clim[1], origin="upper")
        self.im_coronal = self.ax_coronal.imshow(
            self._coronal_slice(), cmap="gray", aspect="auto",
            vmin=clim[0], vmax=clim[1], origin="upper")
        self.im_sagittal = self.ax_sagittal.imshow(
            self._sagittal_slice(), cmap="gray", aspect="auto",
            vmin=clim[0], vmax=clim[1], origin="upper")

        self.overlay_axial    = self.ax_axial.imshow(
            self._axial_voi_overlay(), aspect="equal", origin="upper")
        self.overlay_coronal  = self.ax_coronal.imshow(
            self._coronal_voi_overlay(), aspect="auto", origin="upper")
        self.overlay_sagittal = self.ax_sagittal.imshow(
            self._sagittal_voi_overlay(), aspect="auto", origin="upper")

        self._draw_crosshairs()

        # Cache original zoom limits after first draw
        self.fig.canvas.draw()
        for ax in (self.ax_axial, self.ax_coronal, self.ax_sagittal):
            self._orig_xlim[ax] = ax.get_xlim()
            self._orig_ylim[ax] = ax.get_ylim()

        # Create invisible brush-cursor circles (one per image axis)
        cursor_axes = [self.ax_axial, self.ax_coronal, self.ax_sagittal]
        for ax in cursor_axes:
            circ = Circle((0, 0), radius=self.brush_radius,
                          linewidth=1.5, edgecolor=_BRUSH_CURSOR_COLOR,
                          facecolor="none", linestyle="-", zorder=10, visible=False)
            ax.add_patch(circ)
            self._cursor_patches[ax] = circ

        self._update_status_bar()
        self._update_info_panel()

    def _clim(self):
        lo = self.wl - self.ww / 2
        hi = self.wl + self.ww / 2
        return lo, hi

    # ─── Tkinter toolbar ─────────────────────────────────────────────────────

    def _add_tk_toolbar(self):
        """Inject a Tkinter frame with mode-toggle buttons above the canvas."""
        try:
            import tkinter as tk
            canvas_widget = self.fig.canvas.get_tk_widget()
            parent = canvas_widget.master

            self._tk_frame = tk.Frame(parent, bg="#2a2a2a", pady=3)
            self._tk_frame.pack(side=tk.TOP, fill=tk.X, before=canvas_widget)

            lbl = tk.Label(self._tk_frame, text="  Mode:", bg="#2a2a2a",
                           fg="#aaaaaa", font=("Helvetica", 10))
            lbl.pack(side=tk.LEFT, padx=(6, 2))

            self._tk_buttons: dict[str, tk.Button] = {}
            btn_specs = [
                ("paint",     "🖌  Paint",     "#336633"),
                ("erase",     "⌫  Erase",      "#663333"),
                ("threshold", "⭕  Fat-only",   "#664400"),
                ("pan",       "✋  Pan",        "#334455"),
            ]
            for mode_key, label, active_bg in btn_specs:
                btn = tk.Button(
                    self._tk_frame, text=label,
                    command=lambda m=mode_key: self._set_mode(m),
                    width=11, relief=tk.RAISED, font=("Helvetica", 9),
                    bg="#3a3a3a", fg="#dddddd", activebackground="#555555",
                    bd=1, cursor="hand2",
                )
                btn.pack(side=tk.LEFT, padx=3)
                self._tk_buttons[mode_key] = btn

            # Brush size display
            self._tk_brush_lbl = tk.Label(
                self._tk_frame,
                text=f"  Brush: {self.brush_radius}px  [ / ]",
                bg="#2a2a2a", fg="#aaaaaa", font=("Helvetica", 9),
            )
            self._tk_brush_lbl.pack(side=tk.LEFT, padx=8)

            # Confirm and Save button
            save_btn = tk.Button(
                self._tk_frame, text="\u2713 Confirm and Save",
                command=self._save,
                width=18, relief=tk.RAISED, font=("Helvetica", 9, "bold"),
                bg="#1a5f1a", fg="white", activebackground="#2e8b2e",
                bd=2, cursor="hand2",
            )
            save_btn.pack(side=tk.RIGHT, padx=(4, 10))

            # Keyboard hint
            hint = tk.Label(
                self._tk_frame,
                text="  Ctrl+Z=undo  s=save  q=quit  w/W=WW  l/L=WL",
                bg="#2a2a2a", fg="#666666", font=("Helvetica", 8),
            )
            hint.pack(side=tk.LEFT, padx=4)

            self._tk_active_bg = dict(
                paint="#336633", erase="#663333",
                threshold="#664400", pan="#334455"
            )
            self._highlight_active_button()

        except Exception:
            # Graceful degradation: if Tk is unavailable, toolbar is skipped
            pass

    def _set_mode(self, mode: str):
        self.mode = mode
        self._highlight_active_button()
        self._update_status_bar()
        self.fig.canvas.draw_idle()

    def _highlight_active_button(self):
        if not hasattr(self, "_tk_buttons"):
            return
        for key, btn in self._tk_buttons.items():
            if key == self.mode:
                btn.config(bg=self._tk_active_bg[key],
                           relief="sunken", fg="white")
            else:
                btn.config(bg="#3a3a3a", relief="raised", fg="#dddddd")

    # ─── Slice extraction ────────────────────────────────────────────────────

    def _axial_slice(self):
        return self.volume[self.z_slice, :, :]

    def _coronal_slice(self):
        return np.flipud(self.volume[:, self.y_slice, :])

    def _sagittal_slice(self):
        return np.flipud(self.volume[:, :, self.x_slice])

    # ─── VOI overlay ─────────────────────────────────────────────────────────

    def _voi_rgba(self):
        """Return the colour used for the overlay based on edit state."""
        return _EDITED_VOI_RGBA if self._edited else _AUTO_VOI_RGBA

    def _axial_voi_overlay(self):
        overlay = np.zeros((self.shape[1], self.shape[2], 4), dtype=np.float32)
        voi_slice = self.voi_mask[self.z_slice, :, :]
        overlay[voi_slice] = self._voi_rgba()
        return overlay

    def _coronal_voi_overlay(self):
        overlay = np.zeros((self.shape[0], self.shape[2], 4), dtype=np.float32)
        voi_slice = np.flipud(self.voi_mask[:, self.y_slice, :])
        overlay[voi_slice] = self._voi_rgba()
        return overlay

    def _sagittal_voi_overlay(self):
        overlay = np.zeros((self.shape[0], self.shape[1], 4), dtype=np.float32)
        voi_slice = np.flipud(self.voi_mask[:, :, self.x_slice])
        overlay[voi_slice] = self._voi_rgba()
        return overlay

    # ─── Crosshairs ──────────────────────────────────────────────────────────

    def _draw_crosshairs(self):
        for attr in ("_ch_ax", "_ch_co", "_ch_sa"):
            if hasattr(self, attr):
                for ln in getattr(self, attr):
                    ln.remove()

        kw = dict(color="yellow", linewidth=0.7, alpha=0.55, linestyle="--")
        flipped_z = self.shape[0] - 1 - self.z_slice
        self._ch_ax = [
            self.ax_axial.axhline(self.y_slice, **kw),
            self.ax_axial.axvline(self.x_slice, **kw),
        ]
        self._ch_co = [
            self.ax_coronal.axhline(flipped_z, **kw),
            self.ax_coronal.axvline(self.x_slice, **kw),
        ]
        self._ch_sa = [
            self.ax_sagittal.axhline(flipped_z, **kw),
            self.ax_sagittal.axvline(self.y_slice, **kw),
        ]

    # ─── Refresh ─────────────────────────────────────────────────────────────

    def _refresh_images(self):
        clim = self._clim()
        self.im_axial.set_data(self._axial_slice())
        self.im_axial.set_clim(clim)
        self.im_coronal.set_data(self._coronal_slice())
        self.im_coronal.set_clim(clim)
        self.im_sagittal.set_data(self._sagittal_slice())
        self.im_sagittal.set_clim(clim)

        self.overlay_axial.set_data(self._axial_voi_overlay())
        self.overlay_coronal.set_data(self._coronal_voi_overlay())
        self.overlay_sagittal.set_data(self._sagittal_voi_overlay())

        self._draw_crosshairs()
        self._update_status_bar()
        self.fig.canvas.draw_idle()

    # ─── Status / info panels ─────────────────────────────────────────────────

    def _mode_label(self):
        return {
            "paint":     "PAINT  (left-drag to add)",
            "erase":     "ERASE  (left-drag to remove)",
            "threshold": "FAT-ONLY PAINT  (−190→−30 HU only)",
            "pan":       "PAN  (left-drag to move view)",
        }[self.mode]

    def _update_status_bar(self):
        self.ax_status.cla()
        self.ax_status.axis("off")
        color_map = {"paint": "#88cc88", "erase": "#cc6666",
                     "threshold": "#dd9944", "pan": "#6699cc"}
        msg = (
            f"  Z={self.z_slice}  Y={self.y_slice}  X={self.x_slice}  |  "
            f"Brush: {self.brush_radius}px  |  "
            f"Mode: {self._mode_label()}  |  "
            f"VOI voxels: {self.voi_mask.sum()}  |  "
            f"W/L: {self.ww}/{self.wl}"
        )
        self.ax_status.text(
            0.01, 0.5, msg,
            ha="left", va="center",
            transform=self.ax_status.transAxes,
            fontsize=8.5,
            color=color_map[self.mode],
            bbox=dict(facecolor="#111111", alpha=0.85, edgecolor="none", pad=3),
        )

    def _update_info_panel(self):
        self.ax_info.cla()
        self.ax_info.axis("off")

        total   = int(self.voi_mask.sum())
        orig    = int(self.original_voi_mask.sum())
        diff    = total - orig
        fat_mask = (self.volume >= -190) & (self.volume <= -30)
        fat_voi  = int(np.logical_and(self.voi_mask, fat_mask).sum())

        overlay_note = (
            "● blood-red  (auto)" if not self._edited
            else "● yellow  (edited)"
        )
        lines = [
            f"Vessel: {self.vessel_name}",
            "",
            overlay_note,
            "",
            f"VOI voxels:  {total}",
            f"  Original:  {orig}",
            f"  Delta:     {'+' if diff >= 0 else ''}{diff}",
            "",
            f"Fat voxels:  {fat_voi}",
            "",
            f"Brush: {self.brush_radius}px",
            "",
            "── Modes ──────────",
            "🖌  Paint  (left-drag)",
            "⌫  Erase  (left-drag)",
            "⭕  Fat-only  (−190→−30)",
            "✋  Pan    (left-drag)",
            "",
            "── Keys ────────────",
            "[ / ]   brush size",
            "Ctrl+Z  undo",
            "s       save",
            "q       quit",
        ]

        self.ax_info.text(
            0.05, 0.97, "\n".join(lines),
            ha="left", va="top",
            transform=self.ax_info.transAxes,
            fontsize=7.5,
            family="monospace",
            color="#cccccc",
        )

    # ─── Brush cursor ─────────────────────────────────────────────────────────

    def _update_cursor(self, ax, ix: float, iy: float, visible: bool = True):
        """Move the brush-cursor circle on the given axis."""
        for a, circ in self._cursor_patches.items():
            if a is ax and visible:
                # Radius in data coordinates (pixels of image): just brush_radius
                circ.set_center((ix, iy))
                circ.set_radius(self.brush_radius)
                color = (_THRESHOLD_CURSOR_COLOR if self.mode == "threshold"
                         else _BRUSH_CURSOR_COLOR)
                circ.set_edgecolor(color)
                circ.set_visible(True)
            else:
                circ.set_visible(False)

    # ─── Painting ────────────────────────────────────────────────────────────

    def _paint_voxels(self, z: int, y: int, x: int):
        Z, Y, X = self.shape
        r = self.brush_radius
        zz, yy, xx = np.meshgrid(
            np.arange(max(0, z - r), min(Z, z + r + 1)),
            np.arange(max(0, y - r), min(Y, y + r + 1)),
            np.arange(max(0, x - r), min(X, x + r + 1)),
            indexing="ij",
        )
        in_sphere = (zz - z)**2 + (yy - y)**2 + (xx - x)**2 <= r**2

        if self.mode == "paint":
            self.voi_mask[zz[in_sphere], yy[in_sphere], xx[in_sphere]] = True
        elif self.mode == "erase":
            self.voi_mask[zz[in_sphere], yy[in_sphere], xx[in_sphere]] = False
        elif self.mode == "threshold":
            # Only paint voxels within FAI HU range (−190 to −30 HU)
            coords_z = zz[in_sphere]
            coords_y = yy[in_sphere]
            coords_x = xx[in_sphere]
            hu_vals   = self.volume[coords_z, coords_y, coords_x]
            fat_mask  = (hu_vals >= -190) & (hu_vals <= -30)
            self.voi_mask[
                coords_z[fat_mask], coords_y[fat_mask], coords_x[fat_mask]
            ] = True

    def _save_undo(self):
        self.undo_stack.append(self.voi_mask.copy())

    def _undo(self):
        if self.undo_stack:
            self.voi_mask = self.undo_stack.pop()
            self._refresh_images()
            self._update_info_panel()

    # ─── Coordinate helpers ───────────────────────────────────────────────────

    def _event_to_zyx(self, event) -> Optional[Tuple[int, int, int]]:
        """Convert a matplotlib mouse event to (z, y, x) voxel coordinates."""
        ax = event.inaxes
        if ax not in (self.ax_axial, self.ax_coronal, self.ax_sagittal):
            return None
        if event.xdata is None or event.ydata is None:
            return None

        ix = int(round(event.xdata))
        iy = int(round(event.ydata))

        if ax == self.ax_axial:
            z, y, x = self.z_slice, iy, ix
        elif ax == self.ax_coronal:
            actual_z = self.shape[0] - 1 - iy
            z, y, x  = actual_z, self.y_slice, ix
        else:  # sagittal
            actual_z = self.shape[0] - 1 - iy
            z, y, x  = actual_z, iy, self.x_slice

        z = int(np.clip(z, 0, self.shape[0] - 1))
        y = int(np.clip(y, 0, self.shape[1] - 1))
        x = int(np.clip(x, 0, self.shape[2] - 1))
        return z, y, x

    # ─── Events ──────────────────────────────────────────────────────────────

    def _connect_events(self):
        c = self.fig.canvas.mpl_connect
        c("button_press_event",   self._on_button_press)
        c("button_release_event", self._on_button_release)
        c("motion_notify_event",  self._on_motion)
        c("scroll_event",         self._on_scroll)
        c("key_press_event",      self._on_key)

    def _on_button_press(self, event):
        ax = event.inaxes
        if ax is None:
            return

        # Middle button: start pan
        if event.button == 2:
            self._pan_state[ax] = (
                event.xdata, event.ydata,
                ax.get_xlim(), ax.get_ylim(),
            )
            return

        if event.button not in (1, 3):
            return
        if ax not in (self.ax_axial, self.ax_coronal, self.ax_sagittal):
            return

        # Right-click always erases regardless of toolbar mode
        if event.button == 3:
            effective_mode = "erase"
        else:
            effective_mode = self.mode

        if effective_mode == "pan":
            self._pan_state[ax] = (
                event.xdata, event.ydata,
                ax.get_xlim(), ax.get_ylim(),
            )
            return

        self.painting = True
        self._save_undo()
        if not self._edited and effective_mode in ("paint", "threshold"):
            self._edited = True

        # Temporarily override mode for right-click
        self._active_mode = effective_mode

        coords = self._event_to_zyx(event)
        if coords is None:
            return
        z, y, x = coords
        self._update_slice_from_zyx(ax, z, y, x)
        orig_mode, self.mode = self.mode, self._active_mode
        self._paint_voxels(z, y, x)
        self.mode = orig_mode
        self._refresh_images()
        self._update_info_panel()

    def _on_button_release(self, event):
        self.painting = False
        self._pan_state.pop(event.inaxes, None)

    def _on_motion(self, event):
        ax = event.inaxes
        if ax is None:
            # Hide cursor when off canvas
            for circ in self._cursor_patches.values():
                circ.set_visible(False)
            self.fig.canvas.draw_idle()
            return

        if event.xdata is None or event.ydata is None:
            return

        ix, iy = event.xdata, event.ydata

        # Show brush cursor when hovering an image panel (not in pan mode)
        if ax in self._cursor_patches:
            if self.mode != "pan":
                self._update_cursor(ax, ix, iy, visible=True)
            else:
                for circ in self._cursor_patches.values():
                    circ.set_visible(False)

        # Pan drag (middle or left in pan mode)
        if ax in self._pan_state:
            x0, y0, xlim0, ylim0 = self._pan_state[ax]
            dx = x0 - ix
            dy = y0 - iy
            ax.set_xlim(xlim0[0] + dx, xlim0[1] + dx)
            ax.set_ylim(ylim0[0] + dy, ylim0[1] + dy)
            self.fig.canvas.draw_idle()
            return

        if not self.painting:
            self.fig.canvas.draw_idle()
            return
        if ax not in (self.ax_axial, self.ax_coronal, self.ax_sagittal):
            return

        coords = self._event_to_zyx(event)
        if coords is None:
            return
        z, y, x = coords
        self._update_slice_from_zyx(ax, z, y, x)

        orig_mode, self.mode = self.mode, self._active_mode
        self._paint_voxels(z, y, x)
        self.mode = orig_mode
        self._refresh_images()
        self._update_info_panel()

    def _update_slice_from_zyx(self, ax, z, y, x):
        if ax == self.ax_axial:
            self.y_slice = y
            self.x_slice = x
        elif ax == self.ax_coronal:
            self.z_slice = z
            self.x_slice = x
        else:  # sagittal
            self.z_slice = z
            self.y_slice = y

    def _on_scroll(self, event):
        ax = event.inaxes
        if ax not in (self.ax_axial, self.ax_coronal, self.ax_sagittal):
            return

        delta = 1 if event.button == "up" else -1

        # Ctrl+scroll → zoom
        if event.key == "control":
            factor = 0.85 if delta > 0 else 1.0 / 0.85
            xlim = ax.get_xlim()
            ylim = ax.get_ylim()
            xc = (xlim[0] + xlim[1]) / 2
            yc = (ylim[0] + ylim[1]) / 2
            xh = (xlim[1] - xlim[0]) / 2 * factor
            yh = (ylim[1] - ylim[0]) / 2 * factor
            ax.set_xlim(xc - xh, xc + xh)
            ax.set_ylim(yc - yh, yc + yh)
            self.fig.canvas.draw_idle()
            return

        # Plain scroll → change slice
        if ax == self.ax_axial:
            self.z_slice = int(np.clip(self.z_slice + delta, 0, self.shape[0] - 1))
        elif ax == self.ax_coronal:
            self.y_slice = int(np.clip(self.y_slice + delta, 0, self.shape[1] - 1))
        else:
            self.x_slice = int(np.clip(self.x_slice + delta, 0, self.shape[2] - 1))

        self._refresh_images()

    def _on_key(self, event):
        key = event.key

        if key in ("u", "ctrl+z"):
            self._undo()
        elif key in ("+", "="):
            self._resize_brush(+1)
        elif key == "-":
            self._resize_brush(-1)
        elif key == "]":
            self._resize_brush(+1)
        elif key == "[":
            self._resize_brush(-1)
        elif key == "1":
            self._set_mode("paint")
        elif key == "2":
            self._set_mode("erase")
        elif key == "3":
            self._set_mode("threshold")
        elif key == "4":
            self._set_mode("pan")
        elif key == "s":
            self._save()
            return
        elif key == "q":
            plt.close(self.fig)
            return
        elif key == "w":
            self.ww = min(self.ww + 50, 3000)
        elif key == "W":
            self.ww = max(self.ww - 50, 50)
        elif key == "l":
            self.wl += 20
        elif key == "L":
            self.wl -= 20
        elif key == "r":
            # Reset zoom on all panels
            for ax in (self.ax_axial, self.ax_coronal, self.ax_sagittal):
                if ax in self._orig_xlim:
                    ax.set_xlim(self._orig_xlim[ax])
                    ax.set_ylim(self._orig_ylim[ax])

        self._refresh_images()
        self._update_info_panel()
        self._update_status_bar()
        self.fig.canvas.draw_idle()

    def _resize_brush(self, delta: int):
        self.brush_radius = int(np.clip(self.brush_radius + delta, 1, 20))
        if hasattr(self, "_tk_brush_lbl"):
            self._tk_brush_lbl.config(
                text=f"  Brush: {self.brush_radius}px  [ / ]"
            )
        # Update visible cursor immediately
        for circ in self._cursor_patches.values():
            if circ.get_visible():
                circ.set_radius(self.brush_radius)

    # ─── Save ─────────────────────────────────────────────────────────────────

    def _save(self):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(self.output_path, self.voi_mask)
        try:
            import nibabel as nib
            affine = np.diag([-self.spacing_mm[2], -self.spacing_mm[1],
                               self.spacing_mm[0], 1])
            nii = nib.Nifti1Image(self.voi_mask.astype(np.uint8), affine)
            nii_path = self.output_path.with_suffix(".nii.gz")
            nib.save(nii, nii_path)
            print(f"[voi_editor] Saved → {self.output_path}  and  {nii_path}")
        except ImportError:
            print(f"[voi_editor] Saved → {self.output_path}  (nibabel unavailable)")

        self.fig.suptitle(
            f"✓ SAVED — {self.output_path.name}",
            fontsize=10, color="#88ee88",
        )
        self.fig.canvas.draw_idle()

    # ─── Run ─────────────────────────────────────────────────────────────────

    def run(self):
        print("\n=== PCAT VOI Editor ===")
        print("Toolbar: Paint / Erase / Fat-only / Pan  (or keys 1/2/3/4)")
        print("Keys:  [ / ]  brush size    Ctrl+Z  undo    s  save    q  quit")
        print("       Ctrl+scroll  zoom    middle-drag  pan    r  reset zoom")
        print("       right-click always erases regardless of toolbar mode")
        print("\n⚠️  Blood-red overlay = auto-generated VOI.  Review before saving.\n")
        plt.show()


# ─────────────────────────────────────────────
# Pipeline integration
# ─────────────────────────────────────────────

def launch_voi_editor(
    volume: np.ndarray,
    voi_mask: np.ndarray,
    vessel_name: str,
    output_path,
    spacing_mm,
) -> np.ndarray:
    """
    Launch the VOI editor for mandatory clinical review.  Blocks until closed.
    Returns the (possibly edited) VOI mask.
    """
    editor = VOIEditor(
        volume=volume,
        voi_mask=voi_mask,
        spacing_mm=spacing_mm,
        vessel_name=vessel_name,
        output_path=output_path,
    )
    editor.run()
    return editor.voi_mask


# ─────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Interactive VOI mask editor for PCAT pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dicom",  required=True, help="DICOM series directory")
    parser.add_argument("--voi",    required=True, help=".npy VOI mask file")
    parser.add_argument("--vessel", default="VOI",  help="Vessel name label")
    parser.add_argument("--output", required=True, help="Output .npy path")
    args = parser.parse_args()

    print(f"[voi_editor] Loading DICOM from {args.dicom} …")
    volume, meta = load_dicom_series(args.dicom)
    spacing_mm = meta["spacing_mm"]
    print(f"[voi_editor] Volume {volume.shape}  spacing {spacing_mm}")

    print(f"[voi_editor] Loading VOI mask from {args.voi} …")
    voi_mask = np.load(args.voi)

    editor = VOIEditor(
        volume=volume,
        voi_mask=voi_mask,
        spacing_mm=spacing_mm,
        vessel_name=args.vessel,
        output_path=args.output,
    )
    editor.run()


if __name__ == "__main__":
    main()
