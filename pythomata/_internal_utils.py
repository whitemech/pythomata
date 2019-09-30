# -*- coding: utf-8 -*-
"""Internal utility functions, not supposed to be used by the users."""
import pprint
from copy import deepcopy
from typing import FrozenSet, Set, Callable, Any, Iterable, Tuple

from pythomata.base import (
    State,
    Alphabet,
    TransitionFunction,
    Symbol,
    FORBIDDEN_STATE_SYMBOLS,
    FORBIDDEN_ALPHABET_SYMBOLS,
    SINK,
    NondeterministicTransitionFunction,
)


def _check_at_least_one_state(states: Set[State]):
    """Check that the set of states is not empty."""
    if len(states) == 0:
        raise ValueError(
            "The set of states cannot be empty.".format(pprint.pformat(states))
        )


def _check_no_none_states(states: Set[State]):
    """Check that the set of states does not contain a None."""
    if any(s is None for s in states):
        raise ValueError("A state cannot be 'None'.".format(pprint.pformat(states)))


def _check_initial_state_in_states(initial_state: State, states: Set[State]):
    """Check that the initial state is in the set of states."""
    if initial_state not in states:
        raise ValueError(
            "Initial state {} not in the set of states.".format(
                pprint.pformat(initial_state)
            )
        )


def _check_accepting_states_in_states(accepting_states: Set[State], states: Set[State]):
    """Check that all the accepting states are in the set of states."""
    if not states.issuperset(accepting_states):
        wrong_accepting_states = accepting_states.difference(states)
        raise ValueError(
            "Accepting states {} not in the set of states.".format(
                pprint.pformat(wrong_accepting_states)
            )
        )


def _check_transition_function_is_valid_wrt_states_and_alphabet(
    transition_function: TransitionFunction, states: Set[State], alphabet: Alphabet
):
    """Check that a transition function is compatible with the set of states and the alphabet."""
    if len(transition_function) == 0:
        return

    extracted_states, extracted_alphabet = _extract_states_from_transition_function(
        transition_function
    )
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
                extracted_alphabet.difference(alphabet)
            )
        )


def _check_nondet_transition_function_is_valid_wrt_states_and_alphabet(
    transition_function: NondeterministicTransitionFunction,
    states: Set[State],
    alphabet: Alphabet,
):
    """Check that a non-det tr. function is compatible wrt the set of states and the alphabet."""
    if len(transition_function) == 0:
        return

    extracted_states, extracted_alphabet = _extract_states_from_nondet_transition_function(
        transition_function
    )
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
                extracted_alphabet.difference(alphabet)
            )
        )


def _check_reserved_state_names_not_used(states: Set[State]):
    """Check that the reserved names for states are not used."""
    if not all(
        reserved_name not in states for reserved_name in FORBIDDEN_STATE_SYMBOLS
    ):
        raise ValueError(
            "The following state names are reserved or invalid: {}".format(
                pprint.pformat(states.intersection(FORBIDDEN_STATE_SYMBOLS))
            )
        )


def _check_reserved_symbol_names_not_used(alphabet: Set[Symbol]):
    """Check that the reserved symbol names are not used in the alphabet."""
    if not all(
        reserved_symbol_name not in alphabet
        for reserved_symbol_name in FORBIDDEN_ALPHABET_SYMBOLS
    ):
        raise ValueError(
            "The following symbol names are reserved or invalid: {}".format(
                pprint.pformat(alphabet.intersection(FORBIDDEN_ALPHABET_SYMBOLS))
            )
        )


def _generate_sink_name(states: FrozenSet[State]):
    """Generate a sink name."""
    sink_name = SINK
    while True:
        if sink_name not in states:
            return sink_name
        sink_name = "_" + sink_name


def _extract_states_from_transition_function(
    transition_function: TransitionFunction
) -> Tuple[Set[State], Alphabet]:
    """Extract states from a transition function."""
    states, alphabet = set(), set()
    for start_state in transition_function:
        states.add(start_state)
        for symbol in transition_function[start_state]:
            end_state = transition_function[start_state][symbol]
            states.add(end_state)
            alphabet.add(symbol)

    return states, alphabet


def _extract_states_from_nondet_transition_function(transition_function):
    # type: (NondeterministicTransitionFunction) -> Tuple[Set[State], Alphabet]
    """Extract states from a non-deterministic transition function."""
    states, alphabet = set(), set()
    for start_state in transition_function:
        states.add(start_state)
        for symbol in transition_function[start_state]:
            end_states = transition_function[start_state][symbol]
            states = states.union(end_states)
            alphabet.add(symbol)

    return states, alphabet


def least_fixpoint(starting_set: Set, step: Callable[[Set], Iterable]) -> Set:
    """Do a least fixpoint algorithm."""
    z_current = None
    z_next = starting_set

    while z_current != z_next:
        z_current = z_next
        z_next = deepcopy(z_current)
        z_next = z_next.union(step(z_current))

    return z_current if z_current is not None else set()


def greatest_fixpoint(starting_set: Set, condition: Callable[[Any, Set], bool]) -> Set:
    """Do a greatest fixpoint algorithm."""
    z_current = None
    z_next = starting_set

    while z_current != z_next:
        z_current = z_next
        z_next = deepcopy(z_current)

        for e in z_current:
            if condition(e, z_current):
                z_next.remove(e)

    return z_current if z_current is not None else set()
