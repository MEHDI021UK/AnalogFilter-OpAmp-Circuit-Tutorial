"""Waveform generators for the Op-Amp Circuits branch."""
import numpy as np
from scipy import signal as sig
from ._core import (
    BG, FG, GRID, C_INPUT, C_OUT, C_OUT2, C_OUT3, C_THRESH,
    _make_fig, _fmt_freq_hz,
)

def _wf_follower(p):
    f = p["f_input"]
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 3 / f, 500)
    vin = 2 * np.sin(2 * np.pi * f * t) + 0.5
    t_end = float(t[-1])
    if t_end < 5e-8:
        t_plot, tunits = t * 1e9, "ns"
    elif t_end < 5e-5:
        t_plot, tunits = t * 1e6, "µs"
    elif t_end < 0.5:
        t_plot, tunits = t * 1e3, "ms"
    else:
        t_plot, tunits = t, "s"
    ax.plot(t_plot, vin, color=C_INPUT, linewidth=2, label="Input", linestyle="--")
    ax.plot(t_plot, vin, color=C_OUT, linewidth=1.5, label="Output (identical)")
    ax.set_xlabel(f"Time ({tunits})")
    ax.set_ylabel("Voltage")
    ax.set_title("Voltage Follower — output = input", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_discrete_follower_rf(p):
    """BJT/MOS follower: ~unity AC gain, DC offset (Vbe/Vgs), Zo ~ 1/gm — not an ideal op-amp buffer."""
    f = p["f_input"]
    vbe = p.get("Vbe", 0.68)
    ac_gain = p.get("ac_gain", 0.97)
    v_bias = p.get("v_bias", 2.2)
    v_ac_pk = p.get("v_ac_pk", 0.12)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    t = np.linspace(0, 3 / f, 600)
    vin_ac = v_ac_pk * np.sin(2 * np.pi * f * t)
    v_base = v_bias + vin_ac
    v_emit = (v_bias - vbe) + ac_gain * vin_ac
    t_end = float(t[-1])
    if t_end < 5e-8:
        t_plot, tunits = t * 1e9, "ns"
    elif t_end < 5e-5:
        t_plot, tunits = t * 1e6, "µs"
    elif t_end < 0.5:
        t_plot, tunits = t * 1e3, "ms"
    else:
        t_plot, tunits = t, "s"
    ax1.plot(t_plot, v_base, color=C_INPUT, linewidth=1.8, label="Base (or gate) drive")
    ax1.plot(t_plot, v_emit, color=C_OUT, linewidth=1.8, label="Emitter (or source) output")
    ax1.set_xlabel(f"Time ({tunits})")
    ax1.set_ylabel("Voltage")
    ax1.set_title(
        f"Discrete follower: DC shift ≈ {vbe:.2f} V, AC gain ≈ {ac_gain}",
        fontsize=10,
        fontweight="bold",
    )
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Zo hint: lower gm → higher Re_out (conceptual)
    gm_sweep = np.linspace(0.02, 0.25, 80)
    rout = 1.0 / gm_sweep
    ax2.semilogy(gm_sweep * 1000, rout, color=C_OUT2, linewidth=2)
    ax2.set_xlabel("g_m (mS, conceptual)")
    ax2.set_ylabel("R_out ≈ 1/g_m (Ω)")
    ax2.set_title("More bias current → higher g_m → lower output Z", fontsize=10, fontweight="bold")
    fig.tight_layout(pad=1.5)
    return fig

def _wf_non_inv_amp(p):
    gain = p["gain"]
    f = p["f_input"]
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 3 / f, 500)
    vin = np.sin(2 * np.pi * f * t)
    vout = gain * vin
    ax.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.5, label="Input")
    ax.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label=f"Output  (×{gain})")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title(f"Non-Inverting Amplifier  Av = {gain}", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_inv_amp(p):
    gain = p["gain"]
    f = p["f_input"]
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 3 / f, 500)
    vin = np.sin(2 * np.pi * f * t)
    vout = gain * vin
    ax.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.5, label="Input")
    ax.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label=f"Output  (×{gain})")
    ax.axhline(0, color=FG, linewidth=0.5, alpha=0.3)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title(f"Inverting Amplifier  Av = {gain}", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_summing_amp(p):
    """Inverting summing amplifier: Vout = −Rf·Σ(Vk/Rk)."""
    Rf = float(p.get("Rf", 10e3))
    R1 = float(p.get("R1", 10e3))
    R2 = float(p.get("R2", 10e3))
    R3 = float(p.get("R3", 20e3))
    f1 = float(p.get("f1", 350))
    f2 = float(p.get("f2", 900))
    f3 = float(p.get("f3", 350))
    v1p = float(p.get("v1_pk", 0.18))
    v2p = float(p.get("v2_pk", 0.12))
    v3p = float(p.get("v3_pk", 0.07))
    f_min = min(f1, f2, f3)
    t = np.linspace(0, 4 / max(f_min, 1), 1400)
    v1 = v1p * np.sin(2 * np.pi * f1 * t)
    v2 = v2p * np.sin(2 * np.pi * f2 * t + 0.7)
    v3 = v3p * np.sin(2 * np.pi * f3 * t + 1.4)
    vout = -Rf * (v1 / R1 + v2 / R2 + v3 / R3)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(t * 1e3, v1, color=C_INPUT, linewidth=1.2, alpha=0.85, label="V1")
    ax1.plot(t * 1e3, v2, color=C_OUT2, linewidth=1.2, alpha=0.85, label="V2")
    ax1.plot(t * 1e3, v3, color=C_THRESH, linewidth=1.2, alpha=0.85, label="V3")
    ax1.axhline(0, color=FG, linewidth=0.5, alpha=0.25)
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage")
    ax1.set_title("Multiple inputs → single virtual-ground node", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Vout (inverted sum)")
    ax2.axhline(0, color=FG, linewidth=0.5, alpha=0.25)
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title(
        f"Vout = −Rf·(V1/R1 + V2/R2 + V3/R3)   (Rf={Rf/1e3:.0f} kΩ)",
        fontsize=10,
        fontweight="bold",
    )
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_diff_amp(p):
    gain = p["gain"]
    f = p["f_input"]
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 3 / f, 500)
    common = 2.5
    v1 = common + 0.5 * np.sin(2 * np.pi * f * t)
    v2 = common + 0.5 * np.sin(2 * np.pi * f * t + 0.3) + 0.3 * np.sin(2 * np.pi * 5 * f * t)
    vout = gain * (v2 - v1)
    ax.plot(t * 1e3, v1, color=C_INPUT, linewidth=1, alpha=0.7, label="V1")
    ax.plot(t * 1e3, v2, color=C_OUT2, linewidth=1, alpha=0.7, label="V2")
    ax.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label=f"Output = {gain}×(V2−V1)")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title("Differential Amplifier — common mode rejected", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_instrumentation_amp(p):
    """INA: buffered inputs — large common-mode swing, output only from differential component."""
    G = p.get("G", p.get("gain", 10))
    f_sig = p.get("f_input", 400)
    f_cm = p.get("f_common", 35)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    t = np.linspace(0, 3 / f_sig, 1200)
    Vcm = 2.5 + 0.4 * np.sin(2 * np.pi * f_cm * t)
    v_diff = 0.06 * np.sin(2 * np.pi * f_sig * t)
    v_in_p = Vcm + v_diff / 2
    v_in_n = Vcm - v_diff / 2
    vout = G * v_diff
    ax1.plot(t * 1e3, v_in_p, color=C_INPUT, linewidth=1.2, alpha=0.85, label="VIN+")
    ax1.plot(t * 1e3, v_in_n, color=C_OUT2, linewidth=1.2, alpha=0.85, label="VIN−")
    ax1.plot(t * 1e3, Vcm, color=C_THRESH, linewidth=1, linestyle="--", alpha=0.7, label="Common-mode")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage")
    ax1.set_title("Inputs: matched CM, small differential", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    ax2.plot(t * 1e3, v_diff, color=C_INPUT, linewidth=1.2, alpha=0.8, label="VIN+ − VIN−")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label=f"Vout = G × diff  (G={G})")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("INA output follows differential only", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_howland_concept(p):
    """Voltage-controlled current into load (conceptual Howland behaviour)."""
    Rs = p.get("R_sense", 1000.0)
    f = p.get("f_input", 400)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    t = np.linspace(0, 3 / f, 800)
    v_ctl = 0.25 * np.sin(2 * np.pi * f * t)
    i_load = v_ctl / Rs
    ax1.plot(t * 1e3, v_ctl * 1000, color=C_INPUT, linewidth=2, label="Control voltage (mV)")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("mV")
    ax1.set_title("Howland: program current via voltage", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    v_load = 1.2 * np.sin(2 * np.pi * (f * 0.37) * t)
    ax2.plot(t * 1e3, i_load * 1e3, color=C_OUT, linewidth=2, label=f"I_load ≈ Vctl / {Rs:.0f} Ω")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("I (mA)")
    ax2.set_title("Ideal source: I tracks Vctl while V_load swings", fontsize=10, fontweight="bold")
    ax2.legend(loc="upper left", fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    ax2b = ax2.twinx()
    ax2b.plot(t * 1e3, v_load, color=C_OUT2, linewidth=1.2, alpha=0.75, linestyle=":", label="V_load")
    ax2b.set_ylabel("V_load (V)", color=C_OUT2)
    ax2b.tick_params(axis="y", colors=C_OUT2, labelsize=8)
    for spine in ax2b.spines.values():
        spine.set_color(GRID)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_pga_concept(p):
    """Stepped gain vs time (discrete PGA codes)."""
    f = p.get("f_input", 800)
    gains = p.get("gains", [1, 4, 16, 4, 1])
    duration_ms = float(p.get("segment_ms", 0.75))
    nsp = int(p.get("samples_per_step", 320))
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t_segs = []
    g_segs = []
    for i, g in enumerate(gains):
        dt = duration_ms / 1000.0
        tt = np.linspace(0, dt, nsp, endpoint=False) + i * dt
        t_segs.append(tt)
        g_segs.append(np.full(nsp, g))
    t = np.concatenate(t_segs)
    g_inst = np.concatenate(g_segs)
    vin = 0.08 * np.sin(2 * np.pi * f * t)
    vout = g_inst * vin
    ax.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.2, alpha=0.85, label="Input (fixed amplitude)")
    ax.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Output (switched gain)")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title(f"PGA: discrete gains {gains}", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_vga_concept(p):
    """Continuous gain vs control (linear-in-dB style envelope)."""
    f = p.get("f_input", 2000)
    G0 = p.get("G0", 0.5)
    alpha = p.get("alpha", 2.0)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    t = np.linspace(0, 4 / f, 1600)
    # Slow gain control compared to RF/mid band carrier
    v_ctl = np.linspace(0, 1, len(t))
    gain_env = G0 * np.exp(alpha * (v_ctl - 0.5))
    vin = 0.12 * np.sin(2 * np.pi * f * t)
    vout = gain_env * vin
    ax1.plot(t * 1e3, v_ctl, color=C_THRESH, linewidth=2, label="V_control")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("V")
    ax1.set_title("Gain control voltage (slow)", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1, alpha=0.65, label="Input RF")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Output (envelope ∝ exp(αVctl))")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("VGA: amplitude follows continuous gain law", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_chopper_concept(p):
    """DC input + chopper ripple at modulation frequency (conceptual)."""
    f_in = p.get("f_input", 30)
    f_chop = p.get("f_chop", 5000)
    Av = p.get("Av", 100)
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 3 / f_in, 4000)
    v_sig = 0.002 * np.sin(2 * np.pi * f_in * t) + 0.015
    ripple = p.get("ripple_frac", 0.015) / Av
    v_chop = ripple * Av * np.sin(2 * np.pi * f_chop * t)
    vout = Av * v_sig + v_chop
    ax.plot(t * 1e3, v_sig * 1000, color=C_INPUT, linewidth=1.2, label="Input (mV, slow)")
    ax.plot(t * 1e3, vout, color=C_OUT, linewidth=1.2, alpha=0.9, label="Output (amplified + chop ripple)")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title(f"Chopper / autozero: low offset + ripple at f_chop ≈ {f_chop/1000:.1f} kHz", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_integrator(p):
    R, C = p["R"], p["C"]
    f = p["f_input"]
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    # Square wave → triangle (integration)
    t = np.linspace(0, 3 / f, 1000)
    vin_sq = np.sign(np.sin(2 * np.pi * f * t))
    dt = t[1] - t[0]
    vout = np.zeros_like(t)
    for i in range(1, len(t)):
        vout[i] = vout[i - 1] - (1 / (R * C)) * vin_sq[i] * dt
    vout -= np.mean(vout)
    ax1.plot(t * 1e3, vin_sq, color=C_INPUT, linewidth=1.5, label="Square wave input")
    ax1.plot(t * 1e3, vout / max(abs(vout)) * 0.8, color=C_OUT, linewidth=2, label="Triangle output (integrated)")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage (norm)")
    ax1.set_title("Square → Triangle", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Sine → -cosine (−90° shifted)
    vin_sin = np.sin(2 * np.pi * f * t)
    w = 2 * np.pi * f
    mag = 1 / (w * R * C)
    vout_sin = mag * (-np.cos(2 * np.pi * f * t))
    vout_sin /= max(abs(vout_sin))
    ax2.plot(t * 1e3, vin_sin, color=C_INPUT, linewidth=1.5, label="Sine input")
    ax2.plot(t * 1e3, vout_sin, color=C_OUT, linewidth=2, label="−Cosine output (−90°)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage (norm)")
    ax2.set_title("Sine → inverted Cosine", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_differentiator(p):
    R, C = p["R"], p["C"]
    f = p["f_input"]
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))

    t = np.linspace(0, 3 / f, 1000)
    # Triangle → square (differentiation)
    tri = 2 * np.abs(2 * (f * t % 1) - 1) - 1
    dt = t[1] - t[0]
    vout = np.zeros_like(t)
    for i in range(1, len(t)):
        vout[i] = -R * C * (tri[i] - tri[i - 1]) / dt
    vout = np.clip(vout, -2, 2)
    ax1.plot(t * 1e3, tri, color=C_INPUT, linewidth=1.5, label="Triangle input")
    ax1.plot(t * 1e3, vout / max(abs(vout) + 1e-9), color=C_OUT, linewidth=2, label="Square output")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage (norm)")
    ax1.set_title("Triangle → Square (differentiated)", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Sine → cosine
    vin = np.sin(2 * np.pi * f * t)
    w = 2 * np.pi * f
    vout2 = -R * C * w * np.cos(2 * np.pi * f * t)
    vout2 /= max(abs(vout2))
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.5, label="Sine input")
    ax2.plot(t * 1e3, vout2, color=C_OUT, linewidth=2, label="−Cosine output (+90°)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage (norm)")
    ax2.set_title("Sine → inverted Cosine (+90°)", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_comparator(p):
    Vth = p["V_threshold"]
    f = p["f_input"]
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 3 / f, 1000)
    vin = 2 * np.sin(2 * np.pi * f * t)
    vout = np.where(vin > Vth, 5.0, 0.0)
    ax.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.5, label="Input (sine)")
    ax.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Output (digital)")
    ax.axhline(Vth, color=C_THRESH, linestyle="--", linewidth=1.5, label=f"Threshold = {Vth}V")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title("Comparator — sine to square wave", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    ax.set_ylim(-3, 6)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_schmitt(p):
    VTH, VTL = p["V_TH"], p["V_TL"]
    f = p["f_input"]
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 4 / f, 1000)
    vin = 2 * np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 13 * f * t)
    vout = np.zeros_like(t)
    state = False
    for i in range(len(t)):
        if vin[i] > VTH:
            state = True
        elif vin[i] < VTL:
            state = False
        vout[i] = 5.0 if state else 0.0
    ax.plot(t * 1e3, vin, color=C_INPUT, linewidth=1, alpha=0.8, label="Noisy input")
    ax.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Clean output")
    ax.axhline(VTH, color=C_THRESH, linestyle="--", linewidth=1, alpha=0.7, label=f"V_TH={VTH}V")
    ax.axhline(VTL, color=C_OUT2, linestyle="--", linewidth=1, alpha=0.7, label=f"V_TL={VTL}V")
    ax.fill_between(t * 1e3, VTL, VTH, color=C_THRESH, alpha=0.08)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title("Schmitt Trigger — hysteresis cleans noisy signal", fontsize=11, fontweight="bold")
    ax.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_peak_detector(p):
    f = p["f_input"]
    decay = p.get("decay_tau", 0.02)
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 5 / f, 1000)
    dt = t[1] - t[0]
    vin = (1 + 0.5 * np.sin(2 * np.pi * f * 0.1 * t)) * np.sin(2 * np.pi * f * t)
    vpeak = np.zeros_like(t)
    vpeak[0] = 0
    for i in range(1, len(t)):
        decayed = vpeak[i - 1] * np.exp(-dt / decay)
        vpeak[i] = max(vin[i], decayed)
    ax.plot(t * 1e3, vin, color=C_INPUT, linewidth=1, alpha=0.7, label="Input signal")
    ax.plot(t * 1e3, vpeak, color=C_OUT, linewidth=2.5, label="Peak detector output")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title("Peak Detector — captures envelope", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_precision_rectifier(p):
    f = p["f_input"]
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    t = np.linspace(0, 4 / f, 1000)
    vin = np.sin(2 * np.pi * f * t)

    # Half-wave
    vout_hw = np.maximum(vin, 0)
    ax1.plot(t * 1e3, vin, color=C_INPUT, linewidth=1, alpha=0.7, label="Input")
    ax1.plot(t * 1e3, vout_hw, color=C_OUT, linewidth=2, label="Half-wave rectified")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage")
    ax1.set_title("Half-wave precision rectifier", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    # Full-wave (absolute value)
    vout_fw = np.abs(vin)
    ax2.plot(t * 1e3, vin, color=C_INPUT, linewidth=1, alpha=0.7, label="Input")
    ax2.plot(t * 1e3, vout_fw, color=C_OUT, linewidth=2, label="|Vin| = full-wave")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Full-wave (absolute value)", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_wien_osc(p):
    f = p["f_osc"]
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 5 / f, 1000)
    # Simulated start-up: exponential rise to steady state
    envelope = 1 - np.exp(-t * f * 2)
    vout = envelope * 3 * np.sin(2 * np.pi * f * t)
    ax.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label=f"Sine output at {f} Hz")
    ax.plot(t * 1e3, envelope * 3, color=C_THRESH, linewidth=1, linestyle="--", alpha=0.5, label="AGC envelope")
    ax.plot(t * 1e3, -envelope * 3, color=C_THRESH, linewidth=1, linestyle="--", alpha=0.5)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title("Wien Bridge Oscillator — start-up to steady state", fontsize=11, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_relaxation_osc(p):
    f = p["f_osc"]
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    t = np.linspace(0, 5 / f, 1000)
    # Square wave
    sq = np.sign(np.sin(2 * np.pi * f * t)) * 5
    # Capacitor voltage (triangle-ish)
    tri = 2 * (2 * np.abs(2 * (f * t % 1) - 1) - 1)
    ax.plot(t * 1e3, sq, color=C_OUT, linewidth=2, label="Square output")
    ax.plot(t * 1e3, tri, color=C_OUT2, linewidth=1.5, label="Cap voltage (triangle)")
    ax.axhline(2, color=C_THRESH, linestyle="--", linewidth=1, alpha=0.6, label="V_TH")
    ax.axhline(-2, color=C_THRESH, linestyle="--", linewidth=1, alpha=0.6, label="V_TL")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title("Relaxation Oscillator", fontsize=11, fontweight="bold")
    ax.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_class_a_concept(p):
    """Class A: full 360° conduction — device current never cuts off; Vout tracks Vin."""
    f = float(p.get("f", 1000))
    n = 2500
    t = np.linspace(0, 4 / f, n)
    vin = np.sin(2 * np.pi * f * t)
    av = p.get("Av", 0.85)
    vout = av * vin
    Iq = p.get("I_quiescent", 0.45)
    Iac = p.get("I_ac_peak", 0.38)
    ic = Iq + Iac * vin
    ic = np.clip(ic, 0.02, None)

    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.2, alpha=0.8, label="Vin  (drive)")
    ax1.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label="Vout  (load, linear)")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage (norm)")
    ax1.set_title("Class-A: sinusoidal output, no crossover gap", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    ax2.plot(t * 1e3, ic, color=C_OUT2, linewidth=2, label="Collector / current (always > 0)")
    ax2.axhline(Iq, color=FG, linestyle=":", linewidth=0.8, alpha=0.5, label="Iquiescent")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Current (norm)")
    ax2.set_title("360° conduction — bias keeps device on full cycle", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig


def _wf_class_b_concept(p):
    """Class B: each device conducts ~180°; crossover notch near zero; AB reduces notch."""
    f = float(p.get("f", 1000))
    n = 3600
    t = np.linspace(0, 5 / f, n)
    vin = np.sin(2 * np.pi * f * t)
    vz = float(p.get("V_dead", 0.11))
    vout_b = np.sign(vin) * np.maximum(np.abs(vin) - vz, 0.0)
    small = np.abs(vin) < vz
    vout_b[small] = vin[small] * 0.05
    ab_blend = float(p.get("ab_blend", 0.35))
    vout_ab = np.sign(vin) * np.maximum(np.abs(vin) - vz * (1 - ab_blend), 0.0)
    small2 = np.abs(vin) < vz * (1 - ab_blend * 0.5)
    vout_ab[small2] = vin[small2] * (0.15 + 0.5 * ab_blend)

    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.2, alpha=0.75, label="Vin")
    ax1.plot(t * 1e3, vout_b, color=C_THRESH, linewidth=1.5, label="Class-B  (crossover notch)")
    ax1.plot(t * 1e3, vout_ab, color=C_OUT, linewidth=2, label="Class-AB  (smoother)")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage (norm)")
    ax1.set_title("Output near zero: B has dead zone; AB overlaps conduction", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    i_n = np.maximum(vin - vz * 0.3, 0.0) ** 1.05
    i_p = np.maximum(-vin - vz * 0.3, 0.0) ** 1.05
    ax2.plot(t * 1e3, i_n, color=C_OUT, linewidth=1.5, label="NPN  (positive half)")
    ax2.plot(t * 1e3, -i_p, color=C_OUT3, linewidth=1.5, label="PNP  (negative half)")
    ax2.axhline(0, color=FG, linewidth=0.6, alpha=0.4)
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Branch current (norm)")
    ax2.set_title("Each device carries ~180°; gap at handoff without AB bias", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig


def _wf_class_c_concept(p):
    """Class C: short conduction angle; narrow Ic pulses; LC tank pulls sinusoidal Vout."""
    f = float(p.get("f", 3e6))
    deg = float(p.get("conduction_deg", 72))
    n = 16000
    t = np.linspace(0, 8 / f, n)
    dt = t[1] - t[0]
    fs = 1.0 / dt
    phase = np.mod(2 * np.pi * f * t, 2 * np.pi)
    center = np.pi / 2
    halfw = np.deg2rad(deg) / 2
    d = np.abs(phase - center)
    d = np.minimum(d, 2 * np.pi - d)
    mask = d < halfw
    ic = np.where(mask, np.cos(d / halfw * (np.pi / 2)) ** 2, 0.0) * 2.8

    try:
        b, a = sig.butter(4, [f * 0.985, f * 1.015], btype="band", fs=fs)
        v_load = sig.filtfilt(b, a, ic)
    except ValueError:
        v_load = np.sin(2 * np.pi * f * t) * (np.max(ic) * 0.35)
    mx = np.max(np.abs(v_load)) + 1e-9
    v_load = v_load / mx

    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(t * 1e6, ic, color=C_OUT2, linewidth=1.2, label="Ic  (narrow pulses)")
    ax1.set_xlabel("Time (µs)")
    ax1.set_ylabel("Current (norm)")
    ax1.set_title(f"Class-C: conduction ≈ {deg:.0f}° per RF cycle", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    ax2.plot(t * 1e6, v_load, color=C_OUT, linewidth=2, label="Vload  (tank rings sine)")
    ax2.set_xlabel("Time (µs)")
    ax2.set_ylabel("Voltage (norm)")
    ax2.set_title("Fundamental reconstructed by high-Q tuned load", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig


def _wf_transimpedance(p):
    """Photodiode TIA: V ≈ −I·Zf with dominant pole from Rf‖Cf."""
    Rf = p.get("Rf", 1e6)
    Cf = p.get("Cf", 2e-12)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    f = np.logspace(0, np.log10(p.get("f_plot_max", 200000)), 600)
    w = 2 * np.pi * f
    Zf = Rf / (1 + 1j * w * Rf * Cf)
    ax1.semilogx(f, 20 * np.log10(np.abs(Zf) + 1e-15), color=C_OUT, linewidth=2)
    fp = 1 / (2 * np.pi * Rf * Cf)
    ax1.axvline(fp, color=C_THRESH, linestyle="--", linewidth=1, label=f"pole ≈ {fp:.0f} Hz")
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("|Z_f| (Ω)")
    ax1.set_title("TIA feedback impedance |V / I|", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    f_in = p.get("f_in", 1000)
    I_ac = p.get("I_ac", 40e-9)
    t = np.linspace(0, 3 / f_in, 1200)
    Iin = I_ac * np.sin(2 * np.pi * f_in * t)
    # Dominant-pole approximation
    H = -Rf / (1 + 1j * 2 * np.pi * f_in * Rf * Cf)
    vout = np.abs(H) * I_ac * np.sin(2 * np.pi * f_in * t + np.angle(H))
    ax2.plot(t * 1e3, Iin * 1e9, color=C_INPUT, linewidth=1.2, alpha=0.85, label="I (nA)")
    ax2.plot(t * 1e3, vout * 1e3, color=C_OUT, linewidth=2, label="Vout (mV)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("I / V")
    ax2.set_title("Current in → voltage out (inverting)", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_class_d_concept(p):
    """PWM vs audio + crude averaged output."""
    f_sig = p.get("f_sig", 1000)
    f_sw = p.get("f_sw", 40000)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    t = np.linspace(0, 3 / f_sig, min(8000, int(3 / f_sig * f_sw * 4)))
    sig = 0.85 * np.sin(2 * np.pi * f_sig * t)
    tri = 2 * (2 * ((t * f_sw) % 1) - 1)
    pwm = np.where(sig >= tri, 1.0, -1.0)
    ax1.plot(t * 1e3, pwm, color=C_INPUT, linewidth=0.5, alpha=0.85)
    ax1.set_xlim(0, min(2, t[-1] * 1e3))
    ax1.set_ylim(-1.25, 1.25)
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("PWM")
    ax1.set_title("High-frequency switching (zoomed)", fontsize=10, fontweight="bold")

    win = max(int(f_sw / f_sig / 6), 7)
    k = np.ones(win) / win
    filt = np.convolve(pwm, k, mode="same")
    ax2.plot(t * 1e3, sig, color=FG, linewidth=1.2, linestyle=":", alpha=0.7, label="Target audio")
    ax2.plot(t * 1e3, filt, color=C_OUT, linewidth=2, label="Boxcar average (conceptual LPF)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage (norm)")
    ax2.set_title("Class-D: recover waveform after LC output filter", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_log_amp_concept(p):
    """Compression: log-like output vs input magnitude (conceptual)."""
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    vin = np.logspace(-4, 1, 300)
    Vt = p.get("Vt", 0.026)
    I0 = p.get("I0", 1e-3)
    vout = -Vt * np.log(np.maximum(vin, 1e-9) / I0 + 1e-15)
    vout -= np.nanmedian(vout)
    ax.semilogx(vin * 1000, vout * 1000, color=C_OUT, linewidth=2)
    ax.set_xlabel("Input (mV, normalized scale)")
    ax.set_ylabel("Output (mV, conceptual)")
    ax.set_title("Log amplifier: large dynamic range compressed", fontsize=10, fontweight="bold")
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_antilog_concept(p):
    """Exp-like output vs control voltage — inverse of an ideal log stage."""
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    Vt = p.get("Vt", 0.026)
    span = float(p.get("v_span", 0.12))
    vctrl = np.linspace(-span, span, 500)
    i_norm = np.exp(vctrl / Vt)
    i_norm /= np.max(i_norm)
    ax.plot(vctrl * 1000, i_norm, color=C_OUT, linewidth=2, label="I ∝ exp(V/Vₜ)")
    ax.set_xlabel("Control voltage (mV)")
    ax.set_ylabel("Output (normalized)")
    ax.set_title("Antilog: exponential response vs control", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.6)
    fig.tight_layout(pad=1.5)
    return fig

# ─── RF / distributed concepts ───────────────────────────────────────

def _wf_tl_stub_concept(p):
    """Open stub: imaginary input impedance vs frequency (transmission-line RF)."""
    Z0 = p.get("Z0", 50.0)
    vp = p.get("vp", 1.58e8)
    f_qw = p.get("f_quarter_wave", 2.4e9)
    ell = vp / (4.0 * f_qw)
    f_lo = max(50e6, f_qw * 0.25)
    f_hi = f_qw * 2.2
    f = np.linspace(f_lo, f_hi, 2500)
    beta = 2 * np.pi * f / vp
    bl = beta * ell
    X = -Z0 / np.tan(bl)
    X = np.clip(X, -600, 600)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(f / 1e9, X, color=C_OUT, linewidth=2)
    ax1.axhline(0, color=FG, linewidth=0.5, alpha=0.4)
    ax1.axvline(f_qw / 1e9, color=C_THRESH, linestyle="--", linewidth=1,
                label=f"ℓ = λ/4 @ {f_qw/1e9:.2f} GHz")
    ax1.set_xlabel("Frequency (GHz)")
    ax1.set_ylabel("Im{Zin} open stub (Ω, clipped)")
    ax1.set_title(f"Shunt open stub  Z₀={Z0:.0f} Ω", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    deg = (bl * 180 / np.pi) % 360
    ax2.plot(f / 1e9, deg, color=C_OUT2, linewidth=2, label="βℓ (deg) mod 360")
    ax2.axvline(f_qw / 1e9, color=C_THRESH, linestyle="--", linewidth=1)
    ax2.set_xlabel("Frequency (GHz)")
    ax2.set_ylabel("Electrical length (deg)")
    ax2.set_title("Stub rotates on Smith chart as f moves", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_lattice_rf_allpass_concept(p):
    """Passive bridge / lattice: |H| ≈ flat, phase engineered (RF all-pass idea)."""
    f_lo = p.get("f_lo", 5e6)
    f_hi = p.get("f_hi", 3e9)
    tau = p.get("tau", 5e-10)
    f = np.logspace(np.log10(f_lo), np.log10(f_hi), 600)
    w = 2 * np.pi * f
    s = 1j * w
    H = (1 - s * tau) / (1 + s * tau)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.semilogx(f, 20 * np.log10(np.abs(H) + 1e-15), color=C_OUT, linewidth=2)
    ax1.set_ylim(-0.08, 0.08)
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Gain (dB)")
    ax1.set_title("Lattice / delay: magnitude ≈ unity", fontsize=10, fontweight="bold")

    phase_deg = np.unwrap(np.angle(H)) * 180 / np.pi
    ax2.semilogx(f, phase_deg, color=C_OUT2, linewidth=2)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Phase (°)")
    ax2.set_title("Phase delay vs frequency (group delay shaping)", fontsize=10, fontweight="bold")
    fig.tight_layout(pad=1.5)
    return fig

def _wf_lna_tuned_concept(p):
    """Narrowband gain + Friis intuition (first stage dominates NF when G₁ is good)."""
    f0 = p.get("f0", 2.45e9)
    Q = p.get("Q", 12.0)
    gmax_db = p.get("Gmax_db", 16.0)
    span = p.get("span_frac", 0.06)
    f = np.linspace(f0 * (1 - span), f0 * (1 + span), 900)
    det = f / f0 - f0 / f
    G_db = gmax_db - 10 * np.log10(1 + (Q * det) ** 2)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(f / 1e9, G_db, color=C_OUT, linewidth=2)
    ax1.axvline(f0 / 1e9, color=C_THRESH, linestyle="--", linewidth=1)
    ax1.set_xlabel("Frequency (GHz)")
    ax1.set_ylabel("Power gain (dB, conceptual |S21|)")
    ax1.set_title(f"Tuned LNA passband (Q≈{Q:.0f})", fontsize=10, fontweight="bold")

    F1_db = p.get("nf_lna_db", 0.9)
    F2_db = p.get("nf_follow_db", 6.0)
    g1_db = p.get("gain_lna_db", 14.0)
    F1 = 10 ** (F1_db / 10)
    F2 = 10 ** (F2_db / 10)
    G1 = 10 ** (g1_db / 10)
    Fsys = F1 + (F2 - 1) / G1
    Fsys_db = 10 * np.log10(Fsys)
    cats = ["LNA NF", "Rx chain\nw/ LNA", "Same Rx\n(G₁=0 dB)"]
    vals = [F1_db, Fsys_db, F2_db]
    cols = [C_INPUT, C_OUT, C_OUT2]
    x0 = np.arange(len(cats))
    ax2.bar(x0, vals, color=cols, width=0.55, edgecolor=GRID)
    ax2.set_xticks(x0)
    ax2.set_xticklabels(cats, fontsize=8)
    ax2.set_ylabel("Noise figure (dB)")
    ax2.set_title("Friis: low NF LNA pulls system noise", fontsize=10, fontweight="bold")
    fig.tight_layout(pad=1.5)
    return fig

def _wf_rf_pa_compression(p):
    """Pout vs Pin and gain vs Pin — compression / PSAT behaviour."""
    G0_db = p.get("small_signal_gain_db", 16)
    P1_out_dbm = p.get("p1db_out_dbm", 22)
    Pin_dbm = np.linspace(-28, 6, 450)
    Pin_mw = 10 ** ((Pin_dbm - 30) / 10)
    G0 = 10 ** (G0_db / 10)
    Pideal_mw = Pin_mw * G0
    Psat_mw = 10 ** ((P1_out_dbm + 2.8 - 30) / 10)
    Pout_mw = Psat_mw * np.tanh(Pideal_mw / Psat_mw)
    Pout_dbm = 10 * np.log10(np.maximum(Pout_mw, 1e-18)) + 30
    gain_db = Pout_dbm - Pin_dbm
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(Pin_dbm, Pout_dbm, color=C_OUT, linewidth=2, label="Pout")
    ax1.plot(Pin_dbm, Pin_dbm + G0_db, color=C_THRESH, linestyle=":", linewidth=1.2,
             label=f"Extrapolated (G={G0_db} dB)")
    ax1.set_xlabel("Pin (dBm)")
    ax1.set_ylabel("Pout (dBm)")
    ax1.set_title("PA: output saturates / compresses", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    ax2.plot(Pin_dbm, gain_db, color=C_OUT2, linewidth=2, label="Gain")
    ax2.axhline(G0_db, color=C_THRESH, linestyle="--", linewidth=1, alpha=0.6, label="Small-signal G")
    ax2.set_xlabel("Pin (dBm)")
    ax2.set_ylabel("Gain (dB)")
    ax2.set_title("Gain rolls off toward PSAT", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_npath_comb_concept(p):
    """N-path: periodic replicas around clock / LO (conceptual |H| comb)."""
    f0 = p.get("f_center", 0.95e9)
    f_clk = p.get("f_clk", 130e6)
    k_max = int(p.get("k_max", 3))
    bw_frac = p.get("peak_bw_frac", 0.022)
    f_lo = f0 - (k_max + 1) * f_clk
    f_hi = f0 + (k_max + 1) * f_clk
    f = np.linspace(f_lo, f_hi, 4000)
    sigma = bw_frac * f0
    mag = np.zeros_like(f)
    for k in range(-k_max, k_max + 1):
        mag += np.exp(-0.5 * ((f - (f0 + k * f_clk)) / sigma) ** 2)
    mag /= np.max(mag)
    H_db = 20 * np.log10(mag + 1e-9)
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    ax.plot(f / 1e9, H_db, color=C_OUT, linewidth=2)
    for k in range(-k_max, k_max + 1):
        ax.axvline((f0 + k * f_clk) / 1e9, color=GRID, linestyle=":", linewidth=0.7, alpha=0.7)
    ax.axvline(f0 / 1e9, color=C_THRESH, linestyle="--", linewidth=1.2, label=f"RF ~ {f0/1e9:.2f} GHz")
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Normalized |H| (dB)")
    ax.set_title(
        f"N-path-style passbands every f_clk ≈ {f_clk/1e6:.0f} MHz (conceptual)",
        fontsize=10,
        fontweight="bold",
    )
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_fda_concept(p):
    """Fully differential amp: VOCM-centered complementary outputs, differential gain."""
    vocm = p.get("vocm", 2.5)
    g_db = p.get("gain_db", 12)
    f = p.get("f_input", 2e6)
    v_diff_pk = p.get("v_diff_pk", 0.06)
    G = 10 ** (g_db / 20)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    t = np.linspace(0, 3 / f, 900)
    w = 2 * np.pi * f
    vd = v_diff_pk * np.sin(w * t)
    vip = vocm + vd / 2
    vim = vocm - vd / 2
    vop = vocm + G * vd / 2
    vom = vocm - G * vd / 2
    t_end = float(t[-1])
    if t_end < 5e-8:
        tp, tu = t * 1e9, "ns"
    elif t_end < 5e-5:
        tp, tu = t * 1e6, "µs"
    else:
        tp, tu = t * 1e3, "ms"
    ax1.plot(tp, vip, color=C_INPUT, linewidth=1.5, alpha=0.9, label="VIN+")
    ax1.plot(tp, vim, color=C_OUT2, linewidth=1.5, alpha=0.9, label="VIN−")
    ax1.axhline(vocm, color=GRID, linestyle=":", linewidth=0.8, alpha=0.7)
    ax1.set_xlabel(f"Time ({tu})")
    ax1.set_ylabel("Voltage")
    ax1.set_title("Differential inputs about VOCM", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    ax2.plot(tp, vop, color=C_OUT, linewidth=2, label="VOUT+")
    ax2.plot(tp, vom, color=C_THRESH, linewidth=2, label="VOUT−")
    ax2.axhline(vocm, color=GRID, linestyle=":", linewidth=0.8, alpha=0.7)
    ax2.set_xlabel(f"Time ({tu})")
    ax2.set_ylabel("Voltage")
    ax2.set_title(f"Balanced outputs:  VOUT+ − VOUT− ≈ {G:.2f} × (VIN+ − VIN−)", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_switched_cap_concept(p):
    """Clock + continuous input vs held (ZOH) waveform — discrete-time SC path."""
    f_sig = p.get("f_sig", 650)
    f_clk = p.get("f_clk", 18000)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    t = np.linspace(0, 4 / f_sig, 3000)
    vin = 0.35 * np.sin(2 * np.pi * f_sig * t)
    tick = np.floor(t * f_clk).astype(np.int64)
    t_s = tick.astype(float) / f_clk
    vheld = 0.35 * np.sin(2 * np.pi * f_sig * t_s)
    clk = np.sign(np.sin(2 * np.pi * f_clk * t))
    ax1.plot(t * 1e3, vin, color=C_INPUT, linewidth=1.5, label="Continuous Vin")
    ax1.plot(t * 1e3, vheld, color=C_OUT, linewidth=1.4, drawstyle="steps-post", label="Sampled / held (conceptual)")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage")
    ax1.set_title("Switched-cap: signal becomes piecewise-constant between clocks", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)

    ax2.plot(t * 1e3, clk, color=C_OUT2, linewidth=1, label="φ clock (square)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Clock")
    ax2.set_title(f"f_clk = {f_clk/1000:.1f} kHz  (illustrative)", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_otac_integrator_concept(p):
    """OTA-C building block: |Vout/Vin| ≈ gm/(ωC), −20 dB/decade."""
    gm = p.get("gm", 0.4e-3)
    C = p.get("C", 3e-12)
    f_u = gm / (2 * np.pi * C)
    lo = max(1.5, np.log10(f_u) - 2.3)
    hi = min(10.0, np.log10(f_u) + 2.3)
    if hi <= lo:
        hi = lo + 0.4
    f = np.logspace(lo, hi, 500)
    H = gm / (2 * np.pi * f * C)
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    ax.semilogx(f, 20 * np.log10(H + 1e-15), color=C_OUT, linewidth=2)
    ax.axvline(f_u, color=C_THRESH, linestyle="--", linewidth=1, label=f"≈ unity-gain freq {f_u/1e6:.2f} MHz")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Integrator gain (dB)")
    ax.set_title("Gm/C integrator:  |H| ≈ gm/(ωC)  — biquads stack these blocks", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_lc_ladder_coupled_concept(p):
    """Two close resonances — conceptual |S21| for coupled ladder / duplexer modes."""
    f1 = p.get("f1_hz", 0.92e6)
    f2 = p.get("f2_hz", 1.05e6)
    Q = p.get("Q", 120.0)
    f_lo = min(f1, f2) * (1 - 4 / Q)
    f_hi = max(f1, f2) * (1 + 4 / Q)
    f = np.linspace(f_lo, f_hi, 800)

    def lorentz(f0):
        x = 2 * Q * (f - f0) / f0
        return 1 / np.sqrt(1 + x ** 2)

    h = 0.55 * lorentz(f1) + 0.55 * lorentz(f2)
    h /= np.max(h)
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    ax.plot(f / 1e6, 20 * np.log10(h + 1e-9), color=C_OUT, linewidth=2)
    ax.axvline(f1 / 1e6, color=GRID, linestyle=":", linewidth=0.9, alpha=0.8)
    ax.axvline(f2 / 1e6, color=GRID, linestyle=":", linewidth=0.9, alpha=0.8)
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel("Normalized |response| (dB)")
    ax.set_title("Coupled resonators: two modes close in frequency (conceptual)", fontsize=10, fontweight="bold")
    fig.tight_layout(pad=1.5)
    return fig

def _wf_gic_inductor_z_concept(p):
    """GIC-simulated inductor: |Z(f)| grows ~ f (inductive)."""
    Leff = p.get("Leff", 2.2e-6)
    f = np.logspace(2, 6.5, 500)
    Z = 2 * np.pi * f * Leff
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    ax.loglog(f, Z, color=C_OUT, linewidth=2, label=f"|Z| ≈ ωL  (L≈{Leff*1e6:.1f} µH)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("|Z| (Ω)")
    ax.set_title("Antoniou GIC: synthesize inductance — impedance rises with frequency", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_noninv_summer(p):
    """Non-inverting summer: V+ = weighted average, then Vout = (1+Rf/Rg)·V+."""
    f1 = float(p.get("f1", 380))
    f2 = float(p.get("f2", 1050))
    g = float(p.get("gain", 1.85))
    w1 = float(p.get("w1", 0.5))
    w2 = 1.0 - w1
    t = np.linspace(0, 3.5 / min(f1, f2), 1100)
    v1 = 0.22 * np.sin(2 * np.pi * f1 * t)
    v2 = 0.18 * np.sin(2 * np.pi * f2 * t + 0.6)
    vplus = w1 * v1 + w2 * v2
    vout = g * vplus
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(t * 1e3, v1, color=C_INPUT, linewidth=1.2, alpha=0.85, label="V1")
    ax1.plot(t * 1e3, v2, color=C_OUT2, linewidth=1.2, alpha=0.85, label="V2")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage")
    ax1.set_title("Inputs feed resistor network to V+", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    ax2.plot(t * 1e3, vplus, color=C_THRESH, linewidth=1.2, linestyle="--", alpha=0.8, label="V+ (weighted)")
    ax2.plot(t * 1e3, vout, color=C_OUT, linewidth=2, label=f"Vout = {g:.2f} × V+")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Non-inverting summer + gain", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_dac_buffer_concept(p):
    """Quantized DAC staircase vs ideal sine; buffer reproduces levels and drives load."""
    f = float(p.get("f_sig", 140))
    nbits = int(p.get("nbits", 4))
    t = np.linspace(0, 3 / f, 2000)
    ideal = 0.32 * np.sin(2 * np.pi * f * t)
    nlev = 2 ** nbits
    step = 2.0 / (nlev - 1) * 0.32
    dac = np.round(ideal / step) * step
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(t * 1e3, ideal, color=FG, linewidth=1, linestyle=":", alpha=0.6, label="Ideal target")
    ax1.plot(t * 1e3, dac, color=C_INPUT, linewidth=1.5, drawstyle="steps-mid", label=f"{nbits}-bit DAC output")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage")
    ax1.set_title("Voltage-output DAC is piecewise constant", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    ax2.plot(t * 1e3, dac, color=C_OUT, linewidth=1.5, drawstyle="steps-mid", label="Buffer output (low Z_drv)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Op-amp follower / non-inverting buffer drives cable & ADC C_sample", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_charge_amp_concept(p):
    """Charge amplifier: short current burst integrates on Cf, Rf provides DC bleed."""
    Cf = float(p.get("Cf", 12e-12))
    Rf = float(p.get("Rf", 50e6))
    t = np.linspace(0, 2.5e-3, 2500)
    i_in = np.zeros_like(t)
    i_in[(t > 0.25e-3) & (t < 0.32e-3)] = 25e-6
    dt = t[1] - t[0]
    v = np.zeros_like(t)
    tau = Rf * Cf
    for k in range(1, len(t)):
        v[k] = v[k - 1] + (i_in[k] / Cf) * dt - v[k - 1] * dt / tau
    fig, ax = _make_fig(1, 1, (9, 3.8))
    ax = ax[0]
    ax2 = ax.twinx()
    ax.plot(t * 1e3, v * 1000, color=C_OUT, linewidth=2, label="Vout (mV)")
    ax2.plot(t * 1e3, i_in * 1e6, color=C_INPUT, linewidth=1.2, alpha=0.75, label="I_sensor (µA)")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Vout (mV)")
    ax2.set_ylabel("Current (µA)", color=C_INPUT)
    ax2.tick_params(axis="y", colors=C_INPUT)
    ax.set_title(f"Charge amp: ΔQ on Cf, bleed Rf = {Rf/1e6:.0f} MΩ", fontsize=10, fontweight="bold")
    ax.legend(loc="upper left", fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    ax2.legend(loc="upper right", fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=C_INPUT)
    for spine in ax2.spines.values():
        spine.set_color(GRID)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_isolation_amp_concept(p):
    """Conceptual: recovered signal vs huge common-mode on input side."""
    f = float(p.get("f_sig", 120))
    t = np.linspace(0, 3 / f, 800)
    v_sig = 0.06 * np.sin(2 * np.pi * f * t)
    v_cm = 1.5 * np.sin(2 * np.pi * 7 * t)
    v_line = 2.5 + v_sig + v_cm
    v_iso = 2.5 + v_sig
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(t * 1e3, v_line, color=C_INPUT, linewidth=1.5, label="Line-referenced input (CM + signal)")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage")
    ax1.set_title("Sensor side: common-mode interference", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    ax2.plot(t * 1e3, v_iso, color=C_OUT, linewidth=2, label="Isolated output (CM rejected)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Receiver side: differential / isolated link recovers signal", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_lockin_concept(p):
    """PSD: multiply meas × ref, LPF extracts in-phase component."""
    f = float(p.get("f_ref", 400))
    t = np.linspace(0, 5 / f, 5000)
    ref = np.sin(2 * np.pi * f * t)
    noise = 0.14 * np.sin(2 * np.pi * f * 2.73 * t) + 0.1 * np.sin(2 * np.pi * f * 5.1 * t)
    meas = 0.1 * ref + noise
    prod = meas * ref * 2.0
    win = max(int(len(t) / 80), 21)
    ker = np.ones(win) / win
    demod = np.convolve(prod, ker, mode="same")
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(t * 1e3, meas, color=C_INPUT, linewidth=0.8, alpha=0.9, label="Noisy measurement")
    ax1.plot(t * 1e3, ref * 0.15, color=C_THRESH, linewidth=1, alpha=0.7, label="Reference (scaled)")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Voltage")
    ax1.set_title("Narrowband signal buried in wideband junk", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    ax2.plot(t * 1e3, prod, color=C_OUT2, linewidth=0.6, alpha=0.65, label="meas × ref")
    ax2.plot(t * 1e3, demod, color=C_OUT, linewidth=2, label="Low-pass (in-phase amplitude)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Voltage")
    ax2.set_title("Lock-in / synchronous detection", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_class_gh_concept(p):
    """Class G/H: supply rail steps with envelope to save loss in output devices."""
    f = float(p.get("f_sig", 500))
    t = np.linspace(0, 3 / f, 1000)
    vo = 0.55 * np.sin(2 * np.pi * f * t)
    th = float(p.get("rail_threshold", 0.22))
    rail = np.where(np.abs(vo) > th, 8.0, 3.3)
    fig, (ax1, ax2) = _make_fig(1, 2, (10, 3.8))
    ax1.plot(t * 1e3, vo, color=C_OUT, linewidth=2, label="Output")
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Vout")
    ax1.set_title("Output waveform", fontsize=10, fontweight="bold")
    ax1.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    ax2.plot(t * 1e3, rail, color=C_THRESH, linewidth=2, drawstyle="steps-post", label="Effective rail (conceptual)")
    ax2.set_xlabel("Time (ms)")
    ax2.set_ylabel("Supply (V)")
    ax2.set_title("Class G/H: higher rail only when |Vout| is large", fontsize=10, fontweight="bold")
    ax2.legend(fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_pa_efficiency_arch_concept(p):
    """Illustrative efficiency vs back-off: classic, Doherty-like, ET-like."""
    pnorm = np.linspace(0.02, 1.0, 150)
    p_db = 10 * np.log10(pnorm)
    eta_classb = 0.72 * np.sqrt(pnorm)
    eta_doh = np.minimum(0.58 + 0.32 * pnorm, 0.78)
    eta_et = 0.52 + 0.28 * (pnorm ** 0.35)
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    ax.plot(p_db, 100 * eta_classb, color=C_INPUT, linewidth=2, label="Idealized Class-B back-off")
    ax.plot(p_db, 100 * eta_doh, color=C_OUT, linewidth=2, label="Load-modulated (Doherty-style)")
    ax.plot(p_db, 100 * eta_et, color=C_OUT2, linewidth=2, label="Envelope tracking (conceptual)")
    ax.set_xlabel("Output power (normalized, dB)")
    ax.set_ylabel("Drain efficiency (%)")
    ax.set_title("PA efficiency vs power back-off — illustrative", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_common_emitter_concept(p):
    """Common-emitter: base drive, inverted collector swing."""
    f = float(p.get("f_input", 1300))
    av = float(p.get("Av", -12))
    t = np.linspace(0, 3 / f, 600)
    vb = 1.05 + 0.02 * np.sin(2 * np.pi * f * t)
    vc = 2.85 + av * 0.02 * np.sin(2 * np.pi * f * t)
    fig, ax = _make_fig(1, 1, (9, 3.5))
    ax = ax[0]
    ax.plot(t * 1e3, vb, color=C_INPUT, linewidth=1.5, label="Base (input)")
    ax.plot(t * 1e3, vc, color=C_OUT, linewidth=2, label="Collector (output)")
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Voltage")
    ax.set_title(f"Common-emitter: ~180° phase shift, |Av| ≈ {abs(av):.0f} (conceptual)", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_cascode_bw_concept(p):
    """Single CE vs cascode — conceptual bandwidth extension."""
    f = np.logspace(5, 9, 400)
    f_p1 = float(p.get("f_pole_ce", 12e6))
    f_p2 = float(p.get("f_pole_cascade", 55e6))
    H_ce = 1 / np.sqrt(1 + (f / f_p1) ** 2)
    H_cs = 1 / np.sqrt(1 + (f / f_p2) ** 2)
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    ax.semilogx(f, 20 * np.log10(H_ce + 1e-9), color=C_INPUT, linewidth=2, label="Single CE stage")
    ax.semilogx(f, 20 * np.log10(H_cs + 1e-9), color=C_OUT, linewidth=2, label="Cascode (Miller reduced)")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Normalized gain (dB)")
    ax.set_title("Cascode raises effective pole / bandwidth (illustrative)", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_diff_pair_concept(p):
    """Emitter-coupled pair: differential output current vs Vid."""
    vt = float(p.get("Vt", 0.026))
    iss = float(p.get("Iss", 1e-3))
    vid = np.linspace(-0.1, 0.1, 400)
    i1 = iss / (1 + np.exp(-vid / vt))
    i2 = iss - i1
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    ax.plot(vid * 1000, i1 * 1e3, color=C_OUT, linewidth=2, label="IC1")
    ax.plot(vid * 1000, i2 * 1e3, color=C_OUT2, linewidth=2, label="IC2")
    ax.plot(vid * 1000, (i1 - i2) * 1e3, color=C_THRESH, linewidth=2, linestyle="--", label="ΔI")
    ax.set_xlabel("Vbe1 − Vbe2  (mV)")
    ax.set_ylabel("Collector current (mA)")
    ax.set_title("Differential pair: tanh-shaped steering of tail current", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_current_mirror_concept(p):
    """Iout ≈ N · Iref for simple mirror ratio."""
    n = float(p.get("N", 3))
    iref = np.linspace(0, 180e-6, 60)
    iout = n * iref
    fig, ax = _make_fig(1, 1, (9, 3.8))
    ax = ax[0]
    ax.plot(iref * 1e6, iout * 1e6, color=C_OUT, linewidth=2, label=f"Iout ≈ {n:.2g} × Iref")
    ax.plot(iref * 1e6, iref * 1e6, color=GRID, linestyle=":", linewidth=1, alpha=0.8, label="1:1 line")
    ax.set_xlabel("Iref (µA)")
    ax.set_ylabel("Iout (µA)")
    ax.set_title("BJT current mirror / ratioed copy (idealized)", fontsize=10, fontweight="bold")
    ax.legend(fontsize=8, facecolor=BG, edgecolor=GRID, labelcolor=FG)
    fig.tight_layout(pad=1.5)
    return fig

def _wf_traveling_wave_concept(p):
    """Conceptual flat gain over multi-decade RF span (IC TWA idea)."""
    f = np.logspace(8, 10.8, 120)
    ripple = 0.4 * np.sin(2.3 * np.log10(f))
    gain = 11.5 + ripple
    fig, ax = _make_fig(1, 1, (9, 4))
    ax = ax[0]
    ax.semilogx(f / 1e9, gain, color=C_OUT, linewidth=2)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("Gain (dB)")
    ax.set_title("Distributed / traveling-wave amplifier — wideband gain (conceptual)", fontsize=10, fontweight="bold")
    fig.tight_layout(pad=1.5)
    return fig


OPAMP_GENERATORS = {
    "follower": _wf_follower,
    "discrete_follower_rf": _wf_discrete_follower_rf,
    "common_emitter_concept": _wf_common_emitter_concept,
    "cascode_bw_concept": _wf_cascode_bw_concept,
    "diff_pair_concept": _wf_diff_pair_concept,
    "current_mirror_concept": _wf_current_mirror_concept,
    "traveling_wave_concept": _wf_traveling_wave_concept,
    "non_inverting_amp": _wf_non_inv_amp,
    "inverting_amp": _wf_inv_amp,
    "summing_amp": _wf_summing_amp,
    "noninv_summer": _wf_noninv_summer,
    "dac_buffer_concept": _wf_dac_buffer_concept,
    "diff_amp": _wf_diff_amp,
    "instrumentation_amp": _wf_instrumentation_amp,
    "howland_concept": _wf_howland_concept,
    "pga_concept": _wf_pga_concept,
    "vga_concept": _wf_vga_concept,
    "chopper_concept": _wf_chopper_concept,
    "charge_amp_concept": _wf_charge_amp_concept,
    "isolation_amp_concept": _wf_isolation_amp_concept,
    "lockin_concept": _wf_lockin_concept,
    "integrator": _wf_integrator,
    "differentiator": _wf_differentiator,
    "comparator": _wf_comparator,
    "schmitt": _wf_schmitt,
    "peak_detector": _wf_peak_detector,
    "precision_rectifier": _wf_precision_rectifier,
    "wien_oscillator": _wf_wien_osc,
    "relaxation_osc": _wf_relaxation_osc,
    "class_a_concept": _wf_class_a_concept,
    "class_b_concept": _wf_class_b_concept,
    "class_c_concept": _wf_class_c_concept,
    "transimpedance": _wf_transimpedance,
    "class_d_concept": _wf_class_d_concept,
    "class_gh_concept": _wf_class_gh_concept,
    "pa_efficiency_arch_concept": _wf_pa_efficiency_arch_concept,
    "log_amp_concept": _wf_log_amp_concept,
    "antilog_concept": _wf_antilog_concept,
    "tl_stub_concept": _wf_tl_stub_concept,
    "lattice_rf_allpass": _wf_lattice_rf_allpass_concept,
    "lna_tuned_concept": _wf_lna_tuned_concept,
    "rf_pa_compression": _wf_rf_pa_compression,
    "npath_comb_concept": _wf_npath_comb_concept,
    "fda_concept": _wf_fda_concept,
    "switched_cap_concept": _wf_switched_cap_concept,
    "otac_integrator_concept": _wf_otac_integrator_concept,
    "lc_ladder_coupled_concept": _wf_lc_ladder_coupled_concept,
    "gic_inductor_z_concept": _wf_gic_inductor_z_concept,
}
