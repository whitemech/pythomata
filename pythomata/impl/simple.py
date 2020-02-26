# -*- coding: utf-8 -*-
"""This package contains naive implementations of DFA and NFA."""
import itertools
import pprint
import queue
from copy import deepcopy, copy
from typing import Set, Dict, Tuple, FrozenSet, Iterable, cast, AbstractSet, Generic

from pythomata._internal_utils import greatest_fixpoint, least_fixpoint
from pythomata.alphabets import MapAlphabet, AlphabetLike
from pythomata.core import (
    StateType,
    SymbolType,
    Alphabet,
    DFA,
    FiniteAutomaton,
    Rendering,
    TransitionType,
)
from pythomata.utils import powerset


class SimpleDFA(
    Generic[StateType, SymbolType],
    DFA[StateType, SymbolType, SymbolType],
    Rendering[StateType, SymbolType, SymbolType],
):
    """
    Implementation of a simple DFA.

    It is a naive implementation where all the components of the DFA are
    stored explicitly.

    If the DFA is not complete (i.e. the transition function is partial),
    the successor state is None in those cases where the transition is not specified.
    """

    def __init__(
        self,
        states: Set[StateType],
        alphabet: AlphabetLike[SymbolType],
        initial_state: StateType,
        accepting_states: Set[StateType],
        transition_function: Dict[StateType, Dict[SymbolType, StateType]],
    ):
        """
        Initialize a DFA.

        :param states: the set of states.
        :param alphabet: the alphabet
        :param initial_state: the initial state
        :param accepting_states: the set of accepting states
        :param transition_function: the transition function
        """
        super().__init__()
        alphabet = (
            MapAlphabet(alphabet) if not isinstance(alphabet, Alphabet) else alphabet
        )
        self._check_input(
            states, alphabet, initial_state, accepting_states, transition_function
        )

        self._states = states
        self._alphabet = alphabet
        self._initial_state = initial_state
        self._accepting_states = accepting_states
        self._transition_function = transition_function

        self._build_indexes()

    @property
    def alphabet(self) -> Alphabet:
        """Get the alphabet."""
        return self._alphabet

    @property
    def transition_function(self) -> Dict:
        """Get the transition function."""
        return dict(self._transition_function)

    @property
    def initial_state(self) -> StateType:
        """Get the initial state."""
        return self._initial_state

    def get_successor(self, state: StateType, symbol: SymbolType) -> StateType:
        """Get the successor."""
        return self.transition_function.get(state, {}).get(symbol, None)

    @property
    def states(self) -> Set[StateType]:
        """Get the set of states."""
        return set(self._states)

    @property
    def accepting_states(self) -> Set[StateType]:
        """Get the set of accepting states."""
        return set(self._accepting_states)

    @classmethod
    def _check_input(
        cls,
        states: Set[StateType],
        alphabet: Alphabet,
        initial_state: StateType,
        accepting_states: Set[StateType],
        transition_function: Dict,
    ):
        """
        Check the consistency of the constructor parameters.

        :return: None
        :raises ValueError: if some consistency check fails.
        """
        _check_at_least_one_state(states)
        _check_no_none_states(states)
        _check_initial_state_in_states(initial_state, states)
        _check_accepting_states_in_states(accepting_states, states)
        _check_transition_function_is_valid_wrt_states_and_alphabet(
            transition_function, states, alphabet
        )

    def _build_indexes(self):
        """Build indexes for several components of the object."""
        self._idx_to_state = list(self._states)
        self._state_to_idx = dict(map(reversed, enumerate(self._idx_to_state)))
        self._idx_to_symbol = list(self._alphabet)
        self._symbol_to_idx = dict(map(reversed, enumerate(self._idx_to_symbol)))

        # state -> action -> state
        self._idx_transition_function = {
            self._state_to_idx[state]: {
                self._symbol_to_idx[symbol]: self._state_to_idx[
                    self._transition_function[state][symbol]
                ]
                for symbol in self._transition_function.get(state, {})
            }
            for state in self._states
        }

        # state -> (action, state)
        self._idx_delta_by_state = {}
        for s in self._idx_transition_function:
            self._idx_delta_by_state[s] = set(
                list(self._idx_transition_function[s].items())
            )

        self._idx_initial_state = self._state_to_idx[self._initial_state]
        self._idx_accepting_states = frozenset(
            self._state_to_idx[s] for s in self.accepting_states
        )

    def __eq__(self, other):
        """Check equality with another object."""
        if not isinstance(other, SimpleDFA):
            return False

        return (
            self._states == other.states
            and self._alphabet == other.alphabet
            and self._initial_state == other.initial_state
            and self._accepting_states == other.accepting_states
            and self._transition_function == other.transition_function
        )

    @staticmethod
    def from_transitions(initial_state, accepting_states, transition_function):
        # type: (StateType, Set[StateType], Dict[StateType, Dict[SymbolType, StateType]]) -> SimpleDFA
        """
        Initialize a DFA without explicitly specifying the set of states and the alphabet.

        :param initial_state: the initial state.
        :param accepting_states: the accepting state.
        :param transition_function: the transition function.
        :return: the DFA.
        """
        states, alphabet = _extract_states_from_transition_function(
            transition_function
        )  # type: Set[StateType], Alphabet[SymbolType]

        return SimpleDFA(
            states, alphabet, initial_state, accepting_states, transition_function
        )

    def is_complete(self) -> bool:
        """
        Check whether the automaton is complete.

        :return: True if the automaton is complete, False otherwise.
        """
        complete_number_of_transitions = len(self.states) * len(self.alphabet)
        current_number_of_transitions = sum(
            len(self._transition_function[state]) for state in self._transition_function
        )
        return complete_number_of_transitions == current_number_of_transitions

    def complete(self) -> "SimpleDFA":
        """
        Complete the DFA.

        :return: the completed DFA, if it's not already complete.
               | Otherwise, return the caller instance.
        """
        if self.is_complete():
            return self
        else:
            return self._complete()

    def _complete(self) -> "SimpleDFA":
        """
        Complete the DFA.

        :return: the completed DFA.
        """
        sink_state = _generate_sink_name(self._states)
        transitions = deepcopy(self._transition_function)

        # for every missing transition, add a transition towards the sink state.
        for state in self._states:
            for action in self._alphabet:
                cur_transitions = self._transition_function.get(state, {})
                end_state = cur_transitions.get(action, None)  # type: ignore
                if end_state is None:
                    transitions.setdefault(state, {})[action] = sink_state

        # for every action, add a transition from the sink state to the sink state
        for action in self._alphabet:
            transitions.setdefault(sink_state, {})[action] = sink_state

        return SimpleDFA(
            self.states.union({sink_state}),
            self.alphabet,
            self.initial_state,
            self.accepting_states,
            transitions,
        )

    def minimize(self) -> "SimpleDFA":
        """
        Minimize the DFA.

        :return: the minimized DFA.
        """
        dfa = self
        dfa = dfa.complete()

        def greatest_fixpoint_condition(el: Tuple[int, int], current_set: Set):
            """Condition to say whether the pair must be removed from the bisimulation relation."""
            s, t = el
            s_is_final = s in dfa._idx_accepting_states
            t_is_final = t in dfa._idx_accepting_states
            if s_is_final and not t_is_final or not s_is_final and t_is_final:
                return True

            s_transitions = dfa._idx_transition_function.get(s, {})
            t_transitions = dfa._idx_transition_function.get(t, {})

            for a, s_prime in s_transitions.items():
                t_prime = t_transitions.get(a, None)
                if t_prime is not None and (s_prime, t_prime) in current_set:
                    continue
                else:
                    return True

            for a, t_prime in t_transitions.items():
                s_prime = s_transitions.get(a, None)
                if s_prime is not None and (s_prime, t_prime) in current_set:
                    continue
                else:
                    return True

            return False

        result = greatest_fixpoint(
            set(
                itertools.product(
                    range(len(dfa._idx_to_state)), range(len(dfa._idx_to_state))
                )
            ),
            condition=greatest_fixpoint_condition,
        )

        state2equiv_class = {}  # type: Dict[int, FrozenSet[int]]
        for (s, t) in result:
            state2equiv_class.setdefault(s, frozenset())
            state2equiv_class[s] = state2equiv_class[s].union(frozenset({t}))
        equivalence_classes = set(
            map(lambda x: frozenset(x), state2equiv_class.values())
        )
        equiv_class2new_state = dict(
            (ec, i) for i, ec in enumerate(equivalence_classes)
        )

        new_transition_function = {}  # type: Dict[int, Dict[SymbolType, int]]
        for state in dfa._idx_delta_by_state:
            new_state = equiv_class2new_state[state2equiv_class[state]]
            for action, next_state in dfa._idx_delta_by_state[state]:
                new_next_state = equiv_class2new_state[state2equiv_class[next_state]]

                new_transition_function.setdefault(new_state, {})[
                    dfa._idx_to_symbol[action]
                ] = new_next_state

        new_states = frozenset(equiv_class2new_state.values())
        new_initial_state = equiv_class2new_state[
            state2equiv_class[dfa._idx_initial_state]
        ]
        new_final_states = frozenset(
            s
            for s in set(
                equiv_class2new_state[state2equiv_class[old_state]]
                for old_state in dfa._idx_accepting_states
            )
        )

        new_dfa = SimpleDFA(
            set(new_states),
            dfa.alphabet,
            new_initial_state,
            set(new_final_states),
            new_transition_function,
        )
        return new_dfa

    def reachable(self):
        """
        Get the equivalent reachable automaton.

        :return: the reachable DFA.
        """

        def reachable_fixpoint_rule(current_set: Set) -> Iterable:
            result = set()
            for el in current_set:
                for a in self._idx_transition_function.get(el, {}):
                    result.add(self._idx_transition_function[el][a])
            return result

        result = least_fixpoint({self._idx_initial_state}, reachable_fixpoint_rule)

        idx_new_states = result
        new_transition_function = {}
        for s in idx_new_states:
            for a in self._idx_transition_function.get(s, {}):
                next_state = self._idx_transition_function[s][a]
                if next_state in idx_new_states:
                    new_transition_function.setdefault(self._idx_to_state[s], {})
                    state = self._idx_to_state[s]
                    new_transition_function[state][
                        self._idx_to_symbol[a]
                    ] = self._idx_to_state[next_state]

        new_states = set(map(lambda x: self._idx_to_state[x], idx_new_states))
        new_final_states = new_states.intersection(self._accepting_states)

        return SimpleDFA(
            new_states,
            self.alphabet,
            self._initial_state,
            new_final_states,
            new_transition_function,
        )

    def coreachable(self) -> "SimpleDFA":
        """
        Get the equivalent co-reachable automaton.

        :return: the co-reachable DFA.
        """

        def coreachable_fixpoint_rule(current_set: Set) -> Iterable:
            # least fixpoint
            result = set()
            for s in range(len(self._states)):
                for a in self._idx_transition_function.get(s, {}):
                    next_state = self._idx_transition_function[s][a]
                    if next_state in current_set:
                        result.add(s)
                        break
            return result

        result = least_fixpoint(
            set(self._idx_accepting_states), coreachable_fixpoint_rule
        )

        idx_new_states = result
        if self._idx_initial_state not in idx_new_states:
            return EmptyDFA(alphabet=self.alphabet)

        new_states = set(map(lambda x: self._idx_to_state[x], idx_new_states))
        new_transition_function = (
            {}
        )  # type: Dict[StateType, Dict[SymbolType, StateType]]
        for s in idx_new_states:
            for a in self._idx_transition_function.get(s, {}):
                next_state = self._idx_transition_function[s][a]
                if next_state in idx_new_states:
                    new_transition_function.setdefault(self._idx_to_state[s], {})
                    state = self._idx_to_state[s]
                    new_transition_function[state][
                        self._idx_to_symbol[a]
                    ] = self._idx_to_state[next_state]

        return SimpleDFA(
            new_states,
            self.alphabet,
            self.initial_state,
            set(self._accepting_states),
            new_transition_function,
        )

    def trim(self) -> "SimpleDFA":
        """
        Trim the automaton.

        :return: the trimmed DFA.
        """
        dfa = self
        dfa = dfa.complete()
        dfa = dfa.reachable()
        dfa = dfa.coreachable()
        return dfa

    def levels_to_accepting_states(self) -> dict:
        """
        Return a dict from states to level.

        i.e. the number of steps to reach any accepting state.
        level = -1 if the state cannot reach any accepting state
        """
        res = {accepting_state: 0 for accepting_state in self.accepting_states}
        level = 0

        # least fixpoint
        z_current = set()  # type: Set[StateType]
        z_next = set(self.accepting_states)

        while z_current != z_next:
            level += 1
            z_current = z_next
            z_next = copy(z_current)
            for state in self._transition_function:
                for action in self._transition_function[state]:
                    if state in z_current:
                        continue
                    next_state = self._transition_function[state][action]
                    if next_state in z_current:
                        z_next.add(state)
                        res[state] = level
                        break

        z_current = z_next
        for failure_state in filter(lambda x: x not in z_current, self._states):
            res[failure_state] = -1

        return res

    def renumbering(self) -> "SimpleDFA":
        """Deterministically renumber all the states.

        :raises ValueError: if the symbols of the transitions
                          | cannot be sorted uniquely
        """
        idx = 0
        visited_states = {self._idx_initial_state}
        q = queue.Queue()  # type: queue.Queue

        old_state_to_number = {}

        q.put(self._idx_initial_state)
        while not q.empty():
            current_state = q.get()
            old_state_to_number[current_state] = idx
            idx += 1

            try:
                next_actions = sorted(
                    self._idx_transition_function[current_state],
                    key=lambda x: self._idx_to_symbol[x],
                )
            except TypeError:
                raise TypeError("Cannot sort the transition symbols.")

            for action in next_actions:
                cur_tf = self._idx_transition_function[current_state]
                next_state = cur_tf[action]
                if next_state not in visited_states:
                    visited_states.add(next_state)
                    q.put(next_state)

        new_states = set(range(len(old_state_to_number)))
        new_initial_state = old_state_to_number[self._idx_initial_state]
        new_accepting_states = {
            old_state_to_number[x] for x in self._idx_accepting_states
        }
        new_transition_function = {
            old_state_to_number[start]: {
                self._idx_to_symbol[symbol]: old_state_to_number[end]
                for symbol, end in self._idx_transition_function[start].items()
            }
            for start in self._idx_transition_function
        }

        return SimpleDFA(
            cast(Set[StateType], new_states),
            self.alphabet,
            new_initial_state,
            cast(Set[SimpleDFA], new_accepting_states),
            cast(Dict[StateType, Dict[SymbolType, StateType]], new_transition_function),
        )

    def get_transitions_from(self, state: StateType) -> AbstractSet[TransitionType]:
        """
        Get the outgoing transitions from a state.

        :param state: the starting state.
        :return: the set of transitions object associated with that triple.
                 None if it is not possible to compute such set.
        :raises ValueError: if the state does not belong to the automaton.
        """
        if state not in self.states:
            raise ValueError("The state does not belong to the automaton.")

        transitions = set()  # type: Set[TransitionType]
        for guard, end in self._transition_function.get(state, {}).items():
            transitions.add((state, guard, end))

        return transitions


