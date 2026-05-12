"""
visualizer.py  —  Member 3: Parse Tree GUI Visualizer
Tkinter-based graphical window that draws the parse tree
produced by tree_builder.py.

Requirements: Python 3 standard library only (tkinter is built-in).
Usage: called automatically from main.py after a successful parse.
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
from tree_builder import ParseTreeNode


# ══════════════════════════════════════════════════════════════════
#  Color scheme
# ══════════════════════════════════════════════════════════════════

COLORS = {
    "bg":           "#1E1E2E",   # dark canvas background
    "panel":        "#181825",   # sidebar / panel background
    "variable":     "#CBA6F7",   # purple  — variable nodes
    "variable_bg":  "#313244",
    "terminal":     "#A6E3A1",   # green   — terminal nodes
    "terminal_bg":  "#1E3A2F",
    "epsilon":      "#9399B2",   # gray    — ε nodes
    "epsilon_bg":   "#2A2A3D",
    "edge":         "#585B70",   # connector lines
    "text_primary": "#CDD6F4",
    "text_dim":     "#6C7086",
    "accepted":     "#A6E3A1",
    "rejected":     "#F38BA8",
    "step_arrow":   "#89DCEB",
    "highlight":    "#F5C2E7",
}

NODE_W    = 52
NODE_H    = 34
H_GAP     = 22   # horizontal gap between sibling nodes
V_GAP     = 64   # vertical gap between tree levels
MARGIN    = 40


# ══════════════════════════════════════════════════════════════════
#  Tree layout engine (Reingold-Tilford simplified)
# ══════════════════════════════════════════════════════════════════

def _layout(node: ParseTreeNode, depth: int, offset: float) -> float:
    """
    Assign (x, y) pixel coordinates to every node.
    Returns the next available x offset after this subtree.
    """
    node._depth = depth
    if not node.children:
        node._x = offset + NODE_W / 2
        node._subtree_w = NODE_W
        return offset + NODE_W + H_GAP

    cur = offset
    for child in node.children:
        cur = _layout(child, depth + 1, cur)

    left_x  = node.children[0]._x
    right_x = node.children[-1]._x
    node._x = (left_x + right_x) / 2
    node._subtree_w = cur - offset - H_GAP
    return cur


def _max_depth_and_width(node: ParseTreeNode):
    max_d = node._depth
    max_x = node._x + NODE_W / 2
    for c in node.children:
        d, x = _max_depth_and_width(c)
        if d > max_d: max_d = d
        if x > max_x: max_x = x
    return max_d, max_x


def layout_tree(root: ParseTreeNode):
    _layout(root, 0, MARGIN)
    max_depth, max_x = _max_depth_and_width(root)
    total_w = max_x + MARGIN
    total_h = (max_depth + 1) * (NODE_H + V_GAP) + MARGIN * 2
    return total_w, total_h


def node_center(node: ParseTreeNode):
    cx = node._x
    cy = node._depth * (NODE_H + V_GAP) + MARGIN + NODE_H / 2
    return cx, cy


# ══════════════════════════════════════════════════════════════════
#  Canvas drawing helpers
# ══════════════════════════════════════════════════════════════════

def _node_colors(node: ParseTreeNode, cfg):
    sym = node.symbol
    if sym == "ε":
        return COLORS["epsilon_bg"], COLORS["epsilon"], COLORS["epsilon"]
    if sym in cfg.variables:
        return COLORS["variable_bg"], COLORS["variable"], COLORS["variable"]
    return COLORS["terminal_bg"], COLORS["terminal"], COLORS["terminal"]


def _draw_tree(canvas, node: ParseTreeNode, cfg):
    cx, cy = node_center(node)
    # Draw edges to children first (so nodes draw on top)
    for child in node.children:
        chx, chy = node_center(child)
        canvas.create_line(
            cx, cy + NODE_H / 2,
            chx, chy - NODE_H / 2,
            fill=COLORS["edge"], width=1.5, smooth=True
        )
        _draw_tree(canvas, child, cfg)

    # Draw node
    fill, outline, text_color = _node_colors(node, cfg)
    x0, y0 = cx - NODE_W / 2, cy - NODE_H / 2
    x1, y1 = cx + NODE_W / 2, cy + NODE_H / 2
    canvas.create_rectangle(
        x0, y0, x1, y1,
        fill=fill, outline=outline, width=1.5,
    )
    canvas.create_text(
        cx, cy,
        text=node.symbol,
        fill=text_color,
        font=("Courier New", 12, "bold"),
    )


# ══════════════════════════════════════════════════════════════════
#  Derivation panel
# ══════════════════════════════════════════════════════════════════

def _build_derivation_panel(parent, steps: list[str], accepted: bool, input_str: str):
    frame = tk.Frame(parent, bg=COLORS["panel"], padx=16, pady=12)
    frame.pack(fill=tk.X, padx=0, pady=0)

    # Result banner
    result_text = f"  ✓  String \"{input_str}\" — ACCEPTED" if accepted \
                  else f"  ✗  String \"{input_str}\" — REJECTED"
    result_color = COLORS["accepted"] if accepted else COLORS["rejected"]

    tk.Label(
        frame, text=result_text,
        bg=COLORS["panel"], fg=result_color,
        font=("Courier New", 13, "bold"),
        anchor="w",
    ).pack(fill=tk.X, pady=(0, 10))

    if not steps:
        tk.Label(frame, text="  No derivation steps available.",
                 bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier New", 11)).pack(anchor="w")
        return

    tk.Label(
        frame, text="Leftmost Derivation",
        bg=COLORS["panel"], fg=COLORS["text_dim"],
        font=("Courier New", 10),
    ).pack(anchor="w", pady=(0, 4))

    step_frame = tk.Frame(frame, bg=COLORS["panel"])
    step_frame.pack(fill=tk.X)

    col_w = max(len(s) for s in steps)

    for i, step in enumerate(steps):
        row = tk.Frame(step_frame, bg=COLORS["panel"])
        row.pack(fill=tk.X, pady=1)

        # Step number
        lbl = "Start" if i == 0 else f"  {i:>2} "
        tk.Label(row, text=lbl, width=6,
                 bg=COLORS["panel"], fg=COLORS["text_dim"],
                 font=("Courier New", 11), anchor="e").pack(side=tk.LEFT)

        # Arrow
        arrow = "     " if i == 0 else "  ⇒  "
        tk.Label(row, text=arrow,
                 bg=COLORS["panel"], fg=COLORS["step_arrow"],
                 font=("Courier New", 11)).pack(side=tk.LEFT)

        # Sentential form
        display = step if step else "ε"
        tag_text = "  ← start" if i == 0 else ("  ← accepted ✓" if i == len(steps)-1 else "")
        tag_color = COLORS["accepted"] if i == len(steps)-1 else COLORS["text_dim"]

        tk.Label(row, text=f"{display:<{col_w}}",
                 bg=COLORS["panel"], fg=COLORS["text_primary"],
                 font=("Courier New", 11)).pack(side=tk.LEFT)

        if tag_text:
            tk.Label(row, text=tag_text,
                     bg=COLORS["panel"], fg=tag_color,
                     font=("Courier New", 10)).pack(side=tk.LEFT)


# ══════════════════════════════════════════════════════════════════
#  Legend
# ══════════════════════════════════════════════════════════════════

def _build_legend(parent):
    frame = tk.Frame(parent, bg=COLORS["panel"], padx=16, pady=8)
    frame.pack(fill=tk.X)

    tk.Label(frame, text="Legend",
             bg=COLORS["panel"], fg=COLORS["text_dim"],
             font=("Courier New", 10)).pack(anchor="w", pady=(0, 4))

    items = [
        ("■", COLORS["variable"],  "Variable node"),
        ("■", COLORS["terminal"],  "Terminal node"),
        ("■", COLORS["epsilon"],   "ε node"),
    ]
    row = tk.Frame(frame, bg=COLORS["panel"])
    row.pack(anchor="w")
    for sym, color, label in items:
        tk.Label(row, text=sym, fg=color, bg=COLORS["panel"],
                 font=("Courier New", 14)).pack(side=tk.LEFT, padx=(0, 4))
        tk.Label(row, text=label + "   ", fg=COLORS["text_dim"],
                 bg=COLORS["panel"], font=("Courier New", 10)).pack(side=tk.LEFT)


# ══════════════════════════════════════════════════════════════════
#  Main window builder  (public API)
# ══════════════════════════════════════════════════════════════════

class ParseTreeVisualizer:
    """
    Opens a Tkinter window showing:
      • Accepted / Rejected banner
      • Numbered derivation steps
      • Graphical parse tree (scrollable canvas)

    Usage
    -----
    from visualizer import ParseTreeVisualizer

    viz = ParseTreeVisualizer()
    viz.show(
        accepted        = True,
        input_string    = "aabb",
        derivation      = ["S", "aSb", "aaSbb", "aabb"],
        parse_tree_root = root_node,   # ParseTreeNode or None
        cfg             = cfg_object,  # CFG instance (needs .variables)
    )
    """

    def show(
        self,
        accepted: bool,
        input_string: str,
        derivation: list,
        parse_tree_root,
        cfg,
    ):
        root_win = tk.Tk()
        root_win.title("CFG Parse Tree Visualizer")
        root_win.configure(bg=COLORS["bg"])
        root_win.geometry("960x700")
        root_win.minsize(640, 480)

        # ── top panel: derivation steps ────────────────────────────
        top = tk.Frame(root_win, bg=COLORS["panel"],
                       relief=tk.FLAT, bd=0)
        top.pack(side=tk.TOP, fill=tk.X)

        _build_derivation_panel(top, derivation, accepted, input_string)

        sep = tk.Frame(root_win, bg=COLORS["edge"], height=1)
        sep.pack(fill=tk.X)

        # ── bottom panel: parse tree canvas ────────────────────────
        bottom = tk.Frame(root_win, bg=COLORS["bg"])
        bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        if parse_tree_root is not None:
            total_w, total_h = layout_tree(parse_tree_root)
            canvas_w = max(total_w, 800)
            canvas_h = max(total_h, 400)

            h_scroll = tk.Scrollbar(bottom, orient=tk.HORIZONTAL)
            v_scroll = tk.Scrollbar(bottom, orient=tk.VERTICAL)
            h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
            v_scroll.pack(side=tk.RIGHT,  fill=tk.Y)

            canvas = tk.Canvas(
                bottom,
                bg=COLORS["bg"],
                scrollregion=(0, 0, canvas_w, canvas_h),
                xscrollcommand=h_scroll.set,
                yscrollcommand=v_scroll.set,
                highlightthickness=0,
            )
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            h_scroll.config(command=canvas.xview)
            v_scroll.config(command=canvas.yview)

            # Mouse-wheel scroll
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind("<MouseWheel>", _on_mousewheel)

            # Draw tree
            _draw_tree(canvas, parse_tree_root, cfg)

            # Legend overlay bottom-left
            _build_legend(bottom)

        else:
            tk.Label(
                bottom,
                text="\n  No parse tree — string was rejected.\n",
                bg=COLORS["bg"], fg=COLORS["rejected"],
                font=("Courier New", 13),
            ).pack(expand=True)

        root_win.mainloop()
