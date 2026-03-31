"""Topic subtree: Filters (passive, active, response families, power-supply filters)."""

FILTERS_BRANCH = {
    "__meta__": {
        "icon": "🎛",
        "summary": (
            "A filter is an analog circuit whose primary purpose is to shape the frequency "
            "content of a signal.  Every filter is characterized by a transfer function "
            "H(s) = Vout(s)/Vin(s) expressed in the Laplace domain.  The denominator's roots "
            "(poles) determine roll-off steepness, while the numerator's roots (zeros) create "
            "notches or phase features.\n\n"
            "Filters are classified along four independent axes:\n"
            "  1) Response shape — Low-pass, High-pass, Band-pass, Band-stop/Notch, All-pass\n"
            "  2) Implementation — Passive (R/L/C only), Active (op-amp + R/C), Switched-cap, Digital\n"
            "  3) Order — 1st, 2nd, 3rd … each pole adds ≈20 dB/decade roll-off\n"
            "  4) Approximation family — Butterworth, Chebyshev, Bessel, Elliptic, etc.\n\n"
            "Understanding filters means understanding poles, zeros, Q factor (quality), "
            "damping ratio ζ (= 1/2Q), cutoff frequency ω₀, and how these map to component values."
        ),
    },
    "Passive Filters": {
        "__meta__": {
            "icon": "🔌",
            "summary": (
                "Passive filters use only resistors, inductors, and capacitors (and, at RF, distributed "
                "elements such as transmission-line stubs).  They need no DC power, add no active "
                "device noise, and scale from audio to microwave.  Trade-offs: you cannot get voltage "
                "gain, networks are sensitive to source/load impedance, and good inductors are large "
                "or costly at low frequency.\n\n"
                "This branch walks first-order RC and RL sections, second-order LC and RLC circuits, "
                "twin-T and LC traps, multi-element T and π prototypes, ladder and resonator-based "
                "designs, quartz/ceramic resonators, and stub filters.  Those ideas are the reference "
                "for most active and digital filters later in the tree."
            ),
        },
        "RC Low-Pass Filter": {
            "icon": "📉",
            "summary": (
                "The simplest and most fundamental analog filter.  A resistor in series followed by "
                "a capacitor to ground creates a single-pole low-pass response.\n\n"
                "At low frequencies the capacitor's impedance Xc = 1/(2πfC) is very high, so almost "
                "all input voltage appears at the output.  As frequency rises, Xc drops, and more "
                "signal is shunted to ground through C.  At the cutoff frequency fc, the output is "
                "at −3 dB (≈ 70.7 %) of the input.  Above fc, the output falls at 20 dB/decade "
                "(equivalently 6 dB/octave).\n\n"
                "The time-domain step response is an exponential rise with time constant τ = RC.  "
                "After one time constant, the output reaches ≈ 63.2 % of the step.  After 5τ it is "
                "within 1 % of the final value.\n\n"
                "This filter is memoryless and minimum-phase.  Its phase shifts from 0° at DC to "
                "−90° at high frequency, passing through −45° exactly at fc."
            ),
            "key_params": [
                ("Cutoff frequency", "fc = 1 / (2π R C)"),
                ("Time constant", "τ = R × C"),
                ("Roll-off", "−20 dB / decade  (−6 dB / octave)"),
                ("Phase at fc", "−45°"),
                ("Output impedance", "≈ R  (at low freq) … 0  (at high freq through C)"),
            ],
            "formula": (
                "Transfer function (Laplace):\n"
                "    H(s) = 1 / (1 + s R C)\n\n"
                "Magnitude response:\n"
                "    |H(jω)| = 1 / √(1 + (ω R C)²)\n\n"
                "Phase response:\n"
                "    ∠H(jω) = −arctan(ω R C)\n\n"
                "Cutoff frequency (−3 dB point):\n"
                "    fc = 1 / (2 π R C)    [Hz]\n"
                "    ωc = 1 / (R C)        [rad/s]\n\n"
                "Step response:\n"
                "    vout(t) = Vstep · (1 − e^(−t / RC))    for t ≥ 0\n\n"
                "Impulse response:\n"
                "    h(t) = (1/RC) · e^(−t / RC)           for t ≥ 0"
            ),
            "usage": [
                "Anti-aliasing before ADC sampling.",
                "Smoothing PWM output to approximate analog voltage.",
                "Removing high-frequency sensor noise.",
                "Audio treble attenuation / tone control.",
                "DAC output reconstruction filtering.",
                "Ripple reduction on low-current supply rails.",
            ],
            "real_examples": [
                "Arduino: 10 kΩ + 100 nF → fc ≈ 159 Hz to smooth a noisy analog sensor reading.",
                "Audio: 1 kΩ + 10 nF → fc ≈ 15.9 kHz to gently roll off ultrasonic content.",
                "PWM-to-analog: 4.7 kΩ + 1 µF → fc ≈ 33.9 Hz to smooth a 1 kHz PWM into DC.",
                "DAC output: 100 Ω + 1 nF → fc ≈ 1.59 MHz to suppress DAC glitch energy.",
            ],
            "design_notes": (
                "• The source impedance adds to R, shifting fc downward — always account for it.\n"
                "• The next-stage input impedance loads the output; use a buffer (voltage follower) "
                "if the load is comparable to R.\n"
                "• For 2nd-order (steeper) filtering, cascade two RC sections with a buffer between "
                "them, or switch to an active topology.\n"
                "• Component tolerance directly shifts fc.  Use 1 % resistors and C0G/NP0 capacitors "
                "for precision applications.\n"
                "• At very high frequency, parasitic inductance of the capacitor and resistor body "
                "limits real attenuation."
            ),
            "waveform": {
                "kind": "rc_lowpass",
                "params": {"R": 10e3, "C": 100e-9, "f_input": 500, "f_show_range": (10, 10000)},
            },
        },
        "RC High-Pass Filter": {
            "icon": "📈",
            "summary": (
                "The complement of the RC low-pass: a capacitor in series followed by a resistor "
                "to ground.  It blocks DC and very low frequencies while passing higher ones.\n\n"
                "At high frequencies, Xc → 0 so the capacitor acts as a short and all signal passes.  "
                "At low frequencies, Xc is large and most signal is dropped across the capacitor.\n\n"
                "The cutoff frequency is the same formula as the low-pass: fc = 1/(2πRC).  Below fc "
                "the output falls at +20 dB/decade (rising slope on a Bode plot from left to right).  "
                "The phase shifts from +90° at very low frequency through +45° at fc down to 0° at "
                "high frequency.\n\n"
                "This is the standard AC-coupling circuit: it removes DC offset while passing the "
                "time-varying part of a signal."
            ),
            "key_params": [
                ("Cutoff frequency", "fc = 1 / (2π R C)"),
                ("Roll-off (below fc)", "+20 dB / decade"),
                ("Phase at fc", "+45°"),
                ("DC gain", "0  (capacitor blocks DC)"),
            ],
            "formula": (
                "Transfer function:\n"
                "    H(s) = s R C / (1 + s R C)\n\n"
                "Magnitude:\n"
                "    |H(jω)| = (ω R C) / √(1 + (ω R C)²)\n\n"
                "Phase:\n"
                "    ∠H(jω) = 90° − arctan(ω R C)\n\n"
                "Step response (output decays back to zero):\n"
                "    vout(t) = Vstep · e^(−t / RC)    for t ≥ 0"
            ),
            "usage": [
                "AC coupling between amplifier stages.",
                "Removing DC offset from sensor signals.",
                "Audio input coupling to prevent op-amp saturation.",
                "High-pass crossover in speaker systems.",
                "Pulse-edge emphasis and differentiation.",
            ],
            "real_examples": [
                "Microphone input: 1 µF + 10 kΩ → fc ≈ 15.9 Hz — passes voice, blocks DC bias.",
                "Audio line coupling: 10 µF + 10 kΩ → fc ≈ 1.6 Hz — passes all audio, blocks offset.",
                "Oscilloscope AC-coupling: internal RC high-pass with fc around 1–10 Hz.",
            ],
            "design_notes": (
                "• Choose fc well below your signal band so it does not attenuate wanted content.\n"
                "• Electrolytic capacitors introduce leakage current — use film caps for precision.\n"
                "• If load impedance is low, it forms a divider with R and shifts fc upward.\n"
                "• For audio, very low fc (< 10 Hz) keeps bass intact but needs large C values."
            ),
            "waveform": {
                "kind": "rc_highpass",
                "params": {"R": 10e3, "C": 1e-6, "f_input": 5, "f_show_range": (0.1, 1000)},
            },
        },
        "RL Low-Pass Filter": {
            "icon": "🧲",
            "summary": (
                "An inductor in series with a resistive load.  At low frequencies the inductor's "
                "impedance XL = 2πfL is small, passing signal freely.  At high frequencies XL grows "
                "and the inductor increasingly blocks current, attenuating the output.\n\n"
                "Cutoff frequency: fc = R / (2πL).  Roll-off is −20 dB/decade, identical to the RC "
                "low-pass in shape.  The key difference is that the RL filter handles higher current "
                "more naturally because the inductor is in the power path.\n\n"
                "Used where current-carrying capability matters more than size — for example in "
                "power supply smoothing."
            ),
            "key_params": [
                ("Cutoff frequency", "fc = R / (2π L)"),
                ("Time constant", "τ = L / R"),
                ("Roll-off", "−20 dB / decade"),
            ],
            "formula": (
                "H(s) = R / (R + sL) = 1 / (1 + sL/R)\n\n"
                "|H(jω)| = 1 / √(1 + (ωL/R)²)\n\n"
                "fc = R / (2πL)"
            ),
            "usage": [
                "Power line filtering.",
                "Motor drive smoothing.",
                "Current-path noise reduction.",
            ],
            "real_examples": [
                "DC motor supply: 100 µH + 10 Ω → fc ≈ 15.9 kHz to block switching noise.",
                "LED driver output smoothing.",
            ],
            "design_notes": (
                "• Inductors have parasitic resistance (DCR) that adds to R.\n"
                "• Core saturation limits maximum current — always check rated current.\n"
                "• RL filters are rarely used in small-signal paths because inductors are bulky; "
                "RC or active filters are preferred for signal work."
            ),
            "waveform": {
                "kind": "rl_lowpass",
                "params": {"R": 50, "L": 1e-3, "f_input": 20000},
            },
        },
        "LC Low-Pass Filter": {
            "icon": "⚡",
            "summary": (
                "A second-order filter using an inductor in series and capacitor to ground.  "
                "It has two energy-storage elements, creating a 2-pole response with −40 dB/decade "
                "roll-off — twice as steep as a single RC or RL filter.\n\n"
                "The resonant frequency f0 = 1/(2π√(LC)) is where the inductor and capacitor "
                "impedances are equal.  Near f0 the filter can exhibit peaking (ringing) unless "
                "damped by a resistor.  The quality factor Q = (1/R)√(L/C) for a series-damped version "
                "controls peaking: Q > 0.707 means overshoot, Q = 0.707 is Butterworth-flat, "
                "Q < 0.5 is over-damped.\n\n"
                "LC filters are the workhorse of power electronics because the inductor can carry "
                "large DC current and the capacitor stores charge, together providing efficient "
                "low-loss smoothing."
            ),
            "key_params": [
                ("Resonant frequency", "f0 = 1 / (2π √(LC))"),
                ("Roll-off", "−40 dB / decade"),
                ("Quality factor", "Q = (1/R) √(L/C)  for series-R damped"),
                ("Damping ratio", "ζ = 1 / (2Q)"),
            ],
            "formula": (
                "H(s) = 1 / (s²LC + sRC + 1)          [series R damped]\n"
                "     = ω₀² / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "where  ω₀ = 1/√(LC),   Q = (1/R)√(L/C)\n\n"
                "Undamped (R=0):\n"
                "    H(s) = 1 / (s²LC + 1)  — infinite Q, pure resonance peak\n\n"
                "Step response shows ringing if Q > 0.707."
            ),
            "usage": [
                "Buck / boost converter output filtering.",
                "Switching power supply input filtering.",
                "RF low-pass matching networks.",
                "EMI filtering on power lines.",
            ],
            "real_examples": [
                "Buck converter: 10 µH + 22 µF → f0 ≈ 10.7 kHz, placed after the switching FET.",
                "EMI input filter for a 100 kHz SMPS: 47 µH + 4.7 µF → f0 ≈ 10.7 kHz.",
            ],
            "design_notes": (
                "• Always add damping (series R, or parallel RC snubber) to prevent resonant peaking.\n"
                "• Capacitor ESR provides some natural damping — use it in your model.\n"
                "• Inductor core losses increase with frequency and help damp high-Q peaks.\n"
                "• In power supplies, the LC filter interacts with the control loop — verify stability."
            ),
            "waveform": {
                "kind": "lc_lowpass",
                "params": {"L": 10e-6, "C": 22e-6, "R_damp": 0.5, "f_input": 30000},
            },
        },
        "RLC Band-Pass Filter": {
            "icon": "🎯",
            "summary": (
                "A series RLC circuit naturally forms a band-pass filter.  At the resonant frequency "
                "f0 = 1/(2π√(LC)), the inductor and capacitor impedances cancel and only the "
                "resistance remains, allowing maximum current/voltage transfer.\n\n"
                "Below f0 the capacitor dominates (high impedance), above f0 the inductor dominates — "
                "both reducing output.  The bandwidth BW = f0/Q = R/(2πL) for a series RLC.\n\n"
                "Q factor determines selectivity: higher Q means narrower bandwidth and sharper "
                "selection.  For a series RLC, Q = (1/R)√(L/C) = ω₀L/R."
            ),
            "key_params": [
                ("Center frequency", "f0 = 1 / (2π √(LC))"),
                ("Bandwidth", "BW = f0 / Q  =  R / (2πL)"),
                ("Quality factor", "Q = ω₀L / R = (1/R)√(L/C)"),
                ("Roll-off", "−20 dB/decade on each side (2nd order)"),
            ],
            "formula": (
                "Series RLC band-pass transfer function:\n"
                "    H(s) = sRC / (s²LC + sRC + 1)\n"
                "         = (ω₀/Q)s / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "At resonance: |H(jω₀)| = 1  (max),  phase = 0°.\n"
                "3 dB bandwidth:  BW = ω₀/Q = R/L  [rad/s]."
            ),
            "usage": [
                "Radio tuning circuits — select one station's carrier frequency.",
                "IF (intermediate frequency) filtering in superheterodyne receivers.",
                "Vibration / resonance analysis — isolate one mechanical frequency.",
                "Tone decoding in DTMF or signaling systems.",
            ],
            "real_examples": [
                "AM radio tuner: variable C ≈ 10–365 pF with L ≈ 250 µH tunes 530–1710 kHz.",
                "Guitar pickup resonance: L ≈ 3 H, C ≈ 500 pF → f0 ≈ 4 kHz (the 'tone peak').",
            ],
            "design_notes": (
                "• Very high Q circuits are sensitive to component tolerance.\n"
                "• Inductor losses lower the effective Q — use high-quality cores.\n"
                "• Parallel RLC is the dual: it has a band-stop (notch) characteristic."
            ),
            "waveform": {
                "kind": "rlc_bandpass",
                "params": {"R": 50, "L": 1e-3, "C": 100e-9, "f_input_center": None},
            },
        },
        "Band-Stop / Notch (Twin-T)": {
            "icon": "🚫",
            "summary": (
                "A band-stop (notch) filter rejects a narrow frequency band while passing everything "
                "else.  The classic passive implementation is the Twin-T network: two T-shaped RC "
                "paths (one low-pass, one high-pass) whose outputs combine to cancel at a specific "
                "frequency.\n\n"
                "At the notch frequency, destructive interference between the two paths creates a "
                "deep null.  The depth and sharpness depend on component matching.\n\n"
                "The standard Twin-T uses R, R, 2C in one arm and C, C, R/2 in the other.  "
                "Notch frequency: f0 = 1/(2πRC).  Adding an op-amp buffer or positive feedback "
                "increases the Q (sharpness) of the notch dramatically."
            ),
            "key_params": [
                ("Notch frequency", "f0 = 1 / (2π R C)"),
                ("Passive Q", "≈ 0.25  (shallow notch)"),
                ("Active-boosted Q", "Can reach 10–50 with feedback"),
                ("Notch depth", "Depends on component matching"),
            ],
            "formula": (
                "Passive Twin-T notch frequency:\n"
                "    f0 = 1 / (2π R C)\n\n"
                "General notch transfer function:\n"
                "    H(s) = (s² + ω₀²) / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "At ω = ω₀:  |H(jω₀)| = 0  (ideal infinite null).\n"
                "Bandwidth of the rejection band:  BW = f0 / Q."
            ),
            "usage": [
                "50/60 Hz mains hum rejection in biomedical (ECG, EEG) instruments.",
                "Removing known interference tones in audio or measurement paths.",
                "Feedback-based anti-resonance in control systems.",
            ],
            "real_examples": [
                "ECG amplifier: Twin-T with R = 33 kΩ, C = 100 nF → f0 ≈ 48 Hz (tuned to ~50 Hz).",
                "Guitar pedal hum filter: notch at 60 Hz for US mains.",
            ],
            "design_notes": (
                "• Use 1 % resistors and matched capacitors for deep null.\n"
                "• An op-amp buffer after the Twin-T prevents loading.\n"
                "• Positive feedback around the Twin-T increases Q — useful but can oscillate.\n"
                "• Temperature changes shift component values and detune the notch."
            ),
            "waveform": {
                "kind": "notch",
                "params": {"f0": 50, "Q": 5, "f_signal": 50},
            },
        },
        "RL High-Pass Filter": {
            "icon": "⬆️",
            "summary": (
                "This is the natural high-pass companion to the series RL low-pass.  A resistor sits "
                "in series from the source and an inductor shunts the output node to ground.\n\n"
                "At DC the inductor looks like a short, so the output is pulled down and very little "
                "signal reaches the load.  As frequency rises, the inductive reactance grows and the "
                "shunt draws less current; the output approaches the input.  The −3 dB corner is "
                "fc = R / (2π L), the same formula as the RL low-pass built as L series and R shunt — "
                "only the topology and the measured node change.\n\n"
                "Use it where you already have a series resistor (impedance set by the path), and "
                "you need a gentle high-pass in the power or drive path.  For small-signal precision "
                "work, RC high-pass is usually smaller and cheaper."
            ),
            "key_params": [
                ("Corner", "fc = R / (2π L)"),
                ("Roll-off below fc", "+20 dB / decade"),
                ("Compared to RL LP", "Dual topology — swap which element is series vs shunt"),
            ],
            "formula": (
                "Vout/Vin = jωL / (R + jωL)\n\n"
                "|H| = (ωL) / √(R² + (ωL)²)\n"
                "Phase = 90° − arctan(ωL/R)\n\n"
                "At ω = R/L, |H| = 1/√2  (−3 dB)."
            ),
            "usage": [
                "Block DC or very low-frequency drift while passing ripple or carrier content.",
                "PWM / motor-drive contexts where inductors already exist in the network.",
            ],
            "real_examples": [
                "Conceptual conditioning on a current-fed branch before a wideband sense amplifier.",
            ],
            "design_notes": (
                "• Include inductor DC resistance in R for low-Q estimates.\n"
                "• Watch saturation current — the same issues as RL low-pass apply.\n"
                "• For audio or mV-level signals, RC high-pass is almost always the lighter choice."
            ),
            "waveform": {
                "kind": "rl_highpass",
                "params": {"R": 100, "L": 2.5e-3, "f_input_low": 2000, "f_input_high": 25000},
            },
        },
        "LC High-Pass Filter": {
            "icon": "⚡",
            "summary": (
                "A true second-order high-pass uses an inductor and capacitor together.  A practical "
                "small-signal form is: capacitor in series from the source to the output node, and "
                "an inductor (often in parallel with a damping resistor) from that node to ground.\n\n"
                "Below the cluster of corner frequencies the series capacitor blocks; above it, the "
                "shunt inductor’s rising impedance stops drawing current and the path opens up.  "
                "The asymptotic slope is −40 dB/decade on the low side once both reactances matter — "
                "twice as steep as a lone RC section.\n\n"
                "You see LC high-pass ideas at the front of RF front-ends, in class-D output networks "
                "conceptually, and anywhere an LC network must define a band edge with low loss above "
                "the passband."
            ),
            "key_params": [
                ("Topology", "C series · L (‖ R) shunt to ground"),
                ("Typical notch / peaking", "Depends heavily on damping resistor — always model ESR"),
                ("Compared to LC LP", "Dual placement: swap which reactive element is series vs shunt"),
            ],
            "formula": (
                "For C series and L ‖ R to ground at the output node:\n"
                "    Zc = 1/(jωC),   Zsh = jωRL / (R + jωL)\n"
                "    H = Zsh / (Zc + Zsh)\n\n"
                "Undamped resonance near ω₀ = 1/√(LC) — add enough R (or loss) to avoid unacceptable "
                "peaking in the passband or stopband."
            ),
            "usage": [
                "RF band-definition where loss above band must stay low.",
                "Multisection diplexer / diplexer-like splits with complementary LC networks.",
            ],
            "real_examples": [
                "High-pass section in an amateur-radio diplexer built from air-core L and ATC caps.",
            ],
            "design_notes": (
                "• Simulate with realistic Q — infinity-Q plots lie.\n"
                "• Layout parasitics move effective C and L; tune on a network analyzer when near GHz.\n"
                "• Pair with an LC low-pass when you need a passive band-pass sandwich."
            ),
            "waveform": {
                "kind": "lc_highpass",
                "params": {"L": 820e-6, "C": 100e-9, "R": 75, "f_input_low": 300, "f_input_high": 8000},
            },
        },
        "Series LC Shunt Trap (Band-Stop)": {
            "icon": "🔗",
            "summary": (
                "A series-connected inductor and capacitor, placed as a shunt branch to ground (or "
                "return) from a line, is one of the most common passive stopbands.  At the series "
                "resonant frequency the branch impedance ideally goes to zero and shorts energy "
                "away from the forward path, creating a notch in transmission.\n\n"
                "Real traps have finite Q from winding resistance, skin loss, and capacitor ESR, so "
                "the null is deep but not infinite.  Engineers add a small trim resistor or spread "
                "the winding slightly to guarantee stability when the trap loads an amplifier or a "
                "filter ladder.\n\n"
                "AM/FM duplexers, RF harmonic traps, and switched-mode EMI stacks routinely use this "
                "exact structure."
            ),
            "key_params": [
                ("Series resonance", "f0 = 1 / (2π √(L C))"),
                ("Notch depth", "Limited by series R of L and C ESR"),
                ("Out-of-band", "Above and below f0 the trap detunes and the line recovers"),
            ],
            "formula": (
                "Series arm impedance:  ZLC = jωL + 1/(jωC)  →  ZLC = 0 at ω₀ = 1/√(LC).\n\n"
                "Inserted as shunt on a line, transmission magnitude drops sharply near ω₀.\n\n"
                "Loaded Q of the trap sets notch width; tighter coupling to the line deepens the notch."
            ),
            "usage": [
                "Suppress a harmonic or spurious product on an antenna feed or PA output.",
                "Provide a controlled absorption path at one frequency in a multiplexer.",
            ],
            "real_examples": [
                "Class-C PA output: trap at 2f0 shunted before a low-pass mask.",
            ],
            "design_notes": (
                "• Combine with a network analyzer — traps are unforgiving of a few percent LC error.\n"
                "• Temperature drift of C and L moves f0; NPO/COG C helps.\n"
                "• For high power, verify peak voltage across C and current through L."
            ),
            "waveform": {
                "kind": "notch",
                "params": {"f0": 10.7e6, "Q": 40},
            },
        },
        "Parallel RLC Band-Stop (Nodal)": {
            "icon": "🔕",
            "summary": (
                "The parallel association of L, C, and R is the dual picture to the series RLC "
                "band-pass you already studied.  Across a narrow band the parallel tank can present "
                "a very high impedance to the rest of the circuit if losses are low.\n\n"
                "Depending on how the tank is fed and where you measure, you may implement a band-pass "
                "or band-stop: for example, a parallel LC branch tied through a series feed resistor "
                "creates a voltage divider; at resonance the tank impedance peaks and the division "
                "changes — synthesizers use such moves to steer energy through one path or another.\n\n"
                "Document the port you care about.  Passive band-stop variants often combine a tank "
                "with bridging resistors so the stopband is finite in width and depth."
            ),
            "key_params": [
                ("Parallel resonance", "ω₀ = 1/√(LC) for ideal lossless L and C"),
                ("Parallel Q", "Rp / (ω₀ L) with equivalent shunt Rp modeling losses"),
                ("Design", "Always draw the full two-port — “parallel RLC” alone is ambiguous"),
            ],
            "formula": (
                "Admittance of ideal parallel L and C branch:\n"
                "    Y = jωC + 1/(jωL) = j(ωC − 1/(ωL))\n\n"
                "At ω = ω₀, Y = 0 (infinite impedance).  Add conductance G = 1/Rp for losses.\n\n"
                "Two-port ABCD or S-parameter analysis is standard for RF ladder pieces."
            ),
            "usage": [
                "Narrowband impedance transformation in matching networks.",
                "Branching paths in diplexers / triplexers.",
            ],
            "real_examples": [
                "Antenna tuner: switched C banks with fixed coil form a parallel tank for match.",
            ],
            "design_notes": (
                "• Do not confuse this tank with the series trap — one shorts at resonance, the other "
                "opens in the lossless limit.\n"
                "• Harmonic balance simulators help when signals are large enough to move Q with voltage."
            ),
            "waveform": {
                "kind": "notch",
                "params": {"f0": 455e3, "Q": 25},
            },
        },
        "Passive T & π Low-Pass Sections": {
            "icon": "𝝿",
            "summary": (
                "Beyond a single LC cell, filters are built from repeated T-shaped or π-shaped "
                "sections: series arms (often inductors) alternate with shunt arms (often capacitors "
                "to ground).  A π low-pass visualizes as C–L–C to ground; a T section swaps the "
                "sequence for dual layouts suited to different source and load impedances.\n\n"
                "Design starts from a normalized prototype (Butterworth, Chebyshev, elliptic …), then "
                "denormalizes to 50 Ω, 75 Ω, or whatever your system impedance is, and scales to the "
                "real cutoff.  Band-pass and band-stop multisection filters come from frequency "
                "transformations of the same prototypes.\n\n"
                "These structures are the passive counterpart to active leapfrog and GIC-simulated "
                "ladders — same sensitivity virtues when doubly terminated."
            ),
            "key_params": [
                ("Sections", "Each π or T adds order; typical RF mask is 3–9 reactive elements"),
                ("Impedance", "Prototype normalized to 1 Ω / 1 rad/s then scaled"),
                ("Loss", "Finite Q of inductors rounds corners and lowers stopband attenuation"),
            ],
            "formula": (
                "Element values gₖ come from tables for the chosen approximation and order.\n\n"
                "Denormalize:  L = (Z₀/ωc) L_norm ,  C = C_norm / (Z₀ ωc).\n\n"
                "π vs T is a Δ–Y equivalent problem — choose whichever fits layout and parasitics."
            ),
            "usage": [
                "RF transmitter / receiver channel masks.",
                "CATV diplex filters, LTE/RAN cavity-combined chains.",
            ],
            "real_examples": [
                "5G small-cell duplexer: several π sections realize the wide stopband between RX and TX.",
            ],
            "design_notes": (
                "• Model every coil’s self-resonance — it behaves like an extra hidden C.\n"
                "• Ground vias define the shunt capacitor’s second terminal; poor via inductance "
                "eats stopband depth.\n"
                "• Tune with slug cores or trim caps; torque-seal or thread-lock after alignment."
            ),
            "waveform": {
                "kind": "passive_pi_lp",
                "params": {"fc": 1800, "order": 3},
            },
        },
        "Passive LC Ladder & Coupled Resonators": {
            "icon": "🪜",
            "summary": (
                "A ladder is simply many LC cells in cascade, possibly with different element values "
                "per stage to realize an elliptic or quasi-elliptic response with finite zeros.  "
                "Coupled resonators (magnetically coupled coils, evanescent coupling between cavities) "
                "are another way to build the same polynomial without a one-to-one series/shunt "
                "viscosity.\n\n"
                "High-Q resonators — dielectric pucks, cavity bowls, SAW or BAW stacks — let you hit "
                "steep skirts with lower insertion loss than a string of lumped Litz coils.  The math "
                "still returns to coupling coefficients kᵢⱼ and mode frequencies.\n\n"
                "Expect layout and mechanics to dominate once Q exceeds a few hundred."
            ),
            "key_params": [
                ("Order", "Set by number of resonant modes you control"),
                ("Coupling", "Sets bandwidth; tighter coupling widens the passband"),
                ("Tuning", "Each mode trimmed with correction screws or bias in tunable materials"),
            ],
            "formula": (
                "Coupled-mode matrix formulation (conceptual):\n"
                "    (jωI + jM + Γ) a = κ Vin\n\n"
                "where M holds couplings, Γ holds damping, a holds phasor mode amplitudes."
            ),
            "usage": [
                "Base-station cavity combiners.",
                "SATCOM waveguide filters, radar IF chains.",
            ],
            "real_examples": [
                "Cavity duplexer at 400 MHz with four TM₀₁₀ modes coupled by iris apertures.",
            ],
            "design_notes": (
                "• Temperature drift of dielectric constant shifts passband — many systems need "
                "compensation or ovenizing.\n"
                "• Microphonic noise on large cavities matters in portable radios.\n"
                "• For wide tuning, consider switching banks rather than a single wideband lumped fake."
            ),
            "waveform": {
                "kind": "lc_ladder_coupled_concept",
                "params": {"f1_hz": 0.92e6, "f2_hz": 1.06e6, "Q": 100},
            },
        },
        "Crystal & Ceramic Resonator Filters": {
            "icon": "💎",
            "summary": (
                "Quartz crystals and high-Q ceramics behave electrically like very sharp series or "
                "parallel resonant branches plus static plate capacitance.  The motional arm (Rm, Lm, Cm) "
                "sets the narrow series resonance; C0 shunts the whole package at high frequency.\n\n"
                "Ladder filters chain multiple crystals with small capacitors between them to create "
                "very selective IF filters at a few to a few hundred MHz with kHz-wide passbands.  "
                "Matching networks transform system impedance onto the low motional impedance branch.\n\n"
                "Such filters stay everywhere SONET/SDH timing, legacy radios, and precision clocks still "
                "demand analog selectivity with micro-watts of loss."
            ),
            "key_params": [
                ("Series fs", "Where motional arm resonates — minimum |Z|"),
                ("Parallel fp", "Slightly higher — maximum impedance with C0"),
                ("Motional Q", "Often 10³–10⁶ — sets minimum achievable bandwidth"),
            ],
            "formula": (
                "Motional series branch:  Zm = Rm + jωLm + 1/(jωCm).\n\n"
                "fs solves ωsLm = 1/(ωsCm);  fp includes C0 in parallel mathematics.\n\n"
                "Pole-zero layout of N-crystal ladder follows tabulated Chebyshev or Gaussian masks."
            ),
            "usage": [
                "455 kHz or 10.7 MHz IF strips before demodulation.",
                "Oscillator pulling in TCXOs / OCXOs — frequency trimmed by load C.",
            ],
            "real_examples": [
                "10.7 MHz monolithic crystal filter (4-pole) between mixer and FM demod IC.",
            ],
            "design_notes": (
                "• Never exceed drive level — quartz ages or fractures.\n"
                "• C0 causes spurious paths; include it in every SPICE netlist.\n"
                "• Ceramic parts cost less but drift more; read temperature coefficients on the datasheet."
            ),
            "waveform": {
                "kind": "crystal_resonator",
                "params": {"f0": 10e6, "Q": 12000, "Rm": 30, "Rsrc": 50},
            },
        },
        "Transmission-Line & Stub Filters": {
            "icon": "📡",
            "summary": (
                "When wavelengths are comparable to your physical structure, lumped L and C are "
                "replaced (or augmented) by transmission-line sections.  A quarter-wave shorted stub "
                "looks like an open at the design frequency and vice versa; shunt stubs create narrow "
                "notches or broad equal-ripple masks depending on length and coupling.\n\n"
                "Design uses electrical length θ = βℓ, characteristic impedance Z₀, and rich‑substrate "
                "models (εᵣ, loss tangent, dispersion).  Tools compute S-parameters directly, then "
                "optimize step discontinuities, corners, and via fences.\n\n"
                "This is how WLAN front-ends, radar feed networks, and 5G mm-wave passive beamformers "
                "are realized when lumped parts would be irrelevant."
            ),
            "key_params": [
                ("Electrical length", "βℓ at f₀ — defines resonance condition"),
                ("Z₀", "Set by line width versus ground reference"),
                ("Harmonics", "Stubs repeat at integer multiples — plan stopbands there too"),
            ],
            "formula": (
                "Input impedance of lossless line length ℓ terminated in ZL:\n"
                "    Zin = Z₀ · (ZL + jZ₀ tan βℓ) / (Z₀ + jZL tan βℓ)\n\n"
                "Open stub (ZL = ∞):  Zin = −j Z₀ cot βℓ."
            ),
            "usage": [
                "Microstrip / stripline harmonic traps on PA outputs.",
                "Distributed low-pass masks in mm-wave phased arrays.",
            ],
            "real_examples": [
                "Wi-Fi PA output: λ/4 open stub knocks down second harmonic before the antenna pin.",
            ],
            "design_notes": (
                "• Momentum / EM solvers beat hand formulas once λ/10 rules fail.\n"
                "• Temperature bends the board — copper and εᵣ move θ.\n"
                "• Package launch regions often eat more bandwidth than the stub mathematics predicts."
            ),
            "waveform": {
                "kind": "tl_stub_concept",
                "params": {"Z0": 50, "vp": 1.58e8, "f_quarter_wave": 2.4e9},
            },
        },
        "Passive Lattice All-Pass (Bridge)": {
            "icon": "🔀",
            "summary": (
                "Some passive networks reshape phase while keeping magnitude nominally flat — the "
                "classical lattice (bridge) combines Z₁ and Z₂ arms so |Vout/Vin| stays near unity "
                "while the angle sweeps with frequency.  Today this is exotic in baseband: op-amp "
                "all-pass cells are simpler below a few MHz.\n\n"
                "At RF, however, balanced bridges still appear in phase-shift networks for beam steering "
                "and in measurement bridges where symmetry rejects even-mode error.\n\n"
                "Treat this entry as historical context plus a reminder that “passive” does not mean "
                "“only low-pass sections.”"
            ),
            "key_params": [
                ("Balance", "Symmetry sets common-mode rejection"),
                ("Component spread", "Z₁ and Z₂ often wound components — trimming is manual"),
            ],
            "formula": (
                "Unbalanced lattice simplification (conceptual):\n"
                "    H(s) ∝ (Z₁ − Z₂) / (Z₁ + Z₂) for certain port choices.\n\n"
                "Pick Z₁, Z₂ as RC composites to mold group delay."
            ),
            "usage": [
                "Legacy phased-array passive beamformers.",
                "Precision impedance bridges and phase standards.",
            ],
            "real_examples": [
                "WWII-era coaxial delay equalizer sections rebuilt with modern PTFE dielectric.",
            ],
            "design_notes": (
                "• If your goal is audio or control-loop phase trim, start with the active all-pass "
                "topic instead — fewer transformers, tighter tolerances."
            ),
            "waveform": {
                "kind": "lattice_rf_allpass",
                "params": {"f_lo": 1e6, "f_hi": 2e9, "tau": 4e-10},
            },
        },
    },
    "Active Filters": {
        "__meta__": {
            "icon": "🔧",
            "summary": (
                "Active filters are built with amplifiers (usually op-amps) plus resistors and "
                "capacitors, and sometimes simulated inductors or clocked switches.  They avoid large "
                "magnetic parts at low frequency and can buffer stages, provide gain, and hold stable "
                "input and output impedances.\n\n"
                "Most designs stack second-order sections called biquads.  Each biquad has the form "
                "H(s) = N(s) / (s² + (ω₀/Q)s + ω₀²).  Higher orders are made by cascading biquads "
                "(and sometimes one extra first-order section).\n\n"
                "In this branch you will find: Sallen–Key, multiple-feedback (MFB), state-variable / "
                "KHN, Tow–Thomas, Fliege, Akerberg–Mossberg, twin-T notch, GIC inductor simulation, "
                "leapfrog ladders, OTA-C (gm-C), switched-capacitor, and N-path filters.  The shape "
                "of the response (Butterworth, Chebyshev, Bessel, elliptic, …) is chosen separately — "
                "see “Response Families” under Filters."
            ),
        },
        "Sallen-Key Low-Pass": {
            "icon": "🔑",
            "summary": (
                "The most popular 2nd-order active filter topology.  Named after R. P. Sallen and "
                "E. L. Key (1955, MIT Lincoln Labs).  Uses a single op-amp configured as a "
                "non-inverting stage (often unity gain), with two resistors and two capacitors "
                "forming the frequency-shaping network.\n\n"
                "The op-amp provides buffering (high input Z, low output Z) and can optionally add "
                "gain.  The feedback from output to the node between R1 and R2 creates the "
                "positive feedback that shapes the complex pole pair.\n\n"
                "For equal-component design (R1=R2=R, C1=C2=C), the cutoff frequency is "
                "fc = 1/(2πRC) and Q is fixed at 0.5 (over-damped).  To achieve Butterworth "
                "response (Q = 0.707), gain must be set to 1.586 or component ratios adjusted.\n\n"
                "Advantages: simple, one op-amp, non-inverting output.\n"
                "Limitations: difficult to achieve Q > 5, gain and Q are interlinked, sensitive to "
                "op-amp GBW at high frequencies."
            ),
            "key_params": [
                ("Order", "2nd order (2 poles)"),
                ("Roll-off", "−40 dB / decade"),
                ("Typical Q range", "0.5 – 5"),
                ("Op-amps needed", "1"),
                ("Signal polarity", "Non-inverting"),
            ],
            "formula": (
                "General Sallen-Key low-pass transfer function:\n"
                "    H(s) = K ω₀² / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "where:\n"
                "    ω₀ = 1 / √(R1·R2·C1·C2)\n"
                "    Q  = √(R1·R2·C1·C2) / (R1·C2 + R2·C2 + R1·C1·(1−K))\n"
                "    K  = 1 + Ra/Rb   (gain-setting resistors, or K=1 for unity)\n\n"
                "Equal-component simplification (R1=R2=R, C1=C2=C):\n"
                "    ω₀ = 1/(RC)\n"
                "    Q  = 1/(3−K)\n"
                "    For Butterworth (Q=0.707):  K = 3 − 1/Q ≈ 1.586\n\n"
                "Design procedure:\n"
                "  1. Choose fc, pick C (e.g. standard value).\n"
                "  2. R = 1/(2π·fc·C).\n"
                "  3. Set K via Ra/Rb for desired Q."
            ),
            "usage": [
                "Anti-aliasing before ADCs in data acquisition.",
                "Audio tone shaping and equalization.",
                "Sensor signal conditioning.",
                "Building higher-order Butterworth/Bessel/Chebyshev filters by cascading sections.",
            ],
            "real_examples": [
                "12-bit ADC front-end: Sallen-Key Butterworth at 10 kHz, using OPA2340.",
                "Audio: 4th-order Butterworth LPF at 20 kHz = two cascaded Sallen-Key stages.",
                "Vibration sensor: 2nd-order Bessel at 500 Hz to preserve pulse shape.",
            ],
            "design_notes": (
                "• Op-amp GBW should be ≥ 100× fc for < 1 % gain error.\n"
                "• Use C0G/NP0 capacitors for frequency stability.\n"
                "• For Butterworth Q = 0.707, gain K = 1.586 → Ra/Rb = 0.586.\n"
                "• Cascading two Sallen-Key stages gives a 4th-order filter (−80 dB/dec).\n"
                "• For Q > 3, consider MFB or state-variable instead."
            ),
            "waveform": {
                "kind": "active_lowpass_2nd",
                "params": {"f0": 1000, "Q": 0.707, "gain": 1, "f_input": 3000},
            },
        },
        "Multiple Feedback (MFB) Low-Pass": {
            "icon": "🔄",
            "summary": (
                "The Multiple Feedback topology is an inverting 2nd-order active filter that uses "
                "one op-amp with multiple feedback paths.  Sometimes called the Rauch or "
                "infinite-gain topology.\n\n"
                "Unlike Sallen-Key, the signal enters the inverting node.  The output is phase-inverted. "
                "Two capacitors and three resistors set the frequency, Q, and gain.\n\n"
                "MFB naturally achieves higher Q than Sallen-Key (up to ≈ 25 vs ≈ 5) because gain "
                "and Q are less tightly coupled.  The gain magnitude equals −2Q² at resonance, and "
                "the required op-amp GBW is lower relative to Q.\n\n"
                "This topology is widely used in audio, instrumentation, and communication filters "
                "when moderate Q and compact design are needed."
            ),
            "key_params": [
                ("Order", "2nd order"),
                ("Roll-off", "−40 dB / decade"),
                ("Typical Q range", "0.5 – 25"),
                ("Op-amps needed", "1"),
                ("Signal polarity", "Inverting"),
            ],
            "formula": (
                "MFB low-pass transfer function:\n"
                "    H(s) = −(R3/(R1)) · ω₀² / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "Component relationships:\n"
                "    ω₀ = 1 / √(R2·R3·C1·C2)\n"
                "    Q  = √(R2·R3·C1·C2) / (C2·(R2+R3) + C1·R2·R3/R1)  [simplified forms exist]\n\n"
                "DC gain = −R3/R1.\n\n"
                "Design approach: pick C1, C2, then solve for R1, R2, R3 from fc, Q, and gain."
            ),
            "usage": [
                "Band-pass and low-pass sections in communication receivers.",
                "Audio equalization stages.",
                "Precision measurement filters requiring higher Q.",
                "Anti-aliasing filters where phase inversion is acceptable.",
            ],
            "real_examples": [
                "Narrowband audio filter: MFB band-pass at 1 kHz with Q = 10 for tone detection.",
                "Sensor conditioning: MFB low-pass at 100 Hz for strain gauge signal.",
            ],
            "design_notes": (
                "• The inverting output may require an additional inverter if polarity matters.\n"
                "• For very high Q (> 25), consider state-variable topology.\n"
                "• Component sensitivity increases with Q — use tight-tolerance parts.\n"
                "• The virtual ground at the inverting input provides a defined impedance node."
            ),
            "waveform": {
                "kind": "active_lowpass_2nd",
                "params": {"f0": 1000, "Q": 2.0, "gain": -4, "f_input": 3000},
            },
        },
        "State-Variable / Tow-Thomas": {
            "icon": "🏗",
            "summary": (
                "What it is\n"
                "The state-variable filter is a three-op-amp biquad: one summing amplifier plus two "
                "integrators in a loop.  It realizes one pair of complex poles and gives you several "
                "outputs at once.\n\n"
                "Why it is useful\n"
                "From the same core circuit you get low-pass, band-pass, and high-pass responses that "
                "share the same center frequency and Q.  With weighted summing you can also build "
                "notch and all-pass behavior.  Center frequency and Q are tuned with different "
                "resistors, which is much more convenient than in single-op-amp Sallen–Key or MFB "
                "stages where gain and Q interact.\n\n"
                "Tow–Thomas variant\n"
                "Tow–Thomas is the same family with a rearranged summer.  A useful rule of thumb: "
                "in Tow–Thomas, if you retune f₀ the bandwidth in Hz may stay more nearly constant "
                "(so Q changes); in the classic KHN-style state-variable, fractional bandwidth is "
                "often what stays steadier as you move f₀.\n\n"
                "When to pick it\n"
                "Reach for this topology when Q must be high (laboratory filters, parametric EQ, "
                "synthesizer cores) or when you need several aligned outputs from one section."
            ),
            "key_params": [
                ("Order", "2nd order per section"),
                ("Simultaneous outputs", "LP, BP, HP  (and notch/AP via summing)"),
                ("Q range", "0.5 – 500+"),
                ("Op-amps needed", "3 (basic) or 4 (independent Q control)"),
                ("Tunability", "fc and Q independently adjustable"),
            ],
            "formula": (
                "State-variable design equations (equal integrator caps C):\n"
                "    ω₀ = 1 / (R₄ C)   [integrator sets frequency]\n"
                "    Q  = (1 + R_B/R_A) / 3   [summing amp gain sets Q]\n"
                "    or with 4th amp: Q set independently by R_Q.\n\n"
                "LP output:  H_LP(s) = ω₀² / (s² + (ω₀/Q)s + ω₀²)\n"
                "BP output:  H_BP(s) = (ω₀/Q)s / (s² + (ω₀/Q)s + ω₀²)\n"
                "HP output:  H_HP(s) = s² / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "Notch = LP + HP outputs summed.\n"
                "All-pass = LP − BP + HP (with correct weighting)."
            ),
            "usage": [
                "Precision laboratory measurement filters.",
                "Tunable frequency selection in spectrum analyzers.",
                "Parametric audio equalizers.",
                "Control system notch compensation.",
            ],
            "real_examples": [
                "MAX274/MAX275 integrated state-variable 8th/4th-order filter ICs.",
                "Analog synthesizer voltage-controlled filter (VCF) modules.",
                "Geophone signal conditioning in seismology.",
            ],
            "design_notes": (
                "• High Q circuits are sensitive to component mismatch — use matched resistors.\n"
                "• More op-amps = more power = more noise, but far better performance.\n"
                "• Op-amp GBW requirement is only ≈ 3Q × ω₀ (much less than Sallen-Key's 90Q²).\n"
                "• Layout matters for high Q — keep integrator loops short."
            ),
            "waveform": {
                "kind": "state_variable",
                "params": {"f0": 1000, "Q": 5},
            },
        },
        "Sallen-Key High-Pass": {
            "icon": "📈",
            "summary": (
                "The Sallen-Key (VCVS) high-pass is the dual of the Sallen-Key low-pass: two "
                "capacitors in series to the non-inverting op-amp input, with resistors defining "
                "feedback from output to the intermediate node.  Like the LPF, it uses a single "
                "op-amp, preserves a non-inverting output, and trades off gain against Q.\n\n"
                "Dual relationships map LP design equations by replacing R⇄C and s⇄1/s in the "
                "passive prototype.  For equal capacitor values and matched resistor ratios, "
                "ω₀ and Q are set similarly to the low-pass case, with Butterworth Q = 0.707 again "
                "requiring a specific closed-loop gain (K) or unequal components.\n\n"
                "Use cases include AC coupling with controlled high-pass shaping, subsonic removal "
                "in audio, DC blocking with mild in-band shaping, and as a stage in band-pass "
                "synthesis when cascaded with low-pass sections."
            ),
            "key_params": [
                ("Order", "2nd order"),
                ("Roll-off", "+40 dB/decade below f₀ (high-pass)"),
                ("Typical Q", "0.5 – 5 (same practical limits as SK LPF)"),
                ("Op-amps", "1"),
                ("Polarity", "Non-inverting"),
            ],
            "formula": (
                "Canonical 2nd-order high-pass with gain K:\n"
                "    H(s) = K · s² / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "Component algebra parallels the low-pass Sallen-Key; for unequal C1, C2 and R1, R2 "
                "to the virtual reference node:\n"
                "    ω₀² = 1 / (R1·R2·C1·C2)\n"
                "    Q depends on K and the same resistor/capacitor sums as the LPF dual.\n\n"
                "Equal-value designs: choose C, compute R from ω₀, then trim K (Ra, Rb) for Q."
            ),
            "usage": [
                "DC-block and subsonic filters in audio interfaces.",
                "High-pass reconstruction after DAC with defined corner.",
                "Cascade with Sallen-Key LPF to realize a band-pass skirt.",
            ],
            "real_examples": [
                "Phono / RIAA preamp: subsonic high-pass near 20 Hz, 2nd-order SK.",
                "Biomedical: AC coupling with defined phase at 0.05–5 Hz.",
            ],
            "design_notes": (
                "• Same GBW rules as SK LPF: op-amp bandwidth ≫ Q·f₀ (often use 50–100× f₀).\n"
                "• High-pass sections amplify noise at very high f — check unity-gain bandwidth.\n"
                "• For steep band-pass, prefer state-variable or MFB BP rather than cascaded SK HP+LP "
                "if Q or alignment must be tight."
            ),
            "waveform": {
                "kind": "active_highpass_2nd",
                "params": {"f0": 800, "Q": 0.707, "gain": 1, "f_input_low": 200, "f_input_high": 3200},
            },
        },
        "Sallen-Key Band-Pass": {
            "icon": "🎯",
            "summary": (
                "What you are trying to build\n"
                "A band-pass keeps a band of frequencies and rejects those that are lower and higher.  "
                "A narrow peak (high Q) needs a second-order band-pass transfer function with a clear "
                "center frequency f₀ and bandwidth.\n\n"
                "Why pure Sallen–Key band-pass is uncommon\n"
                "You can build band-pass variants with one op-amp in the Sallen–Key style, but they "
                "usually support only moderate Q and need awkward resistor spreads.  Most catalogs "
                "emphasize Sallen–Key low-pass and high-pass first.\n\n"
                "Practical choices (in order of how often they appear)\n"
                "• Wide passband: cascade a first-order high-pass and a first-order low-pass so the "
                "two corners define the band.\n"
                "• Medium Q with one op-amp: use the MFB band-pass entry in this tree.\n"
                "• Higher Q, or you need matching low-pass, band-pass, and high-pass taps: use the "
                "state-variable (KHN) biquad.\n\n"
                "Use this topic as a decision guide: single non-inverting op-amp simplicity versus "
                "what actually meets your Q and tuning requirements."
            ),
            "key_params": [
                ("Practical Q", "Often < 3 for single-amp SK-style BP without exotic spreads"),
                ("Alternative", "MFB BP or BP output of state-variable biquad"),
                ("Bandwidth", "BW ≈ f₀/Q (for classical biquad BP)"),
            ],
            "formula": (
                "Standard 2nd-order band-pass (conceptual target):\n"
                "    H(s) = H₀ · (ω₀/Q)s / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "Peak gain |H(jω₀)| = H₀.  Equal-R equal-C SK networks rarely hit arbitrary (f₀,Q) "
                "without wide resistor ratios — numerically optimize or switch topology.\n\n"
                "Wideband passband: H(s) ≈ H_hp(s) · H_lp(s) with different corners fL ≪ fH."
            ),
            "usage": [
                "Wide IF or audio band definition via HP+LP cascade.",
                "When a spare op-amp channel exists, prefer MFB or SV for defined Q.",
            ],
            "real_examples": [
                "Audio crossover region: loosely defined BP via 300 Hz HP + 3 kHz LP (not minimal SK BP).",
            ],
            "design_notes": (
                "• If your spec says Q > 5 and one op-amp: use MFB band-pass.\n"
                "• State-variable gives BP output with same ω₀ as LP/HP taps — best for alignment."
            ),
            "waveform": {
                "kind": "active_bandpass_2nd",
                "params": {"f0": 1200, "Q": 3, "gain": 1, "f_input": 1200, "f_input_off": 400},
            },
        },
        "MFB Band-Pass": {
            "icon": "📻",
            "summary": (
                "What it is\n"
                "The multiple-feedback (MFB) band-pass is a single-op-amp circuit with two capacitors "
                "and several resistors.  The signal enters the inverting summing node; the passive "
                "network creates two poles and an s-term in the numerator so the response peaks at f₀.\n\n"
                "Strengths and limits\n"
                "In one package you get moderate to fairly high Q (roughly into the low twenties on a "
                "real board) with equations that appear in standard filter handbooks.  Output is "
                "inverted compared with Sallen–Key; add another inverter only if absolute phase matters.\n\n"
                "Typical applications\n"
                "Tone and carrier detection, narrow channel selection in instruments, and anywhere you "
                "want a sharp peak without committing to a three-op-amp biquad."
            ),
            "key_params": [
                ("Order", "2nd-order band-pass"),
                ("Polarity", "Inverting"),
                ("Typical Q", "2 – 25"),
                ("Op-amps", "1"),
            ],
            "formula": (
                "Standard form:\n"
                "    H(s) = −G · (ω₀/Q)s / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "Design: choose C1, C2 (often equal), then solve R-set for ω₀, Q, and midband gain G.  "
                "Exact symbolic solutions appear in filter cookbooks (Van Valkenburg, Williams/Taylor).  "
                "Use simultaneous equations from coefficient matching.\n\n"
                "Sensitivity: high-Q designs demand tight tolerances (1% or better on R, low-drift C)."
            ),
            "usage": [
                "Carrier or tone detection (FSK, DTMF-style narrow channels).",
                "Narrowband noise measurements and tracking filters.",
            ],
            "real_examples": [
                "1 kHz tone detector: Q = 12 MFB band-pass in handheld test gear.",
            ],
            "design_notes": (
                "• Verify op-amp GBW for peak gain × effective Q.\n"
                "• Layout: keep summing node short; stray C kills Q.\n"
                "• For Q > 25, migrate to state-variable / Tow-Thomas."
            ),
            "waveform": {
                "kind": "active_bandpass_2nd",
                "params": {"f0": 1000, "Q": 8, "gain": 1, "f_input": 1000, "f_input_off": 250},
            },
        },
        "MFB High-Pass": {
            "icon": "⬆️",
            "summary": (
                "The MFB high-pass is the companion to the MFB low-pass: inverting, one op-amp, "
                "different R–C placement so the numerator is s² while maintaining a second-order "
                "denominator.\n\n"
                "You get steeper skirts than a 1st-order RC HP and can realize alignment (e.g. "
                "Butterworth HP stages in a composite filter) with gains set by resistor ratios.  "
                "Like all MFB circuits, watch sensitivity and noise gain at high frequency "
                "where capacitors short the feedback network.\n\n"
                "Often used when the rest of the chain is already inverting or when board space "
                "forbids a 3-op-amp solution."
            ),
            "key_params": [
                ("Order", "2nd order"),
                ("Roll-off", "+40 dB/decade below ω₀"),
                ("Polarity", "Inverting"),
            ],
            "formula": (
                "Canonical:\n"
                "    H(s) = −K · s² / (s² + (ω₀/Q)s + ω₀²)\n\n"
                "Design proceeds like MFB LPF with element roles swapped in the reactance network; "
                "use cookbook tables or symbolic solver for R1..R3, C1, C2 from (ω₀, Q, K).\n\n"
                "After layout, always simulate with real op-amp models and parasitics."
            ),
            "usage": [
                "High-pass shelving in multi-pole crossover or measurement filter banks.",
                "AC front-end after sensors when inversion is acceptable.",
            ],
            "real_examples": [
                "Multi-stage anti-alias: MFB HP @ 8 Hz + LPF before sigma-delta ADC.",
            ],
            "design_notes": (
                "• If non-inverting HP is required with one amp, use Sallen-Key HP instead.\n"
                "• Check stability: stray feedback at very high f can peak undesirably — small series "
                "resistors with caps sometimes added for op-amp stability."
            ),
            "waveform": {
                "kind": "active_highpass_2nd",
                "params": {"f0": 600, "Q": 1.0, "gain": 1, "f_input_low": 150, "f_input_high": 2400},
            },
        },
        "Kerwin–Huelsman–Newcomb (KHN) Biquad": {
            "icon": "🔷",
            "summary": (
                "The KHN biquad is the original name for what many textbooks call the "
                "3-op-amp state-variable filter.  It consists of a summing amplifier plus two "
                "integrators in a loop, producing low-pass and band-pass at integrator outputs "
                "and high-pass at the summer.\n\n"
                "The structure is theoretical reference for modular filter design: ω₀ set by "
                "integrator R–C products, Q set by feedback gains around the summer.  Variants add "
                "a fourth op-amp to decouple Q tuning from other parameters.\n\n"
                "Tow-Thomas and related two-integrator-loop forms are topology rearrangements "
                "with the same biquadratic denominator but different numerator access — compare "
                "sensitivity and tuning equations when choosing."
            ),
            "key_params": [
                ("Outputs", "LP, BP, HP simultaneously (same denominator)"),
                ("Integrators", "2 (each −1/(RCs) block)"),
                ("Q range", "Very high achievable with matched parts"),
            ],
            "formula": (
                "With integrators −1/(R_int·C·s) each:\n"
                "    Denominator:  s² + (ω₀/Q)s + ω₀²  (standard)\n"
                "    BP: proportional to (ω₀/Q)s / D(s)\n"
                "    LP: ω₀² / D(s);  HP: s² / D(s)\n\n"
                "ω₀ ≈ 1/(R_int·C) for equal-time-constant design; exact Q depends on summer gains "
                "and path weights (see state-variable topic for resistor tuning)."
            ),
            "usage": [
                "Same as state-variable: lab instruments, analyzers, parametric EQ, analog synth VCFs.",
            ],
            "real_examples": [
                "University lab exercises: discrete KHN on breadboard for 1–10 kHz tunable BP.",
                "ICs like MF10/LTC1060 use switched-capacitor equivalents of integrator loops.",
            ],
            "design_notes": (
                "• KHN and Tow-Thomas differ in sensitivity patterns — compare with SPICE before ASIC.\n"
                "• For teaching: draw the two integrator loop explicitly to show state variables x1, x2."
            ),
            "waveform": {
                "kind": "state_variable",
                "params": {"f0": 1000, "Q": 8},
            },
        },
        "Fliege Biquad": {
            "icon": "⚡",
            "summary": (
                "The Fliege biquad is a dual-integrator filter structure using two op-amps "
                "(plus a third for summed outputs in some variants) with a symmetric placement of "
                "resistors and capacitors chosen for low passive sensitivity and equal resistor "
                "values in many normalized designs.\n\n"
                "It can realize low-pass, band-pass, high-pass, and notch by weighted summation "
                "of internal node voltages.  Compared to single-amp MFB, you trade component count "
                "for easier tuning and sometimes better center-frequency stability.\n\n"
                "Fliege networks appear in precision audio and measurement circuits where matched "
                "resistor networks are available."
            ),
            "key_params": [
                ("Op-amps", "Typically 2–3"),
                ("Highlight", "Balanced sensitivities; equal-R designs possible"),
            ],
            "formula": (
                "Derive from two integrator blocks with cross-coupling; standard biquad D(s) as usual.  "
                "Detailed resistor design equations are lengthier — use filter design software or "
                "Fliege’s published tables normalized to ω₀ = 1 rad/s.\n\n"
                "Notch: sum LP and HP (or equivalent) with coefficient 1 and −1 for perfect null at ω₀."
            ),
            "usage": [
                "Low-distortion audio filters where resistor matching is feasible.",
                "Bench-built notch and BP stages with hand-matched metal-film arrays.",
            ],
            "real_examples": [
                "Custom hum notch: Fliege-derived 50/60 Hz trap in precision scale instrumentation.",
            ],
            "design_notes": (
                "• If only two op-amps and modest Q, verify startup and saturation with SPICE.\n"
                "• Fliege vs Tow-Thomas: pick based on published sensitivity for your Q and gain."
            ),
            "waveform": {
                "kind": "active_bandpass_2nd",
                "params": {"f0": 1500, "Q": 6, "gain": 1, "f_input": 1500, "f_input_off": 500},
            },
        },
        "Akerberg–Mossberg Biquad": {
            "icon": "🜁",
            "summary": (
                "The Akerberg–Mossberg circuit is another three-op-amp biquad variant in the "
                "two-integrator-loop family.  It was introduced to improve Q sensitivity and "
                "dynamic range relative to some earlier state-variable arrangements.\n\n"
                "It provides low-pass, band-pass, and high-pass outputs similar to KHN/Tow-Thomas "
                "but with different internal feeding of the summer and minor modifications to how "
                "damping is injected.  Designers choose it when SPICE sweeps show lower component "
                "spread or better noise for a given supply in narrowband applications.\n\n"
                "Conceptually: same second-order pole set, alternate routing of signals."
            ),
            "key_params": [
                ("Op-amps", "3 (typical)"),
                ("Class", "Two-integrator loop / state-variable family"),
            ],
            "formula": (
                "Maintain standard denominator s² + (ω₀/Q)s + ω₀².  Specific AM coefficient formulas "
                "match Ra, Rb, Rq around the input summer and integrators — consult specialty texts "
                "(e.g. J. Williams, “Analog Filter and Circuit Design”) for step-by-step tables.\n\n"
                "Always normalize to ω₀ first, scale impedances second, denormalize with physical C."
            ),
            "usage": [
                "High-Q band-pass where Tow-Thomas sensitivity is marginal on paper.",
                "Professional audio / telecom filtering with tight specs.",
            ],
            "real_examples": [
                "Discrete AM biquad at 455 kHz IF (scaled components; layout critical).",
            ],
            "design_notes": (
                "• Benchmark against Tow-Thomas in Monte Carlo for your technology node.\n"
                "• Parasitic input C on summing nodes moves effective ω₀ — guard-ring sensitive nodes."
            ),
            "waveform": {
                "kind": "state_variable",
                "params": {"f0": 2000, "Q": 12},
            },
        },
        "Twin-T Active Notch": {
            "icon": "🪃",
            "summary": (
                "The passive Twin-T network alone gives a deep null at one frequency but is "
                "poorly isolated from source and load.  Wrapping it with an op-amp follower or "
                "controlled positive feedback sharpens the notch (higher Q) and buffers terminals.\n\n"
                "The classic RC twin-T uses three resistors and three capacitors in a bridged-T layout "
                "with matched 2:1 component ratios for symmetry.  A small gain trim around the "
                "amplifier sets exact Q and center frequency drift due to tolerances.\n\n"
                "Active twin-T is a single-frequency reject tool — hum, VLF mechanical resonance, "
                "carrier bleed — where a full state-variable notch would be overkill."
            ),
            "key_params": [
                ("Null depth", "40–60 dB practical with 1% RC"),
                ("Q enhancement", "Positive feedback via divided output boosts Q (watch oscillation)"),
            ],
            "formula": (
                "Symmetric twin-T: for notch at f0, choose R, C with τ = RC = 1/(2π f0).  "
                "Bridge arms: 2R and 2C with center shunt R/2 or C/2 depending on topology variant.\n\n"
                "Transfer near ω₀ behaves like band-reject biquad with finite Q set by active boost.\n"
                "Simulate trim sensitivity: 0.1% RC mismatch can cut null from 60 dB to 25 dB."
            ),
            "usage": [
                "50/60 Hz mains hum removal in measurement front-ends.",
                "Narrow interference cancellation before high-gain stages.",
            ],
            "real_examples": [
                "EE lab: audio Twin-T with multi-turn trim pot for 59.5–60.5 Hz hum null.",
            ],
            "design_notes": (
                "• Use matched caps (same batch) for symmetric T.\n"
                "• Limit positive feedback so loop never meets Barkhausen at f0.\n"
                "• For tunable notch, consider switched-cap or state-variable instead."
            ),
            "waveform": {
                "kind": "notch",
                "params": {"f0": 60, "Q": 20},
            },
        },
        "GIC & Antoniou Inductor Simulation": {
            "icon": "🌀",
            "summary": (
                "A generalized immittance converter (GIC) — the best-known is Antoniou’s circuit "
                "using two op-amps and five impedances — can synthesize a grounded inductor or "
                "frequency-dependent negative resistance (FDNR) from resistors and capacitors only.\n\n"
                "That lets you implement LC ladder prototypes (doubles-terminated passive ladders) "
                "with no magnetic components, preserving low sensitivity of passive ladder filters "
                "at audio to low-RF frequencies.\n\n"
                "Typical flow: synthesize normalized ELLIPTIC / Chebyshev ladder as passive LCR, "
                "then replace inductors by GIC D-element or L-simulation subcircuits, scale "
                "impedances for op-amp drive capability."
            ),
            "key_params": [
                ("Op-amps", "2 per simulated L (classic Antoniou)"),
                ("Strength", "Best stopband / sensitivity for elliptic LC prototypes"),
                ("Limit", "Frequency limited by op-amp BW and noise in inner loops"),
            ],
            "formula": (
                "Antoniou GIC: with Z2Z5 = Z1Z3Z4/C in the standard diagram, port impedance looking "
                "into the terminal mimics L ~ R1·R3·C / R2 (exact formula depends on which port is "
                "grounded — follow textbook diagram carefully).\n\n"
                "Bruton FDNR transform: scale each ladder branch by 1/s to turn L→C, C→D (supercapacitor "
                "element), R→R — implemented with modified GIC networks."
            ),
            "usage": [
                "Very sharp anti-alias and reconstruction with elliptic stopband zeros.",
                "Audio graphic / parametric EQ using ladder prototypes.",
            ],
            "real_examples": [
                "Discrete 4th-order elliptic anti-alias before 192 kHz audio ADC.",
            ],
            "design_notes": (
                "• DC bias paths: every op-amp input must have a DC reference — add large resistors as needed.\n"
                "• Dynamic range: internal nodes can swing more than I/O — check every op-amp output.\n"
                "• Layout symmetry reduces common-mode feedthrough."
            ),
            "waveform": {
                "kind": "gic_inductor_z_concept",
                "params": {"Leff": 3.3e-6},
            },
        },
        "Active Leapfrog (LF) Ladder": {
            "icon": "🪜",
            "summary": (
                "Leapfrog (or active-leapfrog / LF) filters mimic the signal-flow graph of "
                "a passive LC ladder by chaining integrators and scaled summers so each "
                "stage corresponds to a series arm or shunt arm of the prototype ladder.\n\n"
                "Unlike brute-force biquad cascades, leapfrog structures often have lower element "
                "sensitivity (closer to the passive doubly-terminated reference) and natural "
                "scaling for dynamic range stage by stage.  The cost is more op-amps and more "
                "complex design equations.\n\n"
                "Common in low-pass elliptic prototypes derived from LC ladders; pairs naturally "
                "with GIC-simulated inductors as an alternate realization of the same prototype."
            ),
            "key_params": [
                ("Structure", "Chain of integrators / summers mirroring ladder arms"),
                ("Sensitivity", "Often better than isolated biquad cascade for same order"),
                ("Complexity", "Higher op-amp count and tuning effort"),
            ],
            "formula": (
                "Start from normalized LC ladder voltages and currents; write state equations; map each "
                "state to an integrator output with appropriate summing weights.  Textbooks (Sedra/Smith "
                "advanced sections, Johns & Martin) give matrix methods.\n\n"
                "Simulation with ideal blocks first, then degrade to real op-amp macromodels."
            ),
            "usage": [
                "High-order low-pass and band-pass with stringent stopband masks.",
                "Professional audio mastering-grade filters.",
            ],
            "real_examples": [
                "7th-order elliptic leapfrog BP in research-grade lock-in amplifier front-end.",
            ],
            "design_notes": (
                "• Label states to match ladder; debugging is easier when correspondence is 1:1.\n"
                "• Saturation: optimize internal scale factors before fixing final gain.\n"
                "• For odd order, first-order arm appears as single integrator + feed path."
            ),
            "waveform": {
                "kind": "bode_comparison",
                "params": {"family": "chebyshev", "orders": [4]},
            },
        },
        "OTA-C (Transconductance-C) Filters": {
            "icon": "💠",
            "summary": (
                "OTA-C (also gm-C) filters use voltage-controlled transconductors "
                "(operational transconductance amplifiers, OTAs) driving capacitors to ground.  "
                "Each Integrator is approximated as gm / (sC); summers are likewise OTAs.\n\n"
                "On-chip, no large resistors are needed — tunable gm via bias current sets ω₀ "
                "and sometimes Q, enabling VCFs, channel filters, and continuum tunable front-ends "
                "in CMOS/BiCMOS.\n\n"
                "Trade-offs: linear range (linear tunable gm is hard), noise, parasitic poles "
                "at fT/β, and distortion — but integrated active-RC at multi-MHz often loses "
                "to gm-C."
            ),
            "key_params": [
                ("Control", "Ibias → gm → time constants"),
                ("Freq range", "hundreds of kHz to GHz class (process dependent)"),
                ("Typical on-chip", "Gm-C biquad + automatic tuning loop"),
            ],
            "formula": (
                "Integrator:  Vout/Vin ≈ gm / (sC)  for grounded capacitor at output node.\n\n"
                "Biquad: arrange OTAs to match state-variable signal-flow graph with gm/C replacing 1/R.\n\n"
                "ω₀ ∝ gm/C; matching many gm/C ratios tracks on same die if layout is symmetric."
            ),
            "usage": [
                "Bluetooth / WLAN analog baseband channel select (historically; many now digital).",
                "Software-radio tunable IF strips in research.",
                "Analog synthesizer exponential V/oct VCF cores on custom ASIC.",
            ],
            "real_examples": [
                "CMOS 3rd-order Butterworth Gm-C LPF at 10.7 MHz IF.",
            ],
            "design_notes": (
                "• Add common-mode feedback on high-swing nodes in fully differential Gm-C.\n"
                "• Automatic quality-factor tuning loops inject low-level test tones or use PLL references.\n"
                "• Monte Carlo on gm mismatch predicts packaged yield."
            ),
            "waveform": {
                "kind": "otac_integrator_concept",
                "params": {"gm": 0.35e-3, "C": 4e-12},
            },
        },
        "Switched-Capacitor Filters": {
            "icon": "🔁",
            "summary": (
                "Switched-capacitor (SC) circuits use non-overlapping clocks to move charge "
                "between capacitors, emulating a resistor whose value is ≈ 1/(fs·C) (for basic "
                "stray-insensitive integrators).  The equivalent time constant scales with clock "
                "frequency, so tunable and matched filters track fs on chip.\n\n"
                "SC filters dominated early PCM telephony and still appear in precision ADCs, "
                "sensor ASICs, and integrated anti-alias assistants (often fronting digital).  "
                "They are sampled-data systems: response repeats around multiples of fs — "
                "anti-alias before SC + reconstruction after matter.\n\n"
                "Design uses z-domain math (bilinear links to s-domain) or vendor tools for "
                "biquad ladders in Baxter / Fleischer-Laker style."
            ),
            "key_params": [
                ("Clock", "fs sets effective RC; must >> signal bandwidth N·BW rule of thumb"),
                ("Artifacts", "Clock feedthrough, 1/f noise folded, aliasing"),
            ],
            "formula": (
                "Parasitic-insensitive SC integrator: ΔVout/ΔVin ≈ −(Ci/Cf)·z⁻¹ / (1 − z⁻¹) in simplest form; "
                "map to s via z = e^(sT) for fs ≫ fc.\n\n"
                "Effective R ≈ T/C for charge-transfer equivalence in classic analysis.\n\n"
                "Use SPICE with PSS or discrete-time simulator for exact noise and leakage."
            ),
            "usage": [
                "Voice-band CODECs, precision weigh-scale ADC front-ends.",
                "Integrated 5th–8th order LPF after sigma-delta modulator.",
            ],
            "real_examples": [
                "MF10 switched-capacitor filter building-block IC + external clock for audio lab demos.",
            ],
            "design_notes": (
                "• Always simulate with real switch models (Ron, charge injection).\n"
                "• Provide clean non-overlapping clocks; avoid shoot-through between rails.\n"
                "• For wideband continuous-time paths, consider Gm-C instead."
            ),
            "waveform": {
                "kind": "switched_cap_concept",
                "params": {"f_sig": 650, "f_clk": 18000},
            },
        },
        "N-Path & Sampled-Analog Filters": {
            "icon": "🔀",
            "summary": (
                "N-path filters exploit rotating or commutating networks: the signal is "
                "split into N parallel branches each sampled or multiplied by a periodic carrier "
                "at f_clk/N.  Aliasing and image replication shape a band-pass characteristic "
                "around harmonics of the clock — historically important in early SAW-alternative RF "
                "and channelizing.\n\n"
                "Modern quadrature / complex N-path mixers in integrated receivers achieve "
                "tunable RF band-pass with MOSFET switches and heavy digital calibration.\n\n"
                "These are strongly discrete-time / periodic: classical Laplace analysis is "
                "replaced by cyclostationary or harmonic balance methods for accurate prediction."
            ),
            "key_params": [
                ("Clocking", "Defines center frequency / path phasing"),
                ("Image rejection", "Depends on path matching and baseband filtering"),
            ],
            "formula": (
                "Idealized N-path: frequency translation by ±k·f_clk  images; baseband prototype Hbb(z) "
                "maps to RF via convolution with clock spectrum.\n\n"
                "Use spectre RF, Cadence HB, or custom Python for multi-harmonic analysis.\n\n"
                "Frequently paired with complex FIR/IIR digital compensation."
            ),
            "usage": [
                "RF tunable band-pass in cellular receivers (CMOS switch-cap N-path).",
                "Historical FFT analog channel banks.",
            ],
            "real_examples": [
                "Commercial CMOS receiver: 4-path band-pass at 1–2 GHz with digital calibration.",
            ],
            "design_notes": (
                "• Harmonics of LO alias in-band — specify stopbands in z-domain equivalent.\n"
                "• Mismatch between paths shows as image and LO leakage — layout symmetry first.\n"
                "• Compare power vs continuous-time Gm-C at your target band before committing."
            ),
            "waveform": {
                "kind": "npath_comb_concept",
                "params": {"f_center": 0.95e9, "f_clk": 120e6, "k_max": 3},
            },
        },
        "All-Pass Filter": {
            "icon": "🔀",
            "summary": (
                "An all-pass network keeps the magnitude response flat (unity gain versus frequency) "
                "while rotating phase.  Poles and zeros are placed so amplitude stays constant but "
                "group delay changes with frequency.\n\n"
                "Order and phase swing\n"
                "A first-order section sweeps roughly 180° of phase.  A second-order section can sweep "
                "up to about 360° as you move from DC to high frequency.\n\n"
                "Where it is used\n"
                "Use all-pass stages when you must time-align spectral regions without changing their "
                "level — loudspeaker crossovers, delay equalization in communication links, phased "
                "arrays, and loop compensation where phase margin must be nudged without altering gain."
            ),
            "key_params": [
                ("Gain (magnitude)", "|H(jω)| = 1 for all ω"),
                ("Phase range", "0° to −180° (1st order) or 0° to −360° (2nd order)"),
                ("Group delay at DC", "τ = 2RC  (1st order)"),
            ],
            "formula": (
                "1st-order all-pass:\n"
                "    H(s) = (1 − sRC) / (1 + sRC)\n"
                "    Phase: ∠H(jω) = −2·arctan(ωRC)\n"
                "    Group delay: τ(ω) = 2RC / (1 + (ωRC)²)\n\n"
                "2nd-order all-pass:\n"
                "    H(s) = (s² − (ω₀/Q)s + ω₀²) / (s² + (ω₀/Q)s + ω₀²)\n"
                "    Phase: shifts through −360° as ω goes from 0 to ∞."
            ),
            "usage": [
                "Phase alignment in loudspeaker crossover networks.",
                "Group-delay equalization in communication links.",
                "Beamforming / phased array pre-conditioning.",
                "Control-loop phase margin adjustment.",
            ],
            "real_examples": [
                "Speaker crossover: all-pass at crossover frequency to align driver phases.",
                "Analog modem equalizer: cascaded all-pass sections flatten group delay.",
            ],
            "design_notes": (
                "• The op-amp implementation is simple: one op-amp with an RC network.\n"
                "• Cascading multiple all-pass sections builds a custom delay profile.\n"
                "• Real op-amps deviate from unity gain at high frequency — watch GBW."
            ),
            "waveform": {
                "kind": "allpass",
                "params": {"R": 10e3, "C": 10e-9},
            },
        },
    },
    "Response Families": {
        "__meta__": {
            "icon": "📊",
            "summary": (
                "A response family (or approximation) fixes the mathematical trade-off between "
                "passband flatness, stopband attenuation, and phase or delay behavior.  It answers “how "
                "should the ideal brick wall be rounded off,” not “which op-amp circuit is used.”\n\n"
                "The same Butterworth or Chebyshev target can be built with Sallen–Key, MFB, or "
                "state-variable hardware — the family picks the pole pattern; the topology realizes it.\n\n"
                "Choosing the family is one of the first decisions after you know bandwidth, ripple, "
                "and how much delay distortion you can accept."
            ),
        },
        "Butterworth (Maximally Flat)": {
            "icon": "📏",
            "summary": (
                "The Butterworth approximation produces the flattest possible passband.  "
                "There is no ripple — the magnitude response is monotonically decreasing.\n\n"
                "An nth-order Butterworth has the magnitude-squared function:\n"
                "    |H(jω)|² = 1 / (1 + (ω/ωc)^(2n))\n\n"
                "At ωc the gain is always −3 dB regardless of order.  Higher order means steeper "
                "transition but more components.  The pole locations are equally spaced on the "
                "left half of a circle of radius ωc in the s-plane.\n\n"
                "Butterworth is the 'default' choice when you have no special requirements."
            ),
            "key_params": [
                ("Passband", "Maximally flat — no ripple"),
                ("Roll-off", "−20n dB/decade for nth order"),
                ("Transient response", "Moderate overshoot/ringing"),
                ("2nd-order Q", "Q = 0.707 (damping ζ = 0.707)"),
            ],
            "formula": (
                "|H(jω)|² = 1 / (1 + (ω/ωc)^(2n))\n\n"
                "For 2nd order:  Q = 0.707,  ζ = 0.707.\n"
                "For 4th order (cascaded biquads): Q₁ = 0.541, Q₂ = 1.307.\n\n"
                "General pole locations on unit circle:\n"
                "    sₖ = ωc · e^(j·π·(2k+n-1)/(2n))   for k = 1..n (left-half only)"
            ),
            "usage": [
                "General-purpose filtering where flatness matters.",
                "Anti-aliasing filters for ADCs.",
                "Audio applications requiring no tonal coloring in passband.",
            ],
            "real_examples": [
                "Standard 4th-order anti-aliasing filter before a 16-bit ADC.",
                "Audio crossover: 4th-order Linkwitz–Riley = two cascaded 2nd-order Butterworth.",
            ],
            "design_notes": (
                "• Butterworth is the safe default if you're unsure.\n"
                "• For sharper cutoff, consider Chebyshev (at the cost of ripple).\n"
                "• For better pulse fidelity, consider Bessel."
            ),
            "waveform": {
                "kind": "bode_comparison",
                "params": {"family": "butterworth", "orders": [1, 2, 4]},
            },
        },
        "Chebyshev Type I": {
            "icon": "〰️",
            "summary": (
                "Chebyshev Type I filters allow ripple in the passband in exchange for a steeper "
                "transition band (faster roll-off) than Butterworth of the same order.\n\n"
                "The ripple amplitude is a design parameter, typically 0.5 dB, 1 dB, or 3 dB.  "
                "More ripple → steeper cutoff.  The magnitude response oscillates (ripples) between "
                "unity and the ripple floor within the passband, then drops monotonically in the "
                "stopband.\n\n"
                "The poles lie on an ellipse in the s-plane (not a circle like Butterworth)."
            ),
            "key_params": [
                ("Passband", "Equiripple — controlled ripple amplitude"),
                ("Roll-off", "Steeper than Butterworth for same order"),
                ("Typical ripple", "0.5 dB, 1 dB, 2 dB, 3 dB"),
                ("Phase", "More nonlinear than Butterworth"),
            ],
            "formula": (
                "|H(jω)|² = 1 / (1 + ε²·Tₙ²(ω/ωc))\n\n"
                "where Tₙ is the nth-order Chebyshev polynomial,\n"
                "ε = √(10^(ripple_dB/10) − 1).\n\n"
                "At ω = ωc, |H| = 1/√(1+ε²) = ripple floor."
            ),
            "usage": [
                "Sharp selectivity needed with tolerable passband flatness loss.",
                "Channel selection in communication receivers.",
                "Anti-aliasing where transition band must be narrow.",
            ],
            "real_examples": [
                "IF filter in FM receiver with 0.5 dB Chebyshev for sharp channel edges.",
                "Industrial data acquisition with 1 dB ripple Chebyshev anti-alias filter.",
            ],
            "design_notes": (
                "• More ripple = steeper cutoff but worse transient response.\n"
                "• Group delay peaking near cutoff can cause ringing on step inputs.\n"
                "• Filter tables give pole Q and frequency ratios for standard ripple values."
            ),
            "waveform": {
                "kind": "bode_comparison",
                "params": {"family": "chebyshev", "orders": [2, 4]},
            },
        },
        "Bessel (Linear Phase)": {
            "icon": "🫧",
            "summary": (
                "Bessel (Thomson) filters are designed for maximally flat GROUP DELAY, which "
                "means approximately linear phase.  This preserves the shape of time-domain "
                "waveforms — pulses pass through with minimal ringing or overshoot.\n\n"
                "The trade-off is the slowest roll-off of any standard approximation.  "
                "A 4th-order Bessel rolls off more gently than a 2nd-order Butterworth near cutoff.\n\n"
                "Bessel filters are ideal for pulse / digital waveform transmission, oscilloscope "
                "input filtering, and any application where time-domain fidelity matters more than "
                "frequency-domain selectivity."
            ),
            "key_params": [
                ("Passband", "Approximately flat (not maximally flat in magnitude)"),
                ("Phase", "Approximately linear → constant group delay"),
                ("Roll-off", "Slowest of standard families"),
                ("Step response", "Near-zero overshoot"),
            ],
            "formula": (
                "The Bessel polynomial of order n defines the denominator.\n"
                "For 2nd order:  H(s) = 3 / (s² + 3s + 3)\n"
                "Q = 1/√3 ≈ 0.577,  ω₀ = √3 · ωc.\n\n"
                "Group delay at DC:  τ₀ = n / ωc  (approximately)."
            ),
            "usage": [
                "Oscilloscope input bandwidth limiting.",
                "Pulse shape preservation in digital data links.",
                "Medical waveform capture (ECG, EEG).",
                "Servo and control loop filters where phase linearity matters.",
            ],
            "real_examples": [
                "100 MHz oscilloscope: internal Bessel filter limits bandwidth without distorting edges.",
                "ECG monitor: 4th-order Bessel at 150 Hz to preserve QRS complex shape.",
            ],
            "design_notes": (
                "• Bessel requires higher order than Butterworth for same stopband attenuation.\n"
                "• The −3 dB frequency of a Bessel filter is NOT the design frequency — "
                "the design frequency is defined by group delay, and −3 dB falls at a lower point.\n"
                "• Excellent choice when you measure waveform shape, poor choice when you need "
                "aggressive frequency rejection."
            ),
            "waveform": {
                "kind": "bode_comparison",
                "params": {"family": "bessel", "orders": [2, 4]},
            },
        },
    },
    "Power Supply Filters": {
        "__meta__": {
            "icon": "🔋",
            "summary": (
                "Power supply filters operate in the POWER PATH to reduce ripple, suppress "
                "conducted EMI, and keep supply rails clean.  Unlike signal filters, they must "
                "handle significant current and interact with the converter control loop.\n\n"
                "Key types: smoothing capacitors, RC/CRC, LC/CLC/π, ferrite bead filters, "
                "decoupling networks, and EMI filters (common-mode + differential-mode)."
            ),
        },
        "Smoothing / Reservoir Capacitor": {
            "icon": "🫙",
            "summary": (
                "After a rectifier converts AC to pulsating DC, a large 'reservoir' capacitor "
                "stores charge during voltage peaks and releases it during valleys, smoothing "
                "the waveform into near-DC.\n\n"
                "The ripple voltage depends on load current, capacitance, and ripple frequency.  "
                "For full-wave rectification the ripple frequency is 2× line frequency (100 Hz or "
                "120 Hz).  The capacitor charges near the peak of each half-cycle and discharges "
                "approximately linearly between peaks.\n\n"
                "Larger capacitance reduces ripple but increases inrush current and physical size."
            ),
            "key_params": [
                ("Ripple voltage", "ΔV ≈ I_load / (f_ripple × C)"),
                ("Ripple frequency", "f_line (half-wave) or 2·f_line (full-wave)"),
                ("Inrush current", "Can be very large — limit with NTC or resistor"),
            ],
            "formula": (
                "Approximate peak-to-peak ripple voltage:\n"
                "    ΔV_pp ≈ I_load / (f_ripple × C)\n\n"
                "Ripple factor:\n"
                "    r = ΔV_pp / (2 · V_DC)\n\n"
                "For full-wave rectifier on 50 Hz mains:\n"
                "    f_ripple = 100 Hz\n"
                "    ΔV_pp = I_load / (100 × C)\n\n"
                "Example: 100 mA load, 1000 µF:\n"
                "    ΔV = 0.1 / (100 × 0.001) = 1 V peak-to-peak ripple."
            ),
            "usage": [
                "Linear power supply after bridge rectifier.",
                "Bulk energy storage on DC bus.",
                "Reducing low-frequency ripple before a voltage regulator.",
            ],
            "real_examples": [
                "Bench supply: 4700 µF electrolytic after bridge rectifier, 500 mA load → ~1 V ripple.",
                "Tube amplifier: multiple reservoir caps in CRC π-filter chain.",
            ],
            "design_notes": (
                "• Electrolytic capacitors have ESR that adds resistive loss and limits ripple reduction.\n"
                "• Ripple current rating matters — caps can overheat if ripple current is too high.\n"
                "• Voltage rating must exceed peak rectified voltage + safety margin.\n"
                "• An NTC inrush limiter is often needed to protect the rectifier from initial surge."
            ),
            "waveform": {
                "kind": "rectifier_smoothing",
                "params": {"C": 1000e-6, "I_load": 0.1, "f_line": 50},
            },
        },
        "LC / π / CLC Filter": {
            "icon": "🔗",
            "summary": (
                "An LC filter uses an inductor in series and capacitor(s) to ground for low-loss "
                "smoothing.  A π (pi) filter — typically CLC or CRC — adds a second shunt element "
                "for steeper attenuation.\n\n"
                "In a CLC π-filter, the first C absorbs initial ripple, L blocks AC, and the second "
                "C smooths the output further.  This is extremely common in power amplifiers and "
                "DC supply rails.\n\n"
                "The LC resonance at f0 = 1/(2π√(LC)) must be well below the switching/ripple "
                "frequency.  Damping is critical to prevent resonant peaking."
            ),
            "key_params": [
                ("Resonant frequency", "f0 = 1 / (2π √(LC))"),
                ("Attenuation slope", "−40 dB/decade (single LC section)"),
                ("Damping", "ESR, series R, or parallel RC snubber"),
            ],
            "formula": (
                "LC low-pass:\n"
                "    H(s) = 1 / (s²LC + sRC_damp + 1)\n"
                "    f0 = 1/(2π√(LC))\n\n"
                "π-filter (C-L-C): treat as two cascaded stages.\n"
                "Combined attenuation above f0 is very steep.\n\n"
                "Rule of thumb: choose f0 to be 5–10× below ripple frequency."
            ),
            "usage": [
                "SMPS output filtering.",
                "Audio power amplifier supply rails.",
                "Post-regulator ripple cleanup.",
                "EMI input filtering.",
            ],
            "real_examples": [
                "Class-D amplifier output: 22 µH + 10 µF LC, f0 ≈ 10.7 kHz, switching at 400 kHz.",
                "Vacuum tube supply: 10 H + 47 µF π-filter for 120 Hz ripple.",
            ],
            "design_notes": (
                "• Undamped LC can ring — always add damping.\n"
                "• The filter interacts with the converter's control loop — model carefully.\n"
                "• Capacitor ESR often provides enough damping at higher frequencies.\n"
                "• Multi-section filters (e.g., two-stage LC) give very high attenuation."
            ),
            "waveform": {
                "kind": "lc_lowpass",
                "params": {"L": 22e-6, "C": 10e-6, "R_damp": 1.0, "f_input": 400000},
            },
        },
        "Decoupling / Bypass Capacitors": {
            "icon": "🧊",
            "summary": (
                "Decoupling capacitors are placed physically close to IC power pins to provide "
                "a low-impedance path for high-frequency transient currents.  When a digital IC "
                "switches, it draws sharp current spikes; the decoupling cap supplies this charge "
                "locally instead of forcing it through long PCB traces.\n\n"
                "A typical strategy uses MULTIPLE capacitor values in parallel:\n"
                "  • Bulk cap (10–100 µF electrolytic/tantalum): handles low-freq ripple\n"
                "  • Mid-range cap (1–10 µF ceramic): medium transients\n"
                "  • Local cap (100 nF ceramic): high-frequency decoupling\n"
                "  • Optional: 10–100 pF for very high frequency (GHz digital)\n\n"
                "Each capacitor has self-resonance; above it, the cap becomes inductive.  "
                "Multiple values ensure low impedance across a wide frequency band."
            ),
            "key_params": [
                ("Impedance", "Xc = 1 / (2πfC)  below self-resonance"),
                ("Self-resonance", "f_SR = 1 / (2π√(L_ESL × C))"),
                ("ESR", "Limits minimum impedance at resonance"),
                ("Placement", "As close to IC pin as physically possible"),
            ],
            "formula": (
                "Capacitor impedance:\n"
                "    Z = √(ESR² + (Xc − X_ESL)²)\n"
                "    Xc = 1/(2πfC),  X_ESL = 2πf·ESL\n\n"
                "At self-resonance:  Xc = X_ESL → Z = ESR (minimum).\n\n"
                "Target: keep supply impedance below Z_target at all frequencies of interest.\n"
                "    C_min ≈ I_peak × dt / ΔV_max"
            ),
            "usage": [
                "Every IC on every PCB — this is universal practice.",
                "Mixed-signal boards: separate analog and digital decoupling.",
                "FPGA / processor power integrity.",
                "RF module supply pins.",
            ],
            "real_examples": [
                "STM32 microcontroller: 100 nF + 4.7 µF per VDD pin (per datasheet recommendation).",
                "Op-amp: 100 nF ceramic within 5 mm of each supply pin.",
                "FPGA: arrays of 100 nF + 10 nF + 1 µF across voltage island.",
            ],
            "design_notes": (
                "• Trace/via inductance often dominates over cap value — keep paths SHORT.\n"
                "• Use wide traces or dedicated power planes.\n"
                "• MLCC ceramics (X5R, X7R) are preferred for decoupling — low ESR/ESL.\n"
                "• Voltage derating: use ≥ 2× rated voltage for ceramic caps (voltage coefficients).\n"
                "• Never rely on a single large cap — bandwidth coverage requires multiple values."
            ),
            "waveform": {
                "kind": "impedance_vs_freq",
                "params": {"caps": [100e-9, 10e-6], "ESR": [0.01, 0.05], "ESL": [1e-9, 5e-9]},
            },
        },
        "EMI Filters (CM / DM)": {
            "icon": "🛡",
            "summary": (
                "Electromagnetic Interference (EMI) filters suppress conducted noise on power "
                "lines.  Noise is categorized into two modes:\n\n"
                "DIFFERENTIAL MODE (DM): noise current flows in the same loop as the power current "
                "(line to neutral and back).  Suppressed by X-capacitors and series inductors.\n\n"
                "COMMON MODE (CM): noise current flows from both lines to ground/chassis (earth) "
                "through parasitic capacitances.  Suppressed by common-mode chokes and Y-capacitors.\n\n"
                "A complete EMI filter typically combines:\n"
                "  1. Fuse\n"
                "  2. MOV (surge protection)\n"
                "  3. X-capacitor (DM)\n"
                "  4. Common-mode choke (CM)\n"
                "  5. Y-capacitors to ground (CM)\n"
                "  6. Optional second-stage LC (DM)\n\n"
                "Design must meet regulatory limits (FCC, CISPR, EN55032)."
            ),
            "key_params": [
                ("DM attenuation", "Depends on X-cap value and DM inductor"),
                ("CM attenuation", "Depends on CM choke impedance and Y-caps"),
                ("Safety caps", "X-cap: line-to-line, Y-cap: line-to-ground"),
                ("Frequency range", "150 kHz – 30 MHz (conducted EMI standard)"),
            ],
            "formula": (
                "DM filter insertion loss (simple LC):\n"
                "    IL_DM = 20·log₁₀(1 + (f/f0_DM)²)  [dB, approximate]\n\n"
                "CM choke impedance:\n"
                "    Z_CM = 2πf · L_CM\n"
                "    (leakage inductance provides some DM filtering too)\n\n"
                "Y-cap safety limit: typically ≤ 4.7 nF (class I) or ≤ 2.2 nF (class II) "
                "to limit earth leakage current."
            ),
            "usage": [
                "AC mains input of every commercial power supply.",
                "DC input of automotive and industrial converters.",
                "Meeting EMC compliance (FCC Part 15, CISPR 32, EN55032).",
            ],
            "real_examples": [
                "Laptop charger: CM choke + X2 cap + 2× Y1 caps at AC inlet.",
                "Server PSU: multi-stage EMI filter for stringent CISPR Class B limits.",
                "EV charger: high-current CM choke rated for 50+ amps.",
            ],
            "design_notes": (
                "• Start by measuring conducted emissions, then design filter to achieve margin.\n"
                "• CM choke must not saturate under DC bias current.\n"
                "• X-capacitors must be self-healing and safety-rated (X1 or X2 class).\n"
                "• Y-capacitors must meet safety creepage/clearance and leakage current limits.\n"
                "• PCB layout critically affects CM filter performance — keep CM paths short."
            ),
            "waveform": {
                "kind": "emi_filter_concept",
                "params": {},
            },
        },
    },
}
