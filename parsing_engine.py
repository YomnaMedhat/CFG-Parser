class ParserEngine:
    def __init__(self, cfg):
        self.cfg = cfg
        self.derivation_steps = []

    def parse_string(self, input_string):
        self.derivation_steps = []
        start_symbol = self.cfg.start_symbol
        
        print("\n--- Parsing Started ---")
        
        found = self._derive_leftmost(start_symbol, input_string, [start_symbol])

        if found:
            print("\nSTRING ACCEPTED")
            print("\n--- Leftmost Derivation Steps ---")
            print(" => ".join(self.derivation_steps))
        else:
            print("\nSTRING REJECTED")
            
        return found

    def _derive_leftmost(self, current, target, path):
        # 1. SUCCESS: If current string matches target exactly
        if current == target:
            self.derivation_steps = path
            return True

        # 2. TERMINAL CHECK: If current is all terminals but doesn't match target
        if self._is_terminal_string(current):
            return False

        # 3. PRUNING: Heuristic to prevent infinite loops
        if len(current) > len(target) + 5: 
            return False

        # 4. LEFTMOST LOGIC: Find the FIRST variable from the left
        for i, symbol in enumerate(current):
            if symbol in self.cfg.variables:
                for production in self.cfg.productions.get(symbol, []):
                    
                    if production == "ε":
                        replacement = ""
                    else:
                        replacement = production
                    
                    new_string = current[:i] + replacement + current[i+1:]

                    if self._derive_leftmost(new_string, target, path + [new_string]):
                        return True
                
                return False

        return False

    def _is_terminal_string(self, s):
        return all(symbol in self.cfg.terminals for symbol in s) or s == ""