class EmptyDFA(SimpleDFA):
    """Implementation of an empty DFA."""

    def __init__(self, alphabet: AlphabetLike):
        """Initialize an empty DFA."""
        super().__init__({"0"}, alphabet, "0", set(), {})

    def __eq__(self, other):
        """Check equality with another object."""
        return type(self) == type(other) == EmptyDFA


class SimpleNFA(
    Generic[StateType, SymbolType],
    Rendering[StateType, SymbolType, SymbolType],
    FiniteAutomaton[StateType, SymbolType, SymbolType],
):
    """This class implements a NFA."""

    def __init__(
        self,
        states: Set[StateType],
        alphabet: AlphabetLike[SymbolType],
        initial_state: StateType,
        accepting_states: Set[StateType],
        transition_function: Dict[StateType, Dict[SymbolType, Set[StateType]]],
    ):
        """
        Initialize a NFA.

        :param states: the set of states.
        :param alphabet: the alphabet
        :param initial_state: the initial state
        :param accepting_states: the set of accepting states
        :param transition_function: the transition function
        """
        super().__init__()
        alphabet = (
            MapAlphabet(alphabet) if not isinstance(alphabet, Alphabet) else alphabet
        )
        self._check_input(
            states, alphabet, initial_state, accepting_states, transition_function
        )

        self._states = frozenset(states)  # type: FrozenSet[StateType]
        self._alphabet = alphabet  # type: Alphabet[SymbolType]
        self._initial_state = initial_state  # type: StateType
        self._accepting_states = frozenset(
            accepting_states
        )  # type: FrozenSet[StateType]
        self._transition_function = (
            transition_function
        )  # type: Dict[StateType, Dict[SymbolType, Set[StateType]]]

        self._build_indexes()

    def _build_indexes(self):
        self._idx_to_state = sorted(self._states)
        self._state_to_idx = dict(map(reversed, enumerate(self._idx_to_state)))
        self._idx_to_symbol = sorted(self._alphabet)
        self._symbol_to_idx = dict(map(reversed, enumerate(self._idx_to_symbol)))

        # state -> action -> state
        self._idx_transition_function = {
            self._state_to_idx[state]: {
                self._symbol_to_idx[symbol]: set(
                    map(
                        lambda x: self._state_to_idx[x],
                        self._transition_function[state][symbol],
                    )
                )
                for symbol in self._transition_function.get(state, {})
            }
            for state in self._states
        }

        self._idx_initial_state = self._state_to_idx[self._initial_state]
        self._idx_accepting_states = frozenset(
            self._state_to_idx[s] for s in self._accepting_states
        )

    @classmethod
    def _check_input(
        cls,
        states: Set[StateType],
        alphabet: Alphabet[SymbolType],
        initial_state: StateType,
        accepting_states: Set[StateType],
        transition_function: Dict[StateType, Dict[SymbolType, Set[StateType]]],
    ):
        _check_at_least_one_state(states)
        _check_initial_state_in_states(initial_state, states)
        _check_accepting_states_in_states(accepting_states, states)
        _check_nondet_transition_function_is_valid_wrt_states_and_alphabet(
            transition_function, states, alphabet
        )

    @property
    def alphabet(self) -> Alphabet:
        """Get the alphabet."""
        return self._alphabet

    @property
    def states(self) -> Set[StateType]:
        """Get the states."""
        return set(self._states)

    @property
    def initial_state(self) -> StateType:
        """Get the initial state."""
        return self._initial_state

    @property
    def accepting_states(self) -> Set[StateType]:
        """Get the accepting states."""
        return set(self._accepting_states)

    @property
    def transition_function(self) -> Dict[StateType, Dict[SymbolType, Set[StateType]]]:
        """Get the transition function."""
        return self._transition_function

    def get_successors(self, state: StateType, symbol: SymbolType) -> Set[StateType]:
        """Get the successors states."""
        return self._transition_function.get(state, {}).get(symbol, set())

    def determinize(self) -> SimpleDFA:
        """
        Do determinize the NFA.

        :return: the DFA equivalent to the DFA.
        """
        nfa = self

        new_states = {macro_state for macro_state in powerset(nfa._states)}
        initial_state = frozenset([nfa._initial_state])
        final_states = {
            q for q in new_states if len(q.intersection(nfa._accepting_states)) != 0
        }
        transition_function = (
            {}
        )  # type: Dict[FrozenSet[StateType], Dict[SymbolType, FrozenSet[StateType]]]

        for state_set in new_states:
            for action in nfa.alphabet:

                next_macrostate = set()
                for s in state_set:
                    for next_state in nfa._transition_function.get(s, {}).get(
                        action, set()
                    ):
                        next_macrostate.add(next_state)

                transition_function.setdefault(state_set, {})[action] = frozenset(
                    next_macrostate
                )

        return SimpleDFA(
            new_states,
            nfa.alphabet,
            initial_state,
            set(final_states),
            transition_function,
        )

    @classmethod
    def from_transitions(cls, initial_state, accepting_states, transition_function):
        # type: (StateType, Set[StateType], Dict[StateType, Dict[SymbolType, Set[StateType]]]) -> SimpleNFA
        """
        Initialize a DFA without explicitly specifying the set of states and the alphabet.

        :param initial_state: the initial state.
        :param accepting_states: the accepting state.
        :param transition_function: the (nondeterministic) transition function.
        :return: the NFA.
        """
        states, alphabet = _extract_states_from_nondet_transition_function(
            transition_function
        )  # type: Set[StateType], Alphabet[SymbolType]

        return SimpleNFA(
            states, alphabet, initial_state, accepting_states, transition_function
        )

    def get_transitions_from(self, state: StateType) -> AbstractSet[TransitionType]:
        """
        Get the outgoing transitions from a state.

        :param state: the starting state.
        :return: the set of transitions object associated with that triple.
                 None if it is not possible to compute such set.
        :raises ValueError: if the state does not belong to the automaton.
        """
        if state not in self.states:
            raise ValueError("The state does not belong to the automaton.")

        transitions = set()  # type: Set[TransitionType]
        for guard, end_states in self._transition_function.get(state, {}).items():
            for end_state in end_states:
                transitions.add((state, guard, end_state))

        return transitions

    def __eq__(self, other):
        """Check the equality with another object."""
        if not isinstance(other, SimpleNFA):
            return False
        return (
            self.states == other.states
            and self.alphabet == other.alphabet
            and self.initial_state == other.initial_state
            and self.accepting_states == other.accepting_states
            and self.transition_function == other.transition_function
        )


