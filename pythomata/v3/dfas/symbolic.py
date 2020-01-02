# -*- coding: utf-8 -*-
"""
An implementation of a symbolic automaton.

For further details, see:
- Applications of Symbolic Finite Automata, https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ciaa13.pdf
"""
from typing import Set, Dict, Union, Any

from sympy import Symbol, simplify
from sympy.logic.boolalg import BooleanFunction

from pythomata.v3.core import FiniteAutomaton, StateType

PropInt = Dict[Union[str, Symbol], bool]


class SymbolicAutomaton(FiniteAutomaton[int, PropInt]):
    """
    A symbolic automaton.

    By default, the
    """

    def __init__(self):
        """Initialize a Symbolic automaton."""
        self._initial_states = {0}
        self._n_states = 1
        self._final_states = set()  # type: Set[int]

        self._transition_function = {}  # type: Dict[int, Dict[int, BooleanFunction]]

    @property
    def states(self) -> Set[int]:
        return set(range(0, self._n_states))

    @property
    def final_states(self) -> Set[int]:
        return self._final_states

    @property
    def initial_states(self) -> Set[StateType]:
        return self._initial_states

    def get_successors(self, state: int, symbol: PropInt) -> Set[int]:
        if state not in self.states:
            raise ValueError("State not in set of states.")
        if not self._is_valid_symbol(symbol):
            raise ValueError("Symbol {} is not valid.".format(symbol))
        successors = set()
        transition_iterator = self._transition_function.get(state, {}).items()
        [successors.add(successor) for successor, guard in transition_iterator if guard.subs(symbol) == True]
        return successors

    def create_state(self) -> int:
        new_state = self._n_states
        self._n_states += 1
        return new_state

    def remove_state(self, state: int) -> None:
        if state == 0:
            raise ValueError("Cannot remove state {}".format(state))
        if state not in self.states:
            raise ValueError("State {} not found.".format(state))

        self._transition_function.pop(state, None)
        [self._transition_function[s].pop(state, None) for s in self._transition_function]
        self._n_states -= 1

    def set_final_state(self, state: int, is_final: bool) -> None:
        if state not in self.states:
            raise ValueError("State {} not found.".format(state))
        if is_final:
            self.final_states.add(state)
        else:
            try:
                self.final_states.remove(state)
            except KeyError:
                pass

    def add_transition(self, state1: int, guard: BooleanFunction, state2: int) -> None:
        assert state1 in self.states
        assert state2 in self.states
        other_guard = self._transition_function.get(state1, {}).get(state2, None)
        if other_guard is None:
            self._transition_function.setdefault(state1, {})[state2] = guard
        else:
            # take the OR of the two guards.
            self._transition_function[state1][state2] = simplify(other_guard | guard)

    def _is_valid_symbol(self, symbol: Any) -> bool:
        """Return true if the given symbol is valid, false otherwise."""
        try:
            assert isinstance(symbol, dict)
            assert all(isinstance(k, str) for k in symbol.keys())
            assert all(isinstance(v, bool) for v in symbol.values())
        except AssertionError:
            return False
        return True
