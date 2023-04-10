import random

class Grammars:
    def __init__(self, productions, start_symbol):
        self.productions = productions
        self.start_symbol = start_symbol

    def generate_string(self):
        return self._generate_string(self.start_symbol)

    def _generate_string(self, symbol):
        if symbol not in self.productions:
            return symbol
        production = random.choice(self.productions[symbol])
        return ''.join(self._generate_string(s) for s in production)


    def to_finite_automaton(self):
        start_state = 0
        automatons = {start_state: {}}
        state_count = 1

        for symbol in self.productions:
            for production in self.productions[symbol]:
                current_state = start_state
                for s in production:
                    if s not in automatons[current_state]:
                        automatons[current_state][s] = state_count
                        automatons[state_count] = {}
                        state_count += 1
                    current_state = automatons[current_state][s]
                if current_state not in automatons:
                    automatons[current_state] = {}
                automatons[current_state][''] = start_state

        return automatons

    def chomsky_classification(self):
        for symbol, productions in self.productions.items():
            for production in productions:
                if len(production) == 1 and production.islower():
                    continue
                elif len(production) == 2 and production.isupper():
                    continue
                elif len(production) == 1 and production.isupper():
                    return "Type 0: Unrestricted Grammar"
                # If the production is not a pair of nonterminal symbols or a single terminal symbol, it's not in CNF
                elif len(production) != 2 or not production.isupper():
                    return "Type 1: Context-Sensitive Grammar"

        if self.start_symbol in self.productions and 'ε' in self.productions[self.start_symbol]:
            # If there are any other productions for the start symbol, the grammar is not in CNF
            if len(self.productions[self.start_symbol]) > 1:
                return "Type 2: Context-Free Grammar"
            else:
                return "Type 3: Regular Grammar"
        else:
            return "Type 2: Context-Free Grammar"

