#!/usr/bin/env python3
"""
Analog Electronics Tutorial Explorer  —  v2 (Modern UI)
========================================================
A professional desktop tutorial application with:
  • Dark Tokyo Night themed UI via CustomTkinter
  • Branching expandable topic tree with icons
  • Deep technical content with formulas and design notes
  • Real-time waveform/Bode plots with matplotlib
  • Full-text search across all topics
  • Tabbed detail view: Overview, Formulas, Usage, Examples, Design Notes, Waveform

Requirements:
    pip install customtkinter matplotlib numpy scipy
"""

import sys, os, textwrap, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
import tkinter as tk
from tkinter import font as tkfont

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

from topics import TOPICS
from waveform_engine import generate_waveform

# ── Theme ───────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_DARK    = "#1a1b26"
BG_PANEL   = "#1f2335"
# Topic tree: ttk needs clam + explicit layout on Windows or font settings are ignored.
TOPIC_TREE_FONT_SIZE = 20
TOPIC_TREE_ROWHEIGHT = 56
BG_CARD    = "#24283b"
BG_HOVER   = "#292e42"
FG_TEXT    = "#c0caf5"
FG_DIM     = "#565f89"
FG_HEAD    = "#7aa2f7"
FG_ACCENT  = "#9ece6a"
FG_WARN    = "#ff9e64"
FG_LINK    = "#7dcfff"
BORDER     = "#292e42"
SEL_BG     = "#364a82"

# Readable prose in CTk (no Markdown); tune wrap width for the detail column
BODY_FONT_SIZE   = 14
BODY_WRAPLENGTH  = 920
SECTION_TITLE_SZ = 13

# ── Helpers ─────────────────────────────────────────────────────────
def _format_body_text(text: str) -> str:
    """Normalize topic prose for plain labels: trim, collapse extra blank lines."""
    if not text:
        return text
    t = text.replace("\r\n", "\n").strip()
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t
def _flatten_topics(node, path=(), results=None):
    """Recursively collect all leaf topics and their paths."""
    if results is None:
        results = []
    for key, value in node.items():
        if key == "__meta__":
            continue
        current_path = path + (key,)
        if isinstance(value, dict):
            has_children = any(k != "__meta__" and isinstance(v, dict) for k, v in value.items())
            if has_children:
                _flatten_topics(value, current_path, results)
            else:
                results.append((current_path, value))
    return results


class SearchResult:
    def __init__(self, path, node, score):
        self.path = path
        self.node = node
        self.score = score


def search_topics(query: str, topics: dict, max_results: int = 20):
    """Full-text search across all topic content."""
    query_lower = query.lower().strip()
    if not query_lower:
        return []

    all_leaves = _flatten_topics(topics)
    results = []

    for path, node in all_leaves:
        score = 0
        name = path[-1].lower()

        # Name match is strongest
        if query_lower in name:
            score += 100
        if query_lower == name:
            score += 200

        # Search in all text fields
        for field in ["summary", "formula", "design_notes"]:
            text = node.get(field, "")
            if isinstance(text, str) and query_lower in text.lower():
                score += 30

        for field in ["usage", "real_examples"]:
            items = node.get(field, [])
            if isinstance(items, list):
                for item in items:
                    if query_lower in item.lower():
                        score += 20

        # Path components
        for part in path:
            if query_lower in part.lower():
                score += 15

        if score > 0:
            results.append(SearchResult(path, node, score))

    results.sort(key=lambda r: r.score, reverse=True)
    return results[:max_results]


