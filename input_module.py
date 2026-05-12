class CFG:
    def __init__(self):
        self.variables = []
        self.terminals = []
        self.productions = {}
        self.start_symbol = ""

# Input Functions
def read_variables():
    v = input("Enter Variables (comma separated): ")
    return [x.strip() for x in v.split(",")]

def read_terminals():
    t = input("Enter Terminals (comma separated): ")
    return [x.strip() for x in t.split(",")]

def read_productions():
    productions = {}
    n = int(input("Enter Number of Productions: "))
    print("\nFormat: S -> aA | b  (you can write 'epsilon' instead of ε)\n")
    for _ in range(n):
        rule = input("Production: ")
        if "->" not in rule:
            print("Invalid production format!")
            continue
        left, right = rule.split("->")
        left = left.strip()
        right_parts = [r.strip() for r in right.split("|")]
        # Convert the word "epsilon" to ε automatically
        right_parts = ["ε" if r.strip().lower() == "epsilon" else r.strip() for r in right_parts]
        productions[left] = right_parts
    return productions

def read_start_symbol():
    return input("Enter Start Symbol: ").strip()

def read_input_string():
    s = input("Enter Input String (type 'epsilon' for empty string): ").strip()
    # Convert the word "epsilon" to ε automatically
    if s.lower() == "epsilon":
        return "ε"
    return s

# CFG Validation
def validate_cfg(cfg):
    if cfg.start_symbol not in cfg.variables:
        print("ERROR: Start symbol not in variables.")
        return False
    for left, rights in cfg.productions.items():
        if left not in cfg.variables:
            print(f"ERROR: {left} is not a variable.")
            return False
        for prod in rights:
            if prod == "ε":
                continue
            for ch in prod:
                if (
                    ch not in cfg.variables and
                    ch not in cfg.terminals and
                    ch != "ε"
                ):
                    print(f"ERROR: Invalid symbol '{ch}'")
                    return False
    return True

# Print CFG
def print_cfg(cfg):
    print("\n===== CFG =====\n")
    print("Variables:", cfg.variables)
    print("Terminals:", cfg.terminals)
    print("\nProductions:")
    for left, right in cfg.productions.items():
        print(f"  {left} -> {' | '.join(right)}")
    print("\nStart Symbol:", cfg.start_symbol)
    print("\n================\n")

# Main CFG Reader
def read_cfg():
    cfg = CFG()
    cfg.variables = read_variables()
    cfg.terminals = read_terminals()
    cfg.productions = read_productions()
    cfg.start_symbol = read_start_symbol()
    return cfg
