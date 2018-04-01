from typing import List

from pythomata.base.DFA import DFA
from pythomata.base.Symbol import Symbol


class Simulator(object):
    def __init__(self, dfa:DFA):
        self.dfa = dfa.complete()
        self.cur_state = dfa.initial_state


    def make_transition(self, s:Symbol):
        assert s in self.dfa.alphabet.symbols
        transitions = self.dfa.transition_function[self.cur_state]
        self.cur_state = transitions[s]

    def is_true(self):
        return self.cur_state in self.dfa.accepting_states

    def word_acceptance(self, word: List[Symbol]):
        for s in word:
            self.make_transition(s)
        return self.cur_state in self.dfa.accepting_states
