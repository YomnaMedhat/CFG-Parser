"""
tree_builder.py  —  Member 3: Parse Tree Builder
Converts the derivation steps produced by ParserEngine into a
proper ParseTreeNode tree structure.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# ──────────────────────────────────────────────
#  Core data structure
# ──────────────────────────────────────────────

@dataclass
class ParseTreeNode:
    """One node in the parse tree."""
    symbol: str
    children: list["ParseTreeNode"] = field(default_factory=list)
    parent: Optional["ParseTreeNode"] = field(default=None, repr=False)

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def add_child(self, symbol: str) -> "ParseTreeNode":
        child = ParseTreeNode(symbol=symbol, parent=self)
        self.children.append(child)
        return child


# ──────────────────────────────────────────────
#  Tree builder
# ──────────────────────────────────────────────

class ParseTreeBuilder:
    """
    Reconstructs a parse tree from leftmost-derivation steps.

    The derivation steps list looks like:
        ["S", "aA", "aAb", "ab"]
    Each step differs from the previous by exactly one variable
    being replaced by its production.
    """

    def __init__(self, cfg):
        self.cfg = cfg

    # ── public entry point ──────────────────────────────────────────

    def build(self, derivation_steps: list[str]) -> Optional[ParseTreeNode]:
        """
        Return the root ParseTreeNode, or None if derivation is empty.
        """
        if not derivation_steps:
            return None

        root = ParseTreeNode(symbol=self.cfg.start_symbol)

        # We track 'frontier' — the ordered list of leaf nodes that
        # still correspond to symbols in the current sentential form.
        frontier: list[ParseTreeNode] = [root]

        for step_idx in range(1, len(derivation_steps)):
            prev = derivation_steps[step_idx - 1]
            curr = derivation_steps[step_idx]

            # Find which position changed (leftmost variable replaced)
            replace_pos = self._find_replaced_position(prev, curr)
            if replace_pos is None:
                # Fallback: skip this step gracefully
                continue

            # The node at replace_pos in the frontier is the variable
            # that was expanded.
            expanded_node = frontier[replace_pos]
            replaced_symbol = prev[replace_pos] if replace_pos < len(prev) else ""

            # Figure out what production was used
            new_symbols = self._production_used(prev, curr, replace_pos)

            # Attach children to the expanded node
            new_frontier_segment: list[ParseTreeNode] = []
            if new_symbols == ["ε"]:
                # ε-production: add an epsilon leaf
                child = expanded_node.add_child("ε")
                # ε leaves do NOT go into the frontier (they produce nothing)
            else:
                for sym in new_symbols:
                    child = expanded_node.add_child(sym)
                    new_frontier_segment.append(child)

            # Replace the expanded node in the frontier
            frontier = (
                frontier[:replace_pos]
                + new_frontier_segment
                + frontier[replace_pos + 1:]
            )

        return root

    # ── helpers ────────────────────────────────────────────────────

    def _find_replaced_position(
        self, prev: str, curr: str
    ) -> Optional[int]:
        """
        Return the index (character position) in `prev` where the
        leftmost variable was replaced to produce `curr`.
        """
        # Walk both strings simultaneously; the first divergence point
        # is the replacement position.
        min_len = min(len(prev), len(curr))
        for i in range(min_len):
            if prev[i] != curr[i]:
                return i
        # One is a prefix of the other — replacement is at min_len
        if len(prev) != len(curr):
            return min_len
        return None  # identical (shouldn't happen in a proper derivation)

    def _production_used(
        self, prev: str, curr: str, pos: int
    ) -> list[str]:
        """
        Given that `prev[pos]` was expanded, figure out which symbols
        were inserted in `curr` at that position.

        prev: "aAb"  curr: "aXYb"  pos: 1  →  ["X", "Y"]
        prev: "aAb"  curr: "ab"    pos: 1  →  ["ε"]  (empty production)
        """
        # Characters after the replaced symbol in prev
        suffix_prev = prev[pos + 1:]

        # Find where the suffix starts in curr
        # (everything before that is the replacement)
        if suffix_prev:
            suffix_start = curr.rfind(suffix_prev, pos)
            if suffix_start == -1:
                suffix_start = len(curr)
        else:
            suffix_start = len(curr)

        replacement_str = curr[pos:suffix_start]

        if replacement_str == "":
            return ["ε"]

        # Split the replacement string character-by-character,
        # but respect multi-character variable names from the CFG.
        return self._tokenise(replacement_str)

    def _tokenise(self, s: str) -> list[str]:
        """
        Split a string into CFG symbols (variables or terminals).
        Greedy left-to-right, longest-match on variables first.
        """
        tokens = []
        i = 0
        # Sort variables longest-first so greedy match works correctly
        vars_sorted = sorted(self.cfg.variables, key=len, reverse=True)
        while i < len(s):
            matched = False
            for var in vars_sorted:
                if s[i:].startswith(var):
                    tokens.append(var)
                    i += len(var)
                    matched = True
                    break
            if not matched:
                tokens.append(s[i])
                i += 1
        return tokens
