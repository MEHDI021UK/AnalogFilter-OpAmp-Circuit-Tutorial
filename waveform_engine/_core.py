"""Shared matplotlib setup, palette, and figure helpers."""
"""
Waveform engine — generates matplotlib figures for every topic.
Returns a matplotlib Figure object that the UI will embed.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # non-interactive backend; figure embedded in tk canvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from scipy import signal as sig

# ── colour palette ──────────────────────────────────────────────────
BG      = "#1a1b26"
FG      = "#c0caf5"
GRID    = "#292e42"
C_INPUT = "#7aa2f7"   # soft blue
C_OUT   = "#9ece6a"   # green
C_OUT2  = "#ff9e64"   # orange
C_OUT3  = "#bb9af7"   # purple
C_THRESH = "#f7768e"  # red

def _make_fig(rows=1, cols=1, figsize=(9, 4)):
    fig, axes = plt.subplots(rows, cols, figsize=figsize, facecolor=BG)
    if rows * cols == 1:
        axes = [axes]
    elif rows > 1 and cols > 1:
        axes = axes.flatten()
    for ax in (axes if isinstance(axes, (list, np.ndarray)) else [axes]):
        ax.set_facecolor(BG)
        ax.tick_params(colors=FG, labelsize=8)
        ax.xaxis.label.set_color(FG)
        ax.yaxis.label.set_color(FG)
        ax.title.set_color(FG)
        for spine in ax.spines.values():
            spine.set_color(GRID)
        ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)
    return fig, axes

def _fmt_freq_hz(f0: float) -> str:
    """Human-readable frequency for axis labels and legends."""
    if f0 >= 1e6:
        return f"{f0 / 1e6:.4g} MHz"
    if f0 >= 1e3:
        return f"{f0 / 1e3:.4g} kHz"
    return f"{f0:.4g} Hz"

