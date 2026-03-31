"""Waveform generators for the Filters branch."""
import numpy as np
from scipy import signal as sig
from ._core import (
    BG, FG, GRID, C_INPUT, C_OUT, C_OUT2, C_OUT3, C_THRESH,
    _make_fig, _fmt_freq_hz,
)

def _wf_rc_lowpass(p):
    R, C = p["R"], p["C"]
    fc = 1 / (2 * np.pi * R * C)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    # Bode
    f = np.logspace(np.log10(max(1, fc / 100)), np.log10(fc * 100), 500)
    w = 2 * np.pi * f
    H = 1 / (1 + 1j * w * R * C)
    ax1.semilogx(f, 20 * np.log10(np.abs(H)), color=C_OUT, linewidth=2, label="|H(f)|")
    ax1.axvline(fc, color=C_THRESH, linestyle="--", linewidth=1, label=f"fc = {fc:.1f} Hz")
    ax1.axhline(-3, color=FG, linestyle=":", linewidth=0.7, alpha=0.5)
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("Bode magnitude", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Time
    f_in = p.get("f_input", fc * 3)
    t = np.linspace(0, 5 / f_in, 1000)
    vin = np.sin(2 * np.pi * f_in * t)
    # Analytical steady-state
    mag = 1 / np.sqrt(1 + (2 * np.pi * f_in * R * C) ** 2)
    phi = -np.arctan(2 * np.pi * f_in * R * C)
    vout = mag * np.sin(2 * np.pi * f_in * t + phi)
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.5, label=f"Input  {f_in:.0f} Hz")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label=f"Output (attenuated)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Time-domain  (input vs output)", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_rc_highpass(p):
    R, C = p["R"], p["C"]
    fc = 1 / (2 * np.pi * R * C)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    f = np.logspace(np.log10(max(0.01, fc / 100)), np.log10(fc * 100), 500)
    w = 2 * np.pi * f
    H = 1j * w * R * C / (1 + 1j * w * R * C)
    ax1.semilogx(f, 20 * np.log10(np.abs(H)), color=C_OUT, linewidth=2)
    ax1.axvline(fc, color=C_THRESH, linestyle="--", linewidth=1, label=f"fc = {fc:.1f} Hz")
    ax1.axhline(-3, color=FG, linestyle=":", linewidth=0.7, alpha=0.5)
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("Bode magnitude", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    f_in = p.get("f_input", fc * 0.3)
    t = np.linspace(0, 5 / max(f_in, 0.1), 1000)
    vin = np.sin(2 * np.pi * f_in * t)
    ww = 2 * np.pi * f_in
    mag = ww * R * C / np.sqrt(1 + (ww * R * C) ** 2)
    phi = np.pi / 2 - np.arctan(ww * R * C)
    vout = mag * np.sin(2 * np.pi * f_in * t + phi)
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.5, label=f"Input  {f_in:.1f} Hz")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Output (attenuated at low f)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Time-domain", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_rl_lowpass(p):
    R, L = p["R"], p["L"]
    fc = R / (2 * np.pi * L)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    f = np.logspace(np.log10(max(1, fc / 100)), np.log10(fc * 100), 500)
    w = 2 * np.pi * f
    H = R / (R + 1j * w * L)
    ax1.semilogx(f, 20 * np.log10(np.abs(H)), color=C_OUT, linewidth=2)
    ax1.axvline(fc, color=C_THRESH, linestyle="--", linewidth=1, label=f"fc = {fc:.0f} Hz")
    ax1.axhline(-3, color=FG, linestyle=":", linewidth=0.7, alpha=0.5)
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("RL Low-Pass Bode", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    f_in = p.get("f_input", fc * 2)
    t = np.linspace(0, 5 / f_in, 1000)
    vin = np.sin(2 * np.pi * f_in * t)
    ww = 2 * np.pi * f_in
    Hval = R / (R + 1j * ww * L)
    vout = np.abs(Hval) * np.sin(2 * np.pi * f_in * t + np.angle(Hval))
    ax2.plot(t * 1e6, vin, color=C_INPUT, linewidth=1.5, label="Input")
    ax2.plot(t * 1e6, vout, color=C_OUT, linewidth=2, label="Output")
    ax2.set_xlabel("Time (µs)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Time-domain", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_rl_highpass(p):
    """RL high-pass: R series from Vin, L shunt to ground, Vout at junction."""
    R, L = p["R"], p["L"]
    fc = R / (2 * np.pi * L)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    f = np.logspace(np.log10(max(1, fc / 100)), np.log10(fc * 100), 500)
    w = 2 * np.pi * f
    H = 1j * w * L / (R + 1j * w * L)
    ax1.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=C_OUT3, linewidth=2)
    ax1.axvline(fc, color=C_THRESH, linestyle="--", linewidth=1, label=f"fc = {fc:.0f} Hz")
    ax1.axhline(-3, color=FG, linestyle=":", linewidth=0.7, alpha=0.5)
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("RL High-Pass Bode", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    f_in = p.get("f_input_low", fc * 0.3)
    f_hi = p.get("f_input_high", fc * 3)
    f_min = min(f_in, f_hi)
    t = np.linspace(0, 5 / max(f_min, 1), 1000)
    vin = np.sin(2 * np.pi * f_in * t) + 0.6 * np.sin(2 * np.pi * f_hi * t)
    H1 = (1j * 2 * np.pi * f_in * L) / (R + 1j * 2 * np.pi * f_in * L)
    H2 = (1j * 2 * np.pi * f_hi * L) / (R + 1j * 2 * np.pi * f_hi * L)
    vout = np.abs(H1) * np.sin(2 * np.pi * f_in * t + np.angle(H1)) + 0.6 * np.abs(H2) * np.sin(
        2 * np.pi * f_hi * t + np.angle(H2)
    )
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.2, alpha=0.85, label="Input (low + high)")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Output — lows attenuated")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Time-domain", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_lc_highpass(p):
    """2nd-order LC high-pass: C series, L||R load to ground."""
    L, C = p["L"], p["C"]
    Rload = p.get("R", 50.0)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    f0 = 1 / (2 * np.pi * np.sqrt(L * C))
    f = np.logspace(np.log10(max(1, f0 / 50)), np.log10(f0 * 50), 600)
    w = 2 * np.pi * f
    Zc = 1 / (1j * w * C)
    Zrl = (1j * w * L * Rload) / (Rload + 1j * w * L)
    H = Zrl / (Zc + Zrl)
    ax1.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=C_OUT3, linewidth=2)
    ax1.axvline(f0, color=C_THRESH, linestyle="--", linewidth=1, label=f"f₀ ≈ {f0:.0f} Hz")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("LC High-Pass (C series, shunt L‖R)", fontsize=10, fontweight="bold")
    ax1.set_ylim(-60, 15)
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    f_lo = p.get("f_input_low", f0 * 0.2)
    f_hi = p.get("f_input_high", f0 * 2)
    t = np.linspace(0, 5 / max(f_lo, 1), 1000)
    vin = np.sin(2 * np.pi * f_lo * t) + 0.5 * np.sin(2 * np.pi * f_hi * t)

    def hp_at(fx):
        ww = 2 * np.pi * fx
        Zc = 1 / (1j * ww * C)
        Zrl = (1j * ww * L * Rload) / (Rload + 1j * ww * L)
        return Zrl / (Zc + Zrl)

    H1, H2 = hp_at(f_lo), hp_at(f_hi)
    vout = np.abs(H1) * np.sin(2 * np.pi * f_lo * t + np.angle(H1)) + 0.5 * np.abs(H2) * np.sin(
        2 * np.pi * f_hi * t + np.angle(H2)
    )
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.2, alpha=0.85, label="Mixed input")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Output")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Low-frequency content suppressed", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_passive_pi_lp(p):
    """Illustrative 3rd-order Butterworth low-pass (lumped prototype for π / T ladder design)."""
    fc = p.get("fc", 1200)
    order = int(p.get("order", 3))
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    b, a = sig.butter(order, 2 * np.pi * fc, btype="low", analog=True)
    w, h = sig.freqs(b, a, worN=np.logspace(np.log10(fc / 100), np.log10(fc * 80), 800))
    f = w / (2 * np.pi)
    ax.semilogx(f, 20 * np.log10(np.abs(h) + 1e-15), color=C_OUT, linewidth=2, label=f"Analog proto  n={order}")
    ax.axvline(fc, color=C_THRESH, linestyle="--", linewidth=1, label=f"fc ≈ {fc} Hz")
    ax.axhline(-3, color=FG, linestyle=":", linewidth=0.6, alpha=0.5)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Gain (dB)")
    ax.set_title("Higher-order LP prototype (π/T ladders realize similar roll-off)", fontsize=10, fontweight="bold")
    ax.set_ylim(-70, 5)
    ax.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_crystal_resonator(p):
    """Motional series arm: R, L, C — |Z| minimum near series resonance."""
    f0 = p["f0"]
    Q = p["Q"]
    Rm = p.get("Rm", 25.0)
    Lm = Q * Rm / (2 * np.pi * f0)
    Cm = 1 / ((2 * np.pi * f0) ** 2 * Lm)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    span = max(f0 / Q * 15, f0 * 0.002)
    f = np.linspace(max(1, f0 - span), f0 + span, 2500)
    w = 2 * np.pi * f
    Zm = Rm + 1j * w * Lm + 1 / (1j * w * Cm)
    ax1.plot(f, np.abs(Zm), color=C_OUT, linewidth=2)
    ax1.axvline(f0, color=C_THRESH, linestyle="--", linewidth=1, label=f"fs ≈ {_fmt_freq_hz(f0)}")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("|Z| (Ω)")
    ax1.set_title("Crystal motional arm — sharp series resonance", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Phasor current amplitude response (drive with 1 V through 50 Ω source – conceptual)
    Rsrc = p.get("Rsrc", 50.0)
    I = 1.0 / np.abs(Rsrc + Zm)
    ax2.plot(f, 20 * np.log10(I / np.nanmax(I) + 1e-15), color=C_OUT2, linewidth=2)
    ax2.axvline(f0, color=C_THRESH, linestyle="--", linewidth=1)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Rel. current (dB)")
    ax2.set_title("Current peaks where |Z| is minimum", fontsize=10, fontweight="bold")
    fig.tight_layout(pad=1.5)
    return fig

def _wf_lc_lowpass(p):
    L, C = p["L"], p["C"]
    Rd = p.get("R_damp", 1.0)
    f0 = 1 / (2 * np.pi * np.sqrt(L * C))
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    f = np.logspace(np.log10(max(1, f0 / 50)), np.log10(f0 * 50), 600)
    w = 2 * np.pi * f
    s = 1j * w
    H = 1 / (s ** 2 * L * C + s * Rd * C + 1)
    ax1.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=C_OUT, linewidth=2)
    ax1.axvline(f0, color=C_THRESH, linestyle="--", linewidth=1, label=f"f₀ = {f0:.0f} Hz")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("LC Low-Pass Bode (−40 dB/dec)", fontsize=10, fontweight="bold")
    ax1.set_ylim(-80, 20)
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Step response
    num = [1]
    den = [L * C, Rd * C, 1]
    sys_tf = sig.TransferFunction(num, den)
    t_step, y_step = sig.step(sys_tf, N=1000)
    ax2.plot(t_step * 1e3, y_step, color=C_OUT, linewidth=2, label="Step response")
    ax2.axhline(1.0, color=FG, linestyle=":", linewidth=0.7, alpha=0.5)
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Step response (ringing visible)", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_rlc_bandpass(p):
    R, L, C = p["R"], p["L"], p["C"]
    f0 = 1 / (2 * np.pi * np.sqrt(L * C))
    Q = (1 / R) * np.sqrt(L / C)
    BW = f0 / Q
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    f = np.logspace(np.log10(max(1, f0 / 50)), np.log10(f0 * 50), 600)
    w = 2 * np.pi * f
    s = 1j * w
    H = s * R * C / (s ** 2 * L * C + s * R * C + 1)
    ax1.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=C_OUT, linewidth=2)
    ax1.axvline(f0, color=C_THRESH, linestyle="--", linewidth=1, label=f"f₀ = {f0:.0f} Hz  Q={Q:.1f}")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("RLC Band-Pass", fontsize=10, fontweight="bold")
    ax1.set_ylim(-40, 5)
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Time: pass at f0, reject at f0*3
    t = np.linspace(0, 10 / f0, 1000)
    vin = np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * 3 * f0 * t)
    Hf0 = 1j * 2 * np.pi * f0 * R * C / ((1j * 2 * np.pi * f0) ** 2 * L * C + 1j * 2 * np.pi * f0 * R * C + 1)
    Hf3 = 1j * 2 * np.pi * 3 * f0 * R * C / ((1j * 2 * np.pi * 3 * f0) ** 2 * L * C + 1j * 2 * np.pi * 3 * f0 * R * C + 1)
    vout = np.abs(Hf0) * np.sin(2 * np.pi * f0 * t + np.angle(Hf0)) + 0.5 * np.abs(Hf3) * np.sin(2 * np.pi * 3 * f0 * t + np.angle(Hf3))
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1, alpha=0.8, label="Input (f₀ + 3·f₀)")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Output (f₀ passed)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Band-pass effect on mixed signal", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_notch(p):
    f0 = p["f0"]
    Q = p["Q"]
    w0 = 2 * np.pi * f0
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    f_lo = max(0.1, f0 / 100)
    f_hi = f0 * 80
    f = np.logspace(np.log10(f_lo), np.log10(f_hi), 600)
    w = 2 * np.pi * f
    s = 1j * w
    H = (s ** 2 + w0 ** 2) / (s ** 2 + (w0 / Q) * s + w0 ** 2)
    ax1.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=C_OUT, linewidth=2)
    ax1.axvline(
        f0,
        color=C_THRESH,
        linestyle="--",
        linewidth=1,
        label=f"Notch at {_fmt_freq_hz(f0)}",
    )
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title(f"Notch Filter  (Q={Q})", fontsize=10, fontweight="bold")
    ax1.set_ylim(-50, 5)
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Time window: a few cycles at f₀ (RF notches need µs-scale windows, not fixed 100 ms).
    n_cycles = float(p.get("n_cycles", 6))
    t_end = min(n_cycles / f0, 0.2)
    n_pts = int(np.clip(t_end * f0 * 32, 600, 6000))
    t = np.linspace(0, t_end, n_pts)
    vin = np.sin(2 * np.pi * f0 * t) + 0.5 * np.sin(2 * np.pi * f0 * 5 * t)
    Hf5_s = 1j * 2 * np.pi * 5 * f0
    Hf5 = (Hf5_s ** 2 + w0 ** 2) / (Hf5_s ** 2 + (w0 / Q) * Hf5_s + w0 ** 2)
    vout = 0.0 + 0.5 * np.abs(Hf5) * np.sin(2 * np.pi * 5 * f0 * t + np.angle(Hf5))
    f0s = _fmt_freq_hz(f0)
    f5s = _fmt_freq_hz(5 * f0)
    if t_end < 2e-5:
        t_plot, tunits = t * 1e6, "µs"
    elif t_end < 0.5:
        t_plot, tunits = t * 1e3, "ms"
    else:
        t_plot, tunits = t, "s"
    ax2.plot(t_plot, vin, color=C_INPUT, linewidth=1, alpha=0.8, label=f"Input ({f0s} + {f5s})")
    ax2.plot(t_plot, vout, color=C_OUT, linewidth=2, label=f"Output (notch at {f0s})")
    ax2.set_xlabel(f"Time ({tunits})")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Notch removes the unwanted tone", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_active_lp2(p):
    f0, Q, gain = p["f0"], p["Q"], p.get("gain", 1)
    w0 = 2 * np.pi * f0
    K = abs(gain)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    f = np.logspace(np.log10(max(1, f0 / 100)), np.log10(f0 * 50), 600)
    w = 2 * np.pi * f
    s = 1j * w
    H = K * w0 ** 2 / (s ** 2 + (w0 / Q) * s + w0 ** 2)
    ax1.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=C_OUT, linewidth=2)
    ax1.axvline(f0, color=C_THRESH, linestyle="--", linewidth=1, label=f"f₀={f0}Hz  Q={Q:.2f}")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("2nd-Order Active Low-Pass", fontsize=10, fontweight="bold")
    ax1.set_ylim(-60, 20)
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    f_in = p.get("f_input", f0 * 3)
    t = np.linspace(0, 5 / f0, 1000)
    vin = np.sin(2 * np.pi * f_in * t) + np.sin(2 * np.pi * f0 * 0.3 * t)
    # Filter output for both components
    s1 = 1j * 2 * np.pi * f_in
    H1 = K * w0 ** 2 / (s1 ** 2 + (w0 / Q) * s1 + w0 ** 2)
    s2 = 1j * 2 * np.pi * f0 * 0.3
    H2 = K * w0 ** 2 / (s2 ** 2 + (w0 / Q) * s2 + w0 ** 2)
    vout = np.abs(H1) * np.sin(2 * np.pi * f_in * t + np.angle(H1)) + np.abs(H2) * np.sin(2 * np.pi * f0 * 0.3 * t + np.angle(H2))
    sign_label = "inverted" if gain < 0 else ""
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1, alpha=0.8, label="Input (low + high freq)")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label=f"Output {sign_label}")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("High-freq component removed", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_active_hp2(p):
    """2nd-order high-pass: H = K·s² / (s² + (ω₀/Q)s + ω₀²)."""
    f0, Q = p["f0"], p["Q"]
    K = abs(p.get("gain", 1))
    w0 = 2 * np.pi * f0
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    f = np.logspace(np.log10(max(1, f0 / 100)), np.log10(f0 * 50), 600)
    w = 2 * np.pi * f
    s = 1j * w
    H = K * s ** 2 / (s ** 2 + (w0 / Q) * s + w0 ** 2)
    ax1.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=C_OUT3, linewidth=2)
    ax1.axvline(f0, color=C_THRESH, linestyle="--", linewidth=1, label=f"f₀={f0}Hz  Q={Q:.2f}")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("2nd-Order Active High-Pass", fontsize=10, fontweight="bold")
    ax1.set_ylim(-60, 20)
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    f_lo = p.get("f_input_low", f0 * 0.25)
    f_hi = p.get("f_input_high", f0 * 3)
    f_min = min(f_lo, f_hi)
    t = np.linspace(0, 5 / max(f_min, 1), 1200)
    vin = np.sin(2 * np.pi * f_lo * t) + 0.6 * np.sin(2 * np.pi * f_hi * t)

    def H_at(ff):
        ss = 1j * 2 * np.pi * ff
        return K * ss ** 2 / (ss ** 2 + (w0 / Q) * ss + w0 ** 2)

    H1, H2 = H_at(f_lo), H_at(f_hi)
    vout = np.abs(H1) * np.sin(2 * np.pi * f_lo * t + np.angle(H1)) + np.abs(H2) * 0.6 * np.sin(2 * np.pi * f_hi * t + np.angle(H2))
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1, alpha=0.8, label="Input (low + high)")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Low freq attenuated")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Low-frequency component attenuated", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_active_bp2(p):
    """2nd-order band-pass: H = K·(ω₀/Q)s / (s² + (ω₀/Q)s + ω₀²)."""
    f0, Q = p["f0"], p["Q"]
    K = p.get("gain", 1)
    w0 = 2 * np.pi * f0
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    f = np.logspace(np.log10(max(1, f0 / 100)), np.log10(f0 * 100), 600)
    w = 2 * np.pi * f
    s = 1j * w
    H = K * (w0 / Q) * s / (s ** 2 + (w0 / Q) * s + w0 ** 2)
    ax1.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=C_OUT2, linewidth=2)
    ax1.axvline(f0, color=C_THRESH, linestyle="--", linewidth=1, label=f"f₀={f0}Hz  Q={Q:.2f}")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("2nd-Order Active Band-Pass", fontsize=10, fontweight="bold")
    ax1.set_ylim(-50, 15)
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    f_in = p.get("f_input", f0)
    f_off = p.get("f_input_off", f0 * 0.3)
    t = np.linspace(0, 4 / f0, 1200)
    vin = np.sin(2 * np.pi * f_in * t) + 0.5 * np.sin(2 * np.pi * f_off * t)

    def H_at(ff):
        ss = 1j * 2 * np.pi * ff
        return K * (w0 / Q) * ss / (ss ** 2 + (w0 / Q) * ss + w0 ** 2)

    H1, H2 = H_at(f_in), H_at(f_off)
    vout = np.abs(H1) * np.sin(2 * np.pi * f_in * t + np.angle(H1)) + np.abs(H2) * 0.5 * np.sin(2 * np.pi * f_off * t + np.angle(H2))
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1, alpha=0.8, label=f"Input @ {f0}Hz + off-tune")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Narrowband output")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Band-pass emphasizes center frequency", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_state_variable(p):
    f0, Q = p["f0"], p["Q"]
    w0 = 2 * np.pi * f0
    fig, axes = _make_fig(1, 3, (12, 3.5))
    f = np.logspace(np.log10(max(1, f0 / 100)), np.log10(f0 * 100), 600)
    w = 2 * np.pi * f
    s = 1j * w

    H_lp = w0 ** 2 / (s ** 2 + (w0 / Q) * s + w0 ** 2)
    H_bp = (w0 / Q) * s / (s ** 2 + (w0 / Q) * s + w0 ** 2)
    H_hp = s ** 2 / (s ** 2 + (w0 / Q) * s + w0 ** 2)

    for ax, H, label, col in zip(axes, [H_lp, H_bp, H_hp],
                                  ["Low-Pass", "Band-Pass", "High-Pass"],
                                  [C_OUT, C_OUT2, C_OUT3]):
        ax.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=col, linewidth=2)
        ax.axvline(f0, color=C_THRESH, linestyle="--", linewidth=0.8)
        ax.set_xlabel("Freq (Hz)", fontsize=8)
        ax.set_ylabel("dB", fontsize=8)
        ax.set_title(label, fontsize=9, fontweight="bold")
        ax.set_ylim(-50, 20)
    fig.suptitle(f"State-Variable: 3 simultaneous outputs  (f₀={f0}Hz, Q={Q})", color=FG, fontsize=10, fontweight="bold")
    fig.tight_layout(pad=1.2, rect=[0, 0, 1, 0.92])
    return fig

