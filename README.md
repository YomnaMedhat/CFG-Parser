# CFG Parser

A Context-Free Grammar (CFG) parser that checks whether a string is accepted or rejected by a given grammar, generates leftmost derivation steps, and visualizes the parse tree.

---

## Team

| Member | Branch | Responsibility |
|--------|--------|----------------|
| Member 1 | `input-module` | Grammar input & validation |
| Member 2 | `parsing-engine` | Parsing engine & derivation |
| Member 3 | `visualization` | Parse tree & output visualization |

---

## Files

| File | Description |
|------|-------------|
| `input_module.py` | Reads and validates the CFG from the user |
| `parser_engine.py` | Recursive-descent parser, generates derivation steps |
| `tree_builder.py` | Builds the parse tree from derivation steps |
| `output_module.py` | Prints derivation steps and result to the terminal |
| `visualizer.py` | Opens a GUI window showing the parse tree |
| `main.py` | Entry point — connects all modules together |

---

## How to Run

```
python main.py
```

No external libraries required. Only Python 3 standard library is used.

---

## Input Format

```
Enter Variables (comma separated): S,A
Enter Terminals (comma separated): a,b
Enter Number of Productions: 2
Production: S -> aA | b
Production: A -> bS | ε
Enter Start Symbol: S
Enter Input String: aabb
```

> **Important:** Do not add spaces after commas when entering variables and terminals.
> Write `S,A` not `S, A` — otherwise the parser may not recognize the symbols correctly.

---

## Epsilon (ε)

The parser accepts **two ways** to write epsilon (empty string) in productions:

| Input | Meaning |
|-------|---------|
| `ε` | Copy-paste this character directly |
| `epsilon` | Type it as a word — the parser will handle it automatically |

Example:
```
Production: S -> aSb | epsilon
Production: S -> aSb | ε
```
Both are valid.

---

## Example — Accepted

Grammar: aⁿbⁿ (equal number of a's and b's)

```
Variables: S
Terminals: a,b
Productions: S -> aSb | ε
Start Symbol: S
Input String: aaabbb
```

Result: ✓ **ACCEPTED**

---

## Example — Rejected

```
Variables: S
Terminals: a,b
Productions: S -> aSb | ε
Start Symbol: S
Input String: aabbb
```

Result: ✗ **REJECTED** (number of a's does not equal number of b's)

---

## Output

The program produces two outputs:

1. **Terminal** — derivation steps and accepted/rejected result
2. **GUI window** — graphical parse tree with color-coded nodes:
   - 🟣 Purple = Variable node
   - 🟢 Green = Terminal node
   - ⬜ Gray = ε node
