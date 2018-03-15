import unittest

from pythomata.base.NFA import NFA
from pythomata.base.DFA import DFA
from pythomata.base.Alphabet import Alphabet
from pythomata.base.Symbol import Symbol

class TestNFA(unittest.TestCase):
    def setUp(self):
        self.a, self.b, self.c = Symbol("a"), Symbol("b"), Symbol("c")
        self.alphabet = Alphabet({self.a, self.b, self.c})
        self.states = frozenset({"s1", "s2", "s3", "s4", "s5"})
        self.initial_states = frozenset({"s1", "s4"})
        self.accepting_states = frozenset({"s3", "s2"})
        self.transition_function = {
            "s1": {
                self.b: frozenset({"s2","s3"}),
                self.c: frozenset({"s5"})
            },
            "s2": {
                self.b: frozenset({"s1"})
            },
            "s3": {
                self.b: frozenset({"s1"})
            },
            "s4":{
                self.c: frozenset({"s1"}),
                self.b: frozenset({"s1", "s5"})
            },
            "s5":{
                self.c: frozenset({"s5"}),
                self.b: frozenset({"s5"}),
                self.a: frozenset({"s5"})
            }
        }
        self.nfa = NFA(self.alphabet, self.states, self.initial_states, self.accepting_states, self.transition_function)

    def test_nfa_strings(self):
        self.nfa.to_dot("tests/automata/nfa_strings.dot")

    def test_simple_nfa_determinization(self):
        states = frozenset({"s1", "s2"})
        initial_states = frozenset({"s1"})
        accepting_states = frozenset({"s2"})
        transition_function = {
            "s1": {
                self.a: frozenset({"s1"}),
                self.b: frozenset({"s2"}),
                self.c: frozenset({"s2", "s1"}),

            },
            "s2": {
                self.a: frozenset({"s1"}),
                self.b: frozenset({"s2"}),
                self.c: frozenset({"s2", "s1"}),
            }
        }
        nfa = NFA(self.alphabet, states, initial_states, accepting_states, transition_function)
        nfa.to_dot("tests/automata/simple_nfa_strings.dot")
        dfa = NFA.determinize(nfa)
        dfa.to_dot("tests/automata/simple_nfa_strings_determinized.dot")
        dfa_trim = DFA.trim(DFA.minimize(dfa))
        dfa_trim.to_dot("tests/automata/simple_nfa_strings_minimized.dot")

    def test_nfa_determinization(self):
        dfa = NFA.determinize(self.nfa)
        dfa.to_dot("tests/automata/nfa_strings_determinized.dot")
        dfa = DFA.minimize(dfa)
        dfa = DFA.trim(dfa)
        dfa.to_dot("tests/automata/nfa_strings_determinized_minimized.dot")
