"""
main.py  —  CFG Parser  (full integration of all 3 members)
Flow:
  Member 1  →  input_module   (grammar + string input, CLI)
  Member 2  →  parsing_engine (recursive-descent + derivation)
  Member 3  →  tree_builder   (parse tree construction)
              output_module  (CLI output: banner + derivation)
              visualizer     (Tkinter GUI: graphical parse tree)
"""

from input_module   import read_cfg, validate_cfg, print_cfg, read_input_string
from parsing_engine import ParserEngine
from tree_builder   import ParseTreeBuilder
from output_module  import OutputFormatter
from visualizer     import ParseTreeVisualizer


def main():
    # Member 1: read & validate grammar
    cfg = read_cfg()

    print("\nValidating CFG...\n")
    if not validate_cfg(cfg):
        print("CFG is INVALID — please fix the grammar and try again.")
        return

    print("CFG is VALID")
    print_cfg(cfg)

    input_string = read_input_string()
    print(f"\nInput String: \"{input_string}\"")

    # Member 2: parse + derive
    engine   = ParserEngine(cfg)
    accepted = engine.parse_string(input_string)

    # Member 3: build tree
    root = None
    if accepted and engine.derivation_steps:
        builder = ParseTreeBuilder(cfg)
        root    = builder.build(engine.derivation_steps)

    # CLI output (terminal)
    formatter = OutputFormatter()
    formatter.display(
        accepted        = accepted,
        input_string    = input_string,
        derivation      = engine.derivation_steps,
        parse_tree_root = root,
    )

    # GUI output (Tkinter window)
    viz = ParseTreeVisualizer()
    viz.show(
        accepted        = accepted,
        input_string    = input_string,
        derivation      = engine.derivation_steps,
        parse_tree_root = root,
        cfg             = cfg,
    )


if __name__ == "__main__":
    main()
