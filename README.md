# Analog Electronics Tutorial Explorer

Desktop tutorial app for analog filters and op-amp circuits: dark-themed UI, expandable topic tree, full-text search, and matplotlib waveforms/Bode-style plots per topic.

---

## Table of contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Running the application](#running-the-application)
6. [Project structure](#project-structure)
7. [Architecture](#architecture)
8. [Topic data model](#topic-data-model)
9. [User interface guide](#user-interface-guide)
10. [Search behavior](#search-behavior)
11. [Waveform engine](#waveform-engine)
12. [Customization](#customization)
13. [Full curriculum (all topics)](#full-curriculum-all-topics)
14. [Waveform generator kinds (reference)](#waveform-generator-kinds-reference)

---

## Overview

**Analog Electronics Tutorial Explorer** (v2) is a Python 3 desktop application built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) and embedded [Matplotlib](https://matplotlib.org/) figures. Content is organized into two top-level branches that mirror the code layout:

| Branch | Purpose |
|--------|---------|
| **Filters** | Passive and active filters, classical response families, and power-supply / EMI filtering concepts. |
| **Op-Amp Circuits** | Linear amplifiers, math blocks, comparators, oscillators, special amplifiers, power-amp classes, and RF/discrete small-signal topics. |

Detailed explanations, formulas, bullet lists, and design notes live in Python modules under `topics/` (not in this README), so the app stays data-driven and easy to extend.

---

## Features

- **Tokyo Night–style dark theme** — Panel backgrounds, accent colors, and readable body text tuned for long reading sessions.
- **Topic map** — `ttk.Treeview` with per-node icons; top-level branches expand to categories and leaf topics.
- **Welcome screen** — Short orientation and cards highlighting major areas until you select a topic.
- **Rich topic pages** — Breadcrumb path, title with icon, optional **input/output waveform** plot, then sections for overview, key parameters, formulas, usage, real-world examples, and design notes.
- **Search** — Query matches topic titles, summaries, formulas, design notes, usage lines, and example lines; top results appear under the search bar (minimum query length: 2 characters). **Enter** jumps to the best match.
- **Branch/category pages** — Selecting a folder node shows its `__meta__` overview text only.

---

## Requirements

- **Python** 3.10+ recommended (3.14 tested in development).
- **Operating system** — Windows-friendly paths and `run.bat`; the stack (Tk, CustomTkinter) is cross-platform in principle.

Dependencies (see `requirments.txt` — filename kept as in the repo):

| Package | Role |
|---------|------|
| `customtkinter` | Modern themed widgets and layout. |
| `matplotlib` | Figures for waveforms and frequency-domain plots. |
| `numpy` | Numerical arrays for simulations. |
| `scipy` | Signal processing helpers (`scipy.signal`). |

---

## Installation

From the project directory:

```bash
python -m pip install -r requirments.txt
```

---

## Running the application

**Option A — Python**

```bash
cd "path/to/analog trtorial"
python main.py
```

**Option B — Windows batch file**

Double-click `run.bat`. It checks that `python` is on `PATH`, installs/updates dependencies from `requirments.txt`, then starts `main.py`. If something fails, the window stays open so you can read the error.

---

## Project structure

```
analog trtorial/
├── main.py                 # Application entry point and UI (AnalogTutorialApp)
├── run.bat                 # Windows: install deps + launch
├── requirments.txt         # pip dependencies (intentional filename spelling)
├── README.md               # This file
├── topics/
│   ├── __init__.py         # TOPICS = { Filters, Op-Amp Circuits }
│   ├── filters_branch.py   # FILTERS_BRANCH subtree
│   └── op_amp_branch.py    # OP_AMP_BRANCH subtree
└── waveform_engine/        # Package (not a single .py file)
    ├── __init__.py         # generate_waveform(), merged generator registry
    ├── _core.py            # Agg palette, _make_fig(), helpers
    ├── filters.py          # Filter-branch waveform functions
    └── op_amp.py           # Op-amp / RF / discrete waveform functions
```

---

## Architecture

- **`main.py`** — Defines theme constants, helpers (`_flatten_topics`, `search_topics`), and `AnalogTutorialApp`:
  - Builds top bar (title + search), left sidebar (topic tree + optional search results), and scrollable right pane for content.
  - Populates the tree recursively from `TOPICS`.
  - Renders leaf topics by reading standard keys from each topic dict and calling `waveform_engine.generate_waveform` when a `waveform` spec is present.
- **`topics`** — Aggregates two large dictionaries. Editing `filters_branch.py` or `op_amp_branch.py` updates the tutorial text and structure without touching UI code.
- **`waveform_engine`** — Maps each topic’s `waveform.kind` string to a function that returns a `matplotlib.figure.Figure`. Split into `filters.py` and `op_amp.py` to align with the two curriculum branches.

---

## Topic data model

**Category node** (non-leaf):

- May include `__meta__` with at least `icon` and `summary` (branch introduction).

**Leaf topic** (circuit/concept page):

| Key | Type | Purpose |
|-----|------|---------|
| `icon` | `str` | Emoji or symbol shown in the tree and title. |
| `summary` | `str` | Long-form technical overview. |
| `key_params` | `list[tuple[str, str]]` | Label / value rows for the parameters table. |
| `formula` | `str` | Formulas and explanations (monospace-friendly block). |
| `usage` | `list[str]` | Where the circuit is used. |
| `real_examples` | `list[str]` | Concrete products or design examples. |
| `design_notes` | `str` | Practical tips and warnings. |
| `waveform` | `dict` | Optional. Keys: `kind` (generator name), `params` (numeric/tuple args for the plot). |

---

## User interface guide

1. **Topic map (left)** — Expand **Filters** or **Op-Amp Circuits**, then categories, then select a **leaf** topic for the full article + plot. Selecting a **category** shows only its overview.
2. **Right pane** — Breadcrumb at top, then title, then (if defined) the waveform card, then text sections in a fixed order (see [Features](#features)).
3. **Search (top right)** — Type at least two characters; results list appears above the tree. Click a result or press **Enter** to open the top hit.
4. **Window** — Default geometry `1440×900`, minimum `1100×700` (see `main.py`).

Typography for the tree is controlled by `TOPIC_TREE_FONT_SIZE` and `TOPIC_TREE_ROWHEIGHT` in `main.py`.

---

## Search behavior

Scoring is heuristic (see `search_topics` in `main.py`):

- Strong weight on **title** and **exact title** match.
- Medium weight for matches in `summary`, `formula`, `design_notes`.
- Lower weight for `usage` and `real_examples` lines.
- Small bonus if query words appear in the **category path**.

Up to **20** matches are computed; the UI shows up to **10** as buttons with a full path subtitle.

---

## Waveform engine

- **Entry point:** `from waveform_engine import generate_waveform`
- **Input:** `{"kind": "<string>", "params": {...}}`
- **Output:** `matplotlib.figure.Figure` embedded with `FigureCanvasTkAgg` (TkAgg in `main.py`; generator core uses non-interactive Agg in `_core.py` for figure creation before embedding).
- Unknown `kind` values produce a placeholder figure with a short message.

Filter-related kinds are implemented in `waveform_engine/filters.py`; op-amp, RF, and discrete concepts in `waveform_engine/op_amp.py`. The merged registry is `_GENERATORS` in `waveform_engine/__init__.py`.

---

## Customization

| Goal | Where to look |
|------|----------------|
| Colors / theme | Top of `main.py` (`BG_DARK`, `FG_TEXT`, `SEL_BG`, …) |
| Tree font / row height | `TOPIC_TREE_FONT_SIZE`, `TOPIC_TREE_ROWHEIGHT` |
| Body text size / wrap | `BODY_FONT_SIZE`, `BODY_WRAPLENGTH` |
| Add or edit topics | `topics/filters_branch.py`, `topics/op_amp_branch.py` |
| New plot type | Add `_wf_*` function and register in `FILTER_GENERATORS` or `OPAMP_GENERATORS` |
| Dependencies | `requirments.txt` |

---

## Full curriculum (all topics)

Below is the **complete table of contents** of every leaf topic in the app. Full prose, formulas, and parameters are stored in the Python topic files listed in [Project structure](#project-structure).

### Filters

#### Passive Filters

- RC Low-Pass Filter  
- RC High-Pass Filter  
- RL Low-Pass Filter  
- LC Low-Pass Filter  
- RLC Band-Pass Filter  
- Band-Stop / Notch (Twin-T)  
- RL High-Pass Filter  
- LC High-Pass Filter  
- Series LC Shunt Trap (Band-Stop)  
- Parallel RLC Band-Stop (Nodal)  
- Passive T & π Low-Pass Sections  
- Passive LC Ladder & Coupled Resonators  
- Crystal & Ceramic Resonator Filters  
- Transmission-Line & Stub Filters  
- Passive Lattice All-Pass (Bridge)  

#### Active Filters

- Sallen-Key Low-Pass  
- Multiple Feedback (MFB) Low-Pass  
- State-Variable / Tow-Thomas  
- Sallen-Key High-Pass  
- Sallen-Key Band-Pass  
- MFB Band-Pass  
- MFB High-Pass  
- Kerwin–Huelsman–Newcomb (KHN) Biquad  
- Fliege Biquad  
- Akerberg–Mossberg Biquad  
- Twin-T Active Notch  
- GIC & Antoniou Inductor Simulation  
- Active Leapfrog (LF) Ladder  
- OTA-C (Transconductance-C) Filters  
- Switched-Capacitor Filters  
- N-Path & Sampled-Analog Filters  
- All-Pass Filter  

#### Response Families

- Butterworth (Maximally Flat)  
- Chebyshev Type I  
- Bessel (Linear Phase)  

#### Power Supply Filters

- Smoothing / Reservoir Capacitor  
- LC / π / CLC Filter  
- Decoupling / Bypass Capacitors  
- EMI Filters (CM / DM)  

### Op-Amp Circuits

#### Amplifiers

- Voltage Follower (Buffer)  
- Non-Inverting Amplifier  
- Inverting Amplifier  
- Summing Amplifier (Inverting Summer)  
- Non-Inverting Summer  
- Voltage-Output DAC Buffer & Scaling  
- Differential Amplifier  

#### Math / Signal Processing

- Integrator  
- Differentiator  

#### Comparators / Detectors

- Comparator  
- Schmitt Trigger  
- Peak Detector  
- Precision Rectifier  

#### Oscillators / Waveform Gen

- Wien Bridge Oscillator  
- Relaxation Oscillator  

#### Special Amplifiers & Converters

- Instrumentation Amplifier (INA)  
- Transimpedance Amplifier (TIA)  
- Howland / Voltage-to-Current Converter  
- Log Amplifier  
- Antilog (Exponential) Amplifier  
- Programmable-Gain Amplifier (PGA)  
- Fully Differential Amplifier (FDA)  
- Variable-Gain Amplifier (VGA / AGC Core)  
- Chopper & Autozero Amplifiers  
- Charge Amplifier (Piezo / Capacitive Sensor)  
- Isolation Amplifier  
- Lock-In Amplifier (Synchronous Detection)  

#### Power Amplifiers (Classes A–D)

- Class-A Power Amplifier  
- Class-B & Class-AB Power Amplifier  
- Class-C Power Amplifier  
- Class-D Switching Power Amplifier  
- Class-G & Class-H Power Amplifiers  
- Doherty, Envelope Tracking & Multi-Branch PAs  

#### RF & Discrete Small-Signal Amplifiers

- Low-Noise Amplifier (LNA)  
- RF / IF Power Amplifier (PA)  
- Discrete Buffer (Emitter / Source Follower)  
- Common-Emitter / Common-Source Gain Stage  
- Cascode Amplifier  
- Differential Pair (Emitter- / Source-Coupled)  
- Current Mirror & Ratioed Gain Cell  
- Distributed / Traveling-Wave Amplifier (TWA)  

---

## Waveform generator kinds (reference)

These are the `waveform.kind` strings registered in `waveform_engine` (alphabetical). Each must match a topic’s `waveform` block in `topics/`.

| Kind | Typical branch |
|------|----------------|
| `active_bandpass_2nd` | Filters |
| `active_highpass_2nd` | Filters |
| `active_lowpass_2nd` | Filters |
| `allpass` | Filters |
| `antilog_concept` | Op-Amp |
| `bode_comparison` | Filters |
| `cascode_bw_concept` | Op-Amp / RF |
| `charge_amp_concept` | Op-Amp |
| `chopper_concept` | Op-Amp |
| `class_a_concept` | Op-Amp |
| `class_b_concept` | Op-Amp |
| `class_c_concept` | Op-Amp |
| `class_d_concept` | Op-Amp |
| `class_gh_concept` | Op-Amp |
| `common_emitter_concept` | Op-Amp / RF |
| `comparator` | Op-Amp |
| `crystal_resonator` | Filters |
| `current_mirror_concept` | Op-Amp / RF |
| `dac_buffer_concept` | Op-Amp |
| `diff_amp` | Op-Amp |
| `diff_pair_concept` | Op-Amp / RF |
| `differentiator` | Op-Amp |
| `discrete_follower_rf` | Op-Amp / RF |
| `emi_filter_concept` | Filters |
| `fda_concept` | Op-Amp |
| `follower` | Op-Amp |
| `gic_inductor_z_concept` | Op-Amp / Filters |
| `howland_concept` | Op-Amp |
| `impedance_vs_freq` | Filters |
| `instrumentation_amp` | Op-Amp |
| `integrator` | Op-Amp |
| `inverting_amp` | Op-Amp |
| `isolation_amp_concept` | Op-Amp |
| `lattice_rf_allpass` | Op-Amp / RF |
| `lc_highpass` | Filters |
| `lc_ladder_coupled_concept` | Op-Amp / Filters |
| `lc_lowpass` | Filters |
| `lna_tuned_concept` | Op-Amp / RF |
| `lockin_concept` | Op-Amp |
| `log_amp_concept` | Op-Amp |
| `non_inverting_amp` | Op-Amp |
| `noninv_summer` | Op-Amp |
| `notch` | Filters |
| `npath_comb_concept` | Op-Amp / Filters |
| `otac_integrator_concept` | Op-Amp / Filters |
| `pa_efficiency_arch_concept` | Op-Amp |
| `passive_pi_lp` | Filters |
| `peak_detector` | Op-Amp |
| `pga_concept` | Op-Amp |
| `precision_rectifier` | Op-Amp |
| `rc_highpass` | Filters |
| `rc_lowpass` | Filters |
| `rectifier_smoothing` | Filters |
| `relaxation_osc` | Op-Amp |
| `rf_pa_compression` | Op-Amp / RF |
| `rl_highpass` | Filters |
| `rl_lowpass` | Filters |
| `rlc_bandpass` | Filters |
| `schmitt` | Op-Amp |
| `state_variable` | Filters |
| `summing_amp` | Op-Amp |
| `switched_cap_concept` | Op-Amp / Filters |
| `tl_stub_concept` | Op-Amp / RF |
| `transimpedance` | Op-Amp |
| `traveling_wave_concept` | Op-Amp / RF |
| `vga_concept` | Op-Amp |
| `wien_oscillator` | Op-Amp |

---

*Generated to describe the Analog Electronics Tutorial Explorer codebase. For the latest behavior, prefer reading `main.py` and `topics/__init__.py`.*
