# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import Set, FrozenSet

import graphviz

from pythomata._internal_utils import _check_at_least_one_state, _check_reserved_state_names_not_used, \
    _check_reserved_symbol_names_not_used, _check_initial_state_in_states, _check_accepting_states_in_states, \
    _check_nondeterministic_transition_function_is_valid_wrt_states_and_alphabet, \
    _extract_states_from_nondeterministic_transition_function
from pythomata.base import NondeterministicTransitionFunction, State, Symbol
from pythomata.dfa import DFA
from pythomata.utils import powerset


class NFA(object):

    def __init__(self, states: Set[State],
                 alphabet: Set[Symbol],
                 initial_state: State,
                 accepting_states: Set[State],
                 transition_function: NondeterministicTransitionFunction):
        self._check_input(states, alphabet, initial_state, accepting_states, transition_function)

        self._states = frozenset(states)  # type: FrozenSet[State]
        self._alphabet = frozenset(alphabet)  # type: FrozenSet[Symbol]
        self._initial_state = initial_state  # type: State
        self._accepting_states = frozenset(accepting_states)  # type: FrozenSet[State]
        self._transition_function = transition_function  # type: NondeterministicTransitionFunction

        self._build_indexes()

    def _build_indexes(self):
        self._idx_to_state = sorted(self._states)
        self._state_to_idx = dict(map(reversed, enumerate(self._idx_to_state)))
        self._idx_to_symbol = sorted(self._alphabet)
        self._symbol_to_idx = dict(map(reversed, enumerate(self._idx_to_symbol)))

        # state -> action -> state
        self._idx_transition_function = {
            self._state_to_idx[state]: {
                self._symbol_to_idx[symbol]:
                    set(map(lambda x: self._state_to_idx[x], self._transition_function[state][symbol]))
                for symbol in self._transition_function.get(state, {})
            }
            for state in self._states
        }

        self._idx_initial_state = self._state_to_idx[self._initial_state]
        self._idx_accepting_states = frozenset(self._state_to_idx[s] for s in self._accepting_states)

    @classmethod
    def _check_input(cls, states: Set[State],
                     alphabet: Set[Symbol],
                     initial_state: State,
                     accepting_states: Set[State],
                     transition_function: NondeterministicTransitionFunction):
        _check_at_least_one_state(states)
        _check_reserved_state_names_not_used(states)
        _check_reserved_symbol_names_not_used(alphabet)
        _check_initial_state_in_states(initial_state, states)
        _check_accepting_states_in_states(accepting_states, states)
        _check_nondeterministic_transition_function_is_valid_wrt_states_and_alphabet(transition_function, states, alphabet)

    def to_dot(self, path, title=None):
        g = graphviz.Digraph(format='svg')

        fakes = []
        fakes.append('fake' + str(self._initial_state))
        g.node('fake' + str(self._initial_state), style='invisible')

        for state in self._states:
            if state == self._initial_state:
                if state in self._accepting_states:
                    g.node(str(state), root='true',
                           shape='doublecircle')
                else:
                    g.node(str(state), root='true')
            elif state in self._accepting_states:
                g.node(str(state), shape='doublecircle')
            else:
                g.node(str(state))

        g.edge(fakes.pop(), str(self._initial_state), style='bold')
        for state, sym2state in self._transition_function.items():
            s = defaultdict(lambda: [])
            for sym, next_states in sym2state.items():
                for destination in next_states:
                    s[destination].append(sym)
                    g.edge(str(state), str(destination), label=str(sym))

            # for n in s:
            #     labels = list(map(str, sorted(s[n], key=lambda x: len(str(x)))))
            #     label_string = ""
            #     for l in labels:
            #         if len(label_string) + len(l) + len(", ") > LABEL_MAX_LENGTH:
            #             label_string += "\n"
            #         label_string += l + ", "
            #     label_string = label_string[:-2]
            #     g.edge(str(state), str(n), label=label_string)

        if title:
            g.attr(label=title)
            g.attr(fontsize='20')


        g.render(filename=path)

    def determinize(self) -> DFA:
        """Determinize the NFA

        :return: the DFA equivalent to the DFA.
        """

        nfa = self
        new_accepting_states = nfa._accepting_states

        new_states = {}
        # new_states = {macro_state for macro_state in powerset(nfa._states)}
        initial_state = frozenset([nfa._initial_state])
        # final_states = {q for q in new_states if len(q.intersection(new_accepting_states)) != 0}
        final_states = {}
        transition_function = {}

        # queue = [initial_state]
        #
        # while len(queue) == 0:
        #     cur_macrostate = queue.pop(0)
        #
        #     next_macrostate = set()
        #     for state in cur_macrostate:
        #         for action in nfa._transition_function[state]:
        #             next_macrostate.add()


        for state_set in new_states:
            for action in nfa._alphabet:

                next_state = set()
                for s in state_set:
                    for s_prime in nfa._idx_transition_function.get(s, {}).get(action, []):
                        next_state.add(s_prime)

                # next_states = set(s_prime for s in state_set for s_prime in nfa.transition_function.get(s, {}).get(action, []))

                next_state = frozenset(next_state)
                transition_function.setdefault(state_set, {})[action] = next_state

        return DFA(new_states, set(nfa._alphabet), initial_state, set(final_states), transition_function)

    @classmethod
    def from_transitions(cls, initial_state, accepting_states, transition_function):
        # type: (State, Set[State], NondeterministicTransitionFunction) -> NFA
        """
        Initialize a DFA without explicitly specifying the set of states and the alphabet.

        :param initial_state: the initial state.
        :param accepting_states: the accepting state.
        :param transition_function: the (nondeterministic) transition function.
        :return: the NFA.
        """
        states, alphabet = _extract_states_from_nondeterministic_transition_function(transition_function)

        return NFA(states, alphabet, initial_state, accepting_states, transition_function)

    def __eq__(self, other):
        if not isinstance(other, NFA):
            return False
        return self._states == other._states \
            and self._alphabet == other._alphabet \
            and self._initial_state == other._initial_state \
            and self._accepting_states == other._accepting_states \
            and self._transition_function == other._transition_function


class EmptyNFA(NFA):

    def __init__(self):
        super().__init__({"0"}, set(), "0", set(), {})