def _check_at_least_one_state(states: Set[StateType]):
    """Check that the set of states is not empty."""
    if len(states) == 0:
        raise ValueError(
            "The set of states cannot be empty. Found {} instead.".format(
                pprint.pformat(states)
            )
        )


def _check_no_none_states(states: Set[StateType]):
    """Check that the set of states does not contain a None."""
    if any(s is None for s in states):
        raise ValueError("A state cannot be 'None'.")


def _check_initial_state_in_states(initial_state: StateType, states: Set[StateType]):
    """Check that the initial state is in the set of states."""
    if initial_state not in states:
        raise ValueError(
            "Initial state {} not in the set of states.".format(
                pprint.pformat(initial_state)
            )
        )


def _check_accepting_states_in_states(
    accepting_states: Set[StateType], states: Set[StateType]
):
    """Check that all the accepting states are in the set of states."""
    if not states.issuperset(accepting_states):
        wrong_accepting_states = accepting_states.difference(states)
        raise ValueError(
            "Accepting states {} not in the set of states.".format(
                pprint.pformat(wrong_accepting_states)
            )
        )


def _check_transition_function_is_valid_wrt_states_and_alphabet(
    transition_function: Dict, states: Set[StateType], alphabet: Alphabet
):
    """Check that a transition function is compatible with the set of states and the alphabet."""
    if len(transition_function) == 0:
        return

    extracted_states, extracted_alphabet = _extract_states_from_transition_function(
        transition_function
    )  # type: Set[StateType], Alphabet
    if not all(s in states for s in extracted_states):
        raise ValueError(
            "Transition function not valid: "
            "states {} are not in the set of states.".format(
                extracted_states.difference(states)
            )
        )
    if not all(s in alphabet for s in extracted_alphabet):
        raise ValueError(
            "Transition function not valid: "
            "symbols {} are not in the alphabet.".format(
                set(extracted_alphabet).difference(alphabet)
            )
        )


