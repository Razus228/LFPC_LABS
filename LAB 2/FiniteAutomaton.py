class FiniteAutomaton:
    def __init__(self, automaton):
        self.states = automaton['states']

        self.alphabet = automaton['alphabet']

        self.transition = automaton['transition']

        self.start_state = automaton['start_state']

        self.final_states = automaton['final_states']

    def check_string(self, string):
        current_state = self.start_state

        for symbol in string:
            try:
                current_state = self.transition[current_state][symbol]
            except KeyError:
                return False

        return current_state in self.final_states

    def check_strings(self, strings):
        for string in strings:
            if self.check_string(string):
                print(f'String "{string}" is accepted by the automaton.')
            else:
                print(f'String "{string}" is rejected by the automaton.')