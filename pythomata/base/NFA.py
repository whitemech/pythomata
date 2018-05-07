from typing import FrozenSet, Dict

import graphviz

from pythomata.base.DFA import DFA
from pythomata.base.Alphabet import Alphabet
from pythomata.base.Symbol import Symbol
from pythomata.base.utils import powerset


class NFA(object):

    def __init__(self, alphabet: Alphabet, states: FrozenSet, initial_states:FrozenSet, accepting_states: FrozenSet,
                 transition_function: Dict[object, Dict[Symbol, FrozenSet]]):
        self._check_input(alphabet, states, initial_states, accepting_states, transition_function)

        self.alphabet = alphabet
        self.states = states
        self.initial_states = initial_states
        self.accepting_states = accepting_states
        self.transition_function = transition_function

    def _check_input(self, alphabet, states, initial_states, accepting_states, transition_function):
        if any(init_state not in states for init_state in initial_states):
            raise ValueError
        if any(not s in states for s in accepting_states):
            raise ValueError
        for s, sym2state in transition_function.items():
            if s not in states or any(sym not in alphabet.symbols and any(next_state not in states for next_state in next_states) for sym, next_states in sym2state.items()):
                raise ValueError


    def to_dot(self, path, title=None):
        g = graphviz.Digraph(format='svg')

        fakes = []
        for i in range(len(self.initial_states)):
            fakes.append('fake' + str(i))
            g.node('fake' + str(i), style='invisible')

        for state in self.states:
            if state in self.initial_states:
                if state in self.accepting_states:
                    g.node(str(state), root='true',
                           shape='doublecircle')
                else:
                    g.node(str(state), root='true')
            elif state in self.accepting_states:
                g.node(str(state), shape='doublecircle')
            else:
                g.node(str(state))

        for initial_state in self.initial_states:
            g.edge(fakes.pop(), str(initial_state), style='bold')
        for state, sym2states in self.transition_function.items():
            for sym, next_states in sym2states.items():
                for destination in next_states:
                    g.edge(str(state), str(destination),
                           label=str(sym))

        if title:
            g.attr(label=title)
            g.attr(fontsize='20')


        g.render(filename=path)


    def determinize(self):
        # index the set of states: we don't care too much about the states...
        id2states = dict(enumerate(self.states))
        state2id = {v: k for k, v in id2states.items()}

        id2action = dict(enumerate(self.alphabet.symbols))
        action2id = {v: k for k, v in id2action.items()}

        nfa = self.map_states_and_action(state2id, action2id)

        new_accepting_states = nfa.accepting_states

        new_states = powerset(nfa.states)
        initial_state = frozenset({s for s in nfa.initial_states})
        final_states = frozenset({q for q in new_states if len(q.intersection(new_accepting_states)) != 0})
        transition_function = {}
        for state_set in new_states:
            for action in nfa.alphabet.symbols:

                next_states = set()
                for s in state_set:
                    for s_prime in nfa.transition_function.get(s, {}).get(action, []):
                        next_states.add(s_prime)

                # next_states = set(s_prime for s in state_set for s_prime in nfa.transition_function.get(s, {}).get(action, []))

                next_states = frozenset(next_states)
                transition_function.setdefault(state_set, {})[action] = next_states

        return DFA(nfa.alphabet, new_states, initial_state, final_states, transition_function).map_states_and_action(actions_map=id2action)


    @classmethod
    def fromTransitions(cls, alphabet: Alphabet, states: FrozenSet, initial_states:FrozenSet, accepting_states: FrozenSet,
                 transitions: FrozenSet):
        transition_function = {}
        for start, action, end in transitions:
            transition_function.setdefault(start, {}).setdefault(action, set()).add(end)

        for state, sym2states in transition_function.items():
            for sym, end_states in sym2states.items():
                transition_function[state][sym] = frozenset(end_states)

        return NFA(alphabet, states, initial_states, accepting_states, transition_function)


    def map_states_and_action(self, states_map:dict=None, actions_map:dict=None):
        if states_map  is None: states_map  = dict()
        if actions_map is None: actions_map = dict()

        new_alphabet = Alphabet({actions_map.get(s, s) for s in  self.alphabet.symbols})
        new_states = frozenset({states_map.get(s,s) for s in self.states})
        new_accepting_states = frozenset({states_map.get(s,s) for s in self.accepting_states})
        new_initial_states = frozenset({states_map.get(s,s) for s in self.initial_states})

        new_transition_function = {}
        for s, a2nss in self.transition_function.items():
            new_a2nss = {actions_map.get(a,a):frozenset(states_map.get(ns, ns) for ns in nss) for a, nss in a2nss.items()}
            new_transition_function[states_map.get(s,s)] = new_a2nss

        return NFA(new_alphabet, new_states, new_initial_states, new_accepting_states, new_transition_function)

    def map_to_int(self, states=True, actions=False):
        state2id  = {v: k for k, v in enumerate(self.states)}           if states  else dict()
        action2id = {v: k for k, v in enumerate(self.alphabet.symbols)} if actions else dict()
        return self.map_states_and_action(state2id, action2id)