# ── Main Application ────────────────────────────────────────────────
class AnalogTutorialApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("⚡ Analog Electronics Tutorial Explorer")
        self.geometry("1440x900")
        self.minsize(1100, 700)
        self.configure(fg_color=BG_DARK)

        self._current_canvas = None
        self._current_fig = None
        self._tree_items = {}   # iid → (path_tuple, node_or_None)

        self._build_layout()
        self._populate_tree(TOPICS)
        self._show_welcome()

    # ── Layout ──────────────────────────────────────────────────────
    def _build_layout(self):
        # Top bar
        top = ctk.CTkFrame(self, fg_color=BG_PANEL, height=56, corner_radius=0)
        top.pack(fill="x")
        top.pack_propagate(False)

        ctk.CTkLabel(top, text="⚡ Analog Electronics Tutorial Explorer",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=FG_HEAD).pack(side="left", padx=20, pady=12)

        search_frame = ctk.CTkFrame(top, fg_color=BG_PANEL)
        search_frame.pack(side="right", padx=20, pady=10)

        self._search_var = ctk.StringVar()
        self._search_entry = ctk.CTkEntry(
            search_frame, textvariable=self._search_var,
            placeholder_text="🔍  Search topics, formulas, circuits …",
            width=340, height=34,
            fg_color=BG_CARD, border_color=BORDER, text_color=FG_TEXT,
            placeholder_text_color=FG_DIM,
            font=ctk.CTkFont(size=13))
        self._search_entry.pack(side="left")
        self._search_entry.bind("<KeyRelease>", self._on_search)
        self._search_entry.bind("<Return>", self._on_search_enter)

        # Body: left panel + right panel
        body = ctk.CTkFrame(self, fg_color=BG_DARK)
        body.pack(fill="both", expand=True, padx=0, pady=0)

        # Left sidebar
        left = ctk.CTkFrame(body, fg_color=BG_PANEL, width=400, corner_radius=0)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        lbl = ctk.CTkLabel(left, text="TOPIC MAP",
                           font=ctk.CTkFont(size=18, weight="bold"),
                           text_color=FG_DIM)
        lbl.pack(anchor="w", padx=16, pady=(14, 4))

        # Treeview (use ttk inside CTk)
        tree_container = ctk.CTkFrame(left, fg_color=BG_PANEL)
        tree_container.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self._topic_tree_font = tkfont.Font(
            self, family="Segoe UI", size=TOPIC_TREE_FONT_SIZE, weight="normal"
        )
        style = tk.ttk.Style(self)
        # "clam" honors Treeview font on Windows; "default"/native themes often do not.
        style.theme_use("clam")
        style.layout("Dark.Treeview", style.layout("Treeview"))
        style.configure(
            "Dark.Treeview",
            background=BG_PANEL,
            foreground=FG_TEXT,
            fieldbackground=BG_PANEL,
            borderwidth=0,
            rowheight=TOPIC_TREE_ROWHEIGHT,
            font=self._topic_tree_font,
        )
        style.configure("Dark.Treeview.Heading",
                        background=BG_PANEL,
                        foreground=FG_DIM,
                        borderwidth=0)
        style.map("Dark.Treeview",
                  background=[("selected", SEL_BG)],
                  foreground=[("selected", "#ffffff")])

        self._tree = tk.ttk.Treeview(tree_container, style="Dark.Treeview",
                                      show="tree", selectmode="browse")
        ysb = tk.ttk.Scrollbar(tree_container, orient="vertical", command=self._tree.yview)
        self._tree.configure(yscrollcommand=ysb.set)
        ysb.pack(side="right", fill="y")
        self._tree.pack(side="left", fill="both", expand=True)
        self._tree.bind("<<TreeviewSelect>>", self._on_tree_select)

        # Search results panel (hidden by default)
        self._search_panel = ctk.CTkFrame(left, fg_color=BG_CARD, corner_radius=8)
        self._search_results_widgets = []

        # Right content area
        self._right = ctk.CTkScrollableFrame(body, fg_color=BG_DARK)
        self._right.pack(side="left", fill="both", expand=True, padx=0, pady=0)

    # ── Tree population ─────────────────────────────────────────────
    def _populate_tree(self, topics, parent="", path=()):
        for key, value in topics.items():
            if key == "__meta__":
                continue
            icon = ""
            current_path = path + (key,)
            if isinstance(value, dict):
                meta = value.get("__meta__", {})
                icon = meta.get("icon", "") if isinstance(meta, dict) else ""
                if not icon and not isinstance(value.get("summary"), str):
                    icon = "📂"
            text = f"{icon}  {key}" if icon else key
            iid = self._tree.insert(parent, "end", text=text, open=(len(path) < 1))
            self._tree_items[iid] = (current_path, value)

            if isinstance(value, dict):
                has_children = any(
                    k != "__meta__" and isinstance(v, dict) for k, v in value.items()
                )
                if has_children:
                    self._populate_tree(value, parent=iid, path=current_path)

    # ── Event handlers ──────────────────────────────────────────────
    def _on_tree_select(self, event=None):
        sel = self._tree.selection()
        if not sel:
            return
        iid = sel[0]
        path, node = self._tree_items.get(iid, ((), None))
        if node is None:
            return

        # Decide what to show
        if isinstance(node, dict):
            meta = node.get("__meta__")
            if meta and isinstance(meta, dict):
                self._show_topic(path, meta, is_category=True)
            elif "summary" in node:
                self._show_topic(path, node, is_category=False)
            else:
                self._show_topic(path, {"summary": "Select a subtopic from the tree."}, is_category=True)
        else:
            self._show_topic(path, {"summary": str(node)}, is_category=False)

    def _on_search(self, event=None):
        query = self._search_var.get().strip()
        if len(query) < 2:
            self._hide_search_results()
            return
        results = search_topics(query, TOPICS)
        self._show_search_results(results)

    def _on_search_enter(self, event=None):
        query = self._search_var.get().strip()
        if not query:
            return
        results = search_topics(query, TOPICS)
        if results:
            self._show_topic(results[0].path, results[0].node, is_category=False)
            self._hide_search_results()

    def _show_search_results(self, results):
        self._hide_search_results()
        if not results:
            return
        self._search_panel.pack(fill="x", padx=8, pady=(0, 8), before=None)
        self._search_panel.pack(fill="x", padx=8, pady=(0, 8))

        header = ctk.CTkLabel(self._search_panel, text=f"  {len(results)} results found",
                              font=ctk.CTkFont(size=11), text_color=FG_DIM)
        header.pack(anchor="w", padx=10, pady=(8, 4))
        self._search_results_widgets.append(header)

        for r in results[:10]:
            path_str = " › ".join(r.path)
            btn = ctk.CTkButton(
                self._search_panel,
                text=f"  {r.path[-1]}",
                anchor="w",
                fg_color="transparent", hover_color=BG_HOVER,
                text_color=FG_LINK, font=ctk.CTkFont(size=12),
                height=28,
                command=lambda rr=r: self._pick_search_result(rr))
            btn.pack(fill="x", padx=6, pady=1)
            self._search_results_widgets.append(btn)

            sub = ctk.CTkLabel(self._search_panel, text=f"     {path_str}",
                               font=ctk.CTkFont(size=10), text_color=FG_DIM)
            sub.pack(anchor="w", padx=10)
            self._search_results_widgets.append(sub)

    def _hide_search_results(self):
        for w in self._search_results_widgets:
            w.destroy()
        self._search_results_widgets.clear()
        self._search_panel.pack_forget()

    def _pick_search_result(self, result):
        self._show_topic(result.path, result.node, is_category=False)
        self._hide_search_results()

    # ── Content rendering ───────────────────────────────────────────
    def _clear_right(self):
        if self._current_canvas:
            self._current_canvas.get_tk_widget().destroy()
            self._current_canvas = None
        if self._current_fig:
            import matplotlib.pyplot as plt
            plt.close(self._current_fig)
            self._current_fig = None
        for w in self._right.winfo_children():
            w.destroy()

    def _show_welcome(self):
        self._clear_right()
        f = self._right

        ctk.CTkLabel(f, text="⚡  Welcome to Analog Electronics Explorer",
                     font=ctk.CTkFont(size=24, weight="bold"),
                     text_color=FG_HEAD).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(f, text="Select any topic from the tree  •  Use search to jump to a circuit",
                     font=ctk.CTkFont(size=14), text_color=FG_DIM).pack(anchor="w", padx=24, pady=(0, 20))

        cards = [
            ("🎛  Filters", "Passive • Active • Power Supply\nRC, LC, Sallen-Key, MFB, State-Variable, EMI …"),
            ("⚙️  Op-Amp Circuits", "Amplifiers • Math Blocks • Comparators • Detectors\nFollower, Inverting, Integrator, Peak Detector …"),
            ("📊  Response Families", "Butterworth • Chebyshev • Bessel • Elliptic\nHow the roll-off shape is chosen"),
            ("🔋  Power Supply Filters", "Smoothing • LC/π • Decoupling • EMI CM/DM\nRipple reduction, EMC compliance"),
        ]
        for title, desc in cards:
            card = ctk.CTkFrame(f, fg_color=BG_CARD, corner_radius=10)
            card.pack(fill="x", padx=24, pady=6)
            ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=15, weight="bold"),
                         text_color=FG_ACCENT).pack(anchor="w", padx=16, pady=(12, 2))
            ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=12),
                         text_color=FG_TEXT, justify="left").pack(anchor="w", padx=16, pady=(0, 12))

        tip = ctk.CTkFrame(f, fg_color=BG_CARD, corner_radius=10)
        tip.pack(fill="x", padx=24, pady=(16, 6))
        ctk.CTkLabel(tip, text="💡 TIP", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=FG_WARN).pack(anchor="w", padx=16, pady=(10, 2))
        ctk.CTkLabel(tip,
                     text="Every leaf topic includes:\n"
                          "  ✦  Deep technical summary\n"
                          "  ✦  All relevant formulas with explanations\n"
                          "  ✦  Key parameters table\n"
                          "  ✦  Real-world application examples\n"
                          "  ✦  Practical design notes & warnings\n"
                          "  ✦  Interactive input/output waveform plots",
                     font=ctk.CTkFont(size=12), text_color=FG_TEXT,
                     justify="left").pack(anchor="w", padx=16, pady=(0, 12))

    def _show_topic(self, path, node, is_category=False):
        self._clear_right()
        f = self._right

        # Breadcrumb
        bc = "  ›  ".join(path)
        ctk.CTkLabel(f, text=bc, font=ctk.CTkFont(size=11), text_color=FG_DIM
                     ).pack(anchor="w", padx=24, pady=(16, 2))

        # Title
        icon = node.get("icon", "") if isinstance(node, dict) else ""
        title_text = f"{icon}  {path[-1]}" if icon else path[-1]
        ctk.CTkLabel(f, text=title_text,
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=FG_HEAD).pack(anchor="w", padx=24, pady=(0, 12))

        if is_category:
            summary = node.get("summary", "") if isinstance(node, dict) else str(node)
            self._add_section("Overview", _format_body_text(summary))
            return

        # ── Full topic rendering ────────────────────────────────────
        summary = node.get("summary", "")
        key_params = node.get("key_params", [])
        formula = node.get("formula", "")
        usage = node.get("usage", [])
        real_examples = node.get("real_examples", [])
        design_notes = node.get("design_notes", "")
        waveform_spec = node.get("waveform")

        # 1. WAVEFORM first (visual hook)
        if waveform_spec:
            self._add_waveform(waveform_spec, f)

        # 2. Overview
        self._add_section("OVERVIEW", _format_body_text(summary))

        # 3. Key parameters
        if key_params:
            self._add_params_table(key_params)

        # 4. Formula
        if formula:
            self._add_formula_section(formula)

        # 5. Usage
        if usage:
            self._add_bullet_section("WHERE IS THIS USED?", usage, FG_ACCENT)

        # 6. Real-world examples
        if real_examples:
            self._add_bullet_section("REAL-WORLD EXAMPLES", real_examples, FG_WARN)

        # 7. Design notes
        if design_notes:
            self._add_section("PRACTICAL DESIGN NOTES", _format_body_text(design_notes), accent=FG_WARN)

    # ── Section widgets ─────────────────────────────────────────────
    def _add_section(self, title, text, accent=FG_HEAD):
        f = self._right
        card = ctk.CTkFrame(f, fg_color=BG_CARD, corner_radius=10)
        card.pack(fill="x", padx=24, pady=(6, 4))

        ctk.CTkLabel(card, text=title,
                     font=ctk.CTkFont(size=SECTION_TITLE_SZ, weight="bold"),
                     text_color=accent).pack(anchor="w", padx=16, pady=(12, 4))

        # Render text with wrapping
        lbl = ctk.CTkLabel(card, text=text,
                           font=ctk.CTkFont(size=BODY_FONT_SIZE),
                           text_color=FG_TEXT, justify="left",
                           wraplength=BODY_WRAPLENGTH)
        lbl.pack(anchor="w", padx=16, pady=(0, 14))

    def _add_formula_section(self, formula_text):
        f = self._right
        card = ctk.CTkFrame(f, fg_color="#1d2230", corner_radius=10)
        card.pack(fill="x", padx=24, pady=(6, 4))

        ctk.CTkLabel(card, text="📐  FORMULAS",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG_LINK).pack(anchor="w", padx=16, pady=(12, 4))

        # Use monospace for formulas
        text_widget = ctk.CTkTextbox(card,
                                      font=ctk.CTkFont(family="Consolas", size=13),
                                      fg_color="#1d2230",
                                      text_color="#e0af68",
                                      border_width=0,
                                      wrap="word",
                                      height=min(max(formula_text.count("\n") + 1, 4) * 22, 400),
                                      activate_scrollbars=False)
        text_widget.pack(fill="x", padx=16, pady=(0, 14))
        text_widget.insert("1.0", formula_text)
        text_widget.configure(state="disabled")

    def _add_params_table(self, params):
        f = self._right
        card = ctk.CTkFrame(f, fg_color=BG_CARD, corner_radius=10)
        card.pack(fill="x", padx=24, pady=(6, 4))

        ctk.CTkLabel(card, text="📋  KEY PARAMETERS",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG_LINK).pack(anchor="w", padx=16, pady=(12, 4))

        table = ctk.CTkFrame(card, fg_color=BG_CARD)
        table.pack(fill="x", padx=16, pady=(0, 14))

        for i, (name, value) in enumerate(params):
            row_bg = BG_HOVER if i % 2 == 0 else BG_CARD
            row = ctk.CTkFrame(table, fg_color=row_bg, corner_radius=4, height=30)
            row.pack(fill="x", pady=1)
            row.pack_propagate(False)
            ctk.CTkLabel(row, text=name,
                         font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=FG_TEXT, width=220, anchor="w"
                         ).pack(side="left", padx=(12, 8), pady=4)
            ctk.CTkLabel(row, text=value,
                         font=ctk.CTkFont(family="Consolas", size=12),
                         text_color=FG_ACCENT, anchor="w"
                         ).pack(side="left", padx=(0, 12), fill="x", expand=True, pady=4)

    def _add_bullet_section(self, title, items, color):
        f = self._right
        card = ctk.CTkFrame(f, fg_color=BG_CARD, corner_radius=10)
        card.pack(fill="x", padx=24, pady=(6, 4))

        ctk.CTkLabel(card, text=title,
                     font=ctk.CTkFont(size=SECTION_TITLE_SZ, weight="bold"),
                     text_color=color).pack(anchor="w", padx=16, pady=(12, 4))

        for item in items:
            row = ctk.CTkFrame(card, fg_color=BG_CARD)
            row.pack(fill="x", padx=16, pady=1)
            ctk.CTkLabel(row, text="▸",
                         font=ctk.CTkFont(size=BODY_FONT_SIZE - 1), text_color=color,
                         width=22).pack(side="left", anchor="n", pady=2)
            ctk.CTkLabel(row, text=_format_body_text(item),
                         font=ctk.CTkFont(size=BODY_FONT_SIZE - 1), text_color=FG_TEXT,
                         justify="left", wraplength=BODY_WRAPLENGTH - 40, anchor="w"
                         ).pack(side="left", fill="x", expand=True, pady=2)

        # bottom padding
        ctk.CTkFrame(card, fg_color=BG_CARD, height=10).pack()

    def _add_waveform(self, spec, parent):
        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=10)
        card.pack(fill="x", padx=24, pady=(6, 8))

        ctk.CTkLabel(card, text="📈  INPUT / OUTPUT WAVEFORMS",
                     font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=FG_LINK).pack(anchor="w", padx=16, pady=(12, 4))

        try:
            fig = generate_waveform(spec)
            self._current_fig = fig
            canvas = FigureCanvasTkAgg(fig, master=card)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.configure(bg=BG_DARK, highlightthickness=0)
            widget.pack(fill="x", padx=8, pady=(0, 12))
            self._current_canvas = canvas
        except Exception as e:
            ctk.CTkLabel(card, text=f"⚠  Waveform error: {e}",
                         font=ctk.CTkFont(size=11), text_color=FG_WARN
                         ).pack(anchor="w", padx=16, pady=8)


# ── Entry point ─────────────────────────────────────────────────────
if __name__ == "__main__":
    app = AnalogTutorialApp()
    app.mainloop()
