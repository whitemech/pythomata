import unittest

from pythomata.base.NFA import NFA
from pythomata.base.DFA import DFA
from pythomata.base.Alphabet import Alphabet
from pythomata.base.Symbol import Symbol
from pythomata.base.utils import powerset


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

class TestNFAOnSets(unittest.TestCase):

    def test_sets(self):
        inc = Symbol("inc")
        doub = Symbol("doub")
        inc_  =  Symbol(frozenset({inc}))
        doub_ =  Symbol(frozenset({doub}))
        not_  =  Symbol(frozenset())

        initial_states = frozenset({
            frozenset({1}),
            frozenset({2})
        })
        final_states = frozenset({
            frozenset({5}),
            frozenset({6})
        })
        states = frozenset({
            frozenset({1}),
            frozenset({2}),
            frozenset({3}),
            frozenset({4}),
            frozenset({5}),
            frozenset({6}),
        })

        # as list of transitions
        transitions = frozenset({
            (frozenset({1}),    inc_,      frozenset({2})),
            (frozenset({2}),    doub_, frozenset({4})),
            (frozenset({4}),    doub_, frozenset({6})),
            (frozenset({6}),    doub_, frozenset({2})),
        })

        alphabet = Alphabet({inc_, doub_, not_})

        nfa = NFA.fromTransitions(alphabet,states,initial_states,final_states,transitions)
        nfa.to_dot("tests/automata/qui.nfa")

        dfa = nfa.determinize().minimize().trim()
        dfa.to_dot("tests/automata/qui.dfa")


    def test_ldlf_formulas(self):
        a = Symbol("a")
        tt = Symbol("TT")
        eventually_true_tt = Symbol("<true>tt")

        alphabet = {Symbol(frozenset()), Symbol(frozenset({a}))}

        delta = {
            (frozenset(), frozenset(), frozenset()),
            (frozenset(), frozenset({a}), frozenset()),
            (frozenset({eventually_true_tt}), frozenset(), frozenset({tt})),
            (frozenset({eventually_true_tt}), frozenset({a}), frozenset({tt})),
            (frozenset({tt}), frozenset(), frozenset()),
            (frozenset({tt}), frozenset({a}), frozenset()),

        }
        final_states = {frozenset(), frozenset([tt])}
        initial_state = {frozenset([eventually_true_tt])}
        states = {frozenset(), frozenset([eventually_true_tt]), frozenset([tt])}

        x = {}
        x["alphabet"] = alphabet
        x["states"] =  states
        x["initial_states"] =  initial_state
        x["accepting_states"] =  final_states
        x["transitions"] =  delta

        nfa = NFA.fromTransitions(Alphabet(x["alphabet"]), x["states"], x["initial_states"],
                              x["accepting_states"], x["transitions"])
        nfa.to_dot("tests/automata/formulas.nfa")

        transition_function = {
            frozenset(): {
                frozenset():    {frozenset()},
                frozenset({a}): {frozenset()}
            },
            frozenset({eventually_true_tt}): {
                frozenset(): {frozenset({tt})},
                frozenset({a}): {frozenset({tt})}
            },
            frozenset({tt}): {
                frozenset(): {frozenset()},
                frozenset({a}): {frozenset()}
            },
        }

        self.assertEqual(nfa.alphabet, Alphabet(alphabet))
        self.assertEqual(nfa.states, states)
        self.assertEqual(nfa.initial_states, initial_state)
        self.assertEqual(nfa.accepting_states, final_states)
        self.assertEqual(nfa.accepting_states, final_states)
        self.assertEqual(nfa.transition_function, transition_function)

        dfa = nfa.determinize()
        dfa.to_dot("tests/automata/formula_determinized.dfa")
        dfa = dfa.minimize()
        dfa.to_dot("tests/automata/formula_minimized.dfa")

    def test_sapientino_nfa(self):
        states = {0,1,2,3,4,5,6,7,8,9,10,11}
        A,B,C,b = [Symbol(s) for s in ["A","B","C","b"]]
        alphabet = Alphabet(powerset({A,B,C,b}))
        final_states = {1,4,8,3,6}
        initial_state = {0}
        transition_function = {
            (0, frozenset({}),         7),
            (0, frozenset({A}),        7),
            (0, frozenset({B}),        7),
            (0, frozenset({A,B}),      7),
            (0, frozenset({}),         5),
            (0, frozenset({A}),        5),
            (0, frozenset({B}),        5),
            (0, frozenset({A, B}),     5),
            (0, frozenset({A, B, b}),  10),
            (0, frozenset({A, B, b}),  2),
            (0, frozenset({b, A}),     1),
            (0, frozenset({b, B}),     8),

            # left
            (7, frozenset({}), 7),
            (7, frozenset({A}), 7),
            (7, frozenset({B}), 7),
            (7, frozenset({A, B}), 7),
            (7, frozenset({b, A}), 1),
            (7, frozenset({b, B}), 11),
            (7, frozenset({b, A, B}), 10),

            (1, frozenset({}), 1),
            (1, frozenset({A}), 1),
            (1, frozenset({B}), 1),
            (1, frozenset({A, B}), 1),
            (1, frozenset({b}),     1),
            (1, frozenset({b, B}), 10),

            (10, frozenset({}), 10),
            (10, frozenset({A}), 10),
            (10, frozenset({B}), 10),
            (10, frozenset({A, B}), 10),


            (11, frozenset({}), 11),
            (11, frozenset({A}), 11),
            (11, frozenset({B}), 11),
            (11, frozenset({A, B}), 11),
            (11, frozenset({b, A}), 4),

            (4, frozenset({}), 4),
            (4, frozenset({A}), 4),
            (4, frozenset({B}), 4),
            (4, frozenset({A, B}), 4),
            (4, frozenset({b}), 4),

            # right
            (5, frozenset({}), 5),
            (5, frozenset({A}), 5),
            (5, frozenset({B}), 5),
            (5, frozenset({A, B}), 5),
            (5, frozenset({b, A}), 9),
            (5, frozenset({b, B}), 8),
            (5, frozenset({b, A, B}), 2),

            (8, frozenset({}), 8),
            (8, frozenset({A}), 8),
            (8, frozenset({B}), 8),
            (8, frozenset({A, B}), 8),
            (8, frozenset({b}), 8),
            (8, frozenset({b, A}), 2),

            (2, frozenset({}), 2),
            (2, frozenset({A}), 2),
            (2, frozenset({B}), 2),
            (2, frozenset({A, B}), 2),

            (9, frozenset({}),  9),
            (9, frozenset({A}),  9),
            (9, frozenset({B}),  9),
            (9, frozenset({A, B}),  9),
            (9, frozenset({b, B}), 3),

            (3, frozenset({}), 3),
            (3, frozenset({A}), 3),
            (3, frozenset({B}), 3),
            (3, frozenset({A, B}), 3),
            (3, frozenset({b}), 3),


            # null
            (6, frozenset({}), 6),
            (6, frozenset({A}), 6),
            (6, frozenset({B}), 6),
            (6, frozenset({A, B}), 6),
            (6, frozenset({b}), 6),
            (6, frozenset({b, A}), 6),
            (6, frozenset({b, B}), 6),
            (6, frozenset({b, A,B}), 6),


        }

        nfa = NFA.fromTransitions(alphabet, states, initial_state, final_states, transition_function)
        nfa.to_dot("tests/automata/sapientino.nfa")
        nfa.determinize().map_to_int().trim().minimize().trim().to_dot("tests/automata/sapientino.dfa")
