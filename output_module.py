"""
output_module.py  —  Member 3: Output Formatter & Visualiser
Handles all display responsibilities:
  • Pretty derivation steps
  • ASCII parse tree
  • Accepted / Rejected banner
  • Full formatted report
"""

from __future__ import annotations
from tree_builder import ParseTreeNode


# ═══════════════════════════════════════════════════════════════════
#  ASCII Tree Printer
# ═══════════════════════════════════════════════════════════════════

class ASCIITreePrinter:
    """
    Renders a ParseTreeNode as a Unicode box-drawing tree, e.g.:

        S
        ├── a
        ├── A
        │   ├── b
        │   └── B
        │       └── ε
        └── c
    """

    BRANCH = "├── "
    LAST   = "└── "
    PIPE   = "│   "
    BLANK  = "    "

    def render(self, node: ParseTreeNode) -> str:
        lines: list[str] = []
        self._render_node(node, "", True, lines, is_root=True)
        return "\n".join(lines)

    def _render_node(
        self,
        node: ParseTreeNode,
        prefix: str,
        is_last: bool,
        lines: list[str],
        is_root: bool = False,
    ) -> None:
        if is_root:
            connector = ""
        else:
            connector = self.LAST if is_last else self.BRANCH

        lines.append(f"{prefix}{connector}{node.symbol}")

        if is_root:
            child_prefix = prefix
        else:
            child_prefix = prefix + (self.BLANK if is_last else self.PIPE)

        for idx, child in enumerate(node.children):
            child_is_last = idx == len(node.children) - 1
            self._render_node(child, child_prefix, child_is_last, lines)


# ═══════════════════════════════════════════════════════════════════
#  Derivation Formatter
# ═══════════════════════════════════════════════════════════════════

class DerivationFormatter:
    """
    Displays leftmost-derivation steps in a numbered, aligned table.
    """

    ARROW = " ⇒  "

    def render(self, steps: list[str]) -> str:
        if not steps:
            return "  (no derivation steps)"

        lines: list[str] = []
        width = len(str(len(steps)))          # digit width for step numbers
        col_w = max(len(s) for s in steps)    # widest sentential form

        for i, step in enumerate(steps):
            label = f"Step {i:{width}d}" if i > 0 else "Start  "
            arrow = self.ARROW if i > 0 else "       "
            marker = " ← start" if i == 0 else (" ← accepted ✓" if i == len(steps) - 1 else "")
            lines.append(f"  {label}  {arrow}{step:<{col_w}}{marker}")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════
#  Result Banner
# ═══════════════════════════════════════════════════════════════════

def _accepted_banner(input_string: str) -> str:
    msg = f'  String "{input_string}" — ACCEPTED ✓  '
    border = "═" * len(msg)
    return f"\n╔{border}╗\n║{msg}║\n╚{border}╝\n"


def _rejected_banner(input_string: str) -> str:
    msg = f'  String "{input_string}" — REJECTED ✗  '
    border = "═" * len(msg)
    return f"\n╔{border}╗\n║{msg}║\n╚{border}╝\n"


# ═══════════════════════════════════════════════════════════════════
#  Full Output Formatter  (main public API for Member 3)
# ═══════════════════════════════════════════════════════════════════

class OutputFormatter:
    """
    Combines the tree printer, derivation formatter, and banner
    into one cohesive final report.

    Usage
    -----
    from output_module import OutputFormatter

    formatter = OutputFormatter()
    formatter.display(
        accepted       = True,
        input_string   = "aab",
        derivation     = ["S", "aA", "aaB", "aab"],
        parse_tree_root= root_node,          # ParseTreeNode or None
    )
    """

    def __init__(self):
        self._tree_printer  = ASCIITreePrinter()
        self._deriv_fmt     = DerivationFormatter()

    # ── main display ───────────────────────────────────────────────

    def display(
        self,
        accepted: bool,
        input_string: str,
        derivation: list[str],
        parse_tree_root: ParseTreeNode | None,
    ) -> None:
        print(self._build_report(accepted, input_string, derivation, parse_tree_root))

    def get_report(
        self,
        accepted: bool,
        input_string: str,
        derivation: list[str],
        parse_tree_root: ParseTreeNode | None,
    ) -> str:
        """Return the full report as a string (useful for file export)."""
        return self._build_report(accepted, input_string, derivation, parse_tree_root)

    # ── internal builder ───────────────────────────────────────────

    def _build_report(
        self,
        accepted: bool,
        input_string: str,
        derivation: list[str],
        parse_tree_root: ParseTreeNode | None,
    ) -> str:
        parts: list[str] = []

        # 1. Result banner
        if accepted:
            parts.append(_accepted_banner(input_string))
        else:
            parts.append(_rejected_banner(input_string))

        # 2. Derivation steps
        parts.append("┌─────────────────────────────────────┐")
        parts.append("│        Leftmost Derivation           │")
        parts.append("└─────────────────────────────────────┘")
        if derivation:
            parts.append(self._deriv_fmt.render(derivation))
        else:
            parts.append("  (no derivation available)")

        # 3. Parse tree
        parts.append("")
        parts.append("┌─────────────────────────────────────┐")
        parts.append("│            Parse Tree                │")
        parts.append("└─────────────────────────────────────┘")
        if parse_tree_root is not None:
            parts.append(self._tree_printer.render(parse_tree_root))
        else:
            parts.append("  (no parse tree — string was rejected)")

        parts.append("")
        return "\n".join(parts)