def _wf_allpass(p):
    R, C = p["R"], p["C"]
    fc = 1 / (2 * np.pi * R * C)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    f = np.logspace(np.log10(max(0.1, fc / 100)), np.log10(fc * 100), 600)
    w = 2 * np.pi * f
    s = 1j * w
    H = (1 - s * R * C) / (1 + s * R * C)
    ax1.semilogx(f, 20 * np.log10(np.abs(H)), color=C_OUT, linewidth=2, label="|H| ≈ 0 dB")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("All-Pass: magnitude is FLAT", fontsize=10, fontweight="bold")
    ax1.set_ylim(-3, 3)
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    phase = np.angle(H, deg=True)
    ax2.semilogx(f, phase, color=C_OUT2, linewidth=2)
    ax2.axvline(fc, color=C_THRESH, linestyle="--", linewidth=1, label=f"f₀ = {fc:.0f} Hz")
    ax2.axhline(-90, color=FG, linestyle=":", linewidth=0.7, alpha=0.5)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Phase (°)")
    ax2.set_title("Phase shifts 0° → −180°", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_bode_comparison(p):
    family = p["family"]
    orders = p.get("orders", [2, 4])
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    f = np.logspace(-1, 2, 600)  # normalized frequency
    w = 2 * np.pi * f
    colors = [C_OUT, C_OUT2, C_OUT3, C_INPUT]
    for i, n in enumerate(orders):
        if family == "butterworth":
            Hmag = 1 / np.sqrt(1 + f ** (2 * n))
            label = f"Butterworth n={n}"
        elif family == "chebyshev":
            eps = np.sqrt(10 ** (1 / 10) - 1)  # 1 dB ripple
            from numpy.polynomial.chebyshev import chebval
            Tn = np.abs(chebval(f, [0] * n + [1]))
            Hmag = 1 / np.sqrt(1 + eps ** 2 * Tn ** 2)
            label = f"Chebyshev 1dB n={n}"
        elif family == "bessel":
            # approximate: use scipy
            b, a = sig.bessel(n, 1, btype='low', analog=True, norm='mag')
            _, Hval = sig.freqs(b, a, worN=w)
            Hmag = np.abs(Hval)
            label = f"Bessel n={n}"
        else:
            Hmag = 1 / np.sqrt(1 + f ** (2 * n))
            label = f"n={n}"
        ax.semilogx(f, 20 * np.log10(Hmag + 1e-15), color=colors[i % len(colors)],
                     linewidth=2, label=label)
    ax.axhline(-3, color=FG, linestyle=":", linewidth=0.7, alpha=0.5, label="−3 dB")
    ax.axvline(1, color=C_THRESH, linestyle="--", linewidth=0.8, alpha=0.5, label="fc (normalized)")
    ax.set_xlabel("Normalized frequency  (f / fc)")
    ax.set_ylabel("Gain (dB)")
    ax.set_title(f"{family.title()} response comparison", fontsize=11, fontweight="bold")
    ax.set_ylim(-60, 5)
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_rectifier_smoothing(p):
    C = p["C"]
    I = p["I_load"]
    f_line = p["f_line"]
    f_rip = 2 * f_line  # full-wave
    T_rip = 1 / f_rip
    Vpk = 15
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    t = np.linspace(0, 4 / f_line, 2000)
    v_rect = np.abs(Vpk * np.sin(2 * np.pi * f_line * t))
    ax1.plot(t * 1e3, v_rect, color=C_INPUT, linewidth=1, label="Full-wave rectified")

    # Simulate smoothing
    v_cap = np.zeros_like(t)
    v_cap[0] = Vpk
    dt = t[1] - t[0]
    for i in range(1, len(t)):
        v_discharge = v_cap[i - 1] - (I / C) * dt
        v_cap[i] = max(v_discharge, v_rect[i])
    ripple = v_cap.max() - v_cap.min()
    ax1.plot(t * 1e3, v_cap, color=C_OUT, linewidth=2, label=f"Smoothed (C={C*1e6:.0f}µF)")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage (V)")
    ax1.set_title(f"Ripple ≈ {ripple:.2f} V pp", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Compare different C values
    for Cx, col, ls in [(100e-6, C_OUT3, "-"), (470e-6, C_OUT2, "--"), (2200e-6, C_OUT, "-.")]:
        vc = np.zeros_like(t)
        vc[0] = Vpk
        for i in range(1, len(t)):
            vc[i] = max(vc[i - 1] - (I / Cx) * dt, v_rect[i])
        ax2.plot(t * 1e3, vc, color=col, linewidth=1.5, linestyle=ls, label=f"C={Cx*1e6:.0f}µF")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage (V)")
    ax2.set_title("Effect of capacitor size", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_impedance_vs_freq(p):
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    f = np.logspace(3, 9, 1000)
    w = 2 * np.pi * f
    colors = [C_OUT, C_OUT2, C_OUT3]
    caps = p["caps"]
    ESRs = p["ESR"]
    ESLs = p["ESL"]
    Z_total = np.full_like(f, 1e6)
    for i, (Cv, esr, esl) in enumerate(zip(caps, ESRs, ESLs)):
        Xc = 1 / (w * Cv)
        Xl = w * esl
        Z = np.sqrt(esr ** 2 + (Xc - Xl) ** 2)
        ax.loglog(f, Z, color=colors[i % 3], linewidth=1.5, linestyle="--",
                  label=f"C={Cv*1e6:.1f}µF  ESR={esr*1e3:.0f}mΩ")
        Z_total = 1 / (1 / Z_total + 1 / Z)
    ax.loglog(f, Z_total, color=C_THRESH, linewidth=2.5, label="Combined (parallel)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Impedance (Ω)")
    ax.set_title("Decoupling capacitor impedance", fontsize=11, fontweight="bold")
    ax.set_ylim(1e-3, 10)
    ax.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_emi_concept(p):
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    # Conceptual: show attenuation of a 2-stage EMI filter
    f = np.logspace(4, 8, 600)
    w = 2 * np.pi * f
    # Stage 1: CM choke 10mH + Y-cap 4.7nF
    Lcm, Cy = 10e-3, 4.7e-9
    H_cm = 1 / (1 + 1j * w * Lcm / (1 / (1j * w * Cy)))
    # Simplified: CM attenuation
    Zcm = 1j * w * Lcm
    Zy = 1 / (1j * w * Cy)
    H_cm = Zy / (Zcm + Zy)
    # Stage 2: DM LC
    Ldm, Cx = 100e-6, 100e-9
    H_dm = 1 / (1 - w ** 2 * Ldm * Cx + 1j * w * 0.5 * Cx)
    ax.semilogx(f / 1e6, 20 * np.log10(np.abs(H_cm) + 1e-15), color=C_OUT, linewidth=2,
                label="CM filter (choke+Y-cap)")
    ax.semilogx(f / 1e6, 20 * np.log10(np.abs(H_dm) + 1e-15), color=C_OUT2, linewidth=2,
                label="DM filter (L+X-cap)")
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Insertion Loss (dB)")
    ax.set_title("EMI Filter Attenuation (Conceptual)", fontsize=11, fontweight="bold")
    ax.set_ylim(-80, 5)
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig


FILTER_GENERATORS = {
    "rc_lowpass": _wf_rc_lowpass,
    "rc_highpass": _wf_rc_highpass,
    "rl_lowpass": _wf_rl_lowpass,
    "rl_highpass": _wf_rl_highpass,
    "lc_highpass": _wf_lc_highpass,
    "lc_lowpass": _wf_lc_lowpass,
    "passive_pi_lp": _wf_passive_pi_lp,
    "crystal_resonator": _wf_crystal_resonator,
    "rlc_bandpass": _wf_rlc_bandpass,
    "notch": _wf_notch,
    "active_lowpass_2nd": _wf_active_lp2,
    "active_highpass_2nd": _wf_active_hp2,
    "active_bandpass_2nd": _wf_active_bp2,
    "state_variable": _wf_state_variable,
    "allpass": _wf_allpass,
    "bode_comparison": _wf_bode_comparison,
    "rectifier_smoothing": _wf_rectifier_smoothing,
    "impedance_vs_freq": _wf_impedance_vs_freq,
    "emi_filter_concept": _wf_emi_concept,
}
