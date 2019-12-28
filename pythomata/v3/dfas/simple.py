import pprint
from typing import Set, Dict, Tuple, Optional

from pythomata.v3.alphabets import MapAlphabet
from pythomata.v3.core import Alphabet, DFA, StateType, SymbolType


class SimpleDFA(DFA[StateType, SymbolType, StateType]):
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
        alphabet: Alphabet,
        initial_state: StateType,
        accepting_states: Set[StateType],
        transition_function: Dict,
    ):
        """
        Initialize a DFA.

        :param states: the set of states.
        :param alphabet: the alphabet
        :param initial_state: the initial state
        :param accepting_states: the set of accepting states
        :param transition_function: the transition function
        """
        self._check_input(
            states, alphabet, initial_state, accepting_states, transition_function
        )

        self._states = states
        self._alphabet = alphabet
        self._initial_state = initial_state
        self._accepting_states = accepting_states
        self._transition_function = transition_function

    @property
    def alphabet(self) -> Alphabet:
        """Get the alphabet."""
        return self._alphabet

    @property
    def transition_function(self) -> Dict:
        """Get the transition function."""
        return self._transition_function

    @property
    def initial_state(self) -> StateType:
        return self._initial_state

    def get_transition(self, state: StateType, symbol: SymbolType) -> Optional[StateType]:
        return self.transition_function.get(state, {}).get(symbol, None)

    def get_transition_successor(self, transition: StateType) -> StateType:
        """
        Get the successor of the transition.

        In the simple DFA implementation, the transition is the successor state itself.
        """
        return transition

    @property
    def states(self) -> Set[StateType]:
        return self._states

    @property
    def final_states(self) -> Set[StateType]:
        return self._accepting_states

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

    def __eq__(self, other):
        """Check equality with another object."""
        if not isinstance(other, SimpleDFA):
            return False

        return (
            self._states == other.states
            and self._alphabet == other.alphabet
            and self._initial_state == other.initial_state
            and self.final_states == other.final_states
            and self._transition_function == other.transition_function
        )


def _check_at_least_one_state(states: Set[StateType]):
    """Check that the set of states is not empty."""
    if len(states) == 0:
        raise ValueError(
            "The set of states cannot be empty.".format(pprint.pformat(states))
        )


def _check_no_none_states(states: Set[StateType]):
    """Check that the set of states does not contain a None."""
    if any(s is None for s in states):
        raise ValueError("A state cannot be 'None'.".format(pprint.pformat(states)))


def _check_initial_state_in_states(initial_state: StateType, states: Set[StateType]):
    """Check that the initial state is in the set of states."""
    if initial_state not in states:
        raise ValueError(
            "Initial state {} not in the set of states.".format(
                pprint.pformat(initial_state)
            )
        )


def _check_accepting_states_in_states(accepting_states: Set[StateType], states: Set[StateType]):
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
                set(extracted_alphabet).difference(alphabet)
            )
        )


def _extract_states_from_transition_function(
    transition_function: Dict
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