def _check_nondet_transition_function_is_valid_wrt_states_and_alphabet(
    transition_function: Dict, states: Set[StateType], alphabet: Alphabet[SymbolType]
):
    """Check that a non-det tr. function is compatible wrt the set of states and the alphabet."""
    if len(transition_function) == 0:
        return

    (
        extracted_states,
        extracted_alphabet,
    ) = _extract_states_from_nondet_transition_function(
        transition_function
    )  # type: Set[StateType], Alphabet[SymbolType]
    if not all(s in states for s in extracted_states):
        raise ValueError(
            "Transition function not valid: "
            "states {} are not in the set of states.".format(
                extracted_states.difference(states)
            )
        )
    if not all(s in alphabet for s in extracted_alphabet):
        raise ValueError(
            "Transition function not valid: " "some symbols are not in the alphabet."
        )


def _extract_states_from_nondet_transition_function(transition_function):
    # type: (Dict) -> Tuple[Set[StateType], Alphabet]
    """Extract states from a non-deterministic transition function."""
    states, symbols = set(), set()
    for start_state in transition_function:
        states.add(start_state)
        for symbol in transition_function[start_state]:
            end_states = transition_function[start_state][symbol]
            states = states.union(end_states)
            symbols.add(symbol)

    return states, MapAlphabet(symbols)


def _extract_states_from_transition_function(
    transition_function: Dict,
) -> Tuple[Set[StateType], Alphabet]:
    """Extract states from a transition function."""
    states, symbols = set(), set()
    for start_state in transition_function:
        states.add(start_state)
        for symbol in transition_function[start_state]:
            end_state = transition_function[start_state][symbol]
            states.add(end_state)
            symbols.add(symbol)

    return states, MapAlphabet(symbols)


def _generate_sink_name(states: Set[StateType]):
    """Generate a sink name."""
    sink_name = "sink"
    while True:
        if sink_name not in states:
            return sink_name
        sink_name = "_" + sink_name
