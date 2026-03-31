"""Topic subtree: Op-Amp Circuits."""

OP_AMP_BRANCH = {
    "__meta__": {
        "icon": "⚙️",
        "summary": (
            "Operational amplifiers are used inside linear amplifiers, math blocks, comparators, and "
            "many converter circuits.  With negative feedback, closed-loop behavior is set by passive "
            "networks around the part.\n\n"
            "This branch is organized by function:\n"
            "  • Amplifiers — follower, non-inverting, inverting, summing, non-inverting summer, "
            "DAC buffer, differential\n"
            "  • Special amplifiers — INA, TIA, Howland, log / antilog, PGA, FDA, VGA, chopper, "
            "charge, isolation, lock-in\n"
            "  • Math / Signal Processing — integrator, differentiator\n"
            "  • Comparators / Detectors — thresholds, Schmitt, peak, precision rectifier\n"
            "  • Oscillators / Waveform Gen — Wien, relaxation\n"
            "  • Power Amplifiers — classes A through D, G/H, Doherty / envelope tracking\n"
            "  • RF & Discrete — LNA, PA, follower, CE/CS, cascode, diff pair, mirrors, TWA\n\n"
            "Filter-focused circuits live under Filters.  Not every op-amp circuit is a filter."
        ),
    },
    "Amplifiers": {
        "__meta__": {
            "icon": "🔊",
            "summary": (
                "Linear voltage and current amplification is the most basic op-amp function.  "
                "With negative feedback, the closed-loop gain is set entirely by external "
                "resistors, making it predictable and stable.\n\n"
                "Beyond single-input stages, the inverting topology supports summing several "
                "signals on one virtual-ground node — useful for mixers and multi-source "
                "control voltages."
            ),
        },
        "Voltage Follower (Buffer)": {
            "icon": "🛡",
            "summary": (
                "The simplest op-amp circuit: output connected directly to inverting input, "
                "signal applied to non-inverting input.  Gain is exactly 1 (unity).\n\n"
                "The buffer provides IMPEDANCE TRANSFORMATION: extremely high input impedance "
                "(GΩ range for FET-input op-amps) and very low output impedance (< 1 Ω).  "
                "This means it can 'observe' a signal without loading the source, and 'drive' "
                "a load without voltage drop.\n\n"
                "Internally, the op-amp's open-loop gain forces V− = V+ (virtual short), so "
                "Vout = V+.  The feedback is 100 % (β = 1), giving the WIDEST bandwidth but "
                "also the highest demand on op-amp stability (unity-gain stable op-amps required)."
            ),
            "key_params": [
                ("Gain", "Av = 1 (exactly)"),
                ("Input impedance", "Extremely high (op-amp's Zin)"),
                ("Output impedance", "Very low (Zout_OL / (1+Aol))"),
                ("Bandwidth", "Full op-amp GBW"),
            ],
            "formula": (
                "Vout = Vin\n\n"
                "Closed-loop gain:  Av = 1 / (1 + 1/Aol) ≈ 1\n"
                "Closed-loop bandwidth ≈ GBW of op-amp.\n"
                "Output impedance ≈ Zout_open_loop / Aol."
            ),
            "usage": [
                "Buffer between a high-impedance sensor and a low-impedance ADC input.",
                "Isolating a passive filter from the next stage to prevent loading.",
                "Driving a cable or long PCB trace with low impedance.",
                "Reference voltage buffering.",
            ],
            "real_examples": [
                "pH probe buffer: OPA129 (FET input, 10¹³ Ω input Z) as follower.",
                "After RC filter: TLV9001 follower prevents ADC input from loading the filter.",
                "DAC output buffer: OPA340 follower drives 600 Ω headphone load.",
            ],
            "design_notes": (
                "• The op-amp MUST be unity-gain stable (check datasheet).\n"
                "• Capacitive loads can cause oscillation — add a small series resistor (10–47 Ω).\n"
                "• Input bias current × source resistance = offset voltage error.\n"
                "• For very high-impedance sources (> 1 GΩ), use electrometer-grade op-amps."
            ),
            "waveform": {
                "kind": "follower",
                "params": {"f_input": 1000},
            },
        },
        "Non-Inverting Amplifier": {
            "icon": "📐",
            "summary": (
                "The non-inverting amplifier applies the input signal to V+ and uses a resistor "
                "divider (Rf and Rg) from output to V− to set gain.  The output is IN PHASE "
                "with the input.\n\n"
                "Gain: Av = 1 + Rf/Rg.  When Rg → ∞ (removed), gain → 1 (voltage follower).  "
                "When Rf → ∞, gain → 1 + ∞ = open loop.\n\n"
                "Input impedance is very high (essentially the op-amp's differential input Z, "
                "often boosted by feedback).  This makes it ideal for high-impedance sources.\n\n"
                "Bandwidth is limited by the gain-bandwidth product (GBW): BW = GBW / Av.  "
                "Higher gain means lower bandwidth."
            ),
            "key_params": [
                ("Gain", "Av = 1 + Rf/Rg"),
                ("Input impedance", "Very high"),
                ("Output phase", "In-phase with input (0°)"),
                ("Bandwidth", "BW ≈ GBW / Av"),
            ],
            "formula": (
                "Vout = (1 + Rf/Rg) × Vin\n\n"
                "Gain in dB:  G = 20·log₁₀(1 + Rf/Rg)\n\n"
                "Bandwidth:  BW = GBW / (1 + Rf/Rg)\n\n"
                "Noise gain = 1 + Rf/Rg  (same as signal gain).\n\n"
                "Example: Rf = 9 kΩ, Rg = 1 kΩ → Av = 10 (20 dB).\n"
                "With 10 MHz GBW op-amp → BW = 1 MHz."
            ),
            "usage": [
                "Sensor signal amplification (thermocouple, strain gauge).",
                "Audio preamplifier.",
                "Reference voltage scaling.",
                "Buffer with gain for weak signals.",
            ],
            "real_examples": [
                "Thermocouple amp: gain = 100 (Rf=99k, Rg=1k) with AD8628 for low offset.",
                "Electret microphone preamp: gain = 20, followed by active filter.",
                "Voltage reference scaler: 1.25V ref × 2.5 = 3.125V using non-inv amp.",
            ],
            "design_notes": (
                "• For precision: use 0.1 % resistors and low-offset op-amps.\n"
                "• Add a resistor equal to Rf||Rg at V+ to cancel bias current offset.\n"
                "• At high gain, input-referred noise of the op-amp dominates.\n"
                "• Avoid stray capacitance across Rf — it forms a low-pass with Rf, cutting BW."
            ),
            "waveform": {
                "kind": "non_inverting_amp",
                "params": {"gain": 5, "f_input": 1000},
            },
        },
        "Inverting Amplifier": {
            "icon": "🔃",
            "summary": (
                "The inverting amplifier applies the input through Rin to the inverting node (V−), "
                "which is held at virtual ground by the feedback resistor Rf.  The output is "
                "PHASE-INVERTED (180°) relative to the input.\n\n"
                "Gain: Av = −Rf/Rin.  The input impedance equals Rin (not infinite), which is "
                "a key difference from the non-inverting topology.\n\n"
                "The virtual ground at V− makes the inverting node ideal for summing multiple "
                "signals — each through its own input resistor.  This is the basis for summing "
                "amplifiers and audio mixers."
            ),
            "key_params": [
                ("Gain", "Av = −Rf / Rin"),
                ("Input impedance", "= Rin  (not the op-amp's Zin!)"),
                ("Output phase", "Inverted (180°)"),
                ("Noise gain", "1 + Rf/Rin  (higher than |signal gain| by 1)"),
            ],
            "formula": (
                "Vout = −(Rf / Rin) × Vin\n\n"
                "Input impedance:  Zin = Rin\n\n"
                "For summing:  Vout = −Rf × (V1/R1 + V2/R2 + V3/R3 + ...)\n\n"
                "Bandwidth:  BW = GBW / (1 + Rf/Rin)"
            ),
            "usage": [
                "Precision gain with defined input impedance.",
                "Audio mixing / summing amplifier.",
                "Signal inversion.",
                "Weighted signal combination.",
            ],
            "real_examples": [
                "Audio mixer: 4 channels into one inverting summing node, Rf = 10k, R_in each = 10k.",
                "DAC I-to-V: current-output DAC feeds virtual ground through Rf.",
                "Signal inverter: Rf = Rin = 10k for unity-gain inversion.",
            ],
            "design_notes": (
                "• Rin sets the load on the source — choose it high enough not to load the source.\n"
                "• Virtual ground is only valid within the op-amp's bandwidth/slew range.\n"
                "• For very high gain, Rin becomes small → loads the source significantly.\n"
                "• The noise gain (1 + Rf/Rin) is always 1 higher than |Av|."
            ),
            "waveform": {
                "kind": "inverting_amp",
                "params": {"gain": -3, "f_input": 1000},
            },
        },
        "Summing Amplifier (Inverting Summer)": {
            "icon": "➕",
            "summary": (
                "The summing amplifier extends the inverting configuration: several inputs each "
                "feed the op-amp’s inverting node through their own resistor.  The node stays at "
                "virtual ground, so currents add algebraically.\n\n"
                "Output is a weighted sum (inverted): each channel’s contribution scales as "
                "Rf/Rk.  Equal input resistors give equal weighting — the classic audio mixer "
                "starting point.  Different Rk set channel gains or pan laws.\n\n"
                "A non-inverting summer is also possible (resistor network to V+), but the "
                "inverting summer is simpler to analyze and keeps channels isolated from each "
                "other at the summing node."
            ),
            "key_params": [
                ("Weights", "Channel gain ∝ Rf/Rk"),
                ("Polarity", "Output is inverted — add an extra inverter if you need positive sum"),
                ("Headroom", "Clip when any branch saturates the op-amp output"),
            ],
            "formula": (
                "General inverting summer:\n"
                "    Vout = −Rf · (V1/R1 + V2/R2 + V3/R3 + …)\n\n"
                "Equal gains (R1 = R2 = R3 = R):  Vout = −(Rf/R) · (V1 + V2 + V3 + …)\n\n"
                "Average (three inputs): choose Rf = R/3 so Vout = −(V1+V2+V3)/3."
            ),
            "usage": [
                "Analog audio sub-mixers and control-voltage summers.",
                "DAC reference + offset + correction summed into one node.",
                "Bipolar current or voltage summing before a transimpedance or ADC driver.",
            ],
            "real_examples": [
                "Eurorack CV mixer: multiple 100 kΩ inputs, 100 kΩ feedback → unity-weighted inverted sum.",
                "Bipolar current sense: shunt voltages from two legs summed for total load monitoring.",
            ],
            "design_notes": (
                "• Bandwidth is set by noise gain 1 + Rf/Rpar where Rpar is all input resistors in parallel.\n"
                "• For DC precision, bias the non-inverting pin with the Thevenin equivalent of the "
                "summing node resistor network.\n"
                "• Crosstalk in mixers often comes from supply bounce, not the ideal summing node."
            ),
            "waveform": {
                "kind": "summing_amp",
                "params": {
                    "Rf": 10e3,
                    "R1": 10e3,
                    "R2": 10e3,
                    "R3": 20e3,
                    "f1": 320,
                    "f2": 880,
                    "f3": 320,
                },
            },
        },
        "Non-Inverting Summer": {
            "icon": "⊕",
            "summary": (
                "A non-inverting summer combines several voltages at the op-amp’s non-inverting "
                "node through a resistor network, then closes the loop so V− tracks V+.  Unlike "
                "the inverting summer, inputs are not tied to virtual ground — interaction "
                "between sources is set by the network, so design the divider and feedback "
                "carefully.\n\n"
                "With a symmetric three-resistor star (two inputs plus a resistor to ground), "
                "V+ becomes a weighted average of the inputs.  The following non-inverting gain "
                "stage scales that average to the desired output range.\n\n"
                "Trade-off: input impedance is not as cleanly ‘one resistor per channel’ as the "
                "inverting mixer node, but you keep the same polarity as each input."
            ),
            "key_params": [
                ("Weights", "Set by input and grounding resistors at V+"),
                ("Gain", "Additional (1 + Rf/Rg) after the averaging network"),
                ("Interaction", "Sources see each other through the network — simulate"),
            ],
            "formula": (
                "Example: two inputs through R1 and R2 to V+, R3 from V+ to ground.\n"
                "    V+ = (V1/R1 + V2/R2) / (1/R1 + 1/R2 + 1/R3)\n\n"
                "Then with feedback divider to V−:\n"
                "    Vout = (1 + Rf/Rg) · V+\n\n"
                "Match the Thevenin impedance seen by V+ with the impedance at V− for low "
                "bias-current error when required."
            ),
            "usage": [
                "Audio ‘passive mixer’ into a non-inverting gain block.",
                "Adding a DC bias and AC signal at V+ without an extra inverter.",
            ],
            "real_examples": [
                "Reference plus sensor AC coupled into one non-inverting front-end.",
            ],
            "design_notes": (
                "• SPICE every combination of source impedance — the network loads sources.\n"
                "• For many inputs, the inverting summer is often simpler."
            ),
            "waveform": {
                "kind": "noninv_summer",
                "params": {"f1": 360, "f2": 1020, "gain": 1.9, "w1": 0.5},
            },
        },
        "Voltage-Output DAC Buffer & Scaling": {
            "icon": "🎛",
            "summary": (
                "Voltage-output DACs (string, R–2R, or MDAC) present a stepped waveform whose "
                "code-to-code glitch energy and output resistance depend on architecture.  An "
                "op-amp in follower or non-inverting configuration buffers the ladder so the "
                "next stage (filter, line driver, SAR ADC) does not load the resistors and "
                "corrupt linearity.\n\n"
                "Scaling uses gain > 1 when the DAC span is smaller than the desired output "
                "swing; offset can be injected at V+ or via a reference pin.  Current-output "
                "DACs instead use a transimpedance (virtual-ground) stage — see the TIA topic.\n\n"
                "Watch slew rate and settling to the next LSB for fast waveform generation."
            ),
            "key_params": [
                ("Settling", "To ±½ LSB within sample period"),
                ("Glitch impulse", "Mid-code major carries worst — some DACs have deglitchers"),
                ("Noise gain", "Same as closed-loop gain for voltage buffer/gain"),
            ],
            "formula": (
                "Buffered output:  Vload ≈ G · Vdac  (G = 1 for follower).\n\n"
                "Noise / bandwidth: use GBW ≫ (effective noise gain) × signal bandwidth."
            ),
            "usage": [
                "Arbitrary waveform generator output conditioning.",
                "Precision bipolar voltage sourcing after a multiplying DAC.",
            ],
            "real_examples": [
                "OPA350 after 12-bit string DAC into 2-pole reconstruction filter.",
            ],
            "design_notes": (
                "• Place the reconstruction filter after the buffer if the DAC output is noisy.\n"
                "• For high-speed DACs, use parts characterized for ‘DAC buffer’ applications."
            ),
            "waveform": {
                "kind": "dac_buffer_concept",
                "params": {"f_sig": 130, "nbits": 4},
            },
        },
        "Differential Amplifier": {
            "icon": "⚖",
            "summary": (
                "The differential amplifier amplifies the DIFFERENCE between two inputs while "
                "rejecting what is COMMON to both (common-mode rejection).  It uses four resistors "
                "in a bridge-like configuration around a single op-amp.\n\n"
                "For the basic single-op-amp version with matched resistors (R1=R3, R2=R4):\n"
                "    Vout = (R2/R1)(V2 − V1)\n\n"
                "This is the foundation of current sensing (measuring voltage across a shunt), "
                "bridge sensor interfacing, and noise rejection in differential signaling.\n\n"
                "For higher performance (better CMRR, higher input impedance), use an "
                "instrumentation amplifier (3 op-amps: two buffers + one diff amp)."
            ),
            "key_params": [
                ("Differential gain", "Ad = R2/R1  (matched)"),
                ("CMRR", "Depends critically on resistor matching"),
                ("Input impedance", "Finite (R1 and R3 on each input)"),
            ],
            "formula": (
                "With matched ratios R1=R3, R2=R4:\n"
                "    Vout = (R2/R1) × (V2 − V1)\n\n"
                "CMRR degradation from 1% mismatch:\n"
                "    CMRR ≈ 20·log₁₀(Ad / tolerance) ≈ 20·log₁₀(1/0.01) = 40 dB\n\n"
                "For 0.01% resistors: CMRR ≈ 80 dB.\n\n"
                "Instrumentation amp (INA): Av = 1 + 2R/R_gain."
            ),
            "usage": [
                "Current sensing across a shunt resistor.",
                "Wheatstone bridge sensor readout.",
                "Differential-to-single-ended conversion.",
                "Noise rejection in long cable runs.",
            ],
            "real_examples": [
                "Current monitor: INA219 measures voltage across 0.1 Ω shunt → calculates current.",
                "Load cell amplifier: INA125 instrumentation amp with built-in reference.",
                "Audio balanced input: diff amp converts balanced XLR to single-ended.",
            ],
            "design_notes": (
                "• Use 0.01 % matched resistor networks for high CMRR.\n"
                "• For high-side current sensing, use dedicated high-side sense amps (INA180, etc.).\n"
                "• Single-op-amp diff amp has limited input impedance — use INA for high-Z sources.\n"
                "• Mismatch between R1/R3 or R2/R4 directly degrades CMRR."
            ),
            "waveform": {
                "kind": "diff_amp",
                "params": {"gain": 2, "f_input": 500},
            },
        },
    },
    "Math / Signal Processing": {
        "__meta__": {
            "icon": "🧮",
            "summary": (
                "Op-amps can directly perform analog mathematical operations: integration, "
                "differentiation, summation, subtraction, and logarithmic/exponential functions.  "
                "These are the building blocks of analog computers, PID controllers, and active "
                "filter internals."
            ),
        },
        "Integrator": {
            "icon": "∫",
            "summary": (
                "An op-amp integrator replaces the feedback resistor with a capacitor.  "
                "The output is proportional to the time integral of the input voltage.\n\n"
                "With a constant input voltage Vin, the output ramps linearly:\n"
                "    Vout(t) = −(1/RC) × Vin × t\n\n"
                "For a sinusoidal input, integration shifts phase by −90° and reduces amplitude "
                "proportionally to 1/ω — making the integrator act like a low-pass filter with "
                "−20 dB/decade slope and 90° phase shift at all frequencies.\n\n"
                "Practical integrators add a large feedback resistor Rf in parallel with C to "
                "provide a DC path and prevent output saturation from input offset current.  "
                "This limits the integrator's low-frequency gain to −Rf/Rin."
            ),
            "key_params": [
                ("Gain vs frequency", "|H(jω)| = 1/(ωRC)  — drops 20 dB/decade"),
                ("Phase", "−90° (constant, ideal)"),
                ("Unity gain frequency", "f_unity = 1/(2πRC)"),
                ("DC gain (practical)", "−Rf/Rin  (with feedback resistor Rf)"),
            ],
            "formula": (
                "Ideal integrator:\n"
                "    Vout(t) = −(1/RC) ∫₀ᵗ Vin(τ) dτ  +  Vout(0)\n\n"
                "Transfer function:\n"
                "    H(s) = −1/(sRC)\n"
                "    |H(jω)| = 1/(ωRC)\n\n"
                "Unity-gain crossover:  ω₁ = 1/(RC)  →  f₁ = 1/(2πRC)\n\n"
                "Practical (with Rf across C):\n"
                "    H(s) = −Rf / (Rin × (1 + sRfC))\n"
                "    DC gain = −Rf/Rin\n"
                "    Integration behavior above f = 1/(2πRfC)"
            ),
            "usage": [
                "Integral (I) term in analog PID controllers.",
                "Ramp generators from square wave input.",
                "Active filter building block (state-variable internal).",
                "Analog computation (e.g., velocity from acceleration).",
                "Charge amplifiers for piezoelectric sensors.",
            ],
            "real_examples": [
                "Analog PID: integrator with R = 10k, C = 1µF → unity-gain at 15.9 Hz.",
                "Triangle wave generator: integrator fed by square wave from a comparator.",
                "Charge amp: OPA128 with 100 pF feedback for piezo sensor.",
            ],
            "design_notes": (
                "• ALWAYS add a feedback resistor (Rf) to limit DC gain and prevent saturation.\n"
                "• Input offset voltage × Rf/Rin = steady-state output offset.\n"
                "• Low-bias-current op-amps (FET input) are preferred.\n"
                "• Reset switch (analog switch across C) is common for periodic resetting."
            ),
            "waveform": {
                "kind": "integrator",
                "params": {"R": 10e3, "C": 100e-9, "f_input": 1000},
            },
        },
        "Differentiator": {
            "icon": "d/dt",
            "summary": (
                "An op-amp differentiator uses a capacitor at the input and a resistor in "
                "feedback.  The output is proportional to the rate of change (derivative) of "
                "the input voltage.\n\n"
                "For a ramp input, the output is a constant.  For a sine wave, the output is "
                "a cosine (90° phase lead) with amplitude proportional to frequency.\n\n"
                "The gain INCREASES at +20 dB/decade — this means high-frequency noise is "
                "severely amplified.  Therefore, practical differentiators ALWAYS include a "
                "series resistor (Rs) with the input capacitor and/or a capacitor (Cf) across "
                "the feedback resistor to limit the high-frequency gain.\n\n"
                "The result is a differentiator that works within a useful band and becomes "
                "flat or rolls off above a chosen frequency."
            ),
            "key_params": [
                ("Gain vs frequency", "|H(jω)| = ωRC  — rises 20 dB/decade"),
                ("Phase", "+90° (ideal, constant)"),
                ("Unity gain frequency", "f_unity = 1/(2πRC)"),
                ("Max useful frequency", "Limited by Rs or Cf"),
            ],
            "formula": (
                "Ideal differentiator:\n"
                "    Vout(t) = −RC × d(Vin)/dt\n\n"
                "Transfer function:\n"
                "    H(s) = −sRC\n\n"
                "Practical (with series Rs and Cf across Rf):\n"
                "    H(s) = −sRC / ((1+sRsC)(1+sRfCf))\n"
                "    This limits gain above f_max = 1/(2πRsC)."
            ),
            "usage": [
                "Edge / transition detection in waveforms.",
                "Derivative (D) term in analog PID controllers.",
                "Rate-of-change measurement (e.g., dT/dt for thermal runaway detection).",
                "Pulse generation from slow edges.",
            ],
            "real_examples": [
                "PID controller D-term: R = 100k, C = 10nF → unity at 159 Hz.",
                "Transition detector: outputs a spike at each rising/falling edge.",
            ],
            "design_notes": (
                "• NEVER build an ideal differentiator — it will oscillate from noise.\n"
                "• Add Rs ≈ Rf/10 in series with C to limit gain at high frequency.\n"
                "• Op-amp phase shift + differentiator's +90° can cause instability.\n"
                "• Keep the unity-gain crossover well below the op-amp's GBW."
            ),
            "waveform": {
                "kind": "differentiator",
                "params": {"R": 10e3, "C": 10e-9, "f_input": 5000},
            },
        },
    },
    "Comparators / Detectors": {
        "__meta__": {
            "icon": "⚡",
            "summary": (
                "These circuits make DECISIONS or CAPTURE signal properties rather than linearly "
                "amplifying.  Comparators use open-loop (or positive-feedback) op-amp behavior.  "
                "Detectors use diode-feedback techniques to measure peak, envelope, or absolute value."
            ),
        },
        "Comparator": {
            "icon": "⬆⬇",
            "summary": (
                "A comparator outputs one of two states (high or low rail) depending on which "
                "input is larger.  It operates in OPEN LOOP or with POSITIVE feedback — NOT "
                "the negative feedback used in linear amplifiers.\n\n"
                "When V+ > V−: output → V_OH (high)\n"
                "When V+ < V−: output → V_OL (low)\n\n"
                "Dedicated comparator ICs (LM311, LM339, TLV3501) are optimized for this: "
                "fast switching, rail-to-rail output, open-drain outputs.  Using a general op-amp "
                "as a comparator is possible but NOT recommended — op-amps have slow recovery "
                "from saturation and may latch up."
            ),
            "key_params": [
                ("Propagation delay", "Nanoseconds (dedicated) to microseconds (op-amp)"),
                ("Output type", "Push-pull, open-drain, or open-collector"),
                ("Input offset", "Determines minimum detectable difference"),
                ("Hysteresis", "None (basic) — add external for noise immunity"),
            ],
            "formula": (
                "Basic threshold:\n"
                "    Vout = V_OH   if  V+ > V−\n"
                "    Vout = V_OL   if  V+ < V−\n\n"
                "With voltage divider threshold:\n"
                "    V_threshold = Vref × R2/(R1+R2)\n\n"
                "Propagation delay = time from input crossing to output switching."
            ),
            "usage": [
                "Over-voltage / under-voltage detection.",
                "Zero-crossing detection for AC sync.",
                "PWM generation (triangle vs. reference).",
                "ADC flash converter (array of comparators).",
            ],
            "real_examples": [
                "Battery monitor: LM339 compares battery voltage vs. 3.0V reference.",
                "PWM controller: triangle wave vs. error amplifier output → PWM pulses.",
                "Flash ADC: 255 comparators for 8-bit conversion at GHz speeds.",
            ],
            "design_notes": (
                "• DO NOT use a standard op-amp as a comparator in new designs.\n"
                "• Add hysteresis (positive feedback) to avoid oscillation at threshold.\n"
                "• Open-drain outputs need an external pull-up resistor.\n"
                "• Bypass the supply pins close to the comparator IC."
            ),
            "waveform": {
                "kind": "comparator",
                "params": {"V_threshold": 0, "f_input": 200},
            },
        },
        "Schmitt Trigger": {
            "icon": "🔲",
            "summary": (
                "A Schmitt trigger is a comparator with HYSTERESIS — it has TWO thresholds: "
                "a higher one for the rising edge (V_TH) and a lower one for the falling edge "
                "(V_TL).  The output only changes state when the input crosses the appropriate "
                "threshold.\n\n"
                "This prevents chattering (rapid toggling) when the input hovers near a single "
                "threshold.  The hysteresis band (V_TH − V_TL) determines noise immunity.\n\n"
                "Implementation: positive feedback from output to non-inverting input via a "
                "resistor divider.  When output is high, V+ is pulled up → higher threshold "
                "needed to switch.  When output is low, V+ is pulled down → lower threshold."
            ),
            "key_params": [
                ("Upper threshold", "V_TH"),
                ("Lower threshold", "V_TL"),
                ("Hysteresis", "V_hyst = V_TH − V_TL"),
                ("Noise immunity", "Signal noise < V_hyst won't cause false triggers"),
            ],
            "formula": (
                "Inverting Schmitt trigger (input to V−):\n"
                "    V_TH = Vref + (V_OH − Vref) × R1/(R1+R2)\n"
                "    V_TL = Vref + (V_OL − Vref) × R1/(R1+R2)\n"
                "    V_hyst = (V_OH − V_OL) × R1/(R1+R2)\n\n"
                "For symmetric thresholds around 0V with ±Vsat output:\n"
                "    V_TH = +Vsat × R1/(R1+R2)\n"
                "    V_TL = −Vsat × R1/(R1+R2)"
            ),
            "usage": [
                "Cleaning noisy digital signals.",
                "Switch debouncing.",
                "Square-wave generation from sine/triangle input.",
                "Level detection with noise immunity.",
            ],
            "real_examples": [
                "74HC14 hex Schmitt-trigger inverter — used everywhere for signal cleanup.",
                "Thermostat: hysteresis prevents rapid on/off cycling of heater.",
                "Light sensor trigger: Schmitt trigger prevents flickering at dawn/dusk.",
            ],
            "design_notes": (
                "• Choose hysteresis band wider than expected noise amplitude.\n"
                "• Too much hysteresis reduces sensitivity to genuine small signals.\n"
                "• Schmitt triggers are used inside almost all digital input buffers.\n"
                "• Can be combined with RC timing to make a relaxation oscillator."
            ),
            "waveform": {
                "kind": "schmitt",
                "params": {"V_TH": 1.0, "V_TL": -1.0, "f_input": 100},
            },
        },
        "Peak Detector": {
            "icon": "📊",
            "summary": (
                "A peak detector captures and HOLDS the maximum (or minimum) value of an input "
                "waveform.  The basic circuit uses an op-amp driving a diode into a hold capacitor, "
                "with a buffer op-amp reading the capacitor voltage.\n\n"
                "When Vin > Vcap: the op-amp output goes positive, the diode conducts, and the "
                "capacitor charges up to the new peak.  When Vin < Vcap: the diode is reverse-biased, "
                "and the capacitor holds its voltage (ideally).\n\n"
                "In practice, the hold capacitor slowly discharges due to:\n"
                "  • Diode leakage current\n"
                "  • Buffer op-amp input bias current\n"
                "  • Capacitor self-leakage\n\n"
                "The DROOP RATE dV/dt ≈ I_leak / C_hold determines how long the peak is valid.  "
                "Larger C gives slower droop but slower acquisition (the op-amp must charge C "
                "through the diode, limited by slew rate and output current)."
            ),
            "key_params": [
                ("Acquisition time", "Time to capture a new peak to specified accuracy"),
                ("Droop rate", "dV/dt = I_leak / C_hold  [V/s]"),
                ("Diode error", "Eliminated by placing diode inside op-amp feedback loop"),
                ("Hold capacitor", "Tradeoff: speed vs. droop"),
            ],
            "formula": (
                "Ideal behavior:\n"
                "    Vout = max(Vin)   over the hold period\n\n"
                "Droop rate:\n"
                "    dV/dt = −I_leak / C_hold\n\n"
                "Acquisition time (approximate):\n"
                "    t_acq ≈ C_hold × ΔV / I_out_max\n\n"
                "Example: C = 10 nF, I_leak = 1 nA → droop = 0.1 V/s.\n"
                "Example: C = 10 nF, ΔV = 5V, I_out = 20 mA → t_acq = 2.5 µs."
            ),
            "usage": [
                "Audio peak meters (VU meters).",
                "Envelope detection for AM demodulation.",
                "Peak capture before slow ADC sampling.",
                "Vibration peak monitoring.",
                "Sample-and-hold front ends (variant).",
            ],
            "real_examples": [
                "Audio level meter: LF398 S/H + peak detect, C = 1 nF, update every 10 ms.",
                "Ultrasonic receiver: peak detector captures echo amplitude for range calculation.",
                "Power quality monitor: captures peak line voltage each cycle.",
            ],
            "design_notes": (
                "• Use a FET-input op-amp for the buffer to minimize bias current droop.\n"
                "• Place the diode INSIDE the feedback loop to cancel its forward drop.\n"
                "• Add a reset switch (MOSFET) across C to discharge between measurements.\n"
                "• For fast signals, use a Schottky diode for lower capacitance."
            ),
            "waveform": {
                "kind": "peak_detector",
                "params": {"f_input": 200, "decay_tau": 0.02},
            },
        },
        "Precision Rectifier": {
            "icon": "➡️",
            "summary": (
                "A precision rectifier (also called a super diode) uses an op-amp with a diode "
                "in the feedback loop to rectify signals accurately down to millivolt levels — "
                "far below the normal diode forward voltage drop (~0.6V).\n\n"
                "In a basic half-wave precision rectifier, the op-amp drives the diode.  When "
                "Vin > 0, the op-amp output swings positive, the diode conducts, and Vout follows "
                "Vin.  The op-amp's gain 'cancels' the diode drop.  When Vin < 0, the diode is "
                "off and Vout = 0.\n\n"
                "Full-wave precision rectifiers (absolute value circuits) use two op-amps or an "
                "op-amp + resistor network to produce |Vin| as output."
            ),
            "key_params": [
                ("Accuracy", "Diode drop is divided by open-loop gain → negligible error"),
                ("Speed", "Limited by op-amp slew rate and diode recovery"),
                ("Effective forward drop", "~Vd / Aol ≈ 0.6V / 100000 ≈ 6 µV"),
            ],
            "formula": (
                "Half-wave precision rectifier:\n"
                "    Vout = Vin        when Vin > 0\n"
                "    Vout = 0          when Vin < 0\n\n"
                "Full-wave (absolute value):\n"
                "    Vout = |Vin|\n\n"
                "The effective error is reduced by the loop gain:\n"
                "    V_error ≈ V_diode / A_open_loop"
            ),
            "usage": [
                "Precision AC-to-DC conversion for measurement.",
                "Demodulation of AM signals.",
                "Absolute value circuit for control systems.",
                "Low-level AC signal metering.",
            ],
            "real_examples": [
                "True-RMS meter input: precision rectifier + averaging filter.",
                "AM radio detector: precision rectifier for weak-signal demodulation.",
                "Power monitor: rectify AC current sense signal before integration.",
            ],
            "design_notes": (
                "• When the diode is off, the op-amp saturates — recovery time matters.\n"
                "• Use fast op-amps and Schottky diodes for high-frequency signals.\n"
                "• Two-op-amp full-wave designs offer better high-frequency performance.\n"
                "• The AD630 balanced modulator can also serve as a precision rectifier."
            ),
            "waveform": {
                "kind": "precision_rectifier",
                "params": {"f_input": 200},
            },
        },
    },
    "Oscillators / Waveform Gen": {
        "__meta__": {
            "icon": "🌊",
            "summary": (
                "Oscillator circuits use positive feedback and a frequency-selective network to "
                "generate a continuous periodic output.  The Barkhausen criterion requires "
                "loop gain = 1 and loop phase = 0° (or 360°) at the oscillation frequency."
            ),
        },
        "Wien Bridge Oscillator": {
            "icon": "🎵",
            "summary": (
                "The Wien bridge oscillator produces a low-distortion sine wave using a "
                "series-parallel RC network (Wien bridge) as the frequency-selective element.\n\n"
                "The Wien bridge has maximum transmission and zero phase shift at f = 1/(2πRC), "
                "where its gain is exactly 1/3.  The op-amp must provide a gain of exactly 3 "
                "to satisfy the Barkhausen criterion (loop gain = 1).\n\n"
                "Amplitude stabilization is essential: if gain is slightly above 3, the output "
                "grows until clipping; if below 3, oscillation dies.  Classic methods use a "
                "lamp filament (resistance increases with heat) or JFET (resistance controlled "
                "by rectified output) in the gain-setting network.\n\n"
                "The Wien bridge oscillator is the basis of the legendary HP 200A, Hewlett-Packard's "
                "first product (1939), which used a lamp for amplitude stabilization."
            ),
            "key_params": [
                ("Oscillation frequency", "f = 1 / (2π R C)"),
                ("Required gain", "Av = 3  (exactly)"),
                ("Distortion", "Very low with proper AGC — < 0.01 % possible"),
                ("Amplitude control", "Lamp, JFET, or diode-limiting network"),
            ],
            "formula": (
                "Oscillation frequency:\n"
                "    f_osc = 1 / (2π R C)    [for equal R and C]\n\n"
                "Wien bridge transfer function:\n"
                "    H_bridge(s) = sRC / (s²R²C² + 3sRC + 1)\n"
                "    At ω₀ = 1/RC:  |H| = 1/3,  phase = 0°\n\n"
                "Barkhausen: amp gain × bridge gain = 1  →  Av × 1/3 = 1  →  Av = 3.\n"
                "    Av = 1 + R2/R1 = 3  →  R2 = 2·R1."
            ),
            "usage": [
                "Audio test signal generators.",
                "Laboratory sine-wave sources.",
                "Function generator sine-wave section.",
                "Educational demonstration of oscillation principles.",
            ],
            "real_examples": [
                "HP 200A: R = 15.9 kΩ, C = 10 nF → f ≈ 1 kHz sine wave.",
                "Bench audio oscillator: dual-gang potentiometer tunes R for variable frequency.",
            ],
            "design_notes": (
                "• Without AGC, the circuit will either clip or stop oscillating.\n"
                "• A JFET (2N5457) as variable resistor in the gain network works well.\n"
                "• Start-up: gain must be slightly > 3 initially, then AGC brings it to exactly 3.\n"
                "• Use matched R and C pairs for frequency accuracy."
            ),
            "waveform": {
                "kind": "wien_oscillator",
                "params": {"f_osc": 1000},
            },
        },
        "Relaxation Oscillator": {
            "icon": "⏱",
            "summary": (
                "A relaxation oscillator alternates between two states using a capacitor that "
                "charges and discharges between two threshold levels.  The thresholds are set by "
                "a Schmitt trigger (comparator with hysteresis).\n\n"
                "The output is a SQUARE WAVE.  By integrating the square wave (with an RC or "
                "integrator), a TRIANGLE wave can be obtained.\n\n"
                "Operation:\n"
                "1. Capacitor charges through R toward the positive rail.\n"
                "2. When voltage reaches V_TH (upper threshold), output switches low.\n"
                "3. Capacitor discharges through R toward the negative rail.\n"
                "4. When voltage reaches V_TL (lower threshold), output switches high.\n"
                "5. Repeat.\n\n"
                "The 555 timer IC is the most famous relaxation oscillator implementation."
            ),
            "key_params": [
                ("Frequency", "Depends on RC and hysteresis thresholds"),
                ("Output waveform", "Square wave (or triangle with integrator)"),
                ("Duty cycle", "50 % if symmetric thresholds and supply"),
            ],
            "formula": (
                "For symmetric ±V_sat output and thresholds ±V_th:\n"
                "    T = 2RC × ln((V_sat + V_th) / (V_sat − V_th))\n"
                "    f = 1/T\n\n"
                "If V_th ≈ (R1/R2) × V_sat  (from Schmitt divider):\n"
                "    T ≈ 2RC × ln((1 + R1/R2) / (1 − R1/R2))\n\n"
                "555 timer (astable mode):\n"
                "    f = 1.44 / ((R_A + 2·R_B) × C)"
            ),
            "usage": [
                "Simple clock generators.",
                "LED blinkers and timing circuits.",
                "Tone generators (doorbells, alarms).",
                "Triangle / sawtooth wave generation.",
                "PWM signal generation.",
            ],
            "real_examples": [
                "555 astable: RA = 1k, RB = 10k, C = 100nF → f ≈ 685 Hz.",
                "Op-amp relaxation osc: R = 10k, C = 100nF, Schmitt ±2V → ~1 kHz square wave.",
            ],
            "design_notes": (
                "• Frequency stability depends on supply voltage stability and component tolerance.\n"
                "• For precise timing, use crystal oscillators instead.\n"
                "• 555 duty cycle is inherently asymmetric unless modified (diode bypass on RB).\n"
                "• Op-amp slew rate limits maximum frequency."
            ),
            "waveform": {
                "kind": "relaxation_osc",
                "params": {"f_osc": 1000},
            },
        },
    },
    "Special Amplifiers & Converters": {
        "__meta__": {
            "icon": "🔬",
            "summary": (
                "Beyond the four basic gain cells, op-amps appear in precision front-ends that "
                "convert between voltage and current, compress dynamic range, or tune gain under "
                "digital control.  This section also includes charge amplifiers for capacitive "
                "sensors, isolation for safety / CMV, and lock-in style synchronous detection.\n\n"
                "Power output stages and discrete RF transistors live under Power Amplifiers and "
                "RF & Discrete."
            ),
        },
        "Instrumentation Amplifier (INA)": {
            "icon": "🎚",
            "summary": (
                "An instrumentation amplifier is a subtractor with buffered inputs.  The classic "
                "INA uses three op-amps: two matched non-inverting gain stages (or followers plus "
                "gain) on each line feeding a difference amplifier.  The differential gain is set "
                "with one resistor Rg, and input impedance on both pins is very high.\n\n"
                "Integrated INAs (AD620, INA128, AD8232,…) laser-trim internal resistors so CMRR "
                "exceeds 100 dB and offset drift is low.  They are the default front-end for "
                "bridge sensors, biopotential electrodes (with right-leg drive variants), and "
                "precision current sense when paired with shunts.\n\n"
                "Compared with a single-op-amp difference amplifier built from four 1 % resistors, "
                "an INA wins on CMRR, drift, and common-mode input range."
            ),
            "key_params": [
                ("Gain", "Av = 1 + 2R/Rg  (classic 3-op-amp form)"),
                ("CMRR", "80–120+ dB typical integrated"),
                ("Supply", "Single or dual; check input common-mode vs rails"),
            ],
            "formula": (
                "3-op-amp INA (typical):\n"
                "    Differential gain of the two input op-amps:  G = 1 + 2R/Rg\n"
                "    With a unity-gain difference stage:  Vout = G × (VIN+ − VIN−) + Vref\n\n"
                "Noise RTI combines both input stages — check current noise with source impedance."
            ),
            "usage": [
                "Strain gauge and load-cell digitizers.",
                "ECG/EEG acquisition after protection networks.",
                "Low-side and high-side current sense (with dedicated high-side parts).",
            ],
            "real_examples": [
                "HX711 breakout: INA-like front-end plus 24-bit ADC for scales.",
                "INA826 + 350 Ω bridge: torque telemetry on a robot joint.",
            ],
            "design_notes": (
                "• Place RC anti-alias and TVS networks before the INA per datasheet.\n"
                "• Keep sense traces Kelvin-connected at the shunt.\n"
                "• REF must bias output into the ADC’s sweet spot — often mid-supply.\n"
                "• RF interference: add 1–10 nF differential caps only if the INA stays stable."
            ),
            "waveform": {
                "kind": "instrumentation_amp",
                "params": {"G": 10, "f_input": 450, "f_common": 40},
            },
        },
        "Transimpedance Amplifier (TIA)": {
            "icon": "💡",
            "summary": (
                "A transimpedance amplifier converts an incoming current (usually from a photodiode "
                "operated in photoconductive or photovoltaic mode) into a proportional output voltage.  "
                "The photodiode dumps current into the inverting node; a feedback resistor Rf sets "
                "V ≈ −I·Rf, often with a small Cf in parallel for stability and bandwidth shaping.\n\n"
                "Dominant pole ≈ 1/(2π·Rf·Cf) in the simplest model.  Noise is set by Rf Johnson noise, "
                "op-amp voltage and current noise, and diode shot noise — NF optimization is a whole "
                "chapter (choose FET-input amps, cool the detector, use bootstrapping).\n\n"
                "The same topology serves electron multipliers, ion chambers, and any current source "
                "that needs a virtual ground."
            ),
            "key_params": [
                ("Transimpedance", "Rf (Ω) at low frequency"),
                ("Bandwidth", "≈ GBW / noise gain for single-pole compensation"),
                ("Stability", "Cf combats input capacitance peaking"),
            ],
            "formula": (
                "Ideal:  Vout = −I_in · Rf\n\n"
                "With feedback capacitor Cf:  Zf = Rf ∥ (1/sCf)\n\n"
                "Noise gain NG = 1 + Cd/Cf (conceptual) — consult photodiode app notes."
            ),
            "usage": [
                "Optical receivers: fiber, LiDAR front-ends, pulse oximetry LED sense path.",
                "Fluorescence and spectroscopy detectors.",
            ],
            "real_examples": [
                "OPA856 + 100 kΩ Rf for fast photodiode ranging at tens of MHz.",
            ],
            "design_notes": (
                "• Solarize the diode with a reverse bias (speed) or run zero-bias (low dark current).\n"
                "• Never omit a stability capacitor if the diode sits remotely.\n"
                "• Guard rings around the summing node cut leakage on high-impedance PCBs."
            ),
            "waveform": {
                "kind": "transimpedance",
                "params": {"Rf": 1e6, "Cf": 2e-12, "f_in": 1200, "I_ac": 35e-9},
            },
        },
        "Howland / Voltage-to-Current Converter": {
            "icon": "🔁",
            "summary": (
                "The Howland current pump turns a voltage command into a load current that is "
                "substantially independent of load impedance (within the op-amp’s compliance range).  "
                "A difference resistor network around one or two op-amps forces I_load ≈ "
                "k · (Vcontrol − Vref).\n\n"
                "Single-op-amp Howlands trade off headroom versus precision; dual versions improve "
                "linearity.  Applications include 4–20 mA industrial loops, LED/stack current "
                "sources, and electrochemical bias supplies.\n\n"
                "Watch power dissipation: the op-amp may sink/source the full load current."
            ),
            "key_params": [
                ("Transconductance", "Set by resistor ratios"),
                ("Compliance", "Limited by supply minus saturation drops"),
                ("Stability", "Capacitive loads may require snubbers or isolation amp"),
            ],
            "formula": (
                "Infinite output resistance (ideal op-amp, classic Howland):\n"
                "    R2/R1 = R4/R3\n\n"
                "With the usual input applied through R1 to the non-inverting path:\n"
                "    I_load ≈ Vctl / R1\n\n"
                "If R1 = R2 = R3 = R4 = R, then I_load ≈ Vctl / R.\n\n"
                "Resistor labels swap between textbooks—verify I vs Vctl with KCL on your exact diagram."
            ),
            "usage": [
                "4–20 mA two-wire transmitters.",
                "Programmable electrochemical polarizers.",
            ],
            "real_examples": [
                "XTR115 loop-powered 4–20 mA chip embeds a Howland-like core.",
            ],
            "design_notes": (
                "• Use 0.05 % resistors or trim for accurate scaling.\n"
                "• Include a realistic load model when simulating loop phase margin."
            ),
            "waveform": {
                "kind": "howland_concept",
                "params": {"R_sense": 1000, "f_input": 400},
            },
        },
        "Log Amplifier": {
            "icon": "📉",
            "summary": (
                "A log amplifier exploits the exponential I–V of a diode or transistor inside the "
                "feedback path so that output voltage grows roughly as the logarithm of input "
                "amplitude.  That compresses decades of dynamic range onto a single op-amp output "
                "for measurement, AGC sensing, or multiplication (log + add + antilog).\n\n"
                "Temperature compensation (second matched transistor, heater, or ratiometric "
                "scheme) is mandatory because Is and Vt drift.  Practical circuits bias the diode "
                "into its safe region and clamp overrange inputs.\n\n"
                "Dedicated log amps (AD8304,…) integrate matched dies for logging RF power."
            ),
            "key_params": [
                ("Slope", "~k·Vt per decade (temperature sensitive)"),
                ("Dynamic range", "60–100 dB practical in multi-stage log amps"),
            ],
            "formula": (
                "Ideal diode:  I = Is·(exp(V/Vt) − 1)\n"
                "Invert:  V ≈ Vt·ln(I/Is + 1)\n\n"
                "Single-op-amp log: output proportional to −ln(Vin/R + Iref)."
            ),
            "usage": [
                "Wide-dynamic-range photometry and spectroscopy.",
                "RSSI / power metering before ADC.",
            ],
            "real_examples": [
                "AD8307 log detector for RF power down to −80 dBm class.",
            ],
            "design_notes": (
                "• Clamp inputs before the sensitive junction avalanches.\n"
                "• Pair with an identical transistor on-chip for temperature tracking."
            ),
            "waveform": {
                "kind": "log_amp_concept",
                "params": {"Vt": 0.026, "I0": 1e-3},
            },
        },
        "Antilog (Exponential) Amplifier": {
            "icon": "📈",
            "summary": (
                "The antilog is the inverse operator: output voltage or current rises exponentially "
                "with a control input.  Implementations place the exponential device on the input "
                "side and use feedback to linearize the closed loop, or rely on a Gilbert cell in "
                "multiplier ICs.\n\n"
                "Together with a log stage and a summer, you obtain an analog multiplier (log a + "
                "log b = log(ab)).\n\n"
                "Voltage-controlled exponential VCOs reuse the same physics."
            ),
            "key_params": [
                ("Exponent", "Matches device law — temperature compensation mirrors the log cousin"),
            ],
            "formula": (
                "Idealized device law:  I = I₀ exp(Vctrl / Vₜ)  (Vₜ ≈ kT/q for a junction).\n\n"
                "If Vctrl ∝ ln(x), then I ∝ x — analog multipliers sum log-domain voltages, then antilog."
            ),
            "usage": [
                "Analog multipliers and true analog RMS converters.",
                "AGC with exponential gain control law.",
            ],
            "real_examples": [
                "AD633 four-quadrant multiplier block diagrams include implicit antilog stages.",
            ],
            "design_notes": (
                "• Simulate with full temperature corners — exponent moves quickly."
            ),
            "waveform": {
                "kind": "antilog_concept",
                "params": {"Vt": 0.026, "v_span": 0.12},
            },
        },
        "Programmable-Gain Amplifier (PGA)": {
            "icon": "🔢",
            "summary": (
                "PGAs switch precision resistor ratios (CMOS transmission gates, MUXes, or relay "
                "networks) so one signal path can hop between discrete gains under MCU or DSP "
                "control.  Integrated PGAs (PGA112, LTC6910,…) reduce leakage and glitch energy.\n\n"
                "Key metrics: gain step accuracy, settling time after a code change, bandwidth "
                "and noise at each gain, and charge injection that shows as a glitch.\n\n"
                "Multiplexed-channel PGAs also perform input selection — study crosstalk and fault "
                "protection for your sensor harness."
            ),
            "key_params": [
                ("Gain steps", "Often 1·2ⁿ or decade sequence (1, 10, 100,…)"),
                ("Bandwidth", "Shrinks at highest gain (noise gain ↑)"),
            ],
            "formula": (
                "Each digital code selects a feedback network — effective voltage gain is discrete:\n"
                "    Vout = Av[n] · Vin,   n = 0…N−1\n\n"
                "Av[n] is a datasheet table (often 1, 2, 4, … or decade steps); verify offset and "
                "settling at every code."
            ),
            "usage": [
                "Multirange DMM front-ends.",
                "Sensor autosranging before Σ-Δ ADC.",
            ],
            "real_examples": [
                "ADS125H01 integrated ADC + PGA for industrial 0–10 V / ±10 V sensing.",
            ],
            "design_notes": (
                "• Insert RC anti-alias ahead of the PGA if aliasing is a concern.\n"
                "• Soft-step gain changes remove audible glitches in audio-grade PGAs."
            ),
            "waveform": {
                "kind": "pga_concept",
                "params": {"f_input": 900, "gains": [1, 4, 16, 8, 2], "segment_ms": 0.65},
            },
        },
        "Fully Differential Amplifier (FDA)": {
            "icon": "⬌",
            "summary": (
                "FDA ICs are designed to drive SAR and pipeline ADCs that need symmetrical swing "
                "around a VOCM reference.  One diff pair senses the inputs; outputs are true "
                "complementary pins with common-mode servo loops keeping VOCM centered.\n\n"
                "Passive anti-alias filters often straddle the FDA because both legs must stay "
                "balanced — layout symmetry is part of the spec.\n\n"
                "Examples: THS4551, LTC6363, ADA4945 family."
            ),
            "key_params": [
                ("VOCM", "Sets output common point — tie to ADC reference"),
                ("Noise gain", "Matches FDA app note for filter component de-normalization"),
            ],
            "formula": (
                "Fully differential small signal (symmetric feedback):\n"
                "    VOUT+ − VOUT− ≈ G · (VIN+ − VIN−)\n\n"
                "Common-mode output is set by VOCM (often servo’d to ADC VREF): both outputs swing "
                "around VOCM.  Match R networks on each side for good CMRR and even harmonic rejection."
            ),
            "usage": [
                "Single-ended-to-differential conversion before high-speed ADC.",
                "Active anti-alias with balanced outputs.",
            ],
            "real_examples": [
                "14-bit 10 MSPS SAR: ADA4940-1 between transformer and ADS7949 inputs.",
            ],
            "design_notes": (
                "• Run ac / noise simulations in fully differential mode — do not ground one output.\n"
                "• VOCM bandwidth must support the ADC’s input sample glitch."
            ),
            "waveform": {
                "kind": "fda_concept",
                "params": {"vocm": 2.5, "gain_db": 12, "f_input": 2.5e6, "v_diff_pk": 0.055},
            },
        },
        "Variable-Gain Amplifier (VGA / AGC Core)": {
            "icon": "📻",
            "summary": (
                "VGAs provide continuous or stepped gain control from a dc control voltage, "
                "current, or digital word.  OTAs, multiplier cores, and pin-diode attenuators all "
                "appear depending on bandwidth.\n\n"
                "Automatic gain control loops servo the VGA so nominal output level stays constant "
                "despite fading channels — classic in RF IF strips and optical burst receivers."
            ),
            "key_params": [
                ("Gain range", "Often quoted in dB with NF vs gain curves"),
                ("Control bandwidth", "How fast gain may slew without ringing the loop"),
            ],
            "formula": (
                "Linear-in-dB VGAs approximate:  G(Vctl) = G0 · exp(α·Vctl)."
            ),
            "usage": [
                "LTE/5G receivers, ultrasound TGC amplifiers.",
                "Fiber burst-mode receivers.",
            ],
            "real_examples": [
                "AD8367 IF VGA with logarithmic gain control interface.",
            ],
            "design_notes": (
                "• Match VGA output compression point to ADC full scale with margin."
            ),
            "waveform": {
                "kind": "vga_concept",
                "params": {"f_input": 2500, "G0": 0.55, "alpha": 2.2},
            },
        },
        "Chopper & Autozero Amplifiers": {
            "icon": "♻",
            "summary": (
                "Chopper-stabilized and autozero amplifiers periodically null input offset and 1/f "
                "noise by sampling the error on input capacitors or flipping input switches.  The "
                "result is microvolt offsets and flat noise density near DC — invaluable for "
                "thermocouple, bridge, and shunt sensing.\n\n"
                "Side effects include switching ripple at the chop frequency (typically tens of kHz) "
                "and slightly limited large-signal bandwidth — always read the alias and ripple "
                "plots.\n\n"
                "Many precision parts blend chopping with autozero (ADA4522, LTC2057,…)."
            ),
            "key_params": [
                ("Offset", "< 5 µV typical"),
                ("Ripple frequency", "Multiple of internal clock"),
                ("GBW", "Often moderate — not GHz parts"),
            ],
            "formula": (
                "Conceptually:  Vout = Av·(Vdiff + ε); sampler estimates ε and subtracts."
            ),
            "usage": [
                "Portable instrumentation, weigh scales, battery stack monitoring.",
            ],
            "real_examples": [
                "ADS1232 24-bit bridge ADC integrates a chopper front-end.",
            ],
            "design_notes": (
                "• Add RC filtering only if recommended — wrong caps can destabilize the null loop.\n"
                "• Layout return currents from charge injection away from sense nodes."
            ),
            "waveform": {
                "kind": "chopper_concept",
                "params": {"f_input": 25, "f_chop": 6000, "Av": 80, "ripple_frac": 0.012},
            },
        },
        "Charge Amplifier (Piezo / Capacitive Sensor)": {
            "icon": "⚡",
            "summary": (
                "A charge amplifier (often called a charge-sensitive or ‘piezo’ preamp) integrates "
                "sensor charge onto a feedback capacitor Cf so the output voltage represents "
                "charge: ΔV ≈ ΔQ/Cf.  A large feedback resistor Rf bleeds DC so the op-amp does "
                "not saturate from bias currents, forming a lower cutoff with Cf.\n\n"
                "Used with piezoelectric accelerometers, hydrophones, capacitive touch / pressure "
                "sensors, and radiation detectors where the sensor looks predominantly capacitive.\n\n"
                "Cable capacitance appears in parallel with the sensor — the closed-loop "
                "transimpedance-like action reduces its effect versus a bare voltage amplifier."
            ),
            "key_params": [
                ("Sensitivity", "Vout per pC set by Cf"),
                ("Low-frequency cutoff", "≈ 1/(2π Rf Cf)"),
                ("Noise", "Op-amp voltage noise and Rf Johnson noise at the summing node"),
            ],
            "formula": (
                "Ideal:  Vout = −Q_sensor / Cf\n\n"
                "With Rf || Cf: high-pass with corner  fc = 1/(2π Rf Cf).\n\n"
                "Equivalent noise bandwidth grows if Cf is too small — trade sensitivity vs noise."
            ),
            "usage": [
                "IEPE/ICP accelerometer conditioning (sometimes combined with constant-current bias).",
                "MEMS microphone front-ends, capacitive displacement probes.",
            ],
            "real_examples": [
                "ADXL100x family evaluation boards: charge amp or CVC stage before ADC.",
            ],
            "design_notes": (
                "• Use FET-input, low-bias-current op-amps; guard the input node.\n"
                "• Long cables add C — recalculate noise and phase margin.\n"
                "• Some sensors need a bias resistor to define DC operating point."
            ),
            "waveform": {
                "kind": "charge_amp_concept",
                "params": {"Cf": 12e-12, "Rf": 50e6},
            },
        },
        "Isolation Amplifier": {
            "icon": "🔒",
            "summary": (
                "Isolation amplifiers transfer an analog signal across a galvanic barrier "
                "(transformer, capacitive coupling, or optical link) so patient, motor drive, or "
                "high-voltage bus electronics cannot create a hazardous ground path.  Rated "
                "working voltage, creepage, and transient immunity are as important as gain "
                "accuracy.\n\n"
                "Sigma-delta modulators digitize on the ‘hot’ side and reconstruct on the safe "
                "side, or AM/FM carriers cross the barrier.  Common-mode rejection of kV/ms "
                "events is a headline specification.\n\n"
                "Do not confuse with a differential amplifier alone — isolation adds the barrier "
                "and limited power crossing (often isolated DC-DC)."
            ),
            "key_params": [
                ("CMVI", "Common-mode voltage immunity rating"),
                ("CMTI", "Common-mode transient immunity kV/µs"),
                ("Barrier capacitance", "Sets leakage and HF feedthrough"),
            ],
            "formula": (
                "Conceptual:  Vout_side2 = G · Vdiff_side1 + ε_barrier(t)\n\n"
                "ε includes ripple from the isolated supply converter and clock feedthrough."
            ),
            "usage": [
                "Motor drive current sense on 400 V bus.",
                "Medical ECG/EEG with patient safety limits.",
                "EV battery-stack voltage monitoring.",
            ],
            "real_examples": [
                "AMC1300 isolated amplifier + shunt on inverter phase leg.",
            ],
            "design_notes": (
                "• Follow clearance/creepage rules for your pollution degree.\n"
                "• Place the shunt and isolation IC on the same ‘hot’ island with Kelvin sense.\n"
                "• Verify lifetime insulation rating vs working voltage."
            ),
            "waveform": {
                "kind": "isolation_amp_concept",
                "params": {"f_sig": 100},
            },
        },
        "Lock-In Amplifier (Synchronous Detection)": {
            "icon": "🎯",
            "summary": (
                "A lock-in amplifier (or lock-in style channel) multiplies the noisy measurement "
                "by a reference tone at the same frequency and phase, then low-passes the product.  "
                "Quadrature (I/Q) demodulation recovers both amplitude and phase versus the "
                "reference.\n\n"
                "The measurement bandwidth becomes that of the output low-pass — not the wide "
                "front-end — so buried small signals can be recovered in high noise.  Used in "
                "scanned probe microscopy, optical chop experiments, impedance spectroscopy, and "
                "precision AC bridges.\n\n"
                "Implementation mixes analog multipliers, switching demodulators, or ADC + DSP."
            ),
            "key_params": [
                ("Reference phase", "Adjust for maximum DC after LPF"),
                ("Time constant", "Output LPF sets bandwidth vs settling"),
                ("Dynamic reserve", "How much noise can be present before overload"),
            ],
            "formula": (
                "If meas(t) ≈ A·cos(ωt+φ) + noise and ref(t) = cos(ωt), then after LPF:\n"
                "    DC component ∝ (A/2) cos φ  (in-phase channel).\n\n"
                "A second channel with ref = sin(ωt) gives the quadrature component for magnitude."
            ),
            "usage": [
                "Nanoscale displacement sensing with modulated optical carriers.",
                "Thin-film conductivity vs small AC bias.",
            ],
            "real_examples": [
                "Stanford SR830 class dual-phase lock-in (lab instrument).",
            ],
            "design_notes": (
                "• Keep reference and signal path group delays matched in wideband systems.\n"
                "• Harmonics of the reference can demodulate wrong tones — filter first.\n"
                "• For rotating machinery, a tach-derived reference replaces a fixed oscillator."
            ),
            "waveform": {
                "kind": "lockin_concept",
                "params": {"f_ref": 380},
            },
        },
    },
    "Power Amplifiers (Classes A–D)": {
        "__meta__": {
            "icon": "🔊",
            "summary": (
                "Power amplifiers move energy into loads (speakers, antennas, motors) with "
                "efficiency and linearity traded by conduction class (A through D) and by supply "
                "tracking (G/H) or multi-branch architectures (Doherty, envelope tracking).  "
                "These topics are conceptual — real designs add bias, thermal management, "
                "protection, and load-pull data."
            ),
        },
        "Class-A Power Amplifier": {
            "icon": "Ⓐ",
            "summary": (
                "Class-A means the output transistor conducts for the entire 360° of the waveform. "
                "Bias sits in the middle of the load line so current never falls to zero.  Linearity "
                "is excellent and harmonic distortion can be very low — at the price of terrible "
                "efficiency (theoretically below 50 percent for a resistive load in the ideal sine case; "
                "real circuits are often worse).\n\n"
                "Heat sinks dominate.  Used when distortion matters more than battery life — "
                "headphone finals, instrumentation stimulus circuits, vintage audio pre-output drivers."
            ),
            "key_params": [
                ("Conduction angle", "360°"),
                ("Efficiency", "Typically a few percent to about 25 percent practical"),
            ],
            "formula": (
                "Ideal max sine efficiency to resistive load is near 50 percent; realistic Class-A stages are lower."
            ),
            "usage": [
                "High-end audio output stages (small power)",
                "Laboratory function-generator output boosters",
            ],
            "real_examples": [
                "Single-ended tube amp output operating purely Class-A",
            ],
            "design_notes": (
                "• Size the heatsink for continuous worst-case dissipation.\n"
                "• Cascode or active loads recover some efficiency tricks without leaving Class-A."
            ),
            "waveform": {"kind": "class_a_concept", "params": {"f": 700, "Av": 0.82, "I_quiescent": 0.45, "I_ac_peak": 0.38}},
        },
        "Class-B & Class-AB Power Amplifier": {
            "icon": "ⒶⒷ",
            "summary": (
                "Class-B pushes and pulls with complementary devices so each conducts roughly half "
                "the cycle (180°).  Zero quiescent current sounds efficient, but crossover distortion "
                "appears near zero crossing.\n\n"
                "Class-AB adds a small idle bias so both devices share a sliver of conduction — "
                "trading a few mA of quiescent current for far smoother crossovers.  Most audio "
                "power amps, motor H-bridge outputs, and line drivers operate here."
            ),
            "key_params": [
                ("Crossover region", "Bias sets behavior — measure THD vs output level"),
                ("Thermal tracking", "Vbe multiplier on heatsink stabilizes idle"),
            ],
            "formula": (
                "Efficiency approaches π/4 (about 78.5 percent) for ideal sine in Class-B; AB sits between A and B."
            ),
            "usage": [
                "Home theater audio power amps",
                "Linear lab supplies output followers",
            ],
            "real_examples": [
                "LM3886 complementary output with AB bias network",
            ],
            "design_notes": (
                "• Respect safe operating area — do not exceed simultaneous Vce·Ic.\n"
                "• Bootstrap caps extend positive swing on low-cost designs."
            ),
            "waveform": {"kind": "class_b_concept", "params": {"f": 900, "V_dead": 0.11, "ab_blend": 0.4}},
        },
        "Class-C Power Amplifier": {
            "icon": "Ⓒ",
            "summary": (
                "Class-C conducts less than half the cycle (under 180°), heavily biased near cutoff. "
                "Current pulses excite a tuned (LC) load so the fundamental is reconstructed — "
                "efficiency is high but usable only for constant-envelope RF (CW, FM, some FSK).\n\n"
                "Amplitude information is destroyed unless combined with high-level modulation schemes."
            ),
            "key_params": [
                ("Conduction angle", "Often under 90° for high efficiency"),
                ("Load", "Must be tuned or harmonic shorts waste energy"),
            ],
            "formula": (
                "Collector efficiency can exceed 80 percent in narrowband RF service with proper harmonic loading."
            ),
            "usage": [
                "VHF/UHF FM transmit PA stages",
                "RF induction heating drivers",
            ],
            "real_examples": [
                "HAM radio final with pi-network output",
            ],
            "design_notes": (
                "• Never operate wideband audio Class-C into a speaker — spectrum is awful.\n"
                "• Watch for parametric oscillation with saturated bases."
            ),
            "waveform": {"kind": "class_c_concept", "params": {"f": 2.5e6, "conduction_deg": 70}},
        },
        "Class-D Switching Power Amplifier": {
            "icon": "Ⓓ",
            "summary": (
                "Class-D switches the output rail-to-rail at high frequency with duty cycle "
                "controlled so the average (after an LC reconstruction filter) traces the audio or "
                "baseband waveform.  Theoretical efficiency approaches 100 percent minus switching and "
                "conduction losses.\n\n"
                "Dead-time control prevents shoot-through, spread-spectrum PWM may ease EMI, and "
                "speaker cables become part of the filter unless a fully integrated bridge LC is used."
            ),
            "key_params": [
                ("Switching frequency", "Typically 200 kHz–4 MHz audio, higher for smaller magnetics"),
                ("EMI", "Common-mode currents on supplies and cables"),
            ],
            "formula": (
                "First-order: duty D(t) maps to average Vout ≈ D·Vsupply − (1−D)·Vreturn."
            ),
            "usage": [
                "Smartphone / portable speaker amps",
                "Motor servo PWM output stages",
            ],
            "real_examples": [
                "TI TPA3116 2×50 W bridge Class-D for bookshelf systems",
            ],
            "design_notes": (
                "• Layout gate drives for under 10 ns skew; millimeters matter.\n"
                "• Add snubbers on the bridge nodes per evaluation board guidance."
            ),
            "waveform": {"kind": "class_d_concept", "params": {"f_sig": 1000, "f_sw": 40000}},
        },
        "Class-G & Class-H Power Amplifiers": {
            "icon": "🔋",
            "summary": (
                "Class-G and Class-H improve average efficiency by reducing wasted voltage across "
                "the output devices.  Class-G switches between two (or more) supply rails so the "
                "amplifier draws from a low rail for small signals and taps a higher rail only "
                "when the waveform needs headroom.  Class-H often varies the supply continuously "
                "(or in fine steps) to track the envelope, sometimes called ‘rail tracking’.\n\n"
                "Both approaches add supply-switching complexity, EMI from rail transitions, and "
                "control-loop challenges to avoid crossover artifacts when rails change.\n\n"
                "Common in high-power audio and some linear motor drives where Class-D EMI is "
                "unacceptable but pure Class-AB waste is too high."
            ),
            "key_params": [
                ("Rail count", "Two-rail G vs many-step or tracking H"),
                ("Switching losses", "Balance vs conduction loss in the output stage"),
                ("MUTE / sequencing", "Prevent pops when rails engage"),
            ],
            "formula": (
                "Instantaneous device loss ∝ (Vsupply − Vout) · Iout — lowering effective "
                "Vsupply when |Vout| is small reduces average dissipation."
            ),
            "usage": [
                "Pro audio subwoofer and PA racks.",
                "High-voltage piezo drivers with variable compliance rail.",
            ],
            "real_examples": [
                "Crown DriveCore with multiple internal rails for touring PA.",
            ],
            "design_notes": (
                "• Simulate rail hand-off with real load impedance including cable inductance.\n"
                "• Monitor supply bypass at each rail — switching noise couples to the output."
            ),
            "waveform": {"kind": "class_gh_concept", "params": {"f_sig": 550, "rail_threshold": 0.22}},
        },
        "Doherty, Envelope Tracking & Multi-Branch PAs": {
            "icon": "📡",
            "summary": (
                "Cellular basestations and modern radios need high average efficiency at large "
                "peak-to-average power ratios (PAPR).  A **Doherty** amplifier combines a main "
                "device biased for efficiency with an auxiliary path that ‘helps’ only at high "
                "instantaneous power, modulating the main stage’s load line (load modulation).\n\n"
                "**Envelope tracking (ET)** or envelope elimination and restoration (EER) varies "
                "the drain supply with the signal envelope so the transistor sees minimum excess "
                "voltage.  A wideband DC-DC or hybrid supply modulator must track MHz-scale "
                "envelopes with low delay.\n\n"
                "Digital pre-distortion (DPD) often wraps these analog cores to meet ACPR masks."
            ),
            "key_params": [
                ("Combining network", "Impedance inverter line in classic Doherty"),
                ("Delay matching", "Envelope path vs RF path alignment in ET"),
                ("Backoff", "Efficiency curves are specified vs average output power"),
            ],
            "formula": (
                "No single closed form — harmonic balance with modulated drive is standard.  "
                "Conceptually η improves when the active device spends more time near "
                "Vds/Iload that minimizes (Vsupply − Vds)·I."
            ),
            "usage": [
                "LTE/5G massive MIMO remote radio heads.",
                "Broadcast TV transmitters.",
            ],
            "real_examples": [
                "GaN Doherty MMICs at 2.1 GHz for macro cells.",
            ],
            "design_notes": (
                "• Load-pull data for both main and peaking devices under combined excitation.\n"
                "• Memory effects in ET supplies interact with DPD — co-simulate.\n"
                "• Thermal coupling shifts combining point over temperature."
            ),
            "waveform": {"kind": "pa_efficiency_arch_concept", "params": {}},
        },
    },
    "RF & Discrete Small-Signal Amplifiers": {
        "__meta__": {
            "icon": "📶",
            "summary": (
                "Discrete bipolar and FET stages still define LNAs, PAs, and wideband buffers where "
                "op-amps run out of GHz bandwidth or breakdown voltage.  This branch adds core "
                "cells — common-emitter/source gain, cascode stacking, differential pairs, current "
                "mirrors, and on-chip style distributed amplifiers — before system-level LNA/PA "
                "topics.  Bias, S-parameters, stability circles, and thermal limits still rule."
            ),
        },
        "Low-Noise Amplifier (LNA)": {
            "icon": "🛰",
            "summary": (
                "An LNA sits closest to the antenna or sensor chain to establish noise figure. "
                "Design minimizes F = (SNR_in)/(SNR_out) by choosing device, bias, matching network, "
                "and source impedance (sometimes Γ_opt ≠ 50 Ω).\n\n"
                "Linear P₁dB and IP3 decide how large a blocker can be before desense occurs. "
                "Protection diodes / limiters shield against ESD and high-power leaked carriers."
            ),
            "key_params": [
                ("Noise figure", "Often 0.3–3 dB in cellular LNAs"),
                ("IP3", "Third-order intercept, dBm reference"),
            ],
            "formula": (
                "Friis cascade:  F_total = F1 + (F2−1)/G1 + (F3−1)/(G1·G2) + …"
            ),
            "usage": [
                "GPS / GNSS front-ends, cellular receive diversity paths.",
            ],
            "real_examples": [
                "TriQuint / Qorvo GaAs pHEMT die at 2 GHz with NF ≈ 0.5 dB.",
            ],
            "design_notes": (
                "• Match for noise, not just VSWR — use source-pull data.\n"
                "• Include ESD structures in the EM model."
            ),
            "waveform": {
                "kind": "lna_tuned_concept",
                "params": {
                    "f0": 2.45e9,
                    "Q": 14,
                    "Gmax_db": 17,
                    "nf_lna_db": 0.8,
                    "nf_follow_db": 5.5,
                    "gain_lna_db": 15,
                },
            },
        },
        "RF / IF Power Amplifier (PA)": {
            "icon": "📣",
            "summary": (
                "PAs deliver watts to tens/hundreds of watts into controlled impedances, often "
                "with efficiency traded against spectral mask (ACPR).  Classes AB through J, Doherty, "
                "envelope tracking, and digital pre-distortion (DPD) appear in cellular basestations.\n\n"
                "Thermal design, load-pull contours, VSWR survivability, and bias sequencing are "
                "non-optional."
            ),
            "key_params": [
                ("P1dB, PSAT", "Compression and saturation powers"),
                ("Efficiency", "η = P_RF_out / P_DC_in"),
            ],
            "formula": (
                "Load line:  Vpk/Ipk set by supply and device safe operating area."
            ),
            "usage": [
                "Cellular handset transmit chain, radar T/R modules, ISM-band radios.",
            ],
            "real_examples": [
                "GaN MMIC PA modules at 28 GHz for 5G massive MIMO.",
            ],
            "design_notes": (
                "• Simulate harmonics and shared heatsink coupling.\n"
                "• Monitor temperature — gain collapse can occur near thermal runaway."
            ),
            "waveform": {
                "kind": "rf_pa_compression",
                "params": {"small_signal_gain_db": 15, "p1db_out_dbm": 23},
            },
        },
        "Discrete Buffer (Emitter / Source Follower)": {
            "icon": "🔌",
            "summary": (
                "Emitter followers (BJT) and source followers (MOSFET) provide large current gain "
                "with voltage gain slightly less than one.  The emitter (source) tracks the base "
                "(gate) minus a nearly constant junction drop (≈ Vbe or Vgs minus Id/gm), so the "
                "output sits on a different DC level than the driving node even though the AC "
                "waveform is copied with small attenuation.\n\n"
                "Small-signal output resistance is on the order of 1/gm (plus layout and bias-network "
                "terms for BJTs), which is why a follower can drive moderate capacitance or a "
                "terminated line segment faster than some wideband op-amps at the same current.\n\n"
                "Limitations: a single NPN follower sources current to the load well but does not "
                "sink it strongly (use a complementary pair or active pull-down for symmetric drive); "
                "headroom costs one Vbe or Vgs from the positive rail; large-signal slewing can be "
                "nonlinear."
            ),
            "key_params": [
                ("Output Z", "≈ 1/gm to first order (BJT: add base spreading / rb/β effects)"),
                ("Headroom", "Output peak sits ~Vbe (or Vgs) below the driving swing high rail"),
            ],
            "formula": (
                "AC voltage gain (emitter bypassed so bias R is not in the signal path):\n"
                "    Av ≈ g_m R_L′ / (1 + g_m R_L′)  with R_L′ = parallel of load, bias resistors seen at emitter.\n"
                "When g_m R_L′ ≫ 1:  Av → 1 (slightly below 1).\n\n"
                "Equivalent form:  Av ≈ R_L′ / (R_L′ + r_e),   r_e ≈ 1/g_m.\n\n"
                "DC:  V_E ≈ V_B − V_BE(on)   (MOSFET:  V_S ≈ V_G − V_GS)."
            ),
            "usage": [
                "Clock tree buffers, fast sample-hold outputs, scope front-end discrete designs.",
            ],
            "real_examples": [
                "Emitter follower between varicap tank and mixer LO port to isolate tuning capacitance.",
            ],
            "design_notes": (
                "• Add emitter degeneration for thermal stability.\n"
                "• Watch secondary breakdown in fast followers driving inductors."
            ),
            "waveform": {
                "kind": "discrete_follower_rf",
                "params": {
                    "f_input": 100e6,
                    "Vbe": 0.68,
                    "ac_gain": 0.97,
                    "v_bias": 2.2,
                    "v_ac_pk": 0.1,
                },
            },
        },
        "Common-Emitter / Common-Source Gain Stage": {
            "icon": "🔺",
            "summary": (
                "The common-emitter (BJT) and common-source (MOSFET) stages are the workhorse "
                "voltage amplifiers: input on base/gate, output taken from collector/drain, "
                "emitter/source at AC ground (or bypassed).  Voltage gain is roughly −gm·RL′ "
                "(inverting) with RL′ the parallel combination of load resistor, output "
                "resistance, and any tuned network.\n\n"
                "Biasing sets quiescent current and keeps the device in the forward-active / "
                "saturation region.  Degeneration (unbypassed emitter/source resistor) trades "
                "gain for linearity and stabilizes bias.\n\n"
                "This is the template inside op-amps, LNAs (with matching), and IF strips before "
                "mixers."
            ),
            "key_params": [
                ("gm", "≈ Ic/Vt (BJT) or √(2µCoxId/W/L) (MOS in strong inversion)"),
                ("Gain", "−gm RL′ with phase inversion"),
                ("Fmax / FT", "Set upper frequency before current gain rolls off"),
            ],
            "formula": (
                "Small-signal:  Av ≈ −g_m · (r_o ∥ R_C ∥ R_load)\n\n"
                "With emitter degeneration Re (unbypassed):  Av ≈ −R_L′ / (1/g_m + R_e)."
            ),
            "usage": [
                "Discrete IF/RF gain blocks with lumped matching.",
                "Audio driver stages before transformers or followers.",
            ],
            "real_examples": [
                "2N3904 common-emitter stage with bypassed emitter resistor for ~20 dB at 10 MHz.",
            ],
            "design_notes": (
                "• Check S-parameters for unconditional stability with arbitrary Γ_load.\n"
                "• Miller capacitance limits bandwidth — cascode when you need voltage gain at RF."
            ),
            "waveform": {"kind": "common_emitter_concept", "params": {"f_input": 1200, "Av": -11}},
        },
        "Cascode Amplifier": {
            "icon": "🏗",
            "summary": (
                "A cascode stacks two devices: a common-emitter (or common-source) bottom device "
                "provides transconductance while a common-base (or common-gate) top device "
                "holds the bottom collector/drain voltage nearly fixed.  That kills most of the "
                "Miller multiplication of Cμ / Cgd, pushing the dominant pole to higher "
                "frequency.\n\n"
                "You trade extra headroom (another Vce or Vds) for bandwidth and often better "
                "reverse isolation.  LNAs, VCO buffers, and fast discrete pulse amplifiers use "
                "cascodes routinely.\n\n"
                "Integrated circuits extend the idea to folded cascodes and regulated cascodes "
                "for output swing."
            ),
            "key_params": [
                ("Bandwidth", "Roughly set by output node, not input Miller"),
                ("Headroom", "Minimum sum of Vce_sat or Vds_sat for both devices"),
                ("Noise", "Top device adds little if its current noise is degenerated"),
            ],
            "formula": (
                "Voltage gain still ~ g_m1 · R_L at the output node; input impedance is that of "
                "the CE/CS stage.  Dominant pole ≈ 1/(R_out · C_load) when Miller is suppressed."
            ),
            "usage": [
                "UHF/VHF receiver front-end gain before a SAW filter.",
                "Fast photodiode TIA front-ends (sometimes as regulated cascode).",
            ],
            "real_examples": [
                "BFU730F cascode LNA on GPS L1 patch front-end.",
            ],
            "design_notes": (
                "• Bias the cascode base/gate so the lower device stays in active region at peak swing.\n"
                "• Watch breakdown of the upper device in high-supply PAs."
            ),
            "waveform": {"kind": "cascode_bw_concept", "params": {"f_pole_ce": 11e6, "f_pole_cascade": 52e6}},
        },
        "Differential Pair (Emitter- / Source-Coupled)": {
            "icon": "⚡",
            "summary": (
                "Two matched transistors share a tail current source.  The differential input "
                "Vid steers current between the two branches in a tanh-shaped characteristic; "
                "small-signal gain is gm·RL per side for balanced loads.\n\n"
                "This cell is the heart of op-amp input stages, emitter-coupled logic, Gilbert "
                "multipliers, and balanced mixers.  Common-mode gain is low if the tail is ideal; "
                "real tails and mismatch set CMRR.\n\n"
                "Fully differential layouts with symmetric devices and centroiding reduce offset "
                "and even-order distortion."
            ),
            "key_params": [
                ("Tail current", "Sets gm and max linear range (~±25 mV Vid for BJT)"),
                ("CMRR", "Limited by tail output impedance and device mismatch"),
                ("Load", "Resistive, current mirror active load, or tuned tank"),
            ],
            "formula": (
                "Differential output current (ideal long-tail):\n"
                "    ΔI = I_ee · tanh(V_id / (2V_T))   (BJT small-signal g_m = I_ee/(2V_T) at 0).\n\n"
                "MOS obeys similar steering with √(µCoxW/L) and Vov replacing Vt scaling."
            ),
            "usage": [
                "Mixer LO port driven differentially.",
                "Limiting amplifier stages in fiber-optic receivers.",
            ],
            "real_examples": [
                "BFP840ESD differential pair in a 5 GHz LNA first stage.",
            ],
            "design_notes": (
                "• Symmetry in layout beats trimming for offset.\n"
                "• For large signals, degenerate emitters/sources to linearize."
            ),
            "waveform": {"kind": "diff_pair_concept", "params": {"Vt": 0.026, "Iss": 1e-3}},
        },
        "Current Mirror & Ratioed Gain Cell": {
            "icon": "∥",
            "summary": (
                "A current mirror copies a reference current to one or more outputs scaled by "
                "emitter-area ratios (BJT) or W/L ratios (MOS).  It is the standard way to bias "
                "arrays and to implement active loads that increase gain per supply volt.\n\n"
                "Wilson and cascoded mirrors improve output resistance and accuracy at the cost "
                "of headroom.  In RF ICs, mirrors bias gm stages and set PTAT/CTAT references.\n\n"
                "Mismatch and Vce/Vds dependence (Early effect, channel-length modulation) create "
                "copy error — Monte Carlo in simulation."
            ),
            "key_params": [
                ("Ratio", "Iout/Iref ≈ N for N identical devices in parallel"),
                ("Output resistance", "r_o of mirror output device, boosted by cascode"),
                ("Minimum V", "Vbe or Vgs plus saturation headroom"),
            ],
            "formula": (
                "Simple BJT mirror (matched):  Iout ≈ Iref · (Is2/Is1) · exp(ΔVbe/Vt) errors aside.\n\n"
                "Widlar mirror inserts emitter resistor to run Iout ≪ Iref without tiny devices."
            ),
            "usage": [
                "Biasing multi-stage discrete RF boards from one PTAT reference.",
                "Active load for diff pairs inside op-amps.",
            ],
            "real_examples": [
                "LM394 matched pair datasheet mirror examples.",
            ],
            "design_notes": (
                "• Layout: keep mirror devices isothermal.\n"
                "• For low currents, leakage and β degrade matching — use cascoded mirrors."
            ),
            "waveform": {"kind": "current_mirror_concept", "params": {"N": 3}},
        },
        "Distributed / Traveling-Wave Amplifier (TWA)": {
            "icon": "〰",
            "summary": (
                "A traveling-wave (distributed) amplifier splits gate and drain lines into "
                "sections, placing a transistor under each tap so gain adds along artificial "
                "transmission lines instead of stacking voltage gain in one node.  Forward waves "
                "synchronize while reflections are absorbed, yielding multi-octave bandwidth in "
                "MMICs.\n\n"
                "Used in microwave instrumentation, EW receivers, and optical modulator drivers "
                "past where a single transistor’s gain–bandwidth product suffices.\n\n"
                "Design is transmission-line centric: image parameters, terminations, and loss "
                "per section dominate — not a lumped RC model."
            ),
            "key_params": [
                ("Number of sections", "More cells → more gain until line loss wins"),
                ("Image impedance", "Match terminations for forward-wave buildup"),
                ("P1dB", "Distributed compression when outer cells clip first"),
            ],
            "formula": (
                "Conceptual: forward voltage grows ~ n · gm · Z0 per number of synchronized "
                "sections until attenuation balances injection — detailed synthesis uses "
                "even/odd mode analysis of the coupled lines."
            ),
            "usage": [
                "50 GHz+ lab instrumentation front-ends.",
                "Wideband radar stretch processor IF chains.",
            ],
            "real_examples": [
                "GaAs MMIC TWA modules in vector network analyzer receivers.",
            ],
            "design_notes": (
                "• EM simulation of the full line including bond pads.\n"
                "• Thermal gradients between sections skew gm and phase velocity."
            ),
            "waveform": {"kind": "traveling_wave_concept", "params": {}},
        },
    },
}
