# -*- coding: utf-8 -*-
"""This module contains implements utilities to execute a finite automaton."""
from abc import ABC, abstractmethod
from typing import Generic, Set

from pythomata.core import StateType, SymbolType, FiniteAutomaton


class AbstractSimulator(Generic[StateType, SymbolType], ABC):
    """An interface for a simulator of finite automata."""

    @abstractmethod
    def step(self, s: SymbolType) -> StateType:
        """Make a transition, updating the current state of the simulator."""

    @abstractmethod
    def is_true(self) -> bool:
        """Check if the simulator is in a final state."""

    @abstractmethod
    def is_failed(self) -> bool:
        """Check if the simulator is failed (i.e. in an undefined state)."""

    @abstractmethod
    def reset(self) -> StateType:
        """Reset the state of the simulator to its initial state."""


class AutomatonSimulator(AbstractSimulator[Set[StateType], SymbolType]):
    """A DFA simulator."""

    def __init__(self, automaton: FiniteAutomaton):
        """
        Initialize a simulator for a finite automaton.

        :param automaton: the automaton.
        """
        self._automaton = automaton
        self._current_states = self._automaton.initial_states  # type: Set[StateType]

    @property
    def automaton(self) -> FiniteAutomaton:
        """Get the automaton."""
        return self._automaton

    @property
    def cur_state(self) -> Set[StateType]:
        """
        Get the current states of the simulator.

        :return: the index corresponding to the automaton state.
               | If None, then the simulation is in a failure state.
        """
        return self._current_states

    def step(self, symbol: SymbolType) -> Set[StateType]:
        """Do a simulation step."""
        next_macro_state = set()  # type: Set[StateType]
        for state in self.cur_state:
            next_macro_state = next_macro_state.union(
                self.automaton.get_successors(state, symbol)
            )
        return next_macro_state

    def is_true(self):
        """Check whether the simulator is in an accepting state."""
        return not self.is_failed() and any(
            s in self.automaton.final_states for s in self.cur_state
        )

    def is_failed(self) -> bool:
        """Check whether the simulator is in a failed state."""
        return self.cur_state == set()

    def reset(self) -> Set[StateType]:
        """Reset the simulator."""
        self._current_states = self.automaton.initial_states
        return self.cur_state
