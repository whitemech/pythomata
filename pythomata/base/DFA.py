from typing import FrozenSet, Dict, Tuple, Iterable, List
import graphviz
from copy import deepcopy, copy

from pythomata.base.utils import Sink
from pythomata.base.Alphabet import Alphabet
from pythomata.base.Symbol import Symbol


def _check_same_type(i: Iterable):
    l = list(i)
    return len(l) > 0 and not all(type(l[0]) == symbol for symbol in l[1:])


class DFA(object):

    def __init__(self, alphabet: Alphabet, states: FrozenSet, initial_state, accepting_states: FrozenSet,
                 transition_function: Dict[object, Dict[Symbol, object]]):
        self._check_input(alphabet, states, initial_state, accepting_states, transition_function)

        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transition_function = transition_function

    def _check_input(self, alphabet, states, initial_state, accepting_states, transition_function):
        if initial_state and initial_state not in states:
            raise ValueError
        if any(not s in states for s in accepting_states):
            raise ValueError
        for s, sym2state in transition_function.items():
            if s not in states or any(sym not in alphabet.symbols and next_state not in states for sym, next_state in sym2state.items()):
                raise ValueError

    def complete(self):
        sink = Sink()
        transitions = copy(self.transition_function)
        for state in self.states:
            sym2state = self.transition_function.get(state, {})
            for action in self.alphabet.symbols:
                if not action in sym2state:
                    transitions.setdefault(state, {})[action]= sink

        transitions[sink] = {}
        for action in self.alphabet.symbols:
            transitions[sink][action] = sink
        return DFA(self.alphabet, self.states.union({sink}), self.initial_state, self.accepting_states,
                   dict(transitions))

    def minimize(self):
        dfa = self

        # preprocessing

        dfa = dfa.complete()
        dfa = dfa.trim()
        dfa = dfa.complete()

        # index the set of states such that avoid to deepcopy every time the states
        id2states = dict(enumerate(dfa.states))
        state2id = {v: k for k, v in id2states.items()}

        id2action = dict(enumerate(dfa.alphabet.symbols))
        action2id = {v: k for k, v in id2action.items()}

        dfa = dfa.map_states_and_action(state2id, action2id)

        # Greatest−fixpoint
        z_current = set()
        z_next = set()
        for state_s in range(len(dfa.states)):
            for state_t in range(len(dfa.states)):
                s_is_final = state_s in dfa.accepting_states
                t_is_final = state_t in dfa.accepting_states
                if s_is_final and t_is_final or (not s_is_final and not t_is_final):
                    z_next.add((state_s, state_t))

        while z_current != z_next:
            z_current = z_next
            z_next = copy(z_current)

            for (s, t) in z_current:
                skip = False
                s_transitions = dfa.transition_function.get(s, dict())
                t_transitions = dfa.transition_function.get(t, dict())

                for a, s_prime in s_transitions.items():
                    t_prime = t_transitions[a]
                    if t_prime and not (s_prime, t_prime) in z_current:
                        z_next.remove((s, t))
                        skip = True
                        break

                for a, t_prime in t_transitions.items():
                    if skip: break
                    s_prime = s_transitions[a]
                    if s_prime and not (s_prime, t_prime) in z_current:
                        z_next.remove((s, t))
                        break

        state2equiv_class = dict()
        for (s, t) in z_current:
            state2equiv_class.setdefault(s, set()).add(t)
        state2equiv_class = {k: frozenset(v) for k,v in state2equiv_class.items()}

        equivalence_classes = set(map(frozenset,state2equiv_class.values()))
        equiv_class2new_state = dict([(ec, i) for i, ec in enumerate(equivalence_classes)])

        new_transition_function = {}
        for state in dfa.transition_function:
            new_state = equiv_class2new_state[state2equiv_class[state]]
            for action, next_state in dfa.transition_function[state].items():
                new_next_state = equiv_class2new_state[state2equiv_class[next_state]]
                new_transition_function.setdefault(new_state, {})
                new_transition_function[new_state][action] = new_next_state

        new_states = frozenset(equiv_class2new_state.values())
        new_initial_state = equiv_class2new_state[state2equiv_class[dfa.initial_state]] if dfa.initial_state is not None else None
        new_final_states = frozenset(s for s in set(equiv_class2new_state[state2equiv_class[old_state]] for old_state in  dfa.accepting_states))

        new_dfa = DFA(dfa.alphabet, new_states, new_initial_state, new_final_states, new_transition_function)
        return new_dfa._numbering_states().map_states_and_action(actions_map=id2action)



    def reachable(self):

        # least fixpoint
        z_current, z_next = set(), set()
        z_next.add(self.initial_state)

        while z_current != z_next:
            z_current = z_next
            z_next = copy(z_current)
            for s in z_current:
                for a in self.transition_function.get(s, []):
                    next_state = self.transition_function[s][a]
                    z_next.add(next_state)

        new_states = z_current
        new_transition_function = {}
        for s in new_states:
            for a in self.transition_function.get(s, []):
                next_state = self.transition_function[s][a]
                if next_state in new_states:
                    new_transition_function.setdefault(s, {})
                    new_transition_function[s].setdefault(a, {})
                    new_transition_function[s][a] = next_state

        new_final_states = frozenset(new_states.intersection(self.accepting_states))

        return DFA(self.alphabet, new_states, self.initial_state, new_final_states, new_transition_function)

    def coreachable(self):
        # least fixpoint
        z_current, z_next = set(), set()
        z_next = set(self.accepting_states)

        while z_current != z_next:
            z_current = z_next
            z_next = copy(z_current)
            for state in self.states:
                for a in self.transition_function.get(state, []):
                    next_state = self.transition_function[state][a]
                    if next_state in z_next:
                        z_next.add(state)
                        break

        new_states = z_current
        new_transition_function = {}
        for s in new_states:
            for a in self.transition_function.get(s, []):
                next_state = self.transition_function[s][a]
                if next_state in new_states:
                    new_transition_function.setdefault(s, {})
                    new_transition_function[s].setdefault(a, {})
                    new_transition_function[s][a] = next_state

        if self.initial_state not in new_states:
            initial_state = None
        else:
            initial_state = self.initial_state
        return DFA(self.alphabet, new_states, initial_state, self.accepting_states, new_transition_function)

    def trim(self):
        # index the set of states such that avoid to deepcopy every time the states
        id2states = dict(enumerate(self.states))
        state2id = {v: k for k, v in id2states.items()}

        dfa = self.map_states_and_action(states_map=state2id)
        dfa = dfa.reachable()
        dfa = dfa.coreachable()
        dfa = dfa.map_states_and_action(states_map=id2states)
        dfa = dfa._numbering_states()
        return dfa


    def word_acceptance(self, word:List[Symbol]):
        assert all(char in self.alphabet.symbols for char in word)
        complete_dfa = self.complete()

        current_state = complete_dfa.initial_state
        # return false if current_state is None
        if current_state is None:
            return False

        for char in word:
            if char not in complete_dfa.transition_function.get(current_state, {}):
                return False
            else:
                current_state = complete_dfa.transition_function[current_state][char]
        return current_state in complete_dfa.accepting_states


    def to_dot(self, path, title=None):
        g = graphviz.Digraph(format='svg')
        g.node('fake', style='invisible')
        for state in self.states:
            if state == self.initial_state:
                if state in self.accepting_states:
                    g.node(str(state), root='true',
                           shape='doublecircle')
                else:
                    g.node(str(state), root='true')
            elif state in self.accepting_states:
                g.node(str(state), shape='doublecircle')
            else:
                g.node(str(state))

        g.edge('fake', str(self.initial_state), style='bold')
        for state, sym2state in self.transition_function.items():
            for sym, next_state in sym2state.items():
                g.edge(str(state),
                   str(next_state),
                   label=str(sym))

        # if not os.path.exists(path):
        #     os.makedirs(path)
        if title:
            g.attr(label=title)
            g.attr(fontsize='20')

        g.render(filename=path)
        return


    def map_states_and_action(self, states_map:dict=None, actions_map:dict=None):
        if states_map  is None: states_map  = dict()
        if actions_map is None: actions_map = dict()

        new_alphabet = Alphabet({actions_map.get(s, s) for s in  self.alphabet.symbols})
        new_states = frozenset({states_map.get(s,s) for s in self.states})
        new_accepting_states = frozenset({states_map.get(s,s) for s in self.accepting_states})
        new_initial_state = states_map.get(self.initial_state, self.initial_state)

        new_transition_function = {}
        for s, a2ns in self.transition_function.items():
            new_a2ns = {actions_map.get(a,a):states_map.get(ns, ns) for a,ns in a2ns.items()}
            new_transition_function[states_map.get(s,s)] = new_a2ns

        return DFA(new_alphabet, new_states, new_initial_state, new_accepting_states, new_transition_function)

    def map_to_int(self, states=True, actions=False):
        state2id  = {v: k for k, v in enumerate(self.states)}           if states  else dict()
        action2id = {v: k for k, v in enumerate(self.alphabet.symbols)} if actions else dict()
        return self.map_states_and_action(state2id, action2id)

    def _numbering_states(self):
        state2int = {}

        # least fixpoint
        z_current, z_next = set(), set()
        z_next.add(self.initial_state)
        state2int[self.initial_state] = 0

        old = -1
        to_be_visited = [self.initial_state]
        while old != len(state2int):
            old = len(state2int)
            for s in list(to_be_visited):
                del to_be_visited[to_be_visited.index(s)]
                for a, s_prime in self.transition_function.get(s, {}).items():
                    if s_prime not in state2int: state2int[s_prime] = len(state2int)

        for s in self.states:
            if s in state2int:
                continue
            state2int[s] = len(state2int)

        return self.map_states_and_action(states_map=state2int)


    def levels_to_accepting_states(self) -> dict:
        """Return a dict from states to level, i.e. the number of steps to reach any accepting state.
        level = -1 if the state cannot reach any accepting state"""

        res = {accepting_state: 0 for accepting_state in self.accepting_states}
        level = 0

        # least fixpoint
        z_current, z_next = set(), set()
        z_next = set(self.accepting_states)

        while z_current != z_next:
            level += 1
            z_current = z_next
            z_next = copy(z_current)
            for state in self.states:
                for a in self.transition_function.get(state, []):
                    next_state = self.transition_function[state][a]
                    if next_state in z_next:
                        z_next.add(state)
                        res[state] = level
                        break

        z_current = z_next
        for failure_state in filter(lambda x: x not in z_current, self.states):
            res[failure_state] = -1

        return res
