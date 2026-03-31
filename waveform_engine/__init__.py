"""Waveform engine — figures for every topic (Filters + Op-Amp branches)."""
from matplotlib.figure import Figure
from ._core import BG, FG, _make_fig
from .filters import FILTER_GENERATORS
from .op_amp import OPAMP_GENERATORS

_GENERATORS = {**FILTER_GENERATORS, **OPAMP_GENERATORS}

__all__ = ["generate_waveform", "_GENERATORS"]

def generate_waveform(waveform_spec: dict) -> Figure:
    """Given a waveform dict {'kind': ..., 'params': {...}}, return a Figure."""
    kind = waveform_spec.get("kind", "")
    params = waveform_spec.get("params", {})
    gen = _GENERATORS.get(kind)
    if gen is None:
        fig, ax = _make_fig(1, 1, (6, 3))
        ax[0].text(0.5, 0.5, f"No waveform generator for '{kind}'",
                   ha="center", va="center", color=FG, fontsize=12,
                   transform=ax[0].transAxes)
        return fig
    return gen(params)